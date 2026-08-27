#!/usr/bin/env python3
"""Gate07C 4-6 handed BTN+both-blinds Flop Donk adaptation contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_BTNBlinds_6Max.txt").read_text(encoding="utf-8")
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


def context_separation_contract() -> None:
    limp = block(POL, "f$cc_flop_donk_6max_limped_context")
    srp = block(POL, "f$cc_flop_donk_6max_btnopen_context")
    assert "f$cc_pot_family_id = 1" in limp
    assert "f$cc_pf_raise_count = 0" in limp
    assert "f$cc_pf_call_btn" in limp and "f$cc_pf_call_sb" in limp
    assert "f$cc_pot_family_id = 2" in srp
    assert "f$cc_pf_one_raise_ordinary_srp" in srp
    assert "f$cc_pf_single_raiser_pos_id = 4" in srp
    assert "f$cc_pf_call_sb" in srp and "f$cc_pf_call_bb" in srp

    for name, pos, rel in (
        ("f$cc_flop_donk_6max_limped_sb_context", 5, 1),
        ("f$cc_flop_donk_6max_limped_bb_context", 6, 2),
        ("f$cc_flop_donk_6max_btnopen_sb_context", 5, 1),
        ("f$cc_flop_donk_6max_btnopen_bb_context", 6, 2),
    ):
        b = block(POL, name)
        assert f"f$cc_hero_pos_id = {pos}" in b
        assert f"f$cc_relpos_id = {rel}" in b

    parent = block(POL, "f$cc_flop_donk_6max_parent_id")
    assert "f$cc_flop_donk_6max_parent_count != 1 Return 0 Force" in parent
    for idx, token in enumerate(
        (
            "f$cc_flop_donk_6max_limped_sb_context",
            "f$cc_flop_donk_6max_limped_bb_context",
            "f$cc_flop_donk_6max_btnopen_sb_context",
            "f$cc_flop_donk_6max_btnopen_bb_context",
        ),
        start=1,
    ):
        assert f"{token} Return {idx} Force" in parent


def strategy_tightening_contract() -> None:
    limp_sb = block(POL, "f$cc_flop_donk_6max_limped_sb_action")
    limp_bb = block(POL, "f$cc_flop_donk_6max_limped_bb_action")
    srp_sb = block(POL, "f$cc_flop_donk_6max_btnopen_sb_action")
    srp_bb = block(POL, "f$cc_flop_donk_6max_btnopen_bb_action")

    # BTN-open SB is deliberately the tightest: no one-pair or low-pair positive branch.
    assert "f$cc_flop_donk_6max_robust_value" in srp_sb
    assert "f$cc_nut_or_combo_draw" in srp_sb
    assert "f$cc_flop_donk_6max_overpair" not in srp_sb
    assert "f$cc_cbet_flop_strong_top_pair" not in srp_sb
    assert "f$cc_flop_donk_6max_low_pair Return true Force" not in srp_sb

    # BB after SB checks may lead selected strong one-pair/draws, but no low-pair SRP stab.
    assert "f$cc_flop_donk_6max_overpair" in srp_bb
    assert "f$cc_cbet_flop_strong_top_pair" in srp_bb
    assert "f$cc_cbet_flop_premium_draw" in srp_bb
    assert "f$cc_flop_donk_6max_low_pair Return false Force" in srp_bb

    # Source <=7 pair is retained only in the limped BB-after-SB-check branch.
    assert "f$cc_flop_donk_6max_low_pair Return false Force" in limp_sb
    assert "f$cc_flop_donk_6max_low_pair" in limp_bb
    assert "Return true Force" in limp_bb

    # Limped SB can lead premium draws but ordinary good draws are BB-only.
    assert "f$cc_cbet_flop_premium_draw" in limp_sb
    assert "f$cc_cbet_flop_good_draw" not in limp_sb
    assert "f$cc_cbet_flop_good_draw" in limp_bb


def stack_depth_contract() -> None:
    spr = block(POL, "f$cc_flop_donk_6max_drawheavy_low_spr")
    code = executable(spr)
    assert "f$cc_mw_spr_deepest_round_start" in code
    assert "<= 1.25" in code
    assert "shallowest" not in code.lower()

    size = block(POL, "f$cc_flop_donk_6max_size_id")
    pot_line = (
        "f$cc_flop_donk_6max_robust_value && "
        "f$cc_flop_donk_6max_drawheavy_low_spr Return f$cc_flop_donk_size_100_id Force"
    )
    assert pot_line in size
    # POT sizing must not be granted to one-pair or draw branches.
    for line in size.splitlines():
        if "f$cc_flop_donk_size_100_id" in line:
            assert "f$cc_flop_donk_6max_robust_value" in line


def source_boundary_and_safety_contract() -> None:
    covered = block(POL, "f$cc_flop_donk_6max_covered")
    assert "f$cc_flop_donk_6max_parent_id > 0" in covered

    not_source = block(POL, "f$cc_flop_donk_6max_not_source_covered")
    assert "f$cc_flop_donk_6max_covered" in not_source
    assert "!f$cc_flop_donk_source_covered" in not_source

    code = executable(POL)
    for forbidden in (
        "BetMax",
        "HandPower",
        "random",
        "Raise_Committed",
        "StackOffDraws",
        "user_TurnShove",
        "f$cc_cbet_flop_quality_air",
        "f$cc_cbet_flop_pure_air",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate07C executable leak: {forbidden}"

    action = block(POL, "f$cc_flop_donk_6max_action")
    assert "When Others Return false Force" in action


def router_contract() -> None:
    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_source_covered Return 1 Force" in family
    assert "f$cc_flop_donk_6max_covered Return 2 Force" in family
    assert family.index("f$cc_flop_donk_source_covered") < family.index("f$cc_flop_donk_6max_covered")

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_source_covered Return f$cc_flop_donk_source_action Force" in router
    assert "f$cc_flop_donk_6max_covered Return f$cc_flop_donk_6max_action Force" in router

    size = block(ROUTER, "f$cc_flop_donk_size_id")
    assert "f$cc_flop_donk_6max_covered Return f$cc_flop_donk_6max_size_id Force" in size

    strategy = block(ROUTER, "f$cc_flop_donk_strategy_covered")
    assert "f$cc_flop_donk_source_covered" in strategy
    assert "f$cc_flop_donk_6max_covered" in strategy


if __name__ == "__main__":
    context_separation_contract()
    strategy_tightening_contract()
    stack_depth_contract()
    source_boundary_and_safety_contract()
    router_contract()
    print("PASS: Gate07C 4-6h BTN+both-blinds Flop Donk adaptation contract")
