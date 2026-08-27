# Gate08C.1 — HUBB Turn Donk source audit

Status: **implemented, pending/subject to static CI at this commit chain**.

## Scope

This gate maps only the old **HUBB = Hero BB vs SB** Turn-Donk family after an **actual flop X/C**. It does not treat every OOP heads-up caller as HUBB.

CashCrusher recognizes three exact ancestry IDs:

1. true-HU SB open -> BB call (direct HUBB topology);
2. true-HU SB limp -> BB check (direct HUBB topology);
3. 3-6 handed deal reduced preflop to SB-v-BB ordinary SRP, SB open -> BB call (A/P structural descendant, never labelled literal T).

All three additionally require Gate08A closed history: Flop-Donk family 3 was snapshotted, Hero actually checked and called exactly once, the final flop aggressor is the current live SB Villain, Hero did not re-aggress, and Turn is a first-action OOP/no-bet opportunity.

ISO, plain 3BP, squeeze, 4BP, BTN-v-blind and arbitrary reduced-HU opener/caller matchups are excluded.

## Primary Starting Strategy findings

Primary source: `Crusher Strategy/11- NOVO CRUSHFEST HUBB.docx`.

### TP or better — question 2/18

The source asks when to Donk Turn after the flop call and answers: **Donk if Villain 2barrels below 45%**. The source does not specify the Turn size in that answer.

The mature audited DeepCrusher implementation uses the same <=45% threshold, requires a meaningful sample (`pt_hands_headsupchair > 100` and nonzero Turn-CBet stat), and resolves the missing size to **75% pot**.

CashCrusher therefore records:

- action threshold <=45%: **T**;
- >100-hand/nonzero-stat guard: **A** from mature implementation;
- 75% size: **A**, explicitly not promoted to T.

### Draws — question 7/7

After a flop call:

- good draws = OESD / FD / 2mOC+GS -> **X/C Turn** and later River Donk 25% if missed;
- weak draw = GS -> **Donk Turn 25%** and give up River if missed.

CashCrusher implements only the Turn owner here. River instructions are not executed or pre-scheduled by the Turn strategy.

### A/K-high, backdoors and pure air — question 1/7

The source repeats:

- good draws -> X/C Turn;
- weak GS **and air cards** -> **Donk Turn 25%**, give up River;
- if Villain checks Turn, a River probe opportunity is a later-street owner.

Accordingly, bare/no-frontdoor air after the actual flop X/C is a direct-source Turn25 branch. This is not a generic six-max bluff rule outside the exact HUBB ancestry.

### MP/BP — question 2/11: after a big flop CBet

The source states:

- completed Turn -> X/F unless a draw was picked up;
- non-completed Turn -> **Donk 1bb-2bb, maximum 20%**.

Mature DeepCrusher records the >50%-CBet state during Flop defense and later resolves the allowed 1-2bb interval to `TurnMin`/`BetMin`.

CashCrusher adds strategic size ID 5 = **MIN** for this exact family. This is **T source interval + A deterministic BetMin resolution**, not a short-stack commitment rule.

### MP/BP — question 8/11: general Turn Donk

Direct source conditions:

- pair+draw -> X/C;
- bottom pair -> X/F;
- completed flush or completed straight with meaningful overcard -> X/F;
- completed straight undercard **or** non-completed Turn may Donk when:
  - the hand was flop 2nd/3rd pair;
  - it remains current 2nd/3rd pair;
  - Hero has a top-three kicker;
  - board is non-paired;
  - in SRP, flop is not 2BW.
- source size: **25%** (worded as 1-2bb / 25%).

CashCrusher deterministically reconstructs the required **flop 2nd/3rd pair** from the Gate07 family-3 lower-pair snapshot plus persistent exact hole/flop ranks. On the source's positive non-paired-board branch this avoids inventing a stale current-street pair label.

## Flop call-size evidence gap

A closed OpenHoldem round-2 X/C history proves that Hero called; it does **not** preserve the exact amount Hero faced. The big-CBet Q2 rule can override the general Q8 MP/BP size, so absence of a `>50%` marker cannot be interpreted as proof of a small CBet.

Gate08C.1 therefore reserves two **defense-owned** markers:

- `user_cc_flop_donk_hubb_called_gt50`
- `user_cc_flop_donk_hubb_called_le50`

Current Turn attack code never sets them.

For an MP/BP state where action/size genuinely differs across that boundary, HUBB coverage fails closed until exactly one marker exists. Strong-made exploit, good-draw check, weak-GS Turn25 and air Turn25 do not depend on that price proof and remain independently reviewable/executable.

This is intentional source fidelity rather than loss of coverage.

## Short-stack review

No HUBB Turn-Donk action in this gate was zeroed merely because DeepCrusher came from short-stack Spin play. Conversely, no generic commitment/stackoff behavior was transplanted.

The inherited elements were split by ownership:

- <=45% Villain 2bar exploit: retained in exact HUBB state;
- TP+ 75%: retained as **A size-gap resolution**, not universal value sizing;
- weak-GS/air 25%: retained as direct T;
- MP/BP 1-2bb/max20: represented by source-specific MIN ID;
- no `BetMax`, no jam threshold, no `Raise_Committed`, no `EffectiveStack` shortcut.

## Files

- `src/CashCrusher_Turn_Donk_HUBB.txt`
- `src/CashCrusher_Turn_Donk_Common.txt`
- `src/CashCrusher_Turn_Donk.txt`
- `tools/test_turn_donk_hubb.py`

## Next source family

After CI confirmation, Gate08C.2 audits **3wSBvBTN** Turn Donk. The intended order remains source-first: `3wSBvBTN` -> `3wSBvBB` -> `3wBBvBTN`, then six-max P-heavy gaps/runtime/history closure.
