# CashCrusher

CashCrusher is the 6-max post-flop OpenPPL project derived from the audited DeepCrusher / Crusher Framework work.

The project goal is to reuse as much validated post-flop knowledge as possible from the Spin&Go codebase while rebuilding the parts that are format-dependent: six-max range interactions, deeper-stack SPR geometry, non-all-in 3-bet/4-bet pots, and additional positional matchups.

## Scope

- Post-flop only for the current phase.
- OpenPPL / OpenHoldem runtime target.
- 6-max positions: UTG, HJ, CO, BTN, SB, BB.
- Reuse c-bet, donk, float, probe, delayed-bet, defense, board-texture, hand-class and cross-street state machinery when strategically valid.
- Do not transplant short-stack all-in logic mechanically.

## Strategic provenance

Every migrated rule should be classified as one of:

- **T — Transplant:** source rule is directly reusable.
- **A — Adapt:** source principle survives, but ranges, sizing, SPR or thresholds need adaptation.
- **P — Professional-theory fill:** source does not answer the 6-max spot adequately; fill deliberately from established NLHE strategy principles.
- **X — Reject:** rule is too dependent on Spin&Go / short-stack geometry to be a valid 6-max basis.

Source-derived logic and professional-theory additions must remain distinguishable in code comments and audit documents.

## Current stage

Gate 00 establishes the six-max context model before any individual post-flop attack/defense function is ported.

See `STATUS.md`, `ROADMAP.md`, and `docs/architecture/`.