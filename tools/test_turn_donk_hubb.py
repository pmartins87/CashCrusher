#!/usr/bin/env python3
"""Gate08C.1 HUBB Turn Donk source/provenance contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUBB = (ROOT / "src" / "CashCrusher_Turn_Donk_HUBB.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_Donk.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_Turn_Donk_Common.txt").read_text(encoding="utf-8")


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
    true_srp = block(HUBB, "f$cc_turn_donk_hubb_truehu_srp_context")
    for token in (
        "f$cc_turn_donk_parent_id = 1",
        "f$cc_hist_flop_donk_family_id = 3",
        "f$cc_true_hu",
        "f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = 5",
        "f$cc_turn_donk_flop_aggressor_pos_id = 5",
        "f$cc_pf_single_raiser_pos_id = 5",
    ):
        assert token in true_srp

    limped = block(HUBB, "f$cc_turn_donk_hubb_truehu_limped_context")
    assert "f$cc_pot_family_id = 1" in limped
    assert "f$cc_pf_role_bb_check" in limped
    assert "f$cc_pf_call_sb" in limped

    reduced = block(HUBB, "f$cc_turn_donk_hubb_reducedhu_bvb_srp_context")
    assert "f$cc_hu_origin_preflop_reduced" in reduced
    assert "f$cc_hero_pos_id = 6" in reduced
    assert "f$cc_hu_villain_pos_id = 5" in reduced
    assert "f$cc_pf_one_raise_ordinary_srp" in reduced

    origin = block(HUBB, "f$cc_turn_donk_hubb_origin_id")
    assert "Return 1 Force" in origin
    assert "Return 2 Force" in origin
    assert "Return 3 Force" in origin


def hand_class_contract() -> None:
    strong = block(HUBB, "f$cc_turn_donk_hubb_strong_made")
    assert "f$cc_turn_donk_hubb_top_pair_real" in strong
    assert "f$cc_turn_donk_hubb_overpair_real" in strong
    assert "f$cc_turn_donk_hubb_two_pair_plus_real" in strong

    real2p = block(HUBB, "f$cc_turn_donk_hubb_two_pair_plus_real")
    assert "pokerval > pokervalcommon" in real2p
    assert "npcbits > 0" in real2p
    assert "!TwoPairOnBoard" in real2p

    good = block(HUBB, "f$cc_turn_donk_hubb_good_draw")
    assert "f$cc_real_oesd" in good
    assert "f$cc_real_fd" in good
    assert "f$cc_real_gutshot" in good
    assert "f$cc_turn_donk_hubb_two_meaningful_overcards" in good

    weak = block(HUBB, "f$cc_turn_donk_hubb_weak_gs")
    assert "f$cc_real_gutshot" in weak
    assert "!f$cc_turn_donk_hubb_good_draw" in weak

    air = block(HUBB, "f$cc_turn_donk_hubb_air")
    assert "f$cc_hand_no_made" in air
    assert "!f$cc_real_oesd" in air
    assert "!f$cc_real_fd" in air
    assert "!f$cc_real_gutshot" in air


def tp_draw_air_contract() -> None:
    exploit = block(HUBB, "f$cc_turn_donk_hubb_low_turn_cbet_exploit")
    assert "pt_hands_headsupchair > 100" in exploit
    assert "pt_turn_cbet_headsupchair > 0" in exploit
    assert "pt_turn_cbet_headsupchair <= 0.45" in exploit

    strong_action = block(HUBB, "f$cc_turn_donk_hubb_strongmade_action")
    assert "f$cc_turn_donk_hubb_low_turn_cbet_exploit" in strong_action
    assert "f$cc_turn_donk_hubb_strong_made" in strong_action
    assert "f$cc_turn_donk_size_75_id" in block(HUBB, "f$cc_turn_donk_hubb_strongmade_size_id")

    assert "f$cc_turn_donk_hubb_good_draw" in block(HUBB, "f$cc_turn_donk_hubb_gooddraw_check")
    assert "f$cc_turn_donk_size_25_id" in block(HUBB, "f$cc_turn_donk_hubb_weakgs_size_id")
    assert "f$cc_turn_donk_size_25_id" in block(HUBB, "f$cc_turn_donk_hubb_air_size_id")

    dispatch = block(HUBB, "f$cc_turn_donk_hubb_action")
    assert "When f$cc_turn_donk_hubb_good_draw Return false Force" in dispatch
    assert "When f$cc_turn_donk_hubb_weak_gs Return true Force" in dispatch
    assert "When f$cc_turn_donk_hubb_air Return true Force" in dispatch


def mpbp_contract() -> None:
    flop_pair = block(HUBB, "f$cc_turn_donk_hubb_flop_second_or_third_pair_source")
    assert "f$cc_turn_donk_hubb_flop_second_pair_source" in flop_pair
    assert "f$cc_turn_donk_hubb_flop_third_pair_source" in flop_pair

    gt = block(HUBB, "f$cc_turn_donk_hubb_flop_call_gt50_proven")
    le = block(HUBB, "f$cc_turn_donk_hubb_flop_call_le50_proven")
    assert "user_cc_flop_donk_hubb_called_gt50" in gt
    assert "user_cc_flop_donk_hubb_called_le50" in le

    sensitive = block(HUBB, "f$cc_turn_donk_hubb_mpbp_price_sensitive_state")
    assert "f$cc_turn_donk_hubb_flop_second_or_third_pair_source" in sensitive
    assert "f$cc_turn_donk_hubb_current_second_or_third_pair" in sensitive
    assert "!f$cc_real_frontdoor_draw" in sensitive

    needs = block(HUBB, "f$cc_turn_donk_hubb_mpbp_needs_flop_price_provenance")
    assert "f$cc_turn_donk_hubb_flop_call_price_marker_count != 1" in needs

    big = block(HUBB, "f$cc_turn_donk_hubb_bigcbet_mpbp_action")
    assert "!f$cc_turn_completed" in big
    assert "f$cc_turn_donk_size_min_id" in block(HUBB, "f$cc_turn_donk_hubb_bigcbet_mpbp_size_id")

    general = block(HUBB, "f$cc_turn_donk_hubb_general_mpbp_action")
    for token in (
        "f$cc_number_better_kickers <= 2",
        "!PairOnBoard",
        "f$cc_flop_2bw",
        "StraightPossibleOnTurn",
        "f$cc_turn_undercard",
    ):
        assert token in general
    assert "f$cc_turn_donk_size_25_id" in block(HUBB, "f$cc_turn_donk_hubb_general_mpbp_size_id")

    assert "f$cc_real_frontdoor_draw" in block(HUBB, "f$cc_turn_donk_hubb_pair_plus_draw")
    assert "When f$cc_turn_donk_hubb_pair_plus_draw Return false Force" in block(
        HUBB, "f$cc_turn_donk_hubb_action"
    )


def router_and_safety_contract() -> None:
    assert "##f$cc_turn_donk_size_min_id##" in COMMON
    assert "\n5\n" in COMMON

    family = block(ROUTER, "f$cc_turn_donk_family_id")
    assert "f$cc_turn_donk_hubb_covered Return 2 Force" in family
    router = block(ROUTER, "f$cc_turn_donk_router")
    assert "f$cc_turn_donk_hubb_covered Return f$cc_turn_donk_hubb_action Force" in router
    size = block(ROUTER, "f$cc_turn_donk_size_id")
    assert "f$cc_turn_donk_hubb_covered Return f$cc_turn_donk_hubb_size_id Force" in size
    covered = block(ROUTER, "f$cc_turn_donk_strategy_covered")
    assert "f$cc_turn_donk_hubb_covered" in covered

    code = executable(HUBB)
    for forbidden in (
        "f$game_HUBB",
        "HandPower",
        "random",
        "BetMax",
        "Raise_Committed",
        "StackOff",
        "f$EffectiveStack",
        "f$cc_spr_round_start",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden HUBB executable leak: {forbidden}"

    # No Turn policy is allowed to directly schedule River actions.
    assert "user_River" not in code


if __name__ == "__main__":
    ancestry_contract()
    hand_class_contract()
    tp_draw_air_contract()
    mpbp_contract()
    router_and_safety_contract()
    print("PASS: Gate08C.1 HUBB Turn Donk source/provenance contract")
