#!/usr/bin/env python3
"""Gate04A-F static contract tests for Flop Float strategy/topology."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

COMMON = (SRC / "CashCrusher_Flop_Float_Common.txt").read_text(encoding="utf-8")
SOURCE = (SRC / "CashCrusher_Flop_Float_Source.txt").read_text(encoding="utf-8")
SRP = (SRC / "CashCrusher_Flop_Float_SRP_6Max.txt").read_text(encoding="utf-8")
ISO = (SRC / "CashCrusher_Flop_Float_ISO.txt").read_text(encoding="utf-8")
THREE = (SRC / "CashCrusher_Flop_Float_3BP.txt").read_text(encoding="utf-8")
FOUR = (SRC / "CashCrusher_Flop_Float_4BP.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_Flop_Float.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def run_common_contract() -> None:
    first = block(COMMON, "f$cc_flop_float_first_hero_action")
    assert "BotsActionsOnThisRoundIncludingChecks = 0" in first

    opp = block(COMMON, "f$cc_flop_float_opportunity")
    assert "AmountToCall > 0 Return false Force" in opp
    assert "f$cc_relpos_id != 3 Return false Force" in opp
    assert "f$cc_hu && !f$cc_hu_ip Return false Force" in opp
    assert "f$cc_flop_float_first_hero_action" in opp

    caller = block(COMMON, "f$cc_flop_float_caller_role")
    for role in (
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_role_open_call_3bet",
        "f$cc_pf_role_cold_call_3bet",
        "f$cc_pf_role_call_4bet",
    ):
        assert role in caller
    assert "f$cc_pf_role_pfa" not in caller
    assert "f$cc_pf_role_unraised_caller" not in caller


def run_source_contract() -> None:
    husb = block(SOURCE, "f$cc_flop_float_true_hu_husb_context")
    for token in ("f$cc_true_hu", "f$cc_pf_hu_limp_raise_proven", "f$cc_pf_role_srp_caller", "f$cc_hu_matchup_id = 56"):
        assert token in husb

    husb_action = block(SOURCE, "f$cc_flop_float_true_hu_husb_action")
    for token in ("f$cc_hand_pair_or_better Return true Force", "f$cc_flop_float_premium_draw Return true Force", "f$cc_flop_float_good_draw Return true Force", "f$cc_flop_float_husb_air_family Return true Force"):
        assert token in husb_action

    bbsb = block(SOURCE, "f$cc_flop_float_bb_vs_sb_context")
    for token in ("f$cc_hu_origin_preflop_reduced", "f$cc_hero_pos_id = 6", "f$cc_hu_villain_pos_id = 5", "f$cc_hu_matchup_id = 65"):
        assert token in bbsb

    bbsb_action = block(SOURCE, "f$cc_flop_float_bb_vs_sb_action")
    assert "f$cc_flop_float_second_pair_high Return false Force" in bbsb_action
    assert "f$cc_flop_float_real_gutshot_plus Return true Force" in bbsb_action
    assert "f$cc_flop_float_air && f$cc_flop_float_dry_parent Return true Force" in bbsb_action
    assert "f$cc_flop_float_air && f$cc_flop_float_wet_parent Return false Force" in bbsb_action

    # The old short-stack XR shove plan must not be smuggled into initial Float.
    assert "BetMax" not in SOURCE
    assert "f$Raise_Committed" not in SOURCE
    assert "StackOffDraws" not in SOURCE


def run_sixmax_contract() -> None:
    hu = block(SRP, "f$cc_flop_float_srp_6max_hu_context")
    assert "f$cc_hero_pos_id >= 2" in hu and "f$cc_hero_pos_id <= 4" in hu
    assert "f$cc_hu_villain_pos_id < f$cc_hero_pos_id" in hu

    hu_action = block(SRP, "f$cc_flop_float_srp_6max_hu_action")
    assert "f$cc_cbet_flop_weak_top_pair Return false Force" in hu_action
    assert "f$cc_hand_middle_or_bottom_pair Return false Force" in hu_action
    assert "f$cc_cbet_flop_quality_air Return true Force" in hu_action
    assert "f$cc_flop_float_air Return false Force" in hu_action

    mw = block(SRP, "f$cc_flop_float_srp_multiway_context")
    assert "f$cc_flop_float_multiway_opportunity" in mw
    assert "f$cc_relpos_id = 3" in mw

    mw_action = block(SRP, "f$cc_flop_float_srp_multiway_action")
    assert "f$cc_flop_float_air Return false Force" in mw_action
    assert "nplayersplaying >= 4 && f$cc_flop_float_premium_draw && f$cc_real_combo_draw" in mw_action


def run_other_pots_contract() -> None:
    iso_origin = block(ISO, "f$cc_flop_float_iso_hero_provenance_consistent")
    assert "f$cc_flop_float_iso_hero_was_limper" in iso_origin
    assert "f$cc_flop_float_iso_hero_was_postraise_coldcaller" in iso_origin

    iso_cc = block(ISO, "f$cc_flop_float_iso_hu_coldcaller_action")
    assert "f$cc_flop_float_air Return false Force" in iso_cc

    origin = block(THREE, "f$cc_flop_float_3bp_hero_origin_consistent")
    for token in ("f$cc_flop_float_3bp_hero_is_opener_call", "f$cc_flop_float_3bp_hero_is_pre3bet_coldcaller", "f$cc_flop_float_3bp_hero_is_post3bet_coldcaller"):
        assert token in origin

    plain = block(THREE, "f$cc_flop_float_plain3bp_opener_hu_context")
    assert "f$cc_pf_3bet_plain_proven" in plain
    assert "f$cc_hu_villain_pos_id = f$cc_pf_3bet_final_raiser_pos_id" in plain

    cold = block(THREE, "f$cc_flop_float_squeeze_coldcaller_hu_action")
    assert "f$cc_flop_float_premium_draw Return true Force" in cold
    assert "f$cc_flop_float_good_draw Return false Force" in cold
    assert "f$cc_flop_float_air Return false Force" in cold

    four_proof = block(FOUR, "f$cc_flop_float_4bp_opener4_vs_hero3bettor_proven")
    assert "f$cc_pf_raise_count = 3" in four_proof
    assert "f$cc_pf_unique_raiser_count = 2" in four_proof
    assert "f$cc_flop_float_4bp_other_raiser_pos_id < f$cc_hero_pos_id" in four_proof

    four_action = block(FOUR, "f$cc_flop_float_4bp_hu_action")
    assert "f$cc_flop_float_air Return false Force" in four_action
    assert "f$cc_flop_float_premium_draw" in four_action
    assert "BetMax" not in FOUR


def run_global_safety() -> None:
    strategy_texts = [COMMON, SOURCE, SRP, ISO, THREE, FOUR, ROUTER]
    for text in strategy_texts:
        # New CashCrusher strategy must not execute through legacy scenario labels.
        executable = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
        assert "f$game_" not in executable

    router = block(ROUTER, "f$cc_flop_float_router")
    assert "When Others Return false Force" in router
    assert "f$cc_flop_float_source_covered" in router
    assert "f$cc_flop_float_srp_gap_covered" in router
    assert "f$cc_flop_float_iso_covered" in router
    assert "f$cc_flop_float_plain3bp_covered" in router
    assert "f$cc_flop_float_squeeze_covered" in router
    assert "f$cc_flop_float_4bp_covered" in router


if __name__ == "__main__":
    run_common_contract()
    run_source_contract()
    run_sixmax_contract()
    run_other_pots_contract()
    run_global_safety()
    print("PASS: Gate04 Flop Float source/topology/strategy contract")
