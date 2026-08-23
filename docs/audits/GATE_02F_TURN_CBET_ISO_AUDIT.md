# Gate 02F — Turn CBet after an isolation raise

Status: **source boundary audited; strategic policy must be P-heavy with exact limper/coldcaller provenance**.

## 1. Critical source finding

The original Crusher/DeepCrusher routing does **not** provide a clean dedicated "isolator CBet flop -> second barrel turn" tree.

Preflop histories grouped under `f$Init_GotRaised_Or_Isolated` are routed on turn through `f$turn_Raise_GotRaised`. In that legacy router:

- FIRST/MIDDLE with nothing to call goes to **turn donkbet**;
- LAST/MIDDLE with nothing to call goes to **turn floatbet**.

So the source deliberately conflates several histories that CashCrusher now separates. It would be false provenance to take ordinary `f$move_turn_cbet` or the old GotRaised router and call it a dedicated ISO second-barrel strategy.

Therefore the ISO Turn-CBet strategy below is **P-heavy**. DeepCrusher remains useful for:

- current-strength-first reclassification;
- IP/OOP separation;
- runout/completion caution;
- draw quality;
- source preference for protected OOP checking ranges;
- multiway selectivity.

Those are A-level constraints, not exact ISO frequencies.

## 2. Range provenance remains mandatory

CashCrusher already reconstructs two fundamentally different ISO caller origins:

1. **original limper** who limp-called the isolation raise;
2. **post-raise cold caller** who entered after the isolation raise.

They must remain distinct on turn.

The coldcaller range is generally more selected/condensed than an original limp-call range. After calling a flop CBet, both ranges are further selected, especially after a larger flop size.

## 3. Postflop-reduced HU ISO

An ISO pot may begin flop multiway and become HU only after the flop CBet. The current sole Villain must be re-matched to the original pre-raise-limper or post-raise-coldcaller masks. The ordinary HU ISO helpers intentionally used preflop-reduced-HU guards, so Turn needs its own cross-street survivor proof for origin=3.

Current HU after multiway flop must not inherit a flop-HU ISO range merely because only two players remain.

## 4. Professional-theory baseline

### HU versus original limper

Compared with a post-raise coldcaller, limp-call ranges are generally wider and contain more dominated/marginal holdings. A deterministic cash baseline may therefore value barrel robust one-pair somewhat more often and retain selected premium/good-draw semibluffs, especially IP and on clean/high-pressure turns.

### HU versus post-raise coldcaller

The continuing range is more selected. Medium/weak TP and marginal draws check more. Pure-air second barrels require a much stronger range/runout case and are omitted from the first baseline OOP.

### Multiway ISO

When 3+ players remain after the flop CBet:

- robust value dominates;
- two-pair and one-pair are runout/depth/composition sensitive;
- premium draws are selective and position sensitive;
- pure air is absent from the initial four-way+ baseline;
- deepest-effective SPR controls field-wide low-SPR relaxations.

## 5. Stack-depth rule

The short-stack source is a review flag only. No inherited ISO TP+/draw rule is deleted merely because cash starts at 100bb, and no old short-stack stackoff behavior is imported merely because the current hand class is TP+.

A second barrel means **bet this turn**. Response to a raise and willingness to play stacks are separate future nodes using actor-specific effective geometry.

## 6. Fail-closed boundary

ISO Turn-CBet fails closed when:

- ISO history is not proven;
- sole HU survivor cannot be assigned exactly to limper or post-raise coldcaller;
- multiway live composition cannot be reconciled with the two ISO provenance masks;
- actual standard flop CBet history is absent;
- current context/stack geometry is invalid.

No ordinary-SRP, 3BP or generic GotRaised child is used as fallback.
