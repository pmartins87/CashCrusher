# Gate 07F — isolation-pot Flop Donk audit

Status: **reviewed check-range baseline with exact limper/coldcaller provenance**.

## Source boundary

The Framework routes `GotRaised_or_Isolated` FIRST/MIDDLE states with nothing to call into the generic Flop Donk move node. That establishes **ownership ancestry**, not a positive strategy.

The mature `f$move_flop_donkbet` audit explicitly keeps positive source policy only for `(BBorSB)v2pp`. There is no dedicated multi-handed ISO first-action Donk table in the supplied Starting Strategy.

The source material that does discuss ISO play focuses on reacting to the isolator's CBet or exploiting a **missed** ISO CBet with a Float. That strongly supports keeping the first-action OOP range reactive rather than manufacturing a lead.

## Exact range provenance

Gate07F preserves the Gate01E caller decomposition:

- **original limper** before the isolation raise;
- **post-raise coldcaller** who first entered after the isolation raise.

Those ranges are not merged even though both receive the same initial check action in this baseline.

The policy covers both:

- preflop-reduced HU versus the actual isolation raiser;
- current multiway ISO where Hero is FIRST/MIDDLE.

## Cash policy

All reviewed ISO Donk states **check** on Hero's first flop action.

That is a deliberate P/A policy because:

- the isolator owns the uncapped preflop aggression and has a natural CBet range;
- Hero's original-limper and post-raise-coldcaller ranges are selected differently, but neither has source-backed positive lead frequencies;
- checking preserves check-raise/check-call strategy and allows Flop Float when the isolator later checks;
- multiway ISO especially requires strong exact nut/range-advantage evidence before creating a lead frequency.

A future solver-backed exact board/range exception can precede this check parent. Until then, no generic TP+, draw or air Donk is inferred from the `(BBorSB)v2pp` tree.

## Not covered

- true-HU SB limp -> BB raise -> call, because SB is IP and BB is PFA rather than a Donk owner;
- ordinary SRP;
- plain 3BP/squeeze;
- 4BP+;
- any response after the isolator actually CBets.
