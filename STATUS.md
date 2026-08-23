# CashCrusher Status

Last update: 2026-08-23

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime gates are passed.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem.
- Six-max means a table with up to six players; the runtime must support hands dealt 2h, 3h, 4h, 5h or 6h as seats empty/sit out.
- Preflop is currently used only to reconstruct post-flop context/ranges.
- Strategic provenance is mandatory: T / A / P / X.
- Source-derived and professional-theory rules remain explicitly distinguishable.
- Unknown/unsupported strategic context fails closed.
- Legacy global short-stack commitment/all-in conversion is disabled.

## Gate 00 — mechanical context foundation

### Complete in design/code; runtime validation pending

- **00A** — legacy Spin game labels decomposed into strategic properties.
- **00B** — six-max HU ancestry/matchup matrix.
- **00C** — OpenPPL context engine: pot family, Hero role, absolute/relative position, matchup, live masks and preflop-history classification.
- **00D** — raw SPR reconstruction and deep-stack commitment quarantine.
- **00E** — true multiway exact context/composition architecture.
- **00F** — dynamic 2-6 handedness and HU-origin preservation.

### Critical 00F rule

`nplayersplaying = 2` is not enough to choose a HU strategy.

CashCrusher now distinguishes:

1. **TRUE_HU_DEAL** — exactly two were dealt; SB is also Button and is IP postflop;
2. **PREFLOP_REDUCED_TO_HU** — 3-6 were dealt but only two reached flop;
3. **POSTFLOP_REDUCED_TO_HU** — flop began multiway and later action reduced it to HU.

A true-HU `SB/Button-v-BB` and a normal-table `SB-v-BB` can both have matchup ID `56`, but must never share policy by ID alone.

The number of players who reached the flop is reconstructed from `playersdealtbits` and `foldbits1` and survives to later streets.

## Gate 01 — Flop CBet

### Source audit

- Original audit completed.
- Handedness-aware audit v2 published and is authoritative.
- Direct/strong parents identified:
  - true HU SB/Button PFA IP vs BB -> HUSB;
  - true HU BB PFA OOP after SB limp/BB raise -> HUBB limped/initiative ancestry;
  - BTN-v-BB -> 3wBTNvBB;
  - BTN-v-SB -> 3wBTNvSB;
  - SB-v-BB in a 3+ player deal -> 3wSBvBB;
  - opener OOP vs later cold caller -> no direct range parent; 3wSBvBTN is position skeleton only.

### Implemented strategic baselines

The following flop CBet families now contain reviewed A/P strategy rather than false stubs:

- true-HU ordinary SRP: SB/Button PFA IP vs BB;
- true-HU SB limp -> BB raise -> SB call: BB PFA OOP;
- 3-6h ordinary SRP reduced HU: PFA IP vs BB;
- 3-6h ordinary SRP reduced HU: PFA IP vs SB;
- 3-6h ordinary SRP reduced HU: SB PFA OOP vs BB;
- 3-6h ordinary SRP reduced HU: opener PFA OOP vs later-position cold caller.

Professional fills are deterministic combo-selection baselines using made-hand tier, draw quality, backdoors, board pressure, absolute matchup and raw SPR. They are **not claimed as exact solver/GTO frequencies**.

Current strategic size IDs:

- `1` small ~33% pot;
- `2` medium ~50%;
- `3` large ~75%;
- `4` pot reserved, unused by ordinary-SRP baseline.

### Still fail-closed / not yet implemented

- non-HU ISO CBet;
- true-HU standard 3BP CBet;
- 3-6h ordinary 3BP CBet;
- squeeze CBet;
- 4BP CBet;
- all multiway CBet policies;
- flop betsize execution wiring into the final OpenPPL action router;
- full skipped-CBet X/C and X/R follow-through in CashCrusher defense modules.

## Safety/quality infrastructure

- Exact context-ID contract versioned.
- Context acceptance matrix expanded for 2-6h and HU origin.
- Flop-CBet policy acceptance matrix added.
- Static linter checks unresolved/duplicate `f$cc_*`, legacy `f$game_*` dependencies, accidental `StackOffDraws` reuse, and BetMax inside current CBet modules.
- GitHub Actions static-lint workflow exists on the working branch.

## Validation state

### Passed by design/static review

- separation of true HU versus fold-reduced HU;
- pot-family isolation in router;
- source-provenance mapping;
- global betsize-to-all-in conversion disabled;
- uncovered strategy families retain explicit false stubs.

### Still required before merge/release

1. GitHub static lint PASS on current branch/PR;
2. OpenPPL parser validation with the actual OpenHoldem parser;
3. deterministic synthetic/replay states for Gate00 context matrix;
4. deterministic policy fixtures for Gate01 CBet matrix;
5. betsize runtime mapping;
6. follow-through attack/defense nodes after skipped CBet;
7. no table-ready claim until those gates pass.

## Current development direction

Continue Gate 01 one pot family at a time without allowing ordinary-SRP policy to leak into ISO/3BP/squeeze/multiway. After Flop CBet coverage is mature and validated, move to Turn CBet while preserving the same HU-origin and flop-origin provenance across streets.
