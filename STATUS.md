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

## Multiway stack correction

The initial Gate00 generic multiway SPR used the shortest live opponent as a coarse descriptor. That remains useful for detecting short-player/sidepot geometry, but it is no longer allowed to stand in for the whole multiway effective depth.

CashCrusher now preserves both:

- **shallowest effective** = `min(Hero, shortest live opponent)`;
- **deepest effective** = `min(Hero, biggest live opponent)`.

The second is also the mechanical analogue of DeepCrusher `f$EffectiveStack_BKP`, because the source helper uses the biggest active opponent.

Multiway CBet one-pair low-SPR exceptions now use the deepest-effective SPR. Therefore a short third player cannot make a still-deep decision against another live opponent inherit short-stack aggression.

`CashCrusher_Multiway_StackContext.txt` requires coherent shallow/deep bounds before a reviewed multiway context is considered valid.

The linter rejects generic `f$cc_spr_round_start`/bucket helpers inside `CashCrusher_Flop_CBet_Multiway_*` strategy modules.

## Gate 00 — mechanical context foundation

Complete in design/code; OpenHoldem parser/runtime validation still pending:

- legacy Spin game labels decomposed into strategic properties;
- exact dynamic 2-6 handedness;
- true-HU deal vs preflop-reduced HU vs postflop-reduced HU;
- pot family / Hero role / absolute and relative position;
- exact flop-entry count and live-opponent masks;
- ISO, 3BP and squeeze survivor provenance;
- HU effective stack plus multiway shallowest/deepest effective envelopes;
- actor-specific SPR versus `raischair` for future defense nodes;
- true-multiway composition framework.

## Gate 01 — Flop CBet implementation

### Ordinary one-raise HU

Implemented true-HU and reduced-HU ordinary SRP families, including SB-v-BB and opener-OOP-v-later-coldcaller gaps.

### ISO

Implemented HU and multiway. Survivor provenance remains explicit: original limper vs post-raise coldcaller in HU, and exact/coarse limper+coldcaller composition multiway.

### 3BP and squeeze

Implemented HU and multiway. Original opener, pre-3bet coldcaller and post-3bet coldcaller remain separate survivor origins; plain 3BP and squeeze never share a generic fallback.

### Ordinary multiway SRP

Implemented true-threeway FIRST/MIDDLE/LAST and exact 4/5/6-way parents. All current multiway SRP/ISO/3BP/squeeze CBet SPR exceptions have been reaudited against deepest-effective geometry.

### 4BP

Clean HU 4BP families are implemented for true-HU opener4 and reduced-HU opener4/cold4 versus supported original raiser survivors. Multiway 4BP, reversed/backraise/limp-reraise chronology and 5bet+ remain fail-closed.

## CBet sizing and all-in execution

Strategic size IDs remain 33 / 50 / 75 / pot with native `BetThirdPot`, `BetHalfPot`, `BetThreeFourthPot`, `BetPot` execution.

DeepCrusher contains three distinct stack-sensitive mechanisms that must not be conflated:

1. explicit sizing promotion near 60% of Hero `StackSize`;
2. `f$allin_on_betsize_balance_ratio`, with special ~50% `f$EffectiveStack_BKP` logic plus Hero-balance fallback;
3. `f$Raise_Committed`, which can promote an already-approved flop/turn call around separate ~55% geometry.

### Mechanically equivalent BetMax — implemented

`CashCrusher_Flop_CBet_AllinEquivalence.txt` returns local `BetMax` only when the already-reviewed requested CBet:

- reaches Hero's available stack; or
- reaches the deepest/all-live effective relationship.

Shortest-only multiway reach is a sidepot-divergence state and does not qualify.

### Strategic historical 50/60% promotion — audited, not globally activated

`GATE_01K3_STRATEGIC_ALLIN_PROMOTION_AUDIT.md` separates the historical mechanisms from mechanical clipping. The audit result is:

- preserve 50%-effective and 60%-Hero thresholds as useful source diagnostics;
- do not let one generic threshold silently rewrite every CashCrusher CBet size after the strategy node has selected 33/50/75;
- any true strategic flop jam must be owned by the exact SRP/ISO/3BP/4BP node and documented as T/A/P/X;
- 4BP is the strongest future candidate for explicit node-owned flop jams because low SPR can arise naturally at 100bb;
- `f$Raise_Committed` remains deferred to defensive call/raise ownership, not CBet sizing;
- final global `f$allin_on_betsize_balance_ratio` remains deferred until all postflop sizing owners that it can affect are audited.

This is not a global disablement of inherited short-stack mechanisms; it prevents them from overriding cash-specific node strategy outside reviewed contexts.

## Deterministic quality checks

GitHub Actions runs:

1. the static OpenPPL strategy linter; and
2. `tools/test_multiway_stack_geometry.py`.

The deterministic test covers equal stacks, short+deep fields, Hero-capped effective stacks, raised-pot asymmetry, false shallowest-based 50%-effective triggers, sidepot divergence, all-live effective reach and the fact that a mere 60%-of-Hero-stack bet is not mechanically identical to all-in.

## Release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. deterministic OpenPPL/OpenHoldem CBet policy fixtures/replays;
3. whole-bot `f$BestBetsize` ownership integration;
4. any explicit node-owned strategic jam audits that are actually needed;
5. skipped-CBet X/C/X/R and turn follow-through coverage;
6. final regression and unknown-state fail-closed audit.

## Current development direction

Immediate next work:

- current-head CI confirmation;
- source-first audit of whether any clean 4BP flop family needs an explicit node-owned jam size rather than 33/50;
- then Gate 01N flop final-action/history capture so a skipped CBet reaches Delayed CBet rather than being misrouted as Turn CBet;
- after that begin Turn CBet source adaptation using actual flop-action provenance.
