# Gate 00C — Dynamic six-max OpenPPL context engine

Status: **IMPLEMENTED AS MECHANICAL FOUNDATION; parser/runtime validation still pending**.

Gate 00F subsequently strengthened this gate by adding explicit handedness and HU-origin provenance. The current implementation in `src/CashCrusher_Context.txt` is the authoritative version.

## Objective

CashCrusher must know *what game state it is in* before any imported DeepCrusher rule can fire. A strategically good CBet executed in the wrong pot family, wrong handedness, or wrong HU origin is still a bad decision.

The canonical decision context remains:

`Players × PotType × PreflopRole × PostflopPosition × Matchup/Ranges × SPR × Board × History`

Gate 00C implements mechanical axes that can be reconstructed safely from OpenHoldem/OpenPPL. It deliberately does **not** implement poker policy.

## Source-derived mechanical facts

The implementation is grounded in OpenHoldem/OpenPPL behavior rather than invented state assumptions:

- `playersplayingbits`, `opponentsplayingbits`, `nplayersplaying` and `nopponentsplaying` identify players who still hold cards post-flop;
- `playersdealtbits` and `nplayersdealt` preserve the hand-start deal size;
- `foldbits1` preserves preflop folds and therefore lets CashCrusher reconstruct who actually reached the flop;
- position chairs are available through `utgchair`, `mp3chair`, `cutoffchair`, `dealerchair`, `smallblindchair`, `bigblindchair`;
- OpenPPL `Position` gives `First`, `Middle`, `Last` relative to players still in the hand;
- `raisbits1` and `callbits1` retain stable historical preflop action bitmasks after the preflop round;
- `NumberOfRaisesBeforeFlop` is a persisted OpenPPL raise **count** and is preferable to trying to repurpose a current-round bet counter;
- `BotsLastPreflopAction` is persisted by the OpenPPL history layer and distinguishes Hero's final preflop Raise / RaiseMax / Call / Check;
- in true heads-up play the dealer is also the small blind, so a 2h chair map must deliberately allow `dealerchair == smallblindchair`.

The old Crusher classification (`HUSB`, `HUBB`, `3wBTNvBB`, etc.) used positional shells plus separate initiative/history routers. CashCrusher keeps that useful separation but expands it to dynamic six-max cash contexts.

## Six-max cash does not mean six players must be present

The first Gate 00C draft incorrectly required `nplayersdealt = 6`. That assumption was removed.

A six-max cash table naturally changes handedness as players leave, sit out, or wait. CashCrusher therefore supports deals with **2 through 6 players**.

Canonical six-max-equivalent positions are:

| Dealt | Canonical positions |
|---:|---|
| 6 | UTG, HJ, CO, BTN, SB, BB |
| 5 | HJ, CO, BTN, SB, BB |
| 4 | CO, BTN, SB, BB |
| 3 | BTN, SB, BB |
| 2 | SB/Button, BB |

The canonical position ID does not erase handedness. `f$cc_deal_size` remains a separate context dimension because, for example, a BTN-v-BB range in 3h can differ materially from BTN-v-BB in 6h even though both use matchup ID `46`.

## Physical occupancy versus players dealt

CashCrusher separates:

- physical/seated table count;
- number actually dealt into the hand.

A hand can be strategically true HU (`nplayersdealt=2`) even if a third seat is still shown as seated/waiting. Conversely, a six-handed deal can become current-live HU only because four players folded. These cases must never share policy merely because `nplayersplaying=2`.

The detailed HU-origin contract is in `GATE_00F_HANDEDNESS_AND_HU_ORIGIN.md`.

## Stable absolute-position IDs

| ID | Position |
|---:|---|
| 1 | UTG |
| 2 | HJ / MP3 |
| 3 | CO |
| 4 | BTN |
| 5 | SB |
| 6 | BB |

At 2h the dealer/SB is canonicalized as **SB=5**, not BTN=4. This prevents the same physical chair from being counted twice and preserves the key strategic fact that the HU small blind is also the Button and therefore IP postflop.

## Live opponent mask

| Bit value | Position |
|---:|---|
| 1 | UTG |
| 2 | HJ |
| 4 | CO |
| 8 | BTN |
| 16 | SB |
| 32 | BB |

The mask retains exact multiway composition without building a separate function for every possible trio/quartet. Position aliases absent at a shorter handedness are disabled.

## Relative postflop position

| ID | Meaning |
|---:|---|
| 1 | First |
| 2 | Middle |
| 3 | Last |

Current-live HU permits only First or Last. `Middle` in a two-player current state is contradictory context.

## Pot families

The family is classified from `NumberOfRaisesBeforeFlop`:

| ID | Raises | Family |
|---:|---:|---|
| 1 | 0 | Unraised / limped |
| 2 | 1 | One-raise pot |
| 3 | 2 | 3-bet pot |
| 4 | 3 | 4-bet pot |
| 5 | 4+ | 5-bet+ / currently unsupported strategically |

ISO, true-HU limp-raised and squeeze are **subtypes**, not new fundamental pot-family numbers.

## Hero preflop role

The role combines raise count, Hero's historical raise bit and `BotsLastPreflopAction`.

| ID | Role |
|---:|---|
| 1 | final aggressor in one-raise pot / PFA |
| 2 | caller in one-raise pot |
| 3 | final aggressor in two-raise pot / 3bettor |
| 4 | original raiser who called the 3bet |
| 5 | cold caller to a 3bet / squeeze family |
| 6 | final aggressor in three-raise pot / 4bettor |
| 7 | generic 4bet caller |
| 8 | unraised caller / limper |
| 9 | BB checked an unraised pot |

This is intentionally more precise than a single initiative flag. Initiative remains useful on later streets, but the preflop role determines the range that entered the flop.

## Proven ISO versus true-HU limp-raise

For a non-HU one-raise pot, a call bit at a position that acted **before** the sole raiser proves a voluntary limper existed before the raise. That is sufficient for `f$cc_pf_iso_proven`.

Examples:

- UTG limps, HJ raises -> ISO proven;
- CO limps, BTN raises -> ISO proven;
- BTN raises, BB calls -> ordinary SRP;
- UTG raises, BTN calls -> ordinary SRP.

True HU is different:

`SB/Button limp -> BB raise -> SB call`

has no third player to isolate. CashCrusher therefore marks `f$cc_pf_hu_limp_raise_proven` and explicitly keeps `f$cc_pf_iso_proven=false`.

## Conservative squeeze detection

Aggregate action bitmasks do not preserve every chronological detail. CashCrusher refuses to manufacture certainty.

A squeeze is marked **proven** only when:

1. exactly two raises occurred;
2. Hero was one of exactly two unique raisers;
3. Hero's final action tells whether Hero was opener or final 3bettor;
4. reconstructed first raiser acts earlier than final 3bettor in supported first-orbit order;
5. at least one call bit exists strictly between them;
6. the hand is not a true-HU deal.

A reversed-order history compatible with limp-reraise remains subtype-unknown rather than being rewritten as an ordinary 3BP.

## Mechanical validity versus strategic coverage

`f$cc_context_valid` answers only:

> Is this state mechanically coherent enough to route?

It does **not** mean a strategy has been written for that state.

Current validity checks include supported 2-6h deal size, dealt-bit consistency, conditional chair-map integrity, Hero still playing, flop-entry reconstruction, current player count, live-mask consistency, blind/pot sanity, relative position, HU origin, preflop history and Hero-role consistency.

Future attack/defense nodes require separate coverage. A mechanically valid 4BP can remain strategically uncovered and fail closed.

## Provenance

- Mechanical reconstruction from OpenHoldem/OpenPPL: **T/A** from runtime capabilities.
- Dynamic 2-6h six-max-equivalent decomposition: **A** architecture.
- HU-origin preservation and fail-closed unresolved chronology: **P** engineering safety.
- No professional poker frequencies are introduced in Gate 00C.

## File

`src/CashCrusher_Context.txt`
