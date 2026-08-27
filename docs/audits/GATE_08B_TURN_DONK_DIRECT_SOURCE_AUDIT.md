# Gate 08B — direct native `(BBorSB)v2pp` Turn Donk audit

## Scope

This gate audits only the dedicated `Crusher Starting Strategy` descendant for the native three-handed blind-vs-BTN+other-blind family. It does **not** grant source provenance to every history that the old DeepCrusher router happened to send to `f$move_turn_donkbet`.

Canonical Turn-Donk ownership comes from Gate08A: Hero is on the Turn, has not acted yet, faces no bet, is not LAST, does not own final flop aggression, and one approved CLOSED flop parent is proven.

## Primary source findings

The dedicated `(BBorSB)v2pp` source separates hand families materially.

### TP/OP/2P+

`AFTER FLOP X/C: nothing here.`

Therefore this gate adds no generic TP+/OP Turn Donk from the native source. Mature DeepCrusher contains later C++-style current-strength reclassification inside one high-air history, but that is not a primary-source Turn-Donk instruction and is excluded from Gate08B.

### MP/BP

`AFTER FLOP X/C: nothing here.`

No native-source MP/BP Turn Donk is created by this gate.

### Good / medium draws

The source says Ax, completed and 2+ broadway flops prefer X/C, while 1BW / 9-high / paired structures may Donk75. For the later street it states:

> Turn after flop X/C or B/C ... donkbet ... 75% OTT.

This is a direct source action once the relevant executed history is proven.

For **X/C**, Gate08B can prove both pieces independently:

1. pre-action source draw-check substate was snapshotted on flop;
2. closed `did*round2`, `raisbits2` and `lastraised2` history proves the actual clean X/C against the final live aggressor.

Result: **native draw X/C -> Turn Donk75** is executable source policy.

For **B/C**, action counters are insufficient. The source also says weak naked gutshot folds versus a raise, medium draws call only up to the normal/~3x class, and good draws 3bet. Mature DeepCrusher writes `user_DC8_MW_MediumDraw_BC_Eligible` only inside that defense-owned classification. Therefore Gate08B refuses to infer the source B/C branch merely from `Donk -> raise -> call` counters.

Result: B/C remains fail-closed until the future Flop Donk-vs-Raise defensive owner writes an equivalent eligibility marker.

### A/K-high, backdoors and air

The source allows a very narrow flop call:

- Ace-high only with BDSD, up to 33%;
- lower high-card/backdoor only with BDFD + overcard, up to 33%.

After that X/C, the Turn instruction is:

> If we improve to 2HC OESD or FD - we donk bet 50% ...

and no improvement does not create a Turn lead.

Gate08B now snapshots the pre-action high-air/backdoor candidate, but the exact <=33% call-price proof belongs the future flop defensive node. The pre-action snapshot cannot know the size of a bet that has not happened yet, and the closed Hero counters do not preserve that price.

Result: the high-air descendant is coded but **fail-closed until `user_cc_flop_donk_source_highair_called_le33` is supplied by audited defense**. Once that proof exists:

- no made hand + exact 2HC OESD (`HaveStraightDraw && nstraightfillcommon-nstraightfill=2`) -> Donk50;
- no made hand + exact 2HC FD (`HaveFlushDraw && SuitsInHand=1`) -> Donk50;
- otherwise explicit no-donk.

## Short-stack migration review

No generic short-stack removal was applied.

The native Turn-Donk X/C source uses fixed 75% and 50% sizes and does not itself invoke a stackoff/SPR threshold. The earlier Flop source `SPR <= 1.25 -> POT` rule remains separately retained where source-faithful. Its stated future Turn-jam plan is still **not** imported here because the exact executed flop size/history/effective-stack node has not been certified as an owned strategic jam.

Thus the binding migration rule remains: review exact stack-sensitive nodes; do not automatically zero them and do not automatically transplant them.

## Implemented files

- `src/CashCrusher_Flop_Donk_SourceHistoryHelpers.txt`
- `src/CashCrusher_Flop_Donk_ActionHistory.txt` — extended with direct-source X/C substate snapshots
- `src/CashCrusher_Turn_Donk_Common.txt`
- `src/CashCrusher_Turn_Donk_Source.txt`
- `src/CashCrusher_Turn_Donk.txt`
- `tools/test_flop_donk_history.py` — extended snapshot contract
- `tools/test_turn_donk_source.py`

## T / A / P / X ledger

| Item | Provenance | Result |
|---|---|---|
| native draw X/C -> Turn75 | **T/A** | implemented |
| native draw B/C -> Turn75 | **T**, defense-dependent | coded behind future defense proof; currently fail-closed |
| high-air X/C <=33 + 2HC OESD/FD -> Turn50 | **T/A**, defense-dependent | coded behind future price proof |
| high-air X/C no improvement -> no Turn Donk | **T** | explicit once price-proven context exists |
| high-air current TP+/2P+ reclassification from mature C++ | **X for primary-source Gate08B** | not copied |
| generic TP+/OP native Turn Donk | **X** | not created |
| generic MP/BP native Turn Donk | **X** | not created |
| B/C eligibility inferred only from action counters | **X** | prohibited |
| generic Turn jam / commitment threshold | **X at this gate** | not created |

## Validation

The Gate08A ownership/history suite passed in GitHub Actions run #758.

After adding the source-history snapshots and direct native source policy, the combined static suite passed in GitHub Actions **run #776** on commit `0aff3bcd0385daf5c6711b173d3ce9e9b0217f23`.

This is a static/deterministic policy result. Whole-bot `f$turn`, sizing composition and OpenHoldem parser/replay certification remain separate release gates.

## Next gate

Gate08C should map the remaining direct legacy Turn-Donk source families one at a time before any broad six-max professional fill:

1. HUBB;
2. `3wSBvBTN`;
3. `3wSBvBB`;
4. `3wBBvBTN`.

Each must be mapped to CashCrusher by strategic/range ancestry rather than literal old seat labels. In particular, the `3wSBvBB` 75/100 low-SPR decision requires its own cash-depth review instead of automatic deletion or transplant.
