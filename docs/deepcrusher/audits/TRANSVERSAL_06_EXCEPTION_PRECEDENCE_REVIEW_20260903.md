# DeepCrusher transversal audit 06 — exceptional geometry precedence re-review

Date: 2026-09-03  
Frozen good-results baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`  
Parent Candidate I SHA-256: `19e578744e38df4e52046321df290ec39a8c624c5de0181f8e8ceeda9e1b5f87`  
Candidate J SHA-256: `87149e6a86ab419b61a7b87711d0f82978063093ad2baa787dc3bf42cb27c64a`

## Corrected strategic principle

The Starting Strategy describes the ordinary strategic tree unless it explicitly says otherwise. It is not a complete enumeration of every exceptional stack geometry or extreme price state.

`f$Raise_Committed` is intentionally an exceptional stack-geometry helper. Its own DeepCrusher documentation says it converts a call into an all-in raise when the remaining effective stack is economically trivial, including when the call consumes more than ~55% of Hero's stack or Villain has committed most of the relevant stack. Therefore a normal source rule saying CALL must not automatically be interpreted as prohibiting the committed all-in completion.

Likewise, `f$Call_MicroBets` is an explicit exceptional-price helper. A normal-price source FOLD/CALL branch must not automatically suppress the extreme pot-odds exception unless the source itself clearly covers that tiny sizing.

The correct precedence for newly reconciled post-QTo rules is therefore:

`exceptional geometry/price helper -> scenario-specific normal strategy -> generic scenario fallback`

not:

`literal source action -> disable exceptional helper`.

This does **not** mean the exceptional helper is infallible. It means it retains precedence unless there is concrete evidence that its own trigger/action is materially wrong for that exceptional context.

## What from the post-QTo work is kept

### KEEP — QTo / 3wBBvSB gross Over-Donk regression repair

The original motivating defect remains real: at ordinary ~25bb geometry, top pair on a dry board could fall through the generic Over-Donk fallback and fold despite the Crusher material supporting continuation.

Candidate J keeps the class-level 3wBBvSB TP+ dry/non-lowbet CALL and wet/small-dry RAISE logic. The change is only precedence: `f$Raise_Committed` now gets first refusal. Thus:

- ordinary 25bb-style geometry -> source-specific CALL/RAISE;
- genuinely committed geometry -> all-in completion may override the normal CALL.

No QTo/Q72 hand-specific patch exists.

### KEEP — 3wBTNvBB Facing-Bet scenario tree

The scenario-first normal tree spanning Normal/High/Over sizes is retained. It no longer disables commitment. Exceptional committed geometry runs first; otherwise the source-specific call/raise/fold tree applies before generic High/Over fallback.

### KEEP — current-strength reclassification fixes

Repairs that prevent stale flop/turn labels from forcing river actions remain valid. Examples include old TP history being re-evaluated against current river strength and old MP/BP history not auto-folding a current 2P+ hand. These are logic corrections, not attempts to literalize normal strategy over an exceptional stack state.

### KEEP — stale action-history fix

Removal of the generic river barrel from `user_3wBTN_Had_Air_OTF` remains valid because “had air on flop” is not equivalent to “checked flop.” Exact final-action histories remain the correct owners of delayed-barrel lines.

### KEEP — `f$hand_slowplay` scope leak repair

The dry-rainbow TP slowplay rule whose own provenance/comment points to 3wBTNvBB remains scoped to that scenario instead of leaking globally. This is a confirmed scope defect independent of commitment.

### KEEP — delayed-float reachability repair

The HUSB detailed delayed-float subtree remains reachable by excluding HUSB from the broad residual fallback that previously returned before its specific reader. This is an unreachable-code/precedence defect unrelated to stack commitment.

### KEEP — source/comment/provenance corrections

The corrected source policy, comments, and provenance remain. Comments must describe actual executable semantics.

## What from the post-QTo work was wrong and is corrected in Candidate J

### REORDER — flop Facing-Bet CALL/FOLD guards

Candidate C/H/I placed the new 3wBBvSB and 3wBTNvBB normal Facing-Bet ownership **before** `f$Raise_Committed` specifically to stop CALL->JAM conversion. That interpretation was too literal and is reversed.

Candidate J places the recent Facing-Bet tree **after** `f$Raise_Committed`. The normal strategy remains improved; the exceptional committed completion remains legal.

### REORDER — turn draw / turn-donk CALL guards

Recent 3wBBvSB draw-improvement guards and 3wBTNvBB turn-donk CALL/FOLD ownership were also placed before `f$Raise_Committed`. They are moved after it. A committed turn can therefore jam even when the ordinary tree would call.

### REORDER — HUSB turn CALL/FOLD ownership

Candidate I added HUSB guards whose stated purpose was to prevent the generic committed jam. Those action guards now execute only after `f$Raise_Committed` fails. The HUSB normal tree is still used in ordinary geometry.

### REORDER — recent source rules versus `f$Call_MicroBets`

Recent normal-price rules that were deliberately placed before `f$Call_MicroBets` are moved after it, including the new 3wBBvSB pure-air normal-price fold and recent turn/river normal plans. Tiny-bet price protection therefore remains an exception.

## Important separation: pre-QTo inherited code

The frozen baseline already contains older guards that precede `f$Raise_Committed` or `f$Call_MicroBets`, for example some HUSB, 3wBTNvBB, 3wBBvSB and 3wSBvBTN response branches. Those guards **predate the QTo re-review** and were not created by Candidate C–I.

Candidate J does not silently rewrite those older baseline decisions. The baseline is intentionally frozen and the user asked first for a re-review of the work done after the QTo Over-Donk discovery. However, the same corrected principle now makes the inherited pre-helper guards a required later audit target: each must be judged on the actual exceptional geometry, not automatically preserved or automatically removed.

## Candidate J static regression

`test_deepcrusher_candidateJ_exception_precedence.py` passes **27/27** checks.

It verifies:

- frozen baseline SHA unchanged;
- Candidate J has the same 1,283 OpenPPL block sequence as baseline and Candidate I;
- zero duplicate blocks;
- deliberate ~52 and ~76 operational margins remain;
- recent flop Facing-Bet tree executes after `f$Raise_Committed`;
- recent turn 3wBBvSB / 3wBTNvBB / HUSB action ownership executes after `f$Raise_Committed`;
- recent flop/turn/river normal-price rules execute after `f$Call_MicroBets`;
- the ordinary 3wBBvSB TP+ dry/non-lowbet CALL that fixes the motivating QTo class remains present;
- the slowplay scope repair, delayed-float reachability repair, stale-air history fix and current-strength river repair remain present;
- Candidate I -> J executable delta is limited to exactly five top-level action aggregators: `f$flop_Raise`, `f$flop_Call`, `f$turn_Raise`, `f$turn_Call`, `f$river_Call`;
- delimiter imbalance is unchanged.

This is static regression only. Candidate J is not promoted to runtime.

## Updated review invariant

For every future rule, ask in this order:

1. What exact runtime state are we in?
2. Is this ordinary strategy geometry, or an explicit exceptional helper state such as committed stack / microbet / all-in?
3. Does the written Crusher source explicitly cover the exceptional state? If not, do not force its ordinary action literally onto that state.
4. Is the exceptional helper itself strategically reasonable here? If yes, preserve it.
5. Only then reconcile Crusher Starting Strategy, CrusherTBP, user_hardcoded and professional theory for the remaining normal tree.

The audit target remains gross or material poker defects, not harmless implementation differences.
