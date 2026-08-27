# CashCrusher Status

Last update: 2026-08-24

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime, whole-bot composition and replay gates pass.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem, with 2–6 dealt-player runtime support.
- Preflop is reconstructed to identify pot/range/history context; this project is not currently replacing preflop strategy.
- Strategic provenance is mandatory: **T / A / P / X**.
- Source-derived and professional-theory rules remain visibly distinguishable.
- Unsupported strategy fails closed instead of leaking from neighboring pot families.
- OpenPPL uses flat complete `WHEN` rules; indentation is never logical scope.
- A positive bet owns only that street action. Later barrels, raise response and stackoff are separate owners.
- Pre-action plan markers never prove executed history. Later streets consume CLOSED `did*`, `raisbits*`, `lastraised*` and explicit snapshots/defense provenance.

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

HU uses exact effective stack. Multiway preserves shallowest and deepest relationships separately; one short sidepot player cannot collapse the entire decision into short-stack policy.

OpenHoldem parser/runtime certification for Gate00 remains pending.

## Gates01–03 — CBet line

### Gate01 Flop CBet

Static/deterministic baseline covers ordinary HU/reduced-HU SRP IP/OOP, true-HU limp-raised PFA, HU/multiway ISO, plain3BP, squeeze, true-threeway/exact 4–6way ordinary SRP and clean supported HU4BP.

Still fail-closed: multiway 4BP, unresolved/reversed/backraise/limp-reraise 4BP and 5bet+.

Local `BetMax` means natural/mechanical equivalence only. Historical near-all-in thresholds remain diagnostics/exact-node evidence. CLOSED round-2 history distinguishes actual CBet, check and later flop response.

### Gate02 Turn CBet

Static/deterministic coverage exists for all currently supported Flop-CBet parents: ordinary SRP, post-multiway HU/current multiway, ISO, plain3BP, squeeze and clean HU4BP.

Runtime palette: **25 / 33 / 40 / 50 / 62.5 / 75 / 100%**. CLOSED round-3 history proves actual Turn bet/check/call/re-aggression/direct-all-in before River routing.

### Gate03 River CBet

Complete at static/deterministic level for the supported SRP/ISO/plain3BP/squeeze/clean-HU4BP domain.

Runtime palette: **25 / 33 / 50 / 75 / 100%** with natural Hero/HU/deepest-all-live `BetMax` equivalence only.

## Gates04–06 — Float line

### Gate04 Flop Float

Complete at static/deterministic level. Canonical ownership is caller/non-initiator, first flop action, `AmountToCall=0`, exact LAST/IP in the reviewed baseline, with expected PFA having skipped CBet.

Coverage includes HUSB / `3wBBvSB` source ancestry, six-max ordinary SRP, multiway, ISO, plain3BP/squeeze and conservative clean caller-IP 4BP topology. Gate04R repaired pure-coldcaller 3BP reachability with `lastraised1` final-aggressor reconstruction.

### Gate05 Turn Float

Complete at static/deterministic level. CLOSED flop parents distinguish simple call-v-PFA, CBet->raise/XR->call, FlopFloat->raise/XR->call and narrow source-repaired unraised `3wBBvSB` ancestry.

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

Direct source retains TP/OP/2P+ non-Axx leads, <=7 lower-pair non-completed Donk50, selected draw Donk75 and reviewed deepest/all-live `SPR <= 1.25 -> POT` sizing. That SPR rule was retained after exact review rather than automatically deleted as short-stack logic. Its stated future Turn-jam plan remains outside Flop ownership.

Runtime palette: **50 / 75 / 100%** with natural/mechanical BetMax only. CLOSED round-2 Donk history records actual initial Donk/check, raise-call/re-aggression, family/source subtype, player/live-field snapshot and runtime drift.

Canonical audit: `docs/audits/GATE_07_FLOP_DONK_AUDIT.md`.

## Gate08 — Turn Donk

### Gate08A — ownership/history — PASS

Turn Donk is structurally separated from Hero-initiative continuation.

Approved CLOSED flop parent IDs are now:

1. reviewed Flop-Donk opportunity -> Hero CHECK -> one clean CALL against one later live flop aggressor (**X/C**);
2. executed Flop Donk -> later opponent RAISE -> Hero CALL, no Hero re-aggression (**B/C**);
3. **other actual clean flop X/C** outside Gate07-Flop-Donk ancestry, added during the SBvBB audit so `PFA checks -> Villain bets -> PFA calls` can correctly lose initiative and become a real Turn-Donk opportunity.

Parent 3 grants ownership/opportunity only. Exact strategy still requires a child to prove its own range/topology/provenance.

A standard Flop Donk merely called while Hero remains final aggressor is not Turn Donk. Standard CBet/Float continuations are separate owners.

Turn opportunity requires first Hero Turn action, `AmountToCall=0`, FIRST/MIDDLE (not LAST), one valid exact parent and no Hero-owned final flop aggression.

### Gate08B — direct native `(BBorSB)v2pp` — PASS

Direct source descendants:

- source draw X/C -> **Turn Donk75**;
- high-air X/C -> exact 2HC OESD/FD pickup -> **Turn Donk50**, fail-closed until future Flop defense proves source <=33% call price;
- draw Donk -> raise -> medium-draw call -> **Turn Donk75**, fail-closed until future Donk-vs-Raise defense proves medium-draw + normal/~<=3x eligibility.

Mature-only high-air TP+/2P+ reclassification was not promoted to primary source. No generic Turn jam/stackoff/HandPower/random threshold was imported.

Canonical audit: `docs/audits/GATE_08B_TURN_DONK_DIRECT_SOURCE_AUDIT.md`.

### Gate08C.1 — HUBB / BB-v-SB — PASS

Exact true-HU and reduced-HU BvB ancestry mapped separately.

Source/high-ancestry behavior includes stat-gated TP+/OP/2P+, good-draw checks, weak-GS/air Donk25 and price-sensitive MP/BP branches. Required `>50` versus `<=50` flop-call evidence is defense-owned and therefore fail-closed until that defensive node is wired.

Canonical audit: `docs/audits/GATE_08C1_TURN_DONK_HUBB_AUDIT.md`.

### Gate08C.2 — SB-v-BTN — PASS

Source ancestry: BTN open -> SB call -> actual flop X/C, literal 3h and exact 4–6h descendant kept distinct.

Mapped source descendants include:

- Axx flop TP+ X/C -> direct Turn Donk100 source branch;
- non-Axx carried TP+ -> explicit no-donk branch;
- carried MP/BP -> explicit no-donk branch;
- source draw X/C -> improvement on undercard -> Donk75, otherwise check;
- source high-air X/C -> exact 2HC draw pickup -> Donk50.

No-made branches require future defense-owned source X/C provenance. Mature-only made-hand reclassification of the high-air branch remains a visible source gap instead of being silently imported.

Canonical audit: `docs/audits/GATE_08C2_TURN_DONK_SBVBTN_AUDIT.md`.

### Gate08C.3 — SB-v-BB — PASS

Primary source `6- CRUSHFEST 3wSBvBB` preserves two separate preflop origins:

- SB limp -> BB check;
- SB open -> BB call.

This audit discovered and repaired the Gate08A parent-ownership hole described above: the MNR line may be `SB PFA -> flop CHECK -> BB BET -> SB CALL`, which is a genuine Turn-Donk state despite not originating in Gate07 Flop Donk.

Source draw-X/C branch:

- improved draw + Turn OC -> source Donk **75–100%**;
- improved draw + Turn UC -> CHECK with future X/R owned by Turn defense.

The mature short-stack implementation additionally used `SPR <= 1.80 -> POT` and scheduled a River shove. At this gate CashCrusher keeps **75%**, the direct source lower bound, as an A deterministic deep-cash resolution; the 100% upper bound remains explicitly recorded for later exact-node cash-SPR review. It is not globally banned. No River shove is scheduled from Turn.

Limped/MNR draw-call price classes remain defense-owned markers and fail closed until implemented.

Canonical audit: `docs/audits/GATE_08C3_TURN_DONK_SBVBB_AUDIT.md`.

### Gate08C.4 — BB-v-BTN — PASS

Primary/current source is **`12- NOVO CRUSHFEST 3wBBvBTN`**. The older `7- CRUSHFEST 3wBBvBTN - ok` is corroborating only; mature DeepCrusher resolves ambiguities as A.

Exact ancestry: BTN open -> BB call -> actual BB X/C versus BTN, with literal 3h versus 4–6h structural descendants separated.

The Q8/Q9 Turn-Donk line is narrowed to the mature source's **flop JustTopPair X/C** state. Because TP usually X/Rs versus <=50%, actual source-valid TP X/C requires future Flop-defense proof; a top-pair snapshot plus a call is not enough.

Mapped source descendants:

- paired Turn becoming actual trips/boat/quads: completed -> **Donk75**, non-completed -> **Donk50**;
- 4-card straight + made straight -> **Donk50**;
- 4-card flush + K/A-high contributing flush -> **Donk50**;
- 4-card flush Q-high or worse -> **CHECK**;
- other made straight/flush: OC -> CHECK; UC + exact >50 flop call -> CHECK; UC + exact <=50 flop call -> BET, with **50% as A** because source leaves this size open and mature code fills it;
- Turn rank neither strict OC nor strict UC -> source gap;
- mature residual current 2P+ Turn50 fallback -> **X as direct-source rule**, not executed;
- separate source Draw section: missed no-made draw -> explicit CHECK; a no-made flop draw that completes is not silently merged into the TP-section Q8 tree.

River50 follow-through mentioned by source is later-street ownership and is not scheduled here.

Canonical audit: `docs/audits/GATE_08C4_TURN_DONK_BBVBTN_AUDIT.md`.

### Current validation

GitHub Actions **run #826** passed on commit `840d5b36050e30bc270a687cf74d00652140df4a`.

The suite now passes **55 strategy/history/runtime/static contracts**, including Turn Donk history + native + HUBB + SBvBTN + SBvBB + BBvBTN.

A docs-only audit commit follows that tested strategy commit; parser/runtime certification is still pending.

## Remaining Gate08 work

Source/high-ancestry Turn-Donk mapping is now complete for the currently identified legacy source families. Next work is structural, not another seat-label transplant:

1. audit six-max **residual ordinary-SRP / current-multiway / post-multiway** Turn-Donk gaps;
2. audit **ISO** Turn-Donk gaps;
3. audit **plain 3BP / squeeze** Turn-Donk gaps;
4. audit **clean supported 4BP** Turn-Donk gaps;
5. close Turn-Donk **runtime sizing / natural all-in equivalence**;
6. close executed Turn-Donk history for River Donk/Probe ownership;
7. then start **Gate09 River Donk**.

P-heavy positive leads must be justified by exact range/topology; otherwise the reviewed result may legitimately be CHECK. Missing Flop-defense price/class provenance remains fail-closed rather than guessed.

## Remaining release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. whole-bot history-aware `f$flop` / `f$turn` / `f$river` / `f$BestBetsize` composition;
3. deterministic OpenHoldem policy replays;
4. remaining Turn/River Donk, Probe and Delayed/no-action attack gates;
5. all 32 defensive nodes, including the price/class markers already reserved by Turn-Donk source nodes;
6. exact-node commitment and final global callback audit;
7. complete regression / unknown-state fail-closed review.

Unsupported multiway/reversed 4BP and 5bet+ ancestry remains fail-closed unless stronger chronology/provenance is added.

## Immediate development direction

Next small gate: **Gate08D.1 — residual ordinary-SRP Turn Donk coverage audit**.

First enumerate actual clean-X/C states not already owned by HUBB/SBvBTN/SBvBB/BBvBTN, preserving true-HU, preflop-reduced-HU, postflop-reduced-HU and current-multiway origins. Review whether each exact range has a justified cash-game lead subset; otherwise mark a deliberate CHECK baseline. Do not allow a generic OOP/no-initiative rule to manufacture donks across all SRP matchups.
