# CashCrusher Status

Last update: 2026-08-24

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime and whole-bot composition gates pass.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem, with 2–6 dealt-player runtime support.
- Preflop is reconstructed to identify post-flop pot/range/history context; this project is not currently replacing preflop strategy.
- Strategic provenance is mandatory: **T / A / P / X**.
- Source-derived and professional-theory rules remain visibly distinguishable.
- Unsupported strategy fails closed instead of leaking from neighboring pot families.
- OpenPPL uses flat complete `WHEN` rules; indentation is never logical scope.
- A positive bet owns only that street action; later barrels, raise response and stackoff are separate owners.
- Pre-action plan markers never prove executed history. Later streets consume CLOSED `did*`, `raisbits*`, `lastraised*` and explicit snapshots.

## Binding stack-depth migration rule

DeepCrusher short-stack logic is a **review flag, not an automatic deletion/zeroing rule**.

For every stack-sensitive inherited rule, review the exact pot/range/board/history/effective-stack/SPR node. Retain, adapt or reject locally with T/A/P/X provenance. Do not assume a threshold transfers unchanged to 100bb cash, and do not assume it becomes invalid merely because the target starts deeper.

This applies to TP+/draw commitment, `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, historical ~50/55/60% thresholds, `BetMax` and related mechanisms.

## Gate00 — context foundation

Implemented mechanically:

- dynamic 2–6 handed deal size;
- true-HU, preflop-reduced HU and postflop-reduced HU distinction;
- canonical UTG/HJ/CO/BTN/SB/BB positions;
- flop-entry/current-live masks;
- exact HU Villain identity/matchup;
- pot-family and Hero-role taxonomy;
- ordinary SRP / ISO / plain3BP / squeeze / clean 4BP chronology helpers;
- final-aggressor reconstruction from persisted history;
- shallowest + deepest multiway effective geometry;
- context/history consistency guards.

HU uses exact effective stack. Multiway retains shallowest and deepest relationships separately; one short sidepot player cannot collapse the whole decision into short-stack policy.

OpenHoldem parser/runtime certification for Gate00 remains pending.

## Gates01–03 — CBet line

### Gate01 Flop CBet

Static/deterministic baseline covers ordinary HU/reduced-HU SRP IP/OOP, true-HU limp-raised PFA, HU/multiway ISO, plain3BP, squeeze, true-threeway/exact 4–6way ordinary SRP and clean supported HU4BP.

Still fail-closed: multiway 4BP, unresolved/reversed/backraise/limp-reraise 4BP and 5bet+.

Local `BetMax` means natural/mechanical equivalence only. Historical near-all-in thresholds remain diagnostics/exact-node review evidence. CLOSED round-2 history distinguishes actual CBet, check and later flop response.

### Gate02 Turn CBet

Static/deterministic coverage exists for all currently supported Flop-CBet parents: ordinary SRP, post-multiway HU/current multiway, ISO, plain3BP, squeeze and clean HU4BP.

Runtime palette: **25 / 33 / 40 / 50 / 62.5 / 75 / 100%**. CLOSED round-3 history proves actual Turn bet/check/call/re-aggression/direct-all-in before River routing.

### Gate03 River CBet

Complete at static/deterministic level for the supported SRP/ISO/plain3BP/squeeze/clean-HU4BP domain.

Runtime palette: **25 / 33 / 50 / 75 / 100%** with natural Hero/HU/deepest-all-live `BetMax` equivalence only.

## Gates04–06 — Float line

### Gate04 Flop Float

Complete at static/deterministic level. Canonical ownership is caller/non-initiator, first flop action, `AmountToCall=0`, exact LAST/IP in the reviewed baseline, with expected PFA having skipped CBet.

Coverage includes HUSB / `3wBBvSB` source ancestry, six-max ordinary SRP, multiway, ISO, plain3BP/squeeze and a conservative clean caller-IP 4BP topology. Gate04R repaired pure-coldcaller 3BP reachability with `lastraised1` final-aggressor reconstruction.

### Gate05 Turn Float

Complete at static/deterministic level. CLOSED flop parents distinguish simple call-v-PFA, CBet->raise/XR->call, FlopFloat->raise/XR->call and the narrow source-repaired unraised `3wBBvSB` parent.

Coverage spans ordinary SRP, post-multiway/current multiway, ISO, plain3BP, squeeze and clean HU4BP. Runtime palette: **25 / 33 / 50 / 75 / 100%**. CLOSED Turn-Float history provides the River bridge.

Canonical audit: `docs/audits/GATE_05_TURN_FLOAT_AUDIT.md`.

### Gate06 River Float

Complete at static/deterministic level for source/high-ancestry descendants plus six-max ordinary SRP, ISO, plain3BP, squeeze and clean supported HU4BP.

A pot-domain firewall prevents generic River-Float value logic from leaking into unraised, unresolved 4BP or 5bet+ merely because the River is HU/3-handed.

Runtime palette: **25 / 33 / 50 / 75 / 100%**; shortest-only sidepot reach cannot promote the whole action.

Canonical audit: `docs/audits/GATE_06_RIVER_FLOAT_AUDIT.md`.

## Gate07 — Flop Donk

**Complete at static/deterministic level for the supported chronology domain.**

Dedicated positive source belongs to `(BBorSB)v2pp` only:

- BTN limp -> SB call -> BB check;
- BTN raise -> SB call -> BB call.

Reviewed families:

1. native three-handed `(BBorSB)v2pp` source strategy;
2. 4–6h BTN+both-blinds A/P adaptation;
3. HU ordinary-SRP caller reviewed CHECK baseline;
4. residual current-multiway ordinary-SRP caller CHECK baseline;
5. proven ISO OOP caller CHECK baseline;
6. supported plain3BP/squeeze OOP caller CHECK baseline;
7. residual unraised current-multiway professional value/equity lead policy;
8. clean caller-side HU4BP reviewed CHECK baseline.

Direct source retains TP/OP/2P+ non-Axx leads, <=7 lower-pair non-completed Donk50, selected draw Donk75 and the reviewed deepest/all-live `SPR <= 1.25 -> POT` source sizing. That SPR rule was retained after review rather than automatically deleted as short-stack logic. Its stated future Turn-jam plan remains outside Flop ownership.

Runtime palette: **50 / 75 / 100%** with natural/mechanical BetMax only. CLOSED round-2 Donk history records actual initial Donk/check, raise-call/re-aggression, family/source subtype, player/live-field snapshot and runtime drift.

Canonical audit: `docs/audits/GATE_07_FLOP_DONK_AUDIT.md`.

## Gate08 — Turn Donk

### Gate08A ownership/history — PASS

Turn Donk is now structurally separated from Hero-initiative continuation.

Approved CLOSED flop parent IDs:

1. reviewed Flop-Donk opportunity -> Hero CHECK -> one clean CALL against one later live flop aggressor, who owns final flop aggression (**X/C**);
2. executed Flop Donk -> later opponent RAISE -> Hero CALL, no Hero re-aggression, raiser remains live/final aggressor (**B/C**).

A standard Flop Donk that was merely called and left Hero final aggressor is **not** Turn Donk. Standard CBet/Float continuations are also separate owners.

Turn opportunity requires first Hero Turn action, `AmountToCall=0`, FIRST/MIDDLE (not LAST), exact valid parent and no Hero-owned final flop aggression.

Gate08A contracts passed GitHub Actions **run #758**.

### Gate08B direct native `(BBorSB)v2pp` source — PASS

Before adding strategy, Gate07 history was extended to preserve two source CHECK substates that the simple false Donk decision could not distinguish:

- good/medium source draw check candidate;
- high-card/backdoor source call candidate.

Direct source result:

- **draw X/C -> Turn Donk75**: implemented and executable from CLOSED history;
- **high-air X/C -> exact 2HC OESD/FD pickup -> Turn Donk50**: coded but fail-closed until future defense proves the source <=33% flop-call price;
- **draw Donk -> raise -> medium-draw call -> Turn Donk75**: coded but fail-closed until future Donk-vs-Raise defense proves medium-draw + normal/~<=3x raise eligibility.

The high-air mature-C++ TP+/2P+ current-strength reclassification was deliberately **not** copied as primary-source policy. Native TP+/OP and MP/BP X/C sections say `nothing here`, so Gate08B creates no generic Turn lead for them.

No generic Turn jam, stackoff, `HandPower`, random or commitment threshold was introduced.

Canonical audit: `docs/audits/GATE_08B_TURN_DONK_DIRECT_SOURCE_AUDIT.md`.

The combined source/history/static suite passed GitHub Actions **run #776** on commit `0aff3bcd0385daf5c6711b173d3ce9e9b0217f23`. A documentation commit followed without strategy changes.

## Remaining Gate08 source mapping

The next source-first descendants must be audited and mapped one at a time by strategic/range ancestry rather than literal old seat labels:

1. HUBB;
2. `3wSBvBTN`;
3. `3wSBvBB`;
4. `3wBBvBTN`;
5. only then six-max P-heavy gap families and runtime/history closure.

The `3wSBvBB` 75/100 low-SPR rule is explicitly a cash-depth review item: neither automatic deletion nor automatic transplant is allowed.

## Remaining release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. whole-bot history-aware `f$flop` / `f$turn` / `f$river` / `f$BestBetsize` composition;
3. deterministic OpenHoldem policy replays;
4. remaining Turn/River Donk, Probe and Delayed/no-action attack gates;
5. all 32 defensive nodes;
6. exact-node commitment and final global callback audit;
7. complete regression / unknown-state fail-closed review.

Unsupported multiway/reversed 4BP and 5bet+ ancestry remains fail-closed unless stronger chronology/provenance is added.

## Immediate development direction

Next small gate: **Gate08C.1 — HUBB Turn Donk source mapping**.

Audit the exact HUBB Flop X/C source state and map it to CashCrusher true-HU / reduced-HU ancestry without treating all OOP HU callers as identical. Keep opponent 2Bar exploitation, good-draw checks, weak-GS/air block-donks and MP/BP source conditions as separate subfamilies. Any source sizing gap filled from detailed C++ must remain labeled A, not T.
