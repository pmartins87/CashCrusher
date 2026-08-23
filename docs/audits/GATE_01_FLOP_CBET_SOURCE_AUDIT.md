# Gate 01 — Flop CBet source audit for CashCrusher

Status: **SOURCE AUDIT COMPLETE; policy implementation deliberately separated from routing**.

## Scope

This gate audits `DeepCrusher::f$move_flop_cbet` as a source of knowledge for six-max cash. It does not assume that a branch named `3wBTNvBB`, `HUSB`, etc. can be copied to a new absolute position.

CashCrusher defines a flop CBet narrowly as:

> Hero was the final preflop aggressor in a raised pot, reaches the flop with initiative, and faces no flop bet before acting.

A bet in an unraised/limped pot is not called a CBet in CashCrusher even though legacy Crusher sometimes routes a limped-pot "LCBet" through the same move function. ISO CBet, ordinary SRP CBet, 3BP CBet and squeeze-pot CBet remain separate subfamilies.

## Provenance legend

- **T** — direct transplant is strategically and mechanically safe.
- **A** — source principle is useful but ranges, sizes, stack geometry or scope must change.
- **P** — six-max gap must be filled with professional NLHE theory.
- **X** — reject the inherited rule as Spin/shallow-stack or context-specific.

A single source line may contain both A and X components. Example: "bet strong value more on dynamic boards" can be A while "jam because effective stack is <=20 BB" is X.

---

## 1. What is genuinely reusable from the legacy CBet architecture

### T — routing separation, not frequencies

The mature DeepCrusher architecture correctly separates:

- Hero initiative versus Villain initiative;
- action when checked to versus facing a bet;
- ordinary raised pots, limped pots and raised/isolated histories;
- later response when Hero's CBet is raised;
- cross-street provenance bits that remember which flop family created the turn/river state.

CashCrusher should preserve this *shape*. The actual six-max ranges and thresholds are not T simply because the routing is.

### A — board/hand interaction concepts

Across several legacy branches the same professional concepts recur:

- stronger/dynamic boards can justify larger value sizing;
- showdown-value middle/weak pairs are often checked more than top pair+;
- connected boards reduce indiscriminate air betting;
- strong draws can be aggressive while weak draws often prefer realization;
- IP and OOP branches should not share a single policy;
- paired/static boards and highly dynamic boards create different continuation plans.

These are useful A-principles, but exact old percentages and stack thresholds are not automatically preserved.

---

## 2. Legacy branch audit

### 2.1 `3wBTNvBB` — strongest ancestor for BTN PFA IP versus BB

**Six-max descendants:**

- direct: BTN open → BB call;
- structural only: CO/HJ/UTG open → BB call.

**Source behavior:**

- source explicitly warns against under-CBetting;
- dry TP+ uses a small CBet, wet TP+ uses a larger CBet;
- very-dry weak top pair can check;
- high second pair on dry boards can check;
- lower pair classes often use a small CBet;
- no-made hands are bet very broadly, with board-class-specific 30/50 sizing and cross-street plans.

**Classification:**

- BTN-v-BB parent architecture: **A, high confidence**;
- exact 30/50 frequencies/sizes: **A**, not T;
- "bet every residual no-made hand" as a universal deep-cash rule: **X as literal rule**, replaced by range/board-aware P logic;
- cross-street plan states: **A**, to be revisited in Turn/River gates.

**Why not T:** deeper stacks alter raise pressure and future-street EV; conventional cash BTN and BB ranges are related to but not identical with the shallow Spin ranges.

### 2.2 `3wBTNvSB` — strongest ancestor for BTN PFA IP versus SB

**Six-max descendants:**

- direct: BTN open → SB call;
- structural: CO/HJ/UTG open → SB call.

**Source behavior:**

- strong value bets, with larger sizing on wetter structures;
- many MP/BP hands protect checking range;
- dedicated "stack-off draw" betting family;
- no-made betting concentrated on A/K + low-card structures.

**Classification:**

- positional/range-shape parent for BTN-v-SB: **A, high confidence**;
- "stack-off draw" class defined by Spin thresholds: **X**;
- strong-draw aggression as a concept: **A**;
- A/K-high range-pressure concept: **A/P**;
- exact 50/60 sizes: **A**.

CashCrusher will reclassify draws by nut potential, equity quality, overcards/blockers, position and raw SPR instead of importing `f$hand_StackOffDraws` as an automatic cash stack-off category.

### 2.3 `3wSBvBB` — strongest ancestor for SB PFA OOP versus BB

**Six-max descendant:**

- direct: SB raise → BB call.

**Source behavior:**

- substantial checking even with made hands;
- paired-board subtrees;
- TP+ bets some A-high / two-broadway / non-straight families;
- TP+ checks to X/R on lower/connected structures;
- MP/BP mostly checks;
- in raised pots good draws can X/R while medium/weak draws X/C;
- air checks on straight-possible boards and bets more freely elsewhere.

**Classification:**

- OOP parent architecture: **A, high confidence**;
- protecting the OOP check range: **A**;
- board-dependent value betting versus X/R: **A**;
- exact draw tiers and raise thresholds: **A/P**;
- literal "all air except straight-possible" CBet rule: **X as universal deep-cash rule**;
- limped-pot branches inside the same source function: **X for CBet scope** and moved to future limped-pot attack node.

This source is especially valuable because it already recognizes a core deep-cash principle: OOP aggressor strategy cannot simply range-bet every board.

### 2.4 `HUSB`

**Cash use:** ancestry only; no literal six-max PFA range match.

**Source behavior includes:**

- narrow A/K-high TP slowplay under shallow effective-stack conditions;
- TP+/MP/BP 40/50 families;
- frontdoor draws bet;
- straight-possible air checks;
- profile-driven exploit overrides.

**Classification:**

- hand/board concepts: **A**;
- `effective stack <=16` slowplay trigger: **X**;
- global HU range assumptions: **X/A**, depending individual line;
- exploit profile overrides: quarantined for a later exploit layer, **not baseline CashCrusher**;
- default broad air CBet: **X as literal six-max baseline**.

HUSB is useful as corroborating evidence, not as the parent of UTG/HJ/CO/BTN cash ranges.

### 2.5 `HUBB`

**Cash use:** OOP/checking and sizing concepts only. It is not a literal PFA SRP parent for most six-max spots.

**Source behavior:**

- some strong draws deliberately skip CBet to X/R;
- weak pair and air decisions depend strongly on board wetness/backdoors;
- TP+ uses small size on less dynamic boards and large size on connected/draw-heavy boards.

**Classification:**

- polarized OOP sizing concept: **A**;
- check-raise preservation with strong draws: **A**;
- exact 25/75 split: **A/P**;
- HU-specific range assumptions: **X/A**.

### 2.6 `3wBBvSB`

The audited source itself describes this as a route-invariant **"Facing Check (ISO/LP/SRP)"** tree. Hero being BB and checked to does not tell us that Hero is the ordinary SRP PFA.

**Classification:**

- checked-to IP hand/board heuristics: **A**;
- direct six-max SRP-PFA ancestry: **X**;
- old `<=20 BB` versus `>20 BB` value-size split: **X**;
- dry-small / dynamic-larger sizing idea: **A**;
- inherited shove-on-XR plans: **X until re-solved by actual SPR/hand/range context**.

### 2.7 `3wSBvBTN` and `3wBBvBTN`

These are important because six-max creates many OOP-vs-later-position structures, but their preflop roles/ranges are not automatically the same as a cash PFA facing a cold caller.

**Major six-max gap:**

- UTG → HJ/CO/BTN call;
- HJ → CO/BTN call;
- CO → BTN call.

`3wSBvBTN` is the closest positional skeleton (Hero OOP versus later-position Villain), but copying its range policy would be false precision.

**Classification:**

- position/check/bet structure: **A**;
- range frequencies: **P**;
- exact sizing: **P/A**;
- any shallow commitment conversion: **X**.

This family becomes one of CashCrusher's largest professional-theory construction areas.

### 2.8 `3wBTNv2p` — true three-way source

DeepCrusher explicitly says there is no dedicated Starting Strategy file for the exact node and uses human-reviewed CrusherTBP as gap fill.

**Classification:**

- First/Middle/Last multiway architecture: **A**;
- specific two-opponent hand lines: **A/P**;
- RegHU/fish profile distinctions: later exploit layer, not baseline;
- exact 33/50/75/100 sizing map: **A/P**;
- four-, five- and six-way extension: **P**, no literal legacy source.

---

## 3. CashCrusher professional-theory parent rules (P)

These principles fill gaps left by the format change. They are not presented as exact solver frequencies.

### 3.1 Range advantage and nut advantage precede hand class

CashCrusher must not ask only "do I have top pair?". The CBet parent first asks:

1. who has the stronger overall range on this board;
2. who contains more of the nut region;
3. how easily the caller realizes equity;
4. whether Hero is IP or OOP;
5. what future-street SPR remains.

A top pair on `A72r` in BTN-v-BB and the same nominal top pair on `987ss` do not belong to the same CBet family.

### 3.2 Static high-card boards

Where the PFA retains strong range advantage and the caller has relatively few two-pair/straight combinations, a small CBet can be used with a wide range, especially IP.

Typical candidates include many disconnected A-high and K-high rainbow/two-tone boards, subject to the exact matchup.

This is the professional-theory justification for preserving the *concept* behind many legacy small-CBet families without preserving their literal frequencies.

### 3.3 Low/middle connected boards

On boards that strongly interact with the caller's suited connectors, one-gappers, pocket pairs and two-pair/straight region:

- CBet frequency falls;
- checking range strengthens;
- bets become more selective/polar;
- larger sizing can make more sense for the portion that does bet.

This replaces blanket legacy rules such as "bet all air except when straight possible" with a graded range-interaction model.

### 3.4 OOP PFA

OOP PFA must check materially more than IP PFA because:

- Villain realizes position on all later streets;
- Hero's check range must withstand delayed aggression;
- marginal made hands benefit from pot control;
- draws can profit from X/R or X/C rather than automatic lead.

`3wSBvBB` gives useful source ancestry; P theory expands it to the new cold-caller matchups.

### 3.5 Multiway

As more live ranges remain:

- bluff density generally decreases;
- thin-value threshold strengthens;
- bets into multiple players represent stronger ranges;
- nut equity, robust draws and blockers become more important;
- no fixed "reduce CBet by X%" rule is assumed.

Four-way+ has no literal Crusher parent and begins as P.

### 3.6 Deep-stack draws

CashCrusher removes the Spin concept "stack-off draw" as a universal class. Draw aggression instead uses:

- nut versus non-nut draw;
- number/quality of clean outs;
- overcards;
- pair+draw/combo status;
- backdoor redundancy;
- blockers to Villain continue/raise range;
- IP/OOP;
- raw SPR and raise geometry.

### 3.7 Deterministic hardcoding versus mixed solver strategy

A hardcoded OpenPPL strategy cannot safely turn every solver mix into "always bet" or "always check". Where professional play is genuinely mixed, CashCrusher should prefer **hand-feature selection** (blockers, backdoors, kicker quality, suit interaction) to approximate the mix with strategically meaningful combos. Explicit randomization can be considered later only if OpenHoldem runtime behavior is validated and the mix cannot be represented cleanly by combo properties.

---

## 4. Six-max SRP CBet family map

### 4.1 PFA IP versus BB

Exact matchups:

- UTG-v-BB (`16`)
- HJ-v-BB (`26`)
- CO-v-BB (`36`)
- BTN-v-BB (`46`)

Parent:

- `46`: `3wBTNvBB` high-confidence A parent;
- `16/26/36`: same structural parent plus P matchup adjustment.

Important trend: earlier openers carry stronger/narrower ranges, while BB's defend range also changes against each open. Exact CBet policy must therefore keep the absolute matchup ID available rather than collapsing all four into one BTN-v-BB range.

### 4.2 PFA IP versus SB

Exact matchups:

- `15`, `25`, `35`, `45`.

Parent:

- `45`: `3wBTNvSB` high-confidence A parent;
- earlier positions: structural A + P matchup adjustment.

### 4.3 PFA OOP versus later-position cold caller

Exact matchups:

- `12`, `13`, `14`, `23`, `24`, `34`.

Parent:

- no direct source parent;
- `3wSBvBTN` is only positional ancestry;
- policy is primarily **P**, with source-derived hand/board concepts used as constraints.

This family must never silently inherit BTN-v-BB range-bet behavior.

### 4.4 SB-v-BB

Matchup `56`.

Parent:

- `3wSBvBB` high-confidence A parent.

This is the cleanest OOP direct descendant in the project.

---

## 5. ISO, 3BP, squeeze and 4BP

### ISO

An ISO is still a one-raise pot mechanically, but ranges are different from ordinary open/call. CashCrusher routes it separately.

Legacy raised/isolated material is useful for action-history ideas, but exact cash ISO CBet policy is **A/P**.

### 3BP

A two-raise pot has compressed ranges and lower SPR. It receives its own IP/OOP CBet family.

Using the SRP CBet tree unchanged is **X**.

### Squeeze

Squeeze is a 3BP subtype with extra dead money and distinct cold-call/opener ranges. It remains separate whenever Gate 00C can prove it.

### 4BP

Mechanically classified by Gate 00C, strategically uncovered for now. It fails closed until a dedicated professional tree is built.

---

## 6. Sizing contract for future implementation

CashCrusher will support a cleaner flop sizing palette than the inherited short-stack tree:

- small: ~25–33% pot;
- medium: ~45–55% pot;
- large: ~66–80% pot;
- pot / overbet only in specifically justified polarized nodes.

The exact OpenPPL action code will be chosen later by the betsize layer. A legacy 30/33 or 50 size can often map naturally into the small/medium family; a legacy 60/66/75 becomes a candidate large family. This is an **A** mapping, not proof that the old size is optimal in the new range matchup.

Global betsize-to-all-in conversion remains disabled.

---

## 7. Decision from Gate 01 audit

The source has enough high-quality knowledge to justify transplantation, but not enough to justify a literal copy.

The strongest direct SRP parents are:

1. `3wBTNvBB` → BTN-v-BB PFA IP;
2. `3wBTNvSB` → BTN-v-SB PFA IP;
3. `3wSBvBB` → SB-v-BB PFA OOP.

Everything else is either structural ancestry or a theory gap.

Therefore CashCrusher will implement CBet through **new six-max parents**, while preserving exact source provenance for every inherited concept.

## Next implementation boundary

`src/CashCrusher_Flop_CBet.txt` contains the new routing contract. Strategic child functions remain fail-closed until their range/board families are implemented and reviewed. This prevents an unfinished 3BP/multiway node from accidentally inheriting an SRP policy.
