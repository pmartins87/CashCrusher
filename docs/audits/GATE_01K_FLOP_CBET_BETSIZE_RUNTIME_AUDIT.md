# Gate 01K — Flop CBet betsize runtime audit

Status: **native size-ID adapter implemented; whole-bot `f$BestBetsize` integration and stack-sensitive conversion remain separate**.

## 1. OpenHoldem/OpenPPL runtime facts verified

The project OpenHoldem source confirms the following behavior:

- OpenPPL decisions greater than zero are treated as explicit betsize values in **big blinds**, then converted to dollars for `f$betsize`;
- percentage-pot OpenPPL actions are converted into an `f$betsize` raise-to amount;
- `BetThirdPot`, `BetHalfPot`, `BetThreeFourthPot` and `BetPot` are native OpenPPL actions and can therefore be used as a clean adapter for the strategic size IDs;
- `f$allin_on_betsize_balance_ratio` is a separate standard callback;
- that callback affects `f$betsize` **and all betpot functions**;
- when its evaluated value is `<= 0`, OpenHoldem's all-in adjustment is disabled;
- OpenHoldem's generated/default implementation is `0.00`, but CashCrusher does **not** interpret that engine default as a strategic conclusion that auto-all-in must always be disabled.

The last point is important: the earlier over-broad CashCrusher rule was rolled back. Whether the final formula should return a positive ratio in some exact contexts is a later stack-sensitive review question.

## 2. CashCrusher sizing ownership

The current flop-CBet strategy already returns one of these IDs:

| ID | Native adapter | Strategic meaning |
|---:|---|---|
| 0 | no bet / invalid | check or uncovered context |
| 1 | `BetThirdPot` | small, approximately 33% pot |
| 2 | `BetHalfPot` | medium, 50% pot |
| 3 | `BetThreeFourthPot` | large, 75% pot |
| 4 | `BetPot` | pot-sized, only where a reviewed child actually selects it |

This adapter does **not** decide whether a bet should be promoted to all-in. It only translates the child strategy's requested pot-fraction family into a native OpenPPL action.

## 3. Why no global all-in decision is added here

OpenHoldem applies `f$allin_on_betsize_balance_ratio` downstream to betpot/f$betsize actions. Therefore defining a universal ratio during the CBet-size adapter would silently affect not just one 4BP or low-SPR node, but potentially every betpot action using that callback.

CashCrusher consequently leaves the global callback outside Gate 01K. This is **not a prohibition**. It is separation of concerns:

- flop CBet policy chooses bet/check and requested size family;
- the native adapter converts the requested size family;
- later commitment/sizing audit decides whether the final whole-bot callback should be dynamic by context, remain at engine default, or whether explicit node-owned `BetMax` is preferable in particular situations.

## 4. Relation to DeepCrusher sizing

DeepCrusher's `f$BetsizeFlopHeadsup` / `f$BetsizeFlopMultiway` often performs a second transformation: if the requested pot-fraction bet consumes roughly 60% of the remaining stack, it returns `BetMax`.

That behavior is neither copied blindly nor deleted globally.

For CashCrusher it becomes a review target because:

- in an ordinary 100bb SRP, a 60%-of-stack promotion is often very different from the original Spin geometry;
- in a normal 4BP or some 3BP, starting at 100bb can still produce naturally low SPR, so a similar promotion may sometimes be strategically sound;
- the correct decision belongs to the exact pot/range/hand/board/SPR node, not to the historical fact that DeepCrusher used one threshold widely.

## 5. Fail-closed behavior

`f$cc_flop_cbet_native_betsize` returns `0` when:

- the CBet action router is false;
- the strategic size ID is invalid/uncovered.

A positive CBet must already satisfy `f$cc_flop_cbet_size_consistent` before runtime integration is considered valid.

## 6. Remaining Gate 01K work

Still required before a table-ready formula:

1. connect `f$cc_flop_cbet_native_betsize` into the eventual whole-bot `f$BestBetsize`/flop sizing router without stealing ownership from Donk/Float/defense nodes;
2. validate the native action return values in the OpenHoldem parser/runtime fixture;
3. audit stack-sensitive promotion separately, including the inherited 60%-of-stack behavior and `f$allin_on_betsize_balance_ratio` interaction;
4. ensure casino/tablemap betsize interpretation behaves correctly in the target environment.

Static CI can verify dependency and OpenPPL coding discipline, but it does not substitute for this runtime test.
