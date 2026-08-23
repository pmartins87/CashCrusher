# Gate 02E — Ordinary-SRP Turn CBet while the turn remains multiway

Status: **source audit complete; exact BTN-v-SB+BB true3 donor is A/P, every other range family is P-heavy**.

## 1. Source boundary

DeepCrusher has one materially useful initiative Turn-CBet branch for a player still facing two live opponents:

`3wBTNv2p`.

The source itself labels this a **genuine Starting Strategy gap** and says the mature CrusherTBP generic Turn-CBet evidence is being preserved only for that exact v2p route. Its rules continue:

- `mOC-or-better` / gutshot-or-better draw;
- TP+;
- selected second-pair/pocket-pair with top-four-ish kicker (`NumberOfBetterKickers <= 3`) on non-completed turns;
- pocket pair with one board overcard on non-completed turns;
- FD and SD;
- selected gutshot/two-overcard pressure on an overcard non-completed turn.

This is useful source evidence, but it is already a human-reviewed gap fill rather than a dedicated Starting Strategy tree. Therefore CashCrusher classifies the exact BTN-v-SB+BB still-threeway descendant as **A/P**, not T.

No equivalent initiative Turn-CBet tree was found for `3wSBv2p` or `3wBBv2p`. Those labels supply positional ancestry only. Six-max four-, five- and six-way turns have no literal source state.

## 2. A separate conservative DeepCrusher multiway fallback

The mature DeepCrusher corpus also contains a conservative multiway fallback in a later audited decision family:

- nut class continues;
- real trips continues unless super-completed;
- exact two pair continues only on non-completed turn and low SPR;
- all other multiway states decline.

This is **not transplanted as the Turn-CBet tree**, because it belongs to a different downstream ownership context. It is nevertheless corroborating evidence that mature DeepCrusher became deliberately value-heavy when it lacked an exact multiway source branch.

## 3. Why current 3-way is not enough

CashCrusher must distinguish at least:

1. three players entered flop and all three remain on turn;
2. four or more entered flop and only three remain on turn;
3. four or more still remain on turn.

The second category has already experienced one or more folds after Hero's multiway flop CBet. Those surviving ranges are more selected than a true-threeway origin. A simple `nplayersplaying = 3` router would erase that information.

## 4. Current relative position still matters

FIRST / MIDDLE / LAST remain separate strategic structures:

- **LAST:** all live opponents have checked, so Hero can realize the largest betting set;
- **MIDDLE:** at least one player remains behind, constraining thin value and semibluffs;
- **FIRST:** every live opponent remains to act, requiring the strongest/check-protected baseline.

The legacy `3wBTNv2p` donor is specifically a LAST shape. It must not be copied into FIRST/MIDDLE.

## 5. Six-max professional fill

The P-heavy baseline follows these constraints:

- robust value remains the core betting region;
- two-pair is not treated as invulnerable on four-card / newly completed turns at deep effective SPR;
- OP / TP are increasingly checked as current field size, nonblind composition and prior flop size make continuing ranges stronger;
- premium draws remain useful semibluffs, primarily LAST and selectively MIDDLE;
- FIRST uses materially fewer one-pair and draw barrels;
- weak draws and pure air are absent from four-way+ baseline;
- the only meaningful air/pressure continuation inherited near the source donor is restricted to exact true3 LAST configurations and favorable high-pressure turns.

These are professional-theory rules, not solver frequencies.

## 6. Correct stack geometry

All multiway depth relaxations use **deepest-effective SPR**. A short third player cannot make an otherwise deep decision against another live opponent inherit short-stack aggression.

`SPR deepest < X` means every live effective relation is below X. The reverse is not true for the shallowest relation.

No TP/OP condition in this Gate authorizes playing for stacks. If Hero is raised after the second barrel, the response belongs to the later raise/call defensive node with actor-specific geometry.

## 7. Current context classes

`src/CashCrusher_Turn_Multiway_SRP_Context.txt` separates:

- exact true3 still3;
- exact BTN PFA + SB+BB source-adjacent shape;
- other true3 shapes;
- flop4plus -> current3;
- current4plus;
- FIRST/MIDDLE/LAST;
- current blind/nonblind composition;
- flop-size selection pressure;
- deepest-effective SPR bounds.

It also preserves exact Hero position, current opponent mask, flop entrant count and current player count in an audit key.

## 8. Fail-closed rule

The ordinary multiway Turn-CBet family fails closed when:

- flop-entry/current-live masks are inconsistent;
- actual standard flop CBet history is absent;
- dual-bound stack geometry is invalid;
- pot is ISO/3BP/squeeze/4BP;
- a strategic subfamily has not been explicitly implemented.

No HU Turn-CBet child is a fallback for a live multiway state.
