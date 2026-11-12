# Train-only traits: weeks 3–6

Exploratory, not causal. Hit excludes pushes/ungraded; ROI uses $10 settled stakes. No holdout grading.

    market  side         bucket   n  wins  losses  pushes  ungraded    hit_pct          pl  stake         roi                   feature
    recyds  over    (-inf, 0.0] 331   119     124       0        88  48.971193 -192.612606   2430   -7.926445                model_edge
    recyds  over     (0.0, 5.0] 147    46      61       0        40  42.990654 -204.669912   1070  -19.128029                model_edge
    recyds  over   (10.0, 15.0]  59    26      22       0        11  54.166667    9.213073    480    1.919390                model_edge
    recyds  over   (15.0, 20.0]  33    12      13       0         8  48.000000  -25.084943    250  -10.033977                model_edge
    recyds  over    (20.0, inf]  66    27      26       0        13  50.943396  -23.843964    530   -4.498861                model_edge
    recyds  over    (5.0, 10.0] 121    43      53       0        25  44.791667 -149.759114    960  -15.599908                model_edge
    recyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN                model_edge
    recyds under    (-inf, 0.0] 430   175     156       0        99  52.870091  -19.595278   3310   -0.592002                model_edge
    recyds under     (0.0, 5.0] 129    52      52       0        25  50.000000  -65.697730   1040   -6.317089                model_edge
    recyds under   (10.0, 15.0]  46    14      17       0        15  45.161290  -46.622218    310  -15.039425                model_edge
    recyds under   (15.0, 20.0]  23     9       7       0         7  56.250000    9.671450    160    6.044656                model_edge
    recyds under    (20.0, inf]  34    12       8       0        14  60.000000   25.506168    200   12.753084                model_edge
    recyds under    (5.0, 10.0]  95    37      33       0        25  52.857143   -1.599557    700   -0.228508                model_edge
    recyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN                model_edge
rushrecyds  over    (-inf, 0.0] 111    32      36       0        43  47.058824  -79.170725    680  -11.642754                model_edge
rushrecyds  over     (0.0, 5.0]  16     4       4       0         8  50.000000   -4.558251     80   -5.697814                model_edge
rushrecyds  over   (10.0, 15.0]  10     0       6       0         4   0.000000  -60.000000     60 -100.000000                model_edge
rushrecyds  over   (15.0, 20.0]  15     2       4       0         9  33.333333  -22.339181     60  -37.231969                model_edge
rushrecyds  over    (20.0, inf]  16     5       4       0         7  55.555556    3.862349     90    4.291499                model_edge
rushrecyds  over    (5.0, 10.0]  18     6       5       0         7  54.545455    2.634279    110    2.394799                model_edge
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN                model_edge
rushrecyds under    (-inf, 0.0]  77    24      18       0        35  57.142857   29.729392    420    7.078427                model_edge
rushrecyds under     (0.0, 5.0]  20     6       4       0        10  60.000000   13.027723    100   13.027723                model_edge
rushrecyds under   (10.0, 15.0]  26    10      10       0         6  50.000000  -12.470212    200   -6.235106                model_edge
rushrecyds under   (15.0, 20.0]  10     2       1       0         7  66.666667    7.507566     30   25.025221                model_edge
rushrecyds under    (20.0, inf]  33    13      11       0         9  54.166667    3.811655    240    1.588190                model_edge
rushrecyds under    (5.0, 10.0]  20     4       5       0        11  44.444444  -15.523409     90  -17.248232                model_edge
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN                model_edge
   rushyds  over    (-inf, 0.0] 186    66      80       0        40  45.205479 -218.765729   1460  -14.983954                model_edge
   rushyds  over     (0.0, 5.0]  84    30      36       0        18  45.454545 -103.834491    660  -15.732499                model_edge
   rushyds  over   (10.0, 15.0]  24    10      11       0         3  47.619048  -22.531581    210  -10.729324                model_edge
   rushyds  over   (15.0, 20.0]  13     6       5       0         2  54.545455    3.190940    110    2.900855                model_edge
   rushyds  over    (20.0, inf]  13     4       6       0         3  40.000000  -24.984249    100  -24.984249                model_edge
   rushyds  over    (5.0, 10.0]  38    10      21       0         7  32.258065 -122.239960    310  -39.432245                model_edge
   rushyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN                model_edge
   rushyds under    (-inf, 0.0] 174    80      60       0        34  57.142857   96.045632   1400    6.860402                model_edge
   rushyds under     (0.0, 5.0]  72    32      32       0         8  50.000000  -42.007223    640   -6.563629                model_edge
   rushyds under   (10.0, 15.0]  29    12       6       0        11  66.666667   44.973906    180   24.985503                model_edge
   rushyds under   (15.0, 20.0]  23    11       7       0         5  61.111111   26.637588    180   14.798660                model_edge
   rushyds under    (20.0, inf]  18     7       5       0         6  58.333333   11.690267    120    9.741889                model_edge
   rushyds under    (5.0, 10.0]  42    17      16       0         9  51.515152  -10.870157    330   -3.293987                model_edge
   rushyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN                model_edge
    recyds  over   (-inf, 0.25] 630   221     243       0       166  47.629310 -485.150264   4640  -10.455825         prior_carry_share
    recyds  over    (0.25, 0.5]  55    28      19       0         8  59.574468   56.334781    470   11.986124         prior_carry_share
    recyds  over     (0.5, 0.6]  30     8      13       0         9  38.095238  -59.135300    210  -28.159667         prior_carry_share
    recyds  over    (0.6, 0.75]  36    13      21       0         2  38.235294  -95.359553    340  -28.046927         prior_carry_share
    recyds  over    (0.75, inf]   6     3       3       0         0  50.000000   -3.447131     60   -5.745219         prior_carry_share
    recyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         prior_carry_share
    recyds under   (-inf, 0.25] 630   243     221       0       166  52.370690  -72.025039   4640   -1.552264         prior_carry_share
    recyds under    (0.25, 0.5]  55    19      28       0         8  40.425532 -112.735410    470  -23.986257         prior_carry_share
    recyds under     (0.5, 0.6]  30    13       8       0         9  61.904762   34.909182    210   16.623420         prior_carry_share
    recyds under    (0.6, 0.75]  36    21      13       0         2  61.764706   54.998867    340   16.176137         prior_carry_share
    recyds under    (0.75, inf]   6     3       3       0         0  50.000000   -3.484766     60   -5.807944         prior_carry_share
    recyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         prior_carry_share
rushrecyds  over   (-inf, 0.25]  59    11      21       0        27  34.375000 -113.570991    320  -35.490935         prior_carry_share
rushrecyds  over    (0.25, 0.5]  55    16      19       0        20  45.714286  -49.163799    350  -14.046800         prior_carry_share
rushrecyds  over     (0.5, 0.6]  30     7      10       0        13  41.176471  -38.585580    170  -22.697400         prior_carry_share
rushrecyds  over    (0.6, 0.75]  36    13       8       0        15  61.904762   34.010394    210   16.195426         prior_carry_share
rushrecyds  over    (0.75, inf]   6     2       1       0         3  66.666667    7.738446     30   25.794821         prior_carry_share
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN         prior_carry_share
rushrecyds under   (-inf, 0.25]  59    21      11       0        27  65.625000   74.253193    320   23.204123         prior_carry_share
rushrecyds under    (0.25, 0.5]  55    19      16       0        20  54.285714    5.404504    350    1.544144         prior_carry_share
rushrecyds under     (0.5, 0.6]  30    10       7       0        13  58.823529   17.701046    170   10.412380         prior_carry_share
rushrecyds under    (0.6, 0.75]  36     8      13       0        15  38.095238  -60.204600    210  -28.668857         prior_carry_share
rushrecyds under    (0.75, inf]   6     1       2       0         3  33.333333  -11.071429     30  -36.904762         prior_carry_share
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN         prior_carry_share
   rushyds  over   (-inf, 0.25] 208    74     101       0        33  42.285714 -365.460487   1750  -20.883456         prior_carry_share
   rushyds  over    (0.25, 0.5]  76    27      23       0        26  54.000000    7.625802    500    1.525160         prior_carry_share
   rushyds  over     (0.5, 0.6]  32     8      20       0         4  28.571429 -129.845587    280  -46.373424         prior_carry_share
   rushyds  over    (0.6, 0.75]  36    15      12       0         9  55.555556   11.235858    270    4.161429         prior_carry_share
   rushyds  over    (0.75, inf]   6     2       3       0         1  40.000000  -12.720657     50  -25.441314         prior_carry_share
   rushyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         prior_carry_share
   rushyds under   (-inf, 0.25] 208   101      74       0        33  57.714286  136.150738   1750    7.780042         prior_carry_share
   rushyds under    (0.25, 0.5]  76    23      27       0        26  46.000000  -67.510736    500  -13.502147         prior_carry_share
   rushyds under     (0.5, 0.6]  32    20       8       0         4  71.428571   95.911842    280   34.254229         prior_carry_share
   rushyds under    (0.6, 0.75]  36    12      15       0         9  44.444444  -44.359988    270  -16.429625         prior_carry_share
   rushyds under    (0.75, inf]   6     3       2       0         1  60.000000    6.278155     50   12.556309         prior_carry_share
   rushyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         prior_carry_share
    recyds  over    (-inf, 0.4] 171    68      71       0        32  48.920863 -105.678550   1390   -7.602773          prior_snap_share
    recyds  over     (0.4, 0.6] 198    76      76       0        46  50.000000  -93.010426   1520   -6.119107          prior_snap_share
    recyds  over     (0.6, 0.8] 264    91     107       0        66  45.959596 -272.275254   1980  -13.751275          prior_snap_share
    recyds  over     (0.8, inf] 121    37      44       0        40  45.679012 -114.721807    810  -14.163186          prior_snap_share
    recyds  over            NaN  17     1       1       0        15  50.000000   -1.071429     20   -5.357143          prior_snap_share
    recyds under    (-inf, 0.4] 171    71      68       0        32  51.079137  -56.584643   1390   -4.070838          prior_snap_share
    recyds under     (0.4, 0.6] 198    76      76       0        46  50.000000  -90.907925   1520   -5.980785          prior_snap_share
    recyds under     (0.6, 0.8] 264   107      91       0        66  54.040404   32.581387   1980    1.645525          prior_snap_share
    recyds under     (0.8, inf] 121    44      37       0        40  54.320988   17.953326    810    2.216460          prior_snap_share
    recyds under            NaN  17     1       1       0        15  50.000000   -1.379310     20   -6.896552          prior_snap_share
rushrecyds  over    (-inf, 0.4]  56    12      21       0        23  36.363636 -104.689910    330  -31.724215          prior_snap_share
rushrecyds  over     (0.4, 0.6]  62    14      21       0        27  40.000000  -87.123306    350  -24.892373          prior_snap_share
rushrecyds  over     (0.6, 0.8]  62    22      16       0        24  57.894737   33.392128    380    8.787402          prior_snap_share
rushrecyds  over     (0.8, inf]   6     1       1       0         4  50.000000   -1.150442     20   -5.752212          prior_snap_share
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN          prior_snap_share
rushrecyds under    (-inf, 0.4]  56    21      12       0        23  63.636364   63.629242    330   19.281588          prior_snap_share
rushrecyds under     (0.4, 0.6]  62    21      14       0        27  60.000000   44.382457    350   12.680702          prior_snap_share
rushrecyds under     (0.6, 0.8]  62    16      22       0        24  42.105263  -80.857556    380  -21.278304          prior_snap_share
rushrecyds under     (0.8, inf]   6     1       1       0         4  50.000000   -1.071429     20   -5.357143          prior_snap_share
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN          prior_snap_share
   rushyds  over    (-inf, 0.4] 121    42      52       0        27  44.680851 -150.746740    940  -16.036887          prior_snap_share
   rushyds  over     (0.4, 0.6]  73    27      31       0        15  46.551724  -72.675871    580  -12.530323          prior_snap_share
   rushyds  over     (0.6, 0.8]  66    25      26       0        15  49.019608  -41.931410    510   -8.221845          prior_snap_share
   rushyds  over     (0.8, inf]  98    32      50       0        16  39.024390 -223.811049    820  -27.294030          prior_snap_share
   rushyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN          prior_snap_share
   rushyds under    (-inf, 0.4] 121    52      42       0        27  55.319149   38.473514    940    4.092927          prior_snap_share
   rushyds under     (0.4, 0.6]  73    31      27       0        15  53.448276    0.766041    580    0.132076          prior_snap_share
   rushyds under     (0.6, 0.8]  66    26      25       0        15  50.980392  -21.629993    510   -4.241175          prior_snap_share
   rushyds under     (0.8, inf]  98    50      32       0        16  60.975610  108.860451    820   13.275665          prior_snap_share
   rushyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN          prior_snap_share
    recyds  over    (-inf, 0.1]  95    31      34       0        30  47.692308  -66.758014    650  -10.270464         second_back_share
    recyds  over    (0.1, 0.25] 404   140     160       0       104  46.666667 -366.372658   3000  -12.212422         second_back_share
    recyds  over    (0.25, 0.4] 258   102     105       0        51  49.275362 -153.626795   2070   -7.421584         second_back_share
    recyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         second_back_share
    recyds under    (-inf, 0.1]  95    34      31       0        30  52.307692  -11.951246    650   -1.838653         second_back_share
    recyds under    (0.1, 0.25] 404   160     140       0       104  53.333333    9.689100   3000    0.322970         second_back_share
    recyds under    (0.25, 0.4] 258   105     102       0        51  50.724638  -96.075020   2070   -4.641305         second_back_share
    recyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         second_back_share
rushrecyds  over    (-inf, 0.1]  21     9       3       0         9  75.000000   49.070030    120   40.891692         second_back_share
rushrecyds  over    (0.1, 0.25] 101    25      33       0        43  43.103448 -110.314847    580  -19.019801         second_back_share
rushrecyds  over    (0.25, 0.4]  64    15      23       0        26  39.473684  -98.326713    380  -25.875451         second_back_share
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN         second_back_share
rushrecyds under    (-inf, 0.1]  21     3       9       0         9  25.000000  -63.760488    120  -53.133740         second_back_share
rushrecyds under    (0.1, 0.25] 101    33      25       0        43  56.896552   39.110091    580    6.743119         second_back_share
rushrecyds under    (0.25, 0.4]  64    23      15       0        26  60.526316   50.733111    380   13.350819         second_back_share
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN         second_back_share
   rushyds  over    (-inf, 0.1]  46    17      22       0         7  43.589744  -79.198069    390  -20.307197         second_back_share
   rushyds  over    (0.1, 0.25] 194    72      88       0        34  45.000000 -249.844259   1600  -15.615266         second_back_share
   rushyds  over    (0.25, 0.4] 118    37      49       0        32  43.023256 -160.122743    860  -18.618924         second_back_share
   rushyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         second_back_share
   rushyds under    (-inf, 0.1]  46    22      17       0         7  56.410256   25.125924    390    6.442545         second_back_share
   rushyds under    (0.1, 0.25] 194    88      72       0        34  55.000000   44.936730   1600    2.808546         second_back_share
   rushyds under    (0.25, 0.4] 118    49      37       0        32  56.976744   56.407359    860    6.558995         second_back_share
   rushyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         second_back_share
    recyds  over    (-inf, 0.1] 322   125     137       0        60  47.709924 -265.768880   2620  -10.143850        prior_target_share
    recyds  over     (0.1, 0.2] 297   108     113       0        76  48.868778 -181.200037   2210   -8.199097        prior_target_share
    recyds  over     (0.2, 0.3] 124    36      44       0        44  45.000000 -124.690670    800  -15.586334        prior_target_share
    recyds  over     (0.3, inf]  14     4       5       0         5  44.444444  -15.097880     90  -16.775422        prior_target_share
    recyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        prior_target_share
    recyds under    (-inf, 0.1] 322   137     125       0        60  52.290076  -45.515912   2620   -1.737249        prior_target_share
    recyds under     (0.1, 0.2] 297   113     108       0        76  51.131222  -85.070762   2210   -3.849356        prior_target_share
    recyds under     (0.2, 0.3] 124    44      36       0        44  55.000000   28.387158    800    3.548395        prior_target_share
    recyds under     (0.3, inf]  14     5       4       0         5  55.555556    3.862349     90    4.291499        prior_target_share
    recyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        prior_target_share
rushrecyds  over    (-inf, 0.1] 111    24      37       0        50  39.344262 -159.373014    610  -26.126724        prior_target_share
rushrecyds  over     (0.1, 0.2]  63    21      20       0        22  51.219512  -15.173664    410   -3.700894        prior_target_share
rushrecyds  over     (0.2, 0.3]  11     4       2       0         5  66.666667   14.975148     60   24.958580        prior_target_share
rushrecyds  over     (0.3, inf]   1     0       0       0         1        NaN    0.000000      0         NaN        prior_target_share
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN        prior_target_share
rushrecyds under    (-inf, 0.1] 111    37      24       0        50  60.655738   83.583508    610   13.702214        prior_target_share
rushrecyds under     (0.1, 0.2]  63    20      21       0        22  48.780488  -35.046003    410   -8.547806        prior_target_share
rushrecyds under     (0.2, 0.3]  11     2       4       0         5  33.333333  -22.454790     60  -37.424651        prior_target_share
rushrecyds under     (0.3, inf]   1     0       0       0         1        NaN    0.000000      0         NaN        prior_target_share
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN        prior_target_share
   rushyds  over    (-inf, 0.1] 282    98     128       0        56  43.362832 -425.004982   2260  -18.805530        prior_target_share
   rushyds  over     (0.1, 0.2]  63    25      22       0        16  53.191489   -0.437573    470   -0.093101        prior_target_share
   rushyds  over     (0.2, 0.3]  12     3       8       0         1  27.272727  -53.722516    110  -48.838651        prior_target_share
   rushyds  over     (0.3, inf]   1     0       1       0         0   0.000000  -10.000000     10 -100.000000        prior_target_share
   rushyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        prior_target_share
   rushyds under    (-inf, 0.1] 282   128      98       0        56  56.637168  141.706716   2260    6.270209        prior_target_share
   rushyds under     (0.1, 0.2]  63    22      25       0        16  46.808511  -56.937457    470  -12.114353        prior_target_share
   rushyds under     (0.2, 0.3]  12     8       3       0         1  72.727273   39.159457    110   35.599507        prior_target_share
   rushyds under     (0.3, inf]   1     1       0       0         0 100.000000    2.541296     10   25.412961        prior_target_share
   rushyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        prior_target_share
    recyds  over  (-inf, 100.0] 259   110      95       0        54  53.658537   22.835763   2050    1.113940         opp_rush_yds_game
    recyds  over (100.0, 125.0] 287    95     122       0        70  43.778802 -386.795874   2170  -17.824695         opp_rush_yds_game
    recyds  over (125.0, 150.0] 151    53      59       0        39  47.321429 -123.946485   1120  -11.066650         opp_rush_yds_game
    recyds  over   (150.0, inf]  60    15      23       0        22  39.473684  -98.850870    380  -26.013387         opp_rush_yds_game
    recyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         opp_rush_yds_game
    recyds under  (-inf, 100.0] 259    95     110       0        54  46.341463 -266.703717   2050  -13.009937         opp_rush_yds_game
    recyds under (100.0, 125.0] 287   122      95       0        70  56.221198  126.546061   2170    5.831616         opp_rush_yds_game
    recyds under (125.0, 150.0] 151    59      53       0        39  52.678571   -9.754709   1120   -0.870956         opp_rush_yds_game
    recyds under   (150.0, inf]  60    23      15       0        22  60.526316   51.575199    380   13.572421         opp_rush_yds_game
    recyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         opp_rush_yds_game
rushrecyds  over  (-inf, 100.0]  59    17      14       0        28  54.838710    9.011227    310    2.906847         opp_rush_yds_game
rushrecyds  over (100.0, 125.0]  73    22      29       0        22  43.137255  -95.536241    510  -18.732596         opp_rush_yds_game
rushrecyds  over (125.0, 150.0]  38     7      12       0        19  36.842105  -59.259905    190  -31.189424         opp_rush_yds_game
rushrecyds  over   (150.0, inf]  16     3       4       0         9  42.857143  -13.786610     70  -19.695158         opp_rush_yds_game
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN         opp_rush_yds_game
rushrecyds under  (-inf, 100.0]  59    14      17       0        28  45.161290  -47.568971    310  -15.344829         opp_rush_yds_game
rushrecyds under (100.0, 125.0]  73    29      22       0        22  56.862745   33.149369    510    6.499876         opp_rush_yds_game
rushrecyds under (125.0, 150.0]  38    12       7       0        19  63.157895   35.489196    190   18.678524         opp_rush_yds_game
rushrecyds under   (150.0, inf]  16     4       3       0         9  57.142857    5.013120     70    7.161601         opp_rush_yds_game
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN         opp_rush_yds_game
   rushyds  over  (-inf, 100.0] 121    40      55       0        26  42.105263 -206.309941    950  -21.716836         opp_rush_yds_game
   rushyds  over (100.0, 125.0] 136    48      64       0        24  42.857143 -219.267633   1120  -19.577467         opp_rush_yds_game
   rushyds  over (125.0, 150.0]  75    29      29       0        17  50.000000  -35.200015    580   -6.068968         opp_rush_yds_game
   rushyds  over   (150.0, inf]  26     9      11       0         6  45.000000  -28.387481    200  -14.193741         opp_rush_yds_game
   rushyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         opp_rush_yds_game
   rushyds under  (-inf, 100.0] 121    55      40       0        26  57.894737   83.694259    950    8.809922         opp_rush_yds_game
   rushyds under (100.0, 125.0] 136    64      48       0        24  57.142857   80.269547   1120    7.166924         opp_rush_yds_game
   rushyds under (125.0, 150.0]  75    29      29       0        17  50.000000  -44.991779    580   -7.757203         opp_rush_yds_game
   rushyds under   (150.0, inf]  26    11       9       0         6  55.000000    7.497986    200    3.748993         opp_rush_yds_game
   rushyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN         opp_rush_yds_game
    recyds  over    (-inf, 4.0] 333   132     133       0        68  49.811321 -163.004506   2650   -6.151113        opp_rush_yds_carry
    recyds  over     (4.0, 4.5] 203    70      82       0        51  46.052632 -203.751582   1520  -13.404709        opp_rush_yds_carry
    recyds  over     (4.5, 5.0] 125    40      45       0        40  47.058824 -100.510520    850  -11.824767        opp_rush_yds_carry
    recyds  over     (5.0, inf]  96    31      39       0        26  44.285714 -119.490858    700  -17.070123        opp_rush_yds_carry
    recyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        opp_rush_yds_carry
    recyds under    (-inf, 4.0] 333   133     132       0        68  50.188679 -146.233479   2650   -5.518244        opp_rush_yds_carry
    recyds under     (4.0, 4.5] 203    82      70       0        51  53.947368   21.094495   1520    1.387796        opp_rush_yds_carry
    recyds under     (4.5, 5.0] 125    45      40       0        40  52.941176   -5.849519    850   -0.688179        opp_rush_yds_carry
    recyds under     (5.0, inf]  96    39      31       0        26  55.714286   32.651337    700    4.664477        opp_rush_yds_carry
    recyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        opp_rush_yds_carry
rushrecyds  over    (-inf, 4.0]  83    22      25       0        36  46.808511  -57.192961    470  -12.168715        opp_rush_yds_carry
rushrecyds  over     (4.0, 4.5]  51    13      20       0        18  39.393939  -85.049186    330  -25.772481        opp_rush_yds_carry
rushrecyds  over     (4.5, 5.0]  28     7       7       0        14  50.000000   -8.111421    140   -5.793872        opp_rush_yds_carry
rushrecyds  over     (5.0, inf]  24     7       7       0        10  50.000000   -9.217961    140   -6.584258        opp_rush_yds_carry
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN        opp_rush_yds_carry
rushrecyds under    (-inf, 4.0]  83    25      22       0        36  53.191489   -2.171270    470   -0.461972        opp_rush_yds_carry
rushrecyds under     (4.0, 4.5]  51    20      13       0        18  60.606061   45.737241    330   13.859770        opp_rush_yds_carry
rushrecyds under     (4.5, 5.0]  28     7       7       0        14  50.000000   -8.813517    140   -6.295369        opp_rush_yds_carry
rushrecyds under     (5.0, inf]  24     7       7       0        10  50.000000   -8.669740    140   -6.192671        opp_rush_yds_carry
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN        opp_rush_yds_carry
   rushyds  over    (-inf, 4.0] 162    55      73       0        34  42.968750 -244.028866   1280  -19.064755        opp_rush_yds_carry
   rushyds  over     (4.0, 4.5]  90    30      44       0        16  40.540541 -186.845782    740  -25.249430        opp_rush_yds_carry
   rushyds  over     (4.5, 5.0]  64    23      25       0        16  47.916667  -48.705914    480  -10.147065        opp_rush_yds_carry
   rushyds  over     (5.0, inf]  42    18      17       0         7  51.428571   -9.584508    350   -2.738431        opp_rush_yds_carry
   rushyds  over            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        opp_rush_yds_carry
   rushyds under    (-inf, 4.0] 162    73      55       0        34  57.031250   91.145802   1280    7.120766        opp_rush_yds_carry
   rushyds under     (4.0, 4.5]  90    44      30       0        16  59.459459   81.258405    740   10.980866        opp_rush_yds_carry
   rushyds under     (4.5, 5.0]  64    25      23       0        16  52.083333  -16.066109    480   -3.347106        opp_rush_yds_carry
   rushyds under     (5.0, inf]  42    17      18       0         7  48.571429  -29.868086    350   -8.533739        opp_rush_yds_carry
   rushyds under            NaN  14     0       0       0        14        NaN    0.000000      0         NaN        opp_rush_yds_carry
    recyds  over   (-inf, 40.0] 217    90      88       0        39  50.561798  -84.770102   1780   -4.762365 opp_rec_yds_position_game
    recyds  over (120.0, 160.0] 166    48      67       0        51  41.739130 -250.475427   1150  -21.780472 opp_rec_yds_position_game
    recyds  over   (160.0, inf] 143    50      49       0        44  50.505051  -50.325201    990   -5.083354 opp_rec_yds_position_game
    recyds  over   (40.0, 80.0] 139    47      62       0        30  43.119266 -208.531688   1090  -19.131348 opp_rec_yds_position_game
    recyds  over  (80.0, 120.0]  86    36      29       0        21  55.384615   26.773022    650    4.118926 opp_rec_yds_position_game
    recyds  over            NaN  20     2       4       0        14  33.333333  -19.428070     60  -32.380117 opp_rec_yds_position_game
    recyds under   (-inf, 40.0] 217    88      90       0        39  49.438202 -125.496406   1780   -7.050360 opp_rec_yds_position_game
    recyds under (120.0, 160.0] 166    67      48       0        51  58.260870  113.692242   1150    9.886282 opp_rec_yds_position_game
    recyds under   (160.0, inf] 143    49      50       0        44  49.494949  -67.830028    990   -6.851518 opp_rec_yds_position_game
    recyds under   (40.0, 80.0] 139    62      47       0        30  56.880734   74.669142   1090    6.850380 opp_rec_yds_position_game
    recyds under  (80.0, 120.0]  86    29      36       0        21  44.615385 -105.133833    650  -16.174436 opp_rec_yds_position_game
    recyds under            NaN  20     4       2       0        14  66.666667   11.761717     60   19.602862 opp_rec_yds_position_game
rushrecyds  over   (-inf, 40.0] 149    45      43       0        61  51.136364  -34.900343    880   -3.965948 opp_rec_yds_position_game
rushrecyds  over (120.0, 160.0]   3     1       0       0         2 100.000000    8.849558     10   88.495575 opp_rec_yds_position_game
rushrecyds  over   (160.0, inf]   3     1       1       0         1  50.000000   -0.990991     20   -4.954955 opp_rec_yds_position_game
rushrecyds  over   (40.0, 80.0]  27     2      13       0        12  13.333333 -112.529753    150  -75.019835 opp_rec_yds_position_game
rushrecyds  over  (80.0, 120.0]   4     0       2       0         2   0.000000  -20.000000     20 -100.000000 opp_rec_yds_position_game
rushrecyds  over            NaN   2     0       0       0         2        NaN    0.000000      0         NaN opp_rec_yds_position_game
rushrecyds under   (-inf, 40.0] 149    43      45       0        61  48.863636  -74.325682    880   -8.446100 opp_rec_yds_position_game
rushrecyds under (120.0, 160.0]   3     0       1       0         2   0.000000  -10.000000     10 -100.000000 opp_rec_yds_position_game
rushrecyds under   (160.0, inf]   3     1       1       0         1  50.000000   -1.150442     20   -5.752212 opp_rec_yds_position_game
rushrecyds under   (40.0, 80.0]  27    13       2       0        12  86.666667   93.659507    150   62.439672 opp_rec_yds_position_game
rushrecyds under  (80.0, 120.0]   4     2       0       0         2 100.000000   17.899331     20   89.496656 opp_rec_yds_position_game
rushrecyds under            NaN   2     0       0       0         2        NaN    0.000000      0         NaN opp_rec_yds_position_game
   rushyds  over   (-inf, 40.0] 196    76      83       0        37  47.798742 -162.569440   1590  -10.224493 opp_rec_yds_position_game
   rushyds  over (120.0, 160.0]   3     0       3       0         0   0.000000  -30.000000     30 -100.000000 opp_rec_yds_position_game
   rushyds  over   (160.0, inf]   4     2       1       0         1  66.666667    8.129614     30   27.098715 opp_rec_yds_position_game
   rushyds  over   (40.0, 80.0]  35     7      15       0        13  31.818182  -88.282218    220  -40.128281 opp_rec_yds_position_game
   rushyds  over  (80.0, 120.0]   4     0       2       0         2   0.000000  -20.000000     20 -100.000000 opp_rec_yds_position_game
   rushyds  over            NaN 130    41      55       0        34  42.708333 -196.443027    960  -20.462815 opp_rec_yds_position_game
   rushyds under   (-inf, 40.0] 196    83      76       0        37  52.201258  -29.885333   1590   -1.879581 opp_rec_yds_position_game
   rushyds under (120.0, 160.0]   3     3       0       0         0 100.000000   24.590298     30   81.967661 opp_rec_yds_position_game
   rushyds under   (160.0, inf]   4     1       2       0         1  33.333333  -10.950226     30  -36.500754 opp_rec_yds_position_game
   rushyds under   (40.0, 80.0]  35    15       7       0        13  68.181818   62.123091    220   28.237769 opp_rec_yds_position_game
   rushyds under  (80.0, 120.0]   4     2       0       0         2 100.000000   11.124987     20   55.624935 opp_rec_yds_position_game
   rushyds under            NaN 130    55      41       0        34  57.291667   69.467195    960    7.236166 opp_rec_yds_position_game
    recyds  over    (-7.0, 0.0]  69    24      28       0        17  46.153846  -66.003824    520  -12.693043                    spread
    recyds  over   (-inf, -7.0]  29    12      12       0         5  50.000000  -14.646718    240   -6.102799                    spread
    recyds  over     (0.0, 7.0]  73    23      34       0        16  40.350877 -137.274688    570  -24.083279                    spread
    recyds  over     (7.0, inf]  13     3       6       0         4  33.333333  -33.053745     90  -36.726383                    spread
    recyds  over            NaN 587   211     219       0       157  49.069767 -335.778492   4300   -7.808802                    spread
    recyds under    (-7.0, 0.0]  69    28      24       0        17  53.846154    7.958964    520    1.530570                    spread
    recyds under   (-inf, -7.0]  29    12      12       0         5  50.000000  -14.503242    240   -6.043017                    spread
    recyds under     (0.0, 7.0]  73    34      23       0        16  59.649123   69.412577    570   12.177645                    spread
    recyds under     (7.0, inf]  13     6       3       0         4  66.666667   22.369728     90   24.855253                    spread
    recyds under            NaN 587   219     211       0       157  50.930233 -183.575193   4300   -4.269191                    spread
rushrecyds  over    (-7.0, 0.0]  18     6       5       0         7  54.545455    1.757086    110    1.597351                    spread
rushrecyds  over   (-inf, -7.0]   8     3       4       0         1  42.857143  -13.913043     70  -19.875776                    spread
rushrecyds  over     (0.0, 7.0]  17     4      11       0         2  26.666667  -75.440997    150  -50.293998                    spread
rushrecyds  over     (7.0, inf]   4     0       2       0         2   0.000000  -20.000000     20 -100.000000                    spread
rushrecyds  over            NaN 141    36      37       0        68  49.315068  -51.974575    730   -7.119805                    spread
rushrecyds under    (-7.0, 0.0]  18     5       6       0         7  45.454545  -16.291556    110  -14.810506                    spread
rushrecyds under   (-inf, -7.0]   8     4       3       0         1  57.142857    4.572845     70    6.532636                    spread
rushrecyds under     (0.0, 7.0]  17    11       4       0         2  73.333333   56.282449    150   37.521632                    spread
rushrecyds under     (7.0, inf]   4     2       0       0         2 100.000000   17.391304     20   86.956522                    spread
rushrecyds under            NaN 141    37      36       0        68  50.684932  -35.872328    730   -4.914017                    spread
   rushyds  over    (-7.0, 0.0]  33    13      11       0         9  54.166667    3.681366    240    1.533903                    spread
   rushyds  over   (-inf, -7.0]  13     4       7       0         2  36.363636  -35.251760    110  -32.047054                    spread
   rushyds  over     (0.0, 7.0]  33     8      16       0         9  33.333333  -90.373726    240  -37.655719                    spread
   rushyds  over     (7.0, inf]   6     2       1       0         3  66.666667    7.858567     30   26.195222                    spread
   rushyds  over            NaN 287    99     124       0        64  44.394619 -375.079518   2230  -16.819709                    spread
   rushyds under    (-7.0, 0.0]  33    11      13       0         9  45.833333  -40.531885    240  -16.888286                    spread
   rushyds under   (-inf, -7.0]  13     7       4       0         2  63.636364   18.093065    110   16.448241                    spread
   rushyds under     (0.0, 7.0]  33    16       8       0         9  66.666667   58.908948    240   24.545395                    spread
   rushyds under     (7.0, inf]   6     1       2       0         3  33.333333  -11.304348     30  -37.681159                    spread
   rushyds under            NaN 287   124      99       0        64  55.605381  101.304232   2230    4.542791                    spread
    recyds  over   (-inf, 20.0]  56    18      29       0         9  38.297872 -130.709276    470  -27.810484        implied_team_total
    recyds  over   (20.0, 25.0]  81    30      34       0        17  46.875000  -73.757422    640  -11.524597        implied_team_total
    recyds  over   (25.0, 30.0]  40    13      14       0        13  48.148148  -25.562050    270   -9.467426        implied_team_total
    recyds  over    (30.0, inf]   7     1       3       0         3  25.000000  -20.950226     40  -52.375566        implied_team_total
    recyds  over            NaN 587   211     219       0       157  49.069767 -335.778492   4300   -7.808802        implied_team_total
    recyds under   (-inf, 20.0]  56    29      18       0         9  61.702128   75.047279    470   15.967506        implied_team_total
    recyds under   (20.0, 25.0]  81    34      30       0        17  53.125000   -0.034908    640   -0.005454        implied_team_total
    recyds under   (25.0, 30.0]  40    14      13       0        13  51.851852   -6.323363    270   -2.341986        implied_team_total
    recyds under    (30.0, inf]   7     3       1       0         3  75.000000   16.549019     40   41.372548        implied_team_total
    recyds under            NaN 587   219     211       0       157  50.930233 -183.575193   4300   -4.269191        implied_team_total
rushrecyds  over   (-inf, 20.0]  14     4       7       0         3  36.363636  -35.440997    110  -32.219089        implied_team_total
rushrecyds  over   (20.0, 25.0]  21     6      10       0         5  37.500000  -48.396819    160  -30.248012        implied_team_total
rushrecyds  over   (25.0, 30.0]   9     2       4       0         3  33.333333  -22.454790     60  -37.424651        implied_team_total
rushrecyds  over    (30.0, inf]   3     1       1       0         1  50.000000   -1.304348     20   -6.521739        implied_team_total
rushrecyds  over            NaN 141    36      37       0        68  49.315068  -51.974575    730   -7.119805        implied_team_total
rushrecyds under   (-inf, 20.0]  14     7       4       0         3  63.636364   21.644638    110   19.676944        implied_team_total
rushrecyds under   (20.0, 25.0]  21    10       6       0         5  62.500000   26.603310    160   16.627069        implied_team_total
rushrecyds under   (25.0, 30.0]   9     4       2       0         3  66.666667   14.935164     60   24.891940        implied_team_total
rushrecyds under    (30.0, inf]   3     1       1       0         1  50.000000   -1.228070     20   -6.140351        implied_team_total
rushrecyds under            NaN 141    37      36       0        68  50.684932  -35.872328    730   -4.914017        implied_team_total
   rushyds  over   (-inf, 20.0]  23     7       7       0         9  50.000000   -8.318740    140   -5.941957        implied_team_total
   rushyds  over   (20.0, 25.0]  39    16      17       0         6  48.484848  -30.612616    330   -9.276550        implied_team_total
   rushyds  over   (25.0, 30.0]  19     4       7       0         8  36.363636  -35.154197    110  -31.958361        implied_team_total
   rushyds  over    (30.0, inf]   4     0       4       0         0   0.000000  -40.000000     40 -100.000000        implied_team_total
   rushyds  over            NaN 287    99     124       0        64  44.394619 -375.079518   2230  -16.819709        implied_team_total
   rushyds under   (-inf, 20.0]  23     7       7       0         9  50.000000   -7.801024    140   -5.572160        implied_team_total
   rushyds under   (20.0, 25.0]  39    17      16       0         6  51.515152  -19.401887    330   -5.879360        implied_team_total
   rushyds under   (25.0, 30.0]  19     7       4       0         8  63.636364   20.749407    110   18.863097        implied_team_total
   rushyds under    (30.0, inf]   4     4       0       0         0 100.000000   31.619284     40   79.048209        implied_team_total
   rushyds under            NaN 287   124      99       0        64  55.605381  101.304232   2230    4.542791        implied_team_total
