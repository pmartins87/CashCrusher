#!/usr/bin/env python3
"""Gate10I clean caller-side 4BP Turn-Probe contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_Probe_4BP.txt").read_text(encoding="utf-8")


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
    other = block(POL, "f$cc_turn_probe_4bp_other_raiser_pos_id")
    for token in (
        "f$cc_pf_raise_count != 3",
        "!f$cc_pf_role_call_4bet",
        "!f$cc_pf_hero_ever_raised",
        "f$cc_pf_unique_raiser_count != 2",
    ):
        assert token in other

    proven = block(POL, "f$cc_turn_probe_4bp_opener4_vs_hero3bettor_proven")
    assert "f$cc_pf_role_call_4bet" in proven
    assert "f$cc_pf_hero_ever_raised" in proven
    assert "f$cc_turn_probe_4bp_other_raiser_pos_id < f$cc_hero_pos_id" in proven


def ownership_contract() -> None:
    ctx = block(POL, "f$cc_turn_probe_4bp_clean_hu_context")
    for token in (
        "f$cc_turn_probe_hu_opportunity",
        "f$cc_turn_probe_snapshot_valid",
        "f$cc_pot_family_id = 4",
        "f$cc_turn_probe_4bp_opener4_vs_hero3bettor_proven",
        "f$cc_hu_villain_pos_id = f$cc_turn_probe_4bp_other_raiser_pos_id",
        "f$cc_hu_oop",
    ):
        assert token in ctx

    truehu = block(POL, "f$cc_turn_probe_4bp_true_hu_context")
    assert "f$cc_true_hu" in truehu
    assert "f$cc_hero_pos_id = 6" in truehu
    assert "f$cc_hu_villain_pos_id = 5" in truehu

    reduced = block(POL, "f$cc_turn_probe_4bp_reduced_hu_context")
    assert "f$cc_hu_origin_preflop_reduced" in reduced


def policy_contract() -> None:
    action = block(POL, "f$cc_turn_probe_4bp_action")
    assert "f$cc_hand_two_pair_or_better Return true Force" in action
    assert "f$cc_turn_probe_4bp_overpair && !f$cc_turn_probe_4bp_bad_pressure_turn Return true Force" in action
    assert "f$cc_turn_probe_4bp_overpair && f$cc_turn_probe_4bp_hu_spr_below_2 Return true Force" in action
    assert "f$cc_turn_probe_4bp_strong_tp && !f$cc_turn_probe_4bp_bad_pressure_turn Return true Force" in action
    assert "f$cc_turn_probe_second_pair Return false Force" in action
    assert "f$cc_turn_probe_air Return false Force" in action

    spr = block(POL, "f$cc_turn_probe_4bp_hu_spr_below_2")
    assert "f$cc_spr_round_start" in spr
    assert "< 2" in spr


def safety_contract() -> None:
    covered = block(POL, "f$cc_turn_probe_4bp_covered")
    assert "f$cc_turn_probe_4bp_clean_hu_context" in covered

    uncovered = block(POL, "f$cc_turn_probe_4bp_uncovered_context")
    assert "f$cc_pot_family_id = 4" in uncovered
    assert "!f$cc_turn_probe_4bp_covered" in uncovered

    consistency = block(POL, "f$cc_turn_probe_4bp_size_consistent")
    assert "f$cc_turn_probe_4bp_size_id >= 1 && f$cc_turn_probe_4bp_size_id <= 7" in consistency

    code = executable(POL).lower()
    for forbidden in (
        "betmax",
        "raise_committed",
        "random",
        "handpower",
        "shallowest",
        "user_river",
        "user_turn",
        "f$game_",
    ):
        assert forbidden not in code, f"forbidden Gate10I executable leak: {forbidden}"


if __name__ == "__main__":
    chronology_contract()
    ownership_contract()
    policy_contract()
    safety_contract()
    print("PASS: Gate10I clean caller-side 4BP Turn-Probe contract")
