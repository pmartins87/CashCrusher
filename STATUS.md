# CashCrusher Status

Last update: 2026-08-24

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime gates are passed.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem, with 2–6 dealt-player runtime support.
- Preflop is reconstructed to identify post-flop pot/range/history context; this project is not currently replacing the preflop strategy.
- Strategic provenance is mandatory: **T / A / P / X**.
- Source-derived and professional-theory rules remain visibly distinguishable.
- Unsupported strategy fails closed instead of leaking from neighboring pot families.
- OpenPPL code uses flat complete `WHEN` rules; indentation is never logical scope.
- Positive betting decisions own only that street action; later barrels, response to raises and stackoff are separate owners.

## Binding stack-depth migration rule

DeepCrusher short-stack logic is a **review flag, not an automatic deletion/zeroing rule**.

For each stack-sensitive inherited rule:

- do not assume it transfers unchanged to 100bb cash;
- do not assume it becomes invalid merely because the target starts deeper;
- review the exact pot/range/board/action/effective-stack/SPR node;
- retain, adapt or reject locally with T/A/P/X provenance.

This applies to TP+/draw commitment, `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, historical ~50/55/60% thresholds, `BetMax` and related mechanisms.

## Foundation — Gate00

Implemented mechanically:

- dynamic 2–6 handed deal size;
- true-HU, preflop-reduced HU and postflop-reduced HU distinction;
- canonical UTG/HJ/CO/BTN/SB/BB positions;
- flop-entry and current-live masks;
- exact HU Villain identity/matchup;
- pot-family and Hero-role taxonomy;
- ordinary SRP / ISO / plain3BP / squeeze / clean 4BP chronology helpers;
- final-aggressor reconstruction using stable persisted history;
- shallowest + deepest multiway effective geometry;
- context/history consistency guards.

HU uses exact effective stack. Multiway keeps shallowest and deepest relationships separately; a short sidepot player never turns the whole decision into short-stack strategy.

OpenHoldem parser/runtime certification for Gate00 is still pending.

## Gate01 — Flop CBet

Static/deterministic baseline implemented for:

- ordinary HU/reduced-HU SRP IP/OOP;
- true-HU limp-raised PFA;
- HU/multiway ISO;
- plain 3BP;
- squeeze;
- true-threeway and exact 4/5/6-way ordinary SRP;
- clean supported HU 4BP.

Still fail-closed: multiway 4BP, unresolved/reversed/backraise/limp-reraise 4BP and 5bet+.

Local `BetMax` is only natural/mechanical equivalence. Historical near-all-in thresholds are retained as diagnostics/exact-node review evidence. Closed round-2 history distinguishes actual CBet from check and later flop responses.

## Gate02 — Turn CBet

Static/deterministic coverage implemented across all currently supported Flop-CBet parents, including ordinary SRP, post-multiway HU/current multiway, ISO, plain3BP, squeeze and clean HU4BP.

Runtime palette: **25 / 33 / 40 / 50 / 62.5 / 75 / 100%**.

Closed round-3 history proves actual Turn bet/check/call/re-aggression/direct-all-in before River routing.

## Gate03 — River CBet

Complete at static/deterministic level for the currently supported SRP/ISO/plain3BP/squeeze/clean-HU4BP domain.

Runtime palette: **25 / 33 / 50 / 75 / 100%** with natural Hero/HU/deepest-all-live `BetMax` equivalence only.

## Gate04 — Flop Float

Complete at static/deterministic level.

Canonical ownership is first flop action, `AmountToCall=0`, exact LAST/IP, preflop caller/non-initiator, with the expected PFA having skipped CBet.

Coverage includes source-anchored HUSB / `3wBBvSB`, six-max ordinary SRP, multiway, ISO, plain3BP/squeeze and one conservative clean caller-IP 4BP topology.

Gate04R repaired pure-coldcaller 3BP reachability using `lastraised1` final-aggressor reconstruction.

Closed history proves actual Float, check-back, raise-call, re-aggression and runtime drift.

## Gate05 — Turn Float

Complete at static/deterministic level.

Closed flop parents distinguish:

1. call versus the actual final-preflop-aggressor flop bet;
2. CBet -> raise/XR -> Hero call;
3. Flop Float -> raise/XR -> Hero call;
4. narrow source-repaired unraised `3wBBvSB` parent.

Coverage spans ordinary SRP, post-multiway/current multiway, ISO, plain3BP, squeeze and clean HU4BP. Runtime palette is **25 / 33 / 50 / 75 / 100%**. Closed Turn-Float history provides the safe River-parent bridge.

Canonical audit: `docs/audits/GATE_05_TURN_FLOAT_AUDIT.md`.

## Gate06 — River Float

**Complete at static/deterministic level.**

Major ownership correction: the generic/source River-Float value ladder now has an explicit pot-domain firewall, so it cannot leak into unraised, 5bet+ or unresolved 4BP merely because the current river is HU/3-handed.

Implemented families:

- source/high-ancestry River Float descendants;
- ordinary SRP six-max gaps;
- ISO with caller provenance;
- plain3BP;
- squeeze;
- clean supported HU4BP.

Runtime palette: **25 / 33 / 50 / 75 / 100%**. Natural all-in equivalence follows Hero / exact HU / deepest-all-live multiway geometry. A shortest-only sidepot does not promote the action.

Canonical audit: `docs/audits/GATE_06_RIVER_FLOAT_AUDIT.md`.

## Gate07 — Flop Donk

**Complete at static/deterministic level for the supported chronology domain.**

### Source boundary

The dedicated positive source belongs to `(BBorSB)v2pp` only:

- BTN limp -> SB call -> BB check;
- BTN raise -> SB call -> BB call.

Broad legacy Donk-router membership does not grant that strategy to neighboring pot/range families.

Direct source retains:

- TP/OP/2P+ non-Axx leads with 50/75/POT sizing by board structure;
- draw-heavy/completed POT only when corrected **deepest/all-live SPR <=1.25**;
- <=7 lower-pair Donk50 only on non-completed boards;
- selected draw Donk75, with Axx/completed/2+BW check precedence;
- no generic air/backdoor Donk.

The <=1.25 source threshold was reviewed and retained rather than automatically deleted as short-stack logic. The future Turn-jam plan remains outside Flop ownership.

### Reviewed Flop Donk families

1. native three-handed `(BBorSB)v2pp` source strategy;
2. 4–6h BTN+both-blinds A/P adaptation;
3. HU ordinary-SRP caller reviewed CHECK baseline;
4. residual current-multiway ordinary-SRP caller CHECK baseline;
5. proven ISO OOP caller CHECK baseline;
6. supported plain3BP/squeeze OOP caller CHECK baseline;
7. residual unraised current-multiway professional value/equity lead policy;
8. clean caller-side HU4BP reviewed CHECK baseline.

Still fail-closed: multiway/unresolved 4BP, 5bet+ and reversed/backraise/limp-reraise histories.

### Runtime / history

Runtime palette: **50 / 75 / 100%** via native `BetHalfPot`, `BetThreeFourthPot`, `BetPot`.

Local `BetMax` is allowed only when the requested Donk already reaches Hero stack, exact HU effective stack or deepest/all-live multiway effective stack. Shortest-only sidepot reach cannot promote the whole action.

Closed round-2 Donk history now records actual initial Donk versus initial check, direct-all-in versus sized execution, Donk->raise->call, re-aggression, exact family, direct-source value/low-pair/draw subtype, player count/live mask and plan/runtime drift.

Future Turn Donk must consume CLOSED history rather than a pre-action Donk intention.

Canonical audit: `docs/audits/GATE_07_FLOP_DONK_AUDIT.md`.

## Latest validation

GitHub Actions **run #748** completed **SUCCESS** on commit `9f77647687af6d45165ebe137c064c3e00c40c56`.

The combined job passed 49 numbered lint/strategy steps, including all prior CBet/Float gates plus:

- direct-source Flop Donk;
- 4–6h BTN+blinds adaptation;
- HU/MW-SRP/ISO/plain3BP+squeeze reviewed baselines;
- residual unraised multiway Donk policy;
- clean HU caller-side 4BP baseline;
- Flop Donk runtime sizing/all-in equivalence;
- closed Flop Donk action-history contract.

The Gate07 audit document was committed after that strategy-validation head; documentation-only commits do not change the tested strategy.

## Remaining release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. whole-bot history-aware `f$flop` / `f$turn` / `f$river` / `f$BestBetsize` composition;
3. deterministic OpenHoldem policy replays;
4. Turn/River Donk, Probe and Delayed/no-action attack gates;
5. all 32 defensive nodes;
6. exact-node commitment and final global callback audit;
7. complete regression / unknown-state fail-closed review.

Unsupported multiway/reversed 4BP and 5bet+ ancestry remains fail-closed unless stronger chronology/provenance is added.

## Immediate development direction

Next small gate: **Gate08A — Turn Donk ownership + source/history map**.

Start from `f$cc_hist_flop_donk_valid_parent`, `f$cc_hist_flop_donk_standard_called_parent` and the exact direct-source Flop Donk subtype snapshots. Audit DeepCrusher/Crusher Starting Strategy Turn-Donk descendants before adding six-max P fills.

Do not infer a Turn Donk from a Flop Donk plan alone, and do not import the source Turn-jam plan until the exact executed flop size/history/SPR node proves that it belongs.
