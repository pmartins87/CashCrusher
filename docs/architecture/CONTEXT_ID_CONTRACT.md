# CashCrusher context ID contract

This document freezes the mechanical IDs introduced by Gate 00. They are infrastructure, not strategy frequencies.

Changing an ID after strategy code starts depending on it requires a versioned migration.

## Dealt-player / handedness ID

`f$cc_deal_size` is the number of players actually dealt into the hand and is valid from **2 through 6**.

The CashCrusher is a six-max cash bot, not a bot that requires six occupied seats. Players may leave, sit out, or wait. Therefore 2h/3h/4h/5h deals on a six-max table are supported states.

Canonical six-max-equivalent positions by deal size:

- 6h: `UTG HJ CO BTN SB BB`
- 5h: `HJ CO BTN SB BB`
- 4h: `CO BTN SB BB`
- 3h: `BTN SB BB`
- 2h: `SB/Button BB`

Deal size remains a separate context dimension even when two different handednesses share a canonical matchup ID.

## Physical table occupancy versus deal mode

- `f$cc_physical_table_hu`: exactly two players are currently seated at the table.
- `f$cc_true_hu`: exactly two players were dealt into the hand.
- `f$cc_true_hu_full_table`: both are true.
- `f$cc_true_hu_with_waiters`: exactly two were dealt but more than two seats are still reported seated/waiting.

Poker strategy follows the **deal mode**; physical occupancy remains audit metadata.

## HU origin

`f$cc_hu` means only that two players are currently playing. It is insufficient for strategic routing.

- `1` — `TRUE_HU_DEAL`: exactly two players were dealt. SB is also Button and acts IP postflop. Primary legacy ancestry: `HUSB/HUBB`.
- `2` — `PREFLOP_REDUCED_TO_HU`: 3-6 players were dealt, but preflop folds left exactly two players reaching the flop. Six-max-equivalent absolute ranges remain relevant.
- `3` — `POSTFLOP_REDUCED_TO_HU`: 3+ players reached the flop and later a postflop fold reduced the hand to HU. Later-street strategy must retain its multiway origin.
- `0` — not currently HU / invalid.

This distinction is mandatory. A true HU `SB/Button vs BB` and a six-handed `SB vs BB` after four folds can both have numeric matchup ID `56`, while their position, ranges and legacy ancestry are different.

## Players reaching the flop

`f$cc_flop_entry_bits = playersdealtbits - (playersdealtbits BitAnd foldbits1)`

`f$cc_flop_entry_count = BitCount(f$cc_flop_entry_bits)`

The flop-entry count is preserved on later streets so a multiway flop cannot silently become an ordinary HU strategy after a fold.

## Absolute positions

- `1` UTG
- `2` HJ (`mp3chair` in the 6h/5h OpenHoldem mapping)
- `3` CO
- `4` BTN
- `5` SB
- `6` BB
- `0` unknown / invalid

In true HU, the dealer/SB is canonicalized as **SB=5**, not double-counted as BTN=4.

## HU matchup ID

`hero_position_id * 10 + villain_position_id`

Examples:

- `16` = Hero UTG versus BB
- `23` = Hero HJ versus CO
- `46` = Hero BTN versus BB
- `56` = Hero SB versus BB
- `65` = Hero BB versus SB

Direction matters. `46` and `64` are not the same strategic context.

**HU origin must accompany the matchup ID.** `56/origin=1` is true HU HUSB-like geometry; `56/origin=2` is a 3-6h SB-v-BB survivor spot.

## Live opponent position mask

- UTG = `1`
- HJ = `2`
- CO = `4`
- BTN = `8`
- SB = `16`
- BB = `32`

Masks are additive bitsets. Example BTN+BB = `40`.

In true HU, dealer=SB is represented only by SB bit `16`; BTN bit `8` is disabled at 2h to prevent double counting.

## Pot family

- `1` unraised / limped
- `2` one raise
- `3` two raises / 3BP
- `4` three raises / 4BP
- `5` four-or-more raises / 5BP+
- `0` unknown

Subtypes:

- `f$cc_pf_iso_proven`: a non-HU limper existed before the sole raise.
- `f$cc_pf_hu_limp_raise_proven`: true HU SB/Button limped and BB raised. This is **not** ISO.
- `f$cc_pf_squeeze_proven`: a caller existed between opener and final 3bettor in a supported non-HU chronology.
- `f$cc_pf_3bet_plain_proven`: supported two-raise chronology without a squeeze caller.

## Hero preflop role

- `1` final aggressor in one-raise pot / PFA
- `2` one-raise caller
- `3` final aggressor in two-raise pot / 3bettor
- `4` original raiser who called final 3bet
- `5` cold caller in two-raise pot
- `6` final aggressor in three-raise pot / 4bettor
- `7` generic caller of final 4bet
- `8` unraised caller / limper
- `9` BB checked unraised pot
- `0` unknown

## Relative position

- `1` First
- `2` Middle
- `3` Last
- `0` unknown

Current-live HU permits only `1` or `3`.

## Multiway exact mechanical ID — v2

Gate 00F expanded the old key so shorter tables and later-street reductions cannot collide.

Current formula:

`deal_size*100,000,000 + flop_entry_count*10,000,000 + current_players*1,000,000 + pot_family*100,000 + hero_role*10,000 + hero_position*1,000 + opponent_mask*10 + relative_position`

It preserves:

1. players dealt at hand start;
2. players reaching the flop;
3. players currently playing;
4. pot family;
5. Hero role;
6. Hero canonical absolute position;
7. exact current live-opponent mask;
8. relative postflop position.

The ID is for logging, fixtures and exact-match audits. It must **not** be interpreted as a solved strategic policy key.

## SPR bucket

- `1` <1
- `2` 1-<2
- `3` 2-<4
- `4` 4-<6
- `5` 6-<10
- `6` 10-<15
- `7` 15+
- `0` invalid/unknown

SPR buckets are P-provenance engineering bins. Raw SPR remains the canonical numerical input.
