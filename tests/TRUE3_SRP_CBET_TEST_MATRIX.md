# CashCrusher true-threeway ordinary-SRP CBet acceptance matrix

Status: **design/static acceptance contract; OpenHoldem runtime fixtures still required**.

## Mandatory context invariants

A strategy-covered Gate 01J.1 state must satisfy all of:

- `f$cc_threeway = true`;
- `f$cc_flop_entry_count = 3`;
- `f$cc_pot_family_id = 2`;
- `f$cc_pf_role_pfa = true`;
- `f$cc_pf_one_raise_ordinary_srp = true`;
- `f$cc_flop_cbet_opportunity = true`;
- `f$cc_mw_srp_true3_context_consistent = true`.

Any four-way-origin, ISO, 3BP, squeeze, 4BP or non-PFA state must fail this context.

## Caller-composition parents

| # | Example line | Hero | Flop opponents | Expected composition |
|---:|---|---|---|---|
| 1 | BTN open, SB call, BB call | BTN | SB+BB | 1 BOTH_BLINDS |
| 2 | CO open, BTN call, BB call | CO | BTN+BB | 2 ONE_BLIND_ONE_NONBLIND |
| 3 | HJ open, CO call, BTN call | HJ | CO+BTN | 3 TWO_NONBLINDS |
| 4 | UTG open, HJ call, BB call | UTG | HJ+BB | 2 ONE_BLIND_ONE_NONBLIND |

Acceptance:

- live blind + live nonblind counts sum to exactly 2;
- caller composition ID is exactly one of 1/2/3;
- exact `f$cc_opp_live_mask` remains unchanged and available;
- exact `f$cc_mw_srp_true3_range_key` differs when exact seats differ even if composition ID is the same.

## Relative-position families

| # | Example | Expected relative family | Source quality |
|---:|---|---|---|
| 5 | BTN open, SB+BB call | LAST | A/P donor from 3wBTNv2p |
| 6 | CO open, BTN+BB call | MIDDLE | P-heavy; 3wBBv2p only positional shell |
| 7 | HJ open, CO+BTN call | FIRST | P-heavy; no direct PFA-CBet source tree |

Note: exact OpenHoldem relative position must be authoritative. Examples above are fixture descriptions, not replacement logic.

## Strategy anti-leak tests

| # | State | Expected |
|---:|---|---|
| 8 | true3 ordinary SRP, Hero LAST | `f$cc_cbet_mw_srp_true3_last_action` owns decision |
| 9 | true3 ordinary SRP, Hero MIDDLE | middle child owns decision |
| 10 | true3 ordinary SRP, Hero FIRST | first child owns decision |
| 11 | four players entered flop, one later folds leaving three | Gate01J.1 false |
| 12 | three-way ISO | Gate01J.1 false |
| 13 | three-way 3BP | Gate01J.1 false |
| 14 | HU after preflop folds | Gate01J.1 false |
| 15 | true3 caller/non-PFA Hero | Gate01J.1 false |

## Hand-policy sanity fixtures

These are not solver-frequency proofs; they verify intended baseline direction.

| # | Relative pos | Composition | Hand/board parent | Expected baseline |
|---:|---|---|---|---|
| 16 | LAST | both blinds | very strong value | bet |
| 17 | LAST | both blinds | best-backdoor air on static high | selected bet |
| 18 | LAST | two nonblinds | weak top pair | check |
| 19 | MIDDLE | any | pure air | check |
| 20 | MIDDLE | two nonblinds | dynamic-low overpair at high SPR | check |
| 21 | FIRST | any | medium top pair | check |
| 22 | FIRST | any | very strong value | bet |
| 23 | FIRST | any | ordinary air | check |
| 24 | LAST | any | premium draw | bet |

## Sizing consistency

For every fixture:

- action=false -> `f$cc_cbet_mw_srp_true3_size_id = 0`;
- action=true -> size ID > 0;
- no size ID alone implies stack commitment;
- any later stack-sensitive conversion is tested in the node that owns it.

## Runtime gate

Before table release, fixtures must be recreated from deterministic OpenHoldem states or replay logs including:

- dealt-player bits;
- preflop fold/raise/call bits;
- flop-entry count;
- current live mask;
- Hero role/position;
- relative position;
- pot family;
- board/hand descriptors;
- raw SPR;
- resulting CBet action and size ID.
