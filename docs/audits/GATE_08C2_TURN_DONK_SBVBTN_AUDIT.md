# Gate08C.2 — `3wSBvBTN` Turn Donk source audit

Status: **PASS at static/deterministic strategy-contract level**.

Primary source: `Crusher Strategy/5- CRUSHFEST - SBvBTN.docx`.
Secondary audit source: mature `DeepCrusher(1).txt`, used only to resolve explicit source gaps/ambiguities and cross-check implementation.

## 1. Strategic ancestry, not literal label copying

The historical `3wSBvBTN` scenario is Hero in SB versus BTN after BB has folded. CashCrusher maps the Turn-Donk descendant only when the closed history proves:

- Hero SB;
- Villain BTN;
- ordinary one-raise SRP;
- BTN was the single preflop raiser;
- Hero was the SRP caller;
- exactly BTN+SB reached flop;
- Hero was OOP;
- Gate07 family 3 recorded the reviewed flop-check baseline;
- Hero actually **checked and called** one flop bet;
- BTN owns final flop aggression and is still the current live Villain;
- Turn is a valid first-action Donk opportunity.

Origin ID 1 is the literal three-handed ancestry. Origin ID 2 is the same BTN-open/SB-call/BB-gone topology from a 4-6 handed deal and is explicitly **A/P**, not relabelled as direct T.

ISO, plain 3BP, squeeze, 4BP and arbitrary OOP HU callers do not enter this module.

## 2. TP+ — Axx is the direct positive exception

The dedicated source says population CBets frequently and Hero should generally X/R top pair. It then gives one explicit exception:

- on **Axx** boards, prefer **calling flop and Donk Betting Turn** so BTN cannot check and realize equity cheaply.

Later the TP+ section says `AFTER FLOP X/C: nothing here`; this is read together with the earlier explicit Axx exception rather than used to erase it.

Mature DeepCrusher confirms the exception by recording `user_DC8R_3wSBvBTN_AxxTP_FlopCalled` and, after the actual flop call, Donking Turn.

### Size provenance

The Starting Strategy does **not** state the Turn size for this Axx TP+ exception. Mature DeepCrusher uses `Turn100`.

CashCrusher therefore implements:

- Axx TP+ X/C -> Turn Donk: **T**;
- Turn size 100% pot: **A** from mature detailed implementation;
- non-Axx TP+ that nevertheless arrives through actual X/C: reviewed **no Turn Donk**, because the primary source supplies no positive descendant there.

The Flop TP+ state is consumed from Gate07's persisted contribution-aware primary-class snapshot, not reconstructed from current Turn strength.

## 3. MP/BP — no Turn Donk is created

The source says:

- vs flop sizing 51%+, fold MP/BP unless combo backdoor/draw;
- vs 50% or less, call;
- after the flop X/C, unless improving to straight/flush draw, Hero should generally fold versus a 33%+ second barrel.

That section is **defensive Turn ownership**, not a first-action Turn Donk instruction.

CashCrusher therefore marks the lower-pair flop snapshot as a reviewed first-action **check/no-Donk** state. The later response if BTN actually bets Turn belongs the defense gates.

## 4. Draw X/C -> improved undercard Donk75

The source classifies good draws for flop X/R and weaker draws for flop calls. After an actual flop X/C it says:

> If we improve on undercard - we donk bet ... Usually the sizing of 75% would be enough.

The mature audited implementation/CrusherTBP interpretation resolves `improve` as **making PairOrBetter on an undercard**, not merely retaining/upgrading a live draw. CashCrusher keeps that distinction visible:

- `undercard`: **T**;
- an improvement is required: **T**;
- `PairOrBetter` as the deterministic meaning of that improvement: **A**;
- Turn Donk ~75%: **T**.

The source mentions using that bet to create roughly 1:1 River SPR in the original short-stack environment. CashCrusher retains the authored **Turn75** decision but does **not** automatically create a River jam or other commitment rule. The future-street SPR implication is outside this Turn owner and must be reviewed at cash depth separately.

This follows the binding migration rule: short-stack ancestry triggers review, neither automatic deletion nor blind transplant.

## 5. High-card/backdoor X/C -> exact 2HC pickup Donk50

The source permits only narrow flop calls:

- Ace-high + backdoor straight draw up to 33%;
- lower high-card/backdoor hands only with BDFD + overcard, also up to 33%.

After X/C:

- exact improvement to **2-hole-card OESD or FD -> Turn Donk50**;
- otherwise no Turn Donk;
- the stated River behavior after a called Turn Donk belongs River ownership and is not scheduled here.

CashCrusher uses the same exact mechanical interpretation already audited elsewhere:

- OESD: `HaveStraightDraw && (nstraightfillcommon - nstraightfill = 2)`;
- FD: `HaveFlushDraw && SuitsInHand = 1`;
- Hero must still have no made hand for this exact primary-source branch.

### Rejected mature fill

Mature DeepCrusher additionally reclassifies a high-air flop call that improves to TP+/2P+ on Turn and Donks it before the source 2HC-draw branch.

The primary Starting Strategy does not supply that rule. Gate08C.2 therefore records it as a **source gap / X as direct-source policy** and fails closed instead of silently promoting that secondary behavior to T. It may be reconsidered later as an explicit A/P node.

## 6. Why Flop-defense markers are required

Closed `did*round2` history proves Hero really X/C'd. It does **not** preserve the exact CBet amount Hero faced.

That matters because the dedicated source has different flop-call ceilings:

- weak GS without overcard: <=50%;
- other non-best draws: <=75%;
- high-card/backdoor: <=33%.

Therefore Gate08C.2 reserves two future **Flop-defense-owned** provenance markers:

- `user_cc_flop_donk_sbvbtn_source_draw_xc_eligible`
- `user_cc_flop_donk_sbvbtn_source_highair_called_le33`

Turn attack never sets them.

If the flop snapshot says `no made hand` but neither or both markers are present, the source subrange cannot be proved and the SBvBTN Turn node **fails closed**. Absence of evidence is never interpreted as proof that the flop price was small enough.

Axx TP+ does not need such a price marker because the source explicitly gives the call->Donk exception without a CBet-size ceiling.

## 7. Files and validation

Implemented:

- `src/CashCrusher_Turn_Donk_SBVBTN.txt`
- `src/CashCrusher_Turn_Donk.txt` family 3 routing
- `tools/test_turn_donk_sbvbtn.py`
- `.github/workflows/static-lint.yml`

GitHub Actions **run #801** passed on commit `f68fc0577303b8c55b6f9bd479af248f5dd47ec3`.

The suite now includes **53** static strategy/history/runtime contract tests; the new SBvBTN contract passed alongside all earlier gates.

## 8. Next gate

Gate08C.3 is `3wSBvBB` Turn Donk. Its inherited 75/100 low-SPR behavior must be audited node-by-node against the actual source, detailed implementation and 100bb cash geometry. It is explicitly neither an automatic transplant nor an automatic deletion.
