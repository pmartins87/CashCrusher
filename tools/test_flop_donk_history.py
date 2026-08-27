#!/usr/bin/env python3
"""Gate07K / Gate08B.0 closed Flop Donk action-history contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = (ROOT / "src" / "CashCrusher_Flop_Donk_ActionHistory.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def wrapper_contract() -> None:
    wrap = block(HIST, "f$cc_flop_donk_action_with_history")
    assert "Set user_cc_flop_donk_opportunity_seen" in wrap
    assert "Set user_cc_flop_donk_state_snapshot_recorded" in wrap
    for i in range(1, 9):
        assert f"f$cc_flop_donk_family_id = {i} Set user_cc_flop_donk_state_family_{i}" in wrap
    for token in (
        "f$cc_flop_donk_source_value_action Set user_cc_flop_donk_state_source_value",
        "f$cc_flop_donk_source_lowpair_action Set user_cc_flop_donk_state_source_lowpair",
        "f$cc_flop_donk_source_draw_action Set user_cc_flop_donk_state_source_draw",
        "f$cc_flop_donk_source_turn_xc_draw_candidate Set user_cc_flop_donk_state_source_turn_xc_draw",
        "f$cc_flop_donk_source_turn_xc_highair_candidate Set user_cc_flop_donk_state_source_turn_xc_highair",
        "f$cc_flop_donk_router Set user_cc_flop_donk_plan_bet_seen",
        "f$cc_flop_donk_router Return true Force",
    ):
        assert token in wrap


def closed_execution_contract() -> None:
    closed = block(HIST, "f$cc_hist_flop_donk_closed")
    assert "IsTurn || IsRiver" in closed

    bet = block(HIST, "f$cc_hist_flop_donk_initial_bet_executed")
    assert "user_cc_flop_donk_opportunity_seen" in bet
    assert "didchecround2 = 0" in bet
    assert "didbetsizeround2 > 0 || didalliround2 > 0" in bet

    check = block(HIST, "f$cc_hist_flop_donk_initial_check_executed")
    assert "didchecround2 > 0" in check

    called = block(HIST, "f$cc_hist_flop_donk_then_called_raise")
    assert "didcallround2 > 0" in called
    assert "lastraised2 != userchair" in called

    parent = block(HIST, "f$cc_hist_flop_donk_standard_called_parent")
    for token in (
        "didchecround2 = 0",
        "didcallround2 = 0",
        "didraisround2 = 0",
        "didbetsizeround2 = 1",
        "didalliround2 = 0",
        "lastraised2 = userchair",
    ):
        assert token in parent


def snapshot_contract() -> None:
    fam = block(HIST, "f$cc_hist_flop_donk_family_id")
    assert "f$cc_hist_flop_donk_family_marker_count != 1 Return 0 Force" in fam
    for i in range(1, 9):
        assert f"user_cc_flop_donk_state_family_{i} Return {i} Force" in fam

    xc_count = block(HIST, "f$cc_hist_flop_donk_source_turn_xc_marker_count")
    assert "user_cc_flop_donk_state_source_turn_xc_draw" in xc_count
    assert "user_cc_flop_donk_state_source_turn_xc_highair" in xc_count

    draw = block(HIST, "f$cc_hist_flop_donk_source_turn_xc_draw_snapshot")
    assert "f$cc_hist_flop_donk_family_id = 1" in draw
    assert "user_cc_flop_donk_state_source_turn_xc_draw" in draw
    assert "!user_cc_flop_donk_state_source_turn_xc_highair" in draw

    highair = block(HIST, "f$cc_hist_flop_donk_source_turn_xc_highair_snapshot")
    assert "f$cc_hist_flop_donk_family_id = 1" in highair
    assert "user_cc_flop_donk_state_source_turn_xc_highair" in highair
    assert "!user_cc_flop_donk_state_source_turn_xc_draw" in highair

    snap = block(HIST, "f$cc_hist_flop_donk_snapshot_consistent")
    assert "f$cc_hist_flop_donk_primary_class_marker_count != 1 Return false Force" in snap
    assert "f$cc_hist_flop_donk_player_count_marker_count != 1 Return false Force" in snap
    assert "BitCount(f$cc_hist_flop_donk_live_opp_mask) != (f$cc_hist_flop_donk_player_count - 1)" in snap
    assert "f$cc_hist_flop_donk_source_turn_xc_marker_count > 1 Return false Force" in snap
    assert "f$cc_hist_flop_donk_family_id = 1" in snap
    assert "f$cc_hist_flop_donk_source_subtype_marker_count != 1" in snap


def mismatch_and_parent_contract() -> None:
    mismatch = block(HIST, "f$cc_hist_flop_donk_runtime_mismatch")
    for token in (
        "!f$cc_flop_donk_plan_markers_consistent Return true Force",
        "!f$cc_hist_flop_donk_snapshot_consistent Return true Force",
        "f$cc_hist_flop_donk_planned_bet_but_checked Return true Force",
        "f$cc_hist_flop_donk_executed_without_plan Return true Force",
        "f$cc_hist_flop_donk_unexpected_allin_promotion Return true Force",
        "f$cc_hist_flop_donk_expected_allin_not_executed Return true Force",
    ):
        assert token in mismatch

    valid = block(HIST, "f$cc_hist_flop_donk_valid_parent")
    assert "f$cc_hist_flop_donk_initial_bet_executed" in valid
    assert "f$cc_hist_flop_donk_snapshot_consistent" in valid
    assert "!f$cc_hist_flop_donk_runtime_mismatch" in valid


if __name__ == "__main__":
    wrapper_contract()
    closed_execution_contract()
    snapshot_contract()
    mismatch_and_parent_contract()
    print("PASS: Gate07K/08B.0 closed Flop Donk action-history contract")
