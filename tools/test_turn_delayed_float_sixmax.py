#!/usr/bin/env python3
"""Gate12B.5-7 deterministic tests for HUSB boundary + SRP/ISO fills."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMON = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_Common.txt").read_text(encoding="utf-8")
HUSB = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_HUSB_Negative.txt").read_text(encoding="utf-8")
SRP = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_SRP_6Max.txt").read_text(encoding="utf-8")
ISO = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_ISO.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat.txt").read_text(encoding="utf-8")
FLOP_HUSB = (ROOT / "src" / "CashCrusher_Flop_Float_Source.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing function {name}"
    return text.split(marker, 1)[1].split("##", 1)[0]


def run_common_contract() -> None:
    bridge = block(COMMON, "f$cc_turn_delayed_float_gate04_checkback_valid")
    assert "f$cc_hist_flop_float_checkback_parent_valid" in bridge
    family = block(COMMON, "f$cc_turn_delayed_float_gate04_family_id")
    assert "f$cc_hist_flop_float_family_id" in family

    for marker in (
        "user_cc_flop_float_state_had_2pplus",
        "user_cc_flop_float_state_had_overpair",
        "user_cc_flop_float_state_had_top_pair",
        "user_cc_flop_float_state_had_lower_pair",
        "user_cc_flop_float_state_had_no_made",
        "user_cc_flop_float_state_had_premium_draw",
        "user_cc_flop_float_state_had_good_draw",
        "user_cc_flop_float_state_had_air",
    ):
        assert marker in COMMON

    pressure = block(COMMON, "f$cc_turn_delayed_float_bluff_pressure_card")
    assert "f$cc_turn_meaningful_overcard" in pressure
    assert "!f$cc_turn_pairs_flop_rank" in pressure
    assert "!f$cc_turn_new_completion" in pressure

    for size in ("size_33_id", "size_50_id", "size_75_id"):
        assert f"f$cc_turn_delayed_float_{size}" in COMMON


def run_husb_negative_contract() -> None:
    ctx = block(HUSB, "f$cc_turn_delayed_float_husb_source_negative_context")
    for token in (
        "f$cc_true_hu",
        "f$cc_pf_hu_limp_raise_proven",
        "f$cc_pf_role_srp_caller",
        "f$cc_hero_pos_id = 5",
        "f$cc_hu_villain_pos_id = 6",
        "f$cc_hu_matchup_id = 56",
    ):
        assert token in ctx

    # Current reviewed HUSB missed-ISO-CBet source has positive branches for all
    # portable hand regions; old removed checkbacks must not become 12B strategy.
    flop_action = block(FLOP_HUSB, "f$cc_flop_float_true_hu_husb_action")
    for token in (
        "f$cc_hand_pair_or_better Return true",
        "f$cc_flop_float_premium_draw Return true",
        "f$cc_flop_float_good_draw Return true",
        "f$cc_flop_float_husb_air_family Return true",
    ):
        assert token in flop_action
    assert block(HUSB, "f$cc_turn_delayed_float_husb_source_action").strip() == "false"
    assert block(HUSB, "f$cc_turn_delayed_float_husb_source_size_id").strip() == "0"
    assert "f$cc_turn_delayed_float_husb_source_mismatch" in ROUTER


def run_srp_contract() -> None:
    ctx = block(SRP, "f$cc_turn_delayed_float_srp6_context")
    for token in (
        "f$cc_turn_delayed_float_gate04_checkback_valid",
        "f$cc_turn_delayed_float_gate04_family_id = 2",
        "f$cc_deal_size >= 4",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
    ):
        assert token in ctx

    hu = block(SRP, "f$cc_turn_delayed_float_srp6_hu_action")
    assert "f$cc_turn_delayed_float_two_pair_plus_real Return true" in hu
    assert "f$cc_turn_delayed_float_tpop_real && f$cc_turn_delayed_float_thin_value_runout Return true" in hu
    assert "f$cc_turn_delayed_float_srp6_hu_secondpair_thin Return true" in hu
    assert "f$cc_turn_delayed_float_semibluff_candidate Return true" in hu
    assert "f$cc_turn_delayed_float_srp6_hu_air_bluff Return true" in hu

    thin = block(SRP, "f$cc_turn_delayed_float_srp6_hu_secondpair_thin")
    assert "f$cc_turn_delayed_float_flop_had_lower_pair" in thin
    assert "f$cc_turn_undercard" in thin

    bluff = block(SRP, "f$cc_turn_delayed_float_srp6_hu_air_bluff")
    assert "f$cc_turn_delayed_float_flop_had_air" in bluff
    assert "f$cc_turn_delayed_float_bluff_pressure_card" in bluff

    mw = block(SRP, "f$cc_turn_delayed_float_srp6_mw_action")
    assert "f$cc_turn_delayed_float_srp6_exact_threeway" in mw
    assert "f$cc_real_combo_draw" in mw
    assert "air_bluff" not in mw
    assert "When Others Return false Force" in mw


def run_iso_contract() -> None:
    ctx = block(ISO, "f$cc_turn_delayed_float_iso_context")
    for token in (
        "f$cc_turn_delayed_float_gate04_family_id = 3",
        "f$cc_pf_iso_proven",
        "f$cc_flop_float_iso_hero_provenance_consistent",
    ):
        assert token in ctx

    assert "f$cc_flop_float_iso_hero_was_limper" in block(ISO, "f$cc_turn_delayed_float_iso_hu_limper")
    assert "f$cc_flop_float_iso_hero_was_postraise_coldcaller" in block(ISO, "f$cc_turn_delayed_float_iso_hu_coldcaller")

    limper = block(ISO, "f$cc_turn_delayed_float_iso_limper_action")
    cold = block(ISO, "f$cc_turn_delayed_float_iso_coldcaller_action")
    assert "f$cc_turn_delayed_float_iso_limper_secondpair_thin Return true" in limper
    assert "f$cc_turn_delayed_float_iso_limper_air_bluff Return true" in limper
    assert "air_bluff" not in cold
    assert "secondpair_thin" not in cold
    assert "f$cc_turn_delayed_float_semibluff_candidate Return true" in cold

    mw = block(ISO, "f$cc_turn_delayed_float_iso_mw_action")
    assert "f$cc_turn_delayed_float_iso_exact_threeway" in mw
    assert "f$cc_real_combo_draw" in mw
    assert "air_bluff" not in mw


def run_safety_contract() -> None:
    executable = "\n".join(
        line
        for text in (HUSB, SRP, ISO)
        for line in text.splitlines()
        if not line.lstrip().startswith("//")
    )
    for forbidden in ("HandPower", "Random", "random", "BetMax", "Allin", "allin"):
        assert forbidden not in executable, f"forbidden generic token: {forbidden}"

    family = block(ROUTER, "f$cc_turn_delayed_float_family_id")
    for pair in (
        ("f$cc_turn_delayed_float_srp6_hu_context", "Return 2"),
        ("f$cc_turn_delayed_float_srp6_mw_context", "Return 3"),
        ("f$cc_turn_delayed_float_iso_hu_limper", "Return 4"),
        ("f$cc_turn_delayed_float_iso_hu_coldcaller", "Return 5"),
        ("f$cc_turn_delayed_float_iso_mw_context", "Return 6"),
    ):
        assert pair[0] in family and pair[1] in family


if __name__ == "__main__":
    run_common_contract()
    run_husb_negative_contract()
    run_srp_contract()
    run_iso_contract()
    run_safety_contract()
    print("PASS: Gate12B HUSB boundary + six-max SRP/ISO contracts")
