# Gate 01I — Flop CBet in 4-bet pots

Status: **source audit complete for clean HU 4BP families; ambiguous chronology and multiway strategy remain separate**.

## 1. Source boundary

DeepCrusher does not contain a dedicated deep-stack 4-bet-pot flop CBet tree. Its generic initiative routing can reach `f$move_flop_cbet` after reraised preflop histories, but the CBet policy itself is organized mainly by HUSB/HUBB/3w game shells rather than by 4BP range topology.

Therefore:

- initiative, IP/OOP, hand-class, draw-quality and texture concepts are **A-level** donors;
- exact 4BP cash frequencies are **P**;
- no generic DeepCrusher TP+/draw stack-off line is promoted to a 100bb cash 4BP merely because the pot is reraised;
- equally, no commitment mechanism is globally rejected merely because it came from short-stack Spin. A 4BP often reaches naturally low SPR even from a 100bb start, so later stack-sensitive decisions must be re-audited in the exact node.

## 2. What can be reconstructed safely from current OpenPPL history

CashCrusher currently has persisted aggregate preflop information such as total raise count, `raisbits1`, `callbits1`, Hero's last preflop action and canonical positions. These are useful but are **not a full chronological action log**.

For a three-raise pot where Hero is the final 4bettor, two clean first-orbit candidates can nevertheless be isolated conservatively.

### 2.1 Standard opener 4bet

Pattern:

`Hero open -> later seat 3bet -> Hero 4bet`.

Proof requirements used by CashCrusher:

- exactly 3 preflop raises;
- Hero is final 4bettor;
- exactly 2 unique raisers;
- Hero never recorded a preflop call;
- Hero's canonical position is earlier than the other raiser.

The positional ordering rejects a common reversed/limp-reraise shape instead of silently calling it an ordinary open/3bet/4bet pot.

### 2.2 Standard cold 4bet

Pattern:

`opener -> later 3bettor -> still-later Hero cold 4bet`.

Proof requirements:

- exactly 3 raises;
- Hero final 4bettor;
- exactly 3 unique raisers;
- Hero has no preflop call bit;
- the two other raisers can be ordered strictly before Hero as opener < 3bettor < cold4bettor.

This deliberately excludes backraises and other reopened-action histories where aggregate bitmasks do not prove a clean cold-4bet range.

## 3. Histories deliberately kept unknown

The following are not forced into either clean family:

- limp -> raise -> limp-reraise -> 4bet;
- cold-call -> 3bet behind -> backraise 4bet;
- three-raise histories where the final 4bettor's positional order contradicts a clean first-orbit sequence;
- any history where aggregate masks cannot distinguish when a call occurred.

Failing closed here is not a strategy opinion. It is a chronology-evidence limitation.

## 4. HU survivor provenance

For clean standard families, a HU flop can identify whether the sole Villain is:

1. the original opener;
2. the 3bettor;
3. some non-raiser caller.

Only types 1 and 2 are strategically implemented in Gate 01I. A non-raiser surviving a 4BP can have several materially different histories (cold-call open, cold-call 3bet, call after 4bet, multi-action continuation). Current aggregate call bits do not prove that provenance precisely enough, so that family remains fail-closed.

## 5. True HU special case

Clean ordinary true-HU 4BP is:

`SB/Button open -> BB 3bet -> SB/Button 4bet -> BB call`.

Thus the standard final 4bettor is SB/Button and is **IP postflop**.

A true-HU BB final 4bet after a three-raise sequence implies a different/reversed history such as limp-reraise dynamics. It is not assigned the ordinary opener-4bet policy merely because `raise_count = 3`.

## 6. Professional 100bb cash fill

The following are **P**, not claims about Crusher source frequencies.

### 6.1 General 4BP geometry

Even with 100bb starting stacks, a normal 4BP often reaches the flop at low or medium-low SPR. That changes the value of one-pair hands relative to an SRP, but does not create a universal `TP+ = stack off` rule.

The CBet node asks only whether to bet this flop and which broad size family to use. A later raise/call/jam node must re-evaluate commitment.

### 6.2 Static A/K/Q-high and paired boards

The 4bettor commonly retains substantial range advantage and can use small bets at high frequency in clean HU 4BP ranges. Overpairs and strong top pairs are natural value/protection bets. Selected backdoor bluffs are most plausible IP and against the less-condensed continuing family.

### 6.3 Low/middle connected boards

The caller's condensed pairs/suited continues interact better with these structures. Checking rises, especially OOP and against the original opener continuing versus a cold 4bet. Strong value and premium equity remain candidates for larger/polar betting.

### 6.4 Cold4 versus opener-call

This is treated more cautiously than opener4 versus 3bettor-call. An opener that continues after facing a cold 4bet normally reaches the flop with a particularly strong/condensed range. CashCrusher therefore does not import a broad air tail here.

### 6.5 Cold4 versus 3bettor-call

The 3bettor's continue versus a cold 4bet is also strong, but its preflop construction can be wider than the opener's cold4 continue in late-position battles. Static-high IP pressure is allowed somewhat more often, still without pretending the ranges are identical.

## 7. Sizing

Current strategic IDs remain:

- `1` ~33% pot;
- `2` ~50% pot;
- `3` ~75% pot;
- `0` check.

A 4BP often prefers the small family on static boards because the pot is already large and ranges are compressed. Medium sizing is used for more selective dynamic pressure. Whether a low-SPR bet should become an explicit jam belongs to the later sizing/commitment audit, not to a global rule in this CBet policy.

## 8. Implemented now

- true-HU clean opener4: SB/Button 4bettor IP vs BB 3bettor-call;
- reduced-HU clean opener4 vs 3bettor-call, IP/OOP;
- reduced-HU clean cold4 vs original opener-call, IP/OOP;
- reduced-HU clean cold4 vs 3bettor-call, IP/OOP.

Still fail-closed:

- HU 4BP vs non-raiser survivor;
- backraise/reversed/limp-reraise 4BP;
- multiway 4BP policy;
- 5bet+;
- later commitment versus flop aggression.

## Provenance summary

| Element | Provenance |
|---|---|
| initiative / IP-OOP / texture / hand-class architecture | A |
| clean first-orbit 4BP topology proof | A/P engineering from persisted history |
| exact HU 4BP action frequencies | P |
| ambiguous chronology | fail-closed, evidence limitation |
| later commitment/stack-off | separate node review; no blanket conclusion |
