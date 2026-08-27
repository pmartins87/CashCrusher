# Gate 02D.3 — Turn CBet after a multiway flop reduces to heads-up

Status: **source audit complete; CashCrusher policy is A/P for the closest BTN-v-both-blinds origin and P-heavy elsewhere**.

## 1. The historical routing hazard

The legacy `f$game_*` predicates are dynamic positional shells. In the 3-handed source:

- `3wBTNv2p` requires BTN plus two live opponents (`headsupchair == -1`);
- after one opponent folds, `headsupchair` identifies the survivor and the current shell becomes `3wBTNvBB` or `3wBTNvSB`.

That is mechanically useful for current position, but it does **not** preserve the range history.

Example:

`BTN open -> SB call -> BB call`  
flop: BTN CBet into **two** opponents -> SB folds -> BB calls  
turn: BTN versus BB.

The surviving BB called a **multiway flop CBet**. It is not the same range as BB calling a heads-up BTN-v-BB flop CBet. CashCrusher must therefore keep `HU origin = postflop reduced` and must not route this turn to the ordinary BTN-v-BB second-barrel tree.

## 2. What DeepCrusher actually supports

DeepCrusher contains a mature `3wBTNv2p` Turn-CBet branch sourced from CrusherTBP because the dedicated Starting Strategy has a gap for that exact initiative-CBet family. The branch is materially broader than a pure value tree: it can continue TP+, selected second pair/pocket pair, frontdoor draws and some overcard/gutshot pressure.

This is useful evidence, but it describes the state where **both opponents are still live on turn**. It does not explicitly specify the one-fold / one-call transition.

Therefore:

- the BTN-v-SB-v-BB flop origin is the closest **A/P donor**;
- it is not a T transplant;
- the current `3wBTNvBB` or `3wBTNvSB` turn branch is **not** the correct source donor merely because only one opponent remains.

## 3. Other six-max origins

CashCrusher can reach the same current HU state from many flop origins absent from the Spin source, for example:

- UTG PFA vs BTN + BB;
- HJ PFA vs CO + BB;
- CO PFA vs BTN + SB + BB;
- SB PFA vs BTN + BB;
- four-, five- or six-player flops that collapse to one opponent after Hero's CBet.

These are **P-heavy**. The legacy 3-way positional shells may explain FIRST/MIDDLE/LAST structure, but they do not provide the actual six-max ranges or turn frequencies.

## 4. Range-selection consequence of a multiway flop call

The sole turn survivor is more selected than a generic heads-up flop caller because they continued while additional players were still relevant to the flop decision. The effect generally increases with:

- more flop entrants;
- a larger flop CBet;
- a nonblind cold-caller origin versus a wide blind-defense origin;
- dynamic/completed board interaction.

This supports a conservative second-barrel baseline relative to ordinary flop-HU trees:

- robust made value remains active;
- one-pair value is more runout-, range- and SPR-sensitive;
- strong draws remain candidates to barrel;
- weak draws and pure air tighten materially;
- 4-way+ flop origins receive the strongest selection penalty.

These are professional-theory constraints, not solver-exact frequencies.

## 5. Exact survivor provenance

`src/CashCrusher_Turn_PostFlopReducedHU_Context.txt` reconstructs:

- canonical opponent mask that entered the flop;
- current sole survivor position;
- opponents that disappeared on flop;
- original flop entrant count;
- blind versus nonblind survivor class;
- exact Hero position;
- original flop CBet size ID;
- current IP/OOP relation.

The current opponent mask must be a subset of the reconstructed flop-entry mask. Ordinary SRP additionally requires the survivor's persisted preflop call bit.

## 6. Strongest source-descendant family

The exact shape

`BTN PFA -> flop versus SB+BB -> one blind calls flop CBet -> turn HU`

is treated separately.

Its source donor is **`3wBTNv2p`**, not `3wBTNvBB`/`3wBTNvSB`, because the latter describe a heads-up flop origin once used literally. The CashCrusher policy is intentionally narrower than the mature TBP v2p branch because the surviving range has passed an additional multiway selection event.

## 7. 4-way+ flop origins

There is no direct Crusher turn-CBet source. These remain P-heavy. A first deterministic baseline should emphasize:

- trips+ and strong two-pair value;
- overpair / strongest TP only on sufficiently clean runouts and with depth awareness;
- premium draws selectively;
- no generic pure-air second-barrel tail.

A short third player on the flop does not by itself make the surviving deep relationship short-stack. Current HU effective SPR against the actual survivor is the relevant turn geometry.

## 8. Stack-depth rule

Nothing in this Gate globally disables or imports the old short-stack commitment mechanisms.

A Turn CBet with TP/OP means only **bet this street with this size**. Whether Hero later calls a raise, reraises, or plays for stacks belongs to the exact defensive/continuation node and must be reviewed using the actual effective stack and SPR.

## 9. Fail-closed boundary

The node fails closed when:

- current HU Villain cannot be matched to a flop entrant;
- flop-entry/current-live masks are inconsistent;
- ordinary-SRP survivor does not have the required preflop call evidence;
- actual flop CBet history is not the standard executed CBet parent;
- runtime plan/history snapshots are inconsistent.

No ordinary heads-up Turn-CBet strategy is used as fallback.
