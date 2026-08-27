# Gate 01H — HU squeeze-pot flop CBet audit

Status: **HU survivor families audited for first CashCrusher baseline; multiway squeeze remains separate**.

## 1. Source limitation

DeepCrusher has useful initiative/IP-OOP/board/hand architecture but no clean deep-stack squeeze-pot CBet tree. Therefore no squeeze CBet frequency is labelled T merely because the source has a generic CBet branch.

Useful source constraints remain **A**:

- IP and OOP require separate trees;
- static high/paired boards can support broader/smaller pressure;
- lower/connected boards require more checking/selectivity;
- marginal showdown-value hands protect check ranges;
- draw quality matters;
- OOP can preserve strong draws in check-raise lines;
- sizing can grow with polarity/dynamism.

Exact squeeze range/frequency work is **P-heavy**.

## 2. Survivor range must remain explicit

A squeeze can reach a HU flop against three strategically different survivor types already reconstructed by `CashCrusher_3BP_Context.txt`:

1. **original opener** — opened first, later called the squeeze;
2. **pre-3bet cold caller** — called the open, then continued versus the squeeze;
3. **post-3bet cold caller** — acted after the squeeze and cold-called it.

CashCrusher must not merge these just because all are "3BP callers" on the flop.

## 3. Professional-theory fill

### Versus original opener

The opener-call range is selected by having faced both the original flat/dead money and a squeeze. Compared with an ordinary 3BP opener-call, it is typically stronger and the pot starts larger. CashCrusher therefore keeps broad small pressure on favorable high/static boards but reduces marginal low-board aggression.

### Versus pre-3bet cold caller

This range first cold-called an open and then continued against a squeeze. It is often condensed around pairs/suited broadways/strong suited hands with some traps. That makes low/mid connected boards especially dangerous for indiscriminate CBetting. High-card range-advantage boards remain better for the squeezer.

### Versus post-3bet cold caller

This is a selected cold-call of the squeeze itself and can be very strong/condensed. Baseline air frequency is therefore the most conservative of the three HU squeeze families. Strong value remains aggressive; marginal one-pair and medium-strength draws check more.

## 4. Cash-depth caution — corrected rule

DeepCrusher short-stack commitment mechanics are **not globally disabled**. They are simply not assumed to transfer automatically.

This Gate decides only the flop CBet/check and a size family. It does not settle later stack-off versus a raise. If a squeeze pot reaches very low SPR, later sizing/defense audit may legitimately choose an all-in or reuse/adapt a commitment helper.

## 5. Implemented scope

Implemented in `CashCrusher_Flop_CBet_Squeeze.txt`:

- squeeze vs original opener, IP/OOP;
- squeeze vs pre-3bet cold caller, IP/OOP;
- squeeze vs post-3bet cold caller, IP/OOP.

Still separate/fail-closed:

- multiway squeeze CBet;
- reversed/unsupported preflop chronology;
- 4BP;
- response after flop CBet is raised.

## 6. Sizing baseline

Current size IDs remain engineering intentions:

- `1` ~33% pot;
- `2` ~50%;
- `3` ~75%;
- `4` pot reserved.

Static high/paired boards generally use smaller pressure. Dynamic low/mid robust value/premium equity may move to 50/75. These are P/A baseline choices, not solver-exact frequencies.
