# CashCrusher Roadmap

## Gate 00 — six-max context architecture

- [x] **00A** — decompose legacy Spin scenarios into strategic properties instead of literal position copies.
- [x] **00B** — build HU 6-max SRP matchup/ancestry matrix and identify unsupported pot families.
- [x] **00C** — implement OpenPPL context layer: players, pot family, Hero role, absolute/relative position, matchup, history.
- [x] **00D** — implement raw SPR/effective-stack geometry for cash-depth review.
- [x] **00D.2** — preserve explicit multiway shallowest + deepest effective relationships; require coherent dual-bound geometry before multiway strategy.
- [x] **00E** — implement exact true-multiway context/composition classes.
- [x] **00F** — support dynamic 2-6 handed deals and distinguish true HU from preflop-/postflop-reduced HU.
- [ ] **00V** — parser/runtime validation of Gate00 context matrix with deterministic OpenHoldem fixtures.

Gate 00 design/code is frozen enough for strategy work, but it is not release-certified until 00V passes.

## Gate 01 — Flop CBet

### Source/audit and coding safety

- [x] **01A** — source audit and portable CBet combo/texture primitives.
- [x] **01A.2** — handedness-aware source audit v2; true HU HUSB/HUBB ancestry corrected.
- [x] **01A.3** — binding flat-complete-WHEN and per-function provenance contract.
- [x] **01A.4** — corrected short-stack migration rule: stack-sensitive DeepCrusher rules require exact cash-context review; they are not globally banned or forced to zero.
- [x] **01A.5** — per-function Source/Provenance comments are now a hard linter requirement for all `f$cc_*` functions.

### Ordinary one-raise HU families

- [x] **01B.1** — true HU SB/Button PFA IP vs BB ordinary SRP baseline.
- [x] **01B.2** — 3-6h PFA IP vs BB ordinary SRP baseline.
- [x] **01B.3** — 3-6h PFA IP vs SB ordinary SRP baseline.
- [x] **01C.1** — 3-6h SB PFA OOP vs BB ordinary SRP baseline.
- [x] **01C.2** — 3-6h opener PFA OOP vs later-position cold caller baseline (P-heavy).
- [x] **01D** — true HU SB limp -> BB raise -> call, BB PFA OOP baseline.

### Isolation-raise CBet

- [x] **01E.1** — reduced-HU ISO versus original limper, IP/OOP.
- [x] **01E.2** — reduced-HU ISO versus post-raise cold caller, IP/OOP.
- [x] **01E.3** — exact true-threeway ISO with limper/post-raise-coldcaller composition.
- [x] **01E.4** — exact 4/5/6-way ISO with all-limper/mixed/all-coldcaller composition.

### 3-bet-pot and squeeze CBet

- [x] **01F.0** — reconstruct survivor provenance: opener / pre-3bet coldcaller / post-3bet coldcaller.
- [x] **01F.1** — true-HU standard plain 3BP: BB 3bettor OOP vs SB/Button opener-call.
- [x] **01G.1** — 3-6h plain 3BP versus original opener-call, IP/OOP.
- [x] **01G.2** — 3-6h plain 3BP versus post-3bet cold caller, IP/OOP.
- [x] **01H.1** — HU squeeze versus original opener, IP/OOP.
- [x] **01H.2** — HU squeeze versus pre-3bet cold caller, IP/OOP.
- [x] **01H.3** — HU squeeze versus post-3bet cold caller, IP/OOP.
- [x] **01H.4** — multiway plain-3BP/squeeze CBet using exact live opener/pre3bet/post3bet composition.

### 4-bet pots

- [x] **01I.0** — conservative clean 4BP chronology reconstruction from aggregate preflop history.
- [x] **01I.1** — clean HU 4BP: true-HU opener4; reduced-HU opener4-v-3bettor and cold4-v-opener/3bettor, IP/OOP.
- [ ] **01I.2** — multiway 4BP policy after separate review of non-raiser caller provenance.
- [ ] **01I.3** — reversed/limp-reraise/backraise 4BP only if stronger chronology evidence becomes available.
- [ ] **01I.4** — 5bet+ postflop family audit.

### Multiway ordinary SRP

- [x] **01J.1** — true three-way ordinary SRP CBet; legacy 3w ancestry used only where actually supported.
- [x] **01J.2** — exact 4/5/6-way ordinary SRP CBet with new P-theory parent.
- [x] **01J.3** — re-audit all implemented multiway CBet SPR exceptions against deepest-effective geometry; short-only sidepot stacks no longer collapse whole-field SPR.

### Execution / sizing / validation

- [x] **01K.1** — native size-ID adapter: 33/50/75/100 -> `BetThirdPot`/`BetHalfPot`/`BetThreeFourthPot`/`BetPot`.
- [ ] **01K.2** — integrate the local CBet execution adapter into eventual whole-bot `f$BestBetsize` without stealing sizing ownership from other postflop nodes.
- [x] **01K.3A** — source-audit DeepCrusher 50/55/60 commitment mechanisms and implement dual-bound HU/multiway diagnostic geometry.
- [x] **01K.3B** — implement only mechanically forced/equivalent CBet `BetMax`: requested size reaches Hero balance or reaches the deepest/all-live effective relationship. Shortest-only sidepot reach is explicitly not promoted.
- [ ] **01K.3C** — decide strategic near-all-in promotion (historical ~50% effective / ~60% Hero-stack) per exact CBet pot/range/board/hand/SPR node; no global transplant.
- [ ] **01K.3D** — revisit `f$Raise_Committed` separately in defensive flop/turn call/raise ownership; it must not be smuggled into CBet sizing.
- [ ] **01K.4** — compose final global `f$allin_on_betsize_balance_ratio` only after all postflop sizing owners that it can affect have been audited.
- [x] **01L** — static dependency/flat-WHEN/global-provenance/multiway-SPR lint PASS on reviewed implementation.
- [x] **01L.2** — deterministic mathematical multiway stack/all-in-equivalence contract tests run in CI.
- [ ] **01M** — deterministic OpenPPL/OpenHoldem CBet policy fixtures/replays PASS.
- [ ] **01N** — ensure skipped-CBet branches have complete X/C/X/R/turn follow-through before release.

No uncovered pot family may inherit an ordinary-SRP child as fallback.

## Gate 02+ — post-flop attack order after Flop CBet

1. Turn CBet
2. River CBet
3. Flop Float Bet
4. Turn Float Bet
5. River Float Bet
6. Flop Donk Bet
7. Turn Donk Bet
8. River Donk Bet
9. Turn Probe
10. River Probe
11. Delayed CBet / delayed-noaction families

Every node is reviewed source-first, then adapted with T/A/P/X provenance and the same deal-size/HU-origin/flop-origin context contract.

## Defense

After attack coverage is structurally stable, audit the 32 defensive nodes individually:

- raise/call versus CBet;
- raise/call versus Donk;
- raise/call versus Float;
- raise/call versus generic Bet;
- raise/call versus Raise;
- sizing families and actor-specific SPR.

A DeepCrusher commitment helper may be retained, adapted or rejected **per exact node**. The only blanket rule is: do not assume a short-stack threshold or TP+ stack-off frequency still applies at ordinary cash depth without review.

## Final structural phases

- Complete cash-depth betsize architecture.
- Review/adapt commitment/all-in helpers against actual SPR and range geometry.
- Static OpenPPL validation.
- OpenHoldem parser/runtime validation.
- Scenario/handedness/pot-family coverage audit.
- Fail-closed unknown-state review.
- Replay/regression suite.
- Only then merge a table-ready milestone into `main`.
