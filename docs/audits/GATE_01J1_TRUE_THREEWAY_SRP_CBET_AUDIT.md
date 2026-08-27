# Gate 01J.1 — True three-way ordinary-SRP flop CBet audit

Status: **source audit complete; first CashCrusher baseline implemented separately for Hero FIRST / MIDDLE / LAST and caller composition**.

## 1. Exact scope

This gate covers only a flop that was already exactly three-way when the flop began:

- `f$cc_flop_entry_count = 3`;
- current `nplayersplaying = 3`;
- ordinary one-raise SRP;
- Hero is the PFA / final preflop aggressor;
- no flop bet before Hero acts.

It does **not** cover:

- a four-way+ flop that later becomes three-way;
- ISO pots;
- 3BP / squeeze / 4BP;
- multiway pots where Hero was not PFA.

## 2. What DeepCrusher actually contains

### 2.1 Hero LAST: `3wBTNv2p`

DeepCrusher contains a substantial `f$game_3wBTNv2p` branch inside `f$move_flop_cbet`. However, the audited source comments explicitly state that **no dedicated Starting Strategy file covers that exact CBet spot** and that the branch is the mature human-reviewed CrusherTBP gap fill.

Therefore this is not a T-grade literal strategy transplant. It is a useful **A/P donor**:

- relative LAST position matters;
- draw quality and overcards affect betting;
- some TP/second-pair regions check depending on board;
- sizing changes with texture/hand class;
- the source nevertheless ends with a very broad residual `Return true`, which is too strong to copy blindly into ordinary 100bb six-max multiway cash.

### 2.2 Hero FIRST / MIDDLE

The audited `f$move_flop_cbet` does **not** contain corresponding initiative-CBet branches for `f$game_3wSBv2p` or `f$game_3wBBv2p`.

The Starting Strategy file `9- CRUSHFEST BBorSBv2pp - ok25.docx` does cover blinds versus two opponents, but it is mainly a **donk/defense** strategy when BTN owns or may own initiative. It cannot be relabelled as PFA-CBet strategy.

Useful source philosophy from that file is still relevant as A-level constraint:

- three-way pots are more honest;
- betting flop/turn without equity is identified as a major mistake;
- weak multi-street bluffs should be rare;
- board interaction with both opponent ranges matters strongly.

FIRST and MIDDLE PFA-CBet therefore remain **P-heavy**, not disguised transplants.

## 3. Caller-composition axis added

Relative position alone is not enough in six-max cash. The same PFA can face materially different two-caller range structures.

CashCrusher preserves three coarse composition parents while retaining the exact live mask:

1. **BOTH_BLINDS** — both callers are SB+BB; generally the widest two continuing ranges;
2. **ONE_BLIND_ONE_NONBLIND** — mixed range topology;
3. **TWO_NONBLINDS** — two nonblind cold callers; generally more condensed/selected than two blind defenses.

These are P range parents, not exact solver ranges. Exact Hero position and exact opponent mask remain available for later refinement.

## 4. Professional multiway cash fill (P)

Robust principles used for the first baseline:

- CBet frequency falls materially versus HU because two ranges must continue/fold and equity realization changes;
- robust value remains the most reliable betting region;
- top pair / overpair may value bet, but medium/weak one-pair hands check much more than in short-stack Spin;
- low/mid connected boards interact strongly with caller ranges and require more checking;
- premium/nut-potential draws can bet, while many medium draws can remain in checks depending on relative position;
- pure air is sharply reduced; selected backdoor bluffs are concentrated on favorable static high boards, mainly when Hero is LAST;
- FIRST is most conservative because two opponents remain to act;
- MIDDLE must account for both the first player's check and the player still behind;
- LAST has the greatest freedom to value bet and choose equity-backed bluffs after both opponents check;
- no generic residual-air tail is imported from `3wBTNv2p`.

## 5. Stack-depth rule

No commitment helper is globally disabled by this audit. This gate owns only the first flop CBet/check and its sizing family.

If a particular multiway cash node later reaches low SPR where a DeepCrusher commitment helper becomes valid again, that helper can be T/A after exact review. Conversely, a short-stack threshold that fails at 100bb can be X locally.

## 6. Sizing

Current baseline retains the project size IDs:

- `1` ~33% pot;
- `2` ~50%;
- `3` ~75%;
- `4` pot reserved.

General baseline:

- static high / paired: mostly small-to-medium;
- dynamic high: medium for strong ranges;
- dynamic low/mid: larger only for robust value / premium equity;
- no all-in is implied by a size ID.

## 7. Still outside this gate

- four-way+ ordinary SRP;
- multiway ISO;
- multiway ordinary 3BP;
- multiway squeeze;
- 4BP;
- response after the flop CBet is raised;
- turn/river follow-through.
