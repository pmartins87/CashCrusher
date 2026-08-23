# Gate 01 — Deep-stack commitment decoupling from DeepCrusher TP+

Status: **binding strategic migration audit**.

## Why this audit exists

DeepCrusher was built for Spin/short-stack geometry. In that environment, a large fraction of top-pair-plus hands quickly become economically committed. That fact is useful context for understanding the source, but it is **not transferable as a generic six-max cash rule**.

CashCrusher therefore separates two questions that are often coupled in DeepCrusher:

1. **Should Hero bet/call this street with this hand?**
2. **Is Hero willing to play the remaining effective stack for this hand?**

A positive answer to question 1 never automatically answers question 2.

## Concrete DeepCrusher source behavior being quarantined

### 1. `f$Raise_Committed`

DeepCrusher contains a generic helper that promotes an already-profitable flop/turn call into an all-in raise when the call consumes most of Hero's or Villain's effective resources. The core thresholds are approximately 55% of the relevant remaining stack geometry.

That helper makes sense as a short-stack simplification, but it is **X** in CashCrusher because:

- a profitable call can remain a call even when large;
- stack depth, range polarity, nut distribution and future street geometry matter;
- a bluffcatcher must not become a value shove merely because the call is expensive;
- in multiway pots, effective stack versus one actor cannot be replaced by a generic shortest-stack commitment rule.

The CashCrusher linter now rejects any executable reference to `f$Raise_Committed`.

### 2. TP+/overpair frequently behaves like a commitment family

DeepCrusher contains many branches where `TopPairReal`, `TopPairOrBetter`, overpair or a broad TP+ bucket is sufficient to continue aggressively, especially at low/very-low SPR.

That is not treated as an error in the source: it reflects the game geometry the bot was designed for.

For CashCrusher, however:

- **top pair = one-pair hand**;
- **overpair = one-pair hand**;
- one pair may be value, bluffcatch, thin value, check-back, check-call or fold depending on the exact node;
- one pair does not become a stack-off hand because its label says TP+;
- the same hand can be a comfortable stack-off at SPR ~1 and a clear non-stack-off at SPR 8+.

### 3. DeepCrusher itself already contains exceptions

The later source-fidelity work in DeepCrusher contains several corrections where plain top pair is explicitly **not** a generic raise versus polarized large bets, and where some TP+ source families call/check rather than raise.

This reinforces the migration rule: even inside the source, `TP+` is not a universal action truth. CashCrusher must therefore preserve the useful hand classification while discarding any accidental global commitment meaning.

## CashCrusher commitment contract

### A. Attack nodes own only their immediate action

If a flop CBet function returns `true`, it means:

> bet this flop with the reviewed size family.

It does **not** mean:

- call a check-raise;
- 3bet a check-raise;
- call an all-in;
- barrel every turn;
- barrel every river;
- play for stacks.

The same applies to Donk, Float, Probe and Delayed-Bet nodes.

### B. Defense/raise nodes must re-evaluate commitment from scratch

A stack-off decision must be owned by the exact response node and consider, where relevant:

- pot family: SRP / ISO / 3BP / squeeze / 4BP;
- Hero and Villain range provenance;
- exact absolute matchup and IP/OOP/multiway relative position;
- current board/runout and nut distribution;
- hand class **and** kicker/nut quality;
- effective stack and raw SPR versus the relevant actor;
- Villain sizing and line;
- whether the hand began HU or multiway;
- whether Hero's current hand improved or was reclassified on the new street.

### C. No generic made-hand stack-off ladder

CashCrusher will not contain a global rule such as:

```text
TP+ -> stack off
Overpair+ -> stack off
TwoPair+ -> stack off
```

Even two pair can be a non-nut bluffcatch/value hand on some deep, connected or multiway runouts. Stronger made-hand categories increase willingness to continue but do not replace context.

### D. Low-SPR one-pair stack-offs are allowed only locally

This audit does **not** say one pair can never play for stacks.

Examples where one pair can legitimately become a stack-off candidate include some:

- 3BP/4BP low-SPR flops;
- blind-v-blind wide-range pots;
- heavily polarized range-advantage spots;
- shallow effective stacks created naturally by preflop action.

But the rule must be derived in that exact node. It must never arrive through a generic `TP+`, `StrongMade`, `call >55% stack` or `f$Raise_Committed` shortcut.

## OpenPPL enforcement

The static linter enforces several parts of this contract:

- `f$Raise_Committed` executable reference -> hard error;
- `f$hand_StackOffDraws` executable reference -> hard error;
- nonzero `f$allin_on_betsize_balance_ratio` -> hard error;
- `BetMax` without local `ALLIN_OWNER_REVIEWED` marker -> hard error;
- `BetMax` inside current flop-CBet strategy modules -> hard error.

The marker is deliberately noisy. Any future all-in branch must explain why that **exact** node owns the stack-off.

## Migration classification

| DeepCrusher concept | CashCrusher classification |
|---|---|
| TP/overpair hand classification | T/A descriptor |
| board- and sizing-dependent TP behavior | A |
| low-SPR willingness to stack some one-pair hands | A/P, exact-node only |
| global TP+ commitment implication | X |
| `f$Raise_Committed` call-to-shove promotion | X |
| `StackOffDraws` action shortcut | X |
| automatic half-stack bet-to-jam conversion | X |
| explicit exact-node all-in after full deep-stack audit | P/A allowed |

## Consequence for Gate 01

The current Flop CBet baselines may bet top pair or overpair frequently where range/board advantage supports it. That is intentional and is **not** a regression to the DeepCrusher stack-off model.

Commitment will only be decided later when the bot actually faces a raise, a large bet, a later-street barrel or a node whose reviewed strategy explicitly owns an all-in.
