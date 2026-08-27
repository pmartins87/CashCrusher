# Gate08C.4 — 3wBBvBTN Turn Donk audit

Status: **PASS — static/deterministic source mapping; price/defense-dependent descendants deliberately fail closed until Flop defense records their provenance**.

## Source priority

This audit reconciles three layers instead of silently merging them:

1. **Primary/current:** `12- NOVO CRUSHFEST 3wBBvBTN.docx`.
2. **Corroborating old source:** `7- CRUSHFEST 3wBBvBTN - ok.docx`, only where it does not conflict with the NOVO document.
3. **Mature DeepCrusher implementation:** used only to resolve implementation ambiguities/gaps and explicitly labeled **A** rather than upgraded to direct source **T**.

The NOVO document reorganizes and clarifies the older material. Its exact Turn-Donk Q8/Q9 instructions are consistent with the older file, so the newer text is canonical here.

## Exact range/topology owner

The source family is not a generic OOP HU caller. It is:

`BTN open -> BB call -> SB/earlier seats gone -> BB checks flop -> BTN bets -> BB calls -> BB acts first on Turn`.

CashCrusher preserves:

- literal three-handed ancestry separately from a 4–6 handed structural descendant;
- Hero = BB;
- Villain = BTN;
- ordinary one-raise SRP;
- Hero = preflop caller;
- actual final flop aggressor = BTN/current sole Villain;
- actual clean flop X/C from Gate08 parent 1;
- Gate07 reviewed family 3 rather than any arbitrary parent-3 clean X/C.

This is intentionally stricter than merely asking whether Hero is OOP on Turn.

## Flop class: Q8/Q9 is the TP-flop-X/C family

The NOVO questions sit inside the `TP or better` section, but the mature implementation snapshots **`JustTopPair`** on the flop for this Turn-Donk lineage. CashCrusher retains that narrowing as **A**.

This matters because the source normally check-raises TP versus <=50% CBet; a TP flop X/C is an exception, not the generic line. Therefore:

`top-pair snapshot + actual call != source-valid TP X/C`.

Flop defense must eventually write:

- `user_cc_flop_bbvbtn_source_tp_xc_eligible`;
- `user_cc_flop_bbvbtn_source_tp_xc_called_le50` or
- `user_cc_flop_bbvbtn_source_tp_xc_called_gt50`.

The Turn attack node consumes these facts but does not invent them retrospectively.

## Q9 — paired Turn improving to trips

Primary source:

- completed paired Turn -> **Bet 75%**;
- non-completed paired Turn -> **Bet 50%**.

The mature implementation contains an important correction: Q9 is **actual trips/boat/quads**, not generic `TwoPairPlus` created by a paired public board. CashCrusher therefore requires:

- Turn pairs a flop rank; and
- current `Trips || FullHouse || Quads`.

Generic two pair is excluded from Q9.

Provenance: source action/size = **T**; exact contribution-aware correction = **A**.

## Q8 — completed draw after flop TP X/C

### Four-card straight

Source: **Donk 50% Turn**, then River 50%.

CashCrusher implements only the Turn **50%**. The River barrel belongs its own later-street owner and is not scheduled from this node.

### Four-card flush

Source:

- K/A-high flush -> **Donk 50%**;
- Q-high or worse -> **check**, potentially X/C <=50% in defense.

CashCrusher identifies the 4-card flush state with `nsuitedcommon >= 4 && HaveFlush`. The K/A contribution split uses the audited mature/OpenPPL meaning of `NumberOfUnknownSuitedOvercards <= 1`.

The mature ordering puts 4CS before 4CF. That ordering is retained as **A**, which matters only on overlapping four-card straight/flush structures.

### Other made straight/flush

Source:

- Turn overcard -> **check**;
- Turn undercard -> **bet**;
- Turn undercard after flop sizing 51%+ -> **check**.

The source does **not** supply a size for the positive ordinary-UC bet. Mature DeepCrusher uses 50%; CashCrusher therefore uses **50% as A**, not as T.

The 51% split is fail-closed. Missing `>50` cannot be treated as `<=50`; exactly one price marker is required for the UC decision.

Turn ranks that are neither strict overcards nor strict undercards remain a source gap.

## Mature-only residual 2P+ fallback rejected as direct source

Mature DeepCrusher contains a residual `current TwoPairPlus -> Turn50` after the source-exact Q8/Q9 branches.

Neither the NOVO nor old source gives that generic fallback in this flop-TP-X/C Turn-Donk section. CashCrusher keeps it visible as:

`f$cc_turn_donk_bbvbtn_residual_2pplus_mature_only_gap`

and **does not execute it** at Gate08C.4.

Provenance: **X as direct-source policy**. A later professional/source-supported review may decide whether some exact subcase deserves an A/P action.

## Separate Draw section: missed draw is explicit CHECK

The NOVO Draw section says directly that after a flop draw X/C, when the draw **misses Turn**, Hero should not Donk: check and consider X/C, or probe River after BTN checks.

CashCrusher reserves a future defense marker for a source-valid non-best draw X/C. When that marker exists and the Turn remains no-made, the Turn Donk decision is an explicit **check**.

A no-made flop draw that actually becomes a made hand is **not** silently imported into Q8, because Q8 is inside the TP-or-better section. That completion remains a source gap until separately justified.

## Short-stack ownership discipline

No inherited jam/stackoff threshold was needed for the mapped Q8/Q9 first-action Turn decisions. River50 continuation text is preserved in the audit but not executed here.

This follows the project rule: later-street implications and short-stack continuation plans are reviewed in their actual node instead of being erased or smuggled through an earlier action.

## Code

- `src/CashCrusher_Turn_Donk_BBVBTN.txt`
- `src/CashCrusher_Turn_Donk.txt` — family ID 5 routing
- `tools/test_turn_donk_bbvbtn.py`
- `.github/workflows/static-lint.yml`

## Validation

GitHub Actions **run #826** passed on commit:

`840d5b36050e30bc270a687cf74d00652140df4a`

The job passed **55 strategy/static contract steps**, including the new `BBvBTN Turn Donk source/provenance contract`.

This is static/deterministic validation. OpenHoldem parser/runtime and whole-bot callback composition are still separate gates.

## Gate08 source-map state after C4

Source/high-ancestry Turn-Donk families now mapped separately:

1. native `(BBorSB)v2pp`;
2. HUBB / BB-v-SB;
3. SB-v-BTN;
4. SB-v-BB;
5. BB-v-BTN.

The next phase should not invent another legacy seat label. It should audit the **remaining six-max chronology gaps** (ISO/plain3BP/squeeze/4BP and residual multiway/HU states), decide which are deliberate range-check baselines versus P-positive leads, and then close Turn-Donk runtime sizing/history.
