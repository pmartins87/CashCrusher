# CashCrusher Status

Last update: 2026-08-23

Working branch: `gate-00-context-engine`

`main` remains intentionally untouched by development strategy code until parser/runtime gates are passed.

## Project contract

- Target: six-max cash post-flop AI in OpenPPL/OpenHoldem.
- Runtime supports hands dealt 2h, 3h, 4h, 5h or 6h as seats empty/sit out.
- Preflop is used to reconstruct post-flop context/ranges, not to decide current project preflop strategy.
- Strategic provenance is mandatory: T / A / P / X.
- Source-derived and professional-theory rules remain explicitly distinguishable.
- Unknown/unsupported strategic context fails closed.
- OpenPPL strategy code uses flat complete `WHEN` rules; indentation is never logical scope.
- Every `f$cc_*` function requires nearby Source/Provenance documentation in CI.

## Stack-depth migration rule

DeepCrusher short-stack logic is a **review flag**, not an automatic deletion rule.

For every stack-sensitive inherited rule:

- do not assume it transfers unchanged to ordinary 100bb cash;
- do not assume it becomes invalid merely because CashCrusher starts deeper;
- review the exact pot/range/board/action/effective-stack/SPR context;
- classify locally as T, A, P or X.

This applies to TP+/draw commitment lines, `f$Raise_Committed`, `f$hand_StackOffDraws`, `f$allin_on_betsize_balance_ratio`, `BetMax` and related mechanisms.

## Gate 00 — context/stack foundation

Design/code foundation is complete; OpenHoldem parser/runtime certification remains pending.

Important correction now frozen:

- HU uses exact Hero-v-Villain effective stack;
- multiway preserves both **shallowest effective** and **deepest effective**;
- actor-specific defense later uses actor-specific effective stack;
- a short sidepot player cannot make the whole multiway pot inherit short-stack aggression;
- true-HU deal, preflop-reduced HU and postflop-reduced HU remain separate range origins.

## Gate 01 — Flop CBet

Implemented baselines include:

- true-HU and reduced-HU ordinary SRP;
- SB-v-BB and opener-OOP-v-later-coldcaller SRP gaps;
- true-HU limp-raised BB-PFA-OOP;
- HU and multiway ISO;
- HU and multiway plain 3BP/squeeze with opener / pre-3bet coldcaller / post-3bet coldcaller provenance;
- true-threeway and exact 4/5/6-way ordinary SRP;
- clean supported HU 4BP families.

Still fail-closed: multiway 4BP, reversed/backraise/limp-reraise 4BP histories without stronger chronology evidence, and 5bet+.

### Flop sizing / all-in

Native strategic palette remains 33 / 50 / 75 / pot.

Local `BetMax` is currently used only for mechanically forced/equivalent execution when the reviewed requested size already reaches Hero's available stack or the deepest/all-live effective relationship.

Historical DeepCrusher ~50% effective / ~60% Hero-stack promotion remains diagnostic rather than one generic CashCrusher action. This does not ban it: an exact node may restore a strategic jam when its range/board/SPR logic supports it.

`f$Raise_Committed` remains defense-owned and has not been globally disabled.

## Gate 01N — executed flop history now implemented

The project no longer treats a pre-action CBet decision as proof that a CBet actually happened.

`CashCrusher_Flop_ActionHistory.txt` uses closed OpenHoldem round-2 history:

- `didchecround2`;
- `didcallround2`;
- `didraisround2`;
- `didbetsizeround2`;
- `didalliround2`;
- `lastraised2`.

It distinguishes:

- normal executed CBet;
- skipped CBet + check-through;
- check-call;
- check-raise/re-aggression;
- CBet → raise → call;
- CBet → re-aggression;
- planned normal sizing unexpectedly executed all-in;
- planned mechanical all-in unexpectedly executed as normal sizing.

### Flop strategic snapshot for Turn

Before the action, the history-aware CBet wrapper also snapshots only **plan/provenance facts** that disappear after the flop:

- 2P+ / overpair / TP / lower pair / no-made primary class;
- TP kicker bands relevant to direct source trees;
- premium/good/weak draw features;
- BDSD/BDFD;
- quality/pure air;
- flop strategic texture parent and selected exact flop facts.

These markers never prove execution. A Turn source branch consumes them only together with actual executed CBet history.

## Gate 02 — Turn CBet started

### Source audit / foundation

`GATE_02A_TURN_CBET_SOURCE_AUDIT.md` freezes the key source boundary:

- standard Turn CBet is separate from flop X/R, CBet-call-raise, donk, probe and delayed histories;
- current turn hand strength supersedes stale flop class;
- flop class/backdoors remain useful provenance where source explicitly depends on them;
- no generic TP+ stack-off rule;
- HUSB `20bb+ -> 100/200%` is not a literal 100bb-cash transplant;
- HUBB low-SPR shove remains an exact-node candidate, not a global rule;
- BTN-v-BB / BTN-v-SB are the strongest direct reduced-HU IP source descendants;
- SB-v-BB retains its distinct source checking/XR architecture;
- EP/MP range gaps, 3BP/squeeze/4BP and 4-way+ Turn strategy are P-heavy.

Portable turn runout primitives now cover completed/super-completed turns, newly completed straight/flush, OC/mOC, undercard, glued OC, paired turn and the exact HUSB two-low pressure-card source shape.

### Implemented Turn-CBet strategic children

Current router has five source-anchored HU descendants:

1. **true HU HUSB — SB/Button PFA IP vs BB**;
2. **reduced HU BTN PFA IP vs BB**;
3. **reduced HU BTN PFA IP vs SB**;
4. **true HU BB PFA OOP after SB limp → BB raise → call**;
5. **reduced HU SB PFA OOP vs BB** source-safe subset.

Notable source preservation:

- HUSB TP/OP barrels are separate from response to a turn raise;
- HUSB flop-TP demotion on turn overcard gets the smaller source barrel;
- HUSB good-draw and narrow air pressure-card branches remain distinct;
- BTN-v-BB preserves fresh TP vs carried TP/OP and the flop-BDSD weak-TP exception;
- BTN-v-SB does **not** inherit HUSB's generic draw barrel: source says flop draw/air CBet normally gives up turn unless it improves;
- SB-v-BB does **not** inherit an IP TP+ barrel tail: source often checks TP+ after actual CBet to induce/protect X/R, with the explicit newly-straight-completing turn pot-size exception retained;
- true-HU limp-raised HUBB value uses completed/non-completed sizing without automatically importing its historical low-SPR shove.

All other Turn-CBet families currently return false / size 0 rather than borrow a neighboring strategy.

## Current automated checks

GitHub Actions currently runs:

1. global `f$cc_*` dependency / flat-WHEN / provenance linter;
2. deterministic multiway shallowest/deepest stack-geometry tests;
3. deterministic flop final-action/history + strategic-snapshot source contract.

`tests/TURN_CBET_POLICY_MATRIX.md` documents the current Turn source-anchored acceptance cases and explicit fail-closed gaps.

## Remaining release blockers

No table-ready claim before:

1. Gate00 OpenHoldem parser/runtime context validation;
2. whole-bot history-aware `f$flop` and `f$BestBetsize` composition;
3. deterministic OpenHoldem flop/turn policy replays;
4. completion of Turn SRP six-max gaps, ISO, 3BP, squeeze, 4BP and multiway;
5. subsequent River/Float/Donk/Probe/Delayed and 32 defense gates;
6. final stack-sensitive commitment audit in each action owner;
7. full regression / unknown-state fail-closed audit.

## Immediate development direction

Continue Gate02 without broad fallbacks:

- P-heavy UTG/HJ/CO PFA-IP versus blinds;
- P-heavy opener-PFA-OOP versus later nonblind cold caller;
- postflop-reduced-HU and current multiway SRP;
- then ISO → plain 3BP → squeeze → 4BP;
- only after strategic coverage, add Turn runtime sizing/all-in execution and replay fixtures.
