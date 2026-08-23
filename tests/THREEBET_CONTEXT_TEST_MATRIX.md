# CashCrusher 3-bet-pot context acceptance matrix

Status: **design/static acceptance contract; OpenHoldem runtime fixtures still required**.

Purpose: verify that a two-raise pot is not collapsed into one generic 3BP range. The key test is **who survived to the flop** relative to the original opener and final 3bettor.

## Expected survivor IDs

- `1` = original opener who called the 3bet;
- `2` = pre-3bet cold caller who continued after a squeeze;
- `3` = post-3bet cold caller;
- `0` = unknown / unsupported chronology.

## HU plain 3BP — opener survivor

| # | Preflop line | Hero | Expected subtype | Villain type | Rel | Strategy coverage |
|---:|---|---|---|---:|---|---|
| 1 | HJ raise → BTN 3bet → HJ call | BTN | plain | 1 opener | IP | covered |
| 2 | CO raise → SB 3bet → CO call | SB | plain | 1 opener | OOP | covered |
| 3 | BTN raise → BB 3bet → BTN call | BB | plain | 1 opener | OOP | covered |
| 4 | SB raise → BB 3bet → SB call in a 3–6h deal | BB | plain | 1 opener | IP | covered |

Acceptance:

- `f$cc_pf_3bet_plain_proven = true`;
- `f$cc_hu_3bp_villain_is_opener = true`;
- `f$cc_hu_3bp_survivor_type_id = 1`;
- exactly one survivor-type flag is true;
- `f$cc_hu_3bp_survivor_consistent = true`.

## True HU 3BP topology

| # | Preflop line | Hero | Expected | Strategy coverage |
|---:|---|---|---|---|
| 5 | SB/Button raise → BB 3bet → SB/Button call | BB | true HU, 3bettor OOP, opener survivor | covered |
| 6 | attempt to construct ordinary true-HU plain 3bettor IP | SB/Button | topology invalid/unsupported | fail closed |
| 7 | SB/Button limp → BB raise → SB/Button reraise → BB call | either | reversed/limp-reraise chronology, not plain 3BP | fail closed |

Mandatory invariant for case 5:

- `f$cc_true_hu_plain3bp_bb_3bettor_oop = true`;
- `f$cc_true_hu_plain3bp_3bettor_ip_invalid = false`.

Case 6 must never become a normal strategy merely because a generic `3bettor && IP` predicate can be formed.

## Post-3bet cold caller survives

| # | Preflop line | Hero | Original opener | Survivor | Expected subtype | Coverage |
|---:|---|---|---|---|---|---|
| 8 | UTG raise → BTN 3bet → BB coldcall → UTG fold | BTN | UTG | BB | plain 3BP | **not covered** |
| 9 | HJ raise → CO 3bet → BTN coldcall → HJ fold | CO | HJ | BTN | plain 3BP | **not covered** |

Acceptance:

- `f$cc_pf_3bet_plain_proven = true`;
- `f$cc_hu_3bp_villain_is_post3bet_coldcaller = true`;
- `f$cc_hu_3bp_villain_is_opener = false`;
- `f$cc_hu_3bp_survivor_type_id = 3`;
- generic plain-opener CBet child must return false / size 0.

This is a mandatory anti-leak test.

## Squeeze — original opener survives

| # | Preflop line | Hero | Survivor | Expected | Coverage |
|---:|---|---|---|---|---|
| 10 | UTG raise → HJ call → BTN squeeze → HJ fold → UTG call | BTN | UTG opener | squeeze + type 1 | not yet covered |
| 11 | HJ raise → CO call → SB squeeze → CO fold → HJ call | SB | HJ opener | squeeze + type 1 | not yet covered |

Acceptance:

- `f$cc_pf_squeeze_proven = true`;
- `f$cc_hu_3bp_villain_is_opener = true`;
- survivor ID `1`;
- ordinary plain-3BP child must not fire.

## Squeeze — pre-3bet cold caller survives

| # | Preflop line | Hero | Survivor | Expected | Coverage |
|---:|---|---|---|---|---|
| 12 | UTG raise → HJ call → BTN squeeze → UTG fold → HJ call | BTN | HJ | squeeze + type 2 | not yet covered |
| 13 | HJ raise → BTN call → BB squeeze → HJ fold → BTN call | BB | BTN | squeeze + type 2 | not yet covered |

Acceptance:

- `f$cc_pf_squeeze_proven = true`;
- survivor's canonical bit is inside `f$cc_pf_pre3bet_coldcaller_mask`;
- `f$cc_hu_3bp_villain_is_pre3bet_coldcaller = true`;
- survivor ID `2`;
- opener-call 3BP strategy must not fire.

## Squeeze — post-3bet cold caller survives

| # | Preflop line | Hero | Survivor | Expected | Coverage |
|---:|---|---|---|---|---|
| 14 | UTG raise → HJ call → BTN squeeze → BB coldcall → UTG/HJ fold | BTN | BB | squeeze + type 3 | not yet covered |

Acceptance:

- squeeze proven;
- survivor ID `3`;
- no opener/pre-3bet-caller policy leakage.

## Multiway 3BP composition

| # | Line reaching flop | Expected live provenance |
|---:|---|---|
| 15 | UTG raise → BTN 3bet → UTG call → BB coldcall; flop 3-way | opener mask + post-3bet-coldcaller mask |
| 16 | UTG raise → HJ call → BTN squeeze → UTG call → HJ call | opener mask + pre-3bet-coldcaller mask |
| 17 | UTG raise → HJ call → BTN squeeze → UTG/HJ/BB call | opener + pre3bet caller + post3bet caller masks |

All remain strategically fail-closed while multiway 3BP policy is unimplemented.

## Invalid / ambiguous histories

| # | Fault/history | Expected |
|---:|---|---|
| 18 | UTG limp → BTN raise → UTG reraise → BTN call | reversed raiser order; subtype unknown |
| 19 | two raises reported but original/final raiser cannot be reconstructed | survivor unknown; fail closed |
| 20 | same current Villain matches >1 survivor type due contradictory scrape/history | `f$cc_hu_3bp_survivor_consistent = false` |

## Runtime gate

Static success does not prove OpenHoldem behavior. Before release, every acceptance case above needs either:

1. deterministic OpenHoldem replay/table-state fixture with the required persisted preflop bits; or
2. a dedicated test formula/log probe printing raise count, raiser IDs, call masks, survivor flags, HU origin, action and size.
