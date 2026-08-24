# CashCrusher Status

Last update: 2026-08-23

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime gates are passed.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem.
- Runtime supports hands dealt 2h, 3h, 4h, 5h or 6h as seats empty/sit out.
- Preflop is used to reconstruct post-flop context/ranges, not to decide current project preflop strategy.
- Strategic provenance is mandatory: T / A / P / X.
- Source-derived and professional-theory rules remain explicitly distinguishable.
- Unknown/unsupported strategic context fails closed.
- OpenPPL strategy code uses flat complete `WHEN` rules; indentation is never logical scope.
- Every `f$cc_*` function requires nearby Source/Provenance documentation in CI.

## Stack-depth migration rule

DeepCrusher short-stack logic is a **review flag, not an automatic deletion/zeroing rule**.

For every stack-sensitive inherited rule:

- do not assume it transfers unchanged to ordinary 100bb cash;
- do not assume it becomes invalid merely because CashCrusher starts deeper;
- review exact pot/range/board/action/effective-stack/SPR context;
- classify locally as T, A, P or X.

This applies to TP+/draw commitment lines, `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, `BetMax` and related mechanisms.

## Context / stack foundation

Gate00 design/code is implemented. Release certification still needs OpenHoldem parser/runtime fixtures.

Frozen rules:

- HU uses exact Hero-v-Villain effective stack;
- multiway preserves both shallowest and deepest effective relationships;
- a short sidepot player never collapses the whole multiway decision into short-stack policy;
- true-HU deal, preflop-reduced HU and postflop-reduced HU remain distinct range origins;
- pot family, Hero role, exact position, opponent provenance and action history are first-class routing inputs.

## Flop CBet — Gate01

Strategic baseline implemented for ordinary SRP, HU/multiway ISO, plain 3BP+squeeze, true-threeway and 4/5/6-way SRP, and clean supported HU 4BP.

Still fail-closed: multiway 4BP, unresolved/reversed/backraise/limp-reraise 4BP chronology and 5bet+.

Execution/history rules:

- local `BetMax` only for natural/mechanical equivalence;
- historical ~50% effective / ~60% Hero-stack promotion is diagnostic, not generic cash strategy;
- closed round-2 history distinguishes actual CBet, check-through, check-call/XR and CBet-raised histories;
- pre-action plan markers never prove execution.

Whole-bot `f$flop` / `f$BestBetsize` composition and replay certification remain pending.

## Turn CBet — Gate02

Strategic coverage is implemented for all currently supported Flop-CBet parents:

- source-anchored true/reduced HU ordinary SRP;
- six-max EP/MP/CO SRP range gaps;
- flop multiway -> turn HU and turn-still-multiway;
- ISO;
- plain 3BP;
- squeeze;
- clean supported HU 4BP.

Runtime size palette: **25 / 33 / 40 / 50 / 62.5 / 75 / 100%**.

Natural `BetMax` conversion is limited to the reviewed requested size already reaching Hero stack, exact HU effective stack, or deepest/all-live multiway effective relation. A shortest-only sidepot does not promote the action.

### Gate02N complete

Closed round-3 history now proves what actually happened on Turn before River routing:

- standard one-size Turn CBet;
- actual check-through;
- check-call / check-aggression;
- CBet -> raise -> call;
- CBet -> Hero re-aggression;
- direct all-in versus sized execution;
- plan-v-runtime mismatch;
- exact Turn family/hand/runout/player-count/live-opponent snapshot.

River CBet consumes actual executed Turn history, not `f$cc_turn_cbet_router = true` alone.

## River CBet — Gate03 complete at static/deterministic level

Implemented:

- source-anchored ordinary SRP descendants;
- P-heavy six-max SRP gaps;
- post-multiway HU and current-multiway river states;
- ISO with limper/coldcaller provenance;
- plain 3BP with opener/coldcaller provenance;
- squeeze with opener/pre-squeeze/post-squeeze caller provenance;
- clean supported HU 4BP.

Runtime size palette: **25 / 33 / 50 / 75 / 100%**.

Natural all-in equivalence follows the same Hero/HU/deepest-multiway rule. TP/OP in naturally low-SPR 4BP can remain aggressive where the exact node supports it, but there is no generic `TP+ -> stackoff` rule.

River source, six-max gap, other-pot, coverage and runtime contracts are green in CI.

## Flop Float — Gate04 complete at static/deterministic level

### Canonical ownership

Flop Float now has a deliberately narrow meaning:

- Hero is a preflop caller/non-initiator;
- no bet faces Hero;
- it is Hero's first flop action;
- Hero is exact **LAST/IP** in the reviewed baseline;
- expected preflop aggressor has skipped CBet.

`BotsActionsOnThisRoundIncludingChecks = 0` is used so an earlier Hero check cannot be mislabeled as an initial Float. Relative `MIDDLE` is explicitly excluded because a live player remains behind.

### Source-anchored descendants

Implemented directly/high-ancestry:

1. true-HU HUSB: SB/Button limp-call versus BB raise, BB checks;
2. reduced-HU BB caller IP versus SB PFA (`3wBBvSB`).

The source dry/wet, lower-pair delayed-plan and real-draw distinctions are preserved. Historical wet-board TP+ check-raise shove plans remain separate defense/stack-review material and are not imported into the initial 100bb Float action.

### Six-max/P-heavy fills

Implemented:

- nonblind ordinary-SRP caller IP versus earlier opener;
- exact-LAST multiway ordinary SRP checked-to stab;
- ISO, preserving original limper versus post-raise coldcaller;
- plain 3BP, preserving opener-call versus post-3bet coldcaller;
- squeeze, preserving opener / pre-squeeze caller / post-squeeze caller;
- one conservative clean caller-IP 4BP topology: opener -> Hero 3bet -> opener 4bet -> Hero call -> opener checks.

Multiway Float is substantially tighter: pure-air baseline disappears and 4+ way generally requires robust value or combo-draw quality.

Unresolved/reversed 3BP/4BP, generic cold4-caller histories and 5bet+ remain fail-closed.

### Flop Float execution/history

Runtime size palette: **25 / 33 / 50 / 75 / 100%**.

Natural all-in equivalence can return `BetMax` only if the chosen size already reaches Hero stack, exact HU effective stack, or deepest/all-live multiway effective relation. Shortest-only sidepot reach cannot promote the whole action.

Closed round-2 Float history now distinguishes:

- actual initial Float bet;
- normal sized versus direct all-in;
- actual check-back;
- Float -> raise -> call;
- Float -> Hero re-aggression;
- plan-v-runtime drift;
- family/hand/texture/player-count/live-opponent snapshot.

The HUSB source `air Float -> no forced 2Bar / no BxB` intent is retained as plan provenance without pretending the bet executed.

### Validation

GitHub Actions run **#490** completed successfully after the final Gate04 test correction.

That run passed:

- global dependency / flat-WHEN / provenance linter;
- all existing Flop/Turn/River CBet tests;
- Flop Float source/topology contract;
- Flop Float coverage/exclusivity/fail-closed contract;
- Flop Float runtime sizing/natural-all-in contract;
- closed Flop Float action-history contract.

## Critical boundary for the next node

A standard executed **Flop Float is not automatically the parent of Turn Float**.

The audited DeepCrusher `f$move_turn_floatbet` is a checked-to-Turn ownership node with multiple action histories. Gate05 must reconstruct those histories source-first instead of assuming “Float flop -> Float turn”.

## Remaining release blockers

No table-ready claim before:

1. Gate00 parser/runtime context validation;
2. whole-bot history-aware `f$flop` / `f$turn` / `f$river` / `f$BestBetsize` composition;
3. deterministic OpenHoldem policy replays;
4. Turn Float, River Float, Donk, Probe, Delayed/no-action attack gates;
5. all 32 defensive nodes;
6. exact-node commitment and final global callback audit;
7. full regression / unknown-state fail-closed review.

## Immediate development direction

Next gate: **Gate05 — Turn Float source/history audit**.

Before writing its strategy, identify exactly which closed-Flop histories genuinely belong to the legacy/current Turn Float node. Do not assume the newly implemented standard Flop Float parent is its only or even primary parent.
