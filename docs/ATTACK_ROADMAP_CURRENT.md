# CashCrusher — Current Postflop ATTACK Roadmap

This document is the compact live roadmap for the **ATTACK** half of Crusher Framework 5. It exists because the historical root `ROADMAP.md` currently contains much deeper Gate00–05 detail and its old “Gate06+” tail no longer reflects actual branch progress.

## How many attack gates exist?

Crusher Framework 5 defines exactly **13 numbered postflop ATTACK nodes**:

| Gate | Node | Current status |
|---:|---|---|
| 01 | Flop CBet | ✅ static/deterministic layer complete; global replay/composition pending |
| 02 | Turn CBet | ✅ static/deterministic layer complete; global replay/composition pending |
| 03 | River CBet | ✅ static/deterministic layer complete; global replay/composition pending |
| 04 | Flop Float Bet | ✅ static/deterministic layer complete; global replay/composition pending |
| 05 | Turn Float Bet | ✅ static/deterministic layer complete; global replay/composition pending |
| 06 | River Float Bet | ✅ implemented/audited/runtime-covered |
| 07 | Flop Donk Bet | ✅ implemented/audited/runtime-covered |
| 08 | Turn Donk Bet | ✅ implemented/audited/runtime/history-covered |
| 09 | River Donk Bet | ✅ implemented/audited/runtime-covered |
| 10 | Turn Probe Bet | ✅ implemented/audited/runtime-covered |
| 11 | River Probe Bet | ✅ implemented/audited/runtime-covered |
| 12 | Turn Delayed Bets | 🟡 12A Delayed CBet closed; **12B Delayed Float active next** |
| 13 | River Delayed Bet | ⏳ pending Gate12B/history closure |

## Gate12 subdivision

Framework 5 places two distinct functions inside node 12:

- **12A — Turn Delayed CBet:** Hero owns initiative, skips the flop CBet, whole flop checks through, Hero gets first Turn action.
- **12B — Turn Delayed Float / no-initiative delayed bet:** Hero does not own flop initiative, gets a checked-to flop float opportunity, deliberately checks back, and reaches another checked-to Turn state.

They are separate histories and must never share a generic fallback.

### Gate12A checkpoint

Gate12A is **closed at the static/deterministic strategy + runtime layer**.

Validated checkpoint:

- commit `53f23cc99bf39874a8c3014bdaae1fc720f31bc2`
- GitHub Actions push run **#1259**
- run id `32926478303`
- result **SUCCESS**

Canonical audit: `docs/audits/GATE_12A_TURN_DELAYED_CBET_AUDIT.md`.

## Immediate execution order

1. Gate12B source-boundary / ownership reconstruction.
2. Gate12B exact native source descendants and snapshot/history proof.
3. Gate12B six-max SRP / ISO / 3BP / squeeze / clean4BP adaptations only where source is silent.
4. Gate12B coverage, sizing, runtime and closed Turn execution history.
5. Gate13 River Delayed Bet, consuming only valid closed Gate12A/12B histories.
6. Cross-attack global ownership/sizing composition and OpenHoldem deterministic replay certification.
7. Then the **32 defensive nodes** are audited individually.

## Important total-count distinction

“13 gates” is the exact count for the numbered **postflop ATTACK nodes** in Crusher Framework 5. It is **not** the total number of project phases until a table-ready CashCrusher exists. Gate00 infrastructure, ATTACK subgates, 32 defensive nodes, global sizing/ownership composition, parser/runtime fixtures, replay/regression and final integration remain separate project work.

## Policy discipline

Every new child follows the same order: direct source (**T**) → high-ancestry translation (**A**) → deterministic professional fill (**P**) only for genuine source silence → fail closed (**X**) when ownership or range provenance cannot be proven. No ordinary-SRP child may become a generic fallback for another pot family.
