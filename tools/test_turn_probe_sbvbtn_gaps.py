#!/usr/bin/env python3
"""Gate10C 3wSBvBTN reviewed TBP Turn-Probe gap contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAP = (ROOT / "src" / "CashCrusher_Turn_Probe_SBVBTN_Gaps.txt").read_text(encoding="utf-8")
SRC = (ROOT / "src" / "CashCrusher_Turn_Probe_3W_Source.txt").read_text(encoding="utf-8")
SNAP = (ROOT / "src" / "CashCrusher_Turn_Probe_Snapshot.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_Turn_Probe_Common.txt").read_text(encoding="utf-8")
TURN_TEX = (ROOT / "src" / "CashCrusher_Turn_Texture.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def precedence_contract() -> None:
    ctx = block(GAP, "f$cc_turn_probe_sbvbtn_gap_context")
    assert "f$cc_turn_probe_3w_sbvbtn_context" in ctx
    assert "!f$cc_turn_probe_3w_sbvbtn_covered" in ctx

    direct = block(SRC, "f$cc_turn_probe_3w_sbvbtn_covered")
    assert "f$cc_turn_probe_3w_sbvbtn_tpplus_probe" in direct


def bad_board_contract() -> None:
    ace = block(GAP, "f$cc_turn_probe_sbvbtn_board_has_ace")
    assert "AcePresentOnFlop" in ace
    assert "f$cc_turn_is_ace" in ace

    bw = block(GAP, "f$cc_turn_probe_sbvbtn_board_2plus_bw")
    assert "user_cc_turn_probe_flop_had_2plusbw" in bw
    assert "user_cc_turn_probe_flop_had_1bw && f$cc_turn_is_broadway" in bw
    assert "user_cc_turn_probe_flop_had_1bw" in SNAP
    assert "user_cc_turn_probe_flop_had_2plusbw" in SNAP

    bad = block(GAP, "f$cc_turn_probe_sbvbtn_bad_bluff_turn")
    assert "PairOnBoard" in bad
    assert "f$cc_turn_probe_sbvbtn_board_has_ace" in bad
    assert "f$cc_turn_probe_sbvbtn_board_2plus_bw" in bad

    new_flush = block(GAP, "f$cc_turn_probe_sbvbtn_new_flush_completion")
    assert "f$cc_turn_new_flush_completion" in new_flush
    assert "##f$cc_turn_new_flush_completion##" in TURN_TEX


def action_contract() -> None:
    bad_air = block(GAP, "f$cc_turn_probe_sbvbtn_gap_air_bad_check")
    assert "f$cc_turn_probe_sbvbtn_bad_bluff_turn" in bad_air
    assert "f$cc_turn_probe_air" in bad_air

    good = block(GAP, "f$cc_turn_probe_sbvbtn_gap_nomade_good_probe")
    assert "!f$cc_turn_probe_sbvbtn_bad_bluff_turn" in good
    assert "f$cc_hand_no_made" in good

    assert "f$cc_hand_two_pair_or_better" in block(GAP, "f$cc_turn_probe_sbvbtn_gap_twoplus")

    tpop = block(GAP, "f$cc_turn_probe_sbvbtn_gap_tpop")
    assert "f$cc_turn_probe_tpplus" in tpop
    assert "!f$cc_hand_two_pair_or_better" in tpop

    second50 = block(GAP, "f$cc_turn_probe_sbvbtn_gap_secondpair_flush50")
    assert "f$cc_turn_probe_second_pair" in second50
    assert "f$cc_turn_probe_sbvbtn_new_flush_completion" in second50
    assert "!f$cc_turn_pairs_flop_rank" in second50

    thirdcheck = block(GAP, "f$cc_turn_probe_sbvbtn_gap_thirdpair_flush_check")
    assert "f$cc_turn_probe_sbvbtn_gap_third_pair" in thirdcheck
    assert "f$cc_turn_probe_sbvbtn_new_flush_completion" in thirdcheck


def size_contract() -> None:
    size = block(GAP, "f$cc_turn_probe_sbvbtn_gap_size_id")
    for token in (
        "f$cc_turn_probe_sbvbtn_gap_nomade_good_probe Return f$cc_turn_probe_size_75_id Force",
        "f$cc_turn_probe_sbvbtn_gap_twoplus_probe Return f$cc_turn_probe_size_100_id Force",
        "f$cc_turn_probe_sbvbtn_gap_tpop_flush_probe Return f$cc_turn_probe_size_75_id Force",
        "f$cc_turn_probe_sbvbtn_gap_tpop_pot_probe Return f$cc_turn_probe_size_100_id Force",
        "f$cc_turn_probe_sbvbtn_gap_secondpair_flush50 Return f$cc_turn_probe_size_50_id Force",
        "f$cc_turn_probe_sbvbtn_gap_secondpair_75 Return f$cc_turn_probe_size_75_id Force",
        "f$cc_turn_probe_sbvbtn_gap_thirdpair_33 Return f$cc_turn_probe_size_33_id Force",
    ):
        assert token in size

    # Direct source PSB remains separate and higher ancestry.
    direct_size = block(SRC, "f$cc_turn_probe_3w_sbvbtn_size_id")
    assert "f$cc_turn_probe_size_100_id" in direct_size

    for symbol in (
        "f$cc_turn_probe_size_33_id",
        "f$cc_turn_probe_size_50_id",
        "f$cc_turn_probe_size_75_id",
        "f$cc_turn_probe_size_100_id",
    ):
        assert f"##{symbol}##" in COMMON


def residual_and_safety_contract() -> None:
    residual = block(GAP, "f$cc_turn_probe_sbvbtn_gap_residual_needs_size_audit")
    assert "f$cc_turn_probe_sbvbtn_gap_context" in residual
    assert "!f$cc_turn_probe_sbvbtn_gap_covered" in residual

    # Never turn the final DeepCrusher normal-sizing catch-all into an invented
    # fixed size before its exact owner is audited.
    covered = executable(block(GAP, "f$cc_turn_probe_sbvbtn_gap_covered"))
    assert "residual_needs_size_audit" not in covered

    code = executable(GAP).lower()
    for forbidden in (
        "betmax",
        "raise_committed",
        "random",
        "handpower",
        "user_river",
        "f$game_",
        "f$board_badtobluffturn",
        "f$effectivestack",
    ):
        assert forbidden not in code, f"forbidden Gate10C executable leak: {forbidden}"

    action = block(GAP, "f$cc_turn_probe_sbvbtn_gap_action")
    assert "f$cc_turn_probe_sbvbtn_gap_air_bad_check Return false Force" in action
    assert "f$cc_turn_probe_sbvbtn_gap_thirdpair_flush_check Return false Force" in action
    assert "When Others Return false Force" in action


if __name__ == "__main__":
    precedence_contract()
    bad_board_contract()
    action_contract()
    size_contract()
    residual_and_safety_contract()
    print("PASS: Gate10C 3wSBvBTN reviewed TBP Turn-Probe gap contract")
