#!/usr/bin/env python3
"""Deterministic Gate02N tests for closed-turn action provenance.

Covers the round-3 truth table and source-contract requirements for Turn state
snapshots. This is not yet an OpenHoldem parser/replay fixture.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY_FILE = ROOT / "src" / "CashCrusher_Turn_ActionHistory.txt"
EXEC_FILE = ROOT / "src" / "CashCrusher_Turn_CBet_AllinEquivalence.txt"


@dataclass(frozen=True)
class H:
    opportunity: bool = True
    planned_bet: bool = False
    size_recorded: bool = False
    expected_allin: bool = False
    snapshot_ok: bool = True
    plan_ok: bool = True
    checks: int = 0
    calls: int = 0
    raises: int = 0
    betsizes: int = 0
    allins: int = 0
    final_aggressor_hero: bool = False


def initial_cbet(h: H) -> bool:
    return h.opportunity and h.checks == 0 and (h.betsizes > 0 or h.allins > 0)


def direct_allin_cbet(h: H) -> bool:
    return initial_cbet(h) and h.allins > 0 and h.betsizes == 0 and h.raises == 0


def checkthrough(h: H) -> bool:
    return h.opportunity and h.checks > 0 and h.calls == 0 and h.raises == 0 and h.betsizes == 0 and h.allins == 0


def checked_then_called(h: H) -> bool:
    return h.opportunity and h.checks > 0 and h.calls > 0 and h.raises == 0 and h.betsizes == 0 and h.allins == 0


def checked_then_aggressed(h: H) -> bool:
    return h.opportunity and h.checks > 0 and (h.raises > 0 or h.betsizes > 0 or h.allins > 0)


def cbet_then_called_raise(h: H) -> bool:
    return initial_cbet(h) and h.calls > 0 and not h.final_aggressor_hero


def cbet_then_reaggressed(h: H) -> bool:
    return initial_cbet(h) and (h.betsizes >= 2 or h.raises > 0 or (h.betsizes > 0 and h.allins > 0))


def standard_river_cbet_parent(h: H) -> bool:
    return h.opportunity and h.checks == 0 and h.calls == 0 and h.raises == 0 and h.betsizes == 1 and h.allins == 0 and h.final_aggressor_hero


def valid_standard_river_parent(h: H) -> bool:
    return standard_river_cbet_parent(h) and h.snapshot_ok and h.plan_ok and not runtime_mismatch(h)


def unexpected_allin_promotion(h: H) -> bool:
    return h.size_recorded and not h.expected_allin and direct_allin_cbet(h)


def expected_allin_not_executed(h: H) -> bool:
    return h.expected_allin and initial_cbet(h) and h.betsizes > 0 and h.allins == 0


def runtime_mismatch(h: H) -> bool:
    if not h.plan_ok or not h.snapshot_ok:
        return True
    if h.planned_bet and h.checks > 0:
        return True
    if initial_cbet(h) and not h.planned_bet:
        return True
    if unexpected_allin_promotion(h) or expected_allin_not_executed(h):
        return True
    return False


def run_truth_table() -> None:
    # Clean one-size Turn CBet -> canonical River CBet parent.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, final_aggressor_hero=True)
    assert initial_cbet(h) and standard_river_cbet_parent(h) and valid_standard_river_parent(h)

    # Strategy checks and turn checks through -> later no-action/delayed family.
    h = H(checks=1)
    assert checkthrough(h) and not standard_river_cbet_parent(h)

    # Check-call and check-raise are not delayed/checkthrough and not River CBet.
    h = H(checks=1, calls=1)
    assert checked_then_called(h) and not checkthrough(h) and not standard_river_cbet_parent(h)
    h = H(checks=1, betsizes=1, final_aggressor_hero=True)
    assert checked_then_aggressed(h) and not initial_cbet(h) and not standard_river_cbet_parent(h)

    # Turn CBet then Villain raise/call by Hero: Villain closes turn as aggressor.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, calls=1, final_aggressor_hero=False)
    assert initial_cbet(h) and cbet_then_called_raise(h) and not standard_river_cbet_parent(h)

    # Hero bets then re-aggresses: raised-turn continuation, not ordinary river CBet.
    h = H(planned_bet=True, size_recorded=True, betsizes=2, final_aggressor_hero=True)
    assert initial_cbet(h) and cbet_then_reaggressed(h) and not standard_river_cbet_parent(h)

    # Planned mechanical all-in and direct all-in agree, but Hero has no ordinary River CBet parent.
    h = H(planned_bet=True, size_recorded=True, expected_allin=True, allins=1, final_aggressor_hero=True)
    assert direct_allin_cbet(h) and not unexpected_allin_promotion(h) and not standard_river_cbet_parent(h)

    # External/global promotion of a planned normal size is diagnosed.
    h = H(planned_bet=True, size_recorded=True, expected_allin=False, allins=1, final_aggressor_hero=True)
    assert direct_allin_cbet(h) and unexpected_allin_promotion(h) and runtime_mismatch(h)

    # Local adapter expected BetMax but runtime remained normal sized.
    h = H(planned_bet=True, size_recorded=True, expected_allin=True, betsizes=1, final_aggressor_hero=True)
    assert standard_river_cbet_parent(h) and expected_allin_not_executed(h) and runtime_mismatch(h)
    assert not valid_standard_river_parent(h)

    # Executed aggression without canonical plan capture is rejected by valid parent.
    h = H(planned_bet=False, size_recorded=False, betsizes=1, final_aggressor_hero=True)
    assert initial_cbet(h) and standard_river_cbet_parent(h) and runtime_mismatch(h)
    assert not valid_standard_river_parent(h)

    # Snapshot corruption also fail-closes otherwise clean history.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, final_aggressor_hero=True, snapshot_ok=False)
    assert standard_river_cbet_parent(h) and not valid_standard_river_parent(h)


def run_source_contract() -> None:
    history = HISTORY_FILE.read_text(encoding="utf-8")
    execution = EXEC_FILE.read_text(encoding="utf-8")

    for symbol in (
        "didchecround3", "didcallround3", "didraisround3", "didbetsizeround3",
        "didalliround3", "lastraised3", "userchair",
    ):
        assert symbol in history, f"missing OpenHoldem turn-history symbol: {symbol}"

    for name in (
        "##f$cc_turn_cbet_action_with_history##",
        "##f$cc_hist_turn_state_snapshot_consistent##",
        "##f$cc_hist_turn_initial_cbet_executed##",
        "##f$cc_hist_turn_skipped_cbet_checkthrough##",
        "##f$cc_hist_turn_checked_then_called##",
        "##f$cc_hist_turn_checked_then_aggressed##",
        "##f$cc_hist_turn_cbet_then_called_raise##",
        "##f$cc_hist_turn_cbet_then_reaggressed##",
        "##f$cc_hist_river_standard_cbet_parent##",
        "##f$cc_hist_river_standard_cbet_parent_valid##",
        "##f$cc_hist_turn_cbet_runtime_mismatch##",
    ):
        assert name in history, f"missing Gate02N function: {name}"

    # Opportunity marker must be written even when reviewed strategy checks.
    assert "When f$cc_turn_cbet_opportunity Set user_cc_turn_cbet_opportunity_seen" in history
    assert "Set user_cc_turn_cbet_executed" not in history

    # River needs disappearing turn provenance, including origin/composition.
    for marker in (
        "Set user_cc_turn_state_had_2pplus",
        "Set user_cc_turn_state_had_overpair",
        "Set user_cc_turn_state_had_top_pair",
        "Set user_cc_turn_state_had_second_pair",
        "Set user_cc_turn_state_had_third_or_worse_pair",
        "Set user_cc_turn_state_had_no_made",
        "Set user_cc_turn_state_had_premium_draw",
        "Set user_cc_turn_state_had_air",
        "Set user_cc_turn_state_runout_super_completed",
        "Set user_cc_turn_state_runout_new_completion",
        "Set user_cc_turn_state_family_12",
        "Set user_cc_turn_state_was_hu",
        "Set user_cc_turn_state_was_multiway",
        "Set user_cc_turn_state_relpos_middle",
        "Set user_cc_turn_state_players_6",
        "Set user_cc_turn_state_live_utg",
        "Set user_cc_turn_state_live_bb",
    ):
        assert marker in history, f"missing Turn snapshot marker: {marker}"

    # The local execution adapter owns size/all-in plan markers, not history proof.
    for marker in (
        "Set user_cc_turn_cbet_plan_size_recorded",
        "Set user_cc_turn_cbet_plan_size_25",
        "Set user_cc_turn_cbet_plan_size_33",
        "Set user_cc_turn_cbet_plan_size_40",
        "Set user_cc_turn_cbet_plan_size_50",
        "Set user_cc_turn_cbet_plan_size_625",
        "Set user_cc_turn_cbet_plan_size_75",
        "Set user_cc_turn_cbet_plan_size_100",
        "Set user_cc_turn_cbet_plan_expected_allin",
    ):
        assert marker in execution, f"missing Turn plan marker: {marker}"

    assert "When f$cc_turn_cbet_natural_allin_equivalent Return BetMax Force" in execution
    assert "Return BetMax" not in history

    # Residual diagnostic families 5/6 may be snapshotted but can never own a bet plan.
    snapshot_guard = "When user_cc_turn_cbet_plan_bet_seen && (user_cc_turn_state_family_5 || user_cc_turn_state_family_6) Return false Force"
    assert snapshot_guard in history

    # Standard River-CBet parent is deliberately only one normal turn betsize.
    assert "didbetsizeround3 = 1" in history
    assert "didalliround3 = 0" in history


if __name__ == "__main__":
    run_truth_table()
    run_source_contract()
    print("PASS: Gate02N closed-turn action-history + River-parent contract")
