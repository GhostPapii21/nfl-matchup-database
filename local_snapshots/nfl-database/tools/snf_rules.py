"""SNF PHI@WSH postmortem rules (postmortems/2026-11-01_snf.md). Rico approved Nov 2, 8:14 AM ET; MNF start + WR3 exception Rico card Nov 2, 8:19 AM ET; WR3 targets floor 8:20 AM ET. Runs dated >= SNF_FROM.
S1 model-suspect under -> MANUAL_REVIEW (any tier) only with a documented backfield split + D/F (or weak) backup-QB card.
S2 WR3+ UNDER may satisfy the named-defender check with the team coverage profile (man_zone + mof); flag WR3_TEAM_COV.
S3 questionable WR unconfirmed at inactives -> target shares rerun both ways (active / inactive), both reported.
S4 opponent missing 2+ CBs (starters/nickel) -> WR2/WR3 overs join the candidate pool (leg or skip_reason each).
   EXCEPTION (Rico 8:19/8:20 AM ET): with 2+ CBs out, a WR3 over may publish if it clears every other normal gate
   (§7, edge/models, coverage, weather, inactives, §11, opportunity check not 'mixed') AND averages 4+ targets/game
   over his last 4 games with the current QB (leg field tpg_last4_cur_qb). Flag WR3_DEPLETED_SECONDARY_EXCEPTION;
   4.0-4.9 tpg also WR3_TARGETS_BORDERLINE, 5+ full. <4 tpg: falls to DEPTH_RECEIVER. WR4 overs: DEPTH_RECEIVER (rules/rulebook.py).
   Outside the condition WR3/WR4 overs need the DEPTH_RECEIVER rule (replaced the old ban, Rico 2026-11-02 23:59)."""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules import rulebook as _rb
SNF_FROM = _rb.rule("SNF")["effective"]   # from rules/rulebook.py
EXC_FLAG, BORDER_FLAG, TPG_MIN, TPG_FULL = "WR3_DEPLETED_SECONDARY_EXCEPTION", "WR3_TARGETS_BORDERLINE", 4.0, 5.0
SUSPECT_RX = re.compile(r"MODEL-SUSPECT|too far below|below the book", re.I)
QB_BAD = ("D", "F", "WEAK")

def s1_ok(leg):
    """True if this non-PRESS MANUAL_REVIEW is an allowed S1 model-suspect under."""
    if str(leg.get("side", "")).lower() != "under": return False
    rs = leg.get("cut_reasons") or [(leg.get("manual_review") or {}).get("reason", "")]
    if not any(SUSPECT_RX.search(str(r)) for r in rs): return False
    b = leg.get("backfield_split") or {}
    q = leg.get("backup_qb_card") or {}
    return bool(b.get("source") and b.get("detail")) and str(q.get("grade", "")).upper() in QB_BAD and bool(q.get("source"))

def wr3_under_team_cov(leg):
    cv = leg.get("coverage") or {}
    return (str(leg.get("side", "")).lower() == "under" and (leg.get("wr_rank") or 0) >= 3
            and "man_zone" in cv and "mof" in cv)

def check_snf(self, m, legs, live):
    if not _rb.active("SNF", self.game_date, getattr(self, "now", None)): return
    self.snf_notes = []
    for n, l in legs.items():
        if str(l.get("status", "")).upper() == "MANUAL_REVIEW" and s1_ok(l):
            self.snf_notes.append(f"S1 MANUAL REVIEW (model-suspect under, backfield split + backup-QB {l['backup_qb_card'].get('grade')}): {n}")
        if "WR3_TEAM_COV" in (l.get("flags") or []) and not wr3_under_team_cov(l):
            self.fail(f"leg {n}: WR3_TEAM_COV flag needs side under, wr_rank>=3, team man_zone+mof")
    for q in m.get("questionable_wr", []) or []:
        if q.get("confirmed_at_inactives"): continue
        sp = q.get("target_shares") or {}
        if not sp.get("active") or not sp.get("inactive"):
            self.fail(f"questionable WR {q.get('name')} unconfirmed at inactives: target shares must be rerun both ways (active + inactive)")
        else: self.snf_notes.append(f"S3 {q.get('name')} unconfirmed: shares active {sp['active']} | inactive {sp['inactive']}")
    for d in m.get("depleted_secondary", []) or []:
        if len(d.get("cbs_out") or []) < 2: continue
        names = set(legs)
        for c in d.get("wr23_over_pool") or []:
            if not c.get("leg") and not c.get("skip_reason") and not any(c.get("name", "~") in k for k in names):
                self.fail(f"depleted_secondary {d.get('team')}: WR{c.get('wr_rank')} {c.get('name')} over has no leg and no skip_reason")
            lg = legs.get(c.get("leg")) or {}
            if c.get("wr_rank") == 4 and c.get("leg") in live:   # DEPTH_RECEIVER replaces the WR4 ban
                import depth_rule as _dr
                ok, why = _dr.evaluate(dict(legs.get(c["leg"], {}), type="WR", wr_rank=4, side="over"))
                if not ok: self.fail(f"leg {c['leg']}: WR4 over needs DEPTH_RECEIVER: " + "; ".join(why))
            if c.get("wr_rank") == 3 and c.get("leg") in live:
                fl = lg.get("flags") or []; tpg = lg.get("tpg_last4_cur_qb")
                if EXC_FLAG not in fl:
                    self.fail(f"leg {c['leg']}: live WR3 over (depleted secondary) needs flag {EXC_FLAG}")
                elif str(lg.get("opportunity", "")).lower() == "mixed":
                    self.fail(f"leg {c['leg']}: WR3 exception needs opportunity check not 'mixed'")
                elif tpg is None or float(tpg) < TPG_MIN:
                    self.fail(f"leg {c['leg']}: WR3 exception needs >=4.0 targets/g last 4 w/ current QB (tpg_last4_cur_qb={tpg}); ban stands")
                elif float(tpg) < TPG_FULL and BORDER_FLAG not in fl:
                    self.fail(f"leg {c['leg']}: tpg {tpg} in 4.0-4.9 needs flag {BORDER_FLAG}")
                elif float(tpg) >= TPG_FULL and BORDER_FLAG in fl:
                    self.fail(f"leg {c['leg']}: tpg {tpg} >= 5 is full; remove {BORDER_FLAG}")
                else:
                    self.snf_notes.append(f"S4 {EXC_FLAG}{' + '+BORDER_FLAG if float(tpg) < TPG_FULL else ' (full)'}: {c['leg']} tpg {tpg} vs {d.get('team')} CBs out {d.get('cbs_out')}")
        if not d.get("wr23_over_pool"): self.fail(f"depleted_secondary {d.get('team')}: 2+ CBs out but wr23_over_pool missing")
    for n, l in legs.items():
        if EXC_FLAG in (l.get("flags") or []):
            ok = any(len(d.get("cbs_out") or []) >= 2 and any(c.get("leg") == n and c.get("wr_rank") == 3 for c in d.get("wr23_over_pool") or [])
                     for d in m.get("depleted_secondary", []) or [])
            if not ok or str(l.get("side", "")).lower() != "over":
                self.fail(f"leg {n}: {EXC_FLAG} only valid on a WR3 over in a depleted_secondary pool (2+ CBs out)")

def install(G):
    G.check_snf = check_snf
