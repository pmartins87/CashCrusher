# DeepCrusher transversal audit 03 — history provenance, current strength and 3wBTNvBB turn donk

Date: 2026-09-03  
Branch target: `deepcrusher-rereview-20260903`  
Frozen good-results baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`  
Parent Candidate C SHA-256: `f515956f24d28ef804ea7802ece989b4d316fd8116b15462d99c58c930297a7e`  
Candidate D SHA-256: `066446c6ed8bed887a5527115f20b1eff0a44a3250760cb745dd6f62dc0877cb`

## Review standard

This pass follows `docs/deepcrusher/SOURCE_POLICY.md`. Small threshold margins remain untouched. The project-level ~52% lowbet boundary and ~76% normal/high boundary are preserved deliberately. The review target is material action ownership, stale-history leakage and source-specific rules being erased by generic helpers.

## Confirmed material defect 1 — 3wBBvSB source class was narrowed from “TP or better” to TP/OP

The written Crusher Starting Strategy says explicitly: `TP or better (NCF)`; Q3 Facing Bet (LP/SRP): wet -> raise 50%; dry -> call only vs roughly 50%+.

`user_hardcoded.cpp` independently uses its `tp_plus` class for the same branch.

Candidate C protected only current `TopPairReal || OverPairReal`. That left current two-pair+/trips/straight/flush exposed to generic `f$hand_slowplay` / Donk fallback behavior, even though the source class is broader.

### Candidate D repair

Only the source-specific 3wBBvSB Facing-Bet ownership guards are broadened to `f$CF7_StrongMade` (`TwoPairPlus || TopPairReal || OverPairReal`). No global strong-hand slowplay rule is removed in this pass.

This is deliberately scenario-first and lower-risk: explicit source ownership bypasses generic helpers only where the source is clear.

## Confirmed material defect 2 — stale `user_3wBTN_Had_Air_OTF` could force a river barrel after an actual flop CBet

The old marker `user_3wBTN_Had_Air_OTF` is written inside flop strategy branches before/finally alongside actions that actually CBet. It therefore records that the flop hand was air, not that Hero checked back.

The river CBet tail still contained a generic `When user_3wBTN_Had_Air_OTF Return true Force`, under a comment saying a flop check-back with air should delay and barrel.

That conflates hand class on flop with final flop action. This is materially wrong in at least 3wBTNvSB. Its Starting Strategy explicitly says that after the narrow air CBet on A/K + low boards, Hero does not want to invest more chips and should check to showdown/give up rather than BxB bluff.

The newer DeepCrusher architecture already created exact final-action states `user_RNH02_BTNVSB_FlopAirChecked` and `user_DC12AR_3wBTNv2p_FlopAirChecked`, written only when Hero actually checks the flop and feeding the delayed-air trees.

### Candidate D repair

The old marker itself is preserved because other source-aware code still consumes it (for example the 3wBTNvSB turn give-up). Only its stale generic river-barrel consumer is removed. Delayed river barrels remain owned by exact final-check histories.

## Confirmed material defect 3 — 3wBTNvBB TP+ vs turn Donk was being generically raised

Crusher Starting Strategy, `3wBTNvBB TP or better 08/14`, says:

- vs up to roughly 50%: raise 40%;
- vs 51%+ on paired turn: readless call turn, then call/fold river;
- vs 51%+ on completed turn: call only with equity to improve, explicitly saying even overpair alone is insufficient.

`user_hardcoded.cpp` materially corroborates the tree: low bet -> raise 40; paired -> call; completed -> call with current strong made or FD/OESD/GS, otherwise fold; otherwise -> call.

The current generic Normal/High Donk raise nodes can raise TP+ on non-paired turns. Because `f$Raise_Committed` executes before the normal router, explicit calls could also be converted into jams.

### Candidate D repair

Top-level source ownership is added before `f$Raise_Committed` / `f$Call_MicroBets`, gated by actual context: `3wBTNvBB + Hero had initiative + user_did_cbet_OTF + facing turn bet + current StrongMade`.

Action tree using the project’s existing ~52 margin:

- lowbet -> set `user_Turn40`, RAISE;
- non-lowbet paired -> CALL;
- non-lowbet completed, non-paired: current TwoPairPlus -> CALL; TP/OP + real FD/OESD/GS -> CALL; TP/OP without extra equity -> FOLD;
- non-lowbet non-paired, non-completed -> CALL.

The generic Donk nodes remain unchanged and still apply to contexts not owned by this explicit source tree.

## Intentionally not decided yet — paired-turn river plan

The written source says `Readless call turn & call fold river`, while `user_hardcoded.cpp` resolves this more specifically as: strong river improvements continue; ordinary TP facing another barrel folds readless; aggressive-player double-call remains a future read-dependent branch.

This is plausible and internally coherent, but the written phrase “call/fold river” is not sufficiently explicit on its own. The human-reviewed CrusherTBP does not provide a comparably explicit dedicated state here. Candidate D therefore records the turn call but does not silently impose the C++ river interpretation yet. This remains a focused reconciliation item for the next pass.

## Static regression

`test_deepcrusher_candidateD_transversal.py` passes **32/32** checks.

Verified: frozen baseline SHA unchanged; Candidate C parent SHA exact; same 1,283 OpenPPL block sequence and no duplicates; no new executable `f$` references; ~52 and ~76 margins unchanged; 3wBBvSB source-specific Facing-Bet ownership now uses current `f$CF7_StrongMade`; 3wBTNvBB one-pair flop tree was not accidentally broadened; stale generic `user_3wBTN_Had_Air_OTF` river consumer is removed while exact checkback states and intended turn give-up remain; turn-donk raise/call/fold guards execute before commitment/microbet helpers; paired branch precedes completed branch; generic turn Donk logic remains present as fallback outside the source-owned context; Parent C -> Candidate D executable delta is limited to exactly five blocks (`f$flop_Raise`, `f$flop_Call`, `f$turn_Raise`, `f$turn_Call`, `f$move_river_cbet`); delimiter imbalances are unchanged.

Relative to the frozen baseline, Candidate D has executable changes in eleven reviewed blocks total; all prior Candidate C repairs remain preserved.

## What remains to review before runtime promotion

This is the remaining strategic/technical review roadmap, not a bureaucracy checklist. Good branches are preserved; only material defects are changed.

1. **Persistent history vs current hand strength** — audit material `user_*` readers where a historical label can override current hand class; reconcile the 3wBTNvBB paired-turn river plan.
2. **Remaining turn action ownership vs `f$Raise_Committed`** — search every source-explicit TURN CALL/FOLD family and prevent unsupported CALL->JAM conversion without deleting the helper globally.
3. **Remaining shared helper scope** — global `f$hand_slowplay` rules for 2P+/trips/straight+; `f$Call_MicroBets` outside the fixed 3wBBvSB leak; `f$hand_dead` / `f$hand_zombie` and broad strength fallbacks when they precede scenario rules.
4. **Defense nodes 1–32 semantic second pass** — Normal/High/Over CBet, Donk, Float, generic Bet and Raise-vs-Raise after helper ownership fixes.
5. **Attack nodes 33–45 post-helper recheck** — especially cross-street state writers/readers, Delayed/Probe/Donk histories and sizing ownership.
6. **Pot/history/initiative classification end-to-end** — SRP/ISO/Limped overlap; final-action writers versus preliminary hand-class markers; initiative transitions after call/raise/check.
7. **Sizing layer** — `f$BestBetsize`, heads-up/multiway street sizing, `RaiseTo`/`RaiseBy`, all-in conversion; verify sizing helpers preserve selected strategic action and do not leak state.
8. **Static + OpenHoldem parser/runtime validation** — deterministic rebuild, targeted regression corpus, parser/load and runtime/log replay.
9. **Final candidate comparison and promotion decision** — compare against frozen good-results baseline; promote only after runtime behavior matches intended source decisions; baseline remains permanent rollback.

## Reproduction artifacts

- `DeepCrusher_CandidateD_HistoryTurnDonk_20260903.txt`
- `DeepCrusher_CandidateD_from_C_20260903.patch`
- `build_deepcrusher_candidateD.py`
- `test_deepcrusher_candidateD_transversal.py`
