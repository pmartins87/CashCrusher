# Gate 01E.3 — True three-way ISO flop CBet audit

Status: **first true-threeway ISO baseline implemented; four-way+ ISO remains separate**.

## Exact scope

- exactly three players entered and remain on flop;
- Hero made the sole preflop raise after at least one proven limper;
- Hero is PFA/final aggressor;
- no flop bet before Hero acts;
- ISO survivor provenance is mechanically reconstructed.

## Source boundary

DeepCrusher has HU ISO/limped initiative structure and true-threeway positional knowledge, but no clean deep-stack **isolator versus two surviving opponents** CBet tree.

Therefore:

- pot-history/routing architecture is A;
- exact true3 ISO frequencies are P-heavy;
- a HU isolator policy must not leak into a two-opponent ISO pot.

The source's multiway material supports a conservative principle: weak-equity flop/turn aggression should be reduced versus two ranges. That remains an A constraint, not an exact frequency table.

## Survivor composition

CashCrusher distinguishes the two live opponents as:

1. **two original limpers**;
2. **one original limper + one post-raise cold caller**;
3. **two post-raise cold callers**.

The exact masks remain available, so these broad parents do not erase seat/range identity.

The two-limper family is generally the widest/weakest continuation parent; the two-coldcaller family is generally the most selected/condensed. These are professional range-topology assumptions P, not site-specific exact ranges.

## Relative position

FIRST / MIDDLE / LAST remain separate:

- LAST may apply the most pressure after two checks;
- MIDDLE must account for a player behind;
- FIRST is most check-heavy.

## Baseline strategy

- robust value bets broadly;
- strong TP/overpair value bet suitable static boards;
- medium/weak TP tighten sharply compared with HU ISO;
- premium draws remain the main semi-bluff region;
- pure air is restricted to best-backdoor static-high selections when LAST, mainly versus two limpers;
- no blanket air tail.

## Stack depth

No stack-sensitive DeepCrusher helper is globally disabled. This gate owns the flop CBet/check and size family only. Later raise/call/jam behavior gets its own exact SPR/range review.

## Outside scope

- four-way+ ISO;
- multiway 3BP/squeeze;
- 4BP;
- post-CBet raise defense;
- later streets.
