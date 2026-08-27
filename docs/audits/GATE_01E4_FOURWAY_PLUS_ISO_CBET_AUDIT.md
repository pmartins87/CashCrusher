# Gate 01E.4 — Four-way+ ISO flop CBet audit

Status: **first P-heavy baseline implemented for exact 4/5/6-player ISO flops**.

## Source boundary

No DeepCrusher/Starting Strategy node directly solves a 100bb isolator CBetting into three, four or five surviving opponents. Existing HU ISO and three-way material supplies only A-level architecture.

Exact four-way+ ISO policy is P.

## Exact scope

- current flop player count equals flop-entry count;
- 4, 5 or 6 players entered flop;
- Hero made the sole raise after at least one proven limper;
- Hero is final preflop aggressor;
- no flop bet before Hero acts;
- all live opponents are explainable by pre-raise-limper or post-raise-coldcaller masks.

## Range composition

Three broad parents are retained while exact masks/counts remain canonical:

1. **ALL_LIMPERS** — no post-raise cold caller survives;
2. **MIXED** — at least one limper and at least one post-raise cold caller survive;
3. **ALL_COLD_CALLERS** — original limpers folded; all surviving opponents cold-called after the raise.

The last family is treated as the most selected/condensed broad parent. This is P theory, not an exact population range claim.

## Professional-theory baseline

As opponents increase, fold equity collapses and the isolation raise itself produces a more selected field after it is called multiple times. Therefore:

- no pure-air baseline is used four-way+;
- robust value remains active;
- overpairs and strong TP can value/protection bet static boards, especially against limper-heavy fields;
- medium/weak one-pair checks sharply more;
- premium draws are selective and mostly favored when LAST / fewer opponents / limper-heavy;
- dynamic low/mid boards receive the strongest checking bias;
- exact player count 4/5/6 tightens independently rather than using one generic multiway rule.

## Stack depth

No commitment mechanism is globally disabled. This gate owns only first flop CBet/check and size. Any later stack-off is audited at its actual SPR/action node.
