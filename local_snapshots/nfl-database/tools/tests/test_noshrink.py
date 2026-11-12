import ast, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def _default(path):
    for n in ast.walk(ast.parse(open(os.path.join(R, path)).read())):
        if isinstance(n, ast.FunctionDef) and n.name == "oppadj":
            return n.args.defaults[-1].value
def test_sim_v6_full_strength(): assert _default("tools/sim_v6.py") == 1.0
def test_sim_v5_thursday_full_strength(): assert _default("runs/2026-11-05_shared_src/sim_v5.py") == 1.0
def test_no_shrunk_calc():
    assert "0.7*(av-0.5)" not in open(os.path.join(R, "tools/sim_v6.py")).read()
def test_sim_v6_fix_marked_deprecated(): assert os.path.exists(os.path.join(R, "tools/sim_v6_fix/DEPRECATED.md"))
