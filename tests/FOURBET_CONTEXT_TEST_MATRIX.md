# CashCrusher 4-bet-pot acceptance matrix

Status: **static/design contract; OpenHoldem runtime fixtures still required**.

Purpose: prove that `raise_count = 3` does not automatically become one generic 4BP range. Clean first-orbit opener4/cold4 families are separated from reversed/backraise/other-caller histories.

## Clean subtype IDs

- `1` = standard opener 4bet;
- `2` = standard cold 4bet;
- `0` = unresolved/reversed/backraise/other chronology.

## HU survivor IDs

- `1` = original opener;
- `2` = original 3bettor;
- `3` = non-raiser caller whose exact call stage is not proven;
- `0` = invalid/unknown.

## Standard opener 4bet

| # | Line | Hero | Expected subtype | Sole Villain | Coverage |
|---:|---|---|---:|---|---|
| 1 | HJ open → BTN 3bet → HJ 4bet → BTN call | HJ | 1 | 3bettor | covered OOP |
| 2 | CO open → SB 3bet → CO 4bet → SB call | CO | 1 | 3bettor | covered IP |
| 3 | BTN open → BB 3bet → BTN 4bet → BB call | BTN | 1 | 3bettor | covered IP |
| 4 | SB open → BB 3bet → SB 4bet → BB call in 3–6h deal | SB | 1 | 3bettor | covered OOP |

Acceptance:

- `f$cc_pf_4bet_standard_opener4_proven = true`;
- Hero has no preflop call bit;
- `hero_pos < threebettor_pos`;
- survivor ID = `2`;
- action/size route belongs to opener4-v-3bettor family.

## True HU standard 4BP

| # | Line | Hero | Expected |
|---:|---|---|---|
| 5 | SB/Button open → BB 3bet → SB/Button 4bet → BB call | SB/Button | clean subtype 1, Hero IP, survivor 2, covered |
| 6 | attempt to treat BB as ordinary final 4bettor after standard HU open/3bet | BB | impossible under clean standard chronology |

Case 5 must satisfy `f$cc_true_hu_4bp_opener4_ip_vs_threebettor`.

## Standard cold 4bet

| # | Line | Hero | Expected subtype | Sole Villain | Coverage |
|---:|---|---|---:|---|---|
| 7 | UTG open → CO 3bet → BTN cold4 → UTG call, CO fold | BTN | 2 | opener | covered IP |
| 8 | UTG open → BTN 3bet → SB cold4 → BTN call, UTG fold | SB | 2 | 3bettor | covered OOP |
| 9 | HJ open → BTN 3bet → BB cold4 → HJ call, BTN fold | BB | 2 | opener | covered OOP |
| 10 | CO open → BTN 3bet → SB cold4 → BTN call, CO fold | SB | 2 | 3bettor | covered OOP |

Acceptance:

- exactly 3 unique raisers;
- Hero has no call bit;
- opener < 3bettor < Hero in canonical order;
- survivor type exactly matches opener or 3bettor;
- opener and 3bettor policies do not leak into each other.

## Non-raiser survivor — fail closed

| # | Line | Expected |
|---:|---|---|
| 11 | UTG open → BTN 3bet → SB cold4 → BB coldcall → UTG/BTN fold | subtype may be clean cold4, survivor type 3, **strategy not covered** |
| 12 | UTG open → HJ call → BTN 3bet → UTG 4bet → HJ continues, BTN folds | non-raiser survivor; exact call stage/multiple-call history unresolved, **not covered** |

A type-3 survivor must never inherit opener-call or 3bettor-call strategy.

## Reversed / limp-reraise / backraise — fail closed

| # | Line | Expected |
|---:|---|---|
| 13 | true HU SB limp → BB raise → SB 3bet → BB 4bet → SB call | subtype 0; ordinary true-HU opener4 policy must not fire |
| 14 | UTG limp → BTN raise → UTG 3bet → BTN 4bet → UTG call | subtype 0; reversed/limp-reraise chronology |
| 15 | UTG open → CO call → BTN 3bet → CO backraise 4bet | Hero call bit true; subtype 0 |
| 16 | three raises but raiser ordering cannot be reconstructed cleanly | subtype 0 |

## Multiway clean 4BP metadata

| # | Flop composition | Expected |
|---:|---|---|
| 17 | opener4 + 3bettor caller + another caller | multiway metadata records 3bettor and `othercaller_count=1`; strategy pending |
| 18 | cold4 + opener + 3bettor both call | opener and 3bettor live masks both set; strategy pending |
| 19 | cold4 + opener + nonraiser caller | opener mask + othercaller count; strategy pending |

No multiway 4BP action policy is certified by Gate 01I.1.

## Stack-depth acceptance

The following are conceptual invariants, not exact-action fixtures:

- starting 100bb does **not** imply 4BP flop SPR is high;
- a low-SPR 4BP may legitimately support aggressive one-pair/draw lines;
- no `TP+` branch in this first-flop CBet file by itself certifies a later stack-off;
- commitment helpers are reviewed at the later exact response/stack-sensitive node, not globally banned and not globally trusted.

## Runtime gate

Before release, build deterministic OpenHoldem fixtures/log probes for at least cases 1, 3, 5, 7, 8, 11, 13 and 15, printing:

- raise count and unique raiser count;
- raiser/call masks;
- Hero role and Hero call/raise bits;
- clean 4BP subtype;
- opener/3bettor position IDs;
- HU survivor ID;
- HU origin;
- CBet action and size ID.
