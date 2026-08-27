#!/usr/bin/env python3
"""Gate05H closed Turn Float execution-history contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HIST = (SRC / "CashCrusher_Turn_Float_ActionHistory.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_Turn_Float_AllinEquivalence.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def snapshot_contract() -> None:
    effective = block(HIST, "f$cc_turn_float_effective_parent_id")
    assert "f$cc_turn_float_source_limped_bbv_sb_opportunity Return 4 Force" in effective
    assert "f$cc_turn_float_opportunity Return f$cc_turn_float_parent_id Force" in effective

    wrapper = block(HIST, "f$cc_turn_float_action_with_history")
    assert "Set user_cc_turn_float_opportunity_seen" in wrapper
    assert "Set user_cc_turn_float_state_snapshot_recorded" in wrapper
    for idx in range(1, 5):
        assert f"user_cc_turn_float_state_parent_{idx}" in wrapper
    for idx in range(1, 7):
        assert f"user_cc_turn_float_state_family_{idx}" in wrapper
    assert "When f$cc_turn_float_router Return true Force" in wrapper
    # No PRE-action marker may be named as if execution were already proved.
    assert "Set user_cc_turn_float_executed" not in wrapper

    snap = block(HIST, "f$cc_hist_turn_float_snapshot_consistent")
    assert "f$cc_hist_turn_float_parent_marker_count != 1" in snap
    assert "f$cc_hist_turn_float_primary_class_marker_count != 1" in snap
    assert "BitCount(f$cc_hist_turn_float_live_opp_mask) != (f$cc_hist_turn_float_player_count - 1)" in snap
    assert "user_cc_turn_float_plan_bet_seen && f$cc_hist_turn_float_family_marker_count != 1" in snap


def execution_contract() -> None:
    closed = block(HIST, "f$cc_hist_turn_float_closed")
    assert "IsRiver" in closed

    executed = block(HIST, "f$cc_hist_turn_float_initial_bet_executed")
    assert "user_cc_turn_float_opportunity_seen" in executed
    assert "didchecround3 = 0" in executed
    assert "didbetsizeround3 > 0 || didalliround3 > 0" in executed

    check = block(HIST, "f$cc_hist_turn_float_checked_back")
    assert "didchecround3 > 0" in check
    for token in ("didcallround3 = 0", "didraisround3 = 0", "didbetsizeround3 = 0", "didalliround3 = 0"):
        assert token in check

    called = block(HIST, "f$cc_hist_turn_float_then_called_raise")
    assert "didcallround3 > 0" in called
    assert "lastraised3 != userchair" in called

    reag = block(HIST, "f$cc_hist_turn_float_then_reaggressed")
    assert "didbetsizeround3 >= 2" in reag
    assert "didraisround3 > 0" in reag

    standard = block(HIST, "f$cc_hist_turn_float_standard_parent")
    for token in (
        "didchecround3 = 0",
        "didcallround3 = 0",
        "didraisround3 = 0",
        "didbetsizeround3 = 1",
        "didalliround3 = 0",
        "lastraised3 = userchair",
    ):
        assert token in standard


def plan_vs_execution_contract() -> None:
    mismatch = block(HIST, "f$cc_hist_turn_float_runtime_mismatch")
    for token in (
        "!f$cc_turn_float_plan_markers_consistent",
        "!f$cc_hist_turn_float_snapshot_consistent",
        "f$cc_hist_turn_float_planned_bet_but_checked",
        "f$cc_hist_turn_float_executed_without_plan",
        "f$cc_hist_turn_float_unexpected_allin_promotion",
        "f$cc_hist_turn_float_expected_allin_not_executed",
    ):
        assert token in mismatch

    river = block(HIST, "f$cc_hist_river_float_standard_parent_valid")
    assert "f$cc_hist_turn_float_standard_parent" in river
    assert "f$cc_turn_float_plan_markers_consistent" in river
    assert "!f$cc_hist_turn_float_runtime_mismatch" in river

    barrel = block(HIST, "f$cc_hist_turn_float_source_barrel_plan_valid")
    assert "f$cc_hist_river_float_standard_parent_valid" in barrel
    assert "user_cc_turn_float_plan_barrel_river" in barrel

    giveup = block(HIST, "f$cc_hist_turn_float_source_giveup_plan_valid")
    assert "f$cc_hist_river_float_standard_parent_valid" in giveup
    assert "user_cc_turn_float_plan_giveup_river" in giveup

    execute = block(ALLIN, "f$cc_turn_float_execution_betsize")
    # Source River plan is captured as a PRE-action plan in execution adapter.
    assert "f$cc_turn_float_river_plan_id = 1 Set user_cc_turn_float_plan_giveup_river" in execute
    assert "f$cc_turn_float_river_plan_id = 2 Set user_cc_turn_float_plan_barrel_river" in execute


if __name__ == "__main__":
    snapshot_contract()
    execution_contract()
    plan_vs_execution_contract()
    print("PASS: Gate05H closed Turn Float action-history + River-parent contract")
