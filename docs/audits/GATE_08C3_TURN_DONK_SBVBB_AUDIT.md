# Gate08C.3 — 3wSBvBB Turn Donk audit

Status: **PASS — static/deterministic source mapping, with defensive provenance intentionally fail-closed**.

## Primary source

`Crusher Strategy/6- CRUSHFEST 3wSBvBB.docx`.

The source describes Hero **SB OOP versus BB** after the BTN is gone, and it explicitly has two different preflop/range origins:

1. **Limped pot:** SB limp, BB check. The source says medium/weak draws may X/C up to 50%.
2. **MNR/SRP pot:** SB raise, BB call. The source says medium draws may X/C up to 100%, weak draws up to 33%.

CashCrusher therefore does not collapse the two into one generic `3wSBvBB` label. The exact preflop origin remains part of the Turn decision.

## Important ownership repair discovered by this audit

Gate08A previously admitted Turn Donk only after a reviewed Gate07 Flop-Donk opportunity X/C or after Donk-B/C. That was too narrow.

The MNR branch here can be:

`SB PFA -> flop CHECK -> BB BET -> SB CALL`.

Hero entered the flop with preflop initiative, but **lost final flop initiative by actually checking and calling**. On the Turn, first to act with no bet faced, this is a genuine Turn-Donk/lead decision even though it did not originate in the Flop-Donk router.

Gate08A now has a third parent:

`parent 3 = other clean flop X/C`.

It is proved only from closed `did*round2`, `raisbits2`, `lastraised2` and live-aggressor history. Parent 3 grants **opportunity only**; no strategy fires unless an exact child proves its own range/history provenance. This also makes the architecture more faithful to actual initiative instead of module ancestry.

## Direct source Turn branch

For the reviewed medium/weak-draw X/C lineage, the source says:

- if the draw improves and the Turn is an **overcard**: **Donk 75–100%**;
- if the draw improves and the Turn is an **undercard**: **check with X/R intention**;
- source purpose of the large lead is to create roughly **1:1 River SPR** and then move all-in.

The mature DeepCrusher resolves `improve` with `PairOrBetter`, which CashCrusher keeps as an **A** ambiguity resolution.

The source only gives explicit OC/UC branches. Turn ranks that are neither strict overcards nor strict undercards remain **uncovered**, rather than being guessed.

## Flop-defense provenance firewall

The exact source X/C eligibility is price-sensitive and cannot be reconstructed safely on the Turn. Three defense-owned markers are therefore reserved:

- limped medium/weak draw called <=50%;
- MNR medium draw called <=100%;
- MNR weak draw called <=33%.

Until the audited Flop Call-vs-Bet owner writes exactly one marker matching the exact preflop origin, this source branch remains fail-closed.

This is intentional. A Turn module may consume a defensive execution fact; it must not invent one retrospectively.

## 75–100% / short-stack review

This node is an explicit example of the project rule:

> short-stack ancestry requires review; it is neither automatically deleted nor blindly transplanted.

The Starting Strategy directly gives **75–100%**. The mature implementation adds a secondary rule:

- local effective SPR <=1.80 -> pot;
- otherwise -> 75%;
- also persist a River-shove plan.

The `<=1.80` threshold and forced River continuation are not direct source facts and are strongly entangled with Spin stack geometry. They were **not** transplanted as generic cash rules.

At Gate08C.3 CashCrusher chooses the directly authored lower size, **75%**, for the positive Turn lead and records that the 100% upper bound has been reviewed rather than forgotten. Pot sizing remains eligible for a later exact node-owned cash-SPR/runtime review; it is not globally banned. No River shove is scheduled from the Turn node.

## Implemented code

- `src/CashCrusher_Turn_Donk_History.txt`
  - adds canonical clean-X/C primitive;
  - adds parent 3 for X/C outside reviewed Gate07 family ancestry.
- `src/CashCrusher_Turn_Donk_SBVBB.txt`
  - direct 3h versus 4–6h ancestry;
  - limped versus MNR origin split;
  - defense provenance firewall;
  - improved OC -> Donk75;
  - improved UC -> check / Turn-defense X/R ownership;
  - neutral runout source gap remains uncovered.
- `src/CashCrusher_Turn_Donk.txt`
  - family 4 routing.
- `tools/test_turn_donk_history.py`
  - parent-3 ownership regression.
- `tools/test_turn_donk_sbvbb.py`
  - topology, source provenance, sizing and safety contracts.

## Validation

GitHub Actions **run #816** passed on commit `07696a10891242503275016cd0b1f1a0bf2800e8`.

The job passed all **54 strategy/static contract steps**, including:

- Turn Donk ownership/history;
- native Turn Donk;
- HUBB Turn Donk;
- SBvBTN Turn Donk;
- new SBvBB Turn Donk.

This remains static/deterministic validation, not OpenHoldem parser/runtime certification.

## Next exact source family

Gate08C.4: **3wBBvBTN**.

Both the old and `NOVO CRUSHFEST 3wBBvBTN` sources must be reconciled before coding because the newer document contains explicit Turn-Donk guidance and should not be silently mixed with superseded older branches.
