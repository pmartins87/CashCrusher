#!/usr/bin/env python3
"""Gate10D native true-multiway Turn-Probe reviewed-gap contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MW = (ROOT / "src" / "CashCrusher_Turn_Probe_Multiway_SourceGaps.txt").read_text(encoding="utf-8")
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


def context_contract() -> None:
    ctx = block(MW, "f$cc_turn_probe_mw_gap_context")
    assert "f$cc_turn_probe_3w_blinds_vbtn_context" in ctx
    assert "!f$cc_turn_probe_3w_mw_covered" in ctx

    direct = block(SRC, "f$cc_turn_probe_3w_mw_covered")
    assert "f$cc_turn_probe_3w_mw_second_pair_probe" in direct
    assert "f$cc_turn_probe_3w_mw_low_pair_check" in direct


def provenance_contract() -> None:
    value = block(MW, "f$cc_turn_probe_mw_gap_flop_valuecheck_axx")
    assert "f$cc_turn_probe_flop_had_tpplus" in value
    assert "user_cc_turn_probe_flop_was_ahigh" in value
    assert "user_cc_turn_probe_flop_was_ahigh" in SNAP

    draw = block(MW, "f$cc_turn_probe_mw_gap_flop_drawcheck")
    assert "f$cc_turn_probe_flop_had_frontdoor_draw" in draw
    assert "f$cc_turn_probe_flop_had_frontdoor_draw" in SNAP


def action_contract() -> None:
    value = block(MW, "f$cc_turn_probe_mw_gap_value_probe")
    assert "f$cc_turn_probe_mw_gap_flop_valuecheck_axx" in value
    assert "f$cc_turn_probe_tpplus" in value

    draw = block(MW, "f$cc_turn_probe_mw_gap_draw_probe")
    assert "f$cc_turn_probe_mw_gap_flop_drawcheck" in draw
    assert "f$cc_turn_probe_live_frontdoor_draw" in draw

    covered = block(MW, "f$cc_turn_probe_mw_gap_covered")
    assert "f$cc_turn_probe_mw_gap_value_probe" in covered
    assert "f$cc_turn_probe_mw_gap_draw_probe" in covered
    assert "air" not in executable(covered).lower()

    router = block(MW, "f$cc_turn_probe_mw_gap_action")
    assert "f$cc_turn_probe_mw_gap_value_probe Return true Force" in router
    assert "f$cc_turn_probe_mw_gap_draw_probe Return true Force" in router
    assert "When Others Return false Force" in router


def sizing_contract() -> None:
    size = block(MW, "f$cc_turn_probe_mw_gap_size_id")
    assert "When PotSize > 3 Return f$cc_turn_probe_size_33_id Force" in size
    assert "When PotSize <= 3 Return f$cc_turn_probe_size_50_id Force" in size
    assert "##f$cc_turn_probe_size_33_id##" in COMMON
    assert "##f$cc_turn_probe_size_50_id##" in COMMON

    consistency = block(MW, "f$cc_turn_probe_mw_gap_size_consistent")
    assert "f$cc_turn_probe_size_33_id" in consistency
    assert "f$cc_turn_probe_size_50_id" in consistency


def safety_contract() -> None:
    uncovered = block(MW, "f$cc_turn_probe_mw_gap_uncovered_context")
    assert "f$cc_turn_probe_mw_gap_context" in uncovered
    assert "!f$cc_turn_probe_mw_gap_covered" in uncovered

    code = executable(MW).lower()
    for forbidden in (
        "betmax",
        "raise_committed",
        "random",
        "handpower",
        "user_river",
        "user_turn",
        "f$game_",
        "effectivestack",
        "shallowest",
    ):
        assert forbidden not in code, f"forbidden Gate10D executable leak: {forbidden}"


if __name__ == "__main__":
    context_contract()
    provenance_contract()
    action_contract()
    sizing_contract()
    safety_contract()
    print("PASS: Gate10D native multiway Turn-Probe reviewed-gap contract")
