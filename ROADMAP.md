# CashCrusher Roadmap

## Gate 00 — six-max context architecture

- [x] **00A** — decompose legacy Spin scenarios into strategic properties instead of literal position copies.
- [x] **00B** — build HU 6-max SRP matchup/ancestry matrix and identify unsupported pot families.
- [x] **00C** — implement OpenPPL context layer: players, pot family, Hero role, absolute/relative position, matchup, history.
- [x] **00D** — implement raw SPR/buckets and quarantine inherited short-stack commitment/jam conversion.
- [x] **00E** — implement exact true-multiway context/composition classes.
- [x] **00F** — support dynamic 2-6 handed deals and distinguish true HU from preflop-/postflop-reduced HU.
- [ ] **00V** — parser/runtime validation of the Gate00 context matrix with deterministic fixtures.

Gate 00 design/code is frozen enough for strategy work, but it is not release-certified until 00V passes.

## Gate 01 — Flop CBet

### Source/audit and safety

- [x] **01A** — source audit and portable CBet combo/texture primitives.
- [x] **01A.2** — handedness-aware source audit v2; true HU HUSB/HUBB ancestry corrected.
- [x] **01A.3** — binding OpenPPL flat-WHEN/provenance coding contract.
- [x] **01A.4** — deep-stack commitment decoupling: TP+/overpair no longer imply stack-off; `f$Raise_Committed`, `StackOffDraws` and global auto-jam are quarantined.

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
- [ ] **01E.3** — true multiway ISO CBet with live limper/coldcaller composition.

### 3-bet-pot CBet

- [x] **01F.0** — reconstruct 3BP survivor provenance: opener / pre-3bet coldcaller / post-3bet coldcaller.
- [x] **01F.1** — true-HU standard plain 3BP: BB 3bettor OOP vs SB/Button opener-call.
- [x] **01G.1** — 3-6h plain 3BP versus original opener-call, IP/OOP.
- [x] **01G.2** — 3-6h plain 3BP versus post-3bet cold caller, IP/OOP.
- [ ] **01H.1** — squeeze versus original opener, IP/OOP.
- [ ] **01H.2** — squeeze versus pre-3bet cold caller, IP/OOP.
- [ ] **01H.3** — squeeze versus post-3bet cold caller, IP/OOP.
- [ ] **01H.4** — multiway squeeze/3BP CBet using exact live-range composition.

### Higher re-raised pots and multiway SRP

- [ ] **01I** — 4BP CBet, only after separate range/SPR audit.
- [ ] **01J.1** — true three-way ordinary SRP CBet using legacy 3w ancestry where valid.
- [ ] **01J.2** — four-way+ ordinary SRP CBet with new P-theory parent.

### Execution/validation

- [ ] **01K** — map CBet size IDs (~33/~50/~75) into final OpenPPL betsize runtime.
- [ ] **01L** — static dependency/safety lint PASS on current review head.
- [ ] **01M** — deterministic CBet policy fixtures/replays PASS.
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

However, a defense dependency may be brought forward when an attack node explicitly creates an X/C or X/R plan; no dangling strategic plan is allowed into a release branch.

### Binding defense/commitment rule

A made-hand label is never sufficient to authorize stacks by itself. In particular:

- TP is one pair;
- overpair is one pair;
- TP+ in DeepCrusher is source classification, not CashCrusher commitment permission;
- every call/raise/jam response must be rebuilt in the exact node from range provenance, board/runout, sizing, position and actor-specific SPR.

## Final structural phases

- Complete deeper-stack betsize architecture.
- Explicit commitment/all-in nodes from actual SPR; no global half-stack auto-jam.
- Static OpenPPL validation.
- OpenHoldem parser/runtime validation.
- Scenario/handedness/pot-family coverage audit.
- Fail-closed unknown-state review.
- Replay/regression suite.
- Only then merge a table-ready milestone into `main`.
