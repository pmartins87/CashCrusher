#!/usr/bin/env python3
"""Gate12B.8/9 deterministic tests for 3BP, squeeze and clean 4BP fills."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THREE = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_3BP.txt").read_text(encoding="utf-8")
FOUR = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_4BP.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    return text.split(marker, 1)[1].split("##", 1)[0]


def run_3bp_contract() -> None:
    plain = block(THREE, "f$cc_turn_delayed_float_plain3bp_context")
    squeeze = block(THREE, "f$cc_turn_delayed_float_squeeze_context")
    assert "f$cc_turn_delayed_float_gate04_family_id = 4" in plain
    assert "f$cc_turn_delayed_float_gate04_family_id = 5" in squeeze
    assert "f$cc_pot_family_id = 3" in plain and "f$cc_pot_family_id = 3" in squeeze
    assert "f$cc_pf_squeeze_proven" in squeeze
    for role in ("f$cc_pf_role_open_call_3bet", "f$cc_pf_role_cold_call_3bet"):
        assert role in plain and role in squeeze

    plain_hu = block(THREE, "f$cc_turn_delayed_float_plain3bp_hu_action")
    sq_hu = block(THREE, "f$cc_turn_delayed_float_squeeze_hu_action")
    assert "f$cc_turn_delayed_float_plain3bp_secondpair_thin Return true" in plain_hu
    assert "f$cc_turn_delayed_float_plain3bp_air_bluff Return true" in plain_hu
    assert "secondpair_thin" not in sq_hu
    assert "air_bluff" not in sq_hu
    assert "f$cc_turn_delayed_float_semibluff_candidate Return true" in sq_hu

    plain_mw = block(THREE, "f$cc_turn_delayed_float_plain3bp_mw_action")
    sq_mw = block(THREE, "f$cc_turn_delayed_float_squeeze_mw_action")
    for mw in (plain_mw, sq_mw):
        assert "f$cc_turn_delayed_float_two_pair_plus_real Return true" in mw
        assert "f$cc_real_combo_draw" in mw
        assert "air_bluff" not in mw
        assert "When Others Return false Force" in mw

    assert "f$cc_turn_delayed_float_size_33_id" in block(THREE, "f$cc_turn_delayed_float_plain3bp_hu_size_id")
    sq_size = block(THREE, "f$cc_turn_delayed_float_squeeze_hu_size_id")
    assert "f$cc_turn_delayed_float_size_33_id" not in sq_size
    assert "f$cc_turn_delayed_float_size_50_id" in sq_size
    assert "f$cc_turn_delayed_float_size_75_id" in sq_size


def run_4bp_contract() -> None:
    ctx = block(FOUR, "f$cc_turn_delayed_float_4bp_context")
    for token in (
        "f$cc_turn_delayed_float_gate04_family_id = 6",
        "f$cc_pot_family_id = 4",
        "f$cc_pf_role_call_4bet",
        "f$cc_flop_float_4bp_opener4_vs_hero3bettor_proven",
        "f$cc_hu",
        "f$cc_hu_ip",
    ):
        assert token in ctx

    value = block(FOUR, "f$cc_turn_delayed_float_4bp_value_action")
    assert "f$cc_turn_delayed_float_two_pair_plus_real Return true" in value
    assert "f$cc_turn_delayed_float_tpop_real && f$cc_turn_delayed_float_thin_value_runout Return true" in value

    draw = block(FOUR, "f$cc_turn_delayed_float_4bp_draw_action")
    assert "f$cc_turn_delayed_float_semibluff_candidate" in draw

    action = block(FOUR, "f$cc_turn_delayed_float_4bp_action")
    assert "f$cc_turn_delayed_float_4bp_value_action Return true" in action
    assert "f$cc_turn_delayed_float_4bp_draw_action Return true" in action
    assert "When Others Return false Force" in action

    sizes = block(FOUR, "f$cc_turn_delayed_float_4bp_size_id")
    assert "f$cc_turn_delayed_float_size_75_id" in sizes
    assert "f$cc_turn_delayed_float_size_50_id" in sizes
    assert "f$cc_turn_delayed_float_size_33_id" not in sizes


def run_router_contract() -> None:
    family = block(ROUTER, "f$cc_turn_delayed_float_family_id")
    expected = {
        "f$cc_turn_delayed_float_plain3bp_hu_context": 7,
        "f$cc_turn_delayed_float_plain3bp_mw_context": 8,
        "f$cc_turn_delayed_float_squeeze_hu_context": 9,
        "f$cc_turn_delayed_float_squeeze_mw_context": 10,
        "f$cc_turn_delayed_float_4bp_covered": 11,
    }
    for name, ident in expected.items():
        assert f"When {name} Return {ident} Force" in family

    router = block(ROUTER, "f$cc_turn_delayed_float_router")
    for name in (
        "f$cc_turn_delayed_float_plain3bp_covered",
        "f$cc_turn_delayed_float_squeeze_covered",
        "f$cc_turn_delayed_float_4bp_covered",
    ):
        assert name in router
    assert "When Others Return false Force" in router


def run_safety_contract() -> None:
    executable = "\n".join(
        line
        for text in (THREE, FOUR)
        for line in text.splitlines()
        if not line.lstrip().startswith("//")
    )
    for forbidden in ("HandPower", "Random", "random", "BetMax", "Allin", "allin", "Commit", "commit"):
        assert forbidden not in executable, f"forbidden generic token: {forbidden}"


if __name__ == "__main__":
    run_3bp_contract()
    run_4bp_contract()
    run_router_contract()
    run_safety_contract()
    print("PASS: Gate12B 3BP/squeeze/clean4BP contracts")
