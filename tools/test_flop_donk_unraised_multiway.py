#!/usr/bin/env python3
"""Gate07H residual unraised current-multiway Flop Donk contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_Unraised_Multiway.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Flop_Donk.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def ownership_contract() -> None:
    ctx = block(POL, "f$cc_flop_donk_unraised_mw_context")
    for token in (
        "f$cc_flop_donk_opportunity",
        "f$cc_multiway",
        "f$cc_flop_entry_count >= 3",
        "f$cc_pot_family_id = 1",
        "f$cc_pf_raise_count = 0",
        "f$cc_pf_role_unraised_caller || f$cc_pf_role_bb_check",
        "!f$cc_flop_donk_source_covered",
        "!f$cc_flop_donk_6max_covered",
    ):
        assert token in ctx

    three = block(POL, "f$cc_flop_donk_unraised_threeway_context")
    four = block(POL, "f$cc_flop_donk_unraised_fourplus_context")
    assert "nplayersplaying = 3" in three
    assert "nplayersplaying >= 4" in four


def policy_contract() -> None:
    three = block(POL, "f$cc_flop_donk_unraised_threeway_action")
    for token in (
        "f$cc_flop_donk_unraised_robust_value Return true Force",
        "f$cc_flop_donk_unraised_threeway_overpair_lead Return true Force",
        "f$cc_flop_donk_unraised_threeway_strongtp_lead Return true Force",
        "f$cc_hand_middle_or_bottom_pair Return false Force",
        "f$cc_flop_donk_unraised_threeway_draw_lead Return true Force",
        "When Others Return false Force",
    ):
        assert token in three

    four = block(POL, "f$cc_flop_donk_unraised_fourplus_action")
    assert "f$cc_flop_donk_unraised_robust_value Return true Force" in four
    assert "f$cc_hand_top_pair_or_better Return false Force" in four
    assert "f$cc_hand_middle_or_bottom_pair Return false Force" in four
    assert "f$cc_flop_donk_unraised_fourplus_draw_lead Return true Force" in four
    # Four-plus policy must not acquire ordinary premium/good-draw positive branches.
    assert "f$cc_cbet_flop_premium_draw Return true Force" not in four
    assert "f$cc_cbet_flop_good_draw Return true Force" not in four

    draw4 = block(POL, "f$cc_flop_donk_unraised_fourplus_draw_lead")
    assert "f$cc_nut_or_combo_draw" in draw4
    assert "f$cc_hand_no_made" in draw4


def stack_and_safety_contract() -> None:
    spr = executable(block(POL, "f$cc_flop_donk_unraised_drawheavy_low_spr"))
    assert "f$cc_mw_spr_deepest_round_start" in spr
    assert "<= 1.25" in spr
    assert "shallowest" not in spr.lower()

    size = block(POL, "f$cc_flop_donk_unraised_mw_size_id")
    for line in size.splitlines():
        if "f$cc_flop_donk_size_100_id" in line:
            assert "f$cc_flop_donk_unraised_robust_value" in line

    code = executable(POL)
    for forbidden in (
        "BetMax",
        "HandPower",
        "random",
        "Raise_Committed",
        "StackOffDraws",
        "f$cc_cbet_flop_quality_air",
        "f$cc_cbet_flop_pure_air",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate07H leak: {forbidden}"


def router_contract() -> None:
    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_unraised_mw_covered Return 7 Force" in family

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_unraised_mw_covered Return f$cc_flop_donk_unraised_mw_action Force" in router

    size = block(ROUTER, "f$cc_flop_donk_size_id")
    assert "f$cc_flop_donk_unraised_mw_covered Return f$cc_flop_donk_unraised_mw_size_id Force" in size

    covered = block(ROUTER, "f$cc_flop_donk_strategy_covered")
    assert "f$cc_flop_donk_unraised_mw_covered" in covered


if __name__ == "__main__":
    ownership_contract()
    policy_contract()
    stack_and_safety_contract()
    router_contract()
    print("PASS: Gate07H residual unraised multiway Flop Donk contract")
