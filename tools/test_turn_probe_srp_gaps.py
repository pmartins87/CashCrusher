#!/usr/bin/env python3
"""Gate10E ordinary-SRP OOP-caller Turn-Probe six-max gap contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAP = (ROOT / "src" / "CashCrusher_Turn_Probe_SRP_Gaps.txt").read_text(encoding="utf-8")
SRC = (ROOT / "src" / "CashCrusher_Turn_Probe_3W_Source.txt").read_text(encoding="utf-8")
SB = (ROOT / "src" / "CashCrusher_Turn_Probe_SBVBTN_Gaps.txt").read_text(encoding="utf-8")


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
    ctx = block(GAP, "f$cc_turn_probe_srp_hu_gap_context")
    for token in (
        "f$cc_turn_probe_hu_opportunity",
        "f$cc_turn_probe_snapshot_valid",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_hu_oop",
        "f$cc_hu_villain_pos_id = f$cc_pf_single_raiser_pos_id",
    ):
        assert token in ctx

    reserved = block(GAP, "f$cc_turn_probe_srp_native_sbvbtn_reserved")
    assert "f$cc_deal_size = 3" in reserved
    assert "f$cc_hero_pos_id = 5" in reserved
    assert "f$cc_pf_single_raiser_pos_id = 4" in reserved

    bb = block(GAP, "f$cc_turn_probe_srp_native_bbvbtn_gap")
    assert "f$cc_deal_size = 3" in bb
    assert "f$cc_hero_pos_id = 6" in bb
    assert "!f$cc_turn_probe_3w_bbvbtn_covered" in bb

    btn = block(GAP, "f$cc_turn_probe_srp_btn_6max_gap")
    assert "f$cc_deal_size >= 4" in btn and "f$cc_deal_size <= 6" in btn
    assert "f$cc_pf_single_raiser_pos_id = 4" in btn

    assert "f$cc_pf_single_raiser_pos_id = 3" in block(GAP, "f$cc_turn_probe_srp_co_gap")
    ep = block(GAP, "f$cc_turn_probe_srp_ep_gap")
    assert "f$cc_pf_single_raiser_pos_id = 1" in ep
    assert "f$cc_pf_single_raiser_pos_id = 2" in ep


def range_tightening_contract() -> None:
    btn = block(GAP, "f$cc_turn_probe_srp_btn_6max_action")
    co = block(GAP, "f$cc_turn_probe_srp_co_action")
    ep = block(GAP, "f$cc_turn_probe_srp_ep_action")

    assert "f$cc_turn_probe_srp_btn_selected_air Return true Force" in btn
    assert "f$cc_turn_probe_srp_btn_selected_air" not in executable(co)
    assert "f$cc_turn_probe_srp_btn_selected_air" not in executable(ep)
    assert "f$cc_turn_probe_air Return false Force" in co
    assert "f$cc_turn_probe_air Return false Force" in ep

    # EP stays value-heavy rather than inheriting BTN thin-value/draw pressure.
    assert "f$cc_turn_probe_srp_strong_tp Return false Force" in ep
    assert "f$cc_turn_probe_srp_premium_draw Return false Force" in ep

    selected_air = block(GAP, "f$cc_turn_probe_srp_btn_selected_air")
    for token in (
        "f$cc_hero_pos_id = 6",
        "f$cc_turn_probe_flop_had_air",
        "f$cc_turn_probe_flop_had_backdoor",
        "f$cc_turn_probe_air",
        "f$cc_turn_probe_srp_favorable_turn",
    ):
        assert token in selected_air


def source_precedence_contract() -> None:
    direct = block(SRC, "f$cc_turn_probe_3w_bbvbtn_covered")
    assert "f$cc_turn_probe_3w_bbvbtn_air_probe" in direct
    assert "!f$cc_turn_probe_3w_bbvbtn_covered" in block(
        GAP, "f$cc_turn_probe_srp_native_bbvbtn_gap"
    )

    # Native SBvBTN is reserved to direct source + reviewed TBP partition.
    assert "f$cc_turn_probe_sbvbtn_gap_covered" in SB
    gapctx = block(GAP, "f$cc_turn_probe_srp_gap_context")
    assert "f$cc_turn_probe_srp_native_sbvbtn_reserved Return false Force" in gapctx


def sizing_and_safety_contract() -> None:
    bad = block(GAP, "f$cc_turn_probe_srp_bad_bluff_turn")
    for token in (
        "PairOnBoard",
        "f$cc_turn_probe_srp_board_has_ace",
        "f$cc_turn_probe_srp_board_2plus_bw",
        "f$cc_turn_completed",
    ):
        assert token in bad

    size = block(GAP, "f$cc_turn_probe_srp_gap_size_id")
    for token in (
        "f$cc_turn_probe_srp_native_bbvbtn_size_id",
        "f$cc_turn_probe_srp_btn_6max_size_id",
        "f$cc_turn_probe_srp_co_size_id",
        "f$cc_turn_probe_srp_ep_size_id",
    ):
        assert token in size

    covered = block(GAP, "f$cc_turn_probe_srp_gap_covered")
    assert "f$cc_turn_probe_srp_gap_context" in covered

    code = executable(GAP).lower()
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
        assert forbidden not in code, f"forbidden Gate10E executable leak: {forbidden}"


if __name__ == "__main__":
    context_contract()
    range_tightening_contract()
    source_precedence_contract()
    sizing_and_safety_contract()
    print("PASS: Gate10E ordinary-SRP Turn-Probe six-max gaps")
