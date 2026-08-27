# Gate 01J.2 — Four-way+ ordinary-SRP flop CBet audit

Status: **first explicit P-heavy baseline implemented for 4-way, 5-way and 6-way flop origins**.

## 1. Source boundary

DeepCrusher is a three-player Spin framework. Its postflop CBet source does not provide literal four-way, five-way or six-way PFA-CBet trees.

Therefore:

- no four-way+ action frequency is T;
- legacy three-way principles can be A-level constraints only;
- exact four-way+ policy is a professional-theory fill P.

The source still gives useful warnings: multiway ranges interact more strongly, weak equity betting should be reduced, relative position matters, and hand/texture quality should drive aggression.

## 2. Exact scope

Gate 01J.2 requires:

- flop entry count = current player count;
- 4, 5 or 6 players on the flop;
- ordinary one-raise SRP;
- Hero is PFA/final preflop aggressor;
- no flop bet before Hero acts.

A four-way flop later reduced to three players is not Gate 01J.1 on later streets; flop-origin provenance remains separate.

## 3. Axes preserved

The implementation keeps:

- exact player count: 4 / 5 / 6;
- Hero relative position: FIRST / MIDDLE / LAST;
- exact Hero canonical seat;
- exact live-opponent mask;
- count of blind defenders and nonblind cold callers;
- raw SPR;
- board/hand descriptors.

The policy does not pretend that “multiway” is a single range.

## 4. Professional-theory fill

As player count rises:

- fold equity decreases;
- probability that at least one opponent connects rises;
- bluffing frequency should fall sharply;
- marginal one-pair value betting becomes more selective;
- robust value and nut-potential equity become more important;
- checking is especially valuable from FIRST/MIDDLE because multiple players remain behind;
- LAST can value bet somewhat more freely after all previous opponents check;
- static boards can still support small value/range pressure with strong PFA hands;
- dynamic low/mid boards receive the strongest checking bias;
- no pure-air baseline is introduced in four-way+ pots.

This does **not** mean one-pair hands never bet multiway. Strong TP and overpairs can still value/protection bet on suitable static textures. The rule is tighter selection, not a categorical ban.

## 5. Stack depth

As elsewhere, stack-sensitive DeepCrusher helpers are reviewed locally. Gate 01J.2 does not disable them and does not pre-authorize them. It owns the first flop CBet/check and size family only.

## 6. Sizing baseline

- static high/low/paired strong value: mostly ~33%;
- dynamic high robust value/equity: ~50%;
- dynamic low/mid very strong value/premium equity: ~50-75%;
- no generic all-in or pot-sized tail.

## 7. Still outside scope

- multiway ISO;
- multiway 3BP/squeeze;
- 4BP;
- post-CBet raise defense;
- turn/river continuation.
