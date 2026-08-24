# CashCrusher Status

Last update: 2026-08-24

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

Strategic baseline is implemented for ordinary SRP, HU/multiway ISO, plain 3BP+squeeze, true-threeway and 4/5/6-way SRP, and clean supported HU 4BP.

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

River source, six-max gap, other-pot, coverage and runtime contracts remain green in the combined CI suite.

## Flop Float — Gate04 complete at static/deterministic level

### Canonical ownership

Flop Float has a deliberately narrow meaning:

- Hero is a preflop caller/non-initiator;
- no bet faces Hero;
- it is Hero's first flop action;
- Hero is exact **LAST/IP** in the reviewed baseline;
- expected preflop aggressor has skipped CBet.

`BotsActionsOnThisRoundIncludingChecks = 0` is used so an earlier Hero check cannot be mislabeled as an initial Float. Relative `MIDDLE` is explicitly excluded because a live player remains behind.

### Implemented descendants

Direct/high-ancestry source descendants:

1. true-HU HUSB: SB/Button limp-call versus BB raise, BB checks;
2. reduced-HU BB caller IP versus SB PFA (`3wBBvSB`).

Six-max/P-heavy fills:

- nonblind ordinary-SRP caller IP versus earlier opener;
- exact-LAST multiway ordinary SRP checked-to stab;
- ISO, preserving original limper versus post-raise coldcaller;
- plain 3BP and squeeze, preserving caller origin;
- one conservative clean caller-IP 4BP topology: opener -> Hero 3bet -> opener 4bet -> Hero call -> opener checks.

Multiway Float is substantially tighter: pure-air baseline disappears and 4+ way generally requires robust value or combo-draw quality.

Runtime size palette: **25 / 33 / 50 / 75 / 100%**. Natural all-in equivalence can promote only when the selected size already reaches Hero stack, exact HU effective stack, or deepest/all-live multiway effective relation.

Closed round-2 Float history distinguishes actual bet, check-back, Float->raise->call, re-aggression, direct all-in, plan/runtime drift, family, hand, texture and live-field snapshot.

## Gate04R — 3BP pure-coldcaller chronology repair

Gate05A exposed a real reachability defect in the earlier Gate04E 3BP/squeeze context.

The older `f$cc_pf_3bet_first_raiser_pos_id` / `f$cc_pf_3bet_final_raiser_pos_id` chain depends on `f$cc_pf_other_raiser_pos_id`, and that helper requires `f$cc_pf_hero_ever_raised`. Therefore Hero with `f$cc_pf_role_cold_call_3bet` could not obtain a final-3bettor position from that path. Several pure-coldcaller Flop-Float branches had valid strategy bodies but unreachable chronology proof.

The repair is now implemented through `CashCrusher_FinalAggressor_Context.txt`:

- actual final preflop aggressor comes from stable `lastraised1`;
- `raisbits1` independently validates that chair as a raiser;
- the other unique raiser reconstructs the opener in supported two-raise/two-raiser histories;
- first-orbit order distinguishes plain 3BP versus squeeze;
- Hero is classified as opener-call, pre-3bet coldcaller, or post-3bet coldcaller without requiring Hero to have raised.

`CashCrusher_Flop_Float_3BP_CallerRepair.txt` applies this stronger evidence only to the previously unreachable pure-coldcaller descendants. Their poker policy/sizing was not broadened; Gate04E's conservative action maps were preserved.

The canonical Flop Float router now combines the original and repaired coverage while keeping plain3BP/squeeze as the same strategic family IDs.

## Turn Float — Gate05 complete at static/deterministic level

### Canonical ownership and history

Turn Float means a checked-to-Turn no-initiative opportunity after Villain owned the relevant previous aggression. It is not equivalent to “Hero Float-bet flop, therefore bet turn again.”

Three canonical closed-flop parents are implemented:

1. **Called final-preflop-aggressor flop bet** — Hero was a supported preflop caller, called exactly one clean flop bet, and the actual flop aggressor equals the actual final preflop aggressor.
2. **CBet -> raise/XR -> Hero call** — Villain ended flop as aggressor and then gives Hero a checked-to Turn opportunity.
3. **Flop Float -> later raise/XR -> Hero call** — separate selected-range history, never merged with parent 1 or 2.

A narrow source repair also supports the explicit unraised `3wBBvSB` line:

`SB limp -> BB check -> SB bet flop -> BB call -> SB check Turn`.

The repair does not create a generic called-bettor fallback.

Before Turn Float can act:

- it must be Turn;
- context must be valid and Hero must have chips;
- it must be Hero's first Turn action, including checks;
- `AmountToCall = 0`;
- Hero must be exact LAST;
- HU requires Hero IP;
- the relevant parent/source-repair history must be proven and internally consistent.

HU-from-HU-flop, post-multiway-to-HU and current-multiway origins remain distinct.

### Direct/high-ancestry source decisions

`3wBBvSB` Facing Bet -> call -> Turn check preserves the explicit LP/SRP source behavior:

- current no-made real draw -> Float50;
- current no-made air/high-card -> Float50;
- broad source `turn_Completed` -> barrel-river plan;
- otherwise -> give-up-river plan.

BTN Advanced CBet -> flop XR/raise -> call -> Turn check preserves:

- AIR/A-high-like miss -> 33% inside the source 25–40% interval;
- still-live FD/OESD/Gutshot+ does **not** inherit the AIR instruction;
- audited current-DeepCrusher made improvement -> 50%, explicitly classified as A rather than primary-source exact.

The `3wBTNvSB` no-made check philosophy remains an explicit negative source lock and cannot be overwritten by a P bluff rule.

Source coverage is branch-level. A matchup having source ancestry does not mean every current hand class is source-decided.

### Six-max/P-heavy expansion

Implemented separate owners for:

- ordinary SRP simple flop-call -> missed 2Bar;
- ordinary SRP CBet-XR-call;
- ordinary SRP FlopFloat-XR-call;
- ordinary SRP flop-multiway -> Turn-HU;
- ordinary SRP current multiway;
- ISO with original-limper versus post-raise-coldcaller provenance;
- true-HU limp-raised ancestry;
- plain 3BP with opener/pre3bet/post3bet caller origin retained;
- squeeze kept separate from plain 3BP;
- clean supported HU 4BP.

Current-multiway policy is sharply tightened. At 4+ players pure air is absent; positive no-made action is essentially restricted to the strongest reviewed combo-draw class. Multiway low-SPR exceptions use **deepest/all-live effective SPR**, not the short sidepot player.

### Deep-stack commitment boundary

Gate05 does not recreate DeepCrusher's short-stack `TP+ -> stackoff` behavior.

- TP and OP remain one-pair value/SDV classes, not global stack-off classes.
- 2P+ is re-evaluated against completed/dynamic Turn topology rather than treated as an unconditional shove class.
- low SPR can modify an exact node but is never a standalone commitment action.
- strategy files contain no `f$Raise_Committed` or `f$hand_StackOffDraws` action implication.
- strategic policy files do not directly issue `BetMax`.

Runtime palette is **25 / 33 / 50 / 75 / 100%**.

Natural `BetMax` conversion is only mechanical: the already selected size must reach Hero stack, exact HU effective stack, or deepest/all-live multiway effective relation. Reaching only a shallow sidepot stack does not promote the whole action.

Historical 50/55/60% near-all-in logic remains diagnostic only.

### Gate05N closed execution history

Closed Turn-Float history proves what actually happened before River Float routing:

- actual initial Float bet;
- actual check-back;
- sized execution versus direct all-in;
- Float -> raise -> Hero call;
- Float -> Hero re-aggression;
- final aggressor identity;
- exact parent/family/state snapshot;
- plan-v-runtime mismatch;
- source give-up-river versus barrel-river plan only after valid executed history.

`f$cc_hist_river_float_standard_parent_valid` is now the safe bridge for Gate06 River Float. Pre-action `user_*` markers alone never prove execution.

The canonical audit is `docs/audits/GATE_05_TURN_FLOAT_AUDIT.md`.

## Validation

GitHub Actions **run #570** completed successfully on the Gate05 audit head. The strategy-closing run **#568** was also green after the final runtime-test correction.

The combined suite now passes through:

- global dependency / flat-WHEN / provenance / safety lint;
- all Flop/Turn/River CBet tests;
- all Flop Float strategy/coverage/runtime/history tests;
- `lastraised1` final-aggressor + Gate04R caller-side 3BP repair;
- Gate05A Turn-Float history/opportunity;
- Gate05B direct-source strategy;
- Gate05C-F six-max coverage/provenance/fail-closed policy;
- Gate05 runtime sizing + natural all-in equivalence;
- Gate05 closed Turn-Float action history + River-parent contract.

The last test-only correction made the runtime assertion strip `//` comments before checking that executable all-live-effective logic never uses the shallowest multiway relationship. No poker strategy changed in that correction.

## Remaining release blockers

No table-ready claim before:

1. Gate00 parser/runtime context validation;
2. whole-bot history-aware `f$flop` / `f$turn` / `f$river` / `f$BestBetsize` composition;
3. deterministic OpenHoldem policy replays;
4. River Float, Donk, Probe and Delayed/no-action attack gates;
5. all 32 defensive nodes;
6. exact-node commitment and final global callback audit;
7. full regression / unknown-state fail-closed review.

Unsupported multiway/reversed 4BP and 5bet+ ancestry from earlier gates remain fail-closed rather than being patched with neighboring strategy.

## Immediate development direction

Next small gate: **Gate06A — River Float source/history ownership audit only**.

Begin from the newly certified `f$cc_hist_river_float_standard_parent_valid` bridge and audit DeepCrusher/Crusher Starting Strategy for explicit River Float descendants before adding any six-max P policy. Preserve any source give-up/barrel plan only when the closed Turn-Float execution history proves the parent that created it.

Do not yet jump to Donk/Probe/Delayed or defensive nodes until River Float ownership/source boundaries are frozen.