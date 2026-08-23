# CashCrusher Roadmap

## Gate 00 — Six-max context architecture

- [x] 00A — Decompose legacy Spin scenarios into strategic properties instead of literal position copies.
- [x] 00B — Build the heads-up 6-max matchup / ancestry matrix for SRP and identify unsupported HU pot families.
- [ ] 00C — Design the OpenPPL context-symbol layer: players, pot type, preflop role, IP/OOP, matchup, SPR and history.
- [ ] 00D — Define SPR buckets and the replacement policy for short-stack commitment/jam rules.
- [ ] 00E — Define true multiway context classes for 3+ players reaching the flop.

## Gate 01+ — Post-flop attack, one node at a time

Planned order after Gate 00 is frozen:

1. Flop CBet
2. Turn CBet
3. River CBet
4. Flop Float Bet
5. Turn Float Bet
6. River Float Bet
7. Flop Donk Bet
8. Turn Donk Bet
9. River Donk Bet
10. Turn Probe
11. River Probe
12. Delayed CBet / delayed-noaction families

Each node is reviewed source-first, then adapted to six-max using the T/A/P/X provenance system.

## Defense

After the attack tree, audit the 32 defensive nodes individually: raise/call versus CBet, Donk, Float, Bet and Raise by sizing family.

## Final structural phases

- Bet-size architecture for deeper stacks.
- Commitment/all-in reconstruction from SPR rather than inherited Spin thresholds.
- Static OpenPPL validation.
- OpenHoldem parser/runtime validation.
- Scenario coverage audit and fail-closed unknown-state review.