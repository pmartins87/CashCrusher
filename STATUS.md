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
- Every `f$cc_*` function must now have nearby Source/Provenance documentation; CI treats absence as a hard error.

## Stack-depth migration rule

DeepCrusher short-stack logic is a **review flag**, not an automatic deletion rule.

For every stack-sensitive inherited rule:

- do not assume it transfers unchanged to ordinary 100bb cash;
- do not assume it becomes invalid merely because CashCrusher starts deeper;
- review the exact pot/range/board/action/effective-stack/SPR context;
- classify locally as T, A, P or X.

This applies to TP+/draw commitment lines, `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, `BetMax` and related mechanisms.

`CashCrusher_SPR_Commitment.txt` computes geometry only. It does not impose a global commitment policy.

## Gate 00 — mechanical context foundation

Complete in design/code; OpenHoldem parser/runtime validation still pending:

- legacy Spin game labels decomposed into strategic properties;
- exact dynamic 2-6 handedness;
- true-HU deal vs preflop-reduced HU vs postflop-reduced HU;
- pot family / Hero role / absolute and relative position;
- exact flop-entry count and live-opponent masks;
- ISO, 3BP and squeeze survivor provenance;
- raw effective-stack and SPR geometry;
- true-multiway composition framework.

The core `CashCrusher_Context.txt` retrofit is complete: each custom context function now has local Purpose/Source/Provenance comments. The linter was promoted accordingly from warning to global hard error.

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

True three-way preserves two limpers, limper+coldcaller and two post-raise coldcallers. 4/5/6-way preserves all-limper / mixed / all-postraise-coldcaller composition and exact field size.

### 3BP and squeeze

Implemented HU and multiway.

HU distinguishes original opener, pre-3bet coldcaller surviving squeeze, and post-3bet coldcaller. Multiway preserves exact live opener/pre3bet-caller/post3bet-caller counts and exact field size. Plain 3BP and squeeze never share a generic fallback.

### Ordinary multiway SRP

Implemented true three-way FIRST/MIDDLE/LAST with exact caller composition and exact 4/5/6-way parents.

The true-threeway BTN-last source ancestry is A/P because the audited DeepCrusher branch is itself a human-reviewed CrusherTBP gap fill rather than a dedicated Starting Strategy tree. FIRST/MIDDLE and four-way+ are P-heavy and explicitly labelled.

### 4BP

Implemented clean HU families after conservative chronology reconstruction:

- true-HU standard opener4: SB/Button 4bettor IP vs BB 3bettor-call;
- reduced-HU opener4 vs 3bettor-call, IP/OOP;
- reduced-HU cold4 vs original opener-call, IP/OOP;
- reduced-HU cold4 vs original 3bettor-call, IP/OOP.

Still fail-closed:

- non-raiser HU survivor in 4BP because exact call stage is not proven;
- reversed/limp-reraise/backraise chronology;
- multiway 4BP action policy;
- 5bet+.

Normal 100bb 4BP can reach low SPR and may legitimately support aggressive one-pair/draw lines. The exact later commitment decision remains a separate node review.

## CBet size runtime and stack geometry

Strategic IDs remain `1` ~33%, `2` 50%, `3` 75%, `4` pot, `0` check/uncovered.

`CashCrusher_Flop_CBet_Betsize.txt` maps them to native OpenPPL `BetThirdPot`, `BetHalfPot`, `BetThreeFourthPot` and `BetPot` actions.

A deeper source audit found that DeepCrusher had **overlapping, not identical**, stack-sensitive mechanisms:

- explicit betsize routers commonly promoted requested sizes around **60% of Hero StackSize** to `BetMax`;
- `f$allin_on_betsize_balance_ratio` had a special **~50% effective-stack** trigger and a `.50` Hero-balance fallback through OpenHoldem's all-in adjustment;
- `f$Raise_Committed` separately used approximately **55%** call-to-shove logic in flop/turn defense.

These are now deliberately separated instead of being described as one generic commitment rule.

`CashCrusher_Flop_CBet_StackGeometry.txt` exposes requested bet/stack ratios, exact HU effective-stack ratio, projected HU SPR after a full call and historical 50/60% diagnostic flags. It returns no all-in action and does not change the global callback.

## Static quality state

Latest completed global-provenance lint passed. Hard checks include:

- unresolved/duplicate `f$cc_*`;
- executable legacy `f$game_*` dependencies;
- open-ended/nested-looking `WHEN` scope;
- missing nearby Source/Provenance comment for **any** `f$cc_*` function.

Stack-sensitive DeepCrusher mechanisms remain review warnings/targets, not global prohibitions.

## Release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. deterministic CBet policy fixtures/replays;
3. whole-bot `f$BestBetsize` ownership integration;
4. context-aware stack-sensitive size/commitment policy audit;
5. skipped-CBet X/C/X/R and turn follow-through coverage;
6. final regression and unknown-state fail-closed audit.

## Current development direction

Immediate work:

- use the new stack-geometry descriptors to audit size-to-all-in conversion **per CBet family**, beginning with clean HU SRP/3BP/4BP rather than imposing one threshold globally;
- then build deterministic Gate00/Gate01 runtime fixtures and wire the native CBet size adapter into the whole-bot sizing owner.
