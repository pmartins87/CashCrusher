# CashCrusher context ID contract

This document freezes the mechanical IDs introduced by Gate 00. They are infrastructure, not strategy frequencies.

Changing an ID after strategy code starts depending on it requires a versioned migration.

## Absolute positions

- `1` UTG
- `2` HJ (`mp3chair` in six-handed OpenHoldem mapping)
- `3` CO
- `4` BTN
- `5` SB
- `6` BB
- `0` unknown / invalid

## HU matchup ID

`hero_position_id * 10 + villain_position_id`

Examples:

- `16` = Hero UTG versus BB
- `23` = Hero HJ versus CO
- `46` = Hero BTN versus BB
- `64` = Hero BB versus BTN

Direction matters. `46` and `64` are not the same strategic context.

## Live opponent position mask

- UTG = `1`
- HJ = `2`
- CO = `4`
- BTN = `8`
- SB = `16`
- BB = `32`

Masks are additive bitsets. Example BTN+BB = `40`.

## Pot family

- `1` unraised / limped
- `2` one raise (ordinary SRP or ISO subtype)
- `3` two raises / 3BP (ordinary or squeeze subtype)
- `4` three raises / 4BP
- `5` four-or-more raises / 5BP+
- `0` unknown

ISO and squeeze are flags/subtypes, not new base family numbers.

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

HU permits only `1` or `3`.

## Multiway exact mechanical ID

Current formula:

`players*1,000,000 + pot_family*100,000 + hero_role*10,000 + hero_position*1,000 + opponent_mask*10 + relative_position`

The ID is useful for logging, fixtures and exact-match audits. It must **not** be interpreted as a solved strategic policy key.

## SPR bucket

- `1` <1
- `2` 1–<2
- `3` 2–<4
- `4` 4–<6
- `5` 6–<10
- `6` 10–<15
- `7` 15+
- `0` invalid/unknown

SPR buckets are P-provenance engineering bins. Raw SPR remains the canonical numerical input.
