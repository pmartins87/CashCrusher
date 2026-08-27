# CashCrusher context validation matrix v2

This is the acceptance contract for Gate 00C/00D/00E/00F. It is intentionally independent of final poker policy.

Legend:

- `D` = players dealt (`f$cc_deal_size`)
- `F` = players reaching flop (`f$cc_flop_entry_count`)
- `P` = players currently playing
- `PF` = preflop pot family
- `Role` = `f$cc_pf_role_id`
- `Rel` = Hero relative postflop position
- `Origin` = `f$cc_hu_origin_id`
- `ISO/HULR/SQ` = proven ISO / true-HU limp-raise / squeeze subtype
- `Valid` = `f$cc_context_valid`

## A. Dynamic six-max table handedness

The bot targets a six-max cash table but must support hands dealt 2h through 6h as seats become empty or players sit out.

| # | Dealt players | Canonical positions that must exist | Hero sample | Expected Hero ID | Expected |
|---:|---:|---|---|---:|---|
| A1 | 6 | UTG HJ CO BTN SB BB | UTG | 1 | valid |
| A2 | 6 | UTG HJ CO BTN SB BB | HJ | 2 | valid |
| A3 | 5 | HJ CO BTN SB BB | first nonblind / HJ | 2 | valid |
| A4 | 5 | HJ CO BTN SB BB | BTN | 4 | valid |
| A5 | 4 | CO BTN SB BB | CO | 3 | valid |
| A6 | 3 | BTN SB BB | BTN | 4 | valid |
| A7 | 2 | SB/Button BB | SB/Button | 5 | valid; dealerchair=smallblindchair is required |
| A8 | 2 | SB/Button BB | BB | 6 | valid |
| A9 | 1 | unsupported | any | 0 | invalid |
| A10 | 7+ | unsupported | any | 0 | invalid |

### Physical occupancy versus deal mode

| # | Seated at table | D | Expected |
|---:|---:|---:|---|
| A11 | 2 | 2 | `physical_table_hu=1`, `true_hu=1`, `true_hu_full_table=1` |
| A12 | 3 | 2 | `physical_table_hu=0`, `true_hu=1`, `true_hu_with_waiters=1` |
| A13 | 6 | 2 | same as A12; strategy follows HU deal mode, audit retains physical occupancy |
| A14 | 6 | 5 | supported five-handed deal; one seated player was not dealt |
| A15 | 4 | 5 | impossible: seated count < dealt count -> invalid |

## B. HU-origin contract

`f$cc_hu` alone is never a strategy key.

| # | Hand origin | D | F | P now | Origin | Expected strategic provenance |
|---:|---|---:|---:|---:|---:|---|
| B1 | true HU hand | 2 | 2 | 2 | 1 | true-HU tree (`HUSB/HUBB` ancestry) |
| B2 | 6h hand, four fold preflop | 6 | 2 | 2 | 2 | six-max matchup/range tree |
| B3 | 5h hand, three fold preflop | 5 | 2 | 2 | 2 | five-handed/canonical matchup tree |
| B4 | 3h hand, one folds preflop | 3 | 2 | 2 | 2 | 3h survivor tree |
| B5 | 3 players reach flop, one folds flop | 6 | 3 | 2 | 3 | retain multiway-flop provenance on turn/river |
| B6 | 4 players reach flop, two fold before turn | 6 | 4 | 2 | 3 | retain 4-way-flop provenance |
| B7 | current hand is 3-way | 6 | 3 | 3 | 0 | not HU |

Mandatory invariant: an origin-3 later street must **never** enter an ordinary HU turn/river child merely because `nplayersplaying=2`.

## C. True-HU positional semantics

| # | Line | Hero | Matchup | Rel | Expected |
|---:|---|---|---:|---|---|
| C1 | true HU, SB/Button vs BB | SB/Button | 56 | IP/Last | HUSB positional ancestry |
| C2 | true HU, BB vs SB/Button | BB | 65 | OOP/First | HUBB positional ancestry |
| C3 | true HU | SB/Button | — | — | BTN bit is not added to live mask; SB bit is canonical |
| C4 | true HU | BB | villain mask | — | opponent SB/Button = bit 16 only |
| C5 | true HU | SB/Button | villain mask | — | opponent BB = bit 32 only |

This is intentionally different from a 3-6h `SB vs BB` survivor spot: in true HU the SB is also Button and is **IP** postflop; in a normal multi-seat deal SB is **OOP** versus BB.

## D. HU one-raise pots from 3-6h deals

| # | Line reaching flop | D | Hero | PF | Role | HU matchup | Rel | Origin | Expected |
|---:|---|---:|---|---:|---:|---:|---|---:|---|
| D1 | UTG raise, BB call; others fold | 6 | UTG | 2 | 1 | 16 | IP | 2 | valid |
| D2 | HJ raise, CO call; others fold | 6 | HJ | 2 | 1 | 23 | OOP | 2 | valid |
| D3 | HJ raise, BB call; others fold | 6 | HJ | 2 | 1 | 26 | IP | 2 | valid |
| D4 | CO raise, BTN call; others fold | 6 | CO | 2 | 1 | 34 | OOP | 2 | valid |
| D5 | CO raise, SB call; others fold | 6 | CO | 2 | 1 | 35 | IP | 2 | valid |
| D6 | BTN raise, BB call; others fold | 6 | BTN | 2 | 1 | 46 | IP | 2 | `3wBTNvBB` direct ancestry |
| D7 | SB raise, BB call; others fold | 6 | SB | 2 | 1 | 56 | OOP | 2 | `3wSBvBB`, **not HUSB** |
| D8 | BTN raise, BB call | 6 | BB | 2 | 2 | 64 | OOP | 2 | valid |
| D9 | SB raise, BB call | 6 | BB | 2 | 2 | 65 | IP | 2 | valid; **not HUBB true-HU** |
| D10 | HJ raise, BB call | 5 | HJ | 2 | 1 | 26 | IP | 2 | canonical HJ, but deal-size metadata=5 |
| D11 | CO raise, BB call | 4 | CO | 2 | 1 | 36 | IP | 2 | canonical CO, deal-size metadata=4 |
| D12 | BTN raise, BB call; SB folds | 3 | BTN | 2 | 1 | 46 | IP | 2 | same matchup ID as D6, different handedness metadata |

## E. True-HU one-raise subtypes

| # | Line | Hero | PF | Role | Ordinary SRP | ISO | HULR | Expected |
|---:|---|---|---:|---:|---|---|---|---|
| E1 | SB/Button open-raises, BB calls | SB | 2 | 1 | yes | no | no | true-HU SRP PFA IP |
| E2 | SB/Button open-raises, BB calls | BB | 2 | 2 | yes | no | no | true-HU SRP caller OOP |
| E3 | SB limps, BB raises, SB calls | BB | 2 | 1 | no | no | yes | true-HU limp-raised PFA OOP |
| E4 | SB limps, BB raises, SB calls | SB | 2 | 2 | no | no | yes | true-HU limp-raised caller IP |

Mandatory invariant: E3/E4 must **never** set `f$cc_pf_iso_proven`. Isolation requires a third-player context.

## F. ISO and unraised pots on 3-6h deals

| # | Line reaching flop | Hero | PF | Role | Subtype | Expected |
|---:|---|---|---:|---:|---|---|
| F1 | UTG limp, HJ raise, UTG call | HJ | 2 | 1 | ISO proven | valid |
| F2 | CO limp, BTN raise, CO call | CO | 2 | 2 | ISO proven | valid |
| F3 | BTN limp, SB call, BB check | BB | 1 | 9 | unraised | valid |
| F4 | HJ limp, BB check | HJ | 1 | 8 | unraised | valid if other seats folded/checked consistently |

## G. 3-bet pots

| # | Line reaching flop | D | Hero | PF | Role | 3BP subtype | HU origin | Expected |
|---:|---|---:|---|---:|---:|---|---:|---|
| G1 | BTN raise, SB 3bet, BTN call | 6 | SB | 3 | 3 | plain proven | 2 | valid, 6max 3BP family |
| G2 | BTN raise, SB 3bet, BTN call | 6 | BTN | 3 | 4 | plain proven | 2 | valid |
| G3 | UTG raise, HJ call, BTN 3bet, UTG call, HJ fold | 6 | BTN | 3 | 3 | squeeze proven | 2 | valid |
| G4 | UTG raise, HJ call, BTN 3bet, UTG call | 6 | UTG | 3 | 4 | squeeze proven if chronology visible | 2 | valid |
| G5 | HJ raise, CO call, BTN 3bet, HJ folds, CO calls | 6 | CO | 3 | 5 | subtype may remain unknown because Hero not raiser | 2 | preserve cold-call role |
| G6 | UTG limp, BTN raise, UTG 3bet, BTN call | 6 | BTN | 3 | 4 | reversed first-orbit order | 2 | subtype unknown; do not call plain 3BP/squeeze |
| G7 | true HU: SB raises, BB 3bets, SB calls | 2 | BB | 3 | 3 | plain proven | 1 | true-HU 3BP child only |
| G8 | true HU: SB raises, BB 3bets, SB calls | 2 | SB | 3 | 4 | plain proven | 1 | true-HU 3BP caller family |
| G9 | true HU: SB limps, BB raises, SB reraises, BB calls | 2 | SB | 3 | 3 | reversed order | 1 | subtype unknown; fail closed until explicit limp-reraise family exists |

Mandatory invariant: true-HU G7/G8 never enter a 3-6h 3BP child despite identical raise count.

## H. Multiway and provenance

| # | Line reaching flop | D | F | P | Hero | PF | Role | Relative | Expected |
|---:|---|---:|---:|---:|---|---:|---:|---|---|
| H1 | UTG raise, BTN call, BB call | 6 | 3 | 3 | UTG | 2 | 1 | First | exact opponent mask BTN+BB |
| H2 | CO raise, BTN call, BB call | 6 | 3 | 3 | CO | 2 | 1 | First | exact mask BTN+BB |
| H3 | BTN raise, SB call, BB call | 3 | 3 | 3 | BTN | 2 | 1 | Last | legacy `3wBTNv2p` shape only |
| H4 | BTN raise, SB call, BB call | 3 | 3 | 3 | SB | 2 | 2 | First | legacy `3wSBv2p` shape only |
| H5 | BTN raise, SB call, BB call | 3 | 3 | 3 | BB | 2 | 2 | Middle | legacy `3wBBv2p` shape only |
| H6 | UTG raise, HJ call, CO call, BB call | 6 | 4 | 4 | UTG | 2 | 1 | First | new-theory parent required |
| H7 | CO raise, BTN call, SB call, BB call | 6 | 4 | 4 | BTN | 2 | 2 | actual position | no invented 3w mapping |
| H8 | 4 players reach flop, one folds flop | 6 | 4 | 3 | any | any | any | actual position | `mw_requires_new_theory_parent=1`; no 3w ancestor |
| H9 | 3 players reach flop, still 3way turn | 6 | 3 | 3 | any | any | any | actual position | 3w shape may be ancestry only |

The v2 multiway exact ID must differ when any of `D`, `F`, current `P`, pot family, role, Hero position, opponent mask, or relative position differs.

## I. 4-bet and unsupported depth of preflop aggression

| # | Line | D | PF | Role | Expected |
|---:|---|---:|---:|---:|---|
| I1 | BTN raise, SB 3bet, BTN 4bet, SB call; Hero BTN | 6 | 4 | 6 | mechanically valid, 4BP policy uncovered |
| I2 | BTN raise, SB 3bet, BTN 4bet, SB call; Hero SB | 6 | 4 | 7 | mechanically valid, generic 4bet-caller role only |
| I3 | true HU 4BP reaches flop | 2 | 4 | 6/7 | separate true-HU 4BP children |
| I4 | 4+ raises before flop and postflop still exists | any | 5 | 0/currently undefined | mechanically classifiable; policy fail closed |

## J. Mandatory fail-closed states

| # | Fault | Expected |
|---:|---|---|
| J1 | `nplayersdealt = 1` | invalid |
| J2 | `nplayersdealt = 7` | invalid |
| J3 | `BitCount(playersdealtbits) != nplayersdealt` | invalid |
| J4 | physical seated count < dealt count | invalid |
| J5 | missing/negative dealer/SB/BB chair | invalid |
| J6 | missing cutoff in 4h+ | invalid |
| J7 | missing mp3/HJ chair in 5h+ | invalid |
| J8 | missing UTG chair in 6h | invalid |
| J9 | duplicate canonical chairs in 3h+ | invalid |
| J10 | 2h but `dealerchair != smallblindchair` | invalid |
| J11 | 2h but SB chair = BB chair | invalid |
| J12 | Hero does not map to a canonical position | invalid |
| J13 | Hero no longer in `playersplayingbits` | invalid |
| J14 | HU but `Position = Middle` | invalid |
| J15 | one raise reported but `BitCount(raisbits1) != 1` | invalid |
| J16 | no raise reported but historical raiser bit exists | invalid |
| J17 | preflop fold bit points outside `playersdealtbits` | invalid |
| J18 | `F < 2` on a postflop state | invalid |
| J19 | current players > flop-entry count | invalid |
| J20 | `bblind <= 0` | invalid |
| J21 | `potcommon <= 0` postflop | invalid |
| J22 | live opponent-mask bitcount != `nopponentsplaying` | invalid |
| J23 | current HU but HU origin cannot be classified 1/2/3 | invalid |

## K. Flop CBet routing isolation

| # | Context | Expected child family |
|---:|---|---|
| K1 | true HU ordinary SRP, Hero SB/Button PFA IP | `f$cc_flop_cbet_true_hu_srp_sb_pfa_ip` |
| K2 | true HU SB limp -> BB raise -> call, Hero BB PFA OOP | `f$cc_flop_cbet_true_hu_limpraised_bb_pfa_oop` |
| K3 | 6h BTN open -> BB call, flop HU | `f$cc_flop_cbet_hu_srp_pfa_ip` with origin=2 |
| K4 | 6h SB open -> BB call, flop HU | `f$cc_flop_cbet_hu_srp_pfa_oop` with origin=2 |
| K5 | true HU standard 3BP, Hero 3bettor | true-HU 3BP child only |
| K6 | 6h standard 3BP reduced HU | ordinary 3-6h 3BP child only |
| K7 | 6h squeeze reduced HU | squeeze child only |
| K8 | current HU with origin=3 | **no ordinary flop/HU descendant**; later-street trees must preserve multiway origin |
| K9 | one-raise ISO multiway | multiway ISO child only |
| K10 | ordinary SRP multiway | multiway SRP child only |

Until child strategy functions are individually audited and implemented, every K-family child remains an explicit `false` stub.

## L. SPR acceptance checks

The following must hold regardless of action order within the current street:

1. Hero street-start stack = `(balance + currentbet) / bblind`.
2. Villain street-start stack uses the same reconstruction.
3. HU effective stack is the minimum of the two.
4. Current street bet sizes do not inflate the SPR denominator; denominator is `potcommon / bblind`.
5. A short third player may lower coarse multiway SPR, but actor-specific nodes must not use that as effective stack versus a different deep bettor.
6. `f$allin_on_betsize_balance_ratio` remains `0.00` unless a later explicit architecture decision replaces it.
7. HU origin does not change SPR mathematics, but it changes the strategy allowed to consume that SPR.

## Parser/runtime gate

This matrix is a design/static contract. Before a CashCrusher formula is released for table testing, each case needs either:

- a synthetic OpenHoldem replay/log state; or
- a deterministic runtime fixture that prints the context symbols.

No strategic PASS is inferred from static inspection alone.
