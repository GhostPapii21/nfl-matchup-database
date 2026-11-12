# Rules locked from weeks 3–6 only

For each market/side search exactly 6 cells: tier main/alt × directional prior-yard-average edge >= 0/10/20 yards. Require >=15 graded priced quotes and positive training ROI. Choose highest ROI, then larger n, alphabetical tier, lower threshold. Three conditions: market-side identity, tier, edge threshold. Unrepresented or nonpositive cells abstain. No Sharp feature used.

[
  {
    "market": "recyds",
    "side": "under",
    "tier": "main",
    "min_form_edge": 20,
    "train_n": 53,
    "train_roi": 17.6924369433359
  },
  {
    "market": "rushyds",
    "side": "under",
    "tier": "main",
    "min_form_edge": 20,
    "train_n": 52,
    "train_roi": 39.76427531900738
  }
]

Selection is exploratory and book-correlated; sparse weeks are unavailable rather than treated as losing observations.
