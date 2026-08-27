# Gate 05 — Turn Float audit

Status: **static/deterministic implementation complete; OpenHoldem replay certification pending**.

Validated CI baseline: GitHub Actions **run #568** (`32696523757`), green after the final runtime-test correction.

## 1. Canonical ownership

CashCrusher uses **Turn Float** only for a checked-to Turn where Villain owned the relevant previous aggression and Hero is now exact LAST/IP with no bet facing Hero. It is not a generic synonym for "bet Turn after any flop line".

The canonical history layer recognizes three closed-flop parents:

1. Hero called one clean flop bet from the actual final preflop aggressor, who then checks Turn;
2. Hero CBet flop, faced a later raise/XR, called, and the final flop aggressor checks Turn;
3. Hero Flop-Float bet, faced a later raise/XR, called, and the final flop aggressor checks Turn.

A narrow additional source repair reconstructs the explicit unraised `3wBBvSB` LP line:

`SB limp -> BB check -> SB bet flop -> BB call -> SB check Turn`.

The repair is deliberately local. It does not create a generic "called any flop bettor -> Float Turn" fallback.

## 2. Direct/high-ancestry source decisions

### 2.1 `3wBBvSB` Facing Bet -> call -> Turn check

Supported pot labels in the audited source are LP/SRP.

CashCrusher therefore preserves:

- current no-made **real draw -> Float 50%**;
- current no-made **air/high-card -> Float 50%**;
- source follow-up plan: broad `turn_Completed` -> barrel-river plan; otherwise give-up-river plan.

The broad source meaning of `turn_Completed` is retained. It is not silently narrowed to "the Turn card newly completed the board".

Provenance: **A** direct/high-ancestry source transplant over **T** exact history/runtime facts.

### 2.2 BTN Advanced: CBet -> XR/raise -> call -> Turn check

The source explicitly gives a small Float interval to AIR/A-high-like misses after the called-XR history. CashCrusher uses **33%**, inside the audited 25–40% interval.

Important negative boundary: a still-live FD/OESD/Gutshot+ does **not** inherit that AIR instruction. Existing real draw remains a locked check in this source branch.

The current DeepCrusher residual made-improvement branch uses **50%** after the explicit AIR/live-draw cases are removed. CashCrusher keeps that as **A**, not as primary-source-exact text.

### 2.3 `3wBTNvSB` no-made lock

The source's unusually conservative BTN-v-SB philosophy is retained as an explicit negative owner. A valid BTN-v-SB no-made Turn-Float state cannot be overwritten later by a generic professional-theory bluff fallback.

Provenance: **A** negative source rule + **T** exact opponent/history identity.

## 3. Branch-level source coverage

A matchup having source ancestry does not mean every current hand class is source-covered.

CashCrusher therefore distinguishes:

- exact source positive branch;
- exact source locked check;
- same matchup/history but current hand class still unresolved by source.

This prevents a broad source-context flag from silently blocking legitimate six-max gap work or, conversely, letting a P rule overwrite an exact source check.

## 4. Six-max professional gap policy

Where direct source is silent, the implementation is explicitly **P-heavy** and keeps history/range families separate.

### Ordinary SRP

Separate owners exist for:

- simple flop-call -> missed second barrel;
- CBet -> XR -> call;
- Flop Float -> XR -> call;
- flop-multiway -> Turn-HU;
- current Turn still multiway.

The XR-call parents are treated as progressively more selected than a simple flop-call parent. Pure-air stabbing is correspondingly reduced or removed.

### Isolation pots

Original limper and post-raise coldcaller provenance remain distinct. True-HU limp-raised ancestry is also a separate owner rather than being folded into ordinary multi-handed ISO.

### Plain 3BP and squeeze

Plain 3BP and squeeze remain separate. Caller origin is preserved as:

- opener-call;
- pre-3bet coldcaller;
- post-3bet coldcaller.

Coldcaller descendants are not given the same arbitrary air pressure as ordinary opener-call ranges.

### Clean supported 4BP

Only reconstructable clean HU 4BP parents receive policy. Unsupported/reversed/backraise/limp-reraise chronology does not borrow a nearby 4BP child.

### Multiway

Current-multiway Turn Float is substantially tighter than HU. At 4+ players, positive no-made action is effectively restricted to the strongest reviewed combo-draw class; pure air is absent.

Flop-multiway -> Turn-HU remains a post-multiway range origin and does not retroactively become a clean HU hand.

## 5. Deep-stack value/commitment boundary

Gate05 does **not** recreate the old DeepCrusher `TP+ -> stackoff` behavior.

Key protections:

- top pair and overpair are one-pair classes, not global stack-off classes;
- even 2P+ is re-evaluated against completed/dynamic Turn topology;
- low SPR can affect an exact strategy branch, but never acts as a standalone commitment command;
- no Gate05 strategy file uses `f$Raise_Committed` or `f$hand_StackOffDraws`;
- no strategic Gate05 policy branch directly issues `BetMax`.

`BetMax` exists only in the local natural/mechanical all-in-equivalence adapter after a reviewed strategic size is already selected.

## 6. Runtime sizing and all-in equivalence

Turn Float strategic palette:

| Size ID | Intended pot fraction | OpenPPL runtime action |
|---:|---:|---|
| 1 | 25% | `RaiseBy 25%` |
| 2 | ~33% | `BetThirdPot` |
| 3 | 50% | `BetHalfPot` |
| 4 | 75% | `BetThreeFourthPot` |
| 5 | 100% | `BetPot` |

Natural/mechanical `BetMax` is allowed only when the already selected size reaches:

- Hero's remaining stack;
- the exact HU effective stack; or
- in multiway, the deepest/all-live effective relationship.

Reaching only the shallowest sidepot relationship is explicitly insufficient to promote the whole action to `BetMax`.

Historical 50/55/60% near-all-in behavior remains diagnostic evidence only. It is not a generic CashCrusher shove rule.

## 7. Closed Turn-Float action history

Pre-action plan markers do not prove execution.

The closed Turn layer reconstructs and validates:

- opportunity snapshot and exact parent/family;
- actual initial Turn-Float bet;
- actual check-back;
- direct all-in versus ordinary sized execution;
- Float -> later raise -> Hero call;
- Float -> Hero re-aggression;
- final aggressor identity;
- plan-v-runtime mismatch;
- source give-up-river versus barrel-river plan only after a valid executed Float parent is proven.

This creates the safe parent `f$cc_hist_river_float_standard_parent_valid` for Gate06 River Float.

## 8. T / A / P / X classification

| Classification | Gate05 use |
|---|---|
| **T** | OpenHoldem/OpenPPL persisted action facts, exact player/chair/live-mask/history/stack geometry |
| **A** | direct/high-ancestry DeepCrusher Turn-Float descendants, source negative locks, repaired explicit LP history |
| **P** | six-max SRP/ISO/3BP/squeeze/4BP gap policies, branch exclusivity, deterministic sizing selection where source is silent |
| **X** | generic HandPower/random tails, generic `TP+ -> stackoff`, generic 50/55/60 near-all-in promotion, borrowing ordinary SRP policy into unresolved pot families |

## 9. Validation result

GitHub Actions run **#568** passed the full combined suite through the new Gate05 tests:

- global dependency / flat-WHEN / provenance / safety lint;
- all existing Flop/Turn/River CBet regression tests;
- all Flop Float regression tests;
- final-aggressor chronology repair;
- Gate05A Turn-Float history/opportunity;
- Gate05B direct-source strategy;
- Gate05C-F coverage/provenance/fail-closed policy;
- Gate05 runtime sizing + natural all-in equivalence;
- closed Turn-Float action-history + River-parent contract.

The final runtime-test change only made the assertion ignore `//` comments when checking that the executable all-live-effective branch never uses `shallowest`. Strategy code did not change.

## 10. Remaining unsupported/release boundaries

Gate05 is complete only at the **static/deterministic strategy layer**. It is not table-certified yet.

Still fail-closed / pending outside this Gate05 policy baseline:

- unsupported multiway 4BP ancestry inherited from earlier gates;
- reversed/backraise/limp-reraise 4BP chronology without stronger evidence;
- 5bet+ postflop families;
- whole-bot `f$turn` / `f$BestBetsize` composition;
- deterministic OpenHoldem parser/replay certification.

The next attack gate may consume only the closed executed Turn-Float history, never pre-action intent alone.