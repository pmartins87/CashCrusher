# Gate 04A — Flop Float source/topology audit

Status: **source boundary frozen; implementation begins from exact checked-to caller contexts**.

## Node definition

CashCrusher uses **Flop Float** in the narrow routing sense inherited from the audited DeepCrusher/Crusher architecture:

> Hero did not own the preflop initiative, reaches the flop with no bet to call, and has the positional opportunity to bet after the expected aggressor checked.

This is not a generic `AmountToCall = 0 -> bet` node. It is also not Flop CBet, Donk, Probe or Delayed CBet.

For the first CashCrusher baseline the strategic Float owner must be **exact LAST/IP**. Legacy routers also admitted `Position = Middle`, but in six-max a middle-position player still has a live player behind and therefore does not receive the HU/last-to-act Float policy by analogy alone.

## Runtime gate

The canonical first-action gate is built from:

- `IsFlop`;
- `f$cc_context_valid`;
- `AmountToCall = 0`;
- Hero is a preflop caller, not final aggressor;
- exact IP/LAST ownership for the reviewed family;
- `BotsActionsOnThisRoundIncludingChecks = 0`.

The last condition is intentional. OpenPPL's ordinary `BotsActionsOnThisRound` does not count checks; `BotsActionsOnThisRoundIncludingChecks` does. The Float classifier must not relabel a later flop action after Hero already checked as an initial checked-to stab.

## Direct/source-anchored families

### F1 — true-HU HUSB limp/call versus BB raise

Topology:

`SB/Button limp -> BB raise -> Hero call -> BB checks flop -> Hero IP`

Mechanical CashCrusher proof:

- `f$cc_true_hu`;
- one-raise pot;
- `f$cc_pf_hu_limp_raise_proven`;
- Hero role = one-raise caller;
- Hero IP;
- Hero/Villain matchup = SB versus BB.

Current DeepCrusher source boundary:

- air is explicitly allowed to Float 50 in the checked-to ISO/limp-raised history;
- current made pair+ was resolved by the reviewed human/C++ gap interpretation to a 50 family;
- real/good draws bet 50–75, with stronger draws using the larger end;
- no generic fallback survives.

CashCrusher may preserve these **action directions** with direct/high structural ancestry, while future response to a check-raise is separate defense ownership.

### F2 — reduced-HU BB caller IP versus SB PFA

Topology:

`SB raises -> BB calls -> SB checks flop -> BB IP`

This is the closest six-max descendant of the audited `3wBBvSB` Facing-Check tree.

Source direction:

- TP+ dry: small stab;
- TP+ wet: value/protection stab;
- medium pairs often check to delayed families, with some dry weaker-pair bets;
- no-made gutshot-or-better frontdoor draws: bet;
- dry air: stab;
- wet air: check/delay;
- the old generic HandPower/random tail is not accepted.

The source's wet-board `<=20bb / >20bb` sizing split and several `shove vs XR` plans are **short-stack review evidence**, not automatic 100bb cash rules. CashCrusher keeps the betting direction but reassigns cash-depth sizing and does not infer stackoff from TP+.

## Six-max SRP gap families

Normal SRP caller-IP states such as:

- HJ caller versus UTG opener;
- CO caller versus UTG/HJ;
- BTN caller versus UTG/HJ/CO;

have no literal Spin source range family. They are P-heavy.

Professional-theory fill is constrained by:

- current made-hand strength;
- board pressure parent;
- caller/opener positional range asymmetry;
- PFA check range remaining potentially protected;
- IP equity realization;
- preference for equity-rich semibluffs over random air;
- medium showdown value often checking back;
- smaller/wider pressure on static high/paired boards;
- more selective betting on dynamic low/mid boards.

No single BTN-v-blind source frequency is copied into EP/MP cold-call matchups.

## ISO / 3BP / squeeze / 4BP

These are first-class future Float families, not ordinary-SRP fallbacks.

- **ISO caller Float:** original limper and post-raise cold caller have different range origins; exact caller provenance must be proved before strategy.
- **Plain 3BP Float:** opener-call and cold-call-3bet are separate range families.
- **Squeeze Float:** opener, pre-squeeze caller and post-squeeze caller histories are not interchangeable.
- **4BP Float:** call-4bet ranges are strongly condensed and require a dedicated P-heavy policy; unsupported chronology remains fail-closed.

## Multiway checked-to stab

When Hero is exact LAST and the flop is still multiway, `AmountToCall = 0` means all live players before Hero have checked. That state is mechanically classifiable, but strategically it is **not HU Float**.

The multiway checked-to baseline must be tighter:

- robust value bets;
- best draws / selected high-equity semibluffs;
- sharply reduced pure-air stabs as player count/range selection increases;
- medium showdown value checks frequently;
- no short-stack sidepot player may collapse the whole decision into a shallow-stack policy.

Hero in relative `MIDDLE` is not granted this Float strategy merely because no bet currently exists; someone remains to act behind.

## Provenance contract

- **T** — OpenHoldem/OpenPPL action/position/history mechanics.
- **A** — direct structural adaptation of an audited DeepCrusher/Starting Strategy/CrusherTBP node.
- **P** — professional-theory six-max cash fill where no literal source tree exists.
- **X** — rejected legacy behavior, including random/HandPower tails and automatic short-stack stackoff transfer.

Every implementation function must state its local Source/Provenance and use flat complete `WHEN` rules.

## Gate04A implementation order

1. common opportunity/hand/board/size descriptors;
2. F1 true-HU HUSB limp-raised checked-to source descendant;
3. F2 BB-v-SB ordinary-SRP checked-to source descendant;
4. HU ordinary-SRP six-max caller-IP gaps;
5. true multiway ordinary-SRP checked-to LAST baseline;
6. ISO / plain3BP / squeeze / 4BP as separately owned children;
7. sizing/execution/history provenance only after strategic routing is stable.
