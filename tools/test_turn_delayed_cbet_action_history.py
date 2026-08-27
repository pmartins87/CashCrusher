#!/usr/bin/env python3
"""Gate12A.17 CLOSED Turn Delayed-CBet action-history contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_ActionHistory.txt").read_text(encoding="utf-8")


def block(name: str) -> str:
    marker = f"##{name}##"
    assert marker in H, f"missing {name}"
    tail = H.split(marker, 1)[1]
    return tail.split("##", 1)[0]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def wrapper_contract() -> None:
    w = block("f$cc_turn_delayed_cbet_action_with_history")
    assert "Set user_cc_turn_delayed_cbet_opportunity_seen" in w
    assert "Set user_cc_turn_delayed_cbet_state_snapshot_recorded" in w
    for i in range(1, 18):
        assert f"f$cc_turn_delayed_cbet_family_id = {i} Set user_cc_turn_delayed_cbet_state_family_{i}" in w
    for token in (
        "f$cc_turn_delayed_cbet_hubb_thirdpair_deldel_plan",
        "f$cc_turn_delayed_cbet_hubb_air_deldel_plan",
        "f$cc_turn_delayed_cbet_3w_bbvsb_plan_turncheck_bxb_river50",
        "f$cc_turn_delayed_cbet_3w_sbvbb_plan_lowpair_deldel_river50",
        "f$cc_turn_delayed_cbet_3w_sbvbb_plan_draw_connected_deldel",
        "f$cc_turn_delayed_cbet_3w_sbvbb_plan_air_ak_showdown",
    ):
        assert token in w
    assert "When f$cc_turn_delayed_cbet_router Set user_cc_turn_delayed_cbet_plan_bet_seen" in w
    assert "When f$cc_turn_delayed_cbet_router Return true Force" in w
    assert "When Others Return false Force" in w


def closed_history_contract() -> None:
    checked = block("f$cc_hist_turn_delayed_cbet_checked_through")
    for token in (
        "IsRiver",
        "user_cc_turn_delayed_cbet_opportunity_seen",
        "didchecround3 > 0",
        "didcallround3 = 0",
        "didraisround3 = 0",
        "didbetsizeround3 = 0",
        "didalliround3 = 0",
    ):
        if token == "IsRiver":
            assert token in block("f$cc_hist_turn_delayed_cbet_closed")
        else:
            assert token in checked

    normal_bet = block("f$cc_hist_turn_delayed_cbet_standard_bet_parent")
    assert "didbetsizeround3 = 1" in normal_bet
    assert "lastraised3 = userchair" in normal_bet
    assert "didchecround3 = 0" in normal_bet


def integrity_contract() -> None:
    snap = block("f$cc_hist_turn_delayed_cbet_snapshot_consistent")
    assert "f$cc_hist_turn_delayed_cbet_family_marker_count != 1 Return false Force" in snap
    assert "f$cc_hist_turn_delayed_cbet_primary_class_marker_count != 1 Return false Force" in snap
    assert "f$cc_hist_turn_delayed_cbet_player_count_marker_count != 1 Return false Force" in snap
    assert "BitCount(f$cc_hist_turn_delayed_cbet_live_opp_mask) != (f$cc_hist_turn_delayed_cbet_player_count - 1)" in snap
    assert "f$cc_hist_turn_delayed_cbet_source_check_plan_marker_count > 1 Return false Force" in snap

    mismatch = block("f$cc_hist_turn_delayed_cbet_runtime_mismatch")
    assert "f$cc_hist_turn_delayed_cbet_planned_bet_but_checked Return true Force" in mismatch
    assert "f$cc_hist_turn_delayed_cbet_executed_without_plan Return true Force" in mismatch

    parent = block("f$cc_hist_river_delayed_cbet_check_parent_valid")
    assert "f$cc_hist_turn_delayed_cbet_checked_through" in parent
    assert "f$cc_hist_turn_delayed_cbet_snapshot_consistent" in parent
    assert "!f$cc_hist_turn_delayed_cbet_runtime_mismatch" in parent


def source_bridge_contract() -> None:
    expected = {
        "f$cc_hist_river_delayed_cbet_hubb_deldel_valid": ("family_id = 2", "source_plan_hubb"),
        "f$cc_hist_river_delayed_cbet_hubb_air_deldel_valid": ("family_id = 2", "source_plan_hubb_air_deldel"),
        "f$cc_hist_river_delayed_cbet_bbvsb_bxb50_valid": ("family_id = 5", "source_plan_bbvsb_bxb_river50"),
        "f$cc_hist_river_delayed_cbet_sbvbb_lowpair_deldel50_valid": ("family_id = 6", "source_plan_sbvbb_lowpair_deldel50"),
        "f$cc_hist_river_delayed_cbet_sbvbb_draw_deldel50_valid": ("family_id = 6", "source_plan_sbvbb_draw_deldel50"),
        "f$cc_hist_river_delayed_cbet_sbvbb_air_ak_showdown_valid": ("family_id = 6", "source_plan_sbvbb_air_ak_showdown"),
    }
    for name, tokens in expected.items():
        b = block(name)
        assert "f$cc_hist_river_delayed_cbet_check_parent_valid" in b
        for token in tokens:
            assert token in b


def no_generic_leak_contract() -> None:
    code = executable(H).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "stackoff"):
        assert forbidden not in code, forbidden


if __name__ == "__main__":
    wrapper_contract()
    closed_history_contract()
    integrity_contract()
    source_bridge_contract()
    no_generic_leak_contract()
    print("PASS: Gate12A CLOSED action provenance for Gate13")
