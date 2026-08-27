#!/usr/bin/env python3
"""Gate06A deterministic River Float history/source-ownership contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HIST = (SRC / "CashCrusher_River_Float_History.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def ownership_correction_contract() -> None:
    alias = block(HIST, "f$cc_river_after_turn_float_standard_parent_valid")
    assert "f$cc_hist_river_float_standard_parent_valid" in alias

    excluded = block(HIST, "f$cc_river_float_excluded_executed_turn_float")
    assert "f$cc_river_after_turn_float_standard_parent_valid" in excluded

    parent = block(HIST, "f$cc_river_float_parent_called_turn_aggressor")
    assert "f$cc_river_float_turn_call_only" in parent
    assert "f$cc_river_float_excluded_executed_turn_float" in parent
    assert "f$cc_river_after_turn_float_standard_parent_valid" not in parent


def closed_turn_call_contract() -> None:
    call = block(HIST, "f$cc_river_float_turn_call_only")
    for token in (
        "didcallround3 != 1",
        "didchecround3 != 0",
        "didraisround3 != 0",
        "didbetsizeround3 != 0",
        "didalliround3 != 0",
    ):
        assert token in call

    aggr = block(HIST, "f$cc_river_float_turn_aggressor_history_valid")
    assert "raisbits3 >> lastraised3" in aggr

    single = block(HIST, "f$cc_river_float_single_turn_aggressor")
    assert "BitCount(raisbits3) = 1" in single

    live = block(HIST, "f$cc_river_float_turn_aggressor_live_opponent")
    assert "lastraised3 = userchair Return false Force" in live
    assert "playersplayingbits >> lastraised3" in live


def river_opportunity_contract() -> None:
    first = block(HIST, "f$cc_river_float_first_hero_action")
    assert "BotsActionsOnThisRoundIncludingChecks = 0" in first

    opp = block(HIST, "f$cc_river_float_opportunity")
    for token in (
        "!f$cc_context_valid Return false Force",
        "balance <= 0 Return false Force",
        "AmountToCall > 0 Return false Force",
        "f$cc_relpos_id != 3 Return false Force",
        "f$cc_hu && !f$cc_hu_ip Return false Force",
        "f$cc_river_float_parent_id <= 0 Return false Force",
        "f$cc_river_float_excluded_executed_turn_float Return false Force",
    ):
        assert token in opp
    assert "When Others Return true Force" in opp

    hu_id = block(HIST, "f$cc_river_float_hu_aggressor_is_current_villain")
    assert "lastraised3 = headsupchair Return true Force" in hu_id


def source_blocker_contract() -> None:
    cand = block(HIST, "f$cc_river_float_source_bbv_sb_geometry_candidate")
    for token in (
        "f$cc_river_float_current_hu_from_hu_flop",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_hero_pos_id = 6",
        "f$cc_pf_rt_final_aggressor_pos_id = 5",
        "f$cc_river_float_turn_aggressor_pos_id = 5",
    ):
        assert token in cand

    proof = block(HIST, "f$cc_river_float_source_bbv_sb_turn_draw_call_proven")
    assert "user_cc_river_float_src_bbv_sb_turn_draw_called2bar" in proof

    wait = block(HIST, "f$cc_river_float_source_bbv_sb_waiting_defense_snapshot")
    assert "f$cc_river_float_source_bbv_sb_geometry_candidate" in wait
    assert "!f$cc_river_float_source_bbv_sb_turn_draw_call_proven" in wait

    unresolved = block(HIST, "f$cc_river_float_hu_multiway_origin_unresolved")
    assert "f$cc_flop_entry_count >= 3" in unresolved


def no_strategy_contract() -> None:
    code = executable(HIST)
    for action in (
        "BetMax",
        "BetHalfPot",
        "BetThirdPot",
        "BetThreeFourthPot",
        "BetPot",
        "RaiseBy",
    ):
        assert action not in code, f"Gate06A must be history-only: {action}"


if __name__ == "__main__":
    ownership_correction_contract()
    closed_turn_call_contract()
    river_opportunity_contract()
    source_blocker_contract()
    no_strategy_contract()
    print("PASS: Gate06A River Float history/source-ownership contract")
