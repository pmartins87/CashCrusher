#!/usr/bin/env python3
"""Gate05A static contract tests for Turn Float history ownership."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HIST = (SRC / "CashCrusher_Turn_Float_History.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def run_flop_aggressor_contract() -> None:
    valid = block(HIST, "f$cc_turn_float_flop_aggressor_history_valid")
    assert "raisbits2 >> lastraised2" in valid

    pos = block(HIST, "f$cc_turn_float_flop_aggressor_pos_id")
    assert "f$cc_deal_size >= 3 && lastraised2 = dealerchair Return 4 Force" in pos
    assert "lastraised2 = smallblindchair Return 5 Force" in pos

    live = block(HIST, "f$cc_turn_float_flop_aggressor_live_opponent")
    assert "lastraised2 = userchair Return false Force" in live
    assert "playersplayingbits >> lastraised2" in live

    single = block(HIST, "f$cc_turn_float_single_flop_aggressor")
    assert "BitCount(raisbits2) = 1" in single


def run_parent_contract() -> None:
    pf3 = block(HIST, "f$cc_turn_float_pf_threebet_caller_supported")
    assert "f$cc_pf_rt_3bet_order_supported" in pf3
    assert "f$cc_pf_rt_hero_3bet_origin_consistent" in pf3
    assert "f$cc_pf_role_cold_call_3bet" in pf3

    ordinary = block(HIST, "f$cc_turn_float_parent_called_pf_aggressor")
    for token in (
        "f$cc_turn_float_flop_call_only",
        "f$cc_turn_float_single_flop_aggressor",
        "f$cc_turn_float_flop_aggressor_live_opponent",
        "f$cc_turn_float_flop_aggressor_pos_id = f$cc_pf_rt_final_aggressor_pos_id",
    ):
        assert token in ordinary

    cbet_xr = block(HIST, "f$cc_turn_float_parent_cbet_xr_call")
    assert "f$cc_hist_flop_cbet_then_called_raise" in cbet_xr
    assert "!f$cc_hist_flop_cbet_then_reaggressed" in cbet_xr
    assert "f$cc_turn_float_flop_aggressor_live_opponent" in cbet_xr

    float_xr = block(HIST, "f$cc_turn_float_parent_flopfloat_xr_call")
    assert "f$cc_hist_flop_float_then_called_raise" in float_xr
    assert "!f$cc_hist_flop_float_then_reaggressed" in float_xr

    parent_id = block(HIST, "f$cc_turn_float_parent_id")
    assert "f$cc_turn_float_parent_count != 1 Return 0 Force" in parent_id
    assert "Return 1 Force" in parent_id
    assert "Return 2 Force" in parent_id
    assert "Return 3 Force" in parent_id


def run_turn_opportunity_contract() -> None:
    first = block(HIST, "f$cc_turn_float_first_hero_action")
    assert "BotsActionsOnThisRoundIncludingChecks = 0" in first

    opp = block(HIST, "f$cc_turn_float_opportunity")
    for token in (
        "!f$cc_context_valid Return false Force",
        "balance <= 0 Return false Force",
        "AmountToCall > 0 Return false Force",
        "f$cc_relpos_id != 3 Return false Force",
        "f$cc_hu && !f$cc_hu_ip Return false Force",
        "f$cc_turn_float_parent_id <= 0 Return false Force",
    ):
        assert token in opp
    assert "When Others Return true Force" in opp

    hu_identity = block(HIST, "f$cc_turn_float_hu_aggressor_is_current_villain")
    assert "lastraised2 = headsupchair Return true Force" in hu_identity


def run_ownership_exclusion_contract() -> None:
    exclusions = {
        "f$cc_turn_float_excluded_flop_float_standard": "f$cc_hist_flop_float_standard_parent_valid",
        "f$cc_turn_float_excluded_flop_float_checkback": "f$cc_hist_flop_float_checkback_parent_valid",
        "f$cc_turn_float_excluded_standard_cbet": "f$cc_hist_turn_standard_cbet_parent",
        "f$cc_turn_float_excluded_delayed_cbet": "f$cc_hist_turn_delayed_cbet_parent",
    }
    for name, token in exclusions.items():
        assert token in block(HIST, name)

    # Gate05A is context/history only. It must not issue a betting action.
    code = executable(HIST)
    for action in ("BetMax", "BetHalfPot", "BetThirdPot", "BetThreeFourthPot", "BetPot", "RaiseBy"):
        assert action not in code


if __name__ == "__main__":
    run_flop_aggressor_contract()
    run_parent_contract()
    run_turn_opportunity_contract()
    run_ownership_exclusion_contract()
    print("PASS: Gate05A Turn Float history/opportunity contract")
