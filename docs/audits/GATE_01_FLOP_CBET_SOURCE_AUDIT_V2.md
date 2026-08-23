# Gate 01 — Flop CBet source audit v2

Status: **ordinary-SRP HU baseline implemented; other pot families remain fail-closed**.

This document supersedes the handedness assumptions in `GATE_01_FLOP_CBET_SOURCE_AUDIT.md`. The older audit remains useful historically, but its statement that HUSB has no literal CashCrusher range match is no longer correct after Gate 00F.

## 1. Critical correction: true HU exists inside a six-max cash product

A six-max table can be dealt 2h after players leave or sit out. A genuine two-player deal is strategically different from a 3-6h hand that becomes heads-up after folds.

CashCrusher therefore distinguishes:

- **TRUE HU DEAL** — exactly two players dealt; SB is also Button and acts IP postflop;
- **PREFLOP-REDUCED HU** — 3-6 players dealt, exactly two reach flop;
- **POSTFLOP-REDUCED HU** — 3+ reached flop and later action reduces the hand to two players.

This changes source ancestry materially:

- true-HU SB/Button PFA IP vs BB has **HUSB as its direct legacy parent**;
- six-max SB PFA OOP vs BB after four preflop folds has **3wSBvBB as its parent**;
- both can encode numeric matchup `56`, so matchup ID alone is insufficient.

## 2. Provenance framework

- **T** — direct transplant.
- **A** — source principle retained with cash/deep-stack adaptation.
- **P** — professional-theory construction where source is missing or format-dependent.
- **X** — rejected literal Spin/shallow-stack rule.

Exact solver frequencies are **not** being invented. P rules are deterministic professional baselines intended for later empirical/runtime validation.

## 3. Source audit by direct parent

### 3.1 HUSB → true-HU SB/Button PFA IP vs BB

The audited DeepCrusher source is unusually explicit:

- TP+ is a broad CBet family;
- MP/BP is also bet broadly in the readless source;
- real GS/OESD/FD is a betting family;
- air checks on straight-possible flops;
- residual air is otherwise bet broadly;
- a narrow old A/K-high weak-TP slowplay is tied to shallow effective stack;
- profile-dependent Green/Red/PT rules are exploit overrides, not readless baseline.

Cash classification:

| Source concept | CashCrusher |
|---|---|
| true HU positional/range parent | **T/A, highest ancestry confidence** |
| TP+ value pressure | **A** |
| second/lower-pair broad CBet | **A**, reduced at high SPR/dynamic boards |
| frontdoor draw aggression | **A** |
| straight-possible air check | **A** |
| blanket residual-air CBet | **X literal**, replaced by P combo selection |
| `<=16BB` TP slowplay | **X** |
| profile overrides | deferred exploit layer |
| 40/50/75 exact size ladder | **A**, mapped into deep-stack size families |

### 3.2 3wBTNvBB → 3-6h PFA IP versus BB

Direct descendant: BTN-v-BB.

Structural descendants: UTG/HJ/CO-v-BB with absolute matchup retained.

Source lessons:

- under-CBetting is explicitly identified as a mistake;
- TP+ bets smaller on dry boards and larger on wet/dynamic boards;
- very-dry weak TP can check;
- high second pair can check dry boards;
- lower pair classes receive protection bets;
- no-made hands are bet very broadly in the Spin source.

Cash classification:

- BTN-v-BB architecture/range shape: **A, high confidence**;
- earlier opener-v-BB: **A + P**;
- dry-small / dynamic-larger sizing idea: **A**;
- source blanket no-made tail: **X literal**, replaced by backdoor/draw/board selection;
- exact 30/50 frequencies: **A**, not solver truth for cash.

### 3.3 3wBTNvSB → 3-6h PFA IP versus SB

Source protects checking range much more than vBB:

- strong value bets, larger on wet structures;
- MP/BP frequently checks;
- source uses a shallow `StackOffDraws` class;
- no-made betting is concentrated in narrower high-card structures.

Cash classification:

- BTN-v-SB direct ancestry: **A, high confidence**;
- earlier opener-v-SB: **A + P**;
- stronger/more condensed SB continue-range caution: **P/A**;
- `StackOffDraws`: **X**;
- strong-draw aggression as a concept: **A**;
- marginal pairs protecting check-back range: **A/P**.

### 3.4 3wSBvBB → 3-6h SB PFA OOP versus BB

This is the cleanest direct OOP source parent.

Audited source behavior:

- paired-board TP subtrees;
- TP+ bets selected A-high / two-broadway / non-straight families;
- many lower/connected TP+ boards skip CBet into X/R plans;
- MP/BP main plan is check;
- in raised pots good draws can X/R and medium/weak draws X/C;
- air checks straight-possible boards;
- source residual air CBet is very broad elsewhere.

Cash classification:

- OOP check-range architecture: **A, high confidence**;
- TP board-dependent bet versus X/R split: **A**;
- MP/BP check: **A**;
- raised-pot draw check into future X/R/X/C: **A**;
- literal all-nonstraight-air bet: **X**;
- limped-pot branch: out of ordinary-SRP CBet scope.

### 3.5 3wSBvBTN as positional skeleton for opener OOP vs later cold caller

Six-max creates important ranges that Spin does not contain directly:

- UTG-v-HJ/CO/BTN;
- HJ-v-CO/BTN;
- CO-v-BTN.

The old `3wSBvBTN` name supplies only OOP-vs-later-position geometry. Its range policy is not a valid copy.

Cash classification:

- position/history routing: **A**;
- range frequencies: **P**;
- sizing: **P/A**;
- shallow commitment rules: **X**.

This is currently the most theory-heavy ordinary-SRP CBet family.

## 4. Professional deep-stack fill used in Gate 01B/01C

These are broad professional NLHE principles, not claimed exact GTO frequencies.

### 4.1 Board-range interaction precedes nominal hand class

CashCrusher first distinguishes static high, dynamic high, static low/mid, dynamic low/mid, and paired structures. Exact texture remains available under the coarse parent.

A hand called `top pair` does not receive one universal action across `A72r` and `987ss`.

### 4.2 Static high boards

Where the PFA retains meaningful range advantage and the caller has fewer two-pair/straight combinations:

- small CBet is a useful wide-range tool IP;
- OOP can still use small range-pressure bets, but checks more;
- selected air is chosen through backdoors/high-card structure rather than betting every combo.

### 4.3 Dynamic low/mid boards

Caller ranges contain more two-pair/straight/pair+draw density and realize equity well.

Baseline response:

- lower CBet frequency;
- stronger check range;
- polar/stronger betting range;
- larger sizing for very strong value/premium draws when betting;
- marginal one-pair and pure air check much more often.

### 4.4 IP versus BB compared with IP versus SB

BB defend ranges are wider and contain more weak hands; SB cold-call ranges are generally more condensed/stronger and are highly rake/site dependent.

Therefore the baseline vSB tree deliberately:

- checks more marginal pair SDV;
- requires stronger air selection;
- does not inherit the vBB static-low bluff extension.

This is **P**, not a claim that every site's SB flat range is identical.

### 4.5 OOP PFA

OOP strategy checks materially more because Villain controls position later and Hero must defend a check range.

The implementation therefore keeps:

- MP/BP mostly in check;
- many no-made draws in check so future X/R/X/C nodes can own them;
- dynamic-low TP in check more often at high SPR;
- static-high selected air as the narrow baseline bluff family.

### 4.6 Deep-stack draw classification

`StackOffDraws` is removed. CashCrusher distinguishes:

- premium: combo draw, nut FD, OESD+2OC, FD+2OC;
- good: other FD/OESD, GS+2OC;
- weak: remaining frontdoor draw.

Final aggression still depends on position, board and SPR.

## 5. Deterministic selection instead of fake exact mixing

Many professional/solver strategies mix. OpenPPL hardcoding should not silently convert a 35% mix into `always bet`.

Current baseline approximates mixing using combo quality:

- frontdoor draw tier;
- backdoor FD/SD;
- two overcards;
- broadway/high-card blockers;
- top-pair kicker tier;
- raw SPR.

This creates strategically meaningful betting/checking subsets without pretending to know an exact random frequency.

Randomization remains a future option only if runtime behavior is validated and a strategically meaningful deterministic split is insufficient.

## 6. Sizing baseline

Current strategic size IDs:

- `1` — small, approximately one-third pot;
- `2` — medium, approximately half pot;
- `3` — large, approximately three-quarter pot;
- `4` — pot, reserved and unused by ordinary-SRP baseline.

Broad map:

- static high / paired -> small often;
- dynamic high -> medium;
- static low/mid -> small for protection/bluff, medium for stronger value/draws;
- dynamic low/mid -> medium/large, and only with a much stronger betting range.

No size is automatically converted to all-in. Global betsize-to-all-in conversion remains disabled.

## 7. Implemented ordinary-SRP coverage

### TRUE HU

Implemented:

- SB/Button PFA IP vs BB, ordinary open-raised SRP.

Not yet implemented:

- BB PFA OOP after SB limp/BB raise;
- true-HU 3BP;
- true-HU 4BP.

### 3-6h deals reduced to HU preflop

Implemented:

- UTG/HJ/CO/BTN PFA IP vs BB;
- UTG/HJ/CO/BTN PFA IP vs SB when positionally possible;
- SB PFA OOP vs BB;
- UTG/HJ/CO PFA OOP vs later-position cold caller.

Still separate/uncovered:

- ISO;
- 3BP;
- squeeze;
- 4BP.

### Multiway

All CBet children still fail closed. Multiway requires its own Gate because bluff/value thresholds change materially with each additional live range.

## 8. Important limitation

The current policies are a carefully sourced **baseline**, not a completed CashCrusher release.

They still need:

1. OpenPPL parser validation;
2. synthetic/replay context validation;
3. betsize-runtime wiring;
4. check/XR/XC defense nodes so skipped CBets have complete follow-through;
5. cross-street Turn/River plan integration;
6. later empirical refinement.

Until those gates pass, branch code is development code and must not be treated as table-ready.
