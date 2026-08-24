#!/usr/bin/env python3
"""Gate08C.2 SBvBTN Turn Donk source/provenance contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_Donk_SBVBTN.txt").read_text(encoding="utf-8")
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
    src = block(POL, "f$cc_turn_donk_sbvbtn_threehanded_context")
    for token in (
        "f$cc_turn_donk_parent_id = 1",
        "f$cc_hist_flop_donk_family_id = 3",
        "f$cc_deal_size = 3",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_hero_pos_id = 5",
        "f$cc_hu_villain_pos_id = 4",
        "f$cc_turn_donk_flop_aggressor_pos_id = 4",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = 4",
    ):
        assert token in src

    six = block(POL, "f$cc_turn_donk_sbvbtn_sixmax_descendant_context")
    assert "f$cc_deal_size >= 4 && f$cc_deal_size <= 6" in six
    assert "f$cc_hu_origin_preflop_reduced" in six
    assert "f$cc_hero_pos_id = 5" in six
    assert "f$cc_hu_villain_pos_id = 4" in six

    origin = block(POL, "f$cc_turn_donk_sbvbtn_origin_id")
    assert "Return 1 Force" in origin
    assert "Return 2 Force" in origin


def axx_tp_contract() -> None:
    snap = block(POL, "f$cc_turn_donk_sbvbtn_flop_tpplus_snapshot")
    assert "user_cc_flop_donk_state_had_top_pair" in snap
    assert "user_cc_flop_donk_state_had_overpair" in snap
    assert "user_cc_flop_donk_state_had_2pplus" in snap

    ctx = block(POL, "f$cc_turn_donk_sbvbtn_axx_tpplus_context")
    assert "AcePresentOnFlop" in ctx
    assert "f$cc_turn_donk_sbvbtn_flop_tpplus_snapshot" in ctx

    assert "f$cc_turn_donk_sbvbtn_axx_tpplus_context" in block(
        POL, "f$cc_turn_donk_sbvbtn_axx_tpplus_action"
    )
    assert "f$cc_turn_donk_size_100_id" in block(
        POL, "f$cc_turn_donk_sbvbtn_axx_tpplus_size_id"
    )

    nonaxx = block(POL, "f$cc_turn_donk_sbvbtn_nonaxx_tpplus_check")
    assert "!AcePresentOnFlop" in nonaxx


def mpbp_contract() -> None:
    mp = block(POL, "f$cc_turn_donk_sbvbtn_mpbp_check")
    assert "user_cc_flop_donk_state_had_lower_pair" in mp

    action = block(POL, "f$cc_turn_donk_sbvbtn_action")
    assert "When f$cc_turn_donk_sbvbtn_mpbp_check Return false Force" in action


def defense_provenance_contract() -> None:
    draw = block(POL, "f$cc_turn_donk_sbvbtn_draw_xc_defense_proven")
    high = block(POL, "f$cc_turn_donk_sbvbtn_highair_xc_defense_proven")
    assert "user_cc_flop_donk_sbvbtn_source_draw_xc_eligible" in draw
    assert "user_cc_flop_donk_sbvbtn_source_highair_called_le33" in high

    count = block(POL, "f$cc_turn_donk_sbvbtn_nomade_source_marker_count")
    assert "f$cc_turn_donk_sbvbtn_draw_xc_defense_proven" in count
    assert "f$cc_turn_donk_sbvbtn_highair_xc_defense_proven" in count

    need = block(POL, "f$cc_turn_donk_sbvbtn_nomade_needs_defense_provenance")
    assert "user_cc_flop_donk_state_had_no_made" in need
    assert "f$cc_turn_donk_sbvbtn_nomade_source_marker_count != 1" in need

    for name in (
        "f$cc_turn_donk_sbvbtn_draw_xc_context",
        "f$cc_turn_donk_sbvbtn_highair_xc_context",
    ):
        b = block(POL, name)
        assert "user_cc_flop_donk_state_had_no_made" in b
        assert "f$cc_turn_donk_sbvbtn_nomade_source_marker_count = 1" in b


def draw_contract() -> None:
    improve = block(POL, "f$cc_turn_donk_sbvbtn_draw_improved_undercard")
    assert "f$cc_turn_undercard" in improve
    assert "f$cc_hand_pair_or_better" in improve

    action = block(POL, "f$cc_turn_donk_sbvbtn_draw_action")
    assert "f$cc_turn_donk_sbvbtn_draw_improved_undercard" in action

    size = block(POL, "f$cc_turn_donk_sbvbtn_draw_size_id")
    assert "f$cc_turn_donk_size_75_id" in size

    check = block(POL, "f$cc_turn_donk_sbvbtn_draw_check")
    assert "!f$cc_turn_donk_sbvbtn_draw_improved_undercard" in check


def highair_contract() -> None:
    pickup = block(POL, "f$cc_turn_donk_sbvbtn_highair_2hc_draw_pickup")
    assert "!f$cc_hand_no_made Return false Force" in pickup
    assert "HaveStraightDraw && (nstraightfillcommon - nstraightfill = 2)" in pickup
    assert "HaveFlushDraw && SuitsInHand = 1" in pickup

    action = block(POL, "f$cc_turn_donk_sbvbtn_highair_action")
    assert "f$cc_turn_donk_sbvbtn_highair_2hc_draw_pickup" in action
    assert "f$cc_turn_donk_size_50_id" in block(
        POL, "f$cc_turn_donk_sbvbtn_highair_size_id"
    )

    gap = block(POL, "f$cc_turn_donk_sbvbtn_highair_made_improvement_source_gap")
    assert "!f$cc_hand_no_made" in gap
    assert "f$cc_hand_pair_or_better" in gap

    covered = block(POL, "f$cc_turn_donk_sbvbtn_covered")
    assert "!f$cc_turn_donk_sbvbtn_highair_made_improvement_source_gap" in covered


def router_and_safety_contract() -> None:
    action = block(POL, "f$cc_turn_donk_sbvbtn_action")
    assert "When f$cc_turn_donk_sbvbtn_axx_tpplus_context Return true Force" in action
    assert "When f$cc_turn_donk_sbvbtn_nonaxx_tpplus_check Return false Force" in action
    assert "When f$cc_turn_donk_sbvbtn_draw_xc_context Return f$cc_turn_donk_sbvbtn_draw_action Force" in action
    assert "When f$cc_turn_donk_sbvbtn_highair_xc_context Return f$cc_turn_donk_sbvbtn_highair_action Force" in action

    family = block(ROUTER, "f$cc_turn_donk_family_id")
    assert "f$cc_turn_donk_sbvbtn_covered Return 3 Force" in family
    router = block(ROUTER, "f$cc_turn_donk_router")
    assert "f$cc_turn_donk_sbvbtn_covered Return f$cc_turn_donk_sbvbtn_action Force" in router
    size = block(ROUTER, "f$cc_turn_donk_size_id")
    assert "f$cc_turn_donk_sbvbtn_covered Return f$cc_turn_donk_sbvbtn_size_id Force" in size
    covered = block(ROUTER, "f$cc_turn_donk_strategy_covered")
    assert "f$cc_turn_donk_sbvbtn_covered" in covered

    code = executable(POL)
    for forbidden in (
        "f$game_3wSBvBTN",
        "HandPower",
        "random",
        "BetMax",
        "Raise_Committed",
        "StackOff",
        "f$EffectiveStack",
        "f$cc_spr_round_start",
        "user_River",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden SBvBTN executable leak: {forbidden}"


if __name__ == "__main__":
    ancestry_contract()
    axx_tp_contract()
    mpbp_contract()
    defense_provenance_contract()
    draw_contract()
    highair_contract()
    router_and_safety_contract()
    print("PASS: Gate08C.2 SBvBTN Turn Donk source/provenance contract")
