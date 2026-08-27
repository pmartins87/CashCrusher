# Gate 07E — residual multiway ordinary-SRP Flop Donk audit

Status: **reviewed check-range baseline outside the exact BTN+both-blinds families**.

## Source boundary

The legacy Framework sends FIRST/MIDDLE no-initiative SRP states to the Flop Donk move node, but the mature DeepCrusher audit explicitly limits positive source Donks to `(BBorSB)v2pp`.

The dedicated 3wSBvBTN / 3wBBvBTN material is also reactive on flop: Hero checks to BTN and then selects X/R, X/C or fold by hand, board and sizing. That source does not authorize a generic first-action lead into an uncapped preflop raiser.

Gate07B/C already own the one exceptional high-ancestry shape where BTN+SB+BB all reach flop.

## Cash adaptation

For the remaining ordinary-SRP multiway OOP callers, CashCrusher uses a deliberate **range-check baseline**.

Reasons:

- the preflop raiser remains uncapped and still has CBet ownership;
- multiway ranges are more selected and bluff leads require stronger range/nut-advantage evidence than HU;
- no supplied solver dataset identifies exact board/range lead subsets for all UTG/HJ/CO/BTN versus multiple caller combinations;
- checking preserves the existing source architecture for check-raise/check-call defense rather than manufacturing an unsupported lead frequency.

This is a reviewed policy, not a missing fallback. A future solver-backed exact matchup/board exception can precede the broad check parent.

## Exact covered domain

- one-raise ordinary SRP;
- Hero is a preflop caller, never PFA;
- current flop is still multiway;
- Hero acts FIRST/MIDDLE with nothing to call;
- the exact native/source and 4-6h BTN+both-blinds families are excluded because Gate07B/C already own them.

## Not covered

- unraised/limped multiway outside BTN+both-blinds;
- ISO;
- 3BP/squeeze;
- 4BP+;
- postflop action after a Donk/check;
- any defense versus PFA CBet.
