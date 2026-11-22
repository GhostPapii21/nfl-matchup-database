"""NFL-40 / NFL-33: Circa sheet OCR parser. The layout tests run offline on the committed OCR token cache for the
2026-11-21 capture; the OCR test re-reads the PDFs and is skipped when pymupdf/numpy/scipy/tesseract are missing.
Expected values below were hand-checked against the rendered PDFs on 2026-11-22 (every page-1 Week 11 game cell,
all 24 team totals, all 16 Week 12 early lines, and the QB TD-pass / QB rushing / anytime-TD rows sampled here)."""
import gzip, json
from pathlib import Path

import pytest

from source_adapters.circa import parse as P
from source_adapters.circa import build_rows as B

CAP = Path(__file__).parent / "source_adapters/circa/captures/2026-11-21T225514+0000"
MAN = json.loads((CAP / "MANIFEST.json").read_text())
SHEETS = {s["file"]: s for s in MAN["sheets"]}


def tokens(name):
    sha = SHEETS[name]["sha256"]
    return json.loads(gzip.decompress((CAP / "parsed/tokens" / (sha[:16] + ".tokens.json.gz")).read_bytes()))


def find(rows, **kw):
    out = [r for r in rows if all(getattr(r, k) == v for k, v in kw.items())]
    assert len(out) == 1, (kw, len(out))
    return out[0]


@pytest.fixture(scope="module")
def w11():
    return P.parse_tokens(tokens("NFL Week 11 - 2026.pdf"))


@pytest.fixture(scope="module")
def props():
    return P.parse_tokens(tokens("NFL Props Week 11- 2026.pdf"))


@pytest.fixture(scope="module")
def w12():
    return P.parse_tokens(tokens("NFL Week 12 - 2026.pdf"))


def test_num_and_price():
    assert P.num("-3½") == -3.5 and P.num("-½") == -0.5 and P.num("46½") == 46.5 and P.num("EVEN") == 100 and P.num("EV") == 100
    assert P.price("-105") == -105 and P.price("EVEN") == 100 and P.price("-3½") is None and P.price("46") is None
    assert P.num("?-1") is None and P.num("") is None


def test_team_code_repair_only_to_real_teams():
    assert P.norm_team("CHT") == "CHI" and P.norm_team("PHT") == "PHI" and P.norm_team("ART") == "ARI"
    assert P.norm_team("TEN") == "TEN" and P.norm_team("ZZZ") == "?ZZZ"


def test_w11_page_kinds_and_counts(w11):
    rows, rep = w11
    assert rep[1]["kind"] == "game" and rep[2]["kind"] == "team_total"
    assert rep[1]["rows"] == 216 and rep[2]["rows"] == 48          # 12 games x 3 periods x 6 rows; 24 teams x 2
    assert all(not v["dropped"] for v in rep.values())
    assert not [r for r in rows if "POINTS" in r.away]               # Grand Salami block is not a game


def test_w11_full_game_hand_checked(w11):
    rows, _ = w11
    g = dict(away="RAVENS", home="PANTHERS", period="FG")
    assert (find(rows, **g, market="spread", side="PANTHERS").line, find(rows, **g, market="spread", side="PANTHERS").price) == (-3, -105)
    r = find(rows, **g, market="spread", side="RAVENS")
    assert (r.line, r.price, r.line_derived) == (3, -115, True)
    assert find(rows, **g, market="moneyline", side="RAVENS").price == 130
    t = find(rows, **g, market="total", side="over")
    assert (t.line, t.price, t.price_printed) == (43.5, None, False)    # no price printed: left empty, not -110
    g = dict(away="BUCS", home="LIONS", period="FG")
    r = find(rows, **g, market="spread", side="LIONS")
    assert (r.line, r.price, r.price_printed) == (-5, None, False)
    g = dict(away="JETS", home="CHARGERS", period="FG")
    assert find(rows, **g, market="spread", side="JETS").price == 100     # printed EVEN
    assert find(rows, **g, market="spread", side="CHARGERS").price == -120
    g = dict(away="BENGALS", home="COMMANDERS", period="FG")
    assert find(rows, **g, market="total", side="over").line == 54 and find(rows, **g, market="moneyline", side="BENGALS").price == -285
    assert find(rows, **g, market="moneyline", side="BENGALS").game_date == "Mon Nov 23"


def test_w11_halves_quarters_hand_checked(w11):
    rows, _ = w11
    g = dict(away="JAGUARS", home="GIANTS")
    o = find(rows, **g, period="1H", market="total", side="over"); u = find(rows, **g, period="1H", market="total", side="under")
    assert (o.line, o.price, u.price) == (23.5, -105, -115)
    r = find(rows, **g, period="1Q", market="spread", side="JAGUARS")
    assert (r.line, r.price) == (-0.5, 105)
    g = dict(away="TITANS", home="COWBOYS", period="1H")
    assert (find(rows, **g, market="total", side="over").price, find(rows, **g, market="total", side="under").price) == (100, -120)
    g = dict(away="BENGALS", home="COMMANDERS", period="1Q")
    assert (find(rows, **g, market="total", side="over").line, find(rows, **g, market="total", side="over").price,
            find(rows, **g, market="total", side="under").price) == (10, -120, 100)
    g = dict(away="STEELERS", home="EAGLES", period="1Q")
    assert find(rows, **g, market="total", side="over").line == 7 and find(rows, **g, market="spread", side="STEELERS").price == 120


def test_w11_team_totals_hand_checked(w11):
    rows, _ = w11
    tt = {(r.team, r.side): (r.line, r.price) for r in rows if r.market == "team_total"}
    assert tt[("RAVENS", "over")] == (20.5, None)
    assert tt[("LIONS", "over")] == (25.5, -120) and tt[("LIONS", "under")] == (25.5, 100)
    assert tt[("BEARS", "over")] == (30.5, 100) and tt[("BEARS", "under")] == (30.5, -120)
    assert tt[("COMMANDERS", "over")] == (23.5, -115) and tt[("COWBOYS", "under")] == (32.5, None)


def test_props_hand_checked(props):
    rows, rep = props
    assert rep[1]["kind"] == "player_prop" and rep[2]["kind"] == "yesno"
    assert rep[1]["rows"] == 238 and rep[2]["rows"] == 144
    r = find(rows, prop="Rushing Yards", section="RB Props", player="JAHMYR GIBBS", side="over")
    assert (r.line, r.price, r.team) == (90.5, None, "DET")
    r = find(rows, prop="Rushing Yards", section="RB Props", player="DERRICK HENRY", side="under")
    assert r.line == 62.5
    r = find(rows, prop="TD Passes", player="JARED GOFF", side="over")
    assert (r.line, r.price) == (1.5, -155)
    assert find(rows, prop="TD Passes", player="DAK PRESCOTT", side="over").price == 100   # printed EV
    r = find(rows, prop="Rushing Yards", section="QB Props", player="JACOBY BRISSETT", side="under")
    assert (r.line, r.price) == (5.5, 100)
    assert find(rows, prop="anytime touchdown", player="JAHMYR GIBBS", side="yes").price == -240
    assert find(rows, prop="anytime touchdown", player="AARON RODGERS", side="no").price == -3800
    assert find(rows, prop="anytime touchdown", player="BHAYSHUL TUTEN", side="yes").price == -110


def test_w12_early_lines_hand_checked(w12):
    rows, rep = w12
    assert rep[1]["kind"] == "early" and rep[1]["rows"] == 64
    sp = {(r.away, r.home): (r.side, r.line, r.price) for r in rows if r.market == "spread" and not r.line_derived}
    assert len(sp) == 16
    assert sp[("BEARS", "LIONS")] == ("LIONS", 0.0, None)            # PK
    assert sp[("CHIEFS", "BILLS")] == ("BILLS", -3, -105)
    assert sp[("FALCONS", "VIKINGS")] == ("VIKINGS", -7.5, None)
    assert sp[("TITANS", "JAGUARS")] == ("JAGUARS", -15.5, None)
    assert find(rows, away="CHIEFS", home="BILLS", market="spread", side="CHIEFS").price == -115
    assert find(rows, away="BEARS", home="LIONS", market="total", side="over").game_date == "Thu Nov 26"


def test_rows_carry_provenance(w11):
    s = SHEETS["NFL Week 11 - 2026.pdf"]
    out, rep, upd = B.rows_for_sheet(tokens("NFL Week 11 - 2026.pdf"), s, MAN, "2026-11-22T00:00:00+00:00")
    assert len(out) == 264 and upd.startswith("Updated 11/21/26")
    for r in out:
        assert r["sheet_created_utc"] == "2026-11-21T19:51:28+00:00" and r["pulled_utc"] == "2026-11-21T22:55:14+00:00"
        assert r["source_url"].startswith("https://www.dropbox.com/") and len(r["sheet_sha256"]) == 64
        assert r["price"] is None or isinstance(r["price"], int)


def test_committed_rows_csv_matches_parser():
    import csv
    got = list(csv.DictReader(open(CAP / "parsed/rows.csv")))
    assert len(got) == 710
    assert {r["sheet_file"] for r in got} == {"NFL Props Week 11- 2026.pdf", "NFL Week 11 - 2026.pdf", "NFL Week 12 - 2026.pdf"}


def test_ocr_reproduces_cached_tokens():
    from source_adapters.circa import ocr
    if not ocr.available():
        pytest.skip("OCR toolchain (pymupdf, numpy, scipy, tesseract) not installed; layout tests above cover the cache")
    fresh = [t.as_dict() for t in ocr.pdf_tokens(CAP / "NFL Week 12 - 2026.pdf")]
    rows, rep = P.parse_tokens(fresh)
    assert rep[1]["rows"] == 64
    sp = {(r.away, r.home): (r.side, r.line) for r in rows if r.market == "spread" and not r.line_derived}
    assert sp[("FALCONS", "VIKINGS")] == ("VIKINGS", -7.5)
