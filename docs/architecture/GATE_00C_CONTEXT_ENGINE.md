# Gate 00C — Six-max OpenPPL context engine

Status: **IMPLEMENTED AS MECHANICAL FOUNDATION; parser/runtime validation still pending**.

## Objective

CashCrusher must know *what game state it is in* before any imported DeepCrusher rule can fire. A strategically good CBet executed in the wrong pot family or against the wrong positional range is still a bad decision.

The canonical decision context remains:

`Players × PotType × PreflopRole × PostflopPosition × Matchup/Ranges × SPR × Board × History`

Gate 00C implements the mechanical axes that can be reconstructed safely from OpenHoldem/OpenPPL. It deliberately does **not** implement poker policy.

## Source-derived mechanical facts

The implementation is grounded in OpenHoldem/OpenPPL behavior rather than invented state assumptions:

- `playersplayingbits`, `opponentsplayingbits`, `nplayersplaying` and `nopponentsplaying` identify players who still hold cards post-flop.
- six-max position chairs are available through `utgchair`, `mp3chair`, `cutoffchair`, `dealerchair`, `smallblindchair`, `bigblindchair`;
- OpenPPL `Position` gives `First`, `Middle`, `Last` relative to players still in the hand;
- `raisbits1` and `callbits1` retain stable historical preflop action bitmasks after the preflop round;
- `NumberOfRaisesBeforeFlop` is a persisted OpenPPL raise **count** and is therefore preferable to trying to use `nbetsround_preflop` as a raise counter;
- `BotsLastPreflopAction` is persisted by the OpenPPL history layer and distinguishes Hero's final preflop Raise / RaiseMax / Call / Check.

The old Crusher classification (`HUSB`, `HUBB`, `3wBTNvBB`, etc.) used positional shells plus separate initiative/history routers. CashCrusher keeps that useful separation but expands it to all six positions instead of assigning a new strategy directly from a legacy label.

## Strict v0.1 six-max envelope

Gate 00C intentionally starts with **normal six-handed deals only**:

- `nplayersdealt = 6`;
- all six canonical position chairs must exist;
- all six position chairs must be distinct;
- Hero must map to exactly one of UTG/HJ/CO/BTN/SB/BB;
- Hero must still be playing;
- 2–6 players may remain post-flop.

A five-handed table, missing-small-blind positional anomaly, straddle topology or malformed chair map is not silently remapped. It fails the mechanical context gate. Short-handed cash support can be added later with its own explicit position contract.

## Stable IDs

### Absolute position

| ID | Position |
|---:|---|
| 1 | UTG |
| 2 | HJ / MP3 |
| 3 | CO |
| 4 | BTN |
| 5 | SB |
| 6 | BB |

### Live opponent mask

| Bit value | Position |
|---:|---|
| 1 | UTG |
| 2 | HJ |
| 4 | CO |
| 8 | BTN |
| 16 | SB |
| 32 | BB |

The mask retains exact multiway composition without building a separate function for every possible trio/quartet.

### Relative post-flop position

| ID | Meaning |
|---:|---|
| 1 | First |
| 2 | Middle |
| 3 | Last |

In HU only First and Last are legal. `Middle` in a two-player hand is treated as contradictory context.

## Pot families

The family is classified from `NumberOfRaisesBeforeFlop`:

| ID | Raises | Family |
|---:|---:|---|
| 1 | 0 | Unraised / limped |
| 2 | 1 | One-raise pot |
| 3 | 2 | 3-bet pot |
| 4 | 3 | 4-bet pot |
| 5 | 4+ | 5-bet+ / currently unsupported strategically |

ISO and squeeze are **subtypes**, not separate fundamental pot families. This prevents the tree from losing the fact that an ISO is still a one-raise pot and a squeeze is still a 3-bet pot.

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

This is intentionally more precise than a single `f$Init_Hero` flag. Initiative remains useful on later streets, but the preflop role must not be destroyed because it determines the ranges entering the flop.

## Proven ISO detection

For a one-raise pot there is exactly one historical raiser. In normal six-max first-orbit order:

`UTG → HJ → CO → BTN → SB → BB`

A call bit at a position that acted **before** the sole raiser proves a voluntary limp existed before the raise. This is sufficient to mark `f$cc_pf_iso_proven`.

Examples:

- UTG limps, HJ raises → ISO proven;
- CO limps, BTN raises → ISO proven;
- BTN raises, BB calls → not ISO;
- UTG raises, BTN calls → not ISO.

## Conservative squeeze detection

Aggregate action bitmasks do not preserve every chronological detail. CashCrusher therefore refuses to manufacture certainty.

A squeeze is marked **proven** only when:

1. exactly two raises occurred;
2. Hero was one of exactly two unique raisers;
3. Hero's final action tells us whether Hero was opener or final 3bettor;
4. the reconstructed first raiser acts earlier than the final 3bettor in normal first-orbit order;
5. at least one call bit exists strictly between them.

This safely identifies lines such as:

`UTG raise → HJ call → BTN 3bet`.

A reversed-order history compatible with limp-reraise is labelled subtype-unknown rather than rewritten into a normal 3-bet pot.

When Hero was never a raiser in a two-raise pot, the aggregate history may be insufficient to prove who squeezed whom. The mechanical pot remains 3BP, while the subtype stays unknown unless later evidence can prove it.

## Mechanical validity versus strategic coverage

`f$cc_context_valid` answers only:

> Is this state mechanically coherent enough to route?

It does **not** mean a strategy has been written for that state.

Future attack/defense nodes require a separate coverage check. For example, Gate 00C can classify a 4-bet pot correctly even while Gate 01 has no 4-bet-pot flop CBet policy yet. In that situation the policy layer must fail closed.

## Provenance

- Mechanical reconstruction from OpenHoldem/OpenPPL: **T/A** from runtime capabilities.
- Exact six-max context decomposition: **A** architecture.
- Strict fail-closed treatment of unresolved chronology: **P** engineering safety principle.
- No professional poker frequencies are introduced in Gate 00C.

## File

`src/CashCrusher_Context.txt`
