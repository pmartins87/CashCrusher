# Gate 01K.3C-4BP — Clean 4BP explicit flop-jam audit

## Question

After CashCrusher has already selected a flop CBet in a clean HU four-bet pot, should some current `33%/50%` sizes be replaced by an explicit strategic `BetMax` branch merely because the pot is naturally low SPR?

## Source boundary

DeepCrusher has no dedicated deep-stack 4BP flop-CBet strategy tree. Its reusable evidence is therefore structural:

- initiative and IP/OOP architecture;
- hand/board-class architecture;
- source sizing routers that sometimes promote a planned size to `BetMax` near 60% of Hero stack;
- `f$allin_on_betsize_balance_ratio`, including its approximately 50%-effective-stack behavior.

Those last two are real source mechanisms, but they were written for the short-stack Spin environment. They are **A-level evidence for near-commitment handling**, not a T-level 100bb four-bet-pot jam chart.

## Current CashCrusher 4BP policy

`CashCrusher_Flop_CBet_4BP.txt` already makes the strategically important choices before sizing:

- exact clean 4BP survivor topology is required;
- true HU and reduced-HU families remain distinct;
- opener-4bet and cold-4bet ranges remain distinct;
- IP/OOP remains explicit;
- current hand class and board texture select bet/check;
- positive CBet sizes are primarily 33% and 50%;
- a positive flop bet does not automatically authorize later stack-off.

The execution layer separately converts a requested size to `BetMax` when that requested size already reaches Hero's balance or the all-live effective relationship.

## Professional-theory assessment

Low SPR makes stack-off *possible* with materially wider value/equity regions than in a single-raised 100bb pot. It does not imply that a flop shove dominates small betting.

In four-bet pots, small flop sizes can remain strategically useful even at low SPR because they:

- preserve calls from dominated hands;
- permit high-frequency range betting on favorable static boards;
- maintain bluff/value sizing symmetry;
- leave a deliberately tiny turn stack that can be committed on selected runouts;
- avoid converting every planned bluff into an unnecessarily large risk.

Conversely, explicit flop jams can be appropriate on some dynamic boards, at very low residual SPR, and with exact value/equity classes. The current source set does not contain a precise deep-cash rule that identifies those combinations, and a universal threshold such as `requested >= 50% effective` would overwrite the authored 4BP size policy after the fact.

## Decision

### T/A — mechanically equivalent all-in

Already implemented in `CashCrusher_Flop_CBet_AllinEquivalence.txt`.

If the requested 33/50/75/pot CBet already reaches Hero's available balance or reaches the all-live effective relationship, `BetMax` is execution-equivalent and is allowed.

### A/P — historical 50/60% near-all-in promotion

Retained as diagnostic evidence in `CashCrusher_Flop_CBet_StackGeometry.txt`.

It is **not** promoted to one generic 4BP action rule.

### P — explicit 4BP strategic jam

No additional hardcoded jam branch is added at this gate.

This is not a claim that flop jams are absent from good 100bb 4BP strategy. It is a source-precision decision: the current evidence is insufficient to define a reliable deterministic jam subset that is better than the already-reviewed small/medium 4BP policy plus mechanically equivalent all-in handling.

A future solver/data-backed refinement may add exact node-owned jam branches, but each branch must specify at least:

- exact 4BP range topology;
- IP/OOP;
- board family;
- current hand/equity class;
- exact effective SPR;
- intended smaller size being replaced;
- why shove is preferred to the small/medium bet in that node.

## Important non-conclusion

This audit does **not** disable:

- later flop stack-off versus a raise;
- turn jams after a small flop CBet;
- `f$Raise_Committed` in the defensive nodes it actually owns;
- future 4BP explicit jams supported by stronger evidence;
- the final global all-in callback after all sizing owners are audited.

It only rejects the shortcut: `4BP + low SPR => auto-shove every positive CBet`.

## Gate result

**PASS — no extra strategic 4BP flop-jam rule is justified from the current evidence.**

The baseline remains 33/50 where the reviewed 4BP node selected those sizes, with `BetMax` only for mechanically/effectively equivalent execution until stronger node-specific evidence is available.
