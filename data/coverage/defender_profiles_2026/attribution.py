"""INFERRED coverage attribution: the most likely primary defender on every 2026 targeted pass. Research only.

    python3 data/coverage/defender_profiles_2026/attribution.py --raw <dir> [--through-week N]

Everything this writes is INFERRED. It is never a verified defender and must not satisfy the verified-defender rule
for receiving legs. Verified = named on a PBU, INT or DPI in play-by-play (see build.py).

Inputs actually used (free/public): nflverse pbp (pass_length short/deep, pass_location left/middle/right from the
offense's view, receiver, PBU/INT/DPI names, tacklers), nflverse snap counts (who was on the field that game, snap %),
weekly rosters (positions), StatRankings team man % and single-high/two-high % (scheme).
NOT used, because the free data does not have it: per-play routes, player tracking, pre-snap alignment, catch x/y.
nflverse NGS is season/week aggregates per receiver only (see ATTRIBUTION_METHOD.md).

Model, per target, over the CB/S/DB/LB who played defensive snaps for the defense in that game:
  score(d) = snap%(d, game)
           x P(position group | receiver position, zone)          learned from verified plays (other weeks only)
           x zone lean(d) / zone lean(group)                       defender's own side/depth tendency from his
                                                                   verified plays + tackles-after-catch (this play removed)
           x (1 + b_game * links(d, receiver, same game) + b_season * links(d, receiver, season))   (this play removed)
           x scheme factor for safeties on deep throws (two-high vs single-high rate)
  probabilities = scores normalised per play; confidence tier from top probability and margin.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import build as B

HERE = Path(__file__).resolve().parent
ZONES = [f"{l}_{c}" for l in ("short", "deep") for c in ("left", "middle", "right")]
ZI = {z: i for i, z in enumerate(ZONES)}
GROUPS = ["CB", "S", "LB"]
GI = {g: i for i, g in enumerate(GROUPS)}
RPOS = ["WR", "TE", "RB"]
# Chosen on weeks 1-8 from a 20-config grid (see ATTRIBUTION_METHOD.md); weeks 9-12 are the untouched test.
PARAMS = dict(alpha=8.0, b_game=0.5, b_season=0.0, man_boost=1.5, scheme=1.0)


def tier(p1, p2):
    """Tiers set on weeks 1-8 accuracy-by-probability bins (p1 >= 0.5 was ~49% right; below 0.35 ~23%)."""
    if p1 >= 0.5:
        return "high"
    return "med" if (p1 >= 0.35 or p1 >= 2.5 * p2) else "low"


def group_of(pos):
    return {"CB": "CB", "DB": "CB", "S": "S", "LB": "LB"}.get(pos)


def prepare(raw: Path, through: int | None):
    p, a, s, ro, ngs, ftn = B.load(raw, through)
    cover_pos, off_pos, names, pfr2gsis, gsis2pfr, pos_snap = B.id_maps(ro, s)
    t = B.target_plays(p, off_pos)
    links = B.defender_links(p, t, off_pos)
    links["grp"] = links.def_id.map(cover_pos).map(group_of)
    # snaps per game for coverage players
    s = s[s.defense_snaps > 0].copy()
    s["gsis"] = s.pfr_player_id.map(pfr2gsis)
    s["grp"] = s.position.map(B.COVER_POS).map(group_of)
    s = s.dropna(subset=["gsis", "grp"])
    s["team"] = s.team.replace({"LAR": "LA"})
    sr = pd.read_csv(raw / "statrankings_team_cov.csv")
    sr["team"] = sr.team.replace(B.SR_CODE)
    sr = sr.set_index("team")
    return p, t, links, s, sr, names


def fit_pos_prior(vlinks: pd.DataFrame):
    """P(group | rpos, zone) from verified links with a coverage-group defender; Dirichlet-smoothed."""
    c = np.ones((len(RPOS), len(ZONES), len(GROUPS)))
    v = vlinks[vlinks.rpos.isin(RPOS) & vlinks.zone.isin(ZONES) & vlinks.grp.isin(GROUPS)]
    for (r, z, g), n in v.groupby(["rpos", "zone", "grp"]).size().items():
        c[RPOS.index(r), ZI[z], GI[g]] += n
    return c / c.sum(axis=2, keepdims=True)


def zone_counts(links: pd.DataFrame):
    """Per (defender, defteam): counts over the 6 zones, from verified + tackler links."""
    l = links[links.zone.isin(ZONES)]
    zc = defaultdict(lambda: np.zeros(len(ZONES)))
    for (d, tm, z), n in l.groupby(["def_id", "defteam", "zone"]).size().items():
        zc[(d, tm)][ZI[z]] += n
    grp = np.ones((len(GROUPS), len(ZONES)))
    for (g, z), n in l[l.grp.isin(GROUPS)].groupby(["grp", "zone"]).size().items():
        grp[GI[g], ZI[z]] += n
    return zc, grp / grp.sum(axis=1, keepdims=True)


def score_game(plays, cands, zc, grp_zone, pos_prior, rec_game, rec_season, sch, prm, held=None):
    """plays: rows of one game for one defense. cands: DataFrame(gsis, grp, pct). Returns list of prob arrays."""
    out = []
    ids = cands.gsis.tolist()
    gi = np.array([GI[g] for g in cands.grp])
    pct = cands.pct.to_numpy()
    man = sch.get("man", np.nan)
    man = 0.3 if not np.isfinite(man) else man / 100
    two = sch.get("two_high", np.nan)
    two = 0.5 if not np.isfinite(two) else two / 100
    for _, x in plays.iterrows():
        z = ZI.get(x.zone)
        r = RPOS.index(x.rpos) if x.rpos in RPOS else 0
        if z is None:
            out.append(None)
            continue
        pp = pos_prior[r, z, gi]
        lean = np.empty(len(ids))
        aff = np.empty(len(ids))
        for k, d in enumerate(ids):
            cnt = zc.get((d, x.defteam), np.zeros(len(ZONES))).copy()
            rg = rec_game.get((d, x.game_id, x.receiver_player_id), 0)
            rs = rec_season.get((d, x.defteam, x.receiver_player_id), 0)
            if held is not None and d == held[0]:   # remove the held-out verified play itself
                cnt[z] -= 1
                rg -= 1
                rs -= 1
            gz = grp_zone[gi[k]]
            lean[k] = ((cnt[z] + prm["alpha"] * gz[z]) / (cnt.sum() + prm["alpha"])) / gz[z]
            b_game = prm["b_game"] * (1 + prm["man_boost"] * man)
            aff[k] = 1 + b_game * max(rg, 0) + prm["b_season"] * max(rs, 0)
        sf = np.ones(len(ids))
        if x.zone.startswith("deep"):
            f = (two / 0.5) if not x.zone.endswith("middle") else ((1 - two) / 0.5)
            sf = np.where(gi == GI["S"], f ** prm["scheme"], 1.0)
        sc = pct * pp * lean * aff * sf
        out.append(sc / sc.sum() if sc.sum() > 0 else None)
    return out


def receiver_link_maps(links):
    l = links.dropna(subset=["receiver_player_name"])
    # receiver ids: links carry names; map by (game, posteam, name) to id through target plays where possible
    rg = l.groupby(["def_id", "game_id", "rid"]).size().to_dict()
    rs = l.groupby(["def_id", "defteam", "rid"]).size().to_dict()
    return rg, rs


def run(raw: Path, through: int | None, prm=PARAMS, validate_only=False, val_weeks=None, fit_weeks=None):
    p, t, links, snaps, sr, names = prepare(raw, through)
    # receiver id on links (target-play links already carry receiver via play; DPI links: name only)
    rid = t.set_index(["game_id", "play_id"]).receiver_player_id
    links["rid"] = [rid.get((g, pl)) for g, pl in zip(links.game_id, links.play_id)]
    verified = links[(links.label == "verified") & links.grp.isin(GROUPS)]
    zc, grp_zone = zone_counts(links[links.grp.isin(GROUPS)])
    rg, rs = receiver_link_maps(links[links.grp.isin(GROUPS)])
    snaps_g = {k: v for k, v in snaps.groupby(["game_id", "team"])}
    # position prior: fit on fit_weeks (validation) or all verified (production)
    results = []
    games = t.groupby(["game_id", "defteam"])
    for (g, tm), plays in games:
        cands = snaps_g.get((g, tm))
        if cands is None or not len(cands):
            continue
        cands = cands.groupby("gsis").agg(grp=("grp", "first"), pct=("defense_pct", "max")).reset_index()
        sch = {"man": sr.at[tm, "man"] if tm in sr.index else np.nan, "two_high": sr.at[tm, "two_high"] if tm in sr.index else np.nan}
        wk = int(plays.week.iloc[0])
        if validate_only:
            if val_weeks and wk not in val_weeks:
                continue
            pos_prior = PRIOR_CACHE.setdefault(("fold", wk, tuple(sorted(fit_weeks or []))), fit_pos_prior(
                verified[(verified.week != wk) & (verified.week.isin(fit_weeks) if fit_weeks else True)]))
            vp = verified[(verified.game_id == g) & (verified.defteam == tm) & verified.zone.isin(ZONES)]
            vp = vp[vp.play_id.isin(plays.play_id)]
            for _, v in vp.drop_duplicates(["play_id"]).iterrows():
                row = plays[plays.play_id == v.play_id].iloc[0]
                pr = score_game(pd.DataFrame([row]), cands, zc, grp_zone, pos_prior, rg, rs, sch, prm, held=(v.def_id,))[0]
                if pr is None:
                    continue
                order = np.argsort(-pr)
                truth = set(verified[(verified.game_id == g) & (verified.play_id == v.play_id)].def_id)
                in_cands = bool(truth & set(cands.gsis))
                results.append({"week": wk, "game_id": g, "play_id": v.play_id, "link": v.link, "truth_in_candidates": in_cands,
                                "top1": cands.gsis.iloc[order[0]] in truth, "top2": bool(truth & set(cands.gsis.iloc[order[:2]])),
                                "p1": pr[order[0]], "p2": pr[order[1]] if len(pr) > 1 else 0.0,
                                "tier": tier(pr[order[0]], pr[order[1]] if len(pr) > 1 else 0.0)})
            continue
        pos_prior = PRIOR_CACHE.setdefault(("all",), fit_pos_prior(verified))
        probs = score_game(plays, cands, zc, grp_zone, pos_prior, rg, rs, sch, prm)
        for (_, x), pr in zip(plays.iterrows(), probs):
            rec = {"week": wk, "game_id": g, "play_id": x.play_id, "defteam": tm, "posteam": x.posteam, "qtr": x.qtr, "time": x.time,
                   "receiver": x.receiver_player_name, "receiver_id": x.receiver_player_id, "rpos": x.rpos, "zone": x.zone,
                   "result": "INT" if x.int else ("TD" if x.td else ("complete" if x.cmp else "incomplete")),
                   "yards": x.yds, "air_yards": x.air_yards}
            if pr is None:
                rec.update(inferred_defender=None, inferred_defender_id=None, inferred_pos=None, prob=None, second_defender=None,
                           prob2=None, confidence="none", method="no zone in pbp (throwaway/spike/unknown direction)")
            else:
                o = np.argsort(-pr)
                d1, d2 = cands.iloc[o[0]], cands.iloc[o[1]] if len(o) > 1 else None
                rec.update(inferred_defender=names.get(d1.gsis, d1.gsis), inferred_defender_id=d1.gsis, inferred_pos=d1.grp,
                           prob=round(float(pr[o[0]]), 3), second_defender=names.get(d2.gsis, d2.gsis) if d2 is not None else None,
                           prob2=round(float(pr[o[1]]), 3) if d2 is not None else None,
                           confidence=tier(pr[o[0]], pr[o[1]] if len(o) > 1 else 0.0),
                           method="INFERRED: zone+receiver pos prior x defender side/depth lean x same-game receiver links x snap% x shell")
                rec["_probs"] = (cands.gsis.tolist(), pr)
            vv = verified[(verified.game_id == g) & (verified.play_id == x.play_id)]
            rec["verified_defender"] = "; ".join(f"{n} ({k})" for n, k in zip(vv.def_name, vv.link)) or None
            results.append(rec)
    return results, links, names, snaps, sr, t, zc, grp_zone, rg, rs


PRIOR_CACHE: dict = {}


def validate(raw, through, prm):
    PRIOR_CACHE.clear()
    res, *_ = run(raw, through, prm, validate_only=True)
    return pd.DataFrame(res)


def summarize(v: pd.DataFrame):
    v = v.copy()
    rows = []
    for tr in ["high", "med", "low", "ALL"]:
        x = v if tr == "ALL" else v[v.tier == tr]
        rows.append({"tier": tr, "plays": len(x), "top1_acc": round(x.top1.mean(), 3) if len(x) else None,
                     "top2_acc": round(x.top2.mean(), 3) if len(x) else None,
                     "mean_p1": round(x.p1.mean(), 3) if len(x) else None})
    return pd.DataFrame(rows)


def upcoming_matchups(raw, res_links, names, snaps, t, zc, grp_zone, rg, rs, sr, prm, pos_prior):
    g = pd.read_csv(raw / "games.csv")
    g = g[(g.season == 2026) & g.away_score.isna() & g.week.isin([12, 13])]
    last4 = t[t.week > t.week.max() - 4]
    rows = []
    for _, gm in g.iterrows():
        for off, dfn in ((gm.away_team, gm.home_team), (gm.home_team, gm.away_team)):
            off, dfn = off.replace("LAR", "LA"), dfn.replace("LAR", "LA")
            ls = snaps[snaps.team == dfn]
            if not len(ls):
                continue
            lastg = ls.sort_values("week").game_id.iloc[-1]
            cands = ls[ls.game_id == lastg].groupby("gsis").agg(grp=("grp", "first"), pct=("defense_pct", "max")).reset_index()
            top = last4[last4.posteam == off].groupby(["receiver_player_id", "receiver_player_name", "rpos"]).size().nlargest(4)
            sch = {"man": sr.at[dfn, "man"] if dfn in sr.index else np.nan, "two_high": sr.at[dfn, "two_high"] if dfn in sr.index else np.nan}
            for (rid, rname, rpos), n4 in top.items():
                hist = t[(t.receiver_player_id == rid) & t.zone.isin(ZONES)].copy()
                if not len(hist):
                    continue
                hist["defteam"], hist["game_id"] = dfn, "UPCOMING"
                pr = [x for x in score_game(hist, cands, zc, grp_zone, pos_prior, rg, rs, sch, prm) if x is not None]
                share = np.mean(pr, axis=0)
                o = np.argsort(-share)
                zmix = hist.zone.value_counts(normalize=True).head(2)
                rows.append({"week": int(gm.week), "gameday": gm.gameday, "offense": off, "defense": dfn, "receiver": rname, "rpos": rpos,
                             "tgts_last4wks": int(n4), "receiver_top_zones": ", ".join(f"{z} {v:.0%}" for z, v in zmix.items()),
                             "likely_defender_1": names.get(cands.gsis.iloc[o[0]]), "share_1": round(float(share[o[0]]), 3),
                             "likely_defender_2": names.get(cands.gsis.iloc[o[1]]), "share_2": round(float(share[o[1]]), 3),
                             "defense_snaps_from": lastg, "label": "INFERRED (not verified; not usable for the verified-defender rule)"})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True, type=Path)
    ap.add_argument("--through-week", type=int)
    ap.add_argument("--out", type=Path, default=HERE)
    args = ap.parse_args()
    out = args.out
    # 1) validation: hold out each verified PBU/INT play (leave-one-play-out for defender tendencies,
    #    leave-one-week-out for the position prior). Weeks 1-8 were used to pick params and tiers; 9-12 untouched.
    v = validate(args.raw, args.through_week, PARAMS)
    base = validate(args.raw, args.through_week, dict(alpha=1e9, b_game=0, b_season=0, man_boost=0, scheme=0))
    v.to_csv(out / "attribution_validation_plays.csv", index=False)
    summ = []
    for name, x in (("test_wk9_12", v[v.week >= 9]), ("train_wk1_8", v[v.week <= 8]), ("all", v)):
        sm = summarize(x)
        sm.insert(0, "split", name)
        summ.append(sm)
    for name, x in (("baseline_snap_x_position_only_test_wk9_12", base[base.week >= 9]), ("baseline_snap_x_position_only_all", base)):
        sm = summarize(x)
        sm.insert(0, "split", name)
        summ.append(sm)
    summ = pd.concat(summ)
    summ.to_csv(out / "attribution_validation_summary.csv", index=False)
    # 2) production attribution on every target
    PRIOR_CACHE.clear()
    res, links, names, snaps, sr, t, zc, grp_zone, rg, rs = run(args.raw, args.through_week, PARAMS)
    df = pd.DataFrame(res)
    probs = df.pop("_probs") if "_probs" in df else None
    df["label"] = "INFERRED"
    df.to_csv(out / "defender_attribution_inferred.csv", index=False)
    # 3) per-defender totals: expected (probability-weighted) and top-pick counts
    acc = defaultdict(lambda: np.zeros(6))
    for (_, r), pp in zip(df.iterrows(), probs if probs is not None else []):
        if not isinstance(pp, tuple):
            continue
        ids, pr = pp
        for d, q in zip(ids, pr):
            acc[(d, r.defteam)] += q * np.array([1, r.result in ("complete", "TD"), r.yards if r.result in ("complete", "TD") else 0,
                                                 r.result == "TD", r.result == "INT", 0])
    top = df[df.confidence != "none"].groupby(["inferred_defender_id", "defteam"]).agg(
        top_pick_tgts=("play_id", "size"), top_pick_high_med=("confidence", lambda x: int(x.isin(["high", "med"]).sum())),
        top_pick_yds=("yards", lambda x: float(x.sum()))).reset_index()
    tot = pd.DataFrame([{"gsis_id": d, "team": tm, "player": names.get(d, d), "exp_tgts": round(a[0], 1), "exp_rec": round(a[1], 1),
                         "exp_yds": round(a[2], 1), "exp_td": round(a[3], 2), "exp_int": round(a[4], 2)} for (d, tm), a in acc.items()])
    pos = links.drop_duplicates("def_id").set_index("def_id").grp
    tot["pos_group"] = tot.gsis_id.map(pos)
    tot = tot.merge(top.rename(columns={"inferred_defender_id": "gsis_id", "defteam": "team"}), on=["gsis_id", "team"], how="left")
    tot["exp_ypt"] = (tot.exp_yds / tot.exp_tgts).round(2)
    tot["label"] = "INFERRED (vicinity estimate, not charted coverage)"
    tot = tot.sort_values(["team", "exp_tgts"], ascending=[True, False])
    tot.to_csv(out / "defender_inferred_coverage_totals.csv", index=False)
    # 4) upcoming matchups
    pos_prior = PRIOR_CACHE[("all",)]
    up = upcoming_matchups(args.raw, links, names, snaps, t, zc, grp_zone, rg, rs, sr, PARAMS, pos_prior)
    up.to_csv(out / "upcoming_receiver_vs_likely_defender.csv", index=False)
    # 5) profile sections
    write_profile_sections(out / "profiles", tot, up, summ)
    print(summ.to_string(index=False))
    print(json.dumps({"targets": int(len(df)), "attributed": int((df.confidence != "none").sum()),
                      "by_tier": df.confidence.value_counts().to_dict(), "upcoming_rows": int(len(up)),
                      "defenders_with_totals": int(len(tot))}, indent=1))


MARK = "<!-- INFERRED-ATTRIBUTION -->"


def write_profile_sections(pdir, tot, up, summ):
    t9 = summ[(summ.split == "test_wk9_12")].set_index("tier")
    acc = ", ".join(f"{k} {t9.at[k, 'top1_acc']:.0%} (n={int(t9.at[k, 'plays'])})" for k in ("high", "med", "low", "ALL"))
    for f in pdir.glob("*.md"):
        tm = f.stem
        body = f.read_text().split(MARK)[0].rstrip() + "\n\n" + MARK + "\n"
        L = ["## INFERRED coverage attribution (not verified)", "",
             "Most-likely-defender estimate from pbp zone, receiver position, each defender's verified/tackle side-depth tendencies, "
             "same-game receiver links, snap % and shell. **INFERRED only: it never satisfies the verified-defender rule.** "
             f"Held-out accuracy on verified PBU/INT plays, weeks 9–12, top pick right: {acc}.", "",
             "| Defender | Pos | Exp. targets | Exp. rec | Exp. yds | Exp. YPT | Exp. TD | Top-pick targets (high/med) |", "|---|---|---|---|---|---|---|---|"]
        for _, x in tot[(tot.team == tm) & (tot.exp_tgts >= 5)].head(12).iterrows():
            L.append(f"| {x.player} | {x.pos_group} | {x.exp_tgts} | {x.exp_rec} | {x.exp_yds} | {x.exp_ypt} | {x.exp_td} | "
                     f"{int(x.top_pick_tgts) if pd.notna(x.top_pick_tgts) else 0} ({int(x.top_pick_high_med) if pd.notna(x.top_pick_high_med) else 0}) |")
        u = up[up.defense == tm]
        if len(u):
            L += ["", f"### Upcoming: opposing receivers vs likely {tm} defender (INFERRED)", "",
                  "| Wk | Date | Offense | Receiver | Tgts last 4 wks | Receiver's main zones | Likely defender (share) | Next (share) |", "|---|---|---|---|---|---|---|---|"]
            for _, x in u.iterrows():
                L.append(f"| {x.week} | {x.gameday} | {x.offense} | {x.receiver} ({x.rpos}) | {x.tgts_last4wks} | {x.receiver_top_zones} | "
                         f"{x.likely_defender_1} ({x.share_1:.0%}) | {x.likely_defender_2} ({x.share_2:.0%}) |")
            L.append(f"\nDefender pool = {tm} players with defensive snaps in their most recent game ({u.defense_snaps_from.iloc[0]}); check inactives before use.")
        f.write_text(body + "\n".join(L) + "\n")


if __name__ == "__main__":
    main()
