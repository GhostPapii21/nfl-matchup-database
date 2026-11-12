cd "$(dirname "$0")"
for e in sim_v5 sim_v6 sim_v6_fix; do for w in 3 4 5 6 7 8; do echo "$e $w"; done; done | xargs -P 6 -n 2 sh -c 'python3 run_sims_meanmed.py $0 $1'
echo ALLDONE
