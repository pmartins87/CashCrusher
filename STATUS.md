# CashCrusher Status

Last update: 2026-08-23

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime gates are passed.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem.
- Runtime must support hands dealt 2h, 3h, 4h, 5h or 6h as seats empty/sit out.
- Preflop is currently used to reconstruct post-flop context/ranges.
- Strategic provenance is mandatory: T / A / P / X.
- Source-derived and professional-theory rules remain explicitly distinguishable.
- Unknown/unsupported strategic context fails closed.
- OpenPPL strategy code uses flat complete `WHEN` rules; indentation is never logical scope.

## Corrected stack-depth migration rule

A previous CashCrusher note went too far by globally banning/zeroing commitment helpers merely because DeepCrusher is short-stack Spin strategy. That has been rolled back.

Current rule:

- do **not** assume DeepCrusher TP+/draw/commitment frequencies transfer unchanged to ordinary 100bb cash;
- do **not** assume the opposite either;
- `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, `BetMax` and related mechanisms are not globally banned or forced to zero;
- review each stack-sensitive rule in its exact pot/range/board/action/effective-stack/SPR context;
- classify locally as T, A, P or X.

`CashCrusher_SPR_Commitment.txt` now contains only stack/SPR geometry and does not override `f$allin_on_betsize_balance_ratio`.

The linter now reports legacy commitment helpers as **warnings**, not errors.

## Gate 00 — mechanical context foundation

Complete in design/code; runtime validation still pending:

- 00A legacy Spin game labels decomposed into strategic properties;
- 00B HU six-max ancestry/matchup matrix;
- 00C context engine: pot family, Hero role, absolute/relative position, matchup, masks/history;
- 00D cash-depth effective-stack and SPR reconstruction;
- 00E exact true-multiway context/composition architecture;
- 00F dynamic 2-6 handedness and HU-origin preservation.

Critical invariant: current HU is split into true-HU deal, preflop-reduced HU and postflop-reduced HU.

## Gate 01 — Flop CBet

### Implemented ordinary one-raise families

Reviewed A/P baselines exist for:

- true-HU ordinary SRP: SB/Button PFA IP vs BB;
- true-HU SB limp -> BB raise -> SB call: BB PFA OOP;
- 3-6h ordinary SRP reduced HU: PFA IP vs BB;
- 3-6h ordinary SRP reduced HU: PFA IP vs SB;
- 3-6h ordinary SRP reduced HU: SB PFA OOP vs BB;
- 3-6h ordinary SRP reduced HU: opener PFA OOP vs later-position cold caller.

### Implemented ISO families

HU ISO preserves whether sole Villain is:

- original pre-raise limper; or
- post-raise cold caller.

IP/OOP baselines exist for both. Multiway ISO remains pending.

### Implemented plain 3BP families

`CashCrusher_3BP_Context.txt` distinguishes sole HU Villain as:

1. original opener who called the 3bet;
2. pre-3bet cold caller who survived a squeeze;
3. post-3bet cold caller.

Plain 3BP baselines exist for:

- true-HU standard BB 3bettor OOP vs SB/Button opener-call;
- reduced-HU 3bettor IP/OOP vs original opener-call;
- reduced-HU 3bettor IP/OOP vs post-3bet cold caller.

### Implemented HU squeeze families

`CashCrusher_Flop_CBet_Squeeze.txt` now covers all three HU survivor types separately:

- squeeze vs original opener, IP/OOP;
- squeeze vs pre-3bet cold caller, IP/OOP;
- squeeze vs post-3bet cold caller, IP/OOP.

These are explicitly P-heavy because DeepCrusher has no clean dedicated deep-stack squeeze tree. Generic source board/hand/IP-OOP architecture is A; exact squeeze ranges/frequencies are P.

### Current size contract

Current CBet policy exposes size IDs:

- 1 = ~33% pot;
- 2 = ~50%;
- 3 = ~75%;
- 4 = pot reserved.

A size ID is only the current flop sizing intention. Any stack-sensitive conversion remains a separate review question, not something this router decides globally.

### Still fail-closed / pending

- multiway ISO CBet;
- multiway ordinary 3BP/squeeze CBet;
- 4BP CBet;
- true multiway ordinary SRP CBet;
- final betsize execution callback wiring;
- skipped-CBet X/C/X/R follow-through;
- parser/runtime certification.

## Safety/quality infrastructure

Static linter currently checks as hard errors:

- unresolved/duplicate `f$cc_*`;
- executable legacy `f$game_*` dependencies;
- open-ended/nested-looking `WHEN` scope;
- missing local Source/Provenance comments in reviewed `CashCrusher_Flop_CBet*` modules.

It warns, but does not prohibit, uses of stack-sensitive DeepCrusher helpers or explicit all-ins.

Supporting `CashCrusher_Context.txt` still has many per-function provenance warnings; finishing those comments remains a documentation subgate.

## Validation state

Required before merge/release:

1. current-head GitHub static lint PASS;
2. OpenPPL parser validation with actual OpenHoldem parser;
3. deterministic Gate00 context fixtures;
4. deterministic Gate01 policy fixtures;
5. final betsize runtime mapping;
6. skipped-CBet follow-through coverage;
7. no table-ready claim before those gates pass.

## Current development direction

Next strategic work after current-head lint: multiway raised-pot CBet architecture, beginning with true three-way ordinary SRP because DeepCrusher has the strongest direct multiway ancestry there. Four-way+ and multiway squeeze/3BP remain separate P-heavy parents.
