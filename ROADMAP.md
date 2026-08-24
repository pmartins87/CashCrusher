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
- [x] **01K.3C** — audit historical ~50% effective / ~60% Hero-stack CBet promotion. Result: preserve as diagnostics/candidates, not one generic cash action; explicit strategic jams must be owned by exact SRP/ISO/3BP/4BP nodes.
- [x] **01K.3C-4BP** — audit clean 4BP flop explicit-jam question. Result: no generic extra jam branch from historical threshold alone; future exact node-owned jam remains possible when supported.
- [ ] **01K.3D** — revisit `f$Raise_Committed` separately in defensive flop/turn call/raise ownership; it must not be smuggled into CBet sizing.
- [ ] **01K.4** — compose final global `f$allin_on_betsize_balance_ratio` only after all postflop sizing owners that it can affect have been audited.
- [x] **01L** — static dependency/flat-WHEN/global-provenance/multiway-SPR lint PASS on reviewed implementation.
- [x] **01L.2** — deterministic mathematical multiway stack/all-in-equivalence contract tests run in CI.
- [ ] **01M** — deterministic OpenPPL/OpenHoldem CBet policy fixtures/replays PASS.
- [x] **01N.1** — executed flop final-action provenance: CBet vs check-through vs check-call/XR vs CBet-raised histories; plan-v-execution all-in diagnostics.
- [x] **01N.2** — snapshot flop CBet hand/kicker/backdoor/texture provenance needed by Turn source without treating pre-action plan as executed action.
- [ ] **01N.V** — wire history-aware CBet entrypoint into whole-bot `f$flop` and certify markers with OpenHoldem replay/parser fixtures.

No uncovered pot family may inherit an ordinary-SRP child as fallback.

## Gate 02 — Turn CBet

### Foundation / source boundary

- [x] **02A.1** — source-first audit of DeepCrusher + Starting Strategy Turn CBet; separate standard CBet from X/R, CBet-call-raise, donk, probe and delayed histories.
- [x] **02A.2** — portable turn runout descriptors (`completed`, `super-completed`, new straight/flush completion, OC/mOC, undercard, glued OC, pairing).
- [x] **02A.3** — current-turn hand/draw tiers plus carried-flop provenance and Turn size-ID palette.
- [x] **02A.4** — top-level Turn CBet router consumes actual executed flop-CBet history; history mismatch fails closed.

### Ordinary SRP — source-anchored HU descendants

- [x] **02B.1** — true-HU HUSB SB/Button-PFA-IP second-barrel baseline.
- [x] **02B.2** — reduced-HU BTN-PFA-IP vs BB source baseline.
- [x] **02B.3** — reduced-HU BTN-PFA-IP vs SB source baseline.
- [x] **02C.1** — true-HU BB-PFA-OOP after SB limp -> BB raise -> call, ordinary HUBB-CBet subset.
- [x] **02C.2** — reduced-HU SB-PFA-OOP vs BB source-safe subset; preserve source turn-check/XR architecture instead of generic TP+ barrel.

### Ordinary SRP — six-max expansion

- [x] **02D.1** — UTG/HJ/CO PFA IP vs SB/BB P-heavy range adaptation; BTN frequencies are not inherited literally.
- [x] **02D.2** — UTG/HJ/CO PFA OOP vs later nonblind cold caller P-heavy adaptation.
- [x] **02D.3** — ordinary SRP that began flop multiway and became HU only by turn; exact survivor/range-origin policy.
- [x] **02E** — current multiway ordinary-SRP Turn CBet, preserving flop-origin/current-player composition and deepest-effective SPR.

### Other pot families

- [x] **02F** — ISO Turn CBet by surviving original-limper vs post-raise-coldcaller provenance, HU and multiway.
- [x] **02G** — plain 3BP Turn CBet by opener/coldcaller survivor provenance, HU and multiway.
- [x] **02H** — squeeze Turn CBet kept separate from plain 3BP; opener/pre3bet/post3bet survivor origins retained.
- [x] **02I** — clean supported HU 4BP Turn CBet; natural low SPR retained without generic TP+ stackoff.
- [ ] **02I.2** — multiway 4BP Turn CBet remains blocked by the unsupported multiway-4BP flop family.
- [ ] **02I.3** — reversed/backraise/limp-reraise 4BP and 5bet+ only after stronger chronology/source evidence.

### Turn execution / sizing / validation

- [x] **02J.0** — static Turn-CBet strategic coverage/exclusivity audit; residual unsupported states remain diagnostic/fail-closed.
- [x] **02J.1** — exact Turn runtime size adapter: 25/33/40/50/62.5/75/100 using verified native/OpenPPL percentage actions.
- [x] **02J.2A** — stack-sensitive Turn execution geometry with Hero/HU/multiway shallowest+deepest ratios and historical 50/60 diagnostics.
- [x] **02J.2B** — local natural/mechanical `BetMax` only when requested size already reaches Hero stack or every live effective relationship; shortest-only sidepot reach is not promoted.
- [x] **02J.2C** — source audit of historical Turn `TurnMax`/`TurnShove` and ~50/55/60 promotion. Result: no generic near-all-in cash rule; any future strategic shove must be exact-node owned.
- [x] **02J.T** — deterministic static Turn coverage + runtime sizing/all-in-equivalence tests run in CI.
- [ ] **02K** — compose Turn execution adapter into eventual whole-bot `f$BestBetsize` without stealing sizing from Float/Donk/Probe/Delayed/defense nodes.
- [x] **02N** — closed round-3 executed-action provenance for River routing: actual check/bet/all-in/raised-history, plan-v-execution mismatch and turn-state snapshot.
- [ ] **02V** — deterministic OpenPPL/OpenHoldem Turn-CBet fixtures/replays PASS.

## Gate 03 — River CBet

- [x] **03A** — source-first River CBet audit and canonical parent from valid closed Turn-CBet history.
- [x] **03B** — source-anchored ordinary-SRP descendants (HUSB/HUBB/BTN-v-BB/BTN-v-SB/source-safe SB-v-BB subset).
- [x] **03C** — P-heavy six-max SRP gaps, including post-multiway-to-HU and current multiway river states.
- [x] **03D** — ISO River CBet with original-limper versus post-raise-coldcaller provenance retained.
- [x] **03E** — plain 3BP River CBet with opener-call versus post-3bet-coldcaller separation.
- [x] **03F** — squeeze River CBet with opener/pre-squeeze/post-squeeze caller origins retained.
- [x] **03G** — clean supported HU 4BP River CBet; naturally low SPR allowed without generic TP+/OP stackoff.
- [x] **03H.1** — River size/runtime adapter: 25/33/50/75/100.
- [x] **03H.2** — natural/mechanical all-in equivalence using Hero/HU/deepest-multiway effective geometry; short sidepot alone cannot promote.
- [x] **03T** — source, coverage, other-pot, runtime and global lint contracts PASS in CI.
- [ ] **03V** — whole-bot/OpenHoldem replay certification remains pending.

## Gate 04 — Flop Float Bet

### Ownership / source

- [x] **04A** — freeze Float as caller/non-initiator checked-to first-flop action; exact LAST/IP only in first six-max baseline. `MIDDLE` no longer inherits last-to-act Float semantics.
- [x] **04B.1** — true-HU HUSB limp-call versus BB raise source descendant.
- [x] **04B.2** — reduced-HU BB caller IP versus SB PFA (`3wBBvSB`) source descendant, preserving dry/wet and pair-delay distinctions without importing XR stackoff.
- [x] **04C.1** — P-heavy nonblind ordinary-SRP caller-IP versus earlier opener.
- [x] **04C.2** — current multiway ordinary-SRP exact-LAST checked-to stab; 4+ way strongly tightened and pure-air baseline removed.
- [x] **04D** — ISO Float with original-limper versus post-raise-coldcaller provenance, HU and multiway.
- [x] **04E** — plain 3BP and squeeze Float with opener/pre3bet/post3bet caller origins kept separate, HU and multiway.
- [x] **04F** — conservative clean caller-IP 4BP Float for opener4-versus-Hero3bettor chronology; unresolved/reversed/cold4-caller/5bet+ remain fail-closed.
- [x] **04R** — repair pure-coldcall-3bet chronology using actual final preflop aggressor from `lastraised1` + `raisbits1`; preserve Gate04E strategy while making previously unreachable coldcaller branches provable.

### Runtime / history / validation

- [x] **04G.1** — 25/33/50/75/100 OpenPPL runtime sizing.
- [x] **04G.2** — natural all-in equivalence only when reviewed Float size reaches Hero stack, HU effective, or deepest/all-live multiway effective; shortest-sidepot-only reach does not promote.
- [x] **04H** — closed round-2 Float provenance: actual bet, actual check-back, bet-raised-call/re-aggression, all-in drift, family/hand/texture/live-field snapshot.
- [x] **04T** — original Gate04 strategy/topology/coverage/runtime/history suite PASS.
- [x] **04R.T** — repaired caller-side chronology + complete Gate04 regression PASS in GitHub Actions run **#512**.
- [ ] **04V** — whole-bot `f$flop`/`f$BestBetsize` composition and OpenHoldem replay certification pending.

Important boundary: a **standard executed Flop Float is not automatically the parent of Turn Float**. Turn Float requires its own closed-history ownership proof.

## Gate 05 — Turn Float Bet

### History / source ownership

- [x] **05A.1** — source-first audit of `f$move_turn_floatbet`; distinguish missed second-barrel Float from Flop-Float continuation, Delayed Float, Turn CBet and Delayed CBet.
- [x] **05A.2** — audit OpenHoldem `lastraised1/2`, `raisbits1/2`, Hero `did*round2` and `BotsActionsOnThisRoundIncludingChecks` semantics.
- [x] **05A.3** — canonical parent ID 1: supported preflop caller called exactly one clean flop bet from the actual final preflop aggressor, who then yields a checked-to Turn.
- [x] **05A.4** — canonical parent ID 2: Hero CBet -> later raise/XR -> Hero call -> final flop aggressor yields checked-to Turn.
- [x] **05A.5** — canonical parent ID 3: Hero Flop Float -> later raise/XR -> Hero call -> final flop aggressor yields checked-to Turn; strategy still requires separate review.
- [x] **05A.6** — preserve HU-from-HU-flop, post-multiway-to-HU and current-multiway origins; exact HU aggressor can be checked against `headsupchair`.
- [x] **05A.T** — final-aggressor repair + Turn-Float history/opportunity contracts PASS in GitHub Actions run **#512**.

### Direct-source strategy descendants

- [ ] **05B.1** — `3wBBvSB` Facing Bet -> Hero call -> Turn check: source Float50, including completed-vs-non-completed river-plan provenance.
- [ ] **05B.2** — BTN Advanced CBet -> flop raise/XR -> Hero call -> aggressor checks Turn: preserve AIR/A-high source interval 25–40% (current DeepCrusher Turn33) and explicit non-transfer to existing FD/OESD.
- [ ] **05B.3** — audit whether parent ID 3 (Flop Float -> raise -> call) has a direct source descendant or must remain P-only/fail-closed.

### Six-max expansion / runtime

- [ ] **05C** — ordinary SRP six-max Turn Float gaps after direct descendants are frozen.
- [ ] **05D** — ISO Turn Float by exact caller/raiser provenance.
- [ ] **05E** — plain 3BP and squeeze Turn Float, keeping opener/pre3bet/post3bet caller origins separate.
- [ ] **05F** — clean supported 4BP Turn Float and explicit unsupported chronology boundary.
- [ ] **05G** — current multiway and post-multiway-to-HU Turn Float policy.
- [ ] **05H** — sizing, stack geometry, natural all-in equivalence and execution wrapper.
- [ ] **05N** — closed Turn-Float action provenance for River Float routing.
- [ ] **05T** — complete static/deterministic strategy/coverage/runtime/history regression.
- [ ] **05V** — whole-bot/OpenHoldem replay certification.

Gate05A contains **no Turn-Float hand-strength betting policy**. Strategy begins only at 05B.

## Gate 06+ — remaining post-flop attack order

1. River Float Bet
2. Flop Donk Bet
3. Turn Donk Bet
4. River Donk Bet
5. Turn Probe
6. River Probe
7. Delayed CBet / delayed-noaction families

Every node is reviewed source-first, then adapted with T/A/P/X provenance and the same deal-size/HU-origin/action-history context contract.

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
- Compose whole-bot `f$flop` / `f$turn` / `f$river` / `f$BestBetsize` owners without sizing collisions.
- Static OpenPPL validation.
- OpenHoldem parser/runtime validation.
- Scenario/handedness/pot-family coverage audit.
- Fail-closed unknown-state review.
- Replay/regression suite.
- Only then merge a table-ready milestone into `main`.
