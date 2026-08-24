# Gate 06A — River Float history/source ownership audit

Status: **ownership frozen; no River-Float betting policy implemented in this gate**.

## 1. Critical ownership correction

The River Float parent is **not** an executed Turn Float.

DeepCrusher routes `f$move_river_floatbet` when Villain owns the relevant turn aggression, Hero has continued by calling, and Villain then declines to bet the river while Hero is in position. In practical terms the canonical clean parent is:

`Villain bets/raises turn -> Hero call only -> Villain checks river -> Hero exact LAST/IP, AmountToCall=0`.

By contrast:

`Hero Turn Float bet -> Villain call -> river`

leaves **Hero** as the final turn aggressor. That continuation belongs to a River-CBet/continuation-of-Hero-aggression family, not River Float.

Gate05H accidentally created the misleading alias `f$cc_hist_river_float_standard_parent_valid` for an executed normal Turn Float. Gate06A does not delete its underlying history facts, but formally **deprecates that name as a River-Float owner**. New Gate06 code explicitly excludes it and exposes correctly named aliases for future continuation routing.

## 2. What the supplied sources actually contain

### Crusher Framework 5

`f$move_river_floatbet` is empty. The framework supplies the router/ownership shell, not River-Float hand policy.

### CrusherTBP

`f$hand_river_floatbet` contains two broad rules:

1. top non-board pair with top-four kicker, or overpair-or-better -> bet;
2. `3wBBvSB && BotCalledOnFlop && BotCalledOnTurn && Air -> River33`.

The first is a useful manually reviewed value guideline but is not a complete six-max River-Float tree. The second is too broad to be treated as exact source provenance because `BotCalledOnFlop && BotCalledOnTurn` does not identify *why* the turn call occurred.

### Audited DeepCrusher refinement

DeepCrusher later narrows the `3wBBvSB` air bluff to a much more specific source history:

- Hero BB called SB's flop bet with the high-air/backdoor family;
- on the turn that backdoor improved to a real draw;
- Hero called the second barrel at the source-supported price;
- the draw busts / Hero remains no-made on the river;
- SB checks river;
- Hero uses the small source bluff, 25% pot.

Current made value is reclassified before the bluff. DeepCrusher also preserves clear negative bluff boundaries for `3wBTNvSB` no-made and HUSB missed-draw material.

## 3. Why the exact `3wBBvSB` bluff is not executable yet in CashCrusher

The decisive source fact is **turn-call provenance**: the flop high-air/backdoor hand must have improved to a real turn draw and Hero must then have actually called the turn bet.

CashCrusher has not yet audited/composed the defensive Turn-Call node that would write that pre-call snapshot. Closed river symbols can prove that Hero called on turn, but they cannot safely recover the prior-street semantic fact "this was the source high-air/backdoor family that became a draw on turn" after the river card arrives.

Therefore Gate06A creates a source-geometry candidate and a dedicated blocker/marker contract, but the exact source bluff remains fail-closed until the defensive history writer exists. We do **not** replace the missing provenance with `BotCalledOnFlop && BotCalledOnTurn`.

## 4. Canonical clean parent reconstructed now

Gate06A accepts only a clean turn-call history:

- river has begun, so round-3 history is closed;
- Hero made exactly one turn call;
- Hero did not check, bet, raise or go all-in on turn;
- exactly one opponent chair appears in `raisbits3`;
- `lastraised3` identifies that same opponent aggressor;
- that aggressor is still live on river;
- Hero is on the first river action, `AmountToCall=0`, exact LAST;
- if HU, Hero must be IP and the turn aggressor must be the current `headsupchair`.

Raised/reraised multi-aggressor turn histories deliberately fail closed in Gate06A. They require their own later parent rather than being flattened into the clean-call family.

## 5. Handedness/origin boundary

A clean HU flop-entry history can be identified safely (`flop_entry_count=2`). Current multiway river state can also be identified safely.

If the flop began multiway and the river is now HU, closed river counters alone do not always prove whether the turn call itself occurred HU or multiway. Gate06A therefore marks that origin as unresolved instead of silently treating it as a clean HU River Float. A future turn-call snapshot may resolve it.

## 6. Explicit non-owners

The following are not canonical River Float:

- standard executed Turn Float with Hero final aggressor;
- standard Turn CBet with Hero final aggressor;
- checked-back Turn Float / checked-through turn;
- delayed/probe/no-action lines with no turn call;
- Hero turn bet -> Villain raise -> Hero call (different raised-bet history);
- multi-aggressor turn action without a dedicated audited parent.

## 7. Provenance classification

| Class | Gate06A use |
|---|---|
| **T** | `did*round3`, `raisbits3`, `lastraised3`, current live chairs, position and first-river-action facts |
| **A** | DeepCrusher router meaning and exact `3wBBvSB` called-2Bar source history |
| **P** | six-max clean-parent decomposition, exact-LAST safety and unresolved-origin fail-closed contract |
| **X** | executed Turn Float as River-Float parent; generic `BotCalledOnFlop && BotCalledOnTurn && Air` as sufficient proof; neighboring HU fallback for unresolved multiway origin |

## 8. Next subgate

Gate06B may implement **only source/high-ancestry River-Float strategy whose history is actually provable**. The exact `3wBBvSB` busted-draw 25% bluff remains blocked until its turn-call provenance writer is available. Source-silent value and six-max professional fills come later, after this boundary stays green in CI.
