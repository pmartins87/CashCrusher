# Gate 02N — closed Turn action provenance for River routing

Status: **source/runtime boundary audited; implementation required before River CBet strategy**.

## Why this gate exists

A positive Turn-CBet strategy decision is only a **plan**. River strategy must consume what OpenHoldem actually executed after the turn betting round closed. CashCrusher therefore repeats the Gate01N repair one street later instead of allowing a pre-action flag to masquerade as executed turn aggression.

This distinction is especially important because Turn sizing can be affected by mechanical all-in equivalence and, eventually, by global sizing callbacks. A planned 75% barrel and a direct all-in are not interchangeable history facts.

## OpenHoldem runtime findings

Source audit of the project OpenHoldem repository establishes:

- betting rounds are preflop=1, flop=2, turn=3, river=4;
- `didchecround3`, `didcallround3`, `didraisround3`, `didbetsizeround3`, `didalliround3` read the autoplayer action counters for the turn;
- the implementation increments those counters, so values greater than 1 are meaningful for detecting multiple actions/re-aggression even though older symbol help text describes them as boolean-like "true if" symbols;
- successful betpot actions are explicitly registered as `k_autoplayer_function_betsize`;
- OpenPPL `RaiseBy X%` is evaluated into a numeric betsize and is executed through the betsize/swag path, so the current CashCrusher 25/40/62.5 adapters are also represented by `didbetsizeround3` when successfully executed;
- `BetMax` is registered as `k_autoplayer_function_allin`, therefore a direct all-in is represented by `didalliround3` rather than by a normal size marker;
- `lastraised3` is the stable previous-street final aggressor signal once the river is reached. OpenHoldem contains explicit previous-round repair logic that writes Hero as the prior last raiser when Hero's turn aggression closed the street and the new round begins.

These are T-level runtime facts. River routing must not infer them from `user_*` plan variables.

## Canonical histories to distinguish

Gate02N must classify at least:

1. standard executed Turn CBet: one normal betsize, no check/call/re-raise afterwards, Hero final turn aggressor;
2. direct Turn CBet all-in;
3. Turn CBet then Villain raise then Hero call;
4. Turn CBet then Hero re-aggression;
5. planned Turn CBet but actual check;
6. skipped Turn CBet with full check-through;
7. checked then called;
8. checked then aggressed;
9. plan expected natural all-in but execution remained sized;
10. plan expected sized bet but execution became direct all-in;
11. executed CBet without canonical plan capture.

Only case 1 is the normal `River CBet` parent. Raised-turn continuations and check histories belong to separate later nodes.

## Turn-state snapshot required before River

Several DeepCrusher river contracts depend on how Hero arrived at the river, not merely on current river hand strength. The current turn-only helpers are guarded by `IsTurn`, so those facts disappear on the river unless captured while the turn exists.

Gate02N therefore snapshots **provenance**, not future action:

- primary turn hand class: 2P+, overpair, top pair, lower pair, no-made;
- TP kicker band;
- premium/good/weak draw and air provenance;
- turn runout class (`super-completed`, newly completed, paired-flop-rank, glued overcard, other overcard, undercard, neutral);
- exact Turn-CBet family ID;
- whether the turn decision was HU or multiway;
- relative position FIRST/MIDDLE/LAST;
- exact canonical live-opponent mask at the turn decision.

Current river strength always supersedes the stored turn hand class. The snapshot only answers historical questions such as "was this a draw-origin second barrel?" or "did this river begin from a multiway turn that later reduced to HU?".

## OpenPPL safety contract

- flat complete `WHEN` rules only;
- every `f$cc_*` function carries nearby Source/Provenance documentation;
- `user_*` variables remain plan/provenance booleans and never prove execution;
- standard River-CBet parent requires closed round-3 runtime history;
- unsupported or contradictory history fails closed.

## Stack-depth contract

Gate02N does not create any new strategic all-in threshold. It only records whether the local Turn execution adapter expected a mechanically natural all-in and compares that plan with `didalliround3` after the street closes. Historical DeepCrusher ~50/55/60% commitment thresholds remain separate exact-node/global-callback audit material.
