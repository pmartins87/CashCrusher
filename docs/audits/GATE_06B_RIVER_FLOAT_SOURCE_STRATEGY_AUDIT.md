# Gate 06B — River Float direct-source strategy audit

Status: **direct/high-ancestry source policy frozen; six-max professional gap policy not yet added**.

## 1. Source hierarchy

Crusher Framework 5 leaves `f$move_river_floatbet` empty, so it supplies no detailed hand policy for this node.

CrusherTBP supplies the manually reviewed River-Float value baseline:

- top non-board pair with at most four better kicker ranks, or overpair-or-better -> bet;
- a broad `3wBBvSB && BotCalledOnFlop && BotCalledOnTurn && Air -> River33` shortcut.

Mature DeepCrusher keeps the value baseline, makes it contribution-aware, and narrows the 3wBBvSB bluff to the actual source history rather than accepting the broad two-call shortcut.

## 2. General source value baseline implemented

After the corrected Gate06A River-Float parent is proven, CashCrusher implements:

- literal nuts -> 75%;
- 2P+ on super-completed River -> 50%, unless literal nuts;
- other 2P+ -> 75%;
- overpair -> 50%;
- top pair with `NumberOfBetterKickers <= 4` -> 50%;
- everything else -> check at the source layer.

`HaveNuts` is intentionally used as a conservative literal subset of the mature source `CF7_NutClass`. CashCrusher does not pretend that the two descriptors are byte-for-byte equivalent.

The TBP value rule was not HU-only, so this direct-source layer does not add an artificial HU restriction. Later cash/multiway professional review may still tighten a branch where appropriate; that would be P, not a silent rewrite of the source.

## 3. Exact 3wBBvSB source bluff

The mature source line is:

`BB called SB flop bet with the high-air/backdoor family -> Turn improved to a real draw -> BB called the 2Bar -> draw busts -> SB checks River`.

Current source action then reclassifies value first:

- 2P+/nut class -> 75%;
- OP/TP -> 50%;
- no-made busted draw -> 25%;
- residual -> check.

CashCrusher has the exact geometry owner, but the decisive turn-call semantic marker is still not written by the defensive Turn-Call node. Therefore the branch remains fail-closed by default through `user_cc_river_float_src_bbv_sb_turn_draw_called2bar`.

The older TBP shortcut `BotCalledOnFlop && BotCalledOnTurn && Air` is explicitly rejected as sufficient proof.

## 4. Negative source ownership

Mature DeepCrusher explicitly checks 3wBTNvSB no-made River Float. CashCrusher preserves that as a branch-level negative lock for the exact ordinary-SRP BTN-v-SB topology.

The HUSB missed-real-draw check is not separately promoted into a broad no-made lock because CashCrusher cannot yet prove the historical missed-draw class from the clean turn-call parent alone. The source layer already has no generic no-made bluff, so inventing a broader HUSB lock would add unsupported semantics.

## 5. Deep-stack / commitment boundary

Gate06B chooses only River bet/check and a strategic size ID. It contains:

- no `BetMax`;
- no `f$Raise_Committed`;
- no `f$hand_StackOffDraws`;
- no historical 50/55/60 near-all-in promotion;
- no `HandPower` or random tail.

A later runtime layer may convert a reviewed size to all-in only through separately audited stack geometry, exactly as in prior attack gates.

## 6. T / A / P / X

| Class | Gate06B use |
|---|---|
| **T** | current River evaluator/kicker/board facts and Gate06A executed turn-call ownership |
| **A** | TBP/DeepCrusher value ladder, exact 3wBBvSB branch, 3wBTNvSB negative lock |
| **P** | conservative `HaveNuts` translation and branch/coverage engineering only |
| **X** | generic two-call air shortcut, generic River-Float air bluff, HandPower/random tails, automatic stackoff |

## 7. Validation

The Gate06B source contract is covered by `tools/test_river_float_source.py` and joined the full regression workflow. The first complete Gate06B workflow pass was GitHub Actions run **#588**.

## 8. Next boundary

Gate06C should audit six-max cash gaps by pot/range family. It must not manufacture no-made bluffs from insufficient turn-call provenance. In particular, exact source histories waiting on future defensive snapshots stay locked rather than being filled by neighboring P policy.
