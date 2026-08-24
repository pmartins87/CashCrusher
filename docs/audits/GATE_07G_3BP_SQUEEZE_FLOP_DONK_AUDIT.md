# Gate 07G — plain 3BP / squeeze Flop Donk audit

Status: **reviewed check-range baseline with repaired caller provenance**.

## Source boundary

The legacy router can send reraised/no-initiative FIRST/MIDDLE states toward the generic Donk move, but the mature DeepCrusher Flop Donk audit contains no positive 3BP/squeeze first-action strategy. Its only positive Flop Donk tree is `(BBorSB)v2pp`.

No supplied Starting Strategy gives a deep-stack first-action OOP lead table for a caller in a 3-bet or squeeze pot.

## Chronology requirement

Gate07G uses the repaired `lastraised1` evidence layer from Gate05 rather than the older assumption that Hero participated in every raise sequence.

Plain 3BP and squeeze remain separate, and Hero caller origin remains visible:

- original opener who called the 3bet;
- pre-3bet coldcaller in a squeeze;
- post-3bet coldcaller.

The actual final 3bettor must be proven and still live.

## Cash policy

Every reviewed OOP caller state checks to the final 3bettor on Hero's first flop action.

This is strategically conservative and coherent at 100bb:

- the final 3bettor owns a narrow/uncapped range and natural CBet initiative;
- squeeze pots have especially selected ranges and should not inherit plain-3BP or SRP lead frequencies;
- no solver/source evidence available in this project defines a positive Donk subset accurately enough to justify hardcoding one;
- checking preserves check-raise/check-call defense and allows later Float/Probe ownership after a missed CBet.

The baseline can later receive exact solver-backed board/matchup exceptions before the broad check parent.

## Covered

- supported plain 3BP, HU or current multiway, Hero OOP caller;
- supported squeeze, HU or current multiway, Hero OOP caller;
- exact caller-origin provenance must be consistent;
- final 3bettor must remain a live opponent.

## Not covered

- reversed/backraise/limp-reraise two-raise history;
- Hero as final 3bettor (that is CBet ownership);
- 4BP+;
- any response after the 3bettor CBets.
