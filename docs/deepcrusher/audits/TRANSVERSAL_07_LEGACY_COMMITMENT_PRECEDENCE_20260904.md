# DeepCrusher transversal audit 07 — legacy commitment precedence

Date: 2026-09-04  
Frozen baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`  
Parent Candidate J SHA-256: `87149e6a86ab419b61a7b87711d0f82978063093ad2baa787dc3bf42cb27c64a`  
Candidate K SHA-256: `5f0e2f2cbfe2d7988d967dae799b3e5f8a631f14d979bcc0d4139f81efc20a35`

## Why this pass exists

The post-QTo review initially treated several ordinary Starting Strategy CALL/FOLD rules as if they had absolute precedence over `f$Raise_Committed`. That was too literal. The project now treats commitment as an exceptional stack-geometry state: if the ordinary strategy wants to continue and the call consumes most of the effective stack, completing all-in is a deliberate adaptation unless there is evidence specifically about that committed geometry saying otherwise.

Candidate J corrected the new post-QTo guards. This pass audits the older pre-existing guards that were already in the good-results baseline before the QTo review.

## Finding

The legacy baseline still had a large source-specific block *before* `f$Raise_Committed` in `f$flop_Raise`. It covered:

- 3wSBvBTN TP+ Axx exception;
- HUSB TP / MP-BP / draws / air after facing a raise;
- 3wBTNvBB TP+ and no-made after facing X/R;
- 3wSBvBB source check-raise plans;
- 3wBBvSB exact check-raise response families;
- true-multiway draw-donk response families.

Several of those branches returned `false` specifically to preserve a normal CALL. Because they ran first, a call that would otherwise satisfy the project's commitment threshold could never become all-in. The comments even stated that suppressing commitment was intentional.

Under the corrected project rule, that is not a valid default. The written strategy describes the ordinary action tree; it does not automatically veto an exceptional committed state. Some source documents themselves explicitly discuss shallow stacks, 1:1 SPR construction, stacking off, and all-in continuation, reinforcing that normal CALL labels are not universally literal at all stack geometries.

## Candidate K change

### `f$flop_Raise`

The legacy scenario-specific ordinary-strategy block is moved after:

`When f$Raise_Committed Return true Force`

No source action is deleted. When commitment does not fire, the same HUSB / 3w / multiway rules execute in the same relative order as before.

### `f$turn_Raise`

The older 3wSBvBB delayed-check source block is likewise moved after `f$Raise_Committed`. Its existing opponent-all-in legality branches are preserved.

### `f$Raise_Committed` legality guard

A small safety rule is added:

`When HandIsHeadsup && nopponentsallin > 0 Return false Force`

If the only opponent is already all-in, there is no strategic re-raise to make. This prevents the commitment helper from manufacturing an impossible raise and leaves the normal CALL/FOLD path in control. In true multiway pots the guard does not fire merely because one opponent is all-in; another active opponent may still make a raise legal.

## What did NOT change

- The QTo-class repair remains: 3wBBvSB dry TP+ versus a non-low Facing Bet is still a normal-geometry CALL rather than the old grotesque generic Over-Donk fold.
- The deliberate ~52% and ~76% implementation margins remain unchanged.
- No source branch was made looser/tighter merely due a threshold mismatch.
- The HUSB delayed-float reachability repair remains.
- Historical-hand-class vs current-strength river repairs remain.
- Candidate J's corrected new exception ordering remains.

## Static regression

`test_deepcrusher_candidateK_legacy_commitment.py` passes **24/24**.

Verified:

- frozen baseline hash exact;
- Candidate J parent hash exact;
- 1,283 OpenPPL blocks preserved in identical order;
- zero duplicate blocks;
- zero new executable `f$` references;
- J -> K executable delta restricted to exactly three blocks: `f$flop_Raise`, `f$turn_Raise`, `f$Raise_Committed`;
- commitment precedes all audited legacy flop ordinary-strategy guards;
- commitment precedes the legacy 3wSBvBB turn block;
- HU opponent-all-in legality guard precedes commitment evaluation;
- QTo-family repair and later history/current-strength repairs remain present;
- ASCII-only file and delimiter imbalance unchanged from Candidate J.

This remains static validation, but Candidate K is a strict strategic/runtime-ordering improvement over J under the corrected project directive.

## Next review target

1. Legacy rules that still execute before `f$Call_MicroBets`: distinguish harmless same-action cases from normal-price FOLDs that improperly suppress the extreme-price exception.
2. Second semantic pass through defensive nodes 1–32 after helper precedence is settled.
3. Attack nodes 33–45 after the same helper review.
4. Sizing path and OpenHoldem runtime/log validation.
