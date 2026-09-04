# DeepCrusher — Static Closure 2026-09-04

Status: **STATIC STRATEGIC REVIEW CLOSED**

Frozen good-results baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`

Complete parent Candidate N SHA-256: `c37dd9715b1a35cf93f40cd60cb17cbae160c60b225e274e74f7a47df627d84e`

Static Closure Candidate SHA-256: `3bbebb17bae821962d6d3a583830a984a359ca6e748f0846f472d9ada4a7f88f`

## Closure decision

The open-ended static strategic re-review is finished at this candidate. This is not a claim that no future live hand can reveal a bug. It means there is no remaining known static-review item that justifies continuing an alphabetic candidate cycle before OpenHoldem runtime testing.

A new strategic revision should be opened only for a concrete runtime regression, a newly demonstrated source conflict, or a material new exploit requirement.

## Review method

The closure follows `docs/deepcrusher/SOURCE_POLICY.md`: Starting Strategy + human-reviewed CrusherTBP + `user_hardcoded.cpp` cross-check + professional theory for genuine gaps; actual executable OpenPPL semantics outrank labels/comments; small margins such as ~50/~52 and ~75/~76 are preserved unless they create a material unsupported action change; `f$Raise_Committed` and `f$Call_MicroBets` retain legitimate precedence as exceptional geometry/price helpers unless the exceptional action itself is shown wrong.

## Artifact integrity correction

The previously exported `DeepCrusher_CandidateQ_SBVBTN_MPBP_Line_20260904.txt` was found to be truncated (61 block headers instead of the canonical 1,283) and is **not deployable**. Static Closure was rebuilt from the complete Candidate N parent. Only six complete, independently bounded Q blocks were transplanted; the truncated final Q block was not imported.

## Final closure additions over complete Candidate N

### 3wSBvBTN TP+

- Axx remains the source exception: ordinary geometry X/C flop.
- non-Axx TP+ owns X/R across Normal/High/Over CBet buckets.
- exact target is `RaiseTo 6` big blinds.
- `f$Raise_Committed` remains before the ordinary tree.
- opponent-all-in geometry is excluded from an impossible normal X/R.

OpenHoldem source confirms `RaiseTo` is expressed in big blinds and the betsize-adjustment layer clamps requested sizes to legal minimum/maximum bounds.

### 3wSBvBTN MP/BP

- ordinary flop class is CALL/FOLD, not generic X/R;
- existing ~52% lowbet margin calls;
- larger bets call only with the human-reviewed combo-backdoor/draw exception, otherwise fold;
- final-action state is written only after an actual X/C;
- turn continuation is scoped to current MP/BP so improved hands escape stale history;
- commitment and microbet exceptions remain first.

### Turn after 3wSBvBTN source TP+ X/R

- Ace or glued overcard -> check;
- wet turn -> jam;
- dry turn -> 33%.

### Limp-raise router cleanup

Removed an unreachable contradictory `Call Force` branch shadowed by an identical earlier user-clarified `BetMax Force` condition. Executable behavior is unchanged; stale code/comment contradiction is removed.

## Material repairs preserved from the full re-review

- original 3wBBvSB QTo / dry TP+ versus ordinary Over Donk gross-fold regression fixed;
- 3wBBvBTN TP/OP Normal/High/Over CBet action cliff fixed;
- 3wBTNvBB explicit TP/OP facing-bet tree preserved across sizing buckets;
- global dry-TP slowplay scope leak narrowed to its real scenario ancestry;
- HUSB Delayed-Float detailed subtree made reachable;
- repaired paths reclassify current river strength instead of blindly obeying stale flop/turn labels;
- stale “had air” does not equal “checked flop”;
- exceptional commitment/microbet precedence restored;
- stale source-priority comments corrected;
- `user_GotIsolated` has executable preflop writers;
- HUBB pending TP/draw states have executable writers in the complete lineage.

## 45-node closure

All 32 defensive `f$move_*` nodes and all 13 attack `f$move_*` nodes remain present. After the source-reconciliation, helper-precedence, state-provenance and second-pass reviews, there is no unresolved **gross/static** contradiction known in their executable routes. Generic residual High/Over functions are not judged in isolation: source-specific scenario ownership in the top-level routers is part of the final action path.

This PASS is not a solver-optimality claim; it is closure of the requested hardcoded/source-consistency review.

## Regression

`test_deepcrusher_static_closure.py` passes **46/46** checks, including:

- frozen baseline SHA unchanged;
- complete Candidate N parent SHA exact;
- canonical 1,283 OpenPPL block sequence preserved;
- no duplicate blocks;
- no new executable `f$` references vs complete N;
- inherited delimiter-count imbalances not worsened;
- ~35/~52/~76/100 routing boundaries preserved;
- commitment/microbet precedence preserved;
- QTo-family fix and BBvBTN TP cliff fix preserved;
- SBvBTN Axx/non-Axx TP+ ownership and exact 6bb sizing present;
- SBvBTN MP/BP final-action and turn-current-strength guards present;
- `user_GotIsolated` and HUBB pending-state writers present;
- stale limp-raise CALL owner removed;
- all 45 move nodes present;
- final executable delta vs complete N limited to nine intentionally reviewed blocks.

## Known non-blockers

Some obsolete legacy `user_*` readers have no writer in the modern formula. They remain false and are superseded by newer exact states; historical writers are not recreated blindly. Static checks also cannot certify scraper/tablemap state or OpenHoldem parser/runtime behavior.

## Next gate

**Runtime only.** Install/test Static Closure while keeping the frozen good-results baseline as permanent rollback. High-value first observations: original QTo overdonk family; genuine committed continuation; BBvBTN TP around the High/Over boundary; SBvBTN TP+ non-Axx X/R-to-6bb and Axx X/C; SBvBTN MP/BP CALL/FOLD; HUSB ISO routing; HUSB delayed-float; committed-call and microbet exceptions.

If parser/runtime behavior is clean and logs reveal no material regression, promote Static Closure as the new operational DeepCrusher while preserving the 2026-09-03 baseline forever.