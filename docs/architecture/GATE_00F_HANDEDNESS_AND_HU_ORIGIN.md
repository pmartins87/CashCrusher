# Gate 00F — Handedness and HU-origin preservation

Status: **IMPLEMENTED IN ROUTING FOUNDATION; parser/runtime validation pending**.

## Why this gate exists

A six-max cash table is a *maximum-seat format*, not a promise that six players are present every hand.

Players leave, sit out, or wait. Therefore the same CashCrusher session can produce 6h, 5h, 4h, 3h and genuine 2h deals.

At the same time, a hand that starts 6h can become heads-up simply because four players fold. Those two meanings of "HU" are strategically different and must remain different in code.

## Three distinct meanings that must not be collapsed

### 1. Physical table HU

Exactly two players are reported seated.

Symbol: `f$cc_physical_table_hu`.

This is useful operational metadata, but it is not by itself the decisive poker-strategy state because a third player can remain visibly seated while sitting out.

### 2. True HU deal

Exactly two players are dealt into the hand.

Symbol: `f$cc_true_hu`.

This changes the poker geometry itself:

- dealer is also small blind;
- SB/Button acts first preflop and last postflop;
- BB acts last preflop and first postflop;
- preflop ranges are genuine heads-up ranges.

This is the CashCrusher descendant of the old DeepCrusher **HUSB/HUBB** families.

### 3. Current-live HU after folds

`nplayersplaying=2` can also occur in a hand that began 3-6 handed.

That is not enough to select a HU strategy. CashCrusher asks how the hand reached two players.

## HU origin IDs

### Origin 1 — TRUE_HU_DEAL

`nplayersdealt=2`.

Primary strategic ancestry:

- Hero SB/Button -> `HUSB` geometry;
- Hero BB -> `HUBB` geometry.

Deep-stack cash sizing and SPR still require adaptation, but the positional/range parent is fundamentally true HU.

### Origin 2 — PREFLOP_REDUCED_TO_HU

Three to six players were dealt, and preflop folds left exactly two players reaching the flop.

Examples:

- 6h BTN opens, BB calls, everyone else folds;
- 6h SB opens, BB calls after four folds;
- 5h HJ opens, BB calls;
- 3h BTN opens, SB folds, BB calls.

Absolute position and original handedness remain meaningful. A 6h SB-v-BB hand is **not** HUSB: SB is OOP postflop and the best legacy positional parent is `3wSBvBB`.

### Origin 3 — POSTFLOP_REDUCED_TO_HU

Three or more players reached the flop, but a postflop fold later leaves two players.

Example:

`CO raises -> BTN calls -> BB calls -> flop three-way -> BB folds flop -> turn CO vs BTN heads-up`.

The turn is currently HU, but range evolution came from a three-way flop. Ordinary HU turn strategy is therefore not allowed to replace the multiway-origin tree.

## Flop-entry reconstruction

OpenPPL/OpenHoldem preserves:

- `playersdealtbits`: players dealt into the hand;
- `foldbits1`: players that folded preflop.

CashCrusher reconstructs:

`flop_entry_bits = playersdealtbits - (playersdealtbits BitAnd foldbits1)`

and then:

`flop_entry_count = BitCount(flop_entry_bits)`.

This gives a persistent cross-street provenance signal without having to infer later from current player count.

## Canonical six-max-equivalent positions on shorter tables

CashCrusher keeps stable position IDs while also retaining `deal_size`.

| Deal size | Canonical positions |
|---:|---|
| 6h | UTG HJ CO BTN SB BB |
| 5h | HJ CO BTN SB BB |
| 4h | CO BTN SB BB |
| 3h | BTN SB BB |
| 2h | SB/Button BB |

This is a routing abstraction, not a claim that 5h HJ and 6h HJ have identical ranges. `deal_size` remains available to every future policy.

## Why numeric matchup ID is insufficient

Both of these can produce matchup ID `56`:

1. true HU: Hero SB/Button vs BB;
2. six-handed hand: Hero SB vs BB after UTG/HJ/CO/BTN fold.

But their geometry is opposite:

- true HU SB is **IP**;
- normal-table SB is **OOP**.

Their ranges are also different.

Therefore every HU strategy must consume **HU origin** alongside matchup ID.

## True-HU limp raise is not ISO

In true HU:

`SB/Button limps -> BB raises -> SB calls`

there is no third player to isolate. CashCrusher classifies this as `f$cc_pf_hu_limp_raise_proven`, not `f$cc_pf_iso_proven`.

This matters because the postflop ranges differ from both an ordinary HU open-raised pot and a multi-seat isolation pot.

## Multiway IDs also preserve origin

Gate 00F versioned the exact multiway mechanical key so it now includes:

- dealt-player count;
- flop-entry count;
- current player count;
- pot family;
- Hero role;
- Hero position;
- current opponent mask;
- relative position.

A three-way turn that came from a four-way flop therefore cannot collide with a hand that was three-way from the flop.

## Fail-closed rules

CashCrusher rejects or withholds strategy when:

- deal size is outside 2-6;
- dealt-bit count contradicts `nplayersdealt`;
- physical seated count is smaller than dealt count;
- required canonical chairs for the current handedness are missing;
- true HU does not have dealer=SB;
- current HU cannot be assigned origin 1/2/3;
- preflop fold bits point outside dealt players;
- current player count exceeds flop-entry count;
- a later-street origin-3 state tries to use an ordinary HU parent.

## Provenance

- Distinguishing true HU from fold-reduced HU: **T/A**, strongly supported by DeepCrusher's separate HUSB/HUBB and 3w positional families.
- Dynamic 2-6h cash-table support and cross-street flop-entry provenance: **A/P architecture**.
- No betting frequency is introduced by this gate.

## Files affected

- `src/CashCrusher_Context.txt`
- `src/CashCrusher_Range_Topology.txt`
- `src/CashCrusher_Flop_CBet.txt`
- `src/CashCrusher_Multiway_Context.txt`
- `docs/architecture/CONTEXT_ID_CONTRACT.md`
- `tests/CONTEXT_TEST_MATRIX.md`
