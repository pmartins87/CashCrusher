#!/usr/bin/env python3
"""Gate07D HU / reduced-HU ordinary-SRP Flop Donk check-range contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_HU.txt").read_text(encoding="utf-8")
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


def true_hu_contract() -> None:
    srp = block(POL, "f$cc_flop_donk_truehu_srp_bb_context")
    for token in (
        "f$cc_true_hu",
        "f$cc_hu_oop",
        "f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = 5",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = 5",
    ):
        assert token in srp

    limped = block(POL, "f$cc_flop_donk_truehu_limped_bb_context")
    for token in (
        "f$cc_true_hu",
        "f$cc_hu_oop",
        "f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = 5",
        "f$cc_pot_family_id = 1",
        "f$cc_pf_role_bb_check",
        "f$cc_pf_call_sb",
    ):
        assert token in limped


def reduced_hu_contract() -> None:
    red = block(POL, "f$cc_flop_donk_reducedhu_srp_oop_caller_context")
    for token in (
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_oop",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = f$cc_hu_villain_pos_id",
    ):
        assert token in red
    assert "f$cc_hu_origin_postflop_reduced" not in red


def check_only_contract() -> None:
    for name in (
        "f$cc_flop_donk_truehu_srp_bb_action",
        "f$cc_flop_donk_truehu_limped_bb_action",
        "f$cc_flop_donk_reducedhu_srp_oop_caller_action",
        "f$cc_flop_donk_hu_action",
    ):
        b = block(POL, name)
        assert "Return true Force" not in b, f"positive HU Donk leaked into {name}"
        assert "Return false Force" in b

    size = block(POL, "f$cc_flop_donk_hu_size_id")
    assert "When Others Return 0 Force" in size

    covered = block(POL, "f$cc_flop_donk_hu_covered")
    assert "f$cc_flop_donk_hu_parent_id > 0" in covered

    code = executable(POL)
    for forbidden in (
        "BetMax",
        "HandPower",
        "random",
        "Raise_Committed",
        "StackOffDraws",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden HU Donk leak: {forbidden}"


def router_contract() -> None:
    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_hu_covered Return 3 Force" in family

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_hu_covered Return f$cc_flop_donk_hu_action Force" in router

    size = block(ROUTER, "f$cc_flop_donk_size_id")
    assert "f$cc_flop_donk_hu_covered Return f$cc_flop_donk_hu_size_id Force" in size

    covered = block(ROUTER, "f$cc_flop_donk_strategy_covered")
    assert "f$cc_flop_donk_hu_covered" in covered


if __name__ == "__main__":
    true_hu_contract()
    reduced_hu_contract()
    check_only_contract()
    router_contract()
    print("PASS: Gate07D HU / reduced-HU ordinary-SRP Flop Donk check-range contract")
