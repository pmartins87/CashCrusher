# Gate 11 — River Probe — Canonical Audit

Date: 2026-08-25  
Branch: `gate-00-context-engine`  
Final tested strategy/runtime checkpoint: `f48bd20ceaabeb1de9e5e0c7fbf938d0047cabc8`  
GitHub Actions: **#1124**, run id **32898499285**, **PASS**

## 1. Ownership

CashCrusher defines **River Probe** narrowly:

> Hero actually **checked and called exactly one flop bet** (`X/C`), the Turn then **checked through** (`X/X`), and Hero reaches the River in FIRST/MIDDLE position with `AmountToCall = 0` on Hero's first River action.

`CashCrusher_River_Probe_History.txt` proves the history from CLOSED OpenHoldem round counters and actor bits. It does not infer history from a pre-action plan marker.

The flop parent requires:

- one actual flop aggressor (`BitCount(raisbits2)=1`);
- valid/matching `lastraised2`;
- Hero exactly one flop check + one call;
- no Hero flop raise/bet/all-in;
- in HU, the current sole opponent must be that actual flop aggressor.

The Turn parent requires:

- exactly one Hero Turn check;
- zero Hero Turn call/raise/bet/all-in;
- `raisbits3 = 0`.

This separates River Probe from River Donk, River CBet, River Float and delayed/no-action River families.

## 2. Source hierarchy

The audit used the project source order rather than a generic poker fallback:

1. `DeepCrusher.txt` / mature reviewed scenario source;
2. `CrusherTBP.txt` where it fills or clarifies a source gap without contradicting mature source;
3. `Crusher Framework 5.txt` for routing/ownership architecture, not as strategy authority when its node is empty/generic;
4. professional six-max cash adaptation only after the direct/high-ancestry source domain is exhausted.

The Framework's generic River-Probe routing is therefore **not** allowed to manufacture a bet in an unreviewed family.

## 3. Direct/high-ancestry source children

### 3.1 Native 3w SB-v-BTN

A pre-action flop snapshot is only accepted later when CLOSED history proves that the flop actually became X/C. This preserves source candidates such as the historical non-best draw and high-air families without confusing intention with execution.

Resolved source/current-strength branches include robust current value and source missed-air descendants. Best flop draws that the mature source routes to X/R are explicitly excluded from the River-Probe X/C ancestry.

### 3.2 Native 3w BB-v-BTN

The source history markers are reconstructed as actual X/C parents rather than copied by seat label. Current River strength supersedes stale flop class where the mature source does so. Unsupported price/class provenance remains fail-closed.

### 3.3 Native 3w SB-v-BB

Limped and min-raise/opened origins remain separate. Source-dependent flop defense price/class evidence is required where the source needs it; the strategy does not guess a missing <=/> price bucket.

### 3.4 True native multiway

The source's blind-v-BTN+blind high-air line requires exact multiway ancestry and the source <=33%-pot flop-call provenance before it can own River strategy. A generic multiway check-call never inherits this child.

### 3.5 True-HU HUBB

Direct true-HU SRP and limped ancestry are separate from reduced-HU BvB adaptations. Current contribution-aware classes implement the mechanically safe source subset:

- robust trips/set+ value;
- exact contributed two pair;
- real TP/OP where source completion rules are translatable;
- second pair source branches;
- high-card/no-made air source bluff;
- explicit check states for weak pairs.

Source one-hole-card straight/flush and exact third-pair kicker ladders that are not mechanically equivalent to the current portable primitives remain visible translation gaps rather than being approximated silently.

## 4. Professional six-max fills

These families are provenance **P-heavy** and are deliberately more conservative than native Spin descendants.

### 4.1 Ordinary 4–6h SRP

Two exact histories are separated:

- blind caller versus PFA who actually made the flop bet;
- Hero PFA who checked flop and X/C'd the sole caller's stab.

Robust value can lead. One-pair thin value is restricted to clean non-paired/non-completed Rivers. A selected missed-draw bluff exists only in the BTN-open caller-v-PFA range where the pre-action flop draw snapshot plus CLOSED X/C proves provenance. No equivalent PFA-owned snapshot exists, so PFA-v-stab pure air remains check.

### 4.2 ISO

Original limper and post-raise coldcaller origins stay separate. The exact isolator must remain the relevant live opponent. Robust value leads; one-pair and bluff breadth tighten by range origin. No generic ISO-air probe is created.

### 4.3 Plain 3BP / squeeze

Opener-call, pre-squeeze coldcaller and post-3bet coldcaller origins remain separate. Caller-v-final-3bettor and initiative-v-caller-stab directions are distinct histories. The lower-SPR pot family does not authorize generic TP/OP stackoff or air pressure.

### 4.4 Clean HU 4BP

Only mechanically provable clean histories are covered:

1. Hero 3bet/call4 versus opener/final-4bettor;
2. standard opener4 versus original 3bettor survivor;
3. standard cold4 versus original opener survivor;
4. standard cold4 versus original 3bettor survivor.

Robust current value leads; contributed overpair may make a small thin-value lead only on a clean River; TP and air are explicit checks. Other-caller survivor, post-multiway, reversed/backraise/limp-reraise and unresolved call4 chronology remain fail-closed.

The 5bet+ diagnostic was deliberately built **outside** `f$cc_river_probe_base_opportunity`, because Gate11A intentionally supports only pot families 1–4. It reconstructs the same X/C-X/X/position-shaped history solely to expose unsupported 5bet+ states; it cannot route strategy.

## 5. Canonical router and coverage

`CashCrusher_River_Probe.txt` has eight top-level reviewed children. Direct/native children retain precedence over professional fills.

`f$cc_river_probe_child_owner_count` requires exactly one top-level owner for every covered state. `f$cc_river_probe_router_consistent` combines:

- closed-history consistency;
- child exclusivity;
- family-ID consistency;
- action/size consistency.

`f$cc_river_probe_uncovered_context` remains a first-class diagnostic. Unknown legal River-Probe states check rather than inheriting a neighboring family.

Provenance metadata currently uses:

- `1` = direct/high-source child;
- `3` = P-heavy six-max cash adaptation;
- `0` = uncovered.

## 6. Runtime sizing

Canonical Gate11 size IDs are:

| ID | Strategic size | Runtime action |
|---:|---:|---|
| 1 | MIN | `BetMin` |
| 2 | 25% | `RaiseBy 25%` |
| 3 | 33% | `BetThirdPot` |
| 4 | 50% | `BetHalfPot` |
| 5 | 75% | `BetThreeFourthPot` |
| 6 | 100% | `BetPot` |
| 7 | exact 30% | `RaiseBy 30%` |

The source-specific **30% River size is not rounded to 33%**.

For geometry, MIN is treated as the verified 1bb minimum bet and uses a non-fraction sentinel in the fraction mapper.

## 7. Stack geometry and all-in safety

The runtime geometry is valid only for a clean initial River bet:

- `AmountToCall = 0`;
- `currentbet = 0`;
- `potplayer = 0`;
- positive round-start pot and Hero stack.

Historical ~50/~60 commitment thresholds are diagnostic flags only.

`BetMax` is allowed solely as **natural/mechanical execution equivalence** when the already-selected River-Probe size itself reaches:

- Hero's full available stack; or
- the exact HU effective stack; or
- the deepest/all-live multiway effective relationship.

Reaching only the shallowest multiway opponent is a sidepot event and cannot promote the whole action to `BetMax`.

Plan markers record the strategy/runtime plan only. They do not prove that the table action occurred.

## 8. Explicit exclusions

Gate11 does **not** introduce:

- `HandPower` strategy;
- random frequencies;
- generic `BetMax` / `Raise_Committed` / stackoff rules;
- generic TP+ commitment;
- shortest-stack multiway all-in promotion;
- ordinary-SRP fallback into ISO/3BP/4BP;
- source seat-label inheritance without chronology/range proof;
- inferred flop X/C from a pre-action plan marker.

## 9. Validation

Final Gate11 deterministic/static suite in GitHub Actions **#1124** passed:

- global custom dependency/provenance lint;
- closed River-Probe history/native source subset;
- true-HU HUBB source tree;
- native BB-v-BTN;
- native SB-v-BB;
- native true-multiway;
- ordinary-SRP six-max adaptation;
- ISO adaptation;
- plain-3BP/squeeze adaptation;
- clean-HU 4BP adaptation;
- canonical coverage/exclusivity;
- runtime sizing/stack/all-in-equivalence.

Gate11 is therefore **complete at the static/deterministic policy layer for the supported chronology domain**.

It is **not table-certified**. Whole-bot composition and deterministic OpenHoldem parser/replay fixtures remain release gates.

## 10. Remaining River-Probe gaps

The deliberate gaps are:

- residual source-only straight/flush/kicker translations without certified portable equivalence;
- post-multiway SRP/ISO/3BP/4BP histories outside the native source child;
- unsupported/reversed/multiway 4BP ancestry;
- 5bet+;
- whole-bot `f$river` / `f$BestBetsize` composition;
- OpenHoldem parser/runtime replay certification.

The next attack family is **Gate12 — delayed/no-action**, beginning source-first with **12A Turn Delayed CBet**, while keeping 12B Turn Delayed Float and later River delayed/no-action histories separate.
