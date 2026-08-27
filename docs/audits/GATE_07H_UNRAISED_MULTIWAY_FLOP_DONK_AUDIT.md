# Gate 07H — residual unraised multiway Flop Donk audit

Status: **professional-theory fill with source-anchored multiway constraints**.

## Source boundary

The Framework routes limped/no-initiative FIRST/MIDDLE states to the generic Flop Donk owner, but the supplied positive source tree is exact `(BBorSB)v2pp`. Gate07B/C already own that BTN+both-blinds family.

For the remaining unraised 3-6 handed multiway pots there is no dedicated Starting Strategy action table. Treating source silence as “always check” would be safe but unnecessarily passive because these pots have **no preflop aggressor** to whom Hero can defer the betting initiative.

Gate07H therefore uses a clearly labeled **P fill**, not a transplant.

## Professional baseline

The baseline has no air Donks.

Three-way residual unraised pots may lead:

- robust 2P+ value broadly;
- overpairs and strong top pair only on low/mid, non-A-high, non-2+BW structures where protection/value is meaningful;
- premium draws on blind/range-friendly low/mid structures when the source-derived draw-check parent (A-high / completed / 2+BW) is absent.

Four-plus-way pots tighten materially:

- robust 2P+ value;
- only nut/combo draws as no-made pressure on favorable low/mid structures;
- one-pair value, ordinary draws and air check.

This preserves the source lesson that multiway opponents are relatively honest and that Hero should not manufacture folds without equity, while accounting for the absence of a preflop aggressor in a limped pot.

## Stack-depth migration

The source's draw-heavy `SPR ~1:1 -> POT` concept is retained only for robust 2P+ value and translated with **deepest effective SPR <=1.25**.

That is a flop sizing decision only. It does not grant a future Turn jam, call-vs-raise or stack-off.

## Covered domain

- pot family 1 (no preflop raise);
- current multiway, at least three flop entrants;
- Hero is an unraised caller/limper or BB check-option player;
- Hero is FIRST/MIDDLE with nothing to call;
- exact native/4-6h BTN+both-blinds Gate07B/C families excluded.

## Not covered

- HU unraised states already owned by Gate07D where applicable;
- ordinary SRP / ISO / 3BP / squeeze;
- 4BP+;
- response after a lead is raised.
