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
- **TP+/overpair are hand descriptors, not stack-off permissions.** A positive attack action owns only that street's action; later raise/call/jam decisions are re-audited independently.

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

CashCrusher distinguishes:

1. **TRUE_HU_DEAL** — exactly two were dealt; SB is also Button and is IP postflop;
2. **PREFLOP_REDUCED_TO_HU** — 3-6 were dealt but only two reached flop;
3. **POSTFLOP_REDUCED_TO_HU** — flop began multiway and later action reduced it to HU.

A true-HU `SB/Button-v-BB` and a normal-table `SB-v-BB` can both have matchup ID `56`, but must never share policy by ID alone.

The number of players who reached the flop is reconstructed from `playersdealtbits` and `foldbits1` and survives to later streets.

## Gate 01 — Flop CBet

### Source/safety audit

- Handedness-aware source audit v2 is authoritative.
- `OPENPPL_CODING_CONTRACT.md` is binding: flat complete WHENs only; no indentation-based logical scope.
- Per-function source/provenance comments are mandatory in reviewed `CashCrusher_Flop_CBet*` strategy modules.
- `GATE_01_DEEPSTACK_COMMITMENT_DECOUPLING.md` freezes the migration rule that DeepCrusher TP+/overpair/large-call commitment behavior does not transfer globally to cash.

### Implemented ordinary one-raise baselines

Reviewed A/P strategy exists for:

- true-HU ordinary SRP: SB/Button PFA IP vs BB;
- true-HU SB limp -> BB raise -> SB call: BB PFA OOP;
- 3-6h ordinary SRP reduced HU: PFA IP vs BB;
- 3-6h ordinary SRP reduced HU: PFA IP vs SB;
- 3-6h ordinary SRP reduced HU: SB PFA OOP vs BB;
- 3-6h ordinary SRP reduced HU: opener PFA OOP vs later-position cold caller.

### Implemented ISO baselines

`CashCrusher_ISO_Context.txt` preserves whether the surviving HU Villain is:

- the original pre-raise limper; or
- a post-raise cold caller.

Reviewed P/A CBet baselines now exist IP/OOP for both HU survivor types. Multiway ISO remains fail-closed.

### Implemented 3-bet-pot context and baselines

`CashCrusher_3BP_Context.txt` distinguishes the surviving HU range as:

1. original opener who called the 3bet;
2. pre-3bet cold caller who survived a squeeze;
3. post-3bet cold caller.

This prevents a generic "3BP Villain" range from contaminating strategy.

Reviewed flop CBet baselines now exist for:

- true-HU standard plain 3BP: BB 3bettor OOP vs SB/Button opener-call;
- 3-6h plain 3BP: Hero 3bettor IP vs original opener-call;
- 3-6h plain 3BP: Hero 3bettor OOP vs original opener-call;
- 3-6h plain 3BP: Hero 3bettor IP vs post-3bet cold caller;
- 3-6h plain 3BP: Hero 3bettor OOP vs post-3bet cold caller.

The post-3bet coldcaller family is deliberately P-heavy. DeepCrusher has no dedicated deep-stack cold-call-3bet range strategy; source contributes only architecture/hand-board concepts.

### Current commitment safety

The following are now hard project rules:

- a flop CBet with TP or overpair means only "bet this flop";
- it does not pre-authorize call-vs-XR, 3bet-vs-XR, future barrels or stack-off;
- legacy `f$Raise_Committed` is prohibited;
- legacy `f$hand_StackOffDraws` is prohibited;
- `f$allin_on_betsize_balance_ratio` must remain disabled;
- future executable `BetMax` requires an explicit local `ALLIN_OWNER_REVIEWED` marker and exact-node justification;
- current flop-CBet modules may not contain `BetMax` at all.

This directly prevents the short-stack DeepCrusher pattern "TP+ -> get stacks in" from leaking into deep cash.

### Current strategic size IDs

- `1` small ~33% pot;
- `2` medium ~50%;
- `3` large ~75%;
- `4` pot reserved.

A size ID is a street-specific bet intention and has no automatic commitment meaning.

### Still fail-closed / not yet implemented

- multiway ISO CBet;
- all squeeze CBet survivor families;
- multiway 3BP/squeeze CBet;
- 4BP CBet;
- true multiway ordinary SRP CBet;
- flop betsize execution wiring into final OpenPPL action callback;
- full skipped-CBet X/C/X/R follow-through in defense modules.

## Safety/quality infrastructure

- Exact context-ID contract versioned.
- Context acceptance matrix covers 2-6h and HU origin.
- 3BP acceptance matrix covers opener, pre-3bet caller and post-3bet caller provenance.
- Static linter checks:
  - unresolved/duplicate `f$cc_*`;
  - executable legacy `f$game_*`;
  - open-ended/nested-looking WHEN scope;
  - `StackOffDraws`;
  - `f$Raise_Committed`;
  - nonzero global auto-commit callback;
  - unowned `BetMax`;
  - `BetMax` inside current flop-CBet modules;
  - missing local strategy provenance comments.
- GitHub Actions static-lint workflow exists on the working branch.

## Validation state

### Passed by design/static review

- true HU vs fold-reduced HU separation;
- pot-family and survivor-range routing separation;
- source-provenance mapping;
- global betsize-to-all-in conversion disabled;
- TP+/one-pair commitment implication explicitly rejected;
- uncovered squeeze/multiway/4BP families still fail closed.

### Still required before merge/release

1. GitHub static lint PASS on the **current** branch/PR head after latest linter hardening;
2. OpenPPL parser validation with the actual OpenHoldem parser;
3. deterministic synthetic/replay states for Gate00 context matrix;
4. deterministic policy fixtures for Gate01 CBet matrix;
5. betsize runtime mapping;
6. follow-through attack/defense nodes after skipped CBet;
7. no table-ready claim until those gates pass.

## Current development direction

Next strategic subgate: **01H — squeeze-pot flop CBet**. Start with HU squeeze versus the original opener only; do not implement all squeeze survivor types in one pass. Preserve the same exact survivor provenance and the same rule that one-pair aggression is not stack commitment.
