#!/usr/bin/env python3
"""Gate10G isolation-pot Turn-Probe contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ISO = (ROOT / "src" / "CashCrusher_Turn_Probe_ISO.txt").read_text(encoding="utf-8")


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
    limper = block(ISO, "f$cc_turn_probe_iso_hero_was_limper")
    cold = block(ISO, "f$cc_turn_probe_iso_hero_was_postraise_coldcaller")
    assert "f$cc_pf_pre_raise_limper_mask" in limper
    assert "f$cc_pf_post_raise_coldcaller_mask" in cold

    consistent = block(ISO, "f$cc_turn_probe_iso_hero_origin_consistent")
    assert "f$cc_turn_probe_iso_hero_was_limper && f$cc_turn_probe_iso_hero_was_postraise_coldcaller Return false Force" in consistent

    ctx = block(ISO, "f$cc_turn_probe_iso_context")
    for token in (
        "f$cc_turn_probe_base_opportunity",
        "f$cc_turn_probe_snapshot_valid",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_iso_proven",
        "f$cc_pf_role_srp_caller",
        "f$cc_turn_probe_iso_hero_origin_consistent",
    ):
        assert token in ctx


def field_contract() -> None:
    live = block(ISO, "f$cc_turn_probe_iso_raiser_live")
    for pos, bit in ((1,1),(2,2),(3,4),(4,8),(5,16),(6,32)):
        assert f"f$cc_pf_single_raiser_pos_id = {pos}" in live
        assert f"BitAnd {bit}" in live

    limper_hu = block(ISO, "f$cc_turn_probe_iso_hu_limper_context")
    cold_hu = block(ISO, "f$cc_turn_probe_iso_hu_coldcaller_context")
    for b in (limper_hu, cold_hu):
        assert "f$cc_turn_probe_hu_opportunity" in b
        assert "f$cc_hu_origin_preflop_reduced" in b
        assert "f$cc_hu_villain_pos_id = f$cc_pf_single_raiser_pos_id" in b

    mw = block(ISO, "f$cc_turn_probe_iso_multiway_context")
    assert "f$cc_turn_probe_multiway_opportunity" in mw
    assert "f$cc_turn_probe_iso_raiser_live" in mw


def policy_contract() -> None:
    limper = block(ISO, "f$cc_turn_probe_iso_hu_limper_action")
    cold = block(ISO, "f$cc_turn_probe_iso_hu_coldcaller_action")
    mw = block(ISO, "f$cc_turn_probe_iso_multiway_action")

    assert "f$cc_turn_probe_iso_limper_selected_air Return true Force" in limper
    assert "f$cc_turn_probe_air Return false Force" in cold
    assert "f$cc_turn_probe_air Return false Force" in mw
    assert "nplayersplaying = 3 && f$cc_turn_probe_iso_strong_tp" in mw
    assert "nplayersplaying >= 4 && f$cc_real_combo_draw" in mw

    selected = block(ISO, "f$cc_turn_probe_iso_limper_selected_air")
    for token in (
        "f$cc_turn_probe_iso_late_raiser",
        "f$cc_turn_probe_flop_had_air",
        "f$cc_turn_probe_flop_had_backdoor",
        "f$cc_turn_probe_air",
        "!f$cc_turn_probe_iso_bad_bluff_turn",
    ):
        assert token in selected


def coverage_safety_contract() -> None:
    covered = block(ISO, "f$cc_turn_probe_iso_covered")
    assert "f$cc_turn_probe_iso_hu_limper_context" in covered
    assert "f$cc_turn_probe_iso_hu_coldcaller_context" in covered
    assert "f$cc_turn_probe_iso_multiway_context" in covered

    uncovered = block(ISO, "f$cc_turn_probe_iso_uncovered_context")
    assert "f$cc_pf_iso_proven" in uncovered
    assert "!f$cc_turn_probe_iso_covered" in uncovered

    consistency = block(ISO, "f$cc_turn_probe_iso_size_consistent")
    assert "f$cc_turn_probe_iso_size_id >= 1 && f$cc_turn_probe_iso_size_id <= 7" in consistency

    code = executable(ISO).lower()
    for forbidden in (
        "betmax",
        "raise_committed",
        "random",
        "handpower",
        "effectivestack",
        "shallowest",
        "user_river",
        "user_turn",
        "f$game_",
    ):
        assert forbidden not in code, f"forbidden Gate10G executable leak: {forbidden}"


if __name__ == "__main__":
    provenance_contract()
    field_contract()
    policy_contract()
    coverage_safety_contract()
    print("PASS: Gate10G isolation-pot Turn-Probe contract")
