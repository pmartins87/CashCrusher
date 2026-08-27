# Gate 01 — Flop CBet dependency audit

Status: **dependency classes frozen; portable subset implemented**.

The original `f$move_flop_cbet` does not stand alone. It depends on game labels, hand ladders, draws, texture helpers, effective-stack logic, exploit profiles, pot history and cross-street user states. A literal copy would therefore import hidden Spin assumptions even if obvious all-in lines were removed.

This audit classifies those dependencies before any six-max policy is enabled.

## 1. Portable mechanical dependencies — T/A

Implemented in `src/CashCrusher_Postflop_Primitives.txt` or `src/CashCrusher_Flop_Texture.txt`.

### Made-hand ladders

Portable concepts:

- pair or better;
- overpair or better;
- two-pair+;
- trips/set+;
- top pair+;
- second/third/fourth/fifth pair or pocket-pair tier;
- weak top pair / kicker quality.

The source's paired-board correction for second/third/fourth pair is retained because it fixes a mechanical hand-classification issue rather than a Spin strategy assumption.

### Real draws

Portable concepts:

- real flush draw;
- nut flush draw;
- real OESD excluding a straight draw that exists only on board;
- gutshot;
- combo draw;
- pair+draw;
- overcards + draw;
- backdoor flush/straight draws.

The important adaptation is that CashCrusher calls them **draw descriptors**, not `StackOffDraws`.

### Board structure

Portable raw components:

- monotone / two-tone / rainbow;
- paired / trips / unpaired;
- A/K/Q/JT/9-low top-card bands;
- broadway count;
- `StraightPossibleOnFlop`;
- `OpenEndedStraightDrawPossibleOnFlop`;
- `UncoordinatedFlop`;
- exact texture ID for logging.

These are preferred over inheriting a single global `board_dry` or `board_wet` label whose old definition depends on HUSB/HUBB/3w game labels.

## 2. Replaced by Gate 00 — A/X old implementation

### `f$game_HUSB`, `HUBB`, `3wBTNvBB`, `3wSBvBB`, etc.

**Old dependency:** absolute Spin positional shells.

**Replacement:**

- six-max absolute position ID;
- exact HU matchup ID;
- player count;
- relative position;
- exact multiway live mask;
- preflop role and pot family.

Old labels remain documentation ancestry only.

### `f$pot_SingleRaised`, `f$pot_Limped`, raised/isolated shortcuts

**Replacement:** persisted raise count + Hero role + ISO/squeeze proof from `CashCrusher_Context.txt`.

This is necessary because CashCrusher must distinguish ordinary SRP, ISO, 3BP, squeeze, 4BP and unraised pots before strategy fires.

### `f$EffectiveStack`, `f$EffectiveStack_BKP`, shallow stack bands

**Replacement:** raw street-start SPR and actor-specific effective stack from `CashCrusher_SPR_Commitment.txt`.

A literal old threshold such as `<=16 BB`, `<=20 BB`, or "raise consumes half stack => jam" is **X** unless a later node independently re-derives the action from current cash-game geometry.

## 3. Baseline-excluded exploit dependencies

The following source concepts are valuable only for a later exploit layer and must not determine CashCrusher baseline strategy:

- `GreenGuy` / `RedGuy` style opponent classes;
- PT/HUD fold-to-CBet shortcuts;
- RegHU-vs-fish source splits;
- player-specific hardcoded exploit state.

Classification: **X for baseline**, potentially reusable later as **A** exploit infrastructure after six-max statistics are defined.

This separation is critical: a source rule that was profitable because a particular Spin pool overfolded must not masquerade as professional baseline cash strategy.

## 4. Strategic source dependencies requiring adaptation

### Old `f$hand_GoodDraws`, `MediumDraws`, `WeakDraws`

Classification: **A/P**.

Reason: the underlying distinction is useful, but its old membership and response often assume shallow stack-off geometry. CashCrusher will rebuild draw quality from:

- nut potential;
- clean outs;
- overcards;
- pair+draw/combo status;
- blocker properties;
- position;
- pot family;
- raw SPR.

### Old `f$board_dry`, `f$flop_dry_HU`, `f$flop_Wet_HU`, `f$flop_DrawHeavy`

Classification:

- raw connectivity/suit facts: **T/A**;
- game-label-specific dry/wet aggregation: **X/A**;
- strategic use of static vs dynamic boards: **P/A**.

The new texture layer exposes raw facts and only then provides broad P-labelled strategy-parent classes.

### Kicker thresholds such as `NumberOfBetterKickers <= 3`

The mechanical kicker calculation is **T/A**. A particular threshold defining TPGK is only a **descriptor**. Whether that hand is value-bet/check depends on range matchup and board.

## 5. Cross-street state dependencies

The source CBet node writes many user states such as:

- flop sizing selected;
- intentionally skipped CBet;
- expected turn barrel / give-up;
- delayed river plan;
- response plan if raised.

These are strategically valuable architecture (**A**) but should not be transplanted until the corresponding turn/river node is reviewed. CashCrusher must avoid a state name that promises a future action not yet validated for deep cash.

Future convention:

- state records **what actually happened / what family generated it**;
- later street policy decides the action from current context;
- only source-explicit and revalidated plans may encode a stronger future-action commitment.

## 6. Sizing dependencies

Legacy values observed in the CBet tree include roughly 25/30/33/40/50/60/66/75/100 and jam/min variants.

CashCrusher baseline sizing parents are normalized to:

- small: 25–33%;
- medium: 45–55%;
- large: 66–80%;
- pot/overbet: explicit polarized nodes only.

This is an **A** normalization, not an assertion that every source 50 should remain exactly 50 or that every source 75 remains exactly 75.

## 7. Dependency disposition summary

| Legacy dependency | CashCrusher disposition |
|---|---|
| position/game label | replace with exact 6-max context |
| made-hand ladder | transplant/adapt |
| paired-board pair tiers | transplant |
| real draw mechanics | transplant/adapt |
| `StackOffDraws` | reject as stack-off class |
| board raw facts | transplant/adapt |
| game-specific `dry/wet` aggregate | replace |
| shallow stack thresholds | reject/re-derive from SPR |
| global commitment helper | reject |
| exploit/player-profile branch | quarantine from baseline |
| cross-street provenance | preserve architecture, revalidate plan |
| legacy exact sizing | adapt by node |
| HandPower/global scalar fallback | do not use as substitute for range-aware policy |

## 8. Current compile dependency boundary

The following CashCrusher modules now form the intended dependency order:

1. `CashCrusher_Context.txt`
2. `CashCrusher_SPR_Commitment.txt`
3. `CashCrusher_Multiway_Context.txt`
4. `CashCrusher_Postflop_Primitives.txt`
5. `CashCrusher_Flop_Texture.txt`
6. `CashCrusher_Range_Topology.txt`
7. `CashCrusher_Flop_CBet.txt`
8. child CBet strategy files

The custom-symbol linter checks only `f$cc_*` dependencies so built-in OpenPPL/OpenHoldem symbols are not mistaken for missing project definitions.
