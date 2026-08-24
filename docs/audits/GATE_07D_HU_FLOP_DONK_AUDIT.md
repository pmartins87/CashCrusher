# Gate 07D — HU / reduced-HU ordinary-SRP Flop Donk audit

Status: **reviewed check-range baseline**.

## Source finding

The Crusher Framework routes OOP/no-initiative single-raised `HUBB` and limped `HUBB-vlimp` states to `f$move_flop_donkbet` when nothing is currently to call.

The mature DeepCrusher audit of that move node is more restrictive: it states that the supplied Starting Strategy provides a positive **flop-donk** tree only for `(BBorSB)v2pp`, and all other router families fall through to check.

This is consistent with the dedicated HUBB / 3wBBvBTN / SBvBTN material. Their flop strategy is written primarily as **check -> respond to the aggressor's CBet** (X/R, X/C, or fold by hand/board/sizing), not as a positive first-action lead tree.

Therefore broad framework routing is treated as **A ownership ancestry**, not evidence for a positive HU Donk.

## Cash adaptation

For ordinary 100bb cash, checking the full OOP caller range to the preflop aggressor is also a standard strategically coherent simplification. Solver strategies can contain low-frequency leads on particular range/board interactions, but no supplied source or solver dataset in this project identifies an exact subset strongly enough to improve the hardcoded baseline without inventing frequencies.

Gate07D therefore marks the following as deliberately reviewed checks:

1. true-HU SB/Button opens, BB calls, BB acts first on flop;
2. true-HU SB/Button limps, BB checks option, BB acts first on flop;
3. 3-6 handed ordinary SRP reduced preflop to HU where Hero is the OOP caller and the sole Villain is the proven original PFA.

The third family includes the high-ancestry 3wSBvBTN / 3wBBvBTN shapes while also applying a professional range-check baseline to other exact opener-v-OOP-caller ordinary-SRP matchups.

## Why this is a reviewed policy rather than an uncovered hole

A check is an actual strategy choice here, not a failure to decide. It preserves:

- the source's reactive check-raise/check-call architecture;
- PFA's incentive to CBet air/value;
- Hero's full checking range rather than creating an unbalanced unsupported lead range;
- clean ownership for later Float/Probe/Delayed families when Villain checks behind.

A future solver-backed exact matchup/board Donk may override this **only as a specific exception before the broad check parent**.

## Boundaries

Gate07D does not own:

- ISO pots;
- plain 3BP / squeeze;
- 4BP+;
- postflop-reduced HU from a multiway flop;
- unraised 3-6 handed pots with non-HU-limp chronology;
- any current multiway shape.

It also does not authorize any response after checking; those are defensive CBet nodes.
