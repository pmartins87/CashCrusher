# Gate 01E — HU ISO flop CBet audit

Status: **HU source/theory audit complete; multiway ISO remains separate**.

## Scope

This audit covers flop continuation betting when:

- the hand started with 3–6 dealt players;
- at least one player limped before Hero's sole preflop raise;
- Hero is the final and only preflop aggressor;
- the flop is reached heads-up after preflop folds;
- Hero is checked to / has no flop bet to call.

True HU `SB limp -> BB raise -> SB call` is **not** ISO in CashCrusher and remains in the true-HU limp-raised family.

## Critical survivor distinction

A proven isolation raise does not tell us who survived to the flop.

Two strategically different descendants exist:

1. **isolator vs original pre-raise limper**;
2. **isolator vs post-raise cold caller**.

Example:

`UTG limp -> HJ raise -> BTN call -> UTG fold` reaches a HU flop against BTN. Calling this simply "isolator vs limper" would assign the wrong range to Villain.

`src/CashCrusher_ISO_Context.txt` therefore retains pre-raise-limper and post-raise-cold-caller masks separately.

## Source evidence from DeepCrusher

DeepCrusher does not contain a complete deep-cash ISO CBet strategy. The useful source material is structural.

### `3wBBvSB` — "Facing Check (ISO/LP/SRP)"

The audited source explicitly describes this checked-to tree as route-invariant across ISO/LP/SRP. Useful principles:

- TP+ bets small on dry/static boards and larger on dynamic boards;
- high/marginal pairs often check/delay;
- real draws can bet while retaining different response plans versus a raise;
- dry air can use a small bet while wet air often checks.

Classification: **A**. The action-shape is useful, but the exact ranges, shallow-stack thresholds and raise-response commitment plans are not transferable literally.

### HUSB / 3wBTNvBB / 3wBTNvSB

These provide corroborating CBet principles:

- high-card/static boards support broader small betting;
- low connected boards require more selective betting;
- marginal showdown value belongs partly in the check-back range;
- draw quality matters;
- IP and OOP must not share one policy.

Classification: **A**, not T for ISO frequencies.

### Rejected source components

The following are **X** for CashCrusher ISO baseline:

- `<=16/20 BB` commitment/sizing splits;
- `StackOffDraws` as an action category;
- automatic shove plans after a CBet is raised;
- blanket residual-air betting inherited from shallow HU/Spin trees.

## Professional six-max fill — P

The format gap is substantial, so the baseline uses widely accepted deep-stack NLHE principles and labels them P rather than pretending they came from Crusher.

### Isolator vs original limper

Typical limp-call ranges are wider and less structurally protected than a normal cold-call range. As a result, the isolator often retains meaningful range advantage on high-card/static boards.

Baseline consequence:

- IP isolator can CBet static A/K/Q and paired boards relatively wide using selected backdoor air;
- OOP isolator still checks materially more because position dominates future realization;
- low/middle connected boards strongly interact with limp-call suited/pair holdings, so air frequency falls and value/draw bets become more selective/polar;
- marginal one-pair hands protect checking ranges at higher SPR.

This is **P** baseline logic, not an exact solver frequency claim.

### Isolator vs post-raise cold caller

A player who cold-calls after an isolation raise is not treated as a limper. That range is generally more condensed/selected and can contain many pocket pairs, broadways and suited hands that realize well.

Baseline consequence:

- CBet is more selective than versus the original limper;
- marginal pairs check more;
- static high-card boards remain the main bluff-pressure parent;
- dynamic low/mid boards are heavily checked except robust value/premium-equity combinations;
- OOP cold-caller descendants are especially check-heavy.

Again this is **P** professional fill.

## Sizing abstraction

CashCrusher keeps the project-wide deep-stack flop palette:

- `1` = small, about 33%;
- `2` = medium, about 50%;
- `3` = large, about 75%;
- `4` = pot, reserved and not used by this baseline;
- `0` = check / no CBet.

Static high/paired pressure tends toward small sizing. Dynamic boards use medium or large sizing for the robust part of the range. No size implies an automatic jam.

## Fail-closed rule

HU ISO policy fires only if the surviving Villain can be proven to belong to exactly one of:

- pre-raise limper mask;
- post-raise cold-caller mask.

If the aggregate OpenPPL history cannot prove that survivor type, the strategy returns false / size 0 rather than guessing.

## Provenance summary

| Component | Provenance |
|---|---|
| checked-to ISO/LP/SRP structural tree | A from `3wBBvSB` |
| high/static vs low/dynamic board principles | A + P |
| limper-vs-coldcaller survivor separation | A/P architecture |
| exact deep-stack action frequencies | P |
| 33/50/75 mapping | A/P |
| shallow commitment/jam rules | X |
| multiway ISO extension | not yet implemented |
