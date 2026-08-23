# Gate 02A — Turn CBet source-first audit

Status: **source boundary frozen; common history/hand/runout layer implemented; matchup policy proceeds family-by-family**.

## Scope

This audit covers only a **standard second barrel after Hero actually executed a normal flop CBet and remained the final flop aggressor**.

Gate01N defines that parent as `f$cc_hist_turn_standard_cbet_parent`.

The following are explicitly outside this Turn-CBet node even though portions of the historical DeepCrusher `f$move_turn_cbet` function contained them:

- flop check-raise then turn continuation;
- flop check-call;
- flop CBet → Villain raise → Hero call;
- flop CBet → Hero re-raise;
- flop donk continuation;
- skipped flop CBet / Delayed CBet;
- Probe / Float / Delayed Float histories.

This separation is required because the DeepCrusher function accumulated multiple histories over time. CashCrusher routes by **executed action provenance first**, then strategy.

## Sources reviewed

Primary implementation source:

- current audited `DeepCrusher(1).txt`, `##f$move_turn_cbet##`.

Starting Strategy / human-reviewed corpus:

- `1- CRUSHFEST HUSB - ok25.docx`;
- `10- NOVO CRUSHFEST HUSB.docx`;
- `3- CRUSHFEST 3wBTNvBB.docx`;
- `4- CRUSHFEST - 3wBTNvSB.docx`;
- `6- CRUSHFEST 3wSBvBB.docx`;
- `8- CRUSHFEST - 3wBBvSB - ok25 (Review with NCF).docx`;
- `11- NOVO CRUSHFEST HUBB.docx`;
- mature CrusherTBP gap-fill where explicitly identified by the audited DeepCrusher.

The current DeepCrusher is used to understand the already-reconciled implementation and its audit comments. Starting Strategy is used to determine which ideas are genuinely source-supported versus later gap-fill.

## Source-wide strategic findings

### 1. Turn is not determined by current hand class alone

The source repeatedly distinguishes:

- TP already held on flop versus TP first made on turn;
- carried overpair versus current TP;
- flop air/draw CBet versus flop made-hand CBet;
- specific flop backdoor properties;
- whether the turn is an overcard, undercard, paired card, glued overcard, newly completed card or super-completed structure.

Therefore Gate01N now snapshots the flop CBet hand/texture state, but Turn policy always reclassifies **current turn strength first**.

A stale `flop TP` marker can modify the line; it cannot force Hero to remain classified as TP after the board changes.

### 2. A called flop CBet materially changes the range interaction

New Crushfest HUSB explicitly says OOP players under-defend against initial aggression and, once they call, their later-street range is stronger. It warns against later-street proactive overinvestment without equity.

This is source support for **more selective turn pressure than flop pressure**, not for a universal barrel percentage.

### 3. One-pair value and stack commitment are separate questions

The source often barrels TP/OP for value. The Spin implementation also contains many low-SPR or short-stack conversions to shove.

CashCrusher separates them:

- `bet Turn with TP/OP` may be T/A source-supported;
- `play the entire stack` requires its own exact range/SPR/board/action review.

No generic `TP+ -> stack-off` rule is imported.

## Family audit

| CashCrusher Turn family | Best source donor | Fidelity | Treatment |
|---|---|---:|---|
| true-HU SB/Button PFA IP vs BB ordinary SRP | HUSB | high structural/source | A: preserve hand/runout logic; re-audit cash sizing/commitment |
| reduced-HU BTN PFA IP vs BB | `3wBTNvBB` | high | A: strongest ordinary 6-max descendant |
| reduced-HU BTN PFA IP vs SB | `3wBTNvSB` | high | A: strongest BTN-v-SB descendant |
| reduced-HU CO/HJ/UTG PFA IP vs blind | BTN-v-blind source shells | medium/low | A/P: range topology rebuilt |
| reduced-HU SB PFA OOP vs BB | `3wSBvBB` | high positional | A/P: source turn-check/value architecture retained cautiously |
| opener PFA OOP vs later nonblind caller | no direct Spin range family | low | P-heavy |
| true-HU BB PFA OOP after SB limp → BB raise → call | HUBB / HUSB limp mechanics | medium | A/P; separate from ordinary HU SB-open SRP |
| true multiway ordinary SRP | `3wBTNv2p` only where exact shape fits | medium/low | A/P; FIRST/MIDDLE largely P-heavy |
| 4/5/6-way SRP | none | none | P |
| 3BP / squeeze | no dedicated deep-cash source | low | P-heavy, source architecture only |
| 4BP | no dedicated source | none | P-heavy, compressed-SPR geometry explicit |

## HUSB — source-supported second-barrel logic

The New Crushfest HUSB supplies unusually clear source guidance.

### TP or better

Source conclusions include:

- avoid ordinary second barrel on a **super-completed** turn unless Hero has enough additional equity to bet/call;
- standard second-barrel sizing is around **75%**;
- if Hero had flop TP and the turn brings an overcard, the old TP often becomes a lower pair but still has a smaller **50%** value/blocking barrel;
- the source explicitly warns that turn raises are population-strong and TP does not automatically continue versus them.

The last point is especially important for CashCrusher: a positive Turn CBet with TP does not imply a call versus check-raise.

### MP/BP

Source conclusions:

- second pair, non-completed turn: ~50%;
- second pair, completed turn: ~25%;
- third pair: ~25%;
- intent is thin value/equity denial/blocking of later proactive bluffs, not stack commitment.

### Draws

New HUSB identifies “good” second-barrel draws and uses ~75%; weak draws check. It separately says missed draws generally do not 3-barrel bluff.

### Air

Source permits a narrow second barrel when the flop contains two low cards (6 or lower) and the turn brings an mOC/OC that neither pairs nor newly completes straight/flush.

CashCrusher implements the mechanical source-shaped runout predicate as `f$cc_turn_husb_air_pressure_card_source`; the matchup policy decides whether to consume it.

## HUSB old-source compatibility warning

The audited DeepCrusher restored some old HUSB rules when New Crushfest did not actually replace the exact spot. One restored rule says that at **20bb+** a non-completed drawy flop / non-completed turn TP+ line may increase from 75% to 100% or even discretionary 200%.

This cannot be transplanted literally as “Cash starts 100bb, therefore always pot/overbet.”

Why:

- “20bb+” was still expressed inside Spin stack geometry;
- cash 100bb produces much higher absolute and often higher effective turn SPR;
- overbet EV depends on exact range/nut advantage, blockers and board topology.

Classification:

- **T**: the old source really contains the idea;
- **X**: literal `effective stack >=20bb -> 100%` as a universal cash rule;
- **A/P candidate**: exact polar overbet nodes may later be rebuilt where range/board geometry supports them.

## 3wBTN-v-BB — strongest reduced-HU IP source

The audited source has explicit multi-street planning:

- current 2P+ -> strong value barrel;
- TP first made on turn -> value barrel;
- carried OP: glued OC / mOC / other turns use different sizes;
- carried TP with weak kicker checks more; preserved flop BDSD proxy can support a smaller barrel;
- stronger carried TP barrels;
- flop no-made CBet plans contain both barrel and give-up runouts.

This is valuable A-level ancestry for 6-max BTN-v-BB. For UTG/HJ/CO-v-BB, the **structure** transfers better than the literal frequency because the opener range and BB continuing range differ substantially.

## 3wBTN-v-SB — direct BTN-v-SB source

Starting Strategy is clear:

- 2P+/OP and stronger TP pursue value aggressively;
- TP with kicker below J is generally a two-street rather than three-street value hand;
- draws that CBet flop are intended to continue mainly when they actually improve to TP+;
- flop-air CBet gives up turn.

This is a strong reason not to give BTN-v-SB a generic “premium draw always barrel” tail merely because another source family does so.

## 3wSB-v-BB — important OOP exception

After an **actual** flop CBet, the source often checks general TP+ on turn to induce/protect an X/R line. A turn that newly completes a straight is an explicit large second-barrel exception. Air does not automatically 2-barrel after flop CBet.

This architecture is materially different from HUSB and BTN-v-BB. Therefore CashCrusher must not use one generic `PFA SRP Turn CBet` tree for IP and OOP.

## HUBB contamination that Gate01N removes

Historical `f$move_turn_cbet` contains both:

- continuation after a flop X/R; and
- continuation after an ordinary flop CBet.

The X/R source uses different sizings and hand thresholds. Gate01N's standard Turn-CBet parent excludes check-raise and re-aggression histories, so those branches cannot leak into ordinary Turn CBet.

The source also contains an ordinary-CBet rule that shoves TP/OP/2P+ on completed turns at low `StackPotRatio` (e.g. `<1.6`). That is a **contextual low-SPR candidate**, not a universal 100bb cash rule. If CashCrusher later restores a similar jam, the exact node must own it.

## 3wBB-v-SB and other nonmatching histories

The audited DeepCrusher contains source-exact Turn continuation for `3wBBvSB`, including direct all-in ideas on wet/completed turns. Its preflop/flop role is not a clean ordinary six-max PFA-SRP analogue for most CashCrusher matchups.

It may become useful in other attack/initiative families, but it is not a license to import “TP+ wet -> shove” into the ordinary SRP Turn-CBet router.

## True multiway source boundary

`3wBTNv2p` has mature CrusherTBP generic turn-CBet evidence because the dedicated Starting Strategy coverage is incomplete. That is an **A/P donor**, not a direct source tree.

Four-way+ has no literal DeepCrusher ancestor. Professional theory must therefore supply the policy while preserving source-supported principles:

- less fold equity with more players;
- tighter one-pair value threshold;
- reduced pure-air second barrels;
- premium equity and nut advantage matter more;
- deepest-effective stack must control whole-field low-SPR relaxations.

## Professional-theory fill rules for Gate 02

Where source ends, P rules may use:

- range advantage and nut advantage after flop-call filtering;
- turn-card effect on both ranges, not board texture alone;
- IP versus OOP equity realization;
- flop sizing and flop CBet range composition;
- current hand reclassification plus carried blockers/backdoors;
- exact HU SPR or corrected multiway deepest-effective geometry;
- polarization / merge incentives;
- blocker and unblocker effects;
- multiway tightening.

A P fill must remain a deterministic **baseline**, not be described as solver-exact unless solver evidence is actually introduced later.

## Frozen Gate02A decisions

1. Turn CBet consumes **executed** Gate01N history, never initiative alone.
2. Current turn strength supersedes stale flop hand class; stored flop class is provenance.
3. Standard CBet, X/R, CBet-call-raise, donk, probe and delayed histories remain separate.
4. No generic TP+ stack-off rule.
5. No generic HUSB `20bb+ -> pot/overbet` cash transplant.
6. No generic HUBB `SPR<1.6 -> shove` transplant; exact low-SPR node may later earn it.
7. BTN-v-BB and BTN-v-SB receive the strongest direct 3-handed ancestry.
8. SB-v-BB OOP keeps its distinct source tendency to check many TP+ turns rather than inheriting IP barrels.
9. EP/MP opener versus later nonblind caller is P-heavy.
10. 3BP/squeeze/4BP are separate Turn range families from SRP.
11. Multiway low-SPR relaxations use deepest-effective geometry unless an exact actor/sidepot is explicitly owned.
12. Unknown or history-inconsistent states fail closed.
