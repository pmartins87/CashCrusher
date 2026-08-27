# Gate 05A — Turn Float history/source audit

Status: **IMPLEMENTED / STATIC-RUNTIME CONTRACT PASS**

Code-changing Gate04R/Gate05A regression: GitHub Actions run **#512 — PASS**. The subsequent documentation-only combined branch run **#516 — PASS** also retained the complete suite green.

## Scope

This gate freezes only the **history ownership** of Turn Float. It intentionally does not choose Turn hand-strength frequencies yet.

The key question is: when CashCrusher reaches the turn with `AmountToCall = 0`, which prior flop lines truly correspond to the DeepCrusher `f$move_turn_floatbet` family?

## Primary-source findings

### 1. DeepCrusher router meaning

`f$turn_Raise_Noinitiative` routes a LAST/MIDDLE player with `f$act_0_nothing_to_Call` to `f$move_turn_floatbet` and describes the state as Villain having skipped continuation aggression.

CashCrusher keeps the ownership concept but narrows the new six-max baseline to **exact LAST**. `MIDDLE` with a live player behind is not allowed to inherit a last-to-act Float tree.

### 2. 3wBBvSB — Facing Bet -> Turn check

The source strategy is explicit for no-made hands after Hero calls flop aggression and Villain checks turn:

- real draws Float 50%;
- air / A-K-high-backdoor families Float 50%;
- non-completed origin generally gives up river;
- completed turn can create Float50 + river barrel provenance.

This is the strongest direct source anchor for the ordinary `call flop -> aggressor checks turn` parent.

### 3. 3wBTNvSB — no-made restraint

The current audited DeepCrusher starts the 3wBTNvSB Turn-Float branch with `NoMadeHand -> false`. The underlying source emphasizes equity realization against SB's unusually strong range rather than broad bluffing.

This restriction belongs to Gate05 strategy, not to the history bridge itself.

### 4. BTN Advanced — called flop X/R

The BTN Advanced source contains a distinct state after Hero bets flop, calls a flop raise/check-raise, then the aggressor skips the turn barrel. For AIR/A-high it gives a **25–40%** Float range; current DeepCrusher uses Turn33. It explicitly does not automatically transfer the AIR instruction to existing FD/OESD.

Therefore `CBet -> X/R -> call -> Turn check` is a separate Turn-Float parent, not ordinary missed-2Bar history.

CashCrusher also preserves a third parent, `Flop Float -> later raise -> Hero call -> Turn check`, but marks it as an analogous executed-history family whose strategic policy still needs separate Gate05 review.

## Histories that are NOT Turn Float

The following are explicitly quarantined:

| Closed flop history | Correct future owner |
|---|---|
| Hero Flop Float bet -> Villain call | continuation of Hero aggression; not canonical Turn Float |
| Flop Float opportunity -> Hero check-back | Delayed Float |
| Hero ordinary CBet -> Villain call | Turn CBet |
| preflop aggressor checks flop and flop checks through | Delayed CBet |
| Hero calls a flop donk from a player who was not the final preflop aggressor | separate donk/defense history, not ordinary missed-2Bar Float |
| multiple flop aggressors / raised pot without a clean parent | fail closed until separately audited |

## OpenHoldem history audit

The supplied OpenHoldem source establishes several mechanical facts used by this gate:

- `raisbitsN` is the bitmask of chairs that raised/bet in betting round `N`;
- for a previous betting round, `raisbitsN` is stable persisted history;
- `lastraisedN` stores the chair of the last raiser/aggressor in that round;
- on the transition to a later round OpenHoldem repairs the previous-round Hero final-raise history when required, so `lastraisedN`/`raisbitsN` remain usable after the street closes;
- `didcallroundN`, `didraisroundN`, `didbetsizeroundN` and `didalliroundN` are Hero action counters; `didchecroundN` is a boolean-style check history;
- `BotsActionsOnThisRoundIncludingChecks` is required when the first Hero action must distinguish a prior check.

Consequently, a clean ordinary Turn-Float parent can be proven as:

1. Hero had a supported caller-side preflop role;
2. one and only one flop aggressive chair exists;
3. Hero's flop action was exactly one call and no Hero check/aggression;
4. `lastraised2` identifies that flop aggressor;
5. that aggressor is the same player as the **actual final preflop aggressor**;
6. the aggressor remains live;
7. on turn Hero is exact LAST, has not acted, and `AmountToCall = 0`.

In HU this means the sole Villain checked. In current multiway, reaching exact LAST with zero to call means all currently live players before Hero declined to bet.

## Gate04R bug found during Gate05A

The Gate05 audit exposed a real reachability problem in the prior Flop Float 3BP code.

The older `f$cc_pf_3bet_first_raiser_pos_id` / `f$cc_pf_3bet_final_raiser_pos_id` chain depends on `f$cc_pf_other_raiser_pos_id`, which explicitly requires `f$cc_pf_hero_ever_raised`.

That is valid for Hero-as-opener or Hero-as-3bettor reconstruction, but it means a Hero with `f$cc_pf_role_cold_call_3bet` can never obtain a non-zero final-3bettor position from that chain. Several Gate04E pure-coldcaller Float branches therefore had strategy code but no reachable chronology proof.

### Repair

`CashCrusher_FinalAggressor_Context.txt` now adds a stronger caller-side evidence path based on stable `lastraised1` + `raisbits1`:

- actual final preflop aggressor chair/position;
- the other unique raiser in a two-raise pot;
- standard first-orbit order proof;
- plain 3BP versus squeeze proof;
- Hero opener-call / pre-3bet-coldcaller / post-3bet-coldcaller origin.

`CashCrusher_Flop_Float_3BP_CallerRepair.txt` uses that evidence only for the previously unreachable **pure coldcaller** descendants. The strategic action/sizing policy is copied from Gate04E; this corrective gate changes chronology reachability, not poker frequencies.

The top-level Flop Float router now combines original Gate04E coverage with repaired Gate04R coverage while keeping plain-3BP and squeeze as the same family IDs.

## Frozen Turn-Float parent taxonomy

| Parent ID | Closed flop history | Evidence level |
|---:|---|---|
| 1 | supported preflop caller; called exactly one flop bet from actual final preflop aggressor | T/A with P fail-closed reconstruction |
| 2 | Hero CBet -> later raise/XR -> Hero call; Villain is final flop aggressor | A/T; direct BTN Advanced ancestry |
| 3 | Hero Flop Float -> later raise/XR -> Hero call; Villain is final flop aggressor | A/T history owner; strategy still needs separate review |

Any overlap gives parent ID 0.

## Multiway preservation

Gate05A never converts a hand to generic HU merely because only two players remain on turn.

The bridge exposes separately:

- current HU from a HU flop;
- flop multiway -> turn HU;
- turn still multiway.

For current HU, `lastraised2` must resolve to `headsupchair` before a later HU strategy may rely on exact aggressor identity.

## Next gate

**Gate05B — Turn Float direct-source strategy descendants.**

Start only with the two strongest source owners:

1. 3wBBvSB `Facing Bet -> call -> Turn X`, including completed/non-completed river-plan provenance;
2. BTN Advanced `CBet -> X/R -> call -> aggressor X Turn`, preserving the AIR/A-high 25–40% source boundary and the explicit draw exclusion.

Only after those are frozen should six-max SRP/ISO/3BP/squeeze/4BP and multiway P-heavy gaps be filled.
