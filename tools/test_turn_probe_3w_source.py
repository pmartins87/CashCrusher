#!/usr/bin/env python3
"""Gate10B.2 native 3-handed Turn Probe source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = (ROOT / "src" / "CashCrusher_Turn_Probe_3W_Source.txt").read_text(encoding="utf-8")
SNAP = (ROOT / "src" / "CashCrusher_Turn_Probe_Snapshot.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_Turn_Probe_Common.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def exact_context_contract() -> None:
    sb = block(SRC, "f$cc_turn_probe_3w_sbvbtn_context")
    for token in (
        "f$cc_turn_probe_hu_opportunity",
        "f$cc_turn_probe_snapshot_valid",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 5",
        "f$cc_hu_villain_pos_id = 4",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = 4",
    ):
        assert token in sb

    bb = block(SRC, "f$cc_turn_probe_3w_bbvbtn_context")
    assert "f$cc_hero_pos_id = 6" in bb
    assert "f$cc_hu_villain_pos_id = 4" in bb
    assert "f$cc_pot_family_id = 2" in bb

    mw = block(SRC, "f$cc_turn_probe_3w_blinds_vbtn_context")
    for token in (
        "f$cc_turn_probe_multiway_opportunity",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 3",
        "nplayersplaying = 3",
        "f$cc_pot_family_id = 1 || f$cc_pot_family_id = 2",
        "f$cc_hero_pos_id = 5 && f$cc_opp_live_mask = 40",
        "f$cc_hero_pos_id = 6 && f$cc_opp_live_mask = 24",
    ):
        assert token in mw


def sbvbtn_contract() -> None:
    pos = block(SRC, "f$cc_turn_probe_3w_sbvbtn_tpplus_probe")
    assert "f$cc_turn_probe_flop_had_tpplus" in pos
    assert "f$cc_turn_probe_tpplus" in pos

    size = block(SRC, "f$cc_turn_probe_3w_sbvbtn_size_id")
    assert "f$cc_turn_probe_size_100_id" in size

    # Source silence must NOT turn whole positional context into reviewed check.
    cov = executable(block(SRC, "f$cc_turn_probe_3w_sbvbtn_covered"))
    assert "f$cc_turn_probe_3w_sbvbtn_tpplus_probe" in cov
    assert "f$cc_turn_probe_3w_sbvbtn_context" not in cov


def bbvbtn_contract() -> None:
    bad = block(SRC, "f$cc_turn_probe_3w_bbvbtn_air_bad_board")
    assert "PairOnBoard" in bad
    assert "user_cc_turn_probe_flop_had_2plusbw" in bad
    assert "user_cc_turn_probe_flop_had_1bw && f$cc_turn_is_broadway" in bad

    pos = block(SRC, "f$cc_turn_probe_3w_bbvbtn_air_probe")
    assert "f$cc_turn_probe_flop_had_air" in pos
    assert "f$cc_turn_probe_air" in pos
    assert "!f$cc_turn_probe_3w_bbvbtn_air_bad_board" in pos

    size = block(SRC, "f$cc_turn_probe_3w_bbvbtn_size_id")
    assert "f$cc_turn_probe_size_75_id" in size

    cov = executable(block(SRC, "f$cc_turn_probe_3w_bbvbtn_covered"))
    assert "f$cc_turn_probe_3w_bbvbtn_air_probe" in cov
    assert "f$cc_turn_probe_3w_bbvbtn_context" not in cov


def multiway_contract() -> None:
    second = block(SRC, "f$cc_turn_probe_3w_mw_second_pair_probe")
    assert "f$cc_turn_probe_second_pair" in second
    low = block(SRC, "f$cc_turn_probe_3w_mw_low_pair_check")
    assert "f$cc_turn_probe_low_pair" in low

    action = block(SRC, "f$cc_turn_probe_3w_mw_action")
    assert "f$cc_turn_probe_3w_mw_second_pair_probe Return true Force" in action
    assert "f$cc_turn_probe_3w_mw_low_pair_check Return false Force" in action

    size = block(SRC, "f$cc_turn_probe_3w_mw_size_id")
    assert "f$cc_turn_probe_size_50_id" in size

    cov = block(SRC, "f$cc_turn_probe_3w_mw_covered")
    assert "f$cc_turn_probe_3w_mw_second_pair_probe" in cov
    assert "f$cc_turn_probe_3w_mw_low_pair_check" in cov
    # No source-silent air/draw expansion.
    assert "f$cc_turn_probe_air" not in executable(cov)
    assert "f$cc_turn_probe_live_frontdoor_draw" not in executable(cov)


def snapshot_and_safety_contract() -> None:
    for flag in (
        "user_cc_turn_probe_flop_had_tpplus",
        "user_cc_turn_probe_flop_had_air",
        "user_cc_turn_probe_flop_had_1bw",
        "user_cc_turn_probe_flop_had_2plusbw",
    ):
        assert flag in SNAP

    for size_symbol in (
        "f$cc_turn_probe_size_50_id",
        "f$cc_turn_probe_size_75_id",
        "f$cc_turn_probe_size_100_id",
    ):
        assert size_symbol in COMMON

    code = executable(SRC).lower()
    for forbidden in (
        "betmax",
        "raise_committed",
        "random",
        "handpower",
        "user_turn",
        "f$game_",
        "f$effectiveStack_bkp".lower(),
    ):
        assert forbidden.lower() not in code, f"forbidden direct-source leak: {forbidden}"

    dispatch = block(SRC, "f$cc_turn_probe_3w_source_action")
    assert "When Others Return false Force" in dispatch
    consistency = block(SRC, "f$cc_turn_probe_3w_source_size_consistent")
    assert "f$cc_turn_probe_3w_source_size_id = 0" in consistency


if __name__ == "__main__":
    exact_context_contract()
    sbvbtn_contract()
    bbvbtn_contract()
    multiway_contract()
    snapshot_and_safety_contract()
    print("PASS: Gate10B.2 native 3-handed Turn Probe source contract")
