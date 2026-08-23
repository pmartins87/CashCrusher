# Gate 01N — Flop final-action / history audit

Status: **implemented in code + deterministic truth-table test; OpenHoldem replay/parser validation still pending**.

## Problem being solved

A postflop strategy must distinguish:

- Hero **had** a CBet opportunity;
- Hero's strategy **planned** a CBet;
- Hero **actually executed** a CBet;
- Hero had the opportunity but **actually checked**;
- Hero checked and the street **checked through**;
- Hero checked and later **called or raised**;
- Hero CBet and then **called a raise**;
- Hero CBet and then **re-aggressed**.

These histories own different turn nodes. They cannot be reconstructed safely from one pre-action boolean.

## DeepCrusher source lesson

The audited DeepCrusher already discovered this exact class of bug.

Inside `f$flop`, Retro Nothing-Here 02 and Retro12A explain that old markers such as `user_3wBTN_Had_Air_OTF` were written **before** the final flop action. Such a marker could therefore remain true whether Hero later CBet or actually checked back.

The repair was to capture the **final checked action** before allowing the hand to enter Turn Delayed CBet.

CashCrusher generalizes that lesson instead of adding another family-specific patch.

### Provenance classification

- **A**: preserve the DeepCrusher final-action repair principle.
- **T**: use OpenHoldem's executed-action history once the flop is closed.
- **P**: add explicit plan-vs-execution drift diagnostics for CashCrusher runtime composition.

## OpenHoldem source verification

The project OpenHoldem source was checked directly.

### User variables

`Set user_xyz` sets an OpenPPL boolean user variable during formula evaluation. The user-variable engine clears all of them on **hand reset**.

Therefore user variables are suitable for per-hand pre-action metadata such as:

- CBet opportunity seen;
- intended CBet size family;
- whether Gate01K.3B expected a mechanically equivalent direct `BetMax`.

They are **not** proof that the casino/autoplayer actually performed the action.

### Executed action history

`CSymbolEngineHistory::UpdateAfterAutoplayerAction()` updates history only after an autoplayer action succeeds.

For flop (betround 2), relevant closed-street symbols are:

- `didchecround2`;
- `didcallround2`;
- `didraisround2`;
- `didbetsizeround2`;
- `didalliround2`.

OpenHoldem's successful betpot path explicitly registers the action as `k_autoplayer_function_betsize`. OpenPPL percentage-pot decisions are also translated into the betsize path. Consequently `didbetsizeround2` is the expected executed-history signal for current CashCrusher 33/50/75/pot CBet execution.

`lastraised2` supplies the final recorded flop aggressor after the round closes.

## New architecture

File: `src/CashCrusher_Flop_ActionHistory.txt`.

### Pre-action capture

Canonical CBet action entrypoint:

`f$cc_flop_cbet_action_with_history`

It stores only:

- `user_cc_flop_cbet_opportunity_seen`;
- `user_cc_flop_cbet_plan_bet_seen` when the reviewed router plans a bet.

It deliberately never stores an `executed_cbet` user flag.

### Planned sizing capture

`f$cc_flop_cbet_execution_betsize` now stores:

- one of planned 33 / 50 / 75 / 100 size markers;
- `user_cc_flop_cbet_plan_expected_allin` only when Gate01K.3B itself chose the mechanically equivalent `BetMax` path.

These remain plan markers.

### Executed flop classification

At Turn/River, closed round-2 history produces:

- `f$cc_hist_flop_initial_cbet_executed`;
- `f$cc_hist_flop_skipped_cbet_checkthrough`;
- `f$cc_hist_flop_checked_then_called`;
- `f$cc_hist_flop_checked_then_aggressed`;
- `f$cc_hist_flop_cbet_then_called_raise`;
- `f$cc_hist_flop_cbet_then_reaggressed`.

The presence of `didchecround2` has priority when classifying the **initial** CBet decision. A check-raise is therefore never mislabeled as a CBet.

## Canonical turn parents

### Standard Turn CBet

`f$cc_hist_turn_standard_cbet_parent` requires:

1. CBet opportunity was seen;
2. Hero never checked on flop;
3. Hero never called on flop;
4. exactly one normal betsize was executed;
5. no generic re-raise or all-in action followed;
6. `lastraised2 = userchair`.

This means a normal flop CBet called by one or more Villains can reach Turn CBet.

A flop CBet followed by Villain raise + Hero call cannot.

A flop CBet followed by Hero re-raise cannot; it belongs to a separate raised-flop continuation family.

### Turn Delayed CBet

`f$cc_hist_turn_delayed_cbet_parent` requires:

1. Hero had the original CBet opportunity;
2. Hero actually checked;
3. Hero made no later flop call/raise/betsize/all-in action;
4. the hand reached the next street.

A check-call or check-raise therefore cannot leak into Delayed CBet.

## Planned versus executed all-in

Gate01N also separates:

- planned normal bet -> executed normal bet;
- Gate01K.3B planned direct mechanical `BetMax` -> executed all-in;
- planned normal bet -> unexpectedly executed direct all-in;
- planned direct `BetMax` -> unexpectedly executed normal betsize.

`f$cc_hist_flop_unexpected_allin_promotion` is particularly important before the eventual global `f$allin_on_betsize_balance_ratio` is composed. It can expose a callback that silently rewrites a reviewed 33/50/75 node after the node itself has finished deciding strategy.

This diagnostic does **not** assert that the unexpected shove is always strategically wrong. It proves that execution differed from the node-owned plan and therefore requires audit.

## Explicit non-goals

Gate01N does not yet implement:

- Turn CBet strategy;
- Delayed CBet strategy;
- check-call/check-raise defense;
- flop CBet response to a raise;
- whole-bot `f$flop` composition;
- OpenHoldem replay certification.

It only makes the history required by those nodes reliable.

## Validation

`tools/test_flop_action_history.py` covers at least:

- standard CBet-call -> Turn CBet parent;
- skipped CBet/check-through -> Delayed CBet parent;
- check-call exclusion;
- check-raise exclusion;
- CBet -> raise -> call exclusion;
- CBet -> re-aggress exclusion;
- intended mechanical direct all-in;
- unexpected global all-in promotion;
- expected all-in not executed;
- stale planned bet followed by actual check;
- non-CBet aggression from another node not being mislabeled as CBet.

CI runs this together with the global OpenPPL linter and multiway stack-geometry tests.

## Next strategic use

Gate 02 Turn CBet should consume `f$cc_hist_turn_standard_cbet_parent` as its source-history parent.

Later Delayed CBet should consume `f$cc_hist_turn_delayed_cbet_parent`.

Neither should reconstruct flop action from the existence of initiative alone.
