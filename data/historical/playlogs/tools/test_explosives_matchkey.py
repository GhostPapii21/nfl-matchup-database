# Regression: ARI@DAL Q5 5:13 ESPN text has a leading space ("[Rush]  T.Allgeier") that the md table cell strips.
import re,sys
sys.path.insert(0,'/workspace/nfl-database/playlogs/tools')
from test_explosives import play_key
line='- Q5 5:13 [Rush]  T.Allgeier right tackle to DAL 31 for 11 yards (P.Locke). (score ARI 30-DAL 30)'
m=re.match(r'- (Q\d \d+:\d+) \[[^\]]*\] (.*)',line)
assert play_key(m.group(1),m.group(2))==play_key('Q5 5:13','T.Allgeier right tackle to DAL 31 for 11 yards (P.Locke).'), 'leading-space mismatch'
assert play_key('OT 8:32','x')==play_key('Q5 8:32','x'), 'OT/Q5 label mismatch'
print('PASS matchkey')
