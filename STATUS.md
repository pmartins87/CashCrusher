# CashCrusher Status

Last update: 2026-08-23

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime gates are passed.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem.
- Runtime supports hands dealt 2h, 3h, 4h, 5h or 6h as seats empty/sit out.
- Preflop is used to reconstruct post-flop context/ranges, not to decide current project preflop strategy.
- Strategic provenance is mandatory: T / A / P / X.
- Source-derived and professional-theory rules remain explicitly distinguishable.
- Unknown/unsupported strategic context fails closed.
- OpenPPL strategy code uses flat complete `WHEN` rules; indentation is never logical scope.
- Every `f$cc_*` function requires nearby Source/Provenance documentation in CI.

## Stack-depth migration rule

DeepCrusher short-stack logic is a **review flag**, not an automatic deletion rule.

For every stack-sensitive inherited rule:

- do not assume it transfers unchanged to ordinary 100bb cash;
- do not assume it becomes invalid merely because CashCrusher starts deeper;
- review the exact pot/range/board/action/effective-stack/SPR context;
- classify locally as T, A, P or X.

This applies to TP+/draw commitment lines, `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, `BetMax` and related mechanisms.

## Gate 00 — context/stack foundation

Design/code foundation is complete; OpenHoldem parser/runtime certification remains pending.

Frozen stack/context rules:

- HU uses exact Hero-v-Villain effective stack;
- multiway preserves both **shallowest effective** and **deepest effective**;
- actor-specific defense later uses actor-specific effective stack;
- a short sidepot player cannot make the whole multiway pot inherit short-stack aggression;
- true-HU deal, preflop-reduced HU and postflop-reduced HU remain separate range origins.

## Gate 01 — Flop CBet

Implemented strategic baseline includes ordinary SRP, HU/multiway ISO, HU/multiway plain 3BP+squeeze, true3 and 4/5/6-way SRP, and clean supported HU 4BP.

Still fail-closed: multiway 4BP, unresolved/reversed/backraise/limp-reraise 4BP chronology, and 5bet+.

### Flop sizing/history

- local `BetMax` only for mechanical/natural equivalence;
- historical ~50% effective / ~60% Hero-stack promotion remains diagnostic, not a generic cash action;
- `f$Raise_Committed` remains defense-owned;
- closed round-2 action provenance distinguishes actual CBet, check-through, check-call/XR, CBet-raised histories and plan-v-execution drift;
- flop hand/kicker/backdoor/texture plan snapshots are consumed by Turn only together with actual executed history.

Whole-bot `f$flop` / `f$BestBetsize` composition and OpenHoldem replay certification remain pending.

## Gate 02 — Turn CBet strategic coverage complete for currently supported pot families

### Ordinary SRP

Implemented:

- true-HU HUSB PFA-IP;
- reduced-HU BTN-v-BB and BTN-v-SB source descendants;
- true-HU BB-PFA-OOP after SB limp -> BB raise -> call;
- reduced-HU SB-PFA-OOP vs BB source-safe checking/barrel subset;
- UTG/HJ/CO PFA-IP vs SB/BB P-heavy six-max fills;
- UTG/HJ/CO PFA-OOP vs later nonblind cold caller P-heavy fill;
- flop multiway -> turn HU with exact surviving-opponent provenance;
- turn remains multiway with original flop-entry/current-live composition and deepest-effective SPR.

### Other pot families

Implemented:

- ISO HU/multiway: original limper vs post-raise coldcaller kept separate;
- plain 3BP HU/multiway: original opener vs post-3bet coldcaller kept separate;
- squeeze HU/multiway: opener / pre-3bet coldcaller / post-3bet coldcaller retained;
- clean HU 4BP: true-HU opener4 and reduced-HU opener4/cold4 versus exact opener/3bettor survivors.

Still fail-closed:

- multiway 4BP and 4BP that only becomes HU after a multiway flop;
- 4BP `other caller` with unresolved call stage;
- unresolved/reversed 3bet/4bet chronology;
- 5bet+;
- any current survivor that cannot be reconciled with persisted preflop/flop provenance.

## Gate 02J — Turn execution/sizing now implemented locally

### Exact strategic size palette

Turn size IDs are frozen as:

- 25%;
- ~33%;
- 40%;
- 50%;
- 62.5%;
- 75%;
- 100%.

Runtime mapping uses native `BetThirdPot` / `BetHalfPot` / `BetThreeFourthPot` / `BetPot` and verified OpenPPL `RaiseBy 25%`, `RaiseBy 40%`, `RaiseBy 62.5%` for the non-native exact fractions.

### Stack-sensitive execution

`CashCrusher_Turn_CBet_StackGeometry.txt` now measures the requested Turn size against:

- Hero remaining street-start stack;
- exact HU effective stack;
- shallowest MW effective relationship;
- deepest/all-live MW effective relationship.

Historical DeepCrusher ~50% effective / ~60% Hero-stack thresholds remain explicit diagnostics only.

### Local all-in equivalence

`CashCrusher_Turn_CBet_AllinEquivalence.txt` may locally return `BetMax` only when the reviewed requested Turn size already reaches:

1. Hero's remaining stack; or
2. exact HU effective stack; or
3. deepest/all-live MW effective relationship.

Reaching only a short sidepot opponent never promotes the whole action to local `BetMax`.

This preserves natural low-SPR aggression — especially in 3BP/squeeze/4BP — without importing the old global short-stack `TP+ -> stackoff` behavior.

### Historical strategic shove audit

The source does contain genuine exact `TurnMax`/`TurnShove` plans, but several belong to raised-flop or narrow short-stack histories rather than the canonical standard Turn-CBet parent. The mature Turn betsize router also performs generic near-all-in conversion around historical 50/55/60 thresholds.

Current frozen CashCrusher rule: **no generic near-all-in Turn promotion**. Any future strategic `BetMax` must be restored by an exact pot/range/board/history/SPR owner. Natural/mechanical equivalence remains active independently.

## Turn plan provenance prepared for River

The local Turn execution wrapper records PRE-ACTION plan markers only:

- Turn CBet opportunity/plan seen;
- one of seven planned size IDs;
- whether local natural all-in equivalence was expected.

These markers do **not** prove the Turn action actually executed. Gate02N must confirm execution from closed OpenHoldem round-3 history before River CBet may consume it.

## Current automated checks

GitHub Actions currently checks:

1. global `f$cc_*` dependency / flat-WHEN / per-function provenance / multiway-SPR safety;
2. deterministic multiway stack geometry;
3. flop action-history/snapshot contracts;
4. Turn source-boundary / post-multiway-HU / current-multiway SRP contracts;
5. ISO / plain3BP / squeeze / clean-HU-4BP Turn contracts;
6. Turn strategic coverage/exclusivity/fail-closed matrix;
7. Turn runtime 25/33/40/50/62.5/75/100 mapping and natural-all-in/sidepot invariants.

Latest complete runtime-sizing CI cycle passed after Gate02J.1/J.2 code was added.

## Remaining release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. whole-bot history-aware `f$flop` / `f$turn` / `f$BestBetsize` composition;
3. Gate02N closed round-3 actual Turn-action provenance;
4. deterministic OpenHoldem flop/turn policy replays;
5. subsequent River/Float/Donk/Probe/Delayed and 32 defense gates;
6. final exact-node stack-sensitive commitment and global callback audit;
7. full regression / unknown-state fail-closed review.

## Immediate development direction

Next small gate: **02N — Turn final-action provenance**.

Before beginning River CBet, reconstruct from closed round-3 OpenHoldem history:

- actual standard Turn CBet executed;
- actual Turn check;
- Turn CBet -> later raise -> Hero call/re-aggression;
- direct/mechanical all-in versus normal sized execution;
- plan-v-execution mismatch.

River CBet must consume actual executed Turn history, never merely `f$cc_turn_cbet_router = true` or the pre-action plan markers.
