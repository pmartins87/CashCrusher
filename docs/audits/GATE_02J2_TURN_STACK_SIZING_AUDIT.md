# Gate 02J.2 — Turn-CBet stack-sensitive sizing / strategic-jam boundary

Status: **local execution rule frozen: natural/mechanical all-in equivalence only. Historical near-all-in thresholds remain diagnostics, not generic strategy.**

## 1. What the inherited source actually does

The mature DeepCrusher sizing layer contains two different ideas that must not be conflated.

First, its Turn sizing router can convert an already-selected `Turn33/50/66/75/...` plan to `BetMax` when the requested amount is roughly 60% of Hero's remaining stack. The older Framework also contains global postflop all-in conversions around 55–60% stack/effective-stack relationships. Those are **sizing/commitment infrastructure**, not proof that every hand class selecting that size was strategically intended to shove in six-max cash.

Second, some exact strategy histories explicitly set `user_TurnMax` / `user_TurnShove`. Those are genuine strategic all-in plans, but they belong to exact histories, not to a universal threshold.

CashCrusher therefore keeps the two concepts separate.

## 2. HUSB explicit shove plan does not belong to the current standard Turn-CBet parent

The legacy HUSB Turn-CBet source contains an explicit `user_plan_shove_on_noncpl_turn -> user_TurnMax` line. That plan originates from a flop **check-raise / raised-flop continuation history**.

CashCrusher's canonical standard Turn-CBet parent requires:

- exactly one initial sized flop CBet by Hero;
- no flop check;
- no flop call after the CBet;
- no flop re-raise/re-aggression;
- Hero remains final flop aggressor.

Therefore that source shove plan is not silently recoverable by the standard Turn-CBet node. It belongs to a later raised-flop/defensive continuation family.

This is a history-ownership exclusion, not a judgment that the source shove was bad.

## 3. 3wBB-v-SB contains a real source shove, but not a universal cash rule

The mature source also has a direct `3wBBvSB` TP+ Turn shove on wet/completed turns, with a non-all-in 75% resolution on four-card straight/flush turns. That is genuine source evidence.

However:

- the scenario is a narrow positional/preflop-history family;
- the original environment is short-stack Spin geometry;
- the same source explicitly uses SPR-sensitive planning elsewhere;
- CashCrusher's six-max ISO/limp-raised families can start 100bb and can arrive at very different Turn SPRs.

Accordingly, the source evidence is retained as an **exact-node review flag**, not generalized into `TP+ -> BetMax` or `wet turn -> BetMax` across SRP/ISO/3BP.

Where the cash hand has naturally collapsed to very low SPR, the reviewed CashCrusher strategic size can already become all-in through mechanical equivalence. A future exact range/board/SPR audit may restore a strategic shove before that mechanical boundary if the evidence supports it.

## 4. Current CashCrusher local rule

The local Turn execution layer may return `BetMax` only if the reviewed requested size already reaches:

1. Hero's full remaining street-start stack; or
2. the exact sole-Villain HU effective stack; or
3. in multiway, the **deepest/all-live** effective relationship.

The third rule is critical. Reaching only a short sidepot opponent does not justify shoving into a deeper live player.

## 5. Historical thresholds are retained as diagnostics

`CashCrusher_Turn_CBet_StackGeometry.txt` exposes:

- requested bet / Hero stack >= 50%;
- requested bet / Hero stack >= 60%;
- requested bet / HU effective stack >= 50%;
- requested bet / deepest MW effective stack >= 50%.

They deliberately do not cause an action. They exist so later exact-node audits can ask: **would the old Crusher have promoted this size, and is that promotion strategically justified in this specific cash state?**

## 6. Why this does not make CashCrusher artificially passive

The current strategic files already incorporate actual SPR. This matters most in 4BP/squeeze/3BP, where a 100bb hand can naturally reach Turn at SPR <1–2.

Those nodes may choose 50% or 75% with OP/strong TP/strong draws at low SPR. If the requested bet reaches the available/effective stack, the execution layer converts it to the equivalent all-in. Thus genuine low-SPR aggression survives without importing the old global short-stack promotion rule.

## 7. What remains outside this Gate

This Gate does **not** certify:

- the final whole-bot `f$allin_on_betsize_balance_ratio` value;
- the final `f$BestBetsize` composition order;
- response to a Turn raise after Hero barrels;
- explicit strategic shove restoration for raised-flop histories;
- multiway sidepot response against a specific later bettor/raiser.

Those require their own actor/history-specific gates.

## 8. Frozen decision

For the current standard Turn-CBet family:

**reviewed strategic size + natural/mechanical all-in equivalence = implemented behavior.**

No generic 50/55/60% near-all-in promotion is authorized. Any future strategic `BetMax` must name the exact pot family, range origin, hand/board/runout state and SPR rationale that owns it.
