#!/usr/bin/env python3
"""Gate06E contracts for plain-3BP / squeeze River Float."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Float_3BP.txt").read_text(encoding="utf-8")
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


def chronology_contract() -> None:
    plain = block(POL, "f$cc_river_float_plain3bp_context")
    squeeze = block(POL, "f$cc_river_float_squeeze_context")
    assert "f$cc_pf_rt_plain3bet_proven" in plain
    assert "!f$cc_pf_rt_squeeze_proven" in plain
    assert "f$cc_pf_rt_squeeze_proven" in squeeze
    assert "f$cc_river_float_3bp_hero_origin_consistent" in plain
    assert "f$cc_river_float_3bp_turn_aggressor_origin_consistent" in squeeze

    pre = block(POL, "f$cc_river_float_3bp_rt_pre3bet_coldcaller_mask")
    post = block(POL, "f$cc_river_float_3bp_rt_post3bet_coldcaller_mask")
    assert "f$cc_pf_rt_3bet_order_supported" in pre
    assert "f$cc_pf_rt_3bet_first_raiser_pos_id" in pre
    assert "f$cc_pf_rt_final_aggressor_pos_id" in pre
    assert "f$cc_pf_rt_3bet_order_supported" in post
    assert "f$cc_pf_rt_final_aggressor_pos_id" in post


def origin_contract() -> None:
    hero_count = block(POL, "f$cc_river_float_3bp_hero_origin_count")
    for token in (
        "f$cc_river_float_3bp_hero_is_final3bettor",
        "f$cc_river_float_3bp_hero_is_opener_call",
        "f$cc_river_float_3bp_hero_is_pre3bet_coldcaller",
        "f$cc_river_float_3bp_hero_is_post3bet_coldcaller",
    ):
        assert token in hero_count

    agg_count = block(POL, "f$cc_river_float_3bp_turn_aggressor_origin_count")
    for token in (
        "f$cc_river_float_3bp_turn_aggressor_is_opener",
        "f$cc_river_float_3bp_turn_aggressor_is_final3bettor",
        "f$cc_river_float_3bp_turn_aggressor_is_pre3bet_coldcaller",
        "f$cc_river_float_3bp_turn_aggressor_is_post3bet_coldcaller",
    ):
        assert token in agg_count

    # Plain 3BP has no pre-squeeze Hero family; squeeze does.
    assert "pre3bet" not in block(POL, "f$cc_river_float_plain3bp_topology_id")
    assert "f$cc_river_float_squeeze_clean_hu_precold_vs_squeezer" in block(
        POL, "f$cc_river_float_squeeze_topology_id"
    )


def source_silent_policy_contract() -> None:
    code = executable(POL)
    for forbidden in (
        "HandPower",
        "BetMax",
        "f$Raise_Committed",
        "f$hand_StackOffDraws",
        "f$cc_mw_spr_shallowest_round_start",
    ):
        assert forbidden not in code, f"forbidden Gate06E executable leak: {forbidden}"

    # Current no-made is documented as missing provenance, never a positive action.
    missing = block(POL, "f$cc_river_float_3bp_nomade_snapshot_missing")
    assert "f$cc_river_no_made" in missing
    plain_action = block(POL, "f$cc_river_float_plain3bp_action")
    squeeze_action = block(POL, "f$cc_river_float_squeeze_action")
    assert "f$cc_river_no_made" not in plain_action
    assert "f$cc_river_no_made" not in squeeze_action
    assert "f$cc_river_float_3bp_fourplus_robust_value Return true Force" in plain_action
    assert "f$cc_river_float_3bp_fourplus_robust_value Return true Force" in squeeze_action
    assert "When Others Return false Force" in plain_action
    assert "When Others Return false Force" in squeeze_action


def multiway_contract() -> None:
    unresolved = block(POL, "f$cc_river_float_3bp_postmultiway_now_hu_unresolved")
    assert "f$cc_river_float_hu_multiway_origin_unresolved" in unresolved

    four = block(POL, "f$cc_river_float_3bp_fourplus_robust_value")
    assert "f$cc_river_float_source_literal_nuts Return true Force" in four
    assert "f$cc_river_four_card_completion" in four
    assert "FlushPossible" in four
    assert "StraightPossible" in four
    assert "f$cc_river_two_pair_plus Return true Force" in four
    assert "When Others Return false Force" in four

    covered_plain = block(POL, "f$cc_river_float_plain3bp_covered")
    covered_sq = block(POL, "f$cc_river_float_squeeze_covered")
    assert "!f$cc_river_float_source_covered" in covered_plain
    assert "!f$cc_river_float_source_covered" in covered_sq


def router_contract() -> None:
    family = block(ROUTER, "f$cc_river_float_family_id")
    assert "f$cc_river_float_plain3bp_covered Return 4 Force" in family
    assert "f$cc_river_float_squeeze_covered Return 5 Force" in family

    router = block(ROUTER, "f$cc_river_float_router")
    assert "f$cc_river_float_plain3bp_covered Return f$cc_river_float_plain3bp_action Force" in router
    assert "f$cc_river_float_squeeze_covered Return f$cc_river_float_squeeze_action Force" in router

    size = block(ROUTER, "f$cc_river_float_size_id")
    assert "f$cc_river_float_plain3bp_covered Return f$cc_river_float_plain3bp_size_id Force" in size
    assert "f$cc_river_float_squeeze_covered Return f$cc_river_float_squeeze_size_id Force" in size


if __name__ == "__main__":
    chronology_contract()
    origin_contract()
    source_silent_policy_contract()
    multiway_contract()
    router_contract()
    print("PASS: Gate06E plain-3BP/squeeze River-Float provenance/policy contract")
