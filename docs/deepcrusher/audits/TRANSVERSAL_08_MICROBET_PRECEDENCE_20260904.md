# DeepCrusher transversal audit 08 — exceptional microbet precedence

Date: 2026-09-04  
Parent Candidate K SHA-256: `5f0e2f2cbfe2d7988d967dae799b3e5f8a631f14d979bcc0d4139f81efc20a35`  
Candidate L SHA-256: `6543dca3877de35e1eba1a3a0f6e242ab1d2b138392644b6f955890aa84a15f5`

## Rule applied

`f$Call_MicroBets` represents an exceptional price state, not an ordinary strategic node. A normal Starting Strategy X/F or FOLD does not automatically prove that Hero should fold to a 2–20% pot price. The helper keeps precedence unless the tiny-price exception itself is shown strategically wrong.

This pass intentionally does **not** move every historical guard. Only clear normal-price folds that were suppressing the exception are changed; ambiguous flop raise-response families remain for later node-by-node review.

## Candidate L changes

### 1. 3wBBvSB high-air/backdoor turn line

After Hero called flop with the documented backdoor family, the normal source says fold a turn 2Bar unless the hand improves to an eligible draw. Draw-call writers remain before the helper so their cross-street history is preserved.

The final ordinary-air fold is moved after `f$Call_MicroBets`:

- normal price + no improvement -> FOLD, unchanged;
- true microbet -> exceptional-price helper may CALL;
- eligible draw -> source-priced CALL and history capture remain unchanged.

### 2. River explicit X/F states

The river router previously evaluated several normal-price X/F states before `f$Call_MicroBets`, including:

- HUBB weak-pair X/F / XC100 states;
- `user_RiverCheckFoldTP` from the 3wBBvBTN current-TP river plan.

Candidate L evaluates `f$Call_MicroBets` first, then those normal-price states. This does not turn the normal strategy loose: after the microbet exception fails, the exact same X/F / X/C conditions still execute.

The later 3wBTNvBB paired-turn and HUSB MP/BP river states were already after the helper and remain there.

## Deliberately not changed yet

Several flop `f$flop_Call` source guards still precede `f$Call_MicroBets` — HUSB completed/no-redraw responses, exact X/R multiplier caps, true-multiway draw responses, etc. Those involve raise ranges and/or potentially near-dead equity, so they are not moved merely by analogy. They require a semantic node pass.

## Validation

Candidate L passes **14/14** focused static checks:

- exact Candidate K parent hash;
- 1,283 OpenPPL blocks preserved;
- executable delta limited to `f$turn_Call` and `f$river_Call`;
- turn pure-air normal fold now follows microbet;
- HUBB river normal X/F follows microbet;
- `user_RiverCheckFoldTP` follows microbet;
- commitment precedence from Candidate K remains intact;
- HU opponent-all-in legality guard remains intact;
- QTo/3wBBvSB dry-TP repair remains intact;
- ASCII and delimiter invariants unchanged.

Candidate L supersedes Candidate K/J for testing. The frozen good-results DeepCrusher remains the permanent rollback, not the preferred new candidate.
