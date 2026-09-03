# DeepCrusher transversal audit 02 — Facing-Bet ownership, commitment and microbet precedence

Date: 2026-09-03  
Branch: `deepcrusher-rereview-20260903`  
Frozen good-results baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`  
Candidate C SHA-256: `f515956f24d28ef804ea7802ece989b4d316fd8116b15462d99c58c930297a7e`

## Review standard

This pass follows `docs/deepcrusher/SOURCE_POLICY.md`.

Small implementation margins are not treated as defects. In particular, the existing ~52% low-bet boundary and ~76% normal/high boundary are preserved. The target is material action ownership: CALL becoming JAM, source-specific CONTINUE becoming FOLD, source-specific RAISE becoming generic CALL/FOLD, or a helper bypassing a source restriction.

Runtime semantics are traced rather than inferred from names. A 3wBBvSB `SB limp -> Hero BB raise -> SB call` can be classified by the runtime as `f$pot_SingleRaised`; therefore the written `LP/SRP` Facing-Bet rule is not excluded merely because the preflop action was an isolation over a limp.

## Sources reconciled

### 3wBBvSB — TP+ Facing Bet

Crusher Starting Strategy (`8- CRUSHFEST - 3wBBvSB - ok25 (Review with NCF).docx`):

- TP or better, Q3 Facing Bet (LP/SRP):
  - wet -> raise with 50% sizing;
  - dry -> call only versus 50%+ sizing.
- Q4 continuation:
  - second barrel 50% non-completed;
  - 75% completed;
  - top pair lowers the third-barrel size to 25%.

`user_hardcoded.cpp` independently implements the same principal split. On dry bets below the written call threshold it explicitly fills the source gap with a 50% value raise. That completion is not mislabeled as literal Starting Strategy in Candidate C.

### 3wBTNvBB — TP+ versus flop DB/Facing Bet

Crusher Starting Strategy (`3- CRUSHFEST 3wBTNvBB.docx`):

- ~0–75%: dry+ -> call; wet -> raise and barrel;
- ~75–150%: non-CPL -> call; CPL -> raise and barrel;
- >150%: non-CPL -> call; CPL -> call only with additional equity;
- flop raise target: one-third of the stack, to create sub-1:1 SPR on turn;
- after flop raise:
  - SPR <~1.3 with no good additional equity -> all-in;
  - SPR <~1.3 with good additional equity -> 40%;
  - SPR >~1.3 -> 75%.

`user_hardcoded.cpp` reproduces this action tree and one-third-stack flop raise target. Its discrete action model approximates the source 40% with 33%; DeepCrusher already supports an exact `user_Turn40`, so Candidate C uses the source 40% rather than preserving the C++ approximation.

### 3wBBvSB — high-card/backdoor source restriction

Starting Strategy Q4 says that in single-raised pots / wet flops, A/K-high/backdoor/air continues up to ~50% only with the specified good/medium backdoor classes. `user_hardcoded.cpp` similarly requires top BDFD / weak BDFD+2mOC / BDSD+2mOC; otherwise it folds.

The generic `f$Call_MicroBets` could previously call pure A-high/K-high air solely because the bet was tiny. Candidate C adds a source-scoped fail-closed guard before that helper.

## Confirmed material defects repaired

### 1. `f$Raise_Committed` could rewrite explicit flop CALLs into JAM

`f$Raise_Committed` is evaluated before ordinary flop routing and promotes a call to a raise/all-in when the call consumes >55% of Hero's stack or when Villain is sufficiently committed.

This conflicts with explicit source CALL branches, especially large-bet branches such as:

- 3wBBvSB dry TP/OP versus non-low initial bet;
- 3wBTNvBB dry TP/OP in normal sizing;
- 3wBTNvBB non-CPL TP/OP through ~150% and above 150%;
- 3wBTNvBB >150% completed TP/OP with additional equity.

Candidate C installs scenario-specific action-ownership guards *before* `f$Raise_Committed`. The helper is not deleted globally; it remains available in contexts where the project has not established a conflicting source action.

### 2. Generic High/Over routing could erase 3wBTNvBB TP/OP source tree

Candidate C routes the explicit 3wBTNvBB one-pair Facing-Bet tree before generic Normal/High/Over fallbacks. It deliberately keeps the project's ~76 threshold as the operational representation of the source's ~75 boundary.

The change is limited to real current top pair / overpair. Two-pair+ is not globally rewritten in this pass because those stronger classes require a separate scenario review rather than assuming the one-pair reconciliation is automatically optimal for every completed overbet board.

### 3. `f$Call_MicroBets` could bypass 3wBBvSB pure-air folds

A source-scoped false guard now runs before the microbet helper for 3wBBvSB SRP wet flop air with no real draw and without Good/Medium backdoors.

### 4. Turn `f$Raise_Committed` could rewrite explicit draw CALLs into JAM

The already source-encoded 3wBBvSB high-air/backdoor line says, after improvement to a draw on turn:

- GS: call through the ~50% bucket;
- OESD/FD: call through the ~75% bucket.

Those calls were present in `f$turn_Call` but did not have paired guards before turn `f$Raise_Committed`. Candidate C adds the missing false guards to `f$turn_Raise`, preserving CALL ownership.

### 5. Previously confirmed scope/precedence repairs carried into Candidate C

Candidate C also retains:

- `f$hand_slowplay`: the dry-rainbow TP line explicitly sourced from 3wBTNvBB is scoped to `f$game_3wBTNvBB` instead of leaking globally;
- `f$move_turn_Delayed_FloatBet`: generic non-3wBBvSB fallback excludes HUSB so the detailed `user_DC12B_HUSB_FlopMediumMadeCheck` subtree is reachable;
- 25 stale comments claiming `user_hardcoded > Framework > CrusherTBP` are replaced by the binding reconciliation policy.

## Cross-street preservation added

### 3wBBvSB TP/OP Facing-Bet line

Candidate C captures the actual flop Facing-Bet history and preserves the source continuation whether the flop action was CALL or RAISE:

- checked-to turn, non-CPL -> 50%;
- checked-to turn, CPL -> 75%;
- after that actual turn barrel, if river checks to Hero and current hand remains TP/OP -> 25%.

Stronger river improvements are intentionally left to existing stronger-value logic rather than forcibly downsized to 25%.

### 3wBTNvBB TP/OP flop raise line

A dedicated state controls the source one-third-stack flop raise. The sizing rule is additionally gated by the initial-bet buckets so the state cannot leak into a later same-flop re-raise decision.

On a checked turn:

- SPR >1.3 -> 75%;
- SPR <=1.3 + OESD/FD -> 40%;
- SPR <=1.3 without that additional equity -> all-in.

## Why the global commitment helper was not deleted

CrusherTBP/Framework contains the 55% commitment helper and the current good-results baseline has practical evidence in its favor. The defect is not proven to be the helper's existence; the confirmed defect is its precedence over explicit source CALLs.

Candidate C therefore uses the lower-risk architecture already present elsewhere in DeepCrusher: source-specific guards execute first, generic commitment remains fallback.

## Static regression

`tests/deepcrusher/test_candidateC_transversal.py` passes **40/40** checks.

It verifies:

- frozen baseline SHA unchanged;
- Candidate C has a distinct SHA;
- identical 1,283 OpenPPL block sequence;
- no duplicate blocks;
- no new executable `f$` references;
- no literal builder-template residue;
- source-specific CALL/FOLD guards precede `f$Raise_Committed` and `f$Call_MicroBets`;
- one-third-stack and 50%-raise sizing are scoped to the initial Facing-Bet action;
- turn/river source continuations exist;
- explicit turn draw calls precede turn `f$Raise_Committed`;
- delayed-float HUSB detailed subtree is reachable;
- delimiter imbalances are unchanged relative to the frozen baseline;
- executable delta is restricted to exactly ten reviewed blocks:
  - `f$flop_Raise`
  - `f$flop_Call`
  - `f$turn_Raise`
  - `f$move_turn_cbet`
  - `f$move_turn_floatbet`
  - `f$move_river_cbet`
  - `f$move_turn_Delayed_FloatBet`
  - `f$BetsizeFlopHeadsup`
  - `f$BetsizeFlopMultiway`
  - `f$hand_slowplay`

This is static regression, not OpenHoldem runtime certification. Candidate C is **not promoted** over the frozen good-results baseline.

## Still open — do not silently change yet

1. The remaining global `f$hand_slowplay` rules for dry two-pair+/straight+ have wide reach across CBet/Donk/Float/Bet/Raise families. Their global scope is strategically suspicious but not yet sufficiently reconciled scenario-by-scenario to modify safely.
2. Turn/River source-specific CALLs deeper inside the scenario routers still need the same commitment-precedence audit. Only confirmed explicit conflicts are changed.
3. Current-strength versus historical-strength reclassification requires another transversal pass; stale history must not force an action after the hand materially changes class.
4. Two-pair+ versus extreme completed flop bets remains separate from the one-pair repair above.
5. Candidate C still needs OpenHoldem parser/runtime validation before any live replacement decision.

## Reproduction artifacts

- `patches/DeepCrusher_CandidateC_Transversal_20260903.patch` — unified diff from frozen baseline.
- `tools/deepcrusher/build_candidateC_transversal.py` — deterministic local builder.
- `tests/deepcrusher/test_candidateC_transversal.py` — static regression suite.
