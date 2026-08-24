#!/usr/bin/env python3
"""Gate06F clean-HU 4BP River Float contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Float_4BP.txt").read_text(encoding="utf-8")
SRC = (ROOT / "src" / "CashCrusher_River_Float_Source.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_River_Float.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def source_domain_contract() -> None:
    source4 = block(SRC, "f$cc_river_float_source_reviewed_4bp_domain")
    assert "f$cc_river_float_source_reviewed_4bp_hero4_domain" in source4
    assert "f$cc_river_float_source_reviewed_4bp_caller_domain" in source4

    hero = block(SRC, "f$cc_river_float_source_reviewed_4bp_hero4_domain")
    assert "f$cc_river_float_current_hu_from_hu_flop" in hero
    assert "f$cc_hu_4bp_survivor_type_id >= 1" in hero
    assert "f$cc_hu_4bp_survivor_type_id <= 2" in hero

    caller = block(SRC, "f$cc_river_float_source_reviewed_4bp_caller_domain")
    assert "f$cc_turn_float_pf_fourbet_caller_supported" in caller
    assert "f$cc_hu_villain_pos_id = f$cc_flop_float_4bp_other_raiser_pos_id" in caller


def clean_topology_contract() -> None:
    caller = block(POL, "f$cc_river_float_4bp_caller_clean_hu_context")
    for token in (
        "f$cc_pot_family_id = 4",
        "f$cc_river_float_current_hu_from_hu_flop",
        "f$cc_river_float_hu_aggressor_is_current_villain",
        "f$cc_turn_float_pf_fourbet_caller_supported",
        "f$cc_hu_villain_pos_id = f$cc_flop_float_4bp_other_raiser_pos_id",
    ):
        assert token in caller

    hero = block(POL, "f$cc_river_float_4bp_hero4_clean_hu_context")
    for token in (
        "f$cc_pf_role_4bettor",
        "f$cc_pf_4bet_subtype_id > 0",
        "f$cc_hu_4bp_survivor_consistent",
        "f$cc_hu_4bp_survivor_type_id >= 1",
        "f$cc_hu_4bp_survivor_type_id <= 2",
    ):
        assert token in hero

    count = block(POL, "f$cc_river_float_4bp_hero4_family_count")
    assert "f$cc_river_float_4bp_opener4_vs_threebettor" in count
    assert "f$cc_river_float_4bp_cold4_vs_opener" in count
    assert "f$cc_river_float_4bp_cold4_vs_threebettor" in count


def reviewed_check_and_fail_closed_contract() -> None:
    action = block(POL, "f$cc_river_float_4bp_action")
    assert "When !f$cc_river_float_4bp_covered Return false Force" in action
    assert "When Others Return false Force" in action
    assert "Return true Force" not in action

    missing = block(POL, "f$cc_river_float_4bp_nomade_snapshot_missing")
    assert "f$cc_river_no_made" in missing

    uncovered = block(POL, "f$cc_river_float_4bp_uncovered")
    assert "f$cc_pot_family_id = 4" in uncovered
    assert "!f$cc_river_float_4bp_covered" in uncovered

    five = block(POL, "f$cc_river_float_5betplus_uncovered")
    assert "f$cc_pot_family_id = 5" in five

    code = executable(POL)
    for forbidden in (
        "HandPower",
        "random",
        "BetMax",
        "Raise_Committed",
        "StackOffDraws",
        "f$cc_mw_spr_shallowest_round_start",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate06F executable leak: {forbidden}"


def router_contract() -> None:
    family = block(ROUTER, "f$cc_river_float_family_id")
    assert "f$cc_river_float_4bp_covered Return 6 Force" in family

    router = block(ROUTER, "f$cc_river_float_router")
    assert "f$cc_river_float_4bp_covered Return f$cc_river_float_4bp_action Force" in router

    size = block(ROUTER, "f$cc_river_float_size_id")
    assert "f$cc_river_float_4bp_covered Return f$cc_river_float_4bp_size_id Force" in size

    covered = block(ROUTER, "f$cc_river_float_strategy_covered")
    assert "f$cc_river_float_4bp_covered" in covered


if __name__ == "__main__":
    source_domain_contract()
    clean_topology_contract()
    reviewed_check_and_fail_closed_contract()
    router_contract()
    print("PASS: Gate06F clean-HU 4BP River-Float source-domain/policy contract")
