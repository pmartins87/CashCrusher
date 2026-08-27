# CashCrusher Turn CBet acceptance matrix — current Gate02 coverage

Status: **static/design acceptance matrix; OpenHoldem replay fixtures still required**.

The matrix assumes Gate01N has already proven a normal executed flop CBet: one `didbetsizeround2`, no flop check/call/re-raise/all-in, and Hero is `lastraised2`.

## History routing invariants

| Case | Flop history | Expected turn owner |
|---:|---|---|
| H1 | Hero CBet, Villain call | Standard Turn CBet |
| H2 | Hero had CBet opportunity, checks, Villain checks | Delayed CBet, **not** Turn CBet |
| H3 | Hero checks, Villain bets, Hero calls | defense continuation, **not** Turn CBet |
| H4 | Hero checks, Villain bets, Hero raises | raised-flop continuation, **not** Turn CBet |
| H5 | Hero CBet, Villain raises, Hero calls | Villain-aggressor continuation, **not** normal Turn CBet |
| H6 | Hero CBet, Villain raises, Hero re-raises | raised-flop continuation, **not** normal Turn CBet |
| H7 | flop CBet executed direct all-in | no ordinary Turn CBet |
| H8 | multiway flop CBet, one caller folds before turn / only one remains | postflop-reduced-HU family, never flop-HU source family |

## True HU HUSB — SB/Button PFA IP vs BB

| Case | Flop provenance / turn state | Expected action | Size ID |
|---:|---|---|---:|
| HU1 | current 2P+ | bet | 75 |
| HU2 | current TP/OP, super-completed turn, no premium redraw | check | 0 |
| HU3 | current TP/OP, normal turn | bet | 75 |
| HU4 | flop TP demoted by turn overcard | bet | 50 |
| HU5 | current second pair, non-completed | bet | 50 |
| HU6 | current second pair, completed | bet | 25 |
| HU7 | current third-or-worse pair | bet | 25 |
| HU8 | source-qualified no-made good draw | bet | 75 |
| HU9 | weaker no-made frontdoor draw | check | 0 |
| HU10 | flop air + exact two-low pressure turn | bet | 75 |
| HU11 | flop air + paired/newly-completed/non-pressure turn | check | 0 |

Important: HU3/HU4/HU8 do not authorize calling a turn raise or playing for stacks. That is a separate defensive decision.

## Reduced HU BTN vs BB

| Case | Turn state | Expected | Size |
|---:|---|---|---:|
| BB1 | current 2P+ | bet | 75 |
| BB2 | TP first made on turn | bet | 75 |
| BB3 | carried overpair + glued overcard | bet | 75 |
| BB4 | carried overpair + other mOC | bet | 50 |
| BB5 | carried overpair + residual turn | bet | 75 |
| BB6 | carried TP kicker <T, no flop BDSD | check | 0 |
| BB7 | carried TP kicker <T + flop BDSD | bet | 50 |
| BB8 | carried TP kicker T+ | bet | 75 |
| BB9 | no-made flop plan without explicit preserved multi-street plan | fail closed/check | 0 |

BB9 is deliberate: current CashCrusher does not infer the historical `Flop33_Turn75`, `Flop50_Turn50`, etc. plan merely from flop sizing.

## Reduced HU BTN vs SB

| Case | Turn state | Expected | Size |
|---:|---|---|---:|
| SB1 | current 2P+ | bet | 75 |
| SB2 | current overpair | bet | 75 |
| SB3 | current TP kicker <J | bet | 50 |
| SB4 | current TP kicker J+ | bet | 75 |
| SB5 | flop draw CBet remains no-made | check | 0 |
| SB6 | flop air CBet remains no-made | check | 0 |
| SB7 | flop draw/air improved to TP+ | current made-hand branch wins | 50/75 by class |

## True HU BB PFA OOP after SB limp-call

| Case | Turn state | Expected | Size |
|---:|---|---|---:|
| LR1 | current TP/OP/2P+, completed | bet | 75 |
| LR2 | current TP/OP/2P+, non-completed | bet | 33 |
| LR3 | current no-made frontdoor draw | bet | 50 |
| LR4 | lower pair without old exact flop-min provenance | fail closed/check | 0 |
| LR5 | source low-SPR `<1.6` historical shove geometry | **not automatically jammed** | normal source size pending exact jam audit |

LR5 does not ban the source shove. It prevents a low-SPR Spin conversion from being imported before the exact cash response/commitment node owns it.

## Reduced HU SB PFA OOP vs BB

| Case | Turn state | Expected | Size |
|---:|---|---|---:|
| O1 | TP+ and turn newly makes straight possible | bet | 100 |
| O2 | TP+ other turn | check to preserve source X/R architecture | 0 |
| O3 | no-made draw after raised-pot flop CBet | check | 0 |
| O4 | air after flop CBet | check | 0 |

The pot-sized O1 bet is a pot bet, not `BetMax` and not automatic stack commitment.

## Explicit uncovered/fail-closed families

The current router must return false / size 0 for:

- UTG/HJ/CO PFA IP versus blinds until P-heavy range adaptation is written;
- UTG/HJ/CO PFA OOP versus later nonblind cold caller;
- ordinary SRP that began flop multiway and became HU only after flop action;
- current multiway ordinary SRP;
- ISO Turn CBet;
- plain 3BP Turn CBet;
- squeeze Turn CBet;
- 4BP Turn CBet;
- any history mismatch from Gate01N.

No uncovered family may inherit HUSB, BTN-v-BB, BTN-v-SB or SB-v-BB as a generic tail.
