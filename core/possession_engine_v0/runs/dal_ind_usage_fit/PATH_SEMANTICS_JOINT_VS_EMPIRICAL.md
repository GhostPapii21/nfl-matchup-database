# PATH bridge status

**SHARED_PARTIAL_SEMANTICS**

All 2,665 extract rows match the empirical parquet on game/play IDs, team/down/type/yards/completion/interception; the larger filtered parquet also has 121 no_play and 34 null-type rows absent from the extract. Opportunity allocation, conditional-state partitioning, player role weights, yard generation, credit rules, OT implementation, seeds and forecast identities remain nonintegrated. Do not blend forecasts or call this end-to-end integration.


Shared training evidence is partial semantic overlap, not shared forecast or accounting lineage. Original empirical n=500 summary is not rerun or relabeled.

## Superseding implementation

SHARED_ACCOUNTING_V1 is now implemented for opt-in joint_producer.shared_accounting=true using empirical fitted model events. See ../dal_ind_roles_unify/PATH_SEMANTICS_JOINT_VS_EMPIRICAL.md. Legacy independent empirical artifacts retain their separate path and limitations above.
