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

## Stack-depth migration rule

DeepCrusher short-stack logic is a **review flag**, not an automatic deletion rule.

For every stack-sensitive inherited rule:

- do not assume it transfers unchanged to ordinary 100bb cash;
- do not assume it becomes invalid merely because CashCrusher starts deeper;
- review the exact pot/range/board/action/effective-stack/SPR context;
- classify locally as T, A, P or X.

This applies to TP+/draw commitment lines, `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, `BetMax` and related mechanisms.

`CashCrusher_SPR_Commitment.txt` currently computes geometry only. It does not impose a global commitment policy.

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

True three-way preserves:

- two original limpers;
- one limper + one post-raise coldcaller;
- two post-raise coldcallers.

4/5/6-way preserves all-limper / mixed / all-postraise-coldcaller composition and exact field size.

### 3BP and squeeze

Implemented HU and multiway.

HU distinguishes:

1. original opener;
2. pre-3bet coldcaller surviving a squeeze;
3. post-3bet coldcaller.

Multiway preserves exact live opener/pre3bet-caller/post3bet-caller counts and exact 3/4/5/6-player field size. Plain 3BP and squeeze never share a generic fallback.

### Ordinary multiway SRP

Implemented:

- true three-way FIRST/MIDDLE/LAST with exact caller composition;
- exact 4/5/6-way parents.

The true-threeway BTN-last source ancestry is only A/P because the DeepCrusher audit itself identifies that branch as a human-reviewed gap fill rather than a dedicated Starting Strategy tree. FIRST/MIDDLE and four-way+ are P-heavy and explicitly labelled.

### 4BP

Gate 01I now reconstructs only clean first-orbit histories that aggregate OpenPPL preflop masks can support conservatively.

Implemented HU families:

- true-HU standard opener4: SB/Button 4bettor IP vs BB 3bettor-call;
- reduced-HU opener4 vs 3bettor-call, IP/OOP;
- reduced-HU cold4 vs original opener-call, IP/OOP;
- reduced-HU cold4 vs original 3bettor-call, IP/OOP.

Still fail-closed:

- non-raiser HU survivor in a 4BP because exact call stage is not proven;
- reversed/limp-reraise/backraise chronology;
- multiway 4BP action policy;
- 5bet+.

This is an evidence limitation, not a blanket anti-aggression rule. Normal 100bb 4BP can reach low SPR and may legitimately support aggressive one-pair/draw lines.

## CBet size runtime

Strategic IDs remain:

- `1` ~33%;
- `2` 50%;
- `3` 75%;
- `4` pot;
- `0` check/uncovered.

`CashCrusher_Flop_CBet_Betsize.txt` now maps these IDs to native OpenPPL actions:

- `BetThirdPot`;
- `BetHalfPot`;
- `BetThreeFourthPot`;
- `BetPot`.

OpenHoldem source was checked: `f$allin_on_betsize_balance_ratio` can later affect `f$betsize` and all betpot actions. Gate 01K deliberately does not make a global decision about that callback. DeepCrusher's historical ~60%-of-stack BetMax promotion remains a per-context audit target.

## Static quality state

Latest reviewed CBet integration passed the GitHub static lint after multiway integration, clean HU 4BP integration and native size-adapter additions.

The linter checks hard errors for:

- unresolved/duplicate `f$cc_*`;
- executable legacy `f$game_*` dependencies;
- open-ended/nested-looking `WHEN` scope;
- missing local Source/Provenance comments in reviewed `CashCrusher_Flop_CBet*` strategy modules.

Stack-sensitive DeepCrusher mechanisms are review warnings/targets, not globally prohibited.

## Known documentation debt

`CashCrusher_Context.txt` still has many functions documented only by section rather than by individual Purpose/Source/Provenance comments. CI reports those as warnings. Gate 01A.5 remains open until the file is fully retrofitted and the requirement can safely be promoted from warning to error.

## Release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. deterministic CBet policy fixtures/replays;
3. whole-bot `f$BestBetsize` ownership integration;
4. stack-sensitive size/commitment audit;
5. skipped-CBet X/C/X/R and turn follow-through coverage;
6. complete supporting-function provenance comments;
7. final regression and unknown-state fail-closed audit.

## Current development direction

Immediate work is now split between:

- finishing Gate 01A.5 per-function context comments;
- continuing Gate 01K stack-sensitive sizing review without globally trusting or disabling inherited mechanisms;
- building deterministic Gate00/Gate01 runtime fixtures before the Flop CBet gate is called release-certified.
