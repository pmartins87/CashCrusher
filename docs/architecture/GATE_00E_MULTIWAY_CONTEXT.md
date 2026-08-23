# Gate 00E — True multiway six-max context

Status: **MECHANICAL CONTEXT COMPLETE; strategy migration not started**.

## Core decision

A three-way Spin node is not automatically a six-max multiway strategy. It is a source of strategic knowledge whose applicability depends on the properties of the six-max state.

Gate 00E therefore preserves:

- exact number of players still holding cards;
- Hero absolute position;
- exact set of live opponent positions;
- Hero relative post-flop position (`First`, `Middle`, `Last`);
- preflop pot family;
- Hero preflop role;
- SPR geometry.

## Exact live-opponent mask

The six canonical positions are encoded as a bitmask:

`UTG=1, HJ=2, CO=4, BTN=8, SB=16, BB=32`

Example:

- Hero CO;
- BTN and BB remain;
- opponent mask = `8 + 32 = 40`.

This avoids defining a different Boolean function for every possible six-max trio/quartet while preserving exact matchup identity for later range-aware policy.

## Relative-position ancestors from Crusher

The old three-player post-flop shapes remain useful as **structural ancestors**:

- `3wBTNv2p` → Hero is last against two opponents;
- `3wSBv2p` → Hero is first against two opponents;
- `3wBBv2p` → Hero is middle against two opponents.

These mappings are only geometry/ordering ancestry. They do not authorize copying Spin ranges, frequencies or stack-off thresholds.

## Four-way and larger pots

Four-, five- and six-way post-flop states have no literal Crusher ancestor. They are explicitly tagged as requiring a new theory parent.

Professional-theory defaults that will guide later node construction, without yet hardcoding frequencies:

- bluff density generally falls as more ranges remain in the pot;
- thin value thresholds become stronger;
- defending versus bets can be tighter than HU because bets into several ranges are stronger on average;
- nut advantage and absolute hand strength gain importance;
- OOP donks/probes require more selectivity;
- high-equity/nutted draws and blockers can remain candidates for aggression, but not through a universal percentage rule.

These are **P** principles. Every concrete threshold still needs node-level treatment.

## Coarse versus actor-specific SPR

Gate 00E may use the shallowest live effective stack as a broad description of the pot, but later decisions facing a specific bettor/raiser must use actor-specific effective stack whenever possible.

This prevents a short third player from making Hero incorrectly treat a deep heads-up side interaction as a low-SPR stack-off.

## Stable multiway context ID

`f$cc_multiway_exact_context_id` encodes:

`player count + pot family + Hero role + Hero position + live-opponent mask + relative position`

It is a mechanical identity key, **not a strategy ID**. Multiple exact IDs may eventually share one professional strategy family, but that sharing must be decided after range/board analysis rather than assumed in advance.

## Files

- `src/CashCrusher_Multiway_Context.txt`
- `src/CashCrusher_Context.txt`
- `src/CashCrusher_SPR_Commitment.txt`
