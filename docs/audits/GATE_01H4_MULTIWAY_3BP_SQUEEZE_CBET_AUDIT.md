# Gate 01H.4 — Multiway 3BP / squeeze flop CBet audit

Status: **first exact-composition baseline implemented for 3-way and 4-way+ flop origins**.

## Source boundary

DeepCrusher has no clean dedicated deep-stack 3BP CBet tree, and therefore no literal deep-stack **multiway** 3BP/squeeze CBet tree either. The source contributes A-level architecture only:

- initiative and relative position matter;
- static high/paired boards permit more pressure than low connected boards;
- checking ranges require protection;
- draw quality matters;
- pot geometry changes sizing.

Exact multiway 3BP/squeeze frequencies are P.

## Range provenance retained

The implementation uses the exact masks already reconstructed in `CashCrusher_3BP_Context.txt` and counts live opponents from three origins:

1. **original opener** who later called the 3bet/squeeze;
2. **pre-3bet cold caller** who called the open before the squeeze;
3. **post-3bet cold caller** who called after the final 3bet/squeeze.

A strategy does not collapse these into “two 3bet callers”. Exact masks and counts remain available.

## Plain 3BP versus squeeze

These remain separate.

A squeeze has dead money and a different final 3bettor construction, while its continuing ranges have survived more selection. The multiway squeeze baseline is therefore at least as selective as plain 3BP on marginal hands and air.

## Professional-theory fill

- 3BP pots start with lower SPR and tighter ranges than SRP, but multiway continuation remains much stronger than HU continuation;
- static A/K/Q-high and paired boards can preserve substantial 3bettor range advantage and support small value-heavy pressure;
- low/mid dynamic boards check much more;
- overpairs and strong TP remain legitimate value bets on suitable boards; they are not automatically stack-off hands;
- medium/weak one-pair hands tighten substantially;
- premium draws can bet selectively, especially LAST and in exact three-way pots;
- pure-air bluffing is close to absent, with only a narrow best-backdoor static-high exception in the least selected exact-threeway plain-3BP composition;
- four-way+ 3BP/squeeze is extremely value/equity dense.

## Stack depth

This gate does not ban or force any commitment helper. It owns only the first flop CBet/check and size family. Later raises/jams are reviewed at the actual actor-specific SPR.

## Still separate

- 4BP;
- post-CBet raise defense;
- turn/river continuation;
- unsupported/reversed preflop chronology.
