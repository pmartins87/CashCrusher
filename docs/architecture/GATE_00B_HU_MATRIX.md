# Gate 00B — Heads-Up 6-Max Context / Ancestry Matrix

Status: **DONE**

This gate does not port strategy code yet. It establishes which audited DeepCrusher positional families are legitimate ancestors for each heads-up 6-max post-flop context and where professional six-max theory must fill the gap.

## 1. Core decision

Legacy names such as `HUSB`, `HUBB`, `3wBTNvBB`, `3wSBvBTN` are not copied as new six-max states. They are treated as **sources of strategic knowledge**.

The new decision unit is:

`players × pot_type × preflop_role × postflop_position × matchup/ranges × SPR × board × history`

Absolute seat names remain important because they shape ranges, but they do not replace initiative, IP/OOP, pot type or SPR.

## 2. Legacy HU shells and what they actually contribute

| Legacy family | Hero post-flop geometry | Best six-max use | Warning |
|---|---|---|---|
| `HUSB` | IP in full HU (SB=BTN) versus BB | BvB limp/iso mechanics; generic IP cross-street ideas | Full-HU ranges are much wider than normal 6-max ranges |
| `HUBB` | OOP in full HU versus SB/BTN | BvB limp/iso defense; generic OOP mechanics | Full-HU ranges and shallow stack geometry are format-specific |
| `3wBTNvSB` | IP versus SB | BTN-v-SB is close; earlier-position PFA-v-SB only structural | Earlier opens are much tighter than BTN open |
| `3wBTNvBB` | IP versus BB | BTN-v-BB is close; earlier-position PFA-v-BB structurally useful | Range advantage changes strongly by opener |
| `3wSBvBTN` | OOP versus BTN | OOP PFA/caller shell versus an IP nonblind opponent | Blind-v-BTN ranges are not a substitute for UTG-v-HJ etc. |
| `3wSBvBB` | OOP versus BB | SB-v-BB SRP is the closest legacy match | Still needs deeper-stack sizing/SPR work |
| `3wBBvBTN` | OOP versus BTN | BB caller versus IP opener; useful OOP defense shell | Exact only near BTN-v-BB; early opens differ materially |
| `3wBBvSB` | IP versus SB | BB caller versus SB PFA; BvB caller-IP shell | Wider BvB ranges than most nonblind matchups |

`3wBTNv2p`, `3wSBv2p`, `3wBBv2p`, and `3wBlinds_vBTN` remain multiway sources and are deferred to Gate 00E.

## 3. Single-raised pot matrix

The table below assumes a normal open and one caller. `PFA ancestor` is the best legacy shell when Hero is the opener. `Caller ancestor` is the best legacy shell when Hero is the caller.

Confidence means **ancestry confidence**, not that the strategy may be copied unchanged.

| Open → Call | PFA post-flop | PFA ancestor | Caller ancestor | Confidence / treatment |
|---|---|---|---|---|
| UTG → HJ | OOP | `3wSBvBTN` shell | `3wBBvSB` shell | Low; **P-heavy**. No real Spin range analogue |
| UTG → CO | OOP | `3wSBvBTN` shell | `3wBBvSB` shell | Low; **P-heavy** |
| UTG → BTN | OOP | `3wSBvBTN` shell | `3wBBvSB` shell | Medium-low; strong positional analogy, large range gap |
| UTG → SB | IP | `3wBTNvSB` shell | `3wSBvBTN` shell | Medium; **A/P** by range interaction |
| UTG → BB | IP | `3wBTNvBB` shell | `3wBBvBTN` shell | Medium; **A/P** by range interaction |
| HJ → CO | OOP | `3wSBvBTN` shell | `3wBBvSB` shell | Low; **P-heavy** |
| HJ → BTN | OOP | `3wSBvBTN` shell | `3wBBvSB` shell | Medium-low |
| HJ → SB | IP | `3wBTNvSB` shell | `3wSBvBTN` shell | Medium |
| HJ → BB | IP | `3wBTNvBB` shell | `3wBBvBTN` shell | Medium |
| CO → BTN | OOP | `3wSBvBTN` shell | `3wBBvSB` shell | Medium-low; ranges are closer than early-position cases but still new |
| CO → SB | IP | `3wBTNvSB` shell | `3wSBvBTN` shell | Medium-high structural ancestry |
| CO → BB | IP | `3wBTNvBB` shell | `3wBBvBTN` shell | Medium-high structural ancestry |
| BTN → SB | IP | `3wBTNvSB` | `3wSBvBTN` | High ancestry; mostly **A**, not blind copy |
| BTN → BB | IP | `3wBTNvBB` | `3wBBvBTN` | High ancestry; mostly **A**, not blind copy |
| SB → BB | OOP | `3wSBvBB` | `3wBBvSB` | Highest ancestry; still rework stack/SPR/sizing |

### Important interpretation

`HJ → CO` does **not** become “SB versus BTN strategy.” The legacy `3wSBvBTN` family supplies only the OOP strategic shell: who acts first, how initiative is routed, how check/float/donk/probe histories are represented, and some hand/board heuristics. Six-max professional theory must reconstruct the actual HJ-open versus CO-flat range interaction.

Likewise, `UTG → BB` can use `3wBTNvBB` as an IP-PFA-v-BB shell, but its c-bet frequencies, value thresholds and bluff candidates cannot inherit BTN-v-BB ranges mechanically.

## 4. Four canonical HU strategic families for SRP

The 15 matchups collapse structurally into four first-level families while preserving exact matchup tags underneath:

1. **PFA IP / caller OOP**
   - Legacy roots: `3wBTNvBB`, `3wBTNvSB`.
   - Six-max examples: UTG-v-BB, HJ-v-BB, CO-v-BB, BTN-v-BB, UTG-v-SB, BTN-v-SB.

2. **PFA OOP / caller IP**
   - Legacy root: `3wSBvBTN` as positional shell.
   - Six-max examples: UTG-v-HJ/CO/BTN, HJ-v-CO/BTN, CO-v-BTN.
   - This is the largest new theory gap because Spin does not contain early-position open versus later-position flat range geometry.

3. **Caller OOP / PFA IP**
   - Legacy roots: `3wBBvBTN`, `3wSBvBTN` depending blind seat.
   - Strongest direct case: BB versus BTN.

4. **Caller IP / PFA OOP**
   - Legacy root: `3wBBvSB` as positional shell.
   - Exact BvB case: BB versus SB.
   - Nonblind flats versus earlier opens are new six-max range problems.

These families are routing abstractions only. Matchup-specific range tags remain mandatory.

## 5. HU pot families beyond ordinary SRP

### Limped BvB

Primary ancestry: `HUSB` / `HUBB` plus `3wSBvBB` / `3wBBvSB`.

Classification: mostly **A**. Positional and limped-pot mechanics are useful, but full-HU ranges and shallow commitment rules must not be copied.

### Isolation pots

DeepCrusher already contains explicit `GotRaised_Or_Isolated` routing, which is valuable infrastructure.

Classification: **A/P**. Preserve routing and history semantics; rebuild ranges, sizing and deeper-stack responses.

### Standard 3-bet pots

There is no sufficiently reliable direct Spin ancestor for normal 6-max non-all-in 3-bet-pot strategy.

What can be reused:
- initiative/history router;
- hand classification;
- board texture helpers;
- defensive action taxonomy;
- cross-street state machinery.

What must be rebuilt:
- c-bet/check frequencies;
- range/nut-advantage interpretation;
- raise/call thresholds;
- sizing;
- stack-off rules.

Classification: **P-heavy**, with selective **T/A** infrastructure.

### 4-bet pots that are not already all-in

No valid direct strategic ancestor.

Classification: **P**. Treat as a separate pot family, usually low-SPR but not automatically equivalent to Spin shove logic.

### Squeezed pots that become HU on the flop

A squeezed HU flop carries dead money and ranges different from an ordinary 3-bet pot. It must have its own context flag even if later some nodes share strategy.

Classification: **P** until audited.

## 6. Professional-theory principles authorized to fill six-max gaps

When the source does not answer the spot, additions should be grounded in established NLHE principles and explicitly marked `P`:

- range advantage versus nut advantage;
- IP/OOP equity realization;
- positional range asymmetry by opener/caller seats;
- board coverage and nut-density shifts;
- SPR and stack-to-pot geometry;
- polar versus merged betting incentives;
- blocker/unblocker effects for bluff and bluff-catch selection;
- pot odds / MDF as constraints, not automatic strategy generators;
- multi-street runout effects and range reclassification;
- multiway tightening when more than one opponent remains.

When those principles do not justify a precise hardcoded threshold, the state must remain explicitly unresolved rather than receiving a fabricated rule.

## 7. Decisions frozen by Gate 00B

1. No literal Spin-position-to-six-max-position substitution table will control strategy.
2. Every HU state receives both a structural family and an exact six-max matchup tag.
3. SRP ancestry may be strong enough to reuse the DeepCrusher node structure, but not enough to copy frequencies/ranges automatically.
4. `BTN-v-BB`, `BTN-v-SB`, and `SB-v-BB` are the closest six-max descendants of existing 3-handed shells.
5. Early/middle-position PFA versus later nonblind caller is a major professional-theory gap and must be handled deliberately.
6. 3-bet, 4-bet and squeeze pots are first-class context families; they cannot be disguised as SRP or short-stack all-in branches.
7. Short-stack commitment rules remain quarantined until the dedicated SPR gate.
8. Unknown/unmapped contexts must fail closed rather than silently borrowing an unrelated legacy scenario.

## 8. Next gate

**Gate 00C — OpenPPL context-symbol design.**

Define, without yet porting c-bet strategy, the exact symbols that will identify:
- HU versus multiway;
- six-max Hero and Villain seats;
- IP/OOP;
- SRP / limped / iso / 3BP / 4BP / squeeze;
- Hero preflop role (PFA, caller, 3-bettor, 3-bet caller, etc.);
- exact matchup tag;
- SPR bucket;
- initiative/history state;
- fail-closed behavior when classification is uncertain.