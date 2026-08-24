#!/usr/bin/env python3
"""Gate06B deterministic direct/high-ancestry River Float source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
POL = (SRC / "CashCrusher_River_Float_Source.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def reviewed_pot_domain_contract() -> None:
    one = block(POL, "f$cc_river_float_source_reviewed_one_raise_domain")
    assert "f$cc_pot_family_id = 2" in one
    assert "f$cc_pf_one_raise_ordinary_srp" in one
    assert "f$cc_pf_iso_proven" in one
    assert "f$cc_pf_hu_limp_raise_proven" in one

    three = block(POL, "f$cc_river_float_source_reviewed_threebet_domain")
    assert "f$cc_pot_family_id = 3" in three
    assert "f$cc_pf_rt_plain3bet_proven" in three
    assert "f$cc_pf_rt_squeeze_proven" in three

    hero4 = block(POL, "f$cc_river_float_source_reviewed_4bp_hero4_domain")
    for token in (
        "f$cc_pot_family_id = 4",
        "f$cc_river_float_current_hu_from_hu_flop",
        "f$cc_river_float_hu_aggressor_is_current_villain",
        "f$cc_pf_role_4bettor",
        "f$cc_pf_4bet_subtype_id > 0",
        "f$cc_hu_4bp_survivor_consistent",
        "f$cc_hu_4bp_survivor_type_id >= 1",
        "f$cc_hu_4bp_survivor_type_id <= 2",
    ):
        assert token in hero4

    caller4 = block(POL, "f$cc_river_float_source_reviewed_4bp_caller_domain")
    assert "f$cc_turn_float_pf_fourbet_caller_supported" in caller4
    assert "f$cc_hu_villain_pos_id = f$cc_flop_float_4bp_other_raiser_pos_id" in caller4

    domain = block(POL, "f$cc_river_float_source_reviewed_pot_domain")
    assert "f$cc_river_float_source_reviewed_one_raise_domain" in domain
    assert "f$cc_river_float_source_reviewed_threebet_domain" in domain
    assert "f$cc_river_float_source_reviewed_4bp_domain" in domain

    code = executable(domain)
    assert "f$cc_pot_family_id = 1" not in code
    assert "f$cc_pot_family_id = 5" not in code


def value_source_contract() -> None:
    tp = block(POL, "f$cc_river_float_source_top_pair_top4")
    assert "f$cc_river_top_pair" in tp
    assert "f$cc_number_better_kickers <= 4" in tp

    domain = block(POL, "f$cc_river_float_source_general_domain_supported")
    for token in (
        "f$cc_river_float_opportunity",
        "f$cc_river_float_source_reviewed_pot_domain",
        "f$cc_flop_entry_count >= 2",
        "f$cc_flop_entry_count <= 3",
        "nplayersplaying >= 2",
        "nplayersplaying <= 3",
    ):
        assert token in domain

    action = block(POL, "f$cc_river_float_source_general_value_action")
    for token in (
        "!f$cc_river_float_source_general_domain_supported Return false Force",
        "f$cc_river_float_source_literal_nuts Return true Force",
        "f$cc_river_two_pair_plus Return true Force",
        "f$cc_river_overpair Return true Force",
        "f$cc_river_float_source_top_pair_top4 Return true Force",
        "When Others Return false Force",
    ):
        assert token in action

    size = block(POL, "f$cc_river_float_source_general_value_size_id")
    assert "f$cc_river_float_source_literal_nuts Return f$cc_river_size_75_id Force" in size
    assert "f$cc_river_two_pair_plus && f$cc_river_super_completed Return f$cc_river_size_50_id Force" in size
    assert "f$cc_river_two_pair_plus Return f$cc_river_size_75_id Force" in size
    assert "f$cc_river_overpair Return f$cc_river_size_50_id Force" in size
    assert "f$cc_river_float_source_top_pair_top4 Return f$cc_river_size_50_id Force" in size


def exact_bbv_sb_contract() -> None:
    action = block(POL, "f$cc_river_float_source_bbv_sb_exact_action")
    assert "!f$cc_river_float_source_bbv_sb_exact_parent_ready Return false Force" in action
    assert "f$cc_river_two_pair_plus Return true Force" in action
    assert "f$cc_river_overpair || f$cc_river_top_pair Return true Force" in action
    assert "f$cc_river_no_made Return true Force" in action

    size = block(POL, "f$cc_river_float_source_bbv_sb_exact_size_id")
    assert "f$cc_river_two_pair_plus Return f$cc_river_size_75_id Force" in size
    assert "f$cc_river_overpair || f$cc_river_top_pair Return f$cc_river_size_50_id Force" in size
    assert "f$cc_river_no_made Return f$cc_river_size_25_id Force" in size

    lock = block(POL, "f$cc_river_float_source_bbv_sb_snapshot_lock")
    assert "f$cc_river_float_source_bbv_sb_waiting_defense_snapshot" in lock


def negative_source_contract() -> None:
    btn = block(POL, "f$cc_river_float_source_btnv_sb_nomade_lock")
    for token in (
        "f$cc_river_float_parent_id = 1",
        "f$cc_river_float_current_hu_from_hu_flop",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_hero_pos_id = 4",
        "f$cc_river_float_turn_aggressor_pos_id = 5",
        "f$cc_river_no_made",
    ):
        assert token in btn

    locked = block(POL, "f$cc_river_float_source_locked_check")
    assert "f$cc_river_float_source_btnv_sb_nomade_lock" in locked
    assert "f$cc_river_float_source_bbv_sb_snapshot_lock" in locked


def precedence_and_safety_contract() -> None:
    router = block(POL, "f$cc_river_float_source_action")
    exact = "f$cc_river_float_source_bbv_sb_exact_parent_ready Return f$cc_river_float_source_bbv_sb_exact_action Force"
    lock = "f$cc_river_float_source_locked_check Return false Force"
    generic = "f$cc_river_float_source_general_value_action Return true Force"
    assert exact in router and lock in router and generic in router
    assert router.index(exact) < router.index(lock) < router.index(generic)

    covered = block(POL, "f$cc_river_float_source_covered")
    assert "f$cc_river_float_source_bbv_sb_exact_parent_ready" in covered
    assert "f$cc_river_float_source_locked_check" in covered
    assert "f$cc_river_float_source_general_value_action" in covered

    consistency = block(POL, "f$cc_river_float_source_size_consistent")
    assert "f$cc_river_float_source_size_id = 0" in consistency
    assert "f$cc_river_float_source_size_id >= 1 && f$cc_river_float_source_size_id <= 5" in consistency

    code = executable(POL)
    for forbidden in (
        "HandPower",
        "random",
        "BotCalledOnFlop",
        "BotCalledOnTurn",
        "BetMax",
        "Raise_Committed",
        "StackOffDraws",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden executable source leak: {forbidden}"

    # No generic no-made bluff may be introduced outside the exact source branch.
    general = block(POL, "f$cc_river_float_source_general_value_action")
    assert "f$cc_river_no_made" not in general


if __name__ == "__main__":
    reviewed_pot_domain_contract()
    value_source_contract()
    exact_bbv_sb_contract()
    negative_source_contract()
    precedence_and_safety_contract()
    print("PASS: Gate06B River Float direct/high-ancestry source + pot-domain contract")
