# JAX/BAL post-inactives defensive personnel update
Evidence update: 2026-11-05T19:20:08.656709 America/New_York. Personnel reconstruction, NOT a measured post-injury coverage forecast or betting clearance.

## Official availability
BAL Wiggins, Hawkins, Peebles inactive. JAX Hamilton/Murray IR; Huzzie, Silmon-Craig, Wesley Williams inactive; Travon Walker active.
Sources: https://www.baltimoreravens.com/news/nate-wiggins-inactive-for-jaguars-week-9-austin-reed-backup-quarterback ; https://www.jaguars.com/news/in-and-out-2026-week-9-walker-tuten-active-for-jaguars-vs-ravens

## BAL projected personnel, not confirmed starting formation
Front: Madubuike / Travis Jones / Campbell, with Broderick Washington and John Jenkins rotation; edges Hendrickson/Mike Green with rotation. ILB Roquan Smith/Trenton Simpson.
Outside CB: Humphrey remains; Awuzie projected greater outside workload replacing Wiggins, Tampa another option. No player-specific shadow assignment confirmed.
Hybrid nickel: Kyle Hamilton; Keyon Martin rotational option. Deep safety Starks; Hawkins workload shared Wallace/Keondre Jackson. Week8 Wallace47/82 (57%), Jackson12/82 (15%), Awuzie43/82 (52%), Tampa22/82 (27%); not forecasts and no forced normalization across different packages.
Source snap_counts_2026.parquet week8 in week10/bal_secondary/raw. Depth crosscheck https://www.statiqsports.com/nfl/teams/bal/depth-chart . Official article says Awuzie and Tampa may play larger roles, not fixed starters.

## JAX projected personnel, not confirmed starting formation
Edges Hines-Allen/Travon Walker; interior Armstead plus Hamilton replacement committee: Orhorhoro, Dickerson, Regis. Do not identify a single replacement coefficient or guarantee Orhorhoro all nose snaps.
LB Oluokun/Ventrell Miller; Gardeck base/edge role. Outside Hunter/Brown; Lewis nickel; Jaylon/Jarrian Jones depth. Safety Rayuan Lane replaces Murray; Antonio Johnson active/not listed inactive, but exact workload unconfirmed; Merriweather/Huskey alternatives.
Week8: Lane61/61; Merriweather43/61; Huskey18/61; Orhorhoro44/61; Dickerson31/61; Armstead33/61. Johnson absent that game so do not project unchanged safety shares tonight.
Official sources: https://www.jaguars.com/news/day-after-week-8-win-over-colts-hamilton-murray-out-rest-of-season ; https://www.jaguars.com/news/responding-to-change-important-just-to-stay-ready . Official depth chart https://www.jaguars.com/team/depth-chart still lists IR starters, treated stale for availability. Secondary depth listing https://www.profootballnetwork.com/nfl-hq/teams/jacksonville-jaguars/depth-chart does not override official committee comments.

## Receiver coverage mapping is conditional on alignment
BAL offense: outside Flowers/Bateman/Lane may see Hunter/Brown; slot routes may see Lewis/Jarrian; Andrews middle routes may enter LB/safety zones; Hill flats/screens may enter LB/force zones. No shadow or primary defender assignment verified.
JAX offense: outside Washington/Meyers/Thomas enter Humphrey/Awuzie/Tampa side; slot enters Hamilton/Martin or zone; Strange seams/crossers involve Smith/Simpson/Hamilton/Starks/Wallace/Jackson by call. Washington is NOT automatically assigned Awuzie every play.

## What changes and what does not
Remove inactive defenders from available matchup pool; preserve zone responsibility and safety-help uncertainty. Hawkins already missed last2, not a newly missing starter versus Week7/8 baseline. Wiggins is new absence. Hamilton/Murray absences partly present in Week8 sample: do not double-count full replacement penalties. No new man/zone, MOFO/MOFC or pressure percentages fitted from inactives; current 2026 charting missing. Blitz != pressure. No numerical receiving/rush boost. Cached per-defender rates are small samples and not post-replacement team rates. No engine parameter changes performed.
