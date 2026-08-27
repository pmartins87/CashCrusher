#!/usr/bin/env python3
"""Gate05B direct-source Turn Float strategy and anti-leak contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
COMMON = (SRC / "CashCrusher_Turn_Float_Common.txt").read_text(encoding="utf-8")
REPAIR = (SRC / "CashCrusher_Turn_Float_SourceRepair.txt").read_text(encoding="utf-8")
SOURCE = (SRC / "CashCrusher_Turn_Float_Source.txt").read_text(encoding="utf-8")
COVERAGE = (SRC / "CashCrusher_Turn_Float_SourceCoverageRepair.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_Turn_Float.txt").read_text(encoding="utf-8")
TEXTS = (COMMON, REPAIR, SOURCE, COVERAGE, ROUTER)


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def source_repair_contract() -> None:
    pre = block(REPAIR, "f$cc_turn_float_source_limped_bbv_sb_preflop")
    assert "f$cc_pot_family_id = 1" in pre
    assert "f$cc_pf_role_bb_check" in pre
    assert "f$cc_hero_pos_id = 6" in pre
    assert "f$cc_pf_call_sb" in pre

    parent = block(REPAIR, "f$cc_turn_float_source_limped_bbv_sb_parent")
    assert "f$cc_turn_float_flop_call_only" in parent
    assert "f$cc_turn_float_single_flop_aggressor" in parent
    assert "f$cc_turn_float_flop_aggressor_pos_id = 5" in parent

    opp = block(REPAIR, "f$cc_turn_float_source_limped_bbv_sb_opportunity")
    for required in (
        "f$cc_turn_float_first_hero_action",
        "AmountToCall > 0 Return false Force",
        "f$cc_relpos_id != 3 Return false Force",
        "!f$cc_hu Return false Force",
        "!f$cc_hu_ip Return false Force",
        "f$cc_flop_entry_count != 2 Return false Force",
        "lastraised2 != headsupchair Return false Force",
    ):
        assert required in opp


def bbv_sb_source_contract() -> None:
    srp = block(SOURCE, "f$cc_turn_float_source_bbv_sb_srp_context")
    assert "f$cc_turn_float_parent_id = 1" in srp
    assert "f$cc_pf_one_raise_ordinary_srp" in srp
    assert "f$cc_hero_pos_id = 6" in srp
    assert "f$cc_pf_rt_final_aggressor_pos_id = 5" in srp
    assert "f$cc_turn_float_flop_aggressor_pos_id = 5" in srp

    ctx = block(SOURCE, "f$cc_turn_float_source_bbv_sb_context")
    assert "f$cc_turn_float_source_bbv_sb_srp_context" in ctx
    assert "f$cc_turn_float_source_bbv_sb_limped_context" in ctx

    action = block(SOURCE, "f$cc_turn_float_source_bbv_sb_action")
    assert "f$cc_turn_float_current_real_draw Return true Force" in action
    assert "f$cc_turn_float_current_air Return true Force" in action
    assert "When Others Return false Force" in action

    size = block(SOURCE, "f$cc_turn_float_source_bbv_sb_size_id")
    assert "f$cc_turn_float_size_50_id" in size

    river = block(SOURCE, "f$cc_turn_float_source_bbv_sb_river_plan_id")
    assert "When f$cc_turn_completed Return 2 Force" in river
    assert "When Others Return 1 Force" in river
    # Source uses broad turn_Completed, not only a new completion by Turn card.
    assert "f$cc_turn_new_completion" not in river


def btn_advanced_contract() -> None:
    analog = block(COMMON, "f$cc_turn_float_btnadv_flop_draw_marker_analog")
    assert "user_cc_flop_cbet_had_no_made" in analog
    assert "user_cc_flop_cbet_had_premium_draw" in analog
    assert "user_cc_flop_cbet_had_good_draw" in analog
    assert "user_cc_flop_cbet_had_weak_draw" in analog

    ctx = block(SOURCE, "f$cc_turn_float_source_btnadv_context")
    assert "f$cc_turn_float_parent_id = 2" in ctx
    assert "f$cc_pf_one_raise_ordinary_srp" in ctx
    assert "f$cc_pf_role_pfa" in ctx
    assert "f$cc_hero_pos_id = 4" in ctx
    assert "f$cc_turn_float_btnadv_flop_draw_marker_analog" in ctx

    air = block(SOURCE, "f$cc_turn_float_source_btnadv_air_action")
    assert "f$cc_turn_float_current_air" in air
    assert "!f$cc_turn_float_source_btnv_sb_nomade_lock" in air

    draw_lock = block(SOURCE, "f$cc_turn_float_source_btnadv_live_draw_lock")
    assert "f$cc_turn_float_current_real_draw" in draw_lock

    made = block(SOURCE, "f$cc_turn_float_source_btnadv_made_action")
    assert "f$cc_turn_float_btnadv_made_improvement" in made

    size = block(SOURCE, "f$cc_turn_float_source_btnadv_size_id")
    assert "f$cc_turn_float_source_btnadv_air_action Return f$cc_turn_float_size_33_id" in size
    assert "f$cc_turn_float_source_btnadv_made_action Return f$cc_turn_float_size_50_id" in size

    assert "user_AirCalledRaiseOTF" not in "\n".join(
        line.split("//", 1)[0] for line in SOURCE.splitlines()
    )


def negative_source_contract() -> None:
    lock = block(SOURCE, "f$cc_turn_float_source_btnv_sb_nomade_lock")
    assert "f$cc_hero_pos_id = 4" in lock
    assert "f$cc_turn_float_flop_aggressor_pos_id = 5" in lock
    assert "f$cc_hand_no_made" in lock

    global_lock = block(SOURCE, "f$cc_turn_float_source_locked_check")
    assert "f$cc_turn_float_source_btnv_sb_nomade_lock" in global_lock
    assert "f$cc_turn_float_source_btnadv_live_draw_lock" in global_lock

    exact = block(COVERAGE, "f$cc_turn_float_source_exact_covered")
    # BB-v-SB source owns only the exact positive no-made action, not every
    # made-hand state in the same matchup.
    assert "f$cc_turn_float_source_bbv_sb_action" in exact
    assert "f$cc_turn_float_source_bbv_sb_context" not in exact
    assert "f$cc_turn_float_source_btnadv_context" in exact
    assert "f$cc_turn_float_source_btnv_sb_nomade_lock" in exact

    consistent = block(COVERAGE, "f$cc_turn_float_source_exact_consistent")
    assert "f$cc_turn_float_source_exact_locked_check && f$cc_turn_float_source_exact_positive Return false Force" in consistent

    dispatcher = block(SOURCE, "f$cc_turn_float_source_action")
    assert dispatcher.index("f$cc_turn_float_source_locked_check") < dispatcher.index(
        "f$cc_turn_float_source_bbv_sb_context"
    )


def router_and_safety_contract() -> None:
    router = block(ROUTER, "f$cc_turn_float_router")
    assert "f$cc_turn_float_source_exact_locked_check Return false Force" in router
    assert "f$cc_turn_float_source_exact_positive Return f$cc_turn_float_source_action Force" in router
    # Direct source must precede every professional gap family.
    source_offset = router.index("f$cc_turn_float_source_exact_positive")
    for gap in (
        "f$cc_turn_float_srp_gap_covered",
        "f$cc_turn_float_iso_gap_covered",
        "f$cc_turn_float_plain3bp_gap_covered",
        "f$cc_turn_float_squeeze_gap_covered",
        "f$cc_turn_float_4bp_gap_covered",
    ):
        assert source_offset < router.index(gap)
    assert "When Others Return false Force" in router

    size = block(ROUTER, "f$cc_turn_float_size_consistent")
    assert "f$cc_turn_float_size_id = 0" in size
    assert "f$cc_turn_float_size_id >= 1 && f$cc_turn_float_size_id <= 5" in size

    uncovered = block(ROUTER, "f$cc_turn_float_uncovered_recognized")
    assert "!f$cc_turn_float_source_exact_covered" in uncovered

    executable = "\n".join(
        line.split("//", 1)[0] for text in TEXTS for line in text.splitlines()
    )
    assert "HandPower" not in executable
    # Source strategy itself does not own BetMax; canonical full router can only
    # request a strategic size and runtime equivalence is a separate file.
    assert "BetMax" not in executable
    assert "random" not in executable.lower()
    assert "Raise_Committed" not in executable
    assert "StackOffDraws" not in executable


if __name__ == "__main__":
    source_repair_contract()
    bbv_sb_source_contract()
    btn_advanced_contract()
    negative_source_contract()
    router_and_safety_contract()
    print("PASS: Gate05B direct-source Turn Float strategy + LP repair contract")
