#!/usr/bin/env python3
"""Gate08A Turn Donk ownership / closed-flop parent contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = (ROOT / "src" / "CashCrusher_Turn_Donk_History.txt").read_text(encoding="utf-8")


def block(name: str) -> str:
    marker = f"##{name}##"
    assert marker in HIST, f"missing {name}"
    start = HIST.index(marker) + len(marker)
    tail = HIST[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def aggressor_contract() -> None:
    valid = block("f$cc_turn_donk_flop_aggressor_history_valid")
    assert "raisbits2 >> lastraised2" in valid

    live = block("f$cc_turn_donk_flop_aggressor_live_opponent")
    assert "lastraised2 = userchair Return false Force" in live
    assert "playersplayingbits >> lastraised2" in live

    hero = block("f$cc_turn_donk_hero_owned_final_flop_aggression")
    assert "lastraised2 = userchair" in hero


def xc_parent_contract() -> None:
    call = block("f$cc_turn_donk_flop_check_call_only")
    for token in (
        "didchecround2 != 1 Return false Force",
        "didcallround2 != 1 Return false Force",
        "didraisround2 != 0 Return false Force",
        "didbetsizeround2 != 0 Return false Force",
        "didalliround2 != 0 Return false Force",
    ):
        assert token in call

    parent = block("f$cc_turn_donk_parent_flop_xc")
    for token in (
        "user_cc_flop_donk_opportunity_seen",
        "user_cc_flop_donk_state_snapshot_recorded",
        "f$cc_hist_flop_donk_family_marker_count = 1",
        "f$cc_hist_flop_donk_snapshot_consistent",
        "f$cc_turn_donk_flop_check_call_only",
        "f$cc_turn_donk_single_flop_aggressor",
        "f$cc_turn_donk_flop_aggressor_live_opponent",
        "!f$cc_turn_donk_hero_owned_final_flop_aggression",
    ):
        assert token in parent


def bc_parent_contract() -> None:
    parent = block("f$cc_turn_donk_parent_flop_donk_raise_call")
    for token in (
        "f$cc_hist_flop_donk_then_called_raise",
        "!f$cc_hist_flop_donk_then_reaggressed",
        "f$cc_hist_flop_donk_snapshot_consistent",
        "f$cc_flop_donk_plan_markers_consistent",
        "!f$cc_hist_flop_donk_runtime_mismatch",
        "f$cc_hist_flop_donk_family_marker_count = 1",
        "f$cc_turn_donk_flop_aggressor_live_opponent",
        "!f$cc_turn_donk_hero_owned_final_flop_aggression",
    ):
        assert token in parent

    pid = block("f$cc_turn_donk_parent_id")
    assert "f$cc_turn_donk_parent_count != 1 Return 0 Force" in pid
    assert "f$cc_turn_donk_parent_flop_xc Return 1 Force" in pid
    assert "f$cc_turn_donk_parent_flop_donk_raise_call Return 2 Force" in pid


def opportunity_contract() -> None:
    opp = block("f$cc_turn_donk_opportunity")
    for token in (
        "!IsTurn Return false Force",
        "!f$cc_context_valid Return false Force",
        "balance <= 0 Return false Force",
        "!f$cc_turn_donk_first_hero_action Return false Force",
        "AmountToCall > 0 Return false Force",
        "f$cc_relpos_id = 3 Return false Force",
        "f$cc_hu && !f$cc_hu_oop Return false Force",
        "!f$cc_turn_donk_parent_exclusive Return false Force",
        "f$cc_turn_donk_parent_id <= 0 Return false Force",
        "f$cc_turn_donk_hero_owned_final_flop_aggression Return false Force",
    ):
        assert token in opp

    first = block("f$cc_turn_donk_first_hero_action")
    assert "BotsActionsOnThisRoundIncludingChecks = 0" in first


def ownership_separator_contract() -> None:
    cont = block("f$cc_turn_donk_excluded_flop_donk_standard_continuation")
    assert "f$cc_hist_flop_donk_standard_called_parent" in cont

    cbet = block("f$cc_turn_donk_excluded_standard_cbet")
    assert "f$cc_hist_turn_standard_cbet_parent" in cbet

    flt = block("f$cc_turn_donk_excluded_standard_flop_float")
    assert "f$cc_hist_flop_float_standard_parent_valid" in flt

    gap = block("f$cc_turn_donk_xc_source_substate_needs_review")
    assert "f$cc_turn_donk_parent_flop_xc" in gap
    assert "f$cc_hist_flop_donk_family_id = 1" in gap


def no_strategy_leak_contract() -> None:
    executable = "\n".join(line.split("//", 1)[0] for line in HIST.splitlines())
    for forbidden in (
        "BetHalfPot", "BetThreeFourthPot", "BetPot", "BetMax",
        "RaiseBy", "user_Turn25", "user_Turn50", "user_Turn75", "user_Turn100",
        "HandPower", "random",
    ):
        assert forbidden.lower() not in executable.lower(), f"strategy leaked into Gate08A: {forbidden}"


if __name__ == "__main__":
    aggressor_contract()
    xc_parent_contract()
    bc_parent_contract()
    opportunity_contract()
    ownership_separator_contract()
    no_strategy_leak_contract()
    print("PASS: Gate08A Turn Donk ownership/history contract")
