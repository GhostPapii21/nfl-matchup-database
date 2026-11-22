"""OCR for Circa betting-sheet PDFs (NFL-40 / NFL-33).

The sheets are vector glyph outlines with no text layer, plus a raster "Circa" watermark. Pipeline:
  1. delete the raster images (watermark, logo) and render the page at 600 dpi;
  2. connected components -> glyphs (pieces that overlap in x and touch in y are one glyph, so "1/2" is one glyph);
  3. glyphs -> words (same text band, gap under half the glyph height);
  4. tesseract reads every word (full charset and a numeric whitelist);
  5. numeric glyphs are then classified by pixel templates bootstrapped from the words tesseract read cleanly. This is
     what reads the fraction "1/2", which tesseract misses or reads as 1 or 4. The font is one fixed vector font, so
     every copy of a glyph renders the same.
Needs pymupdf, numpy, scipy, Pillow and the tesseract binary. No network.
"""
from __future__ import annotations

import shutil, subprocess, tempfile
from dataclasses import dataclass, asdict, field
from pathlib import Path

DPI = 600
SCALE = DPI / 72.0
GRID = (24, 16)          # template grid rows x cols
NUMCH = "0123456789+-½"
MAX_DIST = 0.22          # template distance above this -> glyph unreadable ("?")


@dataclass
class Token:
    page: int
    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    ocr_full: str = ""
    ocr_num: str = ""
    glyphs: int = 0
    max_glyph_dist: float | None = None
    method: str = ""

    @property
    def yc(self):
        return (self.y0 + self.y1) / 2

    @property
    def xc(self):
        return (self.x0 + self.x1) / 2

    @property
    def h(self):
        return self.y1 - self.y0

    def as_dict(self):
        return asdict(self)


def available() -> bool:
    try:
        import pymupdf, numpy, scipy  # noqa: F401
    except ImportError:
        return False
    return shutil.which("tesseract") is not None


def _render(page):
    import numpy as np, pymupdf
    for img in page.get_images(full=True):
        page.delete_image(img[0])
    pix = page.get_pixmap(dpi=DPI, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
    return a


def _glyphs(ink):
    """-> list of [r0, c0, r1, c1] (inclusive-exclusive) glyph boxes in pixels."""
    from scipy import ndimage
    lab, n = ndimage.label(ink, structure=[[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    boxes = [[s[0].start, s[1].start, s[0].stop, s[1].stop] for s in ndimage.find_objects(lab) if s is not None]
    boxes = [b for b in boxes if (b[2] - b[0]) * (b[3] - b[1]) >= 4]
    # long rules / table lines are not glyphs
    boxes = [b for b in boxes if (b[3] - b[1]) < 40 * SCALE and not ((b[3] - b[1]) > 12 * (b[2] - b[0]) and (b[3] - b[1]) > 15 * SCALE)]
    boxes.sort(key=lambda b: b[1])
    merged = True
    while merged:
        merged, out = False, []
        for b in boxes:
            for o in out:
                xo = min(o[3], b[3]) - max(o[1], b[1])
                narrow = min(o[3] - o[1], b[3] - b[1])
                h = max(o[2] - o[0], b[2] - b[0])
                yg = max(o[0], b[0]) - min(o[2], b[2])
                if xo > 0.3 * narrow and yg < 0.25 * h and xo > 0:
                    o[:] = [min(o[0], b[0]), min(o[1], b[1]), max(o[2], b[2]), max(o[3], b[3])]
                    merged = True
                    break
            else:
                out.append(list(b))
        boxes = sorted(out, key=lambda b: b[1])
    return boxes


def _words(glyphs):
    """group glyph boxes into words: next glyph to the right, inside the word's text band, gap < 0.5 band height."""
    used, words = [False] * len(glyphs), []
    order = sorted(range(len(glyphs)), key=lambda i: glyphs[i][1])
    for i in order:
        if used[i]:
            continue
        used[i] = True
        w = [i]; band = list(glyphs[i][::2])  # [r0, r1]
        right = glyphs[i][3]
        while True:
            best = None
            for j in order:
                if used[j]:
                    continue
                g = glyphs[j]
                if g[1] < right - 2 or g[1] - right > 0.5 * max(band[1] - band[0], g[2] - g[0]):
                    continue
                bh, gh = band[1] - band[0], g[2] - g[0]
                inside = g[0] >= band[0] - 0.15 * bh and g[2] <= band[1] + 0.15 * bh
                descender = band[0] <= g[0] < band[0] + 0.5 * bh and g[2] <= band[1] + 0.5 * bh and gh > 0.6 * bh
                inside = inside or descender
                covers = band[0] >= g[0] - 0.15 * gh and band[1] <= g[2] + 0.15 * gh
                last = glyphs[w[-1]]
                sign_next = gh < 0.6 * bh
                sign_last = (last[2] - last[0]) < 0.6 * bh
                if sign_next and not sign_last and g[1] - right > 0.3 * bh:
                    continue   # "-1/2 +125": a sign after a digit with a gap starts a new number
                if inside or covers:
                    if best is None or g[1] < glyphs[best][1]:
                        best = j
            if best is None:
                break
            used[best] = True; w.append(best)
            g = glyphs[best]; band = [min(band[0], g[0]), max(band[1], g[2])]; right = max(right, g[3])
        words.append([glyphs[k] for k in w])
    return words


def _vec(ink, g, band):
    """glyph pixels inside its word band -> fixed grid (keeps vertical position so '-' differs from '_')."""
    import numpy as np
    from PIL import Image
    r0, r1 = band
    sub = ink[r0:r1, g[1]:g[3]].astype(np.uint8) * 255
    im = Image.fromarray(sub).resize((GRID[1], GRID[0]), Image.BILINEAR)
    v = (np.asarray(im) > 96).astype(np.float32).ravel()
    aspect = (g[3] - g[1]) / max(1, r1 - r0)
    return v, aspect


def _tess(crops, whitelist=None, batch=120):
    from PIL import Image
    out = []
    for i in range(0, len(crops), batch):
        part = crops[i:i + batch]
        gap = 40
        W = max(c.width for c in part) + 80
        H = sum(c.height + gap for c in part) + gap
        canvas = Image.new("L", (W, H), 255)
        y, spans = gap, []
        for c in part:
            canvas.paste(c, (40, y)); spans.append((y, y + c.height)); y += c.height + gap
        with tempfile.TemporaryDirectory() as td:
            fn = Path(td) / "s.png"; canvas.save(fn)
            cmd = ["tesseract", str(fn), "-", "--psm", "4"]
            if whitelist:
                cmd += ["-c", "tessedit_char_whitelist=" + whitelist]
            cmd += ["tsv"]
            tsv = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        words = []
        for line in tsv.splitlines()[1:]:
            f = line.split("\t")
            if len(f) == 12 and f[0] == "5" and f[11].strip():
                words.append((int(f[7]) + int(f[9]) / 2, int(f[6]), f[11].strip()))
        for (a, b) in spans:
            ws = sorted((x, t) for (yc, x, t) in words if a - gap / 2 <= yc < b + gap / 2)
            out.append(" ".join(t for _, t in ws))
    return out


def page_tokens(page, pno: int):
    import numpy as np
    from PIL import Image
    gray = _render(page)
    ink = gray < 140
    words = _words(_glyphs(ink))
    crops = []
    for w in words:
        r0 = min(g[0] for g in w); r1 = max(g[2] for g in w); c0 = min(g[1] for g in w); c1 = max(g[3] for g in w)
        pad = 12
        sub = gray[max(0, r0 - pad):r1 + pad, max(0, c0 - pad):c1 + pad]
        im = Image.fromarray(np.ascontiguousarray(sub))
        im = im.resize((max(1, int(im.width * 64 / im.height)), 64))
        crops.append(im)
    full = _tess(crops)
    num = _tess(crops, whitelist="0123456789+-EVN")
    # bootstrap glyph templates from cleanly read numeric words
    samples = {}
    for w, rf, rn in zip(words, full, num):
        t = rn.replace(" ", "")
        if not t or any(ch not in "0123456789+-" for ch in t) or sum(c.isalpha() for c in rf) >= 2:
            continue
        band = (min(g[0] for g in w), max(g[2] for g in w))
        if len(t) == len(w):
            labels = list(t)
        elif len(t) + 1 == len(w):
            labels = list(t) + ["½"]
        else:
            continue
        for g, ch in zip(w, labels):
            samples.setdefault(ch, []).append(_vec(ink, g, band))
    protos = {}
    for _ in range(2):   # build, then rebuild from majority-consistent samples
        protos = {ch: (np.mean([v for v, a in s], axis=0), float(np.median([a for v, a in s]))) for ch, s in samples.items() if len(s) >= 2}
        if not protos:
            break
        clean = {}
        for ch, s in samples.items():
            for v, a in s:
                best = min(protos, key=lambda k: float(np.mean(np.abs(protos[k][0] - v))) + 0.5 * abs(protos[k][1] - a))
                if best == ch:
                    clean.setdefault(ch, []).append((v, a))
        samples = clean or samples
    toks = []
    for w, rf, rn in zip(words, full, num):
        r0 = min(g[0] for g in w); r1 = max(g[2] for g in w); c0 = min(g[1] for g in w); c1 = max(g[3] for g in w)
        box = (c0 / SCALE, r0 / SCALE, c1 / SCALE, r1 / SCALE)
        letters = sum(c.isalpha() for c in rf)
        tn = rn.replace(" ", "")
        rf_letters = "".join(c for c in rf.upper() if c.isalpha())
        if rf_letters in ("EVEN", "EV") or (tn in ("EVEN", "EV") and rf_letters and set(rf_letters) <= set("EVN")):
            text, dist, method = "EVEN", None, "tesseract"
        elif (letters >= 2 and not (rf[:1] and rf[0] in "+-")) or not protos:
            text, dist, method = rf, None, "tesseract"
        else:
            band = (r0, r1); chars, dists = [], []
            for g in w:
                v, a = _vec(ink, g, band)
                scored = sorted((float(np.mean(np.abs(p - v))) + 0.5 * abs(pa - a), ch) for ch, (p, pa) in protos.items())
                d, ch = scored[0]
                chars.append(ch if d <= MAX_DIST else "?"); dists.append(d)
            text, dist, method = "".join(chars), round(max(dists), 3), "template"
            if "½" in text[:-1]:
                text = "?" + text
        toks.append(Token(pno, *[round(x, 2) for x in box], text=text, ocr_full=rf, ocr_num=rn, glyphs=len(w),
                          max_glyph_dist=dist, method=method))
    toks.sort(key=lambda t: (round(t.yc), t.x0))
    return toks


def pdf_tokens(path):
    import pymupdf
    doc = pymupdf.open(str(path))
    out = []
    for i, page in enumerate(doc):
        out.extend(page_tokens(page, i + 1))
    return out
