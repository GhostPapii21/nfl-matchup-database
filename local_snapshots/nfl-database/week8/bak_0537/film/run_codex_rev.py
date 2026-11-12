import json,glob,subprocess,os
from concurrent.futures import ThreadPoolExecutor
def do(f):
    g=json.load(open(f)); gid=g['gid']; out=f'codex_out/{gid}.json'
    if os.path.exists(out) or not g.get('yt',{}).get('captions'): return
    cap=open(g['yt']['captions']).read()
    p=f"""You are reviewing an NFL highlight video via its auto-generated CAPTIONS ONLY (broadcast commentary audio). You cannot see video frames. Game: {g['score']} (2026 Week {g['week']}, game_id {gid}). Video: {g['yt']['title']} {g['yt']['url']}

Authoritative DB play-by-play (scoring plays, plays >=20 yds, turnovers):
{chr(10).join(g['key_plays'])}

Captions (timestamps = position in video):
{cap}

Task: list every highlight play you can identify in the captions. For each: caption_ts (from captions), team (abbr on offense), player, description, yards, is_score, concept (run gap/direction, play-action, screen, deep shot, RPO, etc. ONLY if the commentary says it or the DB text shows it, else 'unknown'), personnel_formation and coverage_scheme ONLY if commentators explicitly state it else 'unknown', defender_beaten (named in commentary or DB tackler text, else 'unknown'), db_match = the exact matching DB play line (copy 'Q# clock') or 'NO DB MATCH'. Captions are auto-generated and mangle names; use the DB to correct names only when the play clearly matches. Then team_notes for both teams: offensive strengths/patterns and defensive weaknesses supported by the plays above (no generic claims). limitations: what you could not determine. Never invent. Do not run any commands; answer from this prompt."""
    r=subprocess.run(['codex','exec','--skip-git-repo-check','-s','read-only','-c','model_reasoning_effort="low"','--output-schema','schema.json','-o',out,'-'],input=p,capture_output=True,text=True,timeout=900)
    if r.returncode: open(f'codex_out/{gid}.err','w').write(r.stderr[-3000:])
with ThreadPoolExecutor(8) as ex: list(ex.map(do,sorted(glob.glob("games/*.json"),reverse=True)))
print(len(glob.glob('codex_out/*.json')))
