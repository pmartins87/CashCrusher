# DeepCrusher re-review — nodes 39–45

Date: 2026-09-03
Branch: `deepcrusher-rereview-20260903`
Baseline SHA-256: `26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab`
Candidate B SHA-256: `137e7e32caf6831d288a25e70387b2113068ae6b09323365e5a3b8f62954cb89`

## Review rule

This pass looks for material poker/implementation defects, not cosmetic threshold literalism. Small margins such as 50/52 or 75/76 are preserved unless they cause a material unsupported action change.

Sources are reconciled jointly: Crusher written strategy, human-reviewed CrusherTBP, `user_hardcoded.cpp`, actual OpenPPL runtime flow, and professional poker theory for genuine gaps.

## Node status

| # | Node | Status in this pass | Notes |
|---|---|---|---|
| 39 | `f$move_flop_donkbet` | No material regression found | True-multiway positive tree remains source-scoped; Axx value check, low-pair non-completed donk, and draw texture split are not replaced by generic fallback. |
| 40 | `f$move_turn_donkbet` | No material regression found | Source-proven flop histories drive turn donk; current-value reclassification does not erase the recorded history. |
| 41 | `f$move_river_donkbet` | No material regression found in this pass | Scenario-specific HUBB / 3wSBvBB handling precedes residual generic river-donk article logic. Continue transversal helper audit later. |
| 42 | `f$move_turn_Probe` | No material regression found in this pass | Source-silent gaps are explicitly identified; exact source histories remain protected from residual TBP interpretation. |
| 43 | `f$move_river_Probe` | No material regression found in this pass | Scenario/history ownership remains explicit; no newly confirmed gross action inversion in this pass. |
| 44 | `f$move_turn_DelayedCB` | No material regression found in this pass | Ownership guards require no bet to call and actual flop initiative. Source/history subtrees terminate fail-closed. |
| 45 | `f$move_turn_Delayed_FloatBet` | **CONFIRMED MATERIAL PRECEDENCE BUG — FIXED IN CANDIDATE B** | Broad TBP residual returned TRUE for every non-3wBBvSB route before the detailed HUSB subtree, while an executable producer explicitly creates `user_DC12B_HUSB_FlopMediumMadeCheck`. The later HUSB strategy was therefore unreachable. |

“No material regression found” means no gross defect was confirmed during this pass; it is not a declaration that the node can never change. All seven nodes remain subject to the later transversal audit of shared helpers, history writers/readers, sizing and commitment.

## Confirmed node-45 defect

Baseline order:

```text
When f$game_3wBBvSB && uncovered_history Return true
When !f$game_3wBBvSB Return true
...
When f$game_HUSB Return false
...
When f$game_HUSB && user_DC12B_HUSB_FlopMediumMadeCheck && 2P+ -> Turn75
When f$game_HUSB && user_DC12B_HUSB_FlopMediumMadeCheck && TP/OP -> Turn50
When f$game_HUSB && user_DC12B_HUSB_FlopMediumMadeCheck -> check
```

The early `!f$game_3wBBvSB` line catches every HUSB state and exits TRUE. The blanket HUSB false immediately afterward is also unreachable for HUSB for the same reason. The detailed HUSB subtree cannot execute.

This is not a theoretical label disagreement. The file has a concrete flop writer:

```text
When AmountToCall = 0 && !user_Flop_Init_Hero && !f$flop_Raise &&
     f$game_HUSB && user_GotIsolated && f$CF7_MediumMade
Set user_DC12B_HUSB_FlopMediumMadeCheck
```

Therefore the code simultaneously creates the history and prevents its intended reader from acting.

CrusherTBP supplies a broad residual delayed-float rule, but that residual must not precede a more specific scenario history already deliberately modeled in DeepCrusher.

## Candidate B repair

Only the confirmed executable precedence defect was changed in node 45:

```text
When !f$game_3wBBvSB && !f$game_HUSB Return true Force
```

and the earlier blanket HUSB return-false was removed, allowing the existing detailed HUSB subtree to execute:

- HUSB medium-made flop check -> turn 2P+/nut class: `Turn75`, BET;
- HUSB medium-made flop check -> turn TP/OP: `Turn50`, BET;
- unchanged medium-made: CHECK.

The residual CrusherTBP rule remains active for otherwise-uncovered exact delayed-float routes. The 3wBBvSB source-specific tree is unchanged.

## Comment correction

The candidate also replaces 25 stale comments that claimed:

`user_hardcoded > Framework5 > CrusherTBP`

with the binding reconciliation policy: Crusher written strategy + human-reviewed CrusherTBP as primary anchors, `user_hardcoded` as secondary cross-check, professional theory for genuine gaps, and no blind source following.

This is comment-only; it does not change those 25 nodes' executable behavior.

## Regression validation

`test_deepcrusher_candidateB_rereview.py` passes 16/16 checks:

- frozen baseline SHA unchanged;
- candidate has a distinct SHA;
- same 1,283 OpenPPL block sequence;
- zero duplicate blocks;
- stale priority comment removed;
- HUSB excluded from generic 12B fallback;
- HUSB medium-made history producer exists;
- no blanket HUSB exit blocks the detailed reader;
- 2P+ -> Turn75 contract present;
- TP/OP -> Turn50 contract present;
- unchanged medium-made -> check contract present;
- executable delta limited to the confirmed node-45 repair;
- legacy delimiter imbalances preserved exactly relative to the frozen baseline.

This is static regression only. It is not OpenHoldem runtime certification and Candidate B is not promoted over the frozen good-results baseline yet.

## Next transversal pass

Next review target is not another numeric threshold sweep. It is the shared machinery capable of changing many already-reviewed nodes:

1. initiative/history writers and readers;
2. pot classifiers including SRP/ISO overlap;
3. `f$hand_slowplay` scope;
4. `f$Raise_Committed` call-to-jam conversion;
5. action-size router ownership and generic High/Over fallbacks;
6. current-hand-strength classifiers versus stale historical class;
7. dead/unreachable branches and comments that disagree with runtime behavior.