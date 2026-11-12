import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import snf_rules as S
class G:
    def __init__(s, d): s.game_date=d; s.miss=[]
    def fail(s, x): s.miss.append(x)
U=dict(side="under", status="MANUAL_REVIEW", cut_reasons=["MODEL-SUSPECT models 18 pts below book"])
def test_s1_needs_both():
    assert not S.s1_ok(U)
    assert not S.s1_ok({**U, "backfield_split": {"source":"x","detail":"Saquon/Mitchell"}})
    assert S.s1_ok({**U, "backfield_split": {"source":"x","detail":"split"}, "backup_qb_card": {"grade":"D","source":"cards/x"}})
    assert not S.s1_ok({**U, "side":"over", "backfield_split": {"source":"x","detail":"s"}, "backup_qb_card": {"grade":"F","source":"c"}})
def test_s2():
    cv={"man_zone":{}, "mof":{}}
    assert S.wr3_under_team_cov(dict(side="under", wr_rank=3, coverage=cv))
    assert not S.wr3_under_team_cov(dict(side="over", wr_rank=3, coverage=cv))
    assert not S.wr3_under_team_cov(dict(side="under", wr_rank=2, coverage=cv))
def test_s3_s4():
    g=G("2026-11-08"); S.check_snf(g, {"questionable_wr":[{"name":"A","confirmed_at_inactives":False,"target_shares":{"active":{"a":.2}}}],
        "depleted_secondary":[{"team":"PHI","cbs_out":["J","B"],"wr23_over_pool":[{"name":"Burks","wr_rank":3,"leg":"Burks Over"}]}]}, {"Burks Over":{}}, {"Burks Over"})
    assert len(g.miss)==2
    g=G("2026-11-01"); S.check_snf(g, {"questionable_wr":[{"name":"A"}]}, {}, set()); assert not g.miss
def test_start_mnf():
    g=G("2026-11-02"); S.check_snf(g, {"questionable_wr":[{"name":"A"}]}, {}, set()); assert len(g.miss)==1
def DS(r, n=2): return {"depleted_secondary":[{"team":"PHI","cbs_out":["J","B"][:n],"wr23_over_pool":[{"name":"X","wr_rank":r,"leg":"X Over"}]}]}
def run(m, leg):
    g=G("2026-11-02"); S.check_snf(g, m, {"X Over":{"side":"over",**leg}}, {"X Over"}); return g
F=[S.EXC_FLAG]; FB=[S.EXC_FLAG, S.BORDER_FLAG]
def test_wr3_exception():
    g=run(DS(3), dict(flags=F, tpg_last4_cur_qb=5.5)); assert not g.miss and "full" in g.snf_notes[-1]
    g=run(DS(3), dict(flags=FB, tpg_last4_cur_qb=4.2)); assert not g.miss and S.BORDER_FLAG in g.snf_notes[-1]
    assert len(run(DS(3), dict(flags=F, tpg_last4_cur_qb=4.2)).miss)==1      # borderline needs flag
    assert len(run(DS(3), dict(flags=FB, tpg_last4_cur_qb=5.0)).miss)==1     # 5+ is full
    assert len(run(DS(3), dict(flags=F, tpg_last4_cur_qb=3.9)).miss)==1      # <4 banned
    assert len(run(DS(3), dict(flags=F)).miss)==1                            # tpg missing
    assert len(run(DS(3), dict(flags=F, tpg_last4_cur_qb=6, opportunity="mixed")).miss)==1
    assert len(run(DS(3), dict(tpg_last4_cur_qb=6)).miss)==1                 # no flag
    assert len(run(DS(4), dict(flags=F, tpg_last4_cur_qb=6)).miss)==2        # WR4 banned
    assert len(run(DS(3,1), dict(flags=F, tpg_last4_cur_qb=6)).miss)==1      # only 1 CB out
