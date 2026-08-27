# Gate 01 — Cash-depth review of DeepCrusher commitment rules

Status: **corrected after rollback of an over-broad migration rule**.

## Correction

The earlier version of this note extrapolated too far from one valid observation: DeepCrusher is short-stack Spin strategy, so many TP+/draw/commitment lines may not transfer unchanged to a 100bb cash environment.

That does **not** justify globally disabling or prohibiting:

- `f$Raise_Committed`;
- `f$hand_StackOffDraws`;
- `f$allin_on_betsize_balance_ratio`;
- `BetMax` / explicit all-in actions.

The CashCrusher rule is now narrower and source-faithful:

> **Audit stack-sensitive DeepCrusher rules in the exact cash context before reusing them. Do not assume short-stack logic survives; do not assume it fails either.**

## What still remains true

A hand label such as TP+, overpair, strong draw or two-pair is not enough by itself to prove that the same stack-off frequency used in short-stack Spin is correct at 100bb. The relevant decision can depend on:

- pot family: limped / SRP / ISO / 3BP / squeeze / 4BP;
- Hero and Villain range provenance;
- IP/OOP or multiway relative position;
- exact board/runout;
- effective stack and SPR;
- action size and prior street history;
- number of opponents.

This is a **review requirement**, not a prohibition.

## How to migrate a DeepCrusher commitment rule

For every stack-sensitive source line, classify it locally:

- **T — Transplant:** the same effective-stack/SPR geometry and strategic meaning still apply;
- **A — Adapt:** the source idea remains useful but threshold, scope, sizing or range must change;
- **P — Professional fill:** the source does not answer the deeper cash case sufficiently;
- **X — Reject:** the rule is genuinely dependent on shallow Spin geometry.

Do not classify the function name globally. `f$Raise_Committed`, for example, may be wrong in one node and useful in another low-SPR cash node.

## Specific note on TP+

The practical warning that triggered this audit remains important: DeepCrusher frequently reaches stack commitment with TP+ because short-stack Spin SPRs are small. CashCrusher must not mechanically copy that *frequency* to ordinary 100bb pots.

But neither should it hardcode the opposite rule. A top pair or overpair can absolutely be a stack-off in some 3BP/4BP/low-SPR/range matchups. The correct answer belongs to the exact node.

## `f$allin_on_betsize_balance_ratio`

CashCrusher no longer overrides this callback to `0.00` merely because the source game was short stacked. Its eventual definition belongs to the sizing/commitment audit. The DeepCrusher callback should be treated as source material to test/adapt, not as automatically valid or invalid.

## Linter behavior

The linter now treats legacy commitment helpers and explicit all-ins as **review warnings**, not errors. The warnings exist only to make sure short-stack inheritance is noticed and commented when it enters CashCrusher code.

## Bottom line

The migration rule is deliberately conservative in both directions:

- do not copy short-stack commitment automatically;
- do not ban useful commitment machinery automatically.

Review the exact poker state and preserve source provenance.
