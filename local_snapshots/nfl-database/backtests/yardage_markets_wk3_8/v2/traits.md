# Weeks 3–6 traits only

Exploratory univariate splits; missing features are separate nan buckets. Hit% excludes pushes and ungraded; ROI uses settled $10 stakes. No holdout outcomes used.

    market  side           bucket   n  wins  losses  pushes  ungraded          pl  stake    hit_pct         roi             feature
    recyds  over     (-15.0, 0.0] 273   104     103       0        66 -114.441691 2070.0  50.241546   -5.528584          model_edge
    recyds  over    (-inf, -15.0]  58    15      21       0        22  -78.170915  360.0  41.666667  -21.714143          model_edge
    recyds  over       (0.0, 5.0] 147    46      61       0        40 -204.669912 1070.0  42.990654  -19.128029          model_edge
    recyds  over     (10.0, 15.0]  59    26      22       0        11    9.213073  480.0  54.166667    1.919390          model_edge
    recyds  over     (15.0, 20.0]  33    12      13       0         8  -25.084943  250.0  48.000000  -10.033977          model_edge
    recyds  over      (20.0, inf]  66    27      26       0        13  -23.843964  530.0  50.943396   -4.498861          model_edge
    recyds  over      (5.0, 10.0] 121    43      53       0        25 -149.759114  960.0  44.791667  -15.599908          model_edge
    recyds  over              NaN  14     3       7       0         4  -40.894737  100.0  30.000000  -40.894737          model_edge
    recyds under     (-15.0, 0.0] 331   136     117       0        78   27.127971 2530.0  53.754941    1.072252          model_edge
    recyds under    (-inf, -15.0]  99    39      39       0        21  -46.723249  780.0  50.000000   -5.990160          model_edge
    recyds under       (0.0, 5.0] 129    52      52       0        25  -65.697730 1040.0  50.000000   -6.317089          model_edge
    recyds under     (10.0, 15.0]  46    14      17       0        15  -46.622218  310.0  45.161290  -15.039425          model_edge
    recyds under     (15.0, 20.0]  23     9       7       0         7    9.671450  160.0  56.250000    6.044656          model_edge
    recyds under      (20.0, inf]  34    12       8       0        14   25.506168  200.0  60.000000   12.753084          model_edge
    recyds under      (5.0, 10.0]  95    37      33       0        25   -1.599557  700.0  52.857143   -0.228508          model_edge
    recyds under              NaN  14     7       3       0         4   29.734092  100.0  70.000000   29.734092          model_edge
rushrecyds  over     (-15.0, 0.0]  68    20      21       0        27  -34.853612  410.0  48.780488   -8.500881          model_edge
rushrecyds  over    (-inf, -15.0]  43    12      15       0        16  -44.317113  270.0  44.444444  -16.413746          model_edge
rushrecyds  over       (0.0, 5.0]  16     4       4       0         8   -4.558251   80.0  50.000000   -5.697814          model_edge
rushrecyds  over     (10.0, 15.0]  10     0       6       0         4  -60.000000   60.0   0.000000 -100.000000          model_edge
rushrecyds  over     (15.0, 20.0]  15     2       4       0         9  -22.339181   60.0  33.333333  -37.231969          model_edge
rushrecyds  over      (20.0, inf]  16     5       4       0         7    3.862349   90.0  55.555556    4.291499          model_edge
rushrecyds  over      (5.0, 10.0]  18     6       5       0         7    2.634279  110.0  54.545455    2.394799          model_edge
rushrecyds  over              NaN   2     0       1       0         1  -10.000000   10.0   0.000000 -100.000000          model_edge
rushrecyds under     (-15.0, 0.0]  45    16      11       0        18   30.038108  270.0  59.259259   11.125225          model_edge
rushrecyds under    (-inf, -15.0]  32     8       7       0        17   -0.308716  150.0  53.333333   -0.205811          model_edge
rushrecyds under       (0.0, 5.0]  20     6       4       0        10   13.027723  100.0  60.000000   13.027723          model_edge
rushrecyds under     (10.0, 15.0]  26    10      10       0         6  -12.470212  200.0  50.000000   -6.235106          model_edge
rushrecyds under     (15.0, 20.0]  10     2       1       0         7    7.507566   30.0  66.666667   25.025221          model_edge
rushrecyds under      (20.0, inf]  33    13      11       0         9    3.811655  240.0  54.166667    1.588190          model_edge
rushrecyds under      (5.0, 10.0]  20     4       5       0        11  -15.523409   90.0  44.444444  -17.248232          model_edge
rushrecyds under              NaN   2     1       0       0         1    8.547009   10.0 100.000000   85.470085          model_edge
   rushyds  over     (-15.0, 0.0] 144    54      62       0        28 -144.580203 1160.0  46.551724  -12.463811          model_edge
   rushyds  over    (-inf, -15.0]  42    12      18       0        12  -74.185526  300.0  40.000000  -24.728509          model_edge
   rushyds  over       (0.0, 5.0]  84    30      36       0        18 -103.834491  660.0  45.454545  -15.732499          model_edge
   rushyds  over     (10.0, 15.0]  24    10      11       0         3  -22.531581  210.0  47.619048  -10.729324          model_edge
   rushyds  over     (15.0, 20.0]  13     6       5       0         2    3.190940  110.0  54.545455    2.900855          model_edge
   rushyds  over      (20.0, inf]  13     4       6       0         3  -24.984249  100.0  40.000000  -24.984249          model_edge
   rushyds  over      (5.0, 10.0]  38    10      21       0         7 -122.239960  310.0  32.258065  -39.432245          model_edge
   rushyds  over              NaN  14     1       8       0         5  -70.909091   90.0  11.111111  -78.787879          model_edge
   rushyds under     (-15.0, 0.0] 148    69      50       0        29   99.454297 1190.0  57.983193    8.357504          model_edge
   rushyds under    (-inf, -15.0]  26    11      10       0         5   -3.408665  210.0  52.380952   -1.623174          model_edge
   rushyds under       (0.0, 5.0]  72    32      32       0         8  -42.007223  640.0  50.000000   -6.563629          model_edge
   rushyds under     (10.0, 15.0]  29    12       6       0        11   44.973906  180.0  66.666667   24.985503          model_edge
   rushyds under     (15.0, 20.0]  23    11       7       0         5   26.637588  180.0  61.111111   14.798660          model_edge
   rushyds under      (20.0, inf]  18     7       5       0         6   11.690267  120.0  58.333333    9.741889          model_edge
   rushyds under      (5.0, 10.0]  42    17      16       0         9  -10.870157  330.0  51.515152   -3.293987          model_edge
   rushyds under              NaN  14     8       1       0         5   61.123830   90.0  88.888889   67.915367          model_edge
    recyds  over     (-inf, 25.0] 416   163     185       0        68 -409.008406 3480.0  46.839080  -11.753115                line
    recyds  over     (25.0, 50.0] 235    79      81       0        75 -116.211278 1600.0  49.375000   -7.263205                line
    recyds  over     (50.0, 75.0]  87    24      28       0        35  -69.932599  520.0  46.153846  -13.448577                line
    recyds  over    (75.0, 100.0]  33    10      12       0        11  -32.499920  220.0  45.454545  -14.772691                line
    recyds under     (-inf, 25.0] 416   185     163       0        68   -5.243991 3480.0  53.160920   -0.150689                line
    recyds under     (25.0, 50.0] 235    81      79       0        75  -75.432522 1600.0  50.625000   -4.714533                line
    recyds under     (50.0, 75.0]  87    28      24       0        35    6.412585  520.0  53.846154    1.233189                line
    recyds under    (75.0, 100.0]  33    12      10       0        11    5.660855  220.0  54.545455    2.573116                line
rushrecyds  over     (-inf, 25.0]   8     1       4       0         3  -31.189427   50.0  20.000000  -62.378855                line
rushrecyds  over     (100.0, inf]  24    12       4       0         8   65.744404  160.0  75.000000   41.090253                line
rushrecyds  over     (25.0, 50.0]  56    12      21       0        23 -104.759397  330.0  36.363636  -31.745272                line
rushrecyds  over     (50.0, 75.0]  50    13      18       0        19  -65.794322  310.0  41.935484  -21.223975                line
rushrecyds  over    (75.0, 100.0]  50    11      13       0        26  -33.572788  240.0  45.833333  -13.988662                line
rushrecyds under     (-inf, 25.0]   8     4       1       0         3   24.650473   50.0  80.000000   49.300946                line
rushrecyds under     (100.0, inf]  24     4      12       0         8  -84.830567  160.0  25.000000  -53.019104                line
rushrecyds under     (25.0, 50.0]  56    21      12       0        23   64.159386  330.0  63.636364   19.442238                line
rushrecyds under     (50.0, 75.0]  50    18      13       0        19   27.843589  310.0  58.064516    8.981803                line
rushrecyds under    (75.0, 100.0]  50    13      11       0        26    2.806842  240.0  54.166667    1.169518                line
   rushyds  over     (-inf, 25.0] 193    72      91       0        30 -283.091484 1630.0  44.171779  -17.367576                line
   rushyds  over     (25.0, 50.0]  90    20      43       0        27 -253.491241  630.0  31.746032  -40.236705                line
   rushyds  over     (50.0, 75.0]  65    23      23       0        19  -28.771770  460.0  50.000000   -6.254733                line
   rushyds  over    (75.0, 100.0]  24    12      10       0         2    5.280332  220.0  54.545455    2.400151                line
   rushyds under     (-inf, 25.0] 193    91      72       0        30   69.530475 1630.0  55.828221    4.265673                line
   rushyds under     (25.0, 50.0]  90    43      20       0        27  177.818259  630.0  68.253968   28.225121                line
   rushyds under     (50.0, 75.0]  65    23      23       0        19  -27.264087  460.0  50.000000   -5.926976                line
   rushyds under    (75.0, 100.0]  24    10      12       0         2  -32.490805  220.0  45.454545  -14.768548                line
    recyds  over    (-110.0, 0.0]  14     8       6       0         0   15.413633  140.0  57.142857   11.009738               price
    recyds  over (-150.0, -110.0] 562   265     297       0         0 -647.665836 5620.0  47.153025  -11.524303               price
    recyds  over     (0.0, 150.0]   6     3       3       0         0    4.600000   60.0  50.000000    7.666667               price
    recyds  over              NaN 189     0       0       0       189    0.000000    0.0        NaN         NaN               price
    recyds under    (-110.0, 0.0]  18     9       9       0         0   -6.513113  180.0  50.000000   -3.618396               price
    recyds under (-150.0, -110.0] 560   295     265       0         0  -54.009927 5600.0  52.678571   -0.964463               price
    recyds under   (-inf, -150.0]   4     2       2       0         0   -8.080034   40.0  50.000000  -20.200085               price
    recyds under              NaN 189     0       0       0       189    0.000000    0.0        NaN         NaN               price
rushrecyds  over    (-110.0, 0.0]   2     1       1       0         0   -0.825688   20.0  50.000000   -4.128440               price
rushrecyds  over (-150.0, -110.0] 107    48      59       0         0 -168.745842 1070.0  44.859813  -15.770639               price
rushrecyds  over              NaN  79     0       0       0        79    0.000000    0.0        NaN         NaN               price
rushrecyds under    (-110.0, 0.0]   1     1       0       0         0    9.174312   10.0 100.000000   91.743119               price
rushrecyds under (-150.0, -110.0] 108    59      49       0         0   25.455411 1080.0  54.629630    2.356982               price
rushrecyds under              NaN  79     0       0       0        79    0.000000    0.0        NaN         NaN               price
   rushyds  over    (-110.0, 0.0]  14     4      10       0         0  -62.830141  140.0  28.571429  -44.878672               price
   rushyds  over (-150.0, -110.0] 273   120     153       0         0 -480.044021 2730.0  43.956044  -17.584030               price
   rushyds  over     (0.0, 150.0]   6     3       3       0         0   -7.200000   60.0  50.000000  -12.000000               price
   rushyds  over     (150.0, inf]   1     0       1       0         0  -10.000000   10.0   0.000000 -100.000000               price
   rushyds  over              NaN  78     0       0       0        78    0.000000    0.0        NaN         NaN               price
   rushyds under    (-110.0, 0.0]  11     5       6       0         0  -13.336706  110.0  45.454545  -12.124279               price
   rushyds under (-150.0, -110.0] 279   159     120       0         0  195.229079 2790.0  56.989247    6.997458               price
   rushyds under   (-inf, -150.0]   4     3       1       0         0    5.701469   40.0  75.000000   14.253673               price
   rushyds under              NaN  78     0       0       0        78    0.000000    0.0        NaN         NaN               price
    recyds  over      (-inf, 0.1] 593   206     227       0       160 -457.326352 4330.0  47.575058  -10.561810   prior_carry_share
    recyds  over      (0.1, 0.25]  37    15      16       0         6  -27.823912  310.0  48.387097   -8.975456   prior_carry_share
    recyds  over      (0.25, 0.5]  55    28      19       0         8   56.334781  470.0  59.574468   11.986124   prior_carry_share
    recyds  over      (0.5, 0.75]  66    21      34       0        11 -154.494852  550.0  38.181818  -28.089973   prior_carry_share
    recyds  over      (0.75, inf]   6     3       3       0         0   -3.447131   60.0  50.000000   -5.745219   prior_carry_share
    recyds  over              NaN  14     3       7       0         4  -40.894737  100.0  30.000000  -40.894737   prior_carry_share
    recyds under      (-inf, 0.1] 593   227     206       0       160  -63.948879 4330.0  52.424942   -1.476879   prior_carry_share
    recyds under      (0.1, 0.25]  37    16      15       0         6   -8.076160  310.0  51.612903   -2.605213   prior_carry_share
    recyds under      (0.25, 0.5]  55    19      28       0         8 -112.735410  470.0  40.425532  -23.986257   prior_carry_share
    recyds under      (0.5, 0.75]  66    34      21       0        11   89.908050  550.0  61.818182   16.346918   prior_carry_share
    recyds under      (0.75, inf]   6     3       3       0         0   -3.484766   60.0  50.000000   -5.807944   prior_carry_share
    recyds under              NaN  14     7       3       0         4   29.734092  100.0  70.000000   29.734092   prior_carry_share
rushrecyds  over      (-inf, 0.1]  23     5       8       0        10  -35.187939  130.0  38.461538  -27.067645   prior_carry_share
rushrecyds  over      (0.1, 0.25]  36     6      13       0        17  -78.383052  190.0  31.578947  -41.254238   prior_carry_share
rushrecyds  over      (0.25, 0.5]  55    16      19       0        20  -49.163799  350.0  45.714286  -14.046800   prior_carry_share
rushrecyds  over      (0.5, 0.75]  66    20      18       0        28   -4.575186  380.0  52.631579   -1.203996   prior_carry_share
rushrecyds  over      (0.75, inf]   6     2       1       0         3    7.738446   30.0  66.666667   25.794821   prior_carry_share
rushrecyds  over              NaN   2     0       1       0         1  -10.000000   10.0   0.000000 -100.000000   prior_carry_share
rushrecyds under      (-inf, 0.1]  23     8       5       0        10   20.457333  130.0  61.538462   15.736410   prior_carry_share
rushrecyds under      (0.1, 0.25]  36    13       6       0        17   53.795860  190.0  68.421053   28.313611   prior_carry_share
rushrecyds under      (0.25, 0.5]  55    19      16       0        20    5.404504  350.0  54.285714    1.544144   prior_carry_share
rushrecyds under      (0.5, 0.75]  66    18      20       0        28  -42.503553  380.0  47.368421  -11.185146   prior_carry_share
rushrecyds under      (0.75, inf]   6     1       2       0         3  -11.071429   30.0  33.333333  -36.904762   prior_carry_share
rushrecyds under              NaN   2     1       0       0         1    8.547009   10.0 100.000000   85.470085   prior_carry_share
   rushyds  over      (-inf, 0.1]  88    30      41       0        17 -154.940416  710.0  42.253521  -21.822594   prior_carry_share
   rushyds  over      (0.1, 0.25] 120    44      60       0        16 -210.520071 1040.0  42.307692  -20.242315   prior_carry_share
   rushyds  over      (0.25, 0.5]  76    27      23       0        26    7.625802  500.0  54.000000    1.525160   prior_carry_share
   rushyds  over      (0.5, 0.75]  68    23      32       0        13 -118.609729  550.0  41.818182  -21.565405   prior_carry_share
   rushyds  over      (0.75, inf]   6     2       3       0         1  -12.720657   50.0  40.000000  -25.441314   prior_carry_share
   rushyds  over              NaN  14     1       8       0         5  -70.909091   90.0  11.111111  -78.787879   prior_carry_share
   rushyds under      (-inf, 0.1]  88    41      30       0        17   48.793578  710.0  57.746479    6.872335   prior_carry_share
   rushyds under      (0.1, 0.25] 120    60      44       0        16   87.357160 1040.0  57.692308    8.399727   prior_carry_share
   rushyds under      (0.25, 0.5]  76    23      27       0        26  -67.510736  500.0  46.000000  -13.502147   prior_carry_share
   rushyds under      (0.5, 0.75]  68    32      23       0        13   51.551855  550.0  58.181818    9.373064   prior_carry_share
   rushyds under      (0.75, inf]   6     3       2       0         1    6.278155   50.0  60.000000   12.556309   prior_carry_share
   rushyds under              NaN  14     8       1       0         5   61.123830   90.0  88.888889   67.915367   prior_carry_share
    recyds  over      (-inf, 0.1] 322   125     137       0        60 -265.768880 2620.0  47.709924  -10.143850  prior_target_share
    recyds  over       (0.1, 0.2] 297   108     113       0        76 -181.200037 2210.0  48.868778   -8.199097  prior_target_share
    recyds  over       (0.2, 0.3] 124    36      44       0        44 -124.690670  800.0  45.000000  -15.586334  prior_target_share
    recyds  over       (0.3, inf]  14     4       5       0         5  -15.097880   90.0  44.444444  -16.775422  prior_target_share
    recyds  over              NaN  14     3       7       0         4  -40.894737  100.0  30.000000  -40.894737  prior_target_share
    recyds under      (-inf, 0.1] 322   137     125       0        60  -45.515912 2620.0  52.290076   -1.737249  prior_target_share
    recyds under       (0.1, 0.2] 297   113     108       0        76  -85.070762 2210.0  51.131222   -3.849356  prior_target_share
    recyds under       (0.2, 0.3] 124    44      36       0        44   28.387158  800.0  55.000000    3.548395  prior_target_share
    recyds under       (0.3, inf]  14     5       4       0         5    3.862349   90.0  55.555556    4.291499  prior_target_share
    recyds under              NaN  14     7       3       0         4   29.734092  100.0  70.000000   29.734092  prior_target_share
rushrecyds  over      (-inf, 0.1] 111    24      37       0        50 -159.373014  610.0  39.344262  -26.126724  prior_target_share
rushrecyds  over       (0.1, 0.2]  63    21      20       0        22  -15.173664  410.0  51.219512   -3.700894  prior_target_share
rushrecyds  over       (0.2, 0.3]  11     4       2       0         5   14.975148   60.0  66.666667   24.958580  prior_target_share
rushrecyds  over       (0.3, inf]   1     0       0       0         1    0.000000    0.0        NaN         NaN  prior_target_share
rushrecyds  over              NaN   2     0       1       0         1  -10.000000   10.0   0.000000 -100.000000  prior_target_share
rushrecyds under      (-inf, 0.1] 111    37      24       0        50   83.583508  610.0  60.655738   13.702214  prior_target_share
rushrecyds under       (0.1, 0.2]  63    20      21       0        22  -35.046003  410.0  48.780488   -8.547806  prior_target_share
rushrecyds under       (0.2, 0.3]  11     2       4       0         5  -22.454790   60.0  33.333333  -37.424651  prior_target_share
rushrecyds under       (0.3, inf]   1     0       0       0         1    0.000000    0.0        NaN         NaN  prior_target_share
rushrecyds under              NaN   2     1       0       0         1    8.547009   10.0 100.000000   85.470085  prior_target_share
   rushyds  over      (-inf, 0.1] 282    98     128       0        56 -425.004982 2260.0  43.362832  -18.805530  prior_target_share
   rushyds  over       (0.1, 0.2]  63    25      22       0        16   -0.437573  470.0  53.191489   -0.093101  prior_target_share
   rushyds  over       (0.2, 0.3]  12     3       8       0         1  -53.722516  110.0  27.272727  -48.838651  prior_target_share
   rushyds  over       (0.3, inf]   1     0       1       0         0  -10.000000   10.0   0.000000 -100.000000  prior_target_share
   rushyds  over              NaN  14     1       8       0         5  -70.909091   90.0  11.111111  -78.787879  prior_target_share
   rushyds under      (-inf, 0.1] 282   128      98       0        56  141.706716 2260.0  56.637168    6.270209  prior_target_share
   rushyds under       (0.1, 0.2]  63    22      25       0        16  -56.937457  470.0  46.808511  -12.114353  prior_target_share
   rushyds under       (0.2, 0.3]  12     8       3       0         1   39.159457  110.0  72.727273   35.599507  prior_target_share
   rushyds under       (0.3, inf]   1     1       0       0         0    2.541296   10.0 100.000000   25.412961  prior_target_share
   rushyds under              NaN  14     8       1       0         5   61.123830   90.0  88.888889   67.915367  prior_target_share
    recyds  over      (-7.0, 0.0]  69    24      28       0        17  -66.003824  520.0  46.153846  -12.693043              spread
    recyds  over     (-inf, -7.0]  29    12      12       0         5  -14.646718  240.0  50.000000   -6.102799              spread
    recyds  over       (0.0, 7.0]  73    23      34       0        16 -137.274688  570.0  40.350877  -24.083279              spread
    recyds  over       (7.0, inf]  13     3       6       0         4  -33.053745   90.0  33.333333  -36.726383              spread
    recyds  over              NaN 587   214     226       0       147 -376.673229 4400.0  48.636364   -8.560755              spread
    recyds under      (-7.0, 0.0]  69    28      24       0        17    7.958964  520.0  53.846154    1.530570              spread
    recyds under     (-inf, -7.0]  29    12      12       0         5  -14.503242  240.0  50.000000   -6.043017              spread
    recyds under       (0.0, 7.0]  73    34      23       0        16   69.412577  570.0  59.649123   12.177645              spread
    recyds under       (7.0, inf]  13     6       3       0         4   22.369728   90.0  66.666667   24.855253              spread
    recyds under              NaN 587   226     214       0       147 -153.841101 4400.0  51.363636   -3.496389              spread
rushrecyds  over      (-7.0, 0.0]  18     6       5       0         7    1.757086  110.0  54.545455    1.597351              spread
rushrecyds  over     (-inf, -7.0]   8     3       4       0         1  -13.913043   70.0  42.857143  -19.875776              spread
rushrecyds  over       (0.0, 7.0]  17     4      11       0         2  -75.440997  150.0  26.666667  -50.293998              spread
rushrecyds  over       (7.0, inf]   4     0       2       0         2  -20.000000   20.0   0.000000 -100.000000              spread
rushrecyds  over              NaN 141    36      38       0        67  -61.974575  740.0  48.648649   -8.374943              spread
rushrecyds under      (-7.0, 0.0]  18     5       6       0         7  -16.291556  110.0  45.454545  -14.810506              spread
rushrecyds under     (-inf, -7.0]   8     4       3       0         1    4.572845   70.0  57.142857    6.532636              spread
rushrecyds under       (0.0, 7.0]  17    11       4       0         2   56.282449  150.0  73.333333   37.521632              spread
rushrecyds under       (7.0, inf]   4     2       0       0         2   17.391304   20.0 100.000000   86.956522              spread
rushrecyds under              NaN 141    38      36       0        67  -27.325319  740.0  51.351351   -3.692611              spread
   rushyds  over      (-7.0, 0.0]  33    13      11       0         9    3.681366  240.0  54.166667    1.533903              spread
   rushyds  over     (-inf, -7.0]  13     4       7       0         2  -35.251760  110.0  36.363636  -32.047054              spread
   rushyds  over       (0.0, 7.0]  33     8      16       0         9  -90.373726  240.0  33.333333  -37.655719              spread
   rushyds  over       (7.0, inf]   6     2       1       0         3    7.858567   30.0  66.666667   26.195222              spread
   rushyds  over              NaN 287   100     132       0        55 -445.988609 2320.0  43.103448  -19.223647              spread
   rushyds under      (-7.0, 0.0]  33    11      13       0         9  -40.531885  240.0  45.833333  -16.888286              spread
   rushyds under     (-inf, -7.0]  13     7       4       0         2   18.093065  110.0  63.636364   16.448241              spread
   rushyds under       (0.0, 7.0]  33    16       8       0         9   58.908948  240.0  66.666667   24.545395              spread
   rushyds under       (7.0, inf]   6     1       2       0         3  -11.304348   30.0  33.333333  -37.681159              spread
   rushyds under              NaN 287   132     100       0        55  162.428063 2320.0  56.896552    7.001210              spread
    recyds  over     (-inf, 20.0]  56    18      29       0         9 -130.709276  470.0  38.297872  -27.810484  implied_team_total
    recyds  over     (20.0, 25.0]  81    30      34       0        17  -73.757422  640.0  46.875000  -11.524597  implied_team_total
    recyds  over     (25.0, 30.0]  40    13      14       0        13  -25.562050  270.0  48.148148   -9.467426  implied_team_total
    recyds  over      (30.0, inf]   7     1       3       0         3  -20.950226   40.0  25.000000  -52.375566  implied_team_total
    recyds  over              NaN 587   214     226       0       147 -376.673229 4400.0  48.636364   -8.560755  implied_team_total
    recyds under     (-inf, 20.0]  56    29      18       0         9   75.047279  470.0  61.702128   15.967506  implied_team_total
    recyds under     (20.0, 25.0]  81    34      30       0        17   -0.034908  640.0  53.125000   -0.005454  implied_team_total
    recyds under     (25.0, 30.0]  40    14      13       0        13   -6.323363  270.0  51.851852   -2.341986  implied_team_total
    recyds under      (30.0, inf]   7     3       1       0         3   16.549019   40.0  75.000000   41.372548  implied_team_total
    recyds under              NaN 587   226     214       0       147 -153.841101 4400.0  51.363636   -3.496389  implied_team_total
rushrecyds  over     (-inf, 20.0]  14     4       7       0         3  -35.440997  110.0  36.363636  -32.219089  implied_team_total
rushrecyds  over     (20.0, 25.0]  21     6      10       0         5  -48.396819  160.0  37.500000  -30.248012  implied_team_total
rushrecyds  over     (25.0, 30.0]   9     2       4       0         3  -22.454790   60.0  33.333333  -37.424651  implied_team_total
rushrecyds  over      (30.0, inf]   3     1       1       0         1   -1.304348   20.0  50.000000   -6.521739  implied_team_total
rushrecyds  over              NaN 141    36      38       0        67  -61.974575  740.0  48.648649   -8.374943  implied_team_total
rushrecyds under     (-inf, 20.0]  14     7       4       0         3   21.644638  110.0  63.636364   19.676944  implied_team_total
rushrecyds under     (20.0, 25.0]  21    10       6       0         5   26.603310  160.0  62.500000   16.627069  implied_team_total
rushrecyds under     (25.0, 30.0]   9     4       2       0         3   14.935164   60.0  66.666667   24.891940  implied_team_total
rushrecyds under      (30.0, inf]   3     1       1       0         1   -1.228070   20.0  50.000000   -6.140351  implied_team_total
rushrecyds under              NaN 141    38      36       0        67  -27.325319  740.0  51.351351   -3.692611  implied_team_total
   rushyds  over     (-inf, 20.0]  23     7       7       0         9   -8.318740  140.0  50.000000   -5.941957  implied_team_total
   rushyds  over     (20.0, 25.0]  39    16      17       0         6  -30.612616  330.0  48.484848   -9.276550  implied_team_total
   rushyds  over     (25.0, 30.0]  19     4       7       0         8  -35.154197  110.0  36.363636  -31.958361  implied_team_total
   rushyds  over      (30.0, inf]   4     0       4       0         0  -40.000000   40.0   0.000000 -100.000000  implied_team_total
   rushyds  over              NaN 287   100     132       0        55 -445.988609 2320.0  43.103448  -19.223647  implied_team_total
   rushyds under     (-inf, 20.0]  23     7       7       0         9   -7.801024  140.0  50.000000   -5.572160  implied_team_total
   rushyds under     (20.0, 25.0]  39    17      16       0         6  -19.401887  330.0  51.515152   -5.879360  implied_team_total
   rushyds under     (25.0, 30.0]  19     7       4       0         8   20.749407  110.0  63.636364   18.863097  implied_team_total
   rushyds under      (30.0, inf]   4     4       0       0         0   31.619284   40.0 100.000000   79.048209  implied_team_total
   rushyds under              NaN 287   132     100       0        55  162.428063 2320.0  56.896552    7.001210  implied_team_total
    recyds  over   (100.0, 150.0]  10     3       3       0         4   -3.606583   60.0  50.000000   -6.010971 opp_prior_allowance
    recyds  over   (150.0, 200.0] 143    59      52       0        32    0.620473 1110.0  53.153153    0.055898 opp_prior_allowance
    recyds  over   (200.0, 250.0] 381   125     158       0        98 -481.486188 2830.0  44.169611  -17.013646 opp_prior_allowance
    recyds  over     (250.0, inf] 223    86      86       0        51 -102.285169 1720.0  50.000000   -5.946812 opp_prior_allowance
    recyds  over              NaN  14     3       7       0         4  -40.894737  100.0  30.000000  -40.894737 opp_prior_allowance
    recyds under   (100.0, 150.0]  10     3       3       0         4   -3.721166   60.0  50.000000   -6.201943 opp_prior_allowance
    recyds under   (150.0, 200.0] 143    52      59       0        32 -132.607230 1110.0  46.846847  -11.946597 opp_prior_allowance
    recyds under   (200.0, 250.0] 381   158     125       0        98  144.282804 2830.0  55.830389    5.098332 opp_prior_allowance
    recyds under     (250.0, inf] 223    86      86       0        51 -106.291574 1720.0  50.000000   -6.179743 opp_prior_allowance
    recyds under              NaN  14     7       3       0         4   29.734092  100.0  70.000000   29.734092 opp_prior_allowance
rushrecyds  over   (200.0, 250.0]   4     1       0       0         3    8.888889   10.0 100.000000   88.888889 opp_prior_allowance
rushrecyds  over     (250.0, inf] 182    48      59       0        75 -168.460419 1070.0  44.859813  -15.743964 opp_prior_allowance
rushrecyds  over              NaN   2     0       1       0         1  -10.000000   10.0   0.000000 -100.000000 opp_prior_allowance
rushrecyds under   (200.0, 250.0]   4     0       1       0         3  -10.000000   10.0   0.000000 -100.000000 opp_prior_allowance
rushrecyds under     (250.0, inf] 182    59      48       0        75   36.082714 1070.0  55.140187    3.372216 opp_prior_allowance
rushrecyds under              NaN   2     1       0       0         1    8.547009   10.0 100.000000   85.470085 opp_prior_allowance
   rushyds  over    (-inf, 100.0] 121    40      55       0        26 -206.309941  950.0  42.105263  -21.716836 opp_prior_allowance
   rushyds  over   (100.0, 150.0] 211    77      93       0        41 -254.467648 1700.0  45.294118  -14.968685 opp_prior_allowance
   rushyds  over   (150.0, 200.0]  22     7      10       0         5  -35.649386  170.0  41.176471  -20.970227 opp_prior_allowance
   rushyds  over   (200.0, 250.0]   4     2       1       0         1    7.261905   30.0  66.666667   24.206349 opp_prior_allowance
   rushyds  over              NaN  14     1       8       0         5  -70.909091   90.0  11.111111  -78.787879 opp_prior_allowance
   rushyds under    (-inf, 100.0] 121    55      40       0        26   83.694259  950.0  57.894737    8.809922 opp_prior_allowance
   rushyds under   (100.0, 150.0] 211    93      77       0        41   35.277767 1700.0  54.705882    2.075163 opp_prior_allowance
   rushyds under   (150.0, 200.0]  22    10       7       0         5   19.164652  170.0  58.823529   11.273325 opp_prior_allowance
   rushyds under   (200.0, 250.0]   4     1       2       0         1  -11.666667   30.0  33.333333  -38.888889 opp_prior_allowance
   rushyds under              NaN  14     8       1       0         5   61.123830   90.0  88.888889   67.915367 opp_prior_allowance
