# Gate 03E — Plain 3-bet-pot River CBet

Status: **P-heavy policy boundary frozen**.

DeepCrusher has no dedicated deep-stack 3BP three-barrel tree. Its normal River-CBet source architecture is useful, but ordinary Spin game labels do not encode a 100bb cash 3BP range pair. Exact River decisions therefore remain P-heavy.

CashCrusher preserves the same plain-3BP survivor split used on Flop/Turn:

- original opener who called the 3bet;
- post-3bet coldcaller.

A River that becomes HU only after a multiway Turn preserves that multiway selection event. Current HU cannot erase it.

## Professional baseline

3BP River SPR is often naturally lower than SRP. This supports more value continuation with OP/strong TP in some clean runouts, but **does not create automatic TP+ stack-off**. Completion/four-card Rivers still reduce one-pair value when meaningful depth remains.

The opener-call family may carry a narrow missed-premium-draw bluff on clean high-pressure Rivers IP with useful high-card/blocker structure. The post-3bet-coldcaller family is more selected and receives no pure-air baseline in this first deterministic pass.

Multiway 3BP remains strongly value-heavy. Deepest-effective River SPR controls field-wide low-SPR relaxations.

Any future all-in is owned by the River execution/stack-geometry layer or a separately audited exact strategic jam node, not by the hand class alone.
