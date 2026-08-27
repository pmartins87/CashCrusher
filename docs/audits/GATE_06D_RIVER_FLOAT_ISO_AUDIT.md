# Gate 06D — River Float in isolation / true-HU limp-raised pots

Status: **strategy/context/runtime-independent policy complete at the static/deterministic layer; CI PASS in run #616 before this documentation commit**.

## 1. Source ownership finding

The DeepCrusher router for preflop `GotRaised/Isolated` pots explicitly sends a LAST/MIDDLE river state with nothing to call to `f$move_river_floatbet`. Therefore isolation history really can own a River Float decision; it is not an ordinary-SRP fallback.

However, `f$move_river_floatbet` itself does **not** contain a dedicated isolation-pot value/bluff table. Its portable positive strategy is the generic River-Float value ladder already frozen in Gate06B:

- current nutted / 2P+ value;
- current real overpair;
- current real top pair with at most four better kicker ranks;
- source-specific 3wBBvSB busted-draw bluff only when exact prior draw/call provenance is available.

HUSB also contains an explicit negative for a missed real draw on River Float, but that predicate depends on historical real-draw recording. CashCrusher does not yet have a generic defensive Turn-call snapshot capable of proving that history for arbitrary River Float parents.

Result: Gate06D does not invent an ISO-specific source action. Source-sized positive value remains Gate06B; all source-silent ISO behavior below is A/P or P.

## 2. What HUSB ISO material actually contributes

The supplied HUSB source gives meaningful information about how Hero reaches later streets after limp-calling an isolation raise:

- in the ISO pot, raising TP is often unnecessary because SPR is already smaller and Hero has position;
- medium/bottom pair can call a 50% flop CBet and can continue versus sufficiently small Turn aggression;
- A/K-high plus real backdoor structure can call selected small ISO CBet lines and continue reactively;
- the source repeatedly treats completed / pressure runouts more cautiously;
- missed real draws do not become a generic River Float bluff.

These facts constrain the arriving range, but the source does **not** say that every such Turn call should bluff when checked to on the river. They are therefore architecture/range evidence, not a direct betting table.

## 3. True HU limp-raised is separate from multi-handed ISO

CashCrusher distinguishes:

`SB/Button limp -> BB raise -> SB call`

in a real two-seat hand from a multi-handed isolation raise.

The true-HU family requires:

- true-HU deal origin;
- proven HU limp-raise chronology;
- Hero SB/Button caller;
- BB as final preflop aggressor;
- BB as the actual Turn aggressor Hero called;
- BB still the sole River Villain.

It does not require or masquerade as `f$cc_pf_iso_proven`.

This preserves direct HUSB structural ancestry without claiming that 100bb cash is the same range/SPR environment as the Spin source.

## 4. Multi-handed ISO range provenance

Gate06D independently reconstructs Hero and the actual Turn aggressor as one of:

1. original pre-raise limper;
2. post-raise coldcaller;
3. isolation raiser / PFA.

Both identities must be unique. Overlap or an unknown origin fails closed.

This permits clean-HU parents to remain different:

- original limper versus isolator;
- post-raise coldcaller versus isolator;
- isolator who later lost initiative and called Villain Turn aggression.

A coldcaller is not treated as an original limp-call range merely because both are preflop callers.

## 5. Multiway-origin preservation

A current HU River after a multiway ISO flop is not relabeled as clean HU.

Gate06A can prove the flop entrant count and current River field but does not yet snapshot the player count at the exact Turn call that created River Float. Therefore:

- flop multiway -> River HU is an explicit unresolved selected-range parent;
- current River multiway is separate;
- any flop that began 4+ way is outside the supplied 3-max source domain even if later folds leave only two or three players.

No HU bluff tree consumes those states.

## 6. Professional policy for source-silent states

The first deterministic ISO River-Float gap policy is deliberately value-heavy.

For <=3-player source-sized fields, Gate06B already owns TP-top4 / OP / 2P+ value. The remaining weak TP, second pair, lower pair and no-made hands are reviewed checks unless a later exact exploit/history snapshot proves otherwise.

No generic missed-draw bluff is added because current `NoMadeHand` does not tell us what draw Hero held when calling the Turn bet or which blockers remain on the River.

## 7. Four-plus-origin value

When the ISO flop began four-plus way, the generic three-player source value ladder is not used.

The P-heavy robust-value threshold is:

- literal nuts always;
- on four-card straight/flush public structures: literal nuts or full-house+;
- when a flush is possible: made flush+;
- when only a straight is possible: made straight+;
- otherwise: current 2P+.

Literal nuts request 75%; other approved robust values request 50%.

This is a River value-bet decision only. It does not authorize calling a raise or playing stacks.

## 8. Short-stack migration rule

Gate06D neither deletes nor imports old short-stack commitment logic globally.

The historical HUSB fact that an ISO pot can have lower SPR remains strategically relevant. But River Float still owns only bet/check plus requested sizing. Any response to a raise or all-in belongs to the future defensive owner with actor-specific effective-stack geometry.

No `BetMax`, `Raise_Committed`, `StackOffDraws`, HandPower tail or random strategy appears in the Gate06D executable policy.

## 9. Implementation and tests

Implemented:

- `src/CashCrusher_River_Float_ISO.txt`
- canonical River-Float router family ID 3
- `tools/test_river_float_iso.py`
- updated global `tools/test_river_float_coverage.py`
- CI integration in `.github/workflows/static-lint.yml`

The full suite passed in GitHub Actions run **#616**, including the new ISO contract and every prior CBet/Float regression.

## 10. Next boundary

Gate06E should audit **plain 3BP River Float** and **squeeze River Float** source-first. They must remain separate because opener-call, pre-3bet coldcaller and post-3bet coldcaller ranges reach a Turn call through materially different preflop paths.

No plain-3BP policy should be used as a squeeze fallback.
