# Gate06C — River Float ordinary-SRP six-max audit

Date: 2026-08-24

## Scope

This gate reviews only **ordinary one-raise SRP** River-Float states after Gate06A proved the canonical history:

> Hero called Villain's turn aggression, Villain checked River, Hero is first-to-act-for-Hero on River and exact LAST/IP for the reviewed Float opportunity.

ISO, 3BP, squeeze, 4BP, Donk, Probe, Delayed and defensive actions remain separate owners.

## Source boundary

Gate06B already established the strongest supplied-source River-Float rules:

- manually reviewed TBP value baseline: top pair with top-four kicker or better;
- mature DeepCrusher sizing refinement: TP/OP 50, 2P+ 75, super-completed 2P+ 50, nutted class before that reduction;
- exact `3wBBvSB` busted-draw bluff requires its historical flop-backdoor -> turn-real-draw -> called-2Bar provenance and uses 25%;
- `3wBTNvSB + no-made` is an explicit check.

The supplied Crusher environment never has more than three players. Therefore Gate06C corrects an earlier over-broad interpretation: the generic source value ladder may remain high-ancestry for HU/three-way fields, but it is **not source-owned for a hand whose flop began 4+ way or whose River still has 4+ players**.

`f$cc_river_float_source_general_domain_supported` now requires:

- flop entry between 2 and 3 players; and
- current River between 2 and 3 players.

This is a source-domain correction, not a claim that source value becomes strategically wrong in every 4+ situation.

## Ordinary-SRP topology split

`CashCrusher_River_Float_SRP_Gaps.txt` preserves five reviewed topology classes:

1. clean HU, Hero was ordinary-SRP caller and current Villain is the original PFA;
2. clean HU, Hero was PFA but later lost initiative and called turn aggression;
3. current River exactly three-way after source-sized flop entry;
4. flop entered three-way but River is HU while the turn-call player count is unresolved;
5. flop entered four-plus way, regardless of how many players remain on River.

The fifth class is intentionally tested before all others because a 4+ origin remains selected-range provenance even after later folds.

## Professional-theory fills

### Clean HU / source-sized three-way residuals

No extra pure-air bluff is created from `current River no-made` alone.

Reason: River bluff quality depends materially on **which turn-call draw/blocker combinations reached River**. Gate06A can prove the call and aggressor identity, but it cannot yet prove a generic turn-call hand-class snapshot. DeepCrusher's only explicit no-made River-Float bluff itself depends on exactly such history.

Therefore:

- source-silent no-made -> reviewed check;
- weak TP beyond the source top-four-kicker threshold -> reviewed check;
- second pair / third-or-worse pair -> reviewed check.

These are deliberate P baselines, not unimplemented fall-throughs. A future defensive turn-call snapshot may create reviewed busted-draw bluff candidates without changing this ownership contract.

### Four-plus flop origin

The source value ladder is replaced by a tighter P-heavy robust-value baseline because four-plus selection never existed in the source environment.

Generic positive action requires:

- literal nuts; or
- on a public one-card four-to-straight/flush structure: literal nuts or full-house+; or
- on ordinary straight/flush-completed River: current straight-or-better; or
- on a non-completed River: current 2P+.

Sizing:

- literal nuts -> 75%;
- other reviewed robust value -> 50%.

This is a **betting threshold only**. It is not a stack-off threshold and does not imply any raise/jam response.

## Canonical router

`CashCrusher_River_Float.txt` now exists and currently routes only:

1. Gate06B source/high-ancestry coverage;
2. Gate06C ordinary-SRP reviewed gaps.

ISO, plain 3BP, squeeze and 4BP are deliberately absent and therefore fail closed.

A reviewed check has size ID 0. A positive action must own exactly one canonical River size ID.

## Safety checks

Gate06C executable policy contains no:

- `HandPower`;
- random tail;
- `BetMax`;
- `f$Raise_Committed`;
- `f$hand_StackOffDraws`;
- `f$allin_on_betsize_balance_ratio` action;
- generic `no-made -> bet` rule.

The short-stack migration contract remains unchanged: stack-sensitive source logic is reviewed per exact node, not globally banned and not blindly transplanted.

## Validation

New deterministic contracts:

- `tools/test_river_float_srp_gaps.py`;
- `tools/test_river_float_coverage.py`.

`tools/test_river_float_source.py` was also strengthened to require the source-domain <=3-player boundary.

GitHub Actions run **#604** completed **SUCCESS**, including global lint and all 35 strategy/history/runtime contracts currently in the workflow.

## Gate06C result

**PASS at static/deterministic policy level.**

Remaining before River Float is complete:

- ISO River Float;
- plain 3BP River Float;
- squeeze River Float;
- clean supported 4BP River Float;
- River-Float runtime sizing/natural-all-in adapter;
- eventual defensive turn-call snapshot for exact busted-draw bluff provenance;
- whole-bot/OpenHoldem parser/replay certification.
