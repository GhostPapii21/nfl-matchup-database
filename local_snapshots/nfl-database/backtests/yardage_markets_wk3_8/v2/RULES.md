# Train-only locked rules

Each market-side searches model_edge >= 0,5,10,15,20. Keep highest ROI with >=30 graded legs and positive ROI; ties larger n then lower threshold. At most three conditions: market, side, minimum edge. Missing edge/price abstains. Edgecap is identical with model_edge <=15, pre-registered without refitting. Sharp is never used for fitting; ON is Oct27 HINDSIGHT only: over man>=30, under man<30; missing abstains.

{
  "train_weeks": [
    3,
    4,
    5,
    6
  ],
  "rules": [
    {
      "market": "recyds",
      "side": "under",
      "min_model_edge": 15,
      "train_n": 36,
      "train_roi": 9.771560394214056
    },
    {
      "market": "rushyds",
      "side": "under",
      "min_model_edge": 10,
      "train_n": 49,
      "train_roi": 14.959542991255026
    }
  ],
  "variants": {
    "baseline": {},
    "edgecap": {
      "max_model_edge": 15
    }
  },
  "sharp_hindsight": {
    "over_man_min": 30,
    "under_man_lt": 30
  }
}
