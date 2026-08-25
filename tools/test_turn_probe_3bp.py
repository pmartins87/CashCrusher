#!/usr/bin/env python3
"""Gate10H plain-3BP/squeeze Turn-Probe contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_Probe_3BP.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def origin_contract() -> None:
    opener = block(POL, "f$cc_turn_probe_3bp_hero_is_opener_call")
    assert "f$cc_pf_role_open_call_3bet" in opener
    assert "f$cc_hero_pos_id = f$cc_pf_3bet_first_raiser_pos_id" in opener

    pre = block(POL, "f$cc_turn_probe_3bp_hero_is_pre3bet_coldcaller")
    assert "f$cc_pf_role_cold_call_3bet" in pre
    assert "f$cc_pf_squeeze_proven" in pre
    assert "f$cc_pf_pre3bet_coldcaller_mask" in pre

    post = block(POL, "f$cc_turn_probe_3bp_hero_is_post3bet_coldcaller")
    assert "f$cc_pf_role_cold_call_3bet" in post
    assert "f$cc_pf_post3bet_coldcaller_mask" in post

    consistent = block(POL, "f$cc_turn_probe_3bp_hero_origin_consistent")
    assert "f$cc_turn_probe_3bp_hero_is_opener_call && (f$cc_turn_probe_3bp_hero_is_pre3bet_coldcaller || f$cc_turn_probe_3bp_hero_is_post3bet_coldcaller) Return false Force" in consistent
    assert "f$cc_turn_probe_3bp_hero_is_pre3bet_coldcaller && f$cc_turn_probe_3bp_hero_is_post3bet_coldcaller Return false Force" in consistent


def ownership_contract() -> None:
    ctx = block(POL, "f$cc_turn_probe_3bp_context")
    for token in (
        "f$cc_turn_probe_base_opportunity",
        "f$cc_turn_probe_snapshot_valid",
        "f$cc_pot_family_id = 3",
        "f$cc_pf_3bet_order_supported",
        "f$cc_turn_probe_3bp_hero_origin_consistent",
        "f$cc_turn_probe_3bp_final_raiser_live",
    ):
        assert token in ctx

    hu = block(POL, "f$cc_turn_probe_3bp_hu_context")
    assert "f$cc_hu_origin_preflop_reduced" in hu
    assert "f$cc_hu_villain_pos_id = f$cc_pf_3bet_final_raiser_pos_id" in hu

    assert "f$cc_pf_3bet_plain_proven" in block(POL, "f$cc_turn_probe_plain3bp_opener_hu_context")
    assert "f$cc_pf_3bet_plain_proven" in block(POL, "f$cc_turn_probe_plain3bp_postcold_hu_context")
    assert "f$cc_pf_squeeze_proven" in block(POL, "f$cc_turn_probe_squeeze_opener_hu_context")
    assert "f$cc_pf_squeeze_proven" in block(POL, "f$cc_turn_probe_squeeze_precold_hu_context")
    assert "f$cc_pf_squeeze_proven" in block(POL, "f$cc_turn_probe_squeeze_postcold_hu_context")


def policy_contract() -> None:
    opener = block(POL, "f$cc_turn_probe_plain3bp_opener_hu_action")
    assert "f$cc_hand_two_pair_or_better Return true Force" in opener
    assert "f$cc_turn_probe_3bp_overpair Return true Force" in opener
    assert "f$cc_turn_probe_3bp_strong_tp && f$cc_turn_probe_3bp_favorable_turn Return true Force" in opener
    assert "f$cc_turn_probe_air Return false Force" in opener

    cold = block(POL, "f$cc_turn_probe_3bp_coldcaller_hu_action")
    assert "f$cc_turn_probe_3bp_strong_tp Return false Force" in cold
    assert "f$cc_turn_probe_air Return false Force" in cold
    assert "f$cc_turn_probe_3bp_premium_draw && f$cc_turn_probe_3bp_favorable_turn Return true Force" in cold

    squeeze = block(POL, "f$cc_turn_probe_squeeze_opener_hu_action")
    assert "f$cc_turn_probe_3bp_strong_tp && f$cc_turn_probe_3bp_favorable_turn Return true Force" in squeeze
    assert "f$cc_turn_probe_air Return false Force" in squeeze

    mw = block(POL, "f$cc_turn_probe_3bp_multiway_action")
    assert "nplayersplaying = 3 && f$cc_turn_probe_3bp_hero_is_opener_call && f$cc_turn_probe_3bp_overpair" in mw
    assert "nplayersplaying >= 4 && f$cc_real_combo_draw" in mw
    assert "f$cc_turn_probe_air Return false Force" in mw


def coverage_and_safety_contract() -> None:
    covered = block(POL, "f$cc_turn_probe_3bp_covered")
    for token in (
        "f$cc_turn_probe_plain3bp_opener_hu_context",
        "f$cc_turn_probe_plain3bp_postcold_hu_context",
        "f$cc_turn_probe_squeeze_opener_hu_context",
        "f$cc_turn_probe_squeeze_precold_hu_context",
        "f$cc_turn_probe_squeeze_postcold_hu_context",
        "f$cc_turn_probe_3bp_multiway_context",
    ):
        assert token in covered

    uncovered = block(POL, "f$cc_turn_probe_3bp_uncovered_context")
    assert "f$cc_pot_family_id = 3" in uncovered
    assert "!f$cc_turn_probe_3bp_covered" in uncovered

    size = block(POL, "f$cc_turn_probe_3bp_size_consistent")
    assert "f$cc_turn_probe_3bp_size_id >= 1 && f$cc_turn_probe_3bp_size_id <= 7" in size

    code = executable(POL).lower()
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
        assert forbidden not in code, f"forbidden Gate10H executable leak: {forbidden}"


if __name__ == "__main__":
    origin_contract()
    ownership_contract()
    policy_contract()
    coverage_and_safety_contract()
    print("PASS: Gate10H plain-3BP/squeeze Turn-Probe contract")
