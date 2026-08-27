# Gate 07A — Flop Donk source / ownership audit

Status: **source boundary frozen; direct three-handed `(BBorSB)v2pp` branch is suitable for a literal/high-ancestry implementation, broader six-max Donk remains future P work**.

## 1. What the Starting Strategy actually says

The dedicated document `CRUSHFEST (BBorSB)v2pp` describes two common preflop origins:

1. BTN limps, SB calls, BB checks;
2. BTN raises, SB calls, BB calls.

The strategic player state is therefore a blind facing **both** the BTN and the other blind in a three-way flop.

The source philosophy is explicitly not a generic OOP-lead system. It says multiway opponents are relatively honest and that Hero should not bet flop/turn without equity merely to force folds.

## 2. Direct flop value rule

With **top pair or better** the source wants a Donk to deny BTN free overcards/backdoors, with one explicit exception:

- **Axx -> check**, because BTN C-bets/bluffs these structures frequently and there is no overcard to deny.

Sizing on non-Axx:

- draw-heavy / completed structure: pot if SPR is around 1:1, otherwise 75%;
- non-draw-heavy with two-or-more broadway cards: 75%;
- one broadway card: 50%;
- no broadway cards: 75%.

The mature DeepCrusher implementation expresses the low-SPR pot-size condition as `EffectiveStack_BKP / PotSize <= 1.25`. Because `EffectiveStack_BKP` uses the biggest active opponent, the CashCrusher multiway translation must use the **deepest effective** relationship, not the shortest sidepot player.

The source's later “plan to jam Turn around 1:1” is **not part of the Flop Donk action**. Gate07 can preserve the pot-sized flop bet without granting future Turn stackoff authority.

## 3. MP/BP rule

The Starting Strategy is explicit:

- pair rank **7 or lower** on a **non-completed** board -> Donk 50%;
- higher pair buckets check;
- low pair on a completed board also checks.

This is a direct source instruction. The older CrusherTBP completed-board inversion is rejected here because it contradicts the dedicated Starting Strategy.

## 4. Draw rule

For good/medium draws:

- A-high, completed (CPL), or 2+ broadway -> prefer check/call;
- one broadway, 9-high-or-lower, or paired -> Donk 75%.

Overlap priority is the check family first. A paired 2BW board therefore does not become a Donk just because it is paired.

Weak gutshot without overcard is not promoted into the positive Donk family. The source gives separate raise/call instructions after a Donk, but those belong to the future defensive response nodes and are not imported into the initial Donk decision.

## 5. Air / backdoor rule

A/K-high, backdoor-only and pure air material in the source describes **defense versus a CBet and delayed bluffing**, not a positive flop Donk. The direct source Donk tree therefore checks those classes.

## 6. Router boundary found in DeepCrusher

DeepCrusher's framework can route several OOP/no-initiative pot histories into `f$move_flop_donkbet`, including single-raised, limped and got-raised/isolated histories.

However, the mature move function itself explicitly states that the supplied Starting Strategy gives a positive flop-donk tree only for `(BBorSB)v2pp`; broad router membership is not evidence that all those pot/range families share the same strategy.

CashCrusher therefore separates **move-node source evidence** from **router ancestry**. A future ISO/3BP/4BP Donk needs its own P/source audit instead of inheriting this branch.

## 7. Direct source domain chosen for Gate07B

The literal/high-ancestry branch is restricted to the actual three-handed dealt game and the two preflop shapes explicitly described in the Starting Strategy:

- 3-handed BTN limp -> SB call -> BB check;
- 3-handed BTN raise -> SB call -> BB call.

Hero is SB or BB, both other players remain live, and Hero is FIRST/MIDDLE with no current bet to call on Hero's first flop action.

The exact same BTN+both-blinds geometry in a 4-6 handed deal is strategically similar but has different preflop ranges. It is recorded as **A/P ancestry**, not silently labeled direct source. That expansion belongs to Gate07C.

## 8. Short-stack migration decision

No short-stack mechanism is deleted simply because CashCrusher is 100bb.

For this exact node:

- the source **pot-sized flop bet at deepest SPR <=1.25** is retained because the source itself defines it by postflop SPR geometry and the mature implementation already used the biggest active opponent;
- the later Turn jam plan is not inherited by the flop node;
- response versus a raise is not inherited by the flop node;
- TP+/OP is a flop betting class here, not a generic commitment class.

## 9. Fail-closed boundary

The direct Gate07B source branch does not own:

- HU Donk;
- four-plus-player flop Donk;
- 4-6 handed BTN+both-blinds adaptation;
- ISO/3BP/squeeze/4BP/5bet+ Donk;
- other non-initiative OOP router states;
- response after Hero's Donk is raised.

Those are separate future gates.
