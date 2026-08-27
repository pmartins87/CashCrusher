#!/usr/bin/env python3
"""Gate06D deterministic ISO / true-HU limp-raised River Float contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Float_ISO.txt").read_text(encoding="utf-8")
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


def provenance_contract() -> None:
    hero = block(POL, "f$cc_river_float_iso_hero_origin_consistent")
    assert "f$cc_river_float_iso_hero_origin_count = 1" in hero

    agg = block(POL, "f$cc_river_float_iso_turn_aggressor_origin_consistent")
    assert "f$cc_river_float_iso_turn_aggressor_origin_count = 1" in agg

    for name, token in (
        ("f$cc_river_float_iso_hero_was_limper", "f$cc_pf_pre_raise_limper_mask"),
        ("f$cc_river_float_iso_hero_was_postraise_coldcaller", "f$cc_pf_post_raise_coldcaller_mask"),
        ("f$cc_river_float_iso_turn_aggressor_was_limper", "f$cc_pf_pre_raise_limper_mask"),
        ("f$cc_river_float_iso_turn_aggressor_was_coldcaller", "f$cc_pf_post_raise_coldcaller_mask"),
    ):
        assert token in block(POL, name)


def truehu_separation_contract() -> None:
    iso = block(POL, "f$cc_river_float_iso_context")
    assert "!f$cc_true_hu" in iso
    assert "f$cc_pf_iso_proven" in iso

    truehu = block(POL, "f$cc_river_float_truehu_limpraised_context")
    for token in (
        "f$cc_true_hu",
        "f$cc_pf_hu_limp_raise_proven",
        "f$cc_pf_role_srp_caller",
        "f$cc_hero_pos_id = 5",
        "f$cc_pf_rt_final_aggressor_pos_id = 6",
        "f$cc_river_float_turn_aggressor_pos_id = 6",
    ):
        assert token in truehu
    assert "f$cc_pf_iso_proven" not in truehu


def clean_hu_range_origin_contract() -> None:
    limper = block(POL, "f$cc_river_float_iso_clean_hu_limper_vs_isolator")
    cold = block(POL, "f$cc_river_float_iso_clean_hu_coldcaller_vs_isolator")
    pfa = block(POL, "f$cc_river_float_iso_clean_hu_isolator_lost_initiative")
    assert "f$cc_river_float_iso_hero_was_limper" in limper
    assert "f$cc_river_float_iso_hero_was_postraise_coldcaller" in cold
    assert "f$cc_river_float_iso_hero_was_isolator" in pfa
    assert "f$cc_river_float_iso_turn_aggressor_is_isolator" in limper
    assert "f$cc_river_float_iso_turn_aggressor_is_isolator" in cold


def multiway_and_fourplus_contract() -> None:
    postmw = block(POL, "f$cc_river_float_iso_postmultiway_now_hu_unresolved")
    assert "f$cc_river_float_hu_multiway_origin_unresolved" in postmw

    currentmw = block(POL, "f$cc_river_float_iso_current_multiway")
    assert "f$cc_river_float_current_multiway" in currentmw

    fourplus = block(POL, "f$cc_river_float_iso_fourplus_origin")
    assert "f$cc_flop_entry_count >= 4" in fourplus

    robust = block(POL, "f$cc_river_float_iso_fourplus_robust_value")
    for token in (
        "f$cc_river_float_source_literal_nuts Return true Force",
        "f$cc_river_four_card_completion",
        "HaveFullHouse",
        "FlushPossible",
        "HaveFlush",
        "StraightPossible",
        "f$cc_river_straight_or_better",
        "f$cc_river_two_pair_plus Return true Force",
    ):
        assert token in robust


def bluff_and_stack_safety_contract() -> None:
    action = block(POL, "f$cc_river_float_iso_action")
    assert "f$cc_river_float_iso_fourplus_robust_value Return true Force" in action
    assert "When Others Return false Force" in action
    assert "f$cc_river_no_made Return true Force" not in action

    code = executable(POL).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "stackoffdraws",
        "botcalledonflop",
        "botcalledonturn",
    ):
        assert forbidden not in code, f"forbidden executable ISO River Float leak: {forbidden}"


def coverage_and_router_contract() -> None:
    covered = block(POL, "f$cc_river_float_iso_covered")
    assert "!f$cc_river_float_source_covered" in covered
    assert "f$cc_river_float_iso_topology_id > 0" in covered

    consistency = block(POL, "f$cc_river_float_iso_size_consistent")
    assert "f$cc_river_float_iso_size_id = 0" in consistency
    assert "f$cc_river_float_iso_size_id >= 1 && f$cc_river_float_iso_size_id <= 5" in consistency

    family = block(ROUTER, "f$cc_river_float_family_id")
    assert "f$cc_river_float_iso_covered Return 3 Force" in family

    router = block(ROUTER, "f$cc_river_float_router")
    source = "f$cc_river_float_source_covered Return f$cc_river_float_source_action Force"
    srp = "f$cc_river_float_srp_gap_covered Return f$cc_river_float_srp_gap_action Force"
    iso = "f$cc_river_float_iso_covered Return f$cc_river_float_iso_action Force"
    assert source in router and srp in router and iso in router
    assert router.index(source) < router.index(srp) < router.index(iso)


if __name__ == "__main__":
    provenance_contract()
    truehu_separation_contract()
    clean_hu_range_origin_contract()
    multiway_and_fourplus_contract()
    bluff_and_stack_safety_contract()
    coverage_and_router_contract()
    print("PASS: Gate06D ISO / true-HU limp-raised River Float contract")
