#!/usr/bin/env python3
"""Gate06C deterministic ordinary-SRP River Float gap contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
POL = (SRC / "CashCrusher_River_Float_SRP_Gaps.txt").read_text(encoding="utf-8")
SRC_POL = (SRC / "CashCrusher_River_Float_Source.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def topology_contract() -> None:
    ctx = block(POL, "f$cc_river_float_srp_context")
    for token in (
        "f$cc_river_float_opportunity",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller || f$cc_pf_role_pfa",
    ):
        assert token in ctx

    caller = block(POL, "f$cc_river_float_srp_clean_hu_caller_vs_pfa")
    for token in (
        "f$cc_river_float_current_hu_from_hu_flop",
        "f$cc_pf_role_srp_caller",
        "f$cc_river_float_hu_aggressor_is_current_villain",
        "f$cc_pf_rt_final_aggressor_pos_id = f$cc_river_float_turn_aggressor_pos_id",
    ):
        assert token in caller

    pfa = block(POL, "f$cc_river_float_srp_clean_hu_pfa_lost_initiative")
    assert "f$cc_pf_role_pfa" in pfa
    assert "f$cc_river_float_hu_aggressor_is_current_villain" in pfa

    postmw = block(POL, "f$cc_river_float_srp_threeway_origin_now_hu_unresolved")
    assert "f$cc_river_float_hu_multiway_origin_unresolved" in postmw
    assert "f$cc_flop_entry_count = 3" in postmw

    fourplus = block(POL, "f$cc_river_float_srp_fourplus_origin")
    assert "f$cc_flop_entry_count >= 4" in fourplus

    tid = block(POL, "f$cc_river_float_srp_gap_topology_id")
    assert "f$cc_river_float_srp_fourplus_origin Return 5 Force" in tid
    assert "f$cc_river_float_srp_threeway_origin_now_hu_unresolved Return 4 Force" in tid
    assert "f$cc_river_float_srp_current_threeway Return 3 Force" in tid
    assert "f$cc_river_float_srp_clean_hu_caller_vs_pfa Return 1 Force" in tid
    assert "f$cc_river_float_srp_clean_hu_pfa_lost_initiative Return 2 Force" in tid


def provenance_gap_contract() -> None:
    nomade = block(POL, "f$cc_river_float_srp_nomade_snapshot_missing")
    assert "f$cc_river_no_made" in nomade
    assert "!f$cc_river_float_source_bbv_sb_exact_parent_ready" in nomade

    sdv = block(POL, "f$cc_river_float_srp_weak_showdown_value")
    assert "f$cc_number_better_kickers > 4" in sdv
    assert "f$cc_river_second_pair" in sdv
    assert "f$cc_river_third_or_worse_pair" in sdv

    code = executable(POL)
    # No generic busted-draw bluff is allowed before defensive turn-call snapshot.
    assert "user_cc_river_float_turn_call_had_real_draw" not in code
    assert "f$cc_river_no_made Return true Force" not in code


def fourplus_value_contract() -> None:
    robust = block(POL, "f$cc_river_float_srp_fourplus_robust_value")
    for token in (
        "!f$cc_river_float_srp_fourplus_origin Return false Force",
        "f$cc_river_float_source_literal_nuts Return true Force",
        "f$cc_river_four_card_completion && (HaveFullHouse || HaveQuads || HaveStraightFlush) Return true Force",
        "f$cc_river_four_card_completion Return false Force",
        "f$cc_river_completed && f$cc_river_straight_or_better Return true Force",
        "f$cc_river_completed Return false Force",
        "f$cc_river_two_pair_plus Return true Force",
    ):
        assert token in robust

    size = block(POL, "f$cc_river_float_srp_fourplus_size_id")
    assert "f$cc_river_float_source_literal_nuts Return f$cc_river_size_75_id Force" in size
    assert "When Others Return f$cc_river_size_50_id Force" in size

    # Source generic value may not claim four-plus flop origins/current fields.
    domain = block(SRC_POL, "f$cc_river_float_source_general_domain_supported")
    assert "f$cc_flop_entry_count <= 3" in domain
    assert "nplayersplaying <= 3" in domain


def gap_router_contract() -> None:
    covered = block(POL, "f$cc_river_float_srp_gap_covered")
    assert "!f$cc_river_float_source_covered" in covered
    assert "f$cc_river_float_srp_gap_topology_id > 0" in covered

    action = block(POL, "f$cc_river_float_srp_gap_action")
    assert "!f$cc_river_float_srp_gap_covered Return false Force" in action
    assert "f$cc_river_float_srp_fourplus_robust_value Return true Force" in action
    assert "When Others Return false Force" in action

    reviewed_check = block(POL, "f$cc_river_float_srp_reviewed_check")
    assert "f$cc_river_float_srp_gap_covered && !f$cc_river_float_srp_gap_action" in reviewed_check

    consistency = block(POL, "f$cc_river_float_srp_gap_size_consistent")
    assert "f$cc_river_float_srp_gap_size_id = 0" in consistency
    assert "f$cc_river_float_srp_gap_size_id >= 1 && f$cc_river_float_srp_gap_size_id <= 5" in consistency


def safety_contract() -> None:
    code = executable(POL)
    for forbidden in (
        "HandPower",
        "random",
        "BetMax",
        "Raise_Committed",
        "StackOffDraws",
        "allin_on_betsize_balance_ratio",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden executable SRP-gap leak: {forbidden}"


if __name__ == "__main__":
    topology_contract()
    provenance_gap_contract()
    fourplus_value_contract()
    gap_router_contract()
    safety_contract()
    print("PASS: Gate06C ordinary-SRP River Float gap contract")