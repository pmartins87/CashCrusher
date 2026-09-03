# DeepCrusher transversal audit 04 — current river strength versus historical plan

Date: 2026-09-03  
Branch: `deepcrusher-rereview-20260903`  
Frozen good-results baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`  
Parent Candidate D SHA-256: `066446c6ed8bed887a5527115f20b1eff0a44a3250760cb745dd6f62dc0877cb`  
Current Candidate H SHA-256: `a4f45233db5767aa0727bbb8a05e1c43d515a9fc1d086e4dc7c3851b79114a61`

## Review rule

Historical state selects the strategic line; **current hand strength must still select the current action** unless the source explicitly says otherwise. A state meaning “flop low TP”, “turn MP” or “turn TP called paired donk” must not blindly override a river improvement or deterioration.

Small threshold margins remain untouched. This pass is about material action inversions.

## Candidate E — 3wSBvBB historical low-TP plan suppressed strong river improvements

The Starting Strategy describes paired-board low TP as a line that barrels flop/turn and then **decides river**, mainly checking when the ordinary low-TP holding remains weak. It does not say to check strong river improvements.

`user_hardcoded.cpp` explicitly re-evaluates the river and value-bets current two-pair+ for this family.

The DeepCrusher historical states `user_FlopCbet_Turn33_RiverCheck` / `user_FlopCbet_TurnCbet_RiverCheck` previously returned false without first checking whether the river improved the hand materially.

Repair: current `f$CF7_TwoPairPlus` is value-bet at River75 before the historical check branch. The historical ordinary low-TP check remains intact.

Candidate E static regression: **17/17 PASS**.

## Candidate F — 3wBBvBTN dry X/R + turn barrel TP plan could misclassify river strength

Written `3wBBvBTN` source, after dry flop X/R and turn barrel:

- if Hero still has TP with J+ kicker -> all-in;
- if Hero still has TP with T-or-lower kicker -> X/F.

The old OpenPPL applied the kicker test from the historical `user_RaisedFlopTP_3wBBvBTN` line without first proving that Hero still held current top pair. That creates two material failure modes:

1. a river improvement to two-pair+/trips/straight/flush can inherit the old TP fold branch;
2. a river overcard can demote the old TP below current TP, yet the old kicker branch can still manufacture the TP value-jam state.

`user_hardcoded.cpp` contains an explicit audit comment for the same class: river made value cannot fall into the automatic fold of the barreled-TP line; it re-evaluates current two-pair+/straight+/flush+/trips before the TP decision.

Repair:

- current TwoPairPlus -> River75 value before TP branch;
- TP kicker fold/jam rules are gated by current `f$CF7_TopPairReal`;
- a hand degraded below current TP cannot inherit the TP-jam branch and is assigned the check/fold state in this exact dry triple-pressure line.

Candidate F static regression: **18/18 PASS**.

## Candidate G — HUSB MP exploit check/fold could fold a strong river improvement

Old HUSB MP Q8 says that after deliberately checking the turn with MP/BP, the response to a river probe can be profile-dependent:

- opponent overfolded flop -> little air remains -> check/fold plan;
- opponent overcalled flop -> more air remains -> check/call plan;
- unknown/balanced -> simpler small turn barrel instead.

The OpenPPL state `user_RNCF_HUSB_MP_XF_RiverProbe` is written on the **turn**, while Hero still has 2nd/3rd pair. The river `f$river_Call` then folded unconditionally from that historical state. A river improvement to two-pair+/trips/straight/flush was therefore still capable of inheriting the old MP fold.

The C++ implementation repeatedly applies the opposite audit invariant to HUSB MP/BP lines: if the river brought real value, re-route by **current** strength before the historical MP/BP plan.

Repair: current `f$CF7_TwoPairPlus` is guaranteed at least a CALL before the historical XF guard. `f$river_Raise` retains first priority, so this guard does not suppress a value raise when the raise router selects one.

Candidate G static regression: **13/13 PASS**.

## Candidate H — resolved 3wBTNvBB paired-turn Donk river plan

Transversal 03 intentionally left one source interpretation open. Re-reading the complete source plus the already-existing player classifier resolves it without inventing a new threshold.

Starting Strategy `3wBTNvBB TP or better 08/14`:

- vs >~50% turn Donk on paired turn: **readless call turn & call/fold river**;
- vs **confirmed aggressive players call twice**.

`user_hardcoded.cpp` resolves the readless branch as ordinary TP folding to the next river barrel, while strong current river improvements escape the historical TP fold.

DeepCrusher already has `f$RedGuy` as its explicit confirmed-aggressive classifier: at least 100 hands and total AFq >= .53. Candidate H therefore does not invent a new read definition.

River action ownership after the recorded paired-turn call:

- current TwoPairPlus -> at least CALL (raise router still acts first);
- current TP/OP versus `f$RedGuy` -> CALL twice, implementing the written aggressive-player exception;
- otherwise readless -> FOLD to the river barrel.

Candidate H static regression: **16/16 PASS**.

## Why these changes are not generic “play stronger hands more aggressively” patches

Each repair requires both:

1. a specific historical state proving the source line; and
2. a current hand class proving what Hero actually holds now.

No global river looseness was added. No 50/52 or 75/76 boundary was changed. The frozen baseline remains untouched.

## Remaining review after Candidate H

The material review is not finished. Remaining work, in practical order:

1. **Persistent-state audit, remaining candidates** — continue checking historical `user_*` states that can force river/turn actions without current-strength reclassification. Most are legitimate plans; only source-confirmed inversions are changed.
2. **Turn CALL/FOLD versus `f$Raise_Committed`** — complete the source-explicit turn-call inventory and protect any remaining calls that the generic 55% commitment helper can wrongly convert into jam.
3. **Shared helper scope** — reconcile remaining global `f$hand_slowplay` rules for two-pair+/trips/straight+, plus any remaining `f$Call_MicroBets`, `f$hand_dead`, `f$hand_zombie` precedence leaks.
4. **Defense nodes 1–32, second semantic pass** — re-run CBet/Donk/Float/Bet/Raise-vs-Raise after helper repairs, looking for material action cliffs or source rules erased by generic Normal/High/Over routing.
5. **Attack nodes 33–45, post-helper recheck** — verify writers/readers, delayed/probe/donk histories and current-strength upgrades after the transversal changes.
6. **Pot / history / initiative end-to-end** — verify SRP/ISO/Limped overlaps, preliminary hand-class markers versus actual final-action markers, and initiative transitions after check/call/raise.
7. **Sizing ownership** — `f$BestBetsize`, HU/multiway street sizing, `RaiseTo`/`RaiseBy`, near-all-in conversion and state leakage; selected strategic action must survive the sizing layer.
8. **Deterministic static + OpenHoldem parser/runtime validation** — regression corpus, formula load/parser validation and representative runtime/log replay.
9. **Final comparison against frozen good-results baseline** — promote only after runtime behavior is verified; baseline remains permanent rollback.

## Candidate chain

- Baseline: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`
- Candidate D: `066446c6ed8bed887a5527115f20b1eff0a44a3250760cb745dd6f62dc0877cb`
- Candidate E: `cf9a25c47eb1b6a08d4b72abe623cb4d0422587b0c9109d651cb586c1ebba122`
- Candidate F: `a4d75ae1d3768c95cd6e418baf5ce09f267d881960a9ee89a1483796a28d5918`
- Candidate G: `69822761afa407d31acc03385022a2e5269ca57823883424df4f2b7464b91e12`
- Candidate H: `a4f45233db5767aa0727bbb8a05e1c43d515a9fc1d086e4dc7c3851b79114a61`

Candidate H is **not promoted** and has not undergone OpenHoldem runtime validation.