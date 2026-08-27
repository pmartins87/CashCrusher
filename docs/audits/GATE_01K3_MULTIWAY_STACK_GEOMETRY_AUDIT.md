# Gate 01K.3A — Multiway stack-geometry audit

## Question

Which effective-stack notion should CashCrusher use when a multiway flop contains opponents with different stack depths?

The answer is **not one universal number**.

## Source facts

### DeepCrusher

The audited DeepCrusher implementation defines its backup effective stack from the **biggest active opponent**:

- `f$TheBiggestActiveOpponentsChips_BKP = balance_bigstackchair + currentbet_bigstackchair`;
- `f$EffectiveStack_BKP = min(Hero chips, biggest-active-opponent chips) / BB`.

Therefore, in a multiway pot, the DeepCrusher effective-stack ancestor corresponds to CashCrusher's **deepest effective relationship**:

`min(Hero, max(live opponent stacks))`.

This is a source fact about the helper's mechanics. It does **not** prove that every downstream short-stack strategic threshold should transfer to 100bb cash.

### OpenHoldem

OpenHoldem's all-in adjustment compares a requested raise-to size against a configurable fraction of Hero's total available balance (`currentbet + balance`). `BetPot` actions first calculate their requested raise-to amount and can then be converted to all-in by `f$allin_on_betsize_balance_ratio`.

OpenHoldem also caps an entered betsize at Hero's available balance. Natural clipping by Hero's balance and strategic promotion to all-in are therefore separate concepts.

## CashCrusher correction

The first Gate00 SPR implementation retained the shortest live opponent as a coarse multiway descriptor. That is useful for detecting short-stack/sidepot geometry, but it is unsafe as a universal multiway strategic SPR.

CashCrusher now preserves both:

- **shallowest effective** = `min(Hero, min(live opponent stacks))`;
- **deepest effective** = `min(Hero, max(live opponent stacks))`.

Example:

- Hero 100bb;
- Villain A 18bb;
- Villain B 100bb.

Then:

- shallowest effective = 18bb;
- deepest effective = 100bb.

A top-pair/overpair CBet rule must not treat the whole 3-way pot as an 18bb-effective pot merely because Villain A is short while Villain B remains 100bb effective.

## Strategic ownership

The two bounds answer different questions.

| Geometry | Correct use |
|---|---|
| Shallowest effective | detect that at least one opponent can become all-in / sidepot-limited |
| Deepest effective | determine whether Hero still faces a materially deep live opponent |
| Actor-specific effective | price a call/raise/stack decision against a specific bettor/raiser |

For current multiway Flop CBet policy, low-SPR exceptions involving one-pair hands now use the **deepest effective SPR**. This means an exception such as “allow this stronger one-pair bet when SPR < 4” only fires if **every** live effective opponent relationship is below 4.

This is a conservative P-level CashCrusher policy decision, not a claim that deepest SPR is the only relevant multiway variable in poker.

## CBet files reaudited

The following were changed so generic shallowest-based `f$cc_spr_round_start` no longer controls their multiway one-pair exceptions:

- `CashCrusher_Flop_CBet_Multiway_SRP.txt`;
- `CashCrusher_Flop_CBet_Multiway_SRP4Plus.txt`;
- `CashCrusher_Flop_CBet_Multiway_ISO.txt`;
- `CashCrusher_Flop_CBet_Multiway_ISO4Plus.txt`;
- `CashCrusher_Flop_CBet_Multiway_3BP.txt`.

The linter now rejects ambiguous generic SPR helpers in `CashCrusher_Flop_CBet_Multiway_*` strategy modules.

## All-in / sizing implications

The historical DeepCrusher mechanisms remain separate audit targets:

1. explicit sizing-router promotion near **60% of Hero StackSize**;
2. `f$allin_on_betsize_balance_ratio`, including a special **~50% effective-stack** trigger and a Hero-balance fallback;
3. `f$Raise_Committed`, which can convert an already-approved flop/turn call into an all-in raise around a separate **~55%** geometry.

None is globally disabled. None is globally trusted.

For multiway CBet diagnostics, the source-faithful analogue of DeepCrusher's 50%-effective test uses the **deepest effective** denominator. Reaching only the shallowest opponent is instead recorded as a potential sidepot-divergence state.

## New deterministic contract

`tools/test_multiway_stack_geometry.py` validates examples and invariants including:

- equal stacks;
- one short + one deep opponent;
- Hero capping the deepest relationship;
- Hero shorter than every opponent;
- multiway raised-pot asymmetry;
- a case where shallowest-effective would falsely trigger a 50%-effective interpretation while deepest-effective correctly does not;
- a requested bet that reaches the short opponent but not the deep opponent.

This test is now executed in GitHub Actions together with the static OpenPPL linter.

## Remaining work

This gate does **not** yet define CashCrusher's global `f$allin_on_betsize_balance_ratio` or a universal CBet-to-jam rule.

The next sizing audit must distinguish:

- physical/natural all-in because Hero cannot make the requested size without exhausting balance;
- effective all-in versus all live opponents;
- sidepot divergence (short opponent reached, deeper opponent not reached);
- strategic promotion of an otherwise legal smaller bet to Hero all-in;
- HU versus multiway;
- pot family / range topology / hand class / board / projected next-street SPR.

Only the first two are primarily mechanical. Strategic promotion remains node-sensitive.
