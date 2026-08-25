#!/usr/bin/env python3
"""Gate08C.3 SBvBB Turn Donk source/provenance contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_Donk_SBVBB.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_Donk.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_Turn_Donk_History.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def history_repair_contract() -> None:
    clean = block(HIST, "f$cc_turn_donk_clean_flop_xc")
    assert "f$cc_turn_donk_flop_check_call_only" in clean
    assert "f$cc_turn_donk_single_flop_aggressor" in clean
    assert "f$cc_turn_donk_flop_aggressor_live_opponent" in clean
    assert "!f$cc_turn_donk_hero_owned_final_flop_aggression" in clean

    other = block(HIST, "f$cc_turn_donk_parent_other_clean_xc")
    assert "f$cc_turn_donk_clean_flop_xc" in other
    assert "!f$cc_turn_donk_parent_flop_xc" in other

    pid = block(HIST, "f$cc_turn_donk_parent_id")
    assert "f$cc_turn_donk_parent_other_clean_xc Return 3 Force" in pid


def topology_contract() -> None:
    parent = block(POL, "f$cc_turn_donk_sbvbb_xc_parent_proven")
    assert "f$cc_turn_donk_parent_id = 1" in parent
    assert "f$cc_turn_donk_parent_id = 3" in parent
    assert "f$cc_turn_donk_parent_id = 2" not in parent

    common = block(POL, "f$cc_turn_donk_sbvbb_common_context")
    for token in (
        "f$cc_turn_donk_opportunity",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_hu_oop",
        "f$cc_hero_pos_id = 5",
        "f$cc_hu_villain_pos_id = 6",
        "f$cc_turn_donk_hu_aggressor_is_current_villain",
        "f$cc_turn_donk_flop_aggressor_pos_id = 6",
    ):
        assert token in common

    direct = block(POL, "f$cc_turn_donk_sbvbb_threehanded_common")
    assert "f$cc_deal_size = 3" in direct

    six = block(POL, "f$cc_turn_donk_sbvbb_sixmax_common")
    assert "f$cc_deal_size >= 4 && f$cc_deal_size <= 6" in six


def preflop_origin_contract() -> None:
    limp = block(POL, "f$cc_turn_donk_sbvbb_limped_origin")
    for token in (
        "f$cc_pot_family_id = 1",
        "f$cc_pf_raise_count = 0",
        "f$cc_pf_role_unraised_caller",
        "f$cc_pf_call_sb",
    ):
        assert token in limp

    mnr = block(POL, "f$cc_turn_donk_sbvbb_mnr_origin")
    for token in (
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_pfa",
        "f$cc_pf_single_raiser_pos_id = 5",
        "f$cc_pf_call_bb",
    ):
        assert token in mnr

    origin = block(POL, "f$cc_turn_donk_sbvbb_origin_id")
    for i in range(1, 5):
        assert f"Return {i} Force" in origin


def defense_provenance_contract() -> None:
    limp = block(POL, "f$cc_turn_donk_sbvbb_limped_draw_xc_defense_proven")
    med = block(POL, "f$cc_turn_donk_sbvbb_mnr_medium_xc_defense_proven")
    weak = block(POL, "f$cc_turn_donk_sbvbb_mnr_weak_xc_defense_proven")
    assert "user_cc_flop_sbvbb_limped_medweak_draw_called_le50" in limp
    assert "user_cc_flop_sbvbb_mnr_medium_draw_called_le100" in med
    assert "user_cc_flop_sbvbb_mnr_weak_draw_called_le33" in weak

    count = block(POL, "f$cc_turn_donk_sbvbb_draw_xc_marker_count")
    assert "f$cc_turn_donk_sbvbb_limped_draw_xc_defense_proven" in count
    assert "f$cc_turn_donk_sbvbb_mnr_medium_xc_defense_proven" in count
    assert "f$cc_turn_donk_sbvbb_mnr_weak_xc_defense_proven" in count

    proven = block(POL, "f$cc_turn_donk_sbvbb_draw_xc_defense_proven")
    assert "f$cc_turn_donk_sbvbb_draw_xc_marker_count != 1 Return false Force" in proven
    assert "f$cc_turn_donk_sbvbb_limped_origin && f$cc_turn_donk_sbvbb_limped_draw_xc_defense_proven" in proven
    assert "f$cc_turn_donk_sbvbb_mnr_origin && f$cc_turn_donk_sbvbb_mnr_medium_xc_defense_proven" in proven
    assert "f$cc_turn_donk_sbvbb_mnr_origin && f$cc_turn_donk_sbvbb_mnr_weak_xc_defense_proven" in proven


def source_action_contract() -> None:
    improve = block(POL, "f$cc_turn_donk_sbvbb_draw_improved")
    assert "f$cc_turn_donk_sbvbb_draw_xc_defense_proven" in improve
    assert "f$cc_hand_pair_or_better" in improve

    runout = block(POL, "f$cc_turn_donk_sbvbb_source_runout_covered")
    assert "f$cc_turn_overcard_to_flop" in runout
    assert "f$cc_turn_undercard" in runout

    action = block(POL, "f$cc_turn_donk_sbvbb_draw_oc_action")
    assert "f$cc_turn_donk_sbvbb_draw_improved" in action
    assert "f$cc_turn_overcard_to_flop" in action

    uc = block(POL, "f$cc_turn_donk_sbvbb_draw_uc_checkraise_owner")
    assert "f$cc_turn_donk_sbvbb_draw_improved" in uc
    assert "f$cc_turn_undercard" in uc

    gap = block(POL, "f$cc_turn_donk_sbvbb_neutral_runout_source_gap")
    assert "!f$cc_turn_donk_sbvbb_source_runout_covered" in gap


def sizing_review_contract() -> None:
    size = block(POL, "f$cc_turn_donk_sbvbb_draw_oc_size_id")
    assert "f$cc_turn_donk_size_75_id" in size
    assert "f$cc_turn_donk_size_100_id" not in size

    # Mature short-stack <=1.80/persisted river shove must not leak into action.
    code = executable(POL)
    for forbidden in (
        "<= 1.80",
        "user_River",
        "RiverShove",
        "BetMax",
        "Raise_Committed",
        "HandPower",
        "random",
        "f$game_3wSBvBB",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden SBvBB executable leak: {forbidden}"

    diag = block(POL, "f$cc_turn_donk_sbvbb_source_pot_upper_bound_reviewed")
    assert "f$cc_turn_donk_sbvbb_draw_oc_action" in diag


def coverage_and_router_contract() -> None:
    covered = block(POL, "f$cc_turn_donk_sbvbb_covered")
    assert "f$cc_turn_donk_sbvbb_draw_xc_defense_proven" in covered
    assert "f$cc_turn_donk_sbvbb_source_runout_covered" in covered

    family = block(ROUTER, "f$cc_turn_donk_family_id")
    assert "f$cc_turn_donk_sbvbb_covered Return 4 Force" in family

    router = block(ROUTER, "f$cc_turn_donk_router")
    assert "f$cc_turn_donk_sbvbb_covered Return f$cc_turn_donk_sbvbb_action Force" in router

    size = block(ROUTER, "f$cc_turn_donk_size_id")
    assert "f$cc_turn_donk_sbvbb_covered Return f$cc_turn_donk_sbvbb_size_id Force" in size

    all_cov = block(ROUTER, "f$cc_turn_donk_strategy_covered")
    assert "f$cc_turn_donk_sbvbb_covered" in all_cov


if __name__ == "__main__":
    history_repair_contract()
    topology_contract()
    preflop_origin_contract()
    defense_provenance_contract()
    source_action_contract()
    sizing_review_contract()
    coverage_and_router_contract()
    print("PASS: Gate08C.3 SBvBB Turn Donk source/provenance contract")
