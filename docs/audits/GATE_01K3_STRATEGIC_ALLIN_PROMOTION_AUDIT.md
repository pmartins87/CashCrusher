# Gate 01K.3C — Strategic CBet near-all-in promotion audit

## Scope

This audit answers a narrower question than ordinary stack-off strategy:

> After a CashCrusher flop-CBet node has already chosen **BET** and a reviewed pot-fraction size, when may execution replace that legal smaller size with `BetMax`?

It does **not** decide whether Hero should call or raise versus Villain aggression. `f$Raise_Committed` belongs to those later defensive nodes.

## Source mechanisms are separate

DeepCrusher contains at least three different mechanisms that can end with all chips in play.

### 1. Explicit sizing-router ~60% Hero-stack promotion

In flop, turn and river sizing routers, many requested pot fractions are converted to `BetMax` when the requested raise-to amount is at least about 60% of `StackSize`.

This is an execution-size rule. It does not itself inspect hand class because the upstream action node has already chosen to bet/raise.

### 2. `f$allin_on_betsize_balance_ratio`

The callback has two materially different layers:

- special branches return a near-zero ratio when the intended bet is at least about 50% of `f$EffectiveStack_BKP`;
- otherwise a `.50` fallback lets OpenHoldem convert a requested size to all-in once it reaches roughly 50% of Hero's total available balance.

DeepCrusher `f$EffectiveStack_BKP` uses the biggest active opponent. In multiway, its source-faithful effective-stack analogue is therefore CashCrusher **deepest effective**, not shallowest effective.

### 3. `f$Raise_Committed`

This is not a CBet-sizing rule. On flop/turn it can turn an already-approved **call** into an all-in raise when the call consumes roughly 55% of Hero resources or leaves a HU Villain nearly committed.

CashCrusher will audit this with the defensive call/raise nodes it actually owns.

## OpenHoldem runtime facts

`ChangeBetsizeToAllin(amount_to_raise_to)`:

1. evaluates `f$allin_on_betsize_balance_ratio`;
2. multiplies that ratio by Hero's maximum available betsize (`currentbet + balance`);
3. converts the requested amount to all-in when the requested amount reaches that critical size.

Betpot actions are converted through the same all-in adjustment path after `BetsizeForBetpot()` computes their raise-to amount.

OpenHoldem also caps explicit entered bet sizes at Hero's available balance. Therefore:

- **requested size exceeds Hero balance** is a mechanical clipping/all-in fact;
- **requested size merely consumes 50–60% of Hero/effective stack** is a strategic promotion choice.

They must not be conflated.

## Mathematical consequence of the historical 50% effective trigger

For HU, let:

- `E` = street-start effective stack;
- `P` = street-start pot;
- `B` = requested CBet;
- `r = B/E`.

If Villain calls, projected next-street SPR is:

`(E - B) / (P + 2B)`.

At `r = 0.50`, the residual effective stack is only `0.5E`. Even if the original pot were tiny relative to E, projected SPR approaches but never exceeds 0.5. At `r = 0.60`, it approaches at most about 0.333.

This explains why the old short-stack implementation often treated such sizes as near-commitment.

It does **not** prove that a smaller bet and an immediate shove have identical EV in 100bb cash. Fold response, range composition, hand class, blockers, board and future realization still matter.

## CashCrusher classification

### T/A — mechanical all-in equivalence: IMPLEMENTED

`CashCrusher_Flop_CBet_AllinEquivalence.txt` may use `BetMax` when the reviewed requested CBet already:

1. reaches Hero's available stack; or
2. reaches the deepest/all-live effective relationship.

These cases do not require importing a historical 50/60% strategic threshold.

### X as a generic rule — shortest-only multiway reach

If a requested bet reaches one short opponent but not the deepest live effective relationship, global `BetMax` promotion is rejected for that reason alone.

This is a sidepot-divergence state, not whole-field commitment.

### A/P — historical 50% effective trigger: REVIEW CANDIDATE, NOT GENERIC ACTION

The source mechanism is meaningful and remains preserved in diagnostics. It can become correct in particular cash nodes, especially naturally compressed 3BP/4BP geometries.

It is not globally activated in current CBet execution because doing so would silently replace the deliberately authored 33/50/75 size policy in every affected hand class, including bluffs.

### A/P — historical 60% Hero-stack trigger: REVIEW CANDIDATE, NOT GENERIC ACTION

The same conclusion applies. A requested size consuming >=60% of Hero stack creates a tiny residual stack, but this is still a strategic sizing decision unless the requested size already reaches Hero/all-live effective stack.

### Deferred — `f$Raise_Committed`

Ownership belongs to flop/turn defense after Villain aggression. It is not evaluated in this Gate.

## Node-by-node implications

### Ordinary SRP

At ordinary 100bb starting depth, a normal 33/50/75 CBet seldom reaches historical near-all-in thresholds unless preflop sizing was unusually large or Hero began the hand short. A generic source transplant offers little upside and risks severe overbetting when it does trigger.

Status: historical threshold retained as diagnostic; no generic strategic promotion.

### ISO pots

ISO pots can contain heterogeneous stacks and sidepots more often than clean HU SRP. Shortest-only reach is especially unsafe as a shove trigger.

Status: use dual-bound geometry; no generic strategic promotion.

### 3BP / squeeze

SPR is naturally lower and the historical source intuition becomes more relevant. However current CashCrusher 3BP/squeeze policies explicitly choose board/hand-dependent 33/50/75 sizes. Converting every >=50%-effective planned bet into a shove would change those policies after the fact.

Status: candidate for future explicit node-owned jam branches, not a global execution callback.

### 4BP

This is the strongest candidate for explicit flop jams because ordinary 100bb 4BP can reach low SPR naturally. The current 4BP policy intentionally uses mainly 33/50 sizing and states that later stack-off is separate.

Status: future explicit 4BP jam branch may be added where source/professional theory supports it; historical threshold alone is insufficient.

### Multiway

Any strategic promotion must reason about deepest effective stack and sidepot structure. A short opponent does not automatically compress Hero's decision versus a deeper opponent.

Status: no generic strategic promotion.

## Architecture decision

CashCrusher will **not** use a single historical 50/55/60 threshold as the owner of CBet jams.

Instead:

1. upstream strategy owns whether a CBet exists and its intended size family;
2. Gate 01K.3B handles only mechanically forced/equivalent all-ins;
3. future explicit jam branches are owned by exact strategic nodes;
4. the global `f$allin_on_betsize_balance_ratio` is composed only after all affected postflop sizing owners are audited.

This does not disable the inherited mechanisms. It preserves their source meaning and prevents them from silently overriding cash-specific strategy outside the contexts where they remain valid.
