# Gate 01F — Flop CBet in 3-bet pots

Status: **source/context audit complete for HU Hero-3bettor families; implementation scope intentionally staged**.

## 1. Why this node cannot be copied from DeepCrusher

DeepCrusher has useful postflop CBet logic but does **not** contain a clean, dedicated deep-stack 3-bet-pot CBet strategy.

The audited top-level flow is important:

- `f$flop_Raise` sends any `f$Init_Hero` state to `f$flop_Raise_SRP_Initiative`;
- `f$Init_Hero` can be true after Hero raised/3bet preflop and was called;
- `f$flop_Raise_SRP_Initiative` then sends a checked-to flop to the generic `f$move_flop_cbet`;
- `f$move_flop_cbet` is organized mostly by `HUSB`, `HUBB`, `3wBTNvBB`, `3wSBvBB`, etc., with limped-vs-nonlimped distinctions, not a true SRP-vs-3BP range decomposition;
- `f$pot_Reraised` exists in the source but is not used to create a dedicated branch inside `f$move_flop_cbet`.

Therefore a literal claim that DeepCrusher has solved "3BP CBet" would be false. What it gives us is **A-level architecture and hand/board concepts**, not 3BP frequencies.

This is particularly important because Spin stacks make many 3-bet pots very low-SPR. The old action can be reasonable in that geometry while being materially wrong at 100bb+ cash depth.

## 2. Source components that remain useful (A)

Across HUSB/HUBB/3w initiative families, the source consistently supports:

- IP and OOP must not share one tree;
- static/high boards can support small broad pressure;
- lower/connected/draw-heavy boards require more checking or selective betting;
- marginal showdown-value pairs belong partly in the check range;
- draw quality matters;
- OOP can intentionally skip CBet with strong draws to preserve check-raise lines;
- value sizing can grow on more dynamic structures.

These principles are retained as **A** constraints.

## 3. Source components rejected for 3BP cash (X)

The following are not transplanted literally:

- shallow stack thresholds such as `<=16/20 BB`;
- `StackOffDraws` as an action class;
- automatic shove/commit plans after a raise;
- blanket residual-air CBet tails from short-stack HU/Spin;
- use of a game label alone as a proxy for a 3BP range.

## 4. New 3BP survivor taxonomy (P/A architecture)

A two-raise pot can reach a HU flop against multiple fundamentally different ranges.

### 4.1 Original opener called the 3bet

Example:

`HJ open -> BTN 3bet -> HJ call`.

This is the standard baseline 3BP range pair.

### 4.2 Pre-3bet cold caller survived a squeeze

Example:

`UTG open -> HJ call -> BTN squeeze -> UTG fold -> HJ call`.

The HJ range is not the opener-call range. It first cold-called an open and then continued versus a squeeze.

### 4.3 Post-3bet cold caller survived

Example:

`UTG open -> BTN 3bet -> BB coldcall -> UTG fold`.

Calling this simply "BTN 3bettor versus opener" would be a range-routing bug.

`src/CashCrusher_3BP_Context.txt` reconstructs and preserves these categories before policy.

## 5. True HU special case

In supported ordinary true-HU action order:

`SB/Button open -> BB 3bet -> SB/Button call`.

The 3bettor is **BB and OOP**.

An ordinary plain-3BP state with true-HU Hero 3bettor IP is not a normal topology. A SB/Button limp-reraise would reverse first-orbit raiser order and remains outside `f$cc_pf_3bet_plain_proven`.

Therefore CashCrusher must not create a fake symmetric true-HU IP 3bettor strategy merely because the generic router once had an IP stub.

## 6. Professional deep-stack theory fill (P)

The exact frequencies below are not claimed as solver outputs. They are robust professional NLHE principles used to fill the source gap.

### 6.1 3bettor versus opener-call, IP

Compared with SRP:

- ranges are tighter and SPR is lower;
- 3bettor often retains strong range/nut advantage on A-high, K-high and many paired/static boards;
- small CBet can therefore be used broadly on favorable static structures;
- low/middle connected boards interact more with caller pocket pairs/suited continues, so checking rises and bets become more selective;
- marginal one-pair holdings do not need to force three streets simply because SPR is lower;
- robust value and premium draws can use larger sizing on dynamic boards.

### 6.2 3bettor versus opener-call, OOP

OOP does **not** mean "check almost everything" in 3BP. A blind 3bettor can still have substantial range/nut advantage, especially versus late opens.

However:

- the checking range must remain protected;
- marginal made hands check more than IP;
- strong draws can remain in X/R lines;
- low/mid dynamic boards receive materially more checks;
- small betting remains attractive on static high/paired structures when range advantage is strong.

### 6.3 True-HU BB 3bettor OOP

HUBB provides useful A ancestry for the OOP shape, but 3BP range compression is a new P adjustment. The source's calm-board small / dynamic-board large value idea is retained; exact short-stack action is not.

### 6.4 Post-3bet cold caller

A cold-call-3bet range is generally condensed/selected and often stronger than a routine open-call range in the middle of its distribution. CashCrusher will therefore **not** reuse the opener-call policy automatically. This family remains fail-closed until separately implemented.

### 6.5 Squeeze pots

A squeeze changes both the 3bettor's construction and the continuing ranges. Dead money does not justify pretending squeeze = plain 3BP. Squeeze versus opener, squeeze versus original coldcaller and squeeze versus post-3bet coldcaller remain separate P families.

## 7. Sizing contract

Current deep-stack flop palette remains:

- `1` ~33%;
- `2` ~50%;
- `3` ~75%;
- `4` pot, reserved;
- `0` check.

Professional 3BP baseline will generally favor the small family more often than an SRP on static high boards because pot geometry is already larger and SPR lower. Larger sizes are reserved for selectively polar/dynamic regions.

This is P/A architecture, not a hard solver-size claim.

## 8. Implementation staging decision

Implement first:

1. true-HU plain 3BP: BB 3bettor OOP versus SB/Button opener-call;
2. reduced-HU plain 3BP: 3bettor IP versus original opener-call;
3. reduced-HU plain 3BP: 3bettor OOP versus original opener-call.

Keep fail-closed for now:

- plain 3BP versus post-3bet cold caller;
- squeeze versus opener;
- squeeze versus pre-3bet cold caller;
- squeeze versus post-3bet cold caller;
- multiway 3BP;
- reversed/limp-reraise chronology;
- 4BP.

This staging maximizes source/range confidence and prevents a generic 3BP policy from contaminating distinct continuation ranges.

## Provenance summary

| Element | Provenance |
|---|---|
| initiative / IP-OOP / checked-to architecture | A from DeepCrusher |
| hand/board dynamic concepts | A |
| dedicated deep-stack 3BP frequencies | P |
| opener/coldcaller/squeeze survivor taxonomy | P/A architecture |
| true-HU BB-3bettor-OOP topology | T/A mechanics |
| <=16/20BB / StackOffDraws / auto-jam | X |
