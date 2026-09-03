# DeepCrusher transversal audit 01 — shared helper scope and precedence

Date: 2026-09-03
Baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`
Candidate B SHA-256 after this pass: `786c4519b1790c871b51b1bd34201bcf09b2b174811672fa1e8621787930afe9`

## Finding T01 — global `f$hand_slowplay` scope leak

**Status: CONFIRMED MATERIAL SCOPE BUG — fixed in Candidate B.**

The frozen baseline contains:

```text
When IsFlop && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force
// ... 3wBTNvBB CF Q2 TP On dry structures - CALL and let your opponent remain with his bluffs
```

The rule is global in executable scope but its own provenance comment identifies a specific `3wBTNvBB` top-pair line. CrusherTBP contains the same globalized condition. The independent C++ implementation places the dry-call behavior inside the `3wBTNvBB` state machine: after Hero's flop c-bet is raised, a dry/non-wet TP line calls; wet TPGK+ may re-raise.

This matters because `f$hand_slowplay` is not a local flag. It is consumed by many Raise-vs-* families as an early `Return false`, so globalizing a scenario-specific top-pair slowplay can suppress aggression in unrelated CBet/Donk/Bet/Raise contexts.

### Candidate B repair

The condition is now explicitly source-scoped:

```text
When IsFlop && f$game_3wBTNvBB && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force
// SOURCE: RECONCILED 3wBTNvBB CF Q2 TP...
```

The separate `3wBBvSB` dry TP slowplay rule remains unchanged and continues to own that scenario. Other scenarios are no longer blocked by this 3wBTNvBB-derived helper and must be decided by their own strategic nodes.

## Why this is materially different from a 1–3pp threshold margin

This change does not literalize a sizing number. It restores scenario scope. Before the fix, a boolean helper could reverse RAISE to non-raise across unrelated game trees. That is a material semantic leak.

## Candidate B executable delta so far

Relative to the frozen good-results baseline, Candidate B has only two confirmed executable repairs:

1. `f$move_turn_Delayed_FloatBet`: HUSB excluded from the early generic TBP residual so its explicit medium-made history subtree is reachable; the earlier blanket HUSB exit is removed.
2. `f$hand_slowplay`: dry TP slowplay scoped to `f$game_3wBTNvBB` instead of global flop scope.

The remaining changes are comments correcting source-policy/provenance statements.

## Static regression

`test_deepcrusher_candidateB_rereview.py` passes **18/18** checks, including:

- frozen baseline hash;
- exact block sequence preservation;
- no duplicate blocks;
- tightly bounded executable diff;
- HUSB delayed-float producer/reader reachability contracts;
- global dry-TP slowplay removed;
- source-scoped 3wBTNvBB dry-TP slowplay present;
- legacy delimiter imbalance preserved relative to baseline.

Candidate B remains unpromoted pending further shared-helper audit and eventual OpenHoldem runtime testing.