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
- Every `f$cc_*` function now requires nearby Source/Provenance documentation in CI.

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

`CashCrusher_Multiway_StackContext.txt` now requires coherent shallow/deep bounds before a reviewed multiway context is considered valid.

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

Implemented:

- true-HU SB/Button PFA IP vs BB;
- true-HU limp -> BB raise -> call, BB PFA OOP;
- reduced-HU PFA IP vs BB;
- reduced-HU PFA IP vs SB;
- reduced-HU SB PFA OOP vs BB;
- reduced-HU nonblind opener OOP vs later cold caller.

### ISO

Implemented HU and multiway.

HU preserves original limper vs post-raise coldcaller and IP/OOP.

True three-way preserves two original limpers / mixed / two post-raise coldcallers. 4/5/6-way preserves all-limper / mixed / all-postraise-coldcaller composition and exact field size.

### 3BP and squeeze

Implemented HU and multiway.

HU distinguishes original opener, pre-3bet coldcaller surviving squeeze, and post-3bet coldcaller. Multiway preserves exact live opener/pre3bet-caller/post3bet-caller counts and exact field size. Plain 3BP and squeeze never share a generic fallback.

### Ordinary multiway SRP

Implemented true-threeway FIRST/MIDDLE/LAST and exact 4/5/6-way parents. All existing multiway SRP/ISO/3BP/squeeze CBet SPR exceptions have now been reaudited against deepest-effective geometry.

### 4BP

Clean HU 4BP families are implemented for true-HU opener4 and reduced-HU opener4/cold4 versus supported original raiser survivors. Multiway 4BP, reversed/backraise/limp-reraise chronology and 5bet+ remain fail-closed.

## CBet sizing and all-in execution

Strategic size IDs remain:

- `1` ~33%;
- `2` 50%;
- `3` 75%;
- `4` pot;
- `0` check/uncovered.

Native adapter:

- `BetThirdPot`;
- `BetHalfPot`;
- `BetThreeFourthPot`;
- `BetPot`.

DeepCrusher contains distinct stack-sensitive mechanisms rather than one universal threshold:

- explicit flop/turn/river sizing promotion near 60% of Hero `StackSize`;
- `f$allin_on_betsize_balance_ratio`, including a special ~50% effective-stack trigger plus a Hero-balance fallback;
- `f$Raise_Committed`, which can promote an already-approved flop/turn call around separate ~55% geometry.

CashCrusher keeps these as separate audit subjects.

### Implemented now: mechanically equivalent BetMax only

`CashCrusher_Flop_CBet_AllinEquivalence.txt` adds a local execution adapter that can return `BetMax` only when:

1. the reviewed requested CBet already reaches/exceeds Hero's available stack; or
2. the requested CBet reaches the **deepest/all-live effective relationship**, so every live opponent is already covered by the requested amount.

A bet that reaches only a short multiway opponent while a deeper opponent remains is recorded as sidepot divergence and is **not** promoted.

This is deliberately narrower than the historical 50/55/60% rules. Strategic near-all-in promotion remains pending.

## Deterministic quality checks

GitHub Actions now runs:

1. the static OpenPPL strategy linter; and
2. `tools/test_multiway_stack_geometry.py`.

The deterministic test checks equal stacks, short+deep fields, Hero-capped effective stacks, multiway raised-pot asymmetry, false shallowest-based 50%-effective triggers, sidepot divergence, all-live effective reach and the fact that a mere 60%-of-Hero-stack bet is **not mechanically equivalent** to all-in.

A previous CI run after these additions passed; current-head CI must still be checked after the latest context-validation/doc commits before this checkpoint is called green.

## Release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. deterministic OpenPPL/OpenHoldem CBet policy fixtures/replays;
3. whole-bot `f$BestBetsize` ownership integration;
4. strategic near-all-in promotion audit and later global callback composition;
5. skipped-CBet X/C/X/R and turn follow-through coverage;
6. final regression and unknown-state fail-closed audit.

## Current development direction

Next work:

- verify current-head CI after dual-bound context validation;
- finish Gate 01K.3C by auditing strategic CBet near-all-in promotion separately for SRP/ISO/3BP/4BP and HU/multiway rather than applying one source threshold everywhere;
- keep `f$Raise_Committed` outside CBet sizing and revisit it with the defensive nodes it actually owns;
- then move into deterministic OpenHoldem/OpenPPL runtime fixtures before calling Flop CBet release-certified.
