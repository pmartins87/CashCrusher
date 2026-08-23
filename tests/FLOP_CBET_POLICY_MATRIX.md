# CashCrusher flop CBet policy acceptance matrix v1

Purpose: deterministic acceptance contract for the first ordinary-SRP CBet baselines. These are **policy-level** expectations, not parser tests.

The exact runtime fixture must eventually supply real OpenHoldem card/chair/history states that produce the descriptors listed here.

Legend:

- `THU` = true HU deal, origin 1
- `RHU` = 3-6h deal reduced to HU preflop, origin 2
- Size `S/M/L` = strategic ID 1/2/3 = ~33/~50/~75
- `A/P` in rationale identifies source adaptation versus professional fill

## A. HU-origin isolation

| # | Context | Expected |
|---:|---|---|
| A1 | THU SB/Button open -> BB call | true-HU SRP IP child |
| A2 | 6h SB open -> BB call after four folds | reduced-HU SRP OOP child, never HUSB |
| A3 | 6h BTN open -> BB call | reduced-HU SRP IP-vBB child |
| A4 | 3-way flop later becomes HU | no ordinary HU flop/turn descendant by origin alone |
| A5 | THU SB limp -> BB raise -> SB call | HU-limp-raised child, currently uncovered |

## B. True-HU SB/Button PFA IP versus BB

| # | Board parent / hand descriptor | SPR | Expected | Size | Rationale |
|---:|---|---:|---|---|---|
| B1 | static high, two-pair+ | any | BET | S | robust value, small parent |
| B2 | dynamic low/mid, two-pair+ | any | BET | L | polar value |
| B3 | static high, strong TP | any | BET | S | HUSB A + deep sizing |
| B4 | dynamic low/mid, medium TP | 8 | CHECK | — | P high-SPR check protection |
| B5 | static high, weak TP | 12 | BET | S | wide true-HU value parent |
| B6 | static high, second pair | 5 | BET | S | selective HUSB pair adaptation |
| B7 | dynamic low/mid, second pair | any | CHECK | — | deep realization/pot control |
| B8 | dynamic low/mid, premium draw | any | BET | L | strong semi-bluff |
| B9 | dynamic low/mid, ordinary FD/OESD with no OC | any | CHECK | — | preserve IP realization/mix |
| B10 | straight-possible flop, no-frontdoor air | any | CHECK | — | source-explicit HUSB A rule |
| B11 | static A/K/Q-high, quality backdoor air | any | BET | S | P deterministic bluff selector |
| B12 | dynamic low/mid, pure air | any | CHECK | — | reject blanket source tail |

## C. Reduced-HU PFA IP versus BB

| # | Matchup | Board/hand | SPR | Expected | Size |
|---:|---|---|---:|---|---|
| C1 | BTN-v-BB | static high, strong TP | any | BET | S |
| C2 | BTN-v-BB | dynamic low, two-pair+ | any | BET | L |
| C3 | BTN-v-BB | static high, weak TP | 12 | CHECK | — |
| C4 | BTN-v-BB | static high, second pair | 5 | BET | S |
| C5 | UTG-v-BB | same second-pair case | 5 | CHECK | — |
| C6 | CO/BTN-v-BB | static low, second pair | 4 | BET | S |
| C7 | HJ/UTG-v-BB | static low, second pair | 4 | CHECK | — |
| C8 | any opener-v-BB | dynamic low, premium draw | any | BET | L |
| C9 | BTN-v-BB | static low, quality air + two OCs | any | BET | S |
| C10 | UTG-v-BB | same air combo | any | CHECK | — |
| C11 | BTN-v-BB | dynamic high, combo-backdoor air | any | BET | M |
| C12 | any | dynamic low, pure air | any | CHECK | — |

## D. Reduced-HU PFA IP versus SB

| # | Board/hand | Expected | Size | Difference from vBB |
|---:|---|---|---|---|
| D1 | static high, strong TP | BET | S | value retained |
| D2 | dynamic high, strong TP | BET | M | value retained |
| D3 | static high, second pair no draw | CHECK | — | stronger SB continue range |
| D4 | static high, pair+draw | BET | S | value/equity |
| D5 | dynamic low, premium draw | BET | L | robust semi-bluff |
| D6 | static low, ordinary FD with overcard | BET | M | selected draw |
| D7 | static low, pure air | CHECK | — | no vBB bluff extension |
| D8 | static high, quality backdoor air | BET | S | narrow air family |
| D9 | paired board, only ordinary quality air | CHECK unless best-backdoors | — | more selective than vBB |

## E. Reduced-HU SB PFA OOP versus BB

| # | Board/hand | SPR | Expected | Size | Source/theory |
|---:|---|---:|---|---|---|
| E1 | static high, strong TP | any | BET | S | 3wSBvBB A |
| E2 | dynamic low/mid, strong TP | any | CHECK | — | A X/R architecture |
| E3 | dynamic low/mid, two-pair+ | any | BET | L | P deep-stack strong value |
| E4 | dynamic high, overpair | any | BET | M | value/protection |
| E5 | any, second pair | any | CHECK | — | source MP/BP main plan |
| E6 | any, frontdoor draw no made | any | CHECK | — | source X/R/X/C ownership |
| E7 | straight-possible, air | any | CHECK | — | source A |
| E8 | static high, quality air | any | BET | S | P restricted source tail |
| E9 | dynamic low, quality air | any | CHECK | — | caller interaction |

## F. PFA OOP versus later-position cold caller

| # | Board/hand | SPR | Expected | Size | Rationale |
|---:|---|---:|---|---|---|
| F1 | static A/K/Q-high, strong TP | any | BET | S | P range advantage/value |
| F2 | dynamic low, strong TP | 8 | CHECK | — | OOP check protection |
| F3 | dynamic low, two-pair+ | any | BET | L | robust value |
| F4 | static high, medium TP | any | BET | S | selective thin value |
| F5 | any, weak TP | any | CHECK | — | protect check range |
| F6 | any, second/lower pair | any | CHECK | — | SDV/pot control |
| F7 | static/dynamic high, premium draw | any | BET | S/M according to parent |
| F8 | dynamic low, premium draw | any | CHECK | — | preserve X/R family |
| F9 | static high, quality air | any | BET | S | narrow P bluff family |
| F10 | low/mid board, air | any | CHECK | — | no source range parent |

## G. Sizing invariants

1. A CHECK must produce CBet size ID `0`.
2. A BET in covered ordinary-SRP families must produce size ID `1`, `2` or `3`.
3. Current ordinary-SRP policy never emits pot-size ID `4`.
4. Current CBet policy contains no `BetMax` and no inherited `StackOffDraws` shortcut.
5. Global betsize-to-all-in conversion remains disabled.

## H. Coverage invariants

`f$cc_flop_cbet_strategy_covered` is true for:

- THU ordinary SRP SB/Button PFA IP vs BB;
- RHU ordinary SRP PFA IP vs BB;
- RHU ordinary SRP PFA IP vs SB;
- RHU SB PFA OOP vs BB;
- RHU opener PFA OOP vs later-position cold caller.

It remains false for:

- true-HU limp-raised pot;
- ISO;
- 3BP;
- squeeze;
- 4BP;
- all multiway CBet families.

A covered strategy returning `false` means a deliberate CHECK, not missing coverage.
