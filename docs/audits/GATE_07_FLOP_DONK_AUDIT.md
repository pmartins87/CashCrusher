# Gate 07 — Flop Donk canonical audit

Date: 2026-08-24  
Branch: `gate-00-context-engine`

## Result

Gate07 is **PASS at the static/deterministic level for the currently supported chronology domain**.

The canonical router now distinguishes eight reviewed Flop-Donk families, translates the reviewed 50/75/100% strategic palette to OpenPPL runtime actions, applies only natural/mechanical all-in equivalence, and records CLOSED round-2 execution history for future Turn Donk ownership.

Unsupported multiway/unresolved 4BP, 5bet+ and reversed/backraise/limp-reraise histories remain fail-closed. Gate07 does not claim whole-bot/OpenHoldem runtime certification.

## 1. Source boundary

The dedicated Starting Strategy gives a positive Flop Donk tree only for `(BBorSB)v2pp`, with the two explicitly described preflop shapes:

1. `BTN limp -> SB call -> BB check`;
2. `BTN raise -> SB call -> BB call`.

DeepCrusher's broad no-initiative OOP router can reach `f$move_flop_donkbet` from more situations, but router membership is not strategy provenance. The positive source tree therefore belongs only to the exact source-shaped family; other pot/range families require an explicit A/P review or remain unsupported.

### Direct source policy retained

For contribution-aware TP/OP/2P+:

- A-high: check;
- draw-heavy/completed with deepest/all-live effective SPR <= 1.25: POT;
- draw-heavy/completed otherwise: 75%;
- 2+ broadways: 75%;
- 1 broadway: 50%;
- 9-high or lower: 75%.

The `<=1.25` condition was **not deleted merely because it came from short-stack Spin**. DeepCrusher's original effective-stack helper uses the biggest active opponent, so CashCrusher migrates this exact source relationship to corrected **deepest-effective multiway SPR**. The future source Turn-jam plan is not a Flop action and was not smuggled into this gate.

For lower pairs, the dedicated source rule is preserved as `pair rank <=7` on a **non-completed** flop -> Donk50. The older CrusherTBP completed-board inversion is X because it conflicts with the dedicated Starting Strategy.

For no-made good/medium draws:

- A-high / completed / 2+BW: check;
- otherwise 1BW / 9-high-or-lower / paired: Donk75;
- weak naked gutshot without overcard is not promoted;
- generic air/backdoor lead is absent.

## 2. Reviewed families

### Family 1 — native `(BBorSB)v2pp`

T/A direct/high-ancestry implementation of the dedicated Starting Strategy.

### Family 2 — 4–6 handed BTN + both blinds

A/P adaptation of the same structural shell. Limped and BTN-open SRP origins remain distinct, and Hero SB versus Hero BB ownership remains visible. The native 3-handed ranges are not silently reused as if the deal had started three-handed.

### Family 3 — HU ordinary SRP caller

P reviewed CHECK baseline for true-HU / preflop-reduced-HU ordinary-SRP OOP non-initiator states. No source-backed positive Donk range was found.

### Family 4 — residual current-multiway ordinary SRP caller

P reviewed CHECK baseline outside the exact BTN+both-blinds family. This protects the checking range instead of manufacturing generic multiway leads from router ancestry.

### Family 5 — proven ISO OOP caller

P reviewed CHECK baseline. Original-limper versus post-raise-coldcaller provenance is retained rather than merged.

### Family 6 — supported plain 3BP / squeeze OOP caller

P reviewed CHECK baseline with opener/pre-3bet/post-3bet caller origin retained. Plain 3BP and squeeze chronology remain explicit.

### Family 7 — residual unraised current-multiway

P/A positive no-PFA fill:

- three-way: robust 2P+, selected OP/strong TP on favorable low/mid structures, and selected premium draws;
- four-plus: materially tighter, with robust 2P+ and only strongest reviewed no-made nut/combo-draw pressure;
- no pure-air lead;
- deepest-effective SPR controls the source-descended low-SPR POT exception.

### Family 8 — clean caller-side HU 4BP

A/P chronology:

`opener -> Hero 3bet -> opener 4bet -> Hero call`.

When Hero is OOP and receives the canonical first-action Donk opportunity, the reviewed strategy is CHECK. DeepCrusher has no dedicated deep-stack 4BP Donk tree, and naturally low 4BP SPR is not evidence for inventing a lead or converting TP/OP into generic stackoff.

A generic caller-side 4BP chronology module was added so later streets can reuse this proof without treating aggregate call/raise bits as a complete action log.

## 3. Runtime sizing

Strategic size IDs are:

- 1 = 50% -> `BetHalfPot`;
- 2 = 75% -> `BetThreeFourthPot`;
- 3 = 100% -> `BetPot`.

A POT request remains a POT request. It is not synonymous with all-in.

### Natural all-in equivalence

Local `BetMax` is allowed only when the already-reviewed requested size reaches:

1. Hero's available stack; or
2. exact HU effective stack; or
3. deepest/all-live multiway effective relationship.

Reaching only the shallowest multiway opponent is a sidepot event and cannot promote the entire action to `BetMax`.

Historical ~50/55/60% near-all-in rules remain visible as diagnostics/review evidence. They are not erased, and they are not activated as generic Flop Donk commitment.

## 4. Closed action history

`CashCrusher_Flop_Donk_ActionHistory.txt` separates pre-action provenance from actual execution.

Pre-action snapshots retain:

- reviewed Gate07 family;
- primary current hand class;
- exact direct-source positive subtype: value / low-pair / draw;
- player count and live-opponent mask;
- planned size and expected natural-all-in state.

Closed round-2 history then proves separately:

- actual initial Donk bet;
- actual initial check;
- sized bet versus direct all-in;
- Donk -> raise -> Hero call;
- Donk -> Hero re-aggression;
- standard one-bet Donk surviving to Turn with Hero still final aggressor;
- plan/runtime drift.

Future Turn Donk must consume these CLOSED predicates. `user_*` plan markers alone never prove that the flop bet occurred.

## 5. Explicit exclusions

Gate07 does not grant strategy to:

- multiway 4BP;
- unresolved/reversed/backraise/limp-reraise 4BP;
- 5bet+;
- an unreviewed neighboring pot family merely because DeepCrusher's old router would have called `f$move_flop_donkbet`;
- response to a raise over the Donk;
- future Turn/River barrel or stackoff plans.

Those remain separate owners/gates.

## 6. Validation

Combined GitHub Actions run **#748** completed **SUCCESS** on commit `9f77647687af6d45165ebe137c064c3e00c40c56`.

The single combined job passed 49 numbered strategy/lint steps, including:

- global dependency / flat-WHEN / provenance / safety lint;
- direct-source Flop Donk contract;
- 4–6h BTN+blinds adaptation;
- HU reviewed-check baseline;
- residual multiway SRP baseline;
- ISO baseline;
- plain3BP/squeeze baseline;
- residual unraised multiway policy;
- clean HU caller-side 4BP baseline;
- Flop Donk runtime sizing/all-in-equivalence contract;
- closed Flop Donk action-history contract.

## 7. Release boundary / next gate

This PASS is static/deterministic. Table-ready certification still requires whole-bot `f$flop` / `f$BestBetsize` composition, OpenHoldem parser/runtime fixtures and deterministic replays.

The next source-first attack gate is **Turn Donk**. Its first task is ownership/history mapping from the newly trustworthy closed Flop Donk parents, especially the direct `(BBorSB)v2pp` source subtypes. No Turn action should be inferred merely from a Flop Donk strategy intention.
