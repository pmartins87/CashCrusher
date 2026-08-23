# CashCrusher context validation matrix

This is the acceptance contract for Gate 00C/00D/00E. It is intentionally independent of poker policy.

Legend:

- PF = preflop pot family
- Role = `f$cc_pf_role_id`
- Rel = Hero relative post-flop position
- Valid = `f$cc_context_valid`
- ISO/SQ = proven subtype flags

## HU one-raise pots

| # | Line reaching flop | Hero | PF | Role | HU matchup | Rel | ISO | Expected |
|---:|---|---|---:|---:|---|---|---|---|
| 1 | UTG raise, BB call | UTG | 2 | 1 | 16 | IP/Last | no | valid |
| 2 | HJ raise, CO call | HJ | 2 | 1 | 23 | OOP/First | no | valid |
| 3 | HJ raise, BB call | HJ | 2 | 1 | 26 | IP/Last | no | valid |
| 4 | CO raise, BTN call | CO | 2 | 1 | 34 | OOP/First | no | valid |
| 5 | CO raise, SB call | CO | 2 | 1 | 35 | IP/Last | no | valid |
| 6 | BTN raise, BB call | BTN | 2 | 1 | 46 | IP/Last | no | valid |
| 7 | SB raise, BB call | SB | 2 | 1 | 56 | OOP/First | no | valid |
| 8 | BTN raise, BB call | BB | 2 | 2 | 64 | OOP/First | no | valid |
| 9 | SB raise, BB call | BB | 2 | 2 | 65 | IP/Last | no | valid |

## ISO and unraised pots

| # | Line reaching flop | Hero | PF | Role | Subtype | Expected |
|---:|---|---|---:|---:|---|---|
| 10 | UTG limp, HJ raise, UTG call | HJ | 2 | 1 | ISO proven | valid |
| 11 | CO limp, BTN raise, CO call | CO | 2 | 2 | ISO proven | valid |
| 12 | BTN limp, SB call, BB check | BB | 1 | 9 | unraised | valid |
| 13 | HJ limp, BB check | HJ | 1 | 8 | unraised | valid |

## 3-bet pots

| # | Line reaching flop | Hero | PF | Role | 3BP subtype | Expected |
|---:|---|---|---:|---:|---|---|
| 14 | BTN raise, SB 3bet, BTN call | SB | 3 | 3 | plain proven | valid |
| 15 | BTN raise, SB 3bet, BTN call | BTN | 3 | 4 | plain proven | valid |
| 16 | UTG raise, HJ call, BTN 3bet, UTG call, HJ fold | BTN | 3 | 3 | squeeze proven | valid |
| 17 | UTG raise, HJ call, BTN 3bet, UTG call | UTG | 3 | 4 | squeeze proven if Hero/other raiser reconstruction sees HJ call | valid |
| 18 | HJ raise, CO call, BTN 3bet, HJ folds, CO calls | CO | 3 | 5 | subtype may remain unknown because Hero was not a raiser | valid mechanically; strategy must preserve cold-call role |
| 19 | UTG limp, BTN raise, UTG 3bet, BTN call | BTN | 3 | 4 | reversed first-orbit order | 3bet subtype unknown; do NOT call this plain 3BP/squeeze |

## Multiway

| # | Line reaching flop | Hero | Players | PF | Role | Relative position | Expected |
|---:|---|---|---:|---:|---:|---|---|
| 20 | UTG raise, BTN call, BB call | UTG | 3 | 2 | 1 | First | exact opponent mask BTN+BB |
| 21 | CO raise, BTN call, BB call | CO | 3 | 2 | 1 | First | exact opponent mask BTN+BB |
| 22 | BTN raise, SB call, BB call | BTN | 3 | 2 | 1 | Last | legacy `3wBTNv2p` shape only |
| 23 | BTN raise, SB call, BB call | SB | 3 | 2 | 2 | First | legacy `3wSBv2p` shape only |
| 24 | BTN raise, SB call, BB call | BB | 3 | 2 | 2 | Middle | legacy `3wBBv2p` shape only |
| 25 | UTG raise, HJ call, CO call, BB call | UTG | 4 | 2 | 1 | First | new-theory parent required |
| 26 | CO raise, BTN call, SB call, BB call | BTN | 4 | 2 | 2 | Middle/Last according to actual live order | preserve exact Position; no invented legacy mapping |

## 4-bet and unsupported depth of preflop aggression

| # | Line | PF | Role | Expected |
|---:|---|---:|---:|---|
| 27 | BTN raise, SB 3bet, BTN 4bet, SB call; Hero BTN | 4 | 6 | mechanically valid, 4BP strategy not yet covered |
| 28 | BTN raise, SB 3bet, BTN 4bet, SB call; Hero SB | 4 | 7 | mechanically valid, generic 4bet-caller role only |
| 29 | 4+ raises before flop and postflop still exists | 5 | 0/currently undefined | mechanically classifiable but policy must fail closed |

## Mandatory fail-closed states

| # | Fault | Expected |
|---:|---|---|
| 30 | `nplayersdealt = 5` | invalid in strict v0.1 six-max envelope |
| 31 | missing/negative canonical position chair | invalid |
| 32 | duplicate canonical position chairs | invalid |
| 33 | Hero does not map to UTG/HJ/CO/BTN/SB/BB | invalid |
| 34 | Hero no longer in `playersplayingbits` | invalid |
| 35 | HU but `Position = Middle` | invalid |
| 36 | one raise reported but `BitCount(raisbits1) != 1` | invalid |
| 37 | no raise reported but historical raiser bit exists | invalid |
| 38 | `bblind <= 0` | invalid |
| 39 | `potcommon <= 0` post-flop | invalid |
| 40 | opponent live-mask bitcount != `nopponentsplaying` | multiway exact context invalid |

## SPR acceptance checks

The following must hold regardless of action order within the current street:

1. Hero street-start stack = `(balance + currentbet) / bblind`.
2. Villain street-start stack uses the same reconstruction.
3. HU effective stack is the minimum of the two.
4. Current street bet sizes do not inflate the SPR denominator; denominator is `potcommon / bblind`.
5. A short third player may lower the coarse multiway SPR, but actor-specific nodes must not use that as the effective stack versus a different deep bettor.
6. `f$allin_on_betsize_balance_ratio` remains `0.00` throughout Gate 00 and later unless an explicit architecture decision replaces it.

## Parser/runtime gate

This matrix is a design/static contract. Before a CashCrusher formula is released for table testing, each case needs either:

- a synthetic OpenHoldem replay/log state; or
- a deterministic runtime fixture that prints the context symbols.

No strategic PASS is inferred from static inspection alone.
