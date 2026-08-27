#!/usr/bin/env python3
"""Gate08C.4 BBvBTN Turn Donk source/provenance contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_Donk_BBVBTN.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_Donk.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def ancestry_contract() -> None:
    direct = block(POL, "f$cc_turn_donk_bbvbtn_threehanded_context")
    for token in (
        "f$cc_turn_donk_parent_id = 1",
        "f$cc_hist_flop_donk_family_id = 3",
        "f$cc_deal_size = 3",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_oop",
        "f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = 4",
        "f$cc_turn_donk_flop_aggressor_pos_id = 4",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = 4",
        "f$cc_pf_call_bb",
    ):
        assert token in direct

    six = block(POL, "f$cc_turn_donk_bbvbtn_sixmax_descendant_context")
    assert "f$cc_deal_size >= 4 && f$cc_deal_size <= 6" in six
    assert "f$cc_hero_pos_id = 6" in six
    assert "f$cc_hu_villain_pos_id = 4" in six

    origin = block(POL, "f$cc_turn_donk_bbvbtn_origin_id")
    assert "Return 1 Force" in origin
    assert "Return 2 Force" in origin


def tp_defense_contract() -> None:
    snap = block(POL, "f$cc_turn_donk_bbvbtn_flop_tp_snapshot")
    assert "user_cc_flop_donk_state_had_top_pair" in snap
    assert "state_had_overpair" not in snap
    assert "state_had_2pplus" not in snap

    proof = block(POL, "f$cc_turn_donk_bbvbtn_tp_xc_defense_proven")
    assert "user_cc_flop_bbvbtn_source_tp_xc_eligible" in proof

    le = block(POL, "f$cc_turn_donk_bbvbtn_tp_xc_price_le50")
    gt = block(POL, "f$cc_turn_donk_bbvbtn_tp_xc_price_gt50")
    assert "user_cc_flop_bbvbtn_source_tp_xc_called_le50" in le
    assert "user_cc_flop_bbvbtn_source_tp_xc_called_gt50" in gt

    count = block(POL, "f$cc_turn_donk_bbvbtn_tp_xc_price_marker_count")
    assert "f$cc_turn_donk_bbvbtn_tp_xc_price_le50" in count
    assert "f$cc_turn_donk_bbvbtn_tp_xc_price_gt50" in count


def q9_contract() -> None:
    q9 = block(POL, "f$cc_turn_donk_bbvbtn_q9_tripsplus_context")
    assert "f$cc_turn_pairs_flop_rank" in q9
    assert "HaveTrips || HaveFullHouse || HaveQuads" in q9
    assert "HaveTwoPair" not in q9

    assert "f$cc_turn_completed" in block(POL, "f$cc_turn_donk_bbvbtn_q9_completed_action")
    assert "!f$cc_turn_completed" in block(POL, "f$cc_turn_donk_bbvbtn_q9_noncompleted_action")

    size = block(POL, "f$cc_turn_donk_bbvbtn_q9_size_id")
    assert "f$cc_turn_donk_size_75_id" in size
    assert "f$cc_turn_donk_size_50_id" in size


def q8_fourcard_contract() -> None:
    cs = block(POL, "f$cc_turn_donk_bbvbtn_q8_4cs_action")
    assert "nstraightcommon >= 4" in cs
    assert "HaveStraight" in cs
    assert "f$cc_turn_donk_size_50_id" in block(POL, "f$cc_turn_donk_bbvbtn_q8_4cs_size_id")

    cf = block(POL, "f$cc_turn_donk_bbvbtn_q8_4cf_onecard_flush")
    assert "nsuitedcommon >= 4" in cf
    assert "HaveFlush" in cf

    kh = block(POL, "f$cc_turn_donk_bbvbtn_q8_4cf_khigh_plus")
    assert "NumberOfUnknownSuitedOvercards <= 1" in kh
    qh = block(POL, "f$cc_turn_donk_bbvbtn_q8_4cf_qhigh_or_worse")
    assert "NumberOfUnknownSuitedOvercards > 1" in qh

    ka = block(POL, "f$cc_turn_donk_bbvbtn_q8_4cf_khigh_action")
    assert "!f$cc_turn_donk_bbvbtn_q8_4cs_action" in ka
    assert "f$cc_turn_donk_size_50_id" in block(POL, "f$cc_turn_donk_bbvbtn_q8_4cf_khigh_size_id")

    qcheck = block(POL, "f$cc_turn_donk_bbvbtn_q8_4cf_qhigh_check")
    assert "!f$cc_turn_donk_bbvbtn_q8_4cs_action" in qcheck


def q8_oc_uc_contract() -> None:
    other = block(POL, "f$cc_turn_donk_bbvbtn_q8_other_made_draw")
    assert "HaveStraight || HaveFlush" in other
    assert "!f$cc_turn_donk_bbvbtn_q8_4cs_action" in other
    assert "!f$cc_turn_donk_bbvbtn_q8_4cf_onecard_flush" in other

    oc = block(POL, "f$cc_turn_donk_bbvbtn_q8_other_oc_check")
    assert "f$cc_turn_overcard_to_flop" in oc

    gt = block(POL, "f$cc_turn_donk_bbvbtn_q8_other_uc_gt50_check")
    assert "f$cc_turn_undercard" in gt
    assert "f$cc_turn_donk_bbvbtn_tp_xc_price_gt50" in gt
    assert "f$cc_turn_donk_bbvbtn_tp_xc_price_marker_count = 1" in gt

    le = block(POL, "f$cc_turn_donk_bbvbtn_q8_other_uc_le50_action")
    assert "f$cc_turn_undercard" in le
    assert "f$cc_turn_donk_bbvbtn_tp_xc_price_le50" in le
    assert "f$cc_turn_donk_bbvbtn_tp_xc_price_marker_count = 1" in le

    # Positive UC size is A from mature implementation, not a source-invented jam.
    sz = block(POL, "f$cc_turn_donk_bbvbtn_q8_other_uc_size_id")
    assert "f$cc_turn_donk_size_50_id" in sz

    need = block(POL, "f$cc_turn_donk_bbvbtn_q8_other_uc_needs_price_provenance")
    assert "f$cc_turn_donk_bbvbtn_tp_xc_price_marker_count != 1" in need

    neutral = block(POL, "f$cc_turn_donk_bbvbtn_q8_neutral_runout_source_gap")
    assert "!f$cc_turn_overcard_to_flop" in neutral
    assert "!f$cc_turn_undercard" in neutral


def source_gap_and_draw_contract() -> None:
    gap = block(POL, "f$cc_turn_donk_bbvbtn_residual_2pplus_mature_only_gap")
    assert "f$cc_hand_two_pair_or_better" in gap
    assert "!HaveStraight" in gap
    assert "!HaveFlush" in gap

    drawproof = block(POL, "f$cc_turn_donk_bbvbtn_draw_xc_defense_proven")
    assert "user_cc_flop_bbvbtn_source_nonbest_draw_xc_eligible" in drawproof

    drawctx = block(POL, "f$cc_turn_donk_bbvbtn_draw_xc_context")
    assert "user_cc_flop_donk_state_had_no_made" in drawctx
    assert "f$cc_turn_donk_bbvbtn_draw_xc_defense_proven" in drawctx

    missed = block(POL, "f$cc_turn_donk_bbvbtn_missed_draw_check")
    assert "f$cc_hand_no_made" in missed

    completed = block(POL, "f$cc_turn_donk_bbvbtn_completed_nomade_draw_source_gap")
    assert "!f$cc_hand_no_made" in completed


def router_coverage_safety_contract() -> None:
    action = block(POL, "f$cc_turn_donk_bbvbtn_action")
    assert "f$cc_turn_donk_bbvbtn_q9_completed_action Return true Force" in action
    assert "f$cc_turn_donk_bbvbtn_q8_4cs_action Return true Force" in action
    assert "f$cc_turn_donk_bbvbtn_q8_4cf_khigh_action Return true Force" in action
    assert "f$cc_turn_donk_bbvbtn_q8_4cf_qhigh_check Return false Force" in action
    assert "f$cc_turn_donk_bbvbtn_q8_other_oc_check Return false Force" in action
    assert "f$cc_turn_donk_bbvbtn_q8_other_uc_gt50_check Return false Force" in action
    assert "f$cc_turn_donk_bbvbtn_q8_other_uc_le50_action Return true Force" in action
    assert "f$cc_turn_donk_bbvbtn_missed_draw_check Return false Force" in action

    covered = block(POL, "f$cc_turn_donk_bbvbtn_tp_source_decision_covered")
    assert "f$cc_turn_donk_bbvbtn_residual_2pplus_mature_only_gap Return false Force" in covered
    assert "f$cc_turn_donk_bbvbtn_q8_other_uc_needs_price_provenance Return false Force" in covered
    assert "f$cc_turn_donk_bbvbtn_q8_neutral_runout_source_gap Return false Force" in covered

    family = block(ROUTER, "f$cc_turn_donk_family_id")
    assert "f$cc_turn_donk_bbvbtn_covered Return 5 Force" in family
    r = block(ROUTER, "f$cc_turn_donk_router")
    assert "f$cc_turn_donk_bbvbtn_covered Return f$cc_turn_donk_bbvbtn_action Force" in r
    s = block(ROUTER, "f$cc_turn_donk_size_id")
    assert "f$cc_turn_donk_bbvbtn_covered Return f$cc_turn_donk_bbvbtn_size_id Force" in s

    code = executable(POL)
    for forbidden in (
        "f$game_3wBBvBTN",
        "HandPower",
        "random",
        "BetMax",
        "Raise_Committed",
        "StackOff",
        "River50Plan",
        "user_River",
        "f$EffectiveStack",
        "f$cc_spr_round_start",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden BBvBTN executable leak: {forbidden}"


if __name__ == "__main__":
    ancestry_contract()
    tp_defense_contract()
    q9_contract()
    q8_fourcard_contract()
    q8_oc_uc_contract()
    source_gap_and_draw_contract()
    router_coverage_safety_contract()
    print("PASS: Gate08C.4 BBvBTN Turn Donk source/provenance contract")
