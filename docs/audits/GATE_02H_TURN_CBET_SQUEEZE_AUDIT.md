# Gate 02H — Squeeze-pot Turn CBet

Status: **source boundary audited; policy is P-heavy and preserves three distinct survivor origins**.

## 1. Source boundary

DeepCrusher has no dedicated deep-stack squeeze second-barrel tree. The legacy `Init_GotRaised_Or_Isolated` family is broader than a squeeze and routes no-bet turn states through donk/float ownership rather than a clean squeeze-CBet node. Consequently, exact squeeze Turn-CBet frequencies cannot be attributed to Crusher.

Reusable A-level source principles are limited to current-strength-first evaluation, IP/OOP separation, runout/completion sensitivity, draw quality, protected checking ranges and conservative multiway treatment.

## 2. Three materially different continuation ranges

CashCrusher preserves:

1. **original opener** who called the squeeze;
2. **pre-3bet cold caller** who first flatted the open and then continued versus the squeeze;
3. **post-3bet cold caller** who entered after the squeeze.

The second and third categories are not interchangeable with opener-call. They have survived a more selective preflop path, and a flop CBet call selects them further.

## 3. HU that arose only after a multiway flop

If squeeze pot began flop multiway and becomes HU only after Hero's flop CBet, current handedness cannot erase the multiway selection event. The sole survivor is rematched to opener/pre3bet/post3bet masks and receives an additional selection penalty.

## 4. Professional-theory baseline

Squeeze ranges are tighter and more polarized/selected than ordinary SRP and usually more selected than plain 3BP. The first deterministic baseline therefore:

- keeps trips+/strong two-pair active;
- value-barrels overpair/strong TP primarily on cleaner turns and with position/depth support;
- checks medium/weak TP aggressively against pre3bet/post3bet coldcaller continuations;
- barrels premium draws mainly IP and selectively OOP on favorable pressure turns;
- greatly restricts pure-air second barrels; only the opener-survivor IP family receives a narrow quality-air/high-pressure candidate;
- uses no pure-air baseline against pre3bet/post3bet coldcallers;
- uses no pure-air baseline multiway.

These are P rules, not solver-exact frequencies.

## 5. Multiway squeeze

Current live composition preserves opener, pre3bet-coldcaller and post3bet-coldcaller counts. A field containing selected coldcaller-origin ranges is treated more strongly than opener-only continuation. Four-way+ or large-flop-size origins tighten further. Deepest-effective SPR controls any field-wide low-SPR relaxation.

## 6. Stack-depth rule

Natural low SPR in squeeze pots may make strong one-pair hands willing to play large pots in some exact nodes. That does **not** justify importing the Spin-wide TP+ stackoff behavior. This Gate chooses only the turn bet/check and its strategic size ID. Response to a raise remains a separate node.

No inherited commitment helper is globally disabled by this audit.

## 7. Fail-closed boundary

Squeeze Turn-CBet fails closed if subtype proof, survivor origin, multiway composition, flop-action provenance, or stack geometry is inconsistent. Plain-3BP policy is never a squeeze fallback.
