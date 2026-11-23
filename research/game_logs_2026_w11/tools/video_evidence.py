"""Attach defender mentions from official highlight auto-captions. Label: video (highlight transcript). refs NFL-56."""
import json, glob, re, os, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RAW = f'{OUT}/raw'
MAP = {'hsAI52kOhcw': 'ARI@KC', 'E4M4HIAfJl4': 'IND@HOU'}
if os.path.exists(f'{OUT}/video/map.json'): MAP.update(json.load(open(f'{OUT}/video/map.json')))
sb = json.load(open(f'{RAW}/scoreboard.json')); ab2id = {}
for e in sb['events']:
    for c in e['competitions'][0]['competitors']: ab2id[c['team']['abbreviation']] = c['team']['id']
KW = re.compile(r'\b(coverage|covered|covering|cover|man[- ]to[- ]man|zone|blitz\w*|beat|beats|beaten|burn\w*|broke up|breaks up|pass breakup|deflect\w*|picked|intercept\w*|over the top|in his face|on him|matched up|trailing|step on|separation|leverage|miss\w*|double|bracket\w*|safety help|cornerback|corner)\b', re.I)
ev = collections.defaultdict(lambda: collections.defaultdict(list)); md = ['# Video evidence (official NFL YouTube highlight auto-captions)', '',
     'Captions are machine-generated (ASR) broadcast commentary: names can be misspelled, and a mention near a coverage word is **not** a verified assignment. Label: `video (highlight transcript)`.', '']
for vid, game in MAP.items():
    fn = f'{OUT}/video/{vid}.json'
    if not os.path.exists(fn): continue
    x = json.load(open(fn)); away, home = game.split('@')
    md += [f'## {game}: {x["title"]}', f'URL https://www.youtube.com/watch?v={vid} | track: {x.get("track_name")} | retrieved via Firecrawl youtube-com/video_transcript', '']
    segs = x.get('segments', [])
    allln = {}
    for tm in (away, home):
        rr = json.load(open(f'{RAW}/roster_{ab2id[tm]}.json')) if os.path.exists(f'{RAW}/roster_{ab2id[tm]}.json') else {'athletes': []}
        for g in rr['athletes']:
            for a in g['items']: allln.setdefault(a['lastName'].lower(), set()).add(tm + a['displayName'])
    COMMON = {'downs', 'jones', 'johnson', 'brown', 'smith', 'williams', 'white', 'green', 'young', 'hill', 'king', 'rice', 'gray', 'long', 'moore', 'james', 'walker', 'washington', 'allen', 'carter', 'scott', 'wilson', 'davis', 'harris', 'jackson', 'thomas', 'taylor', 'baker', 'cook', 'bell', 'love', 'wright', 'lewis', 'clark', 'hunt', 'price', 'reed', 'ward', 'rush', 'pass', 'field', 'fields', 'house', 'banks', 'bush', 'stone', 'woods', 'mack', 'hicks', 'turner', 'parker', 'mitchell', 'campbell', 'evans', 'collins'}
    nocw = collections.Counter()
    for de in (away, home):
        r = json.load(open(f'{RAW}/roster_{ab2id[de]}.json')) if os.path.exists(f'{RAW}/roster_{ab2id[de]}.json') else {'athletes': []}
        names = {}
        for g in r['athletes']:
            for a in g['items']:
                if a.get('position', {}).get('abbreviation') in ('CB', 'S', 'SS', 'FS', 'LB', 'OLB', 'ILB', 'MLB', 'DB', 'NB', 'DE', 'DT', 'EDGE'):
                    names[a['lastName']] = (a['displayName'], a['position']['abbreviation'])
        for i, s in enumerate(segs):
            win = ' '.join(z['text'] for z in segs[max(0, i - 1): i + 2])
            for ln, (full, pos) in names.items():
                if len(ln) < 4: continue
                first = full.split(' ')[0]
                full_hit = re.search(re.escape(full), win, re.I)
                ambiguous = ln.lower() in COMMON or len(allln.get(ln.lower(), ())) > 1
                if ambiguous and not full_hit: continue
                if re.search(r'\b' + re.escape(ln) + r'\b', s['text'], re.I):
                    k = KW.search(win)
                    t = s['start_ms'] // 1000
                    if not k: nocw[(de, full)] += 1; continue
                    line = f'{full} ({pos}) @{t//60}:{t%60:02d} "{win.strip()[:220]}"' + (f' [coverage word: {k.group(0)}]' if k else ' [no coverage word]')
                    ev[game][de].append(line)
        md.append(f'### {de} defenders mentioned near a coverage word ({len(ev[game][de])})'); md += [f'- {l}' for l in ev[game][de]] or ['- none']
        md.append('Other mentions without a coverage word (count only): ' + (', '.join(f'{n} x{c}' for (t, n), c in nocw.items() if t == de) or 'none')); md.append('')
    kws = collections.Counter(m.group(0).lower() for m in KW.finditer(x.get('full_text', '')))
    md.append(f'Scheme words in commentary (counts, not charting): {dict(kws)}\n')
json.dump(ev, open(f'{OUT}/video/evidence.json', 'w'), indent=1)
open(f'{OUT}/VIDEO_EVIDENCE.md', 'w').write('\n'.join(md) + '\n')
print('\n'.join(md)[:4000])
