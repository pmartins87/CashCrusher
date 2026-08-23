# Gate 00D — SPR and commitment reconstruction

Status: **IMPLEMENTED AS GEOMETRY/SAFETY FOUNDATION; strategic jam nodes still pending**.

## Why the Spin rule cannot survive unchanged

DeepCrusher inherited a global OpenHoldem helper that can convert an intended bet/raise into all-in when the planned sizing becomes a large fraction of effective stack. In the Spin environment this often matched shallow-stack geometry.

In deeper six-max cash, the same rule would create serious errors:

- ordinary turn/river bets could become unintended jams;
- a call-worthy hand could be promoted into a raise merely because stacks are short relative to the call;
- a strategy originally designed around ~8–25 BB could contaminate 100 BB+ pots;
- river bluffcatching and river value raising would lose their separate EV logic.

Therefore the inherited global commitment rule is classified **X** for CashCrusher.

## Global safety change

CashCrusher defines:

`f$allin_on_betsize_balance_ratio = 0.00`

This disables OpenHoldem's global betsize-to-all-in adjustment.

No generic CashCrusher helper is allowed to say “we are committed, therefore jam.” An all-in must be explicitly owned by the attack/defense node that has considered:

- hand class;
- range interaction;
- board/runout;
- pot family;
- position;
- effective stack;
- current and future street geometry.

## Why `potcommon` is used for street-start pot

OpenHoldem internally separates:

- `potcommon`: money already in the common pot;
- `potplayer`: current-street player bets.

The current `pot` is their sum. While a flop/turn/river bet is sitting in front of Hero, that bet belongs to current-street player contribution, so `potcommon` remains the appropriate denominator for **pot at the beginning of the current betting street**.

This lets CashCrusher reconstruct initial street SPR even when Hero is facing a bet.

## Street-start effective stack

For each player:

`street_start_stack = balance + currentbet`

Adding the current-street contribution back to balance makes the quantity stable as the current round progresses.

In HU:

`effective_stack = min(Hero street-start stack, Villain street-start stack)`

Then:

`initial_SPR = effective_stack / street_start_pot`

All quantities are normalized to BB.

## Multiway SPR

Multiway pots need more care. A single “SPR” is not sufficient for every decision because Hero can be deep against one opponent and shallow against another.

Gate 00D therefore exposes two concepts:

1. **shallowest-live effective SPR** — coarse descriptor for overall pot geometry;
2. **effective SPR versus current raiser (`raischair`)** — actor-specific descriptor for a defense/raise node.

The coarse multiway number must not later be used as a universal excuse to stack off against every player.

## Engineering SPR buckets

Raw SPR remains available. Buckets are provided only to simplify routing and audits:

| Bucket | Initial SPR |
|---:|---|
| 1 | < 1 |
| 2 | 1–<2 |
| 3 | 2–<4 |
| 4 | 4–<6 |
| 5 | 6–<10 |
| 6 | 10–<15 |
| 7 | 15+ |

These boundaries are **P — CashCrusher engineering choices**, not universal GTO laws. A later node may use the raw SPR instead of a bucket whenever precision matters.

## Strategic consequence

A source rule such as “shove turn after pot-sized flop bet at very low SPR” is no longer accepted merely because the old source said shove. During each node audit we ask:

1. Is the underlying line still strategically valid at the actual CashCrusher SPR?
2. Is the hand/range class still stack-off quality in this 6-max matchup?
3. Is a jam the best sizing, or did the Spin source choose jam only because almost no stack remained?

Only then can the line be classified T/A/P or rejected X.

## File

`src/CashCrusher_SPR_Commitment.txt`
