# Gate 01K.3 — Stack-sensitive CBet sizing audit

Status: **source mechanisms decomposed; mechanical review geometry implemented; no global all-in policy chosen yet**.

## 1. Important source correction: DeepCrusher did not have one single commitment threshold

A close source read shows at least **three different mechanisms** that can move an otherwise non-all-in postflop line toward all-in. They must not be discussed as if they were one rule.

### 1.1 Flop/turn/river betsize routers — approximately 60% of Hero stack

`f$BetsizeFlopHeadsup` and `f$BetsizeFlopMultiway` contain repeated rules of the form:

`requested pot-fraction size >= 0.60 * StackSize -> BetMax`.

Examples exist for 25%, 30%, 33%, 40%, 50%, 60%, 66%, 75% and 100% pot sizing families.

This is a **direct sizing conversion** inside DeepCrusher's betsize router.

### 1.2 `f$allin_on_betsize_balance_ratio` — effective-stack half threshold plus balance fallback

DeepCrusher's standard callback is more complex than a fixed `0.50` return.

When no call is faced, it checks the requested bet size against roughly **50% of `f$EffectiveStack_BKP`**. If that condition is met, it returns `.001`, which makes OpenHoldem's downstream all-in adjustment effectively trigger on any positive selected betsize. Otherwise the function can fall back to `.50`.

OpenHoldem source confirms the callback is evaluated by `ChangeBetsizeToAllin()` and compared against `currentbet + balance` (`MaximumPossibleBetsizeBecauseOfBalance`). It affects direct `f$betsize` and betpot actions.

Thus DeepCrusher combined:

- an **effective-stack-aware 50% trigger** that deliberately forces the callback threshold extremely low; and
- a **Hero total-balance 50% fallback** inside OpenHoldem's standard all-in adjustment.

This is not the same rule as the 60%-of-`StackSize` conversion in the explicit betsize routers.

### 1.3 `f$Raise_Committed` — call-to-shove promotion around 55%

Separately, `f$Raise_Committed` promotes some flop/turn calls into raises/all-ins when:

- `AmountToCall > StackSize * 0.55`; or
- in HU, the Villain bet consumes roughly 55% of the relevant Villain resource expression.

This mechanism belongs to **defense/raise ownership**, not initial CBet sizing. It must not be merged into the current CBet gate simply because the percentages are similar.

## 2. Why the distinction matters for CashCrusher

The user-level migration rule is deliberately neutral:

> short-stack origin is a reason to audit context, not a reason to keep or delete a rule automatically.

For a 100bb-start SRP, converting a 50% pot flop CBet to all-in because it crosses a historical residual-stack threshold can be absurd.

For a 100bb-start 4BP, the exact same requested pot fraction can occur at SPR near 1 or below. In that geometry an all-in conversion may be perfectly reasonable, depending on range/hand/board.

Therefore CashCrusher must know **the geometry first**, and policy second.

## 3. OpenHoldem betpot semantics verified

`BetsizeForBetpot()` computes:

- `pot_after_i_call = pot + call`;
- `additional_money_into_pot = factor * pot_after_i_call`;
- `final_betsize = current_user_bet + call + additional_money_into_pot`.

For the current flop-CBet node:

- `AmountToCall = 0` by definition;
- a clean first flop bet should also have `currentbet = 0` and `potplayer = 0` after all prior players checked;
- therefore the native 33/50/75/100 actions reduce cleanly to the requested fraction of the street-start common pot.

CashCrusher now exposes this mechanical geometry explicitly instead of trying to infer it later from a strategic hand label.

## 4. Mechanical review facts added

`src/CashCrusher_Flop_CBet_StackGeometry.txt` exposes, without choosing an action:

- requested pot fraction;
- requested bet in BB;
- requested bet / Hero available stack;
- requested bet / exact HU effective stack;
- requested bet / shallowest-live effective stack in multiway;
- residual Hero stack after the requested bet;
- residual HU effective stack after the requested bet;
- HU turn SPR **if** Villain can fully call the requested bet;
- diagnostic flags corresponding to the historical 50% effective-stack, 50% Hero-balance and 60% Hero-stack thresholds.

These are review facts only.

## 5. No global policy yet

The existence of a diagnostic flag does **not** mean CashCrusher should jam.

Examples:

- `legacy_effective_half_trigger = true` in a 4BP with SPR 1.1 may eventually support a direct shove with much of a value/bluff range;
- the same flag in a peculiar multiway sidepot geometry may not;
- `legacy_hero_60_trigger = false` does not prove a shove is wrong if Villain is much shorter and the effective stack is already committed;
- a TP or overpair does not settle the question by itself.

## 6. Next decision layer

Before defining the final callback or explicit BetMax rules, CashCrusher must classify stack-sensitive CBet policy by at least:

- pot family: SRP / ISO / 3BP / squeeze / 4BP;
- HU versus exact multiway composition;
- range provenance;
- IP/OOP;
- board parent and hand/equity class;
- raw starting-street SPR;
- requested bet / Hero stack;
- requested bet / effective stack;
- projected residual SPR after a call.

This should produce a context-aware conversion policy rather than a universal historical percentage.

## 7. Multiway caution

OpenHoldem's global all-in adjustment is based on Hero's own balance, whereas poker strategy in multiway pots also depends on multiple opponent stacks and sidepot eligibility. Therefore a single global ratio is particularly dangerous as a substitute for multiway strategic reasoning.

CashCrusher exposes the shallowest-live effective ratio only as a **coarse review descriptor**. It does not claim that the shortest opponent is the only strategically relevant stack.

## Provenance summary

| Mechanism | Source | CashCrusher treatment now |
|---|---|---|
| ~60% `StackSize` in DeepCrusher betsize routers | DeepCrusher | measured, not automatically copied/rejected |
| ~50% `EffectiveStack_BKP` callback trigger | DeepCrusher | measured, not automatically copied/rejected |
| `.50` balance-ratio fallback | DeepCrusher + OpenHoldem callback semantics | measured, later context review |
| ~55% `f$Raise_Committed` | DeepCrusher defense | deferred to defensive node audit |
| exact CashCrusher conversion-to-jam policy | not in source for 100bb six-max | future A/P per-context decision |
