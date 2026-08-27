#!/usr/bin/env python3
"""Gate07F isolation-pot Flop Donk check-range contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_ISO.txt").read_text(encoding="utf-8")
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


def origin_contract() -> None:
    limper = block(POL, "f$cc_flop_donk_iso_hero_was_limper")
    cold = block(POL, "f$cc_flop_donk_iso_hero_was_postraise_coldcaller")
    assert "f$cc_pf_pre_raise_limper_mask" in limper
    assert "f$cc_pf_post_raise_coldcaller_mask" in cold

    count = block(POL, "f$cc_flop_donk_iso_hero_origin_count")
    assert "f$cc_flop_donk_iso_hero_was_limper" in count
    assert "f$cc_flop_donk_iso_hero_was_postraise_coldcaller" in count

    consistent = block(POL, "f$cc_flop_donk_iso_hero_origin_consistent")
    assert "f$cc_flop_donk_iso_hero_origin_count = 1" in consistent


def topology_contract() -> None:
    hu = block(POL, "f$cc_flop_donk_iso_hu_context")
    for token in (
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_oop",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_iso_proven",
        "f$cc_pf_role_srp_caller",
        "f$cc_hu_villain_pos_id = f$cc_pf_single_raiser_pos_id",
        "f$cc_flop_donk_iso_hero_origin_consistent",
    ):
        assert token in hu

    mw = block(POL, "f$cc_flop_donk_iso_multiway_context")
    for token in (
        "f$cc_multiway",
        "f$cc_flop_entry_count >= 3",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_iso_proven",
        "f$cc_pf_role_srp_caller",
        "f$cc_flop_donk_iso_hero_origin_consistent",
    ):
        assert token in mw

    parent = block(POL, "f$cc_flop_donk_iso_parent_id")
    for idx, token in enumerate(
        (
            "f$cc_flop_donk_iso_hu_limper_context",
            "f$cc_flop_donk_iso_hu_coldcaller_context",
            "f$cc_flop_donk_iso_mw_limper_context",
            "f$cc_flop_donk_iso_mw_coldcaller_context",
        ),
        start=1,
    ):
        assert f"{token} Return {idx} Force" in parent


def check_only_contract() -> None:
    action = block(POL, "f$cc_flop_donk_iso_action")
    assert "Return true Force" not in action
    assert "Return false Force" in action

    size = block(POL, "f$cc_flop_donk_iso_size_id")
    assert "When Others Return 0 Force" in size

    code = executable(POL)
    for forbidden in ("BetMax", "HandPower", "random", "Raise_Committed", "StackOffDraws"):
        assert forbidden.lower() not in code.lower(), f"forbidden ISO Donk leak: {forbidden}"


def router_contract() -> None:
    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_iso_covered Return 5 Force" in family

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_iso_covered Return f$cc_flop_donk_iso_action Force" in router

    size = block(ROUTER, "f$cc_flop_donk_size_id")
    assert "f$cc_flop_donk_iso_covered Return f$cc_flop_donk_iso_size_id Force" in size

    covered = block(ROUTER, "f$cc_flop_donk_strategy_covered")
    assert "f$cc_flop_donk_iso_covered" in covered


if __name__ == "__main__":
    origin_contract()
    topology_contract()
    check_only_contract()
    router_contract()
    print("PASS: Gate07F isolation-pot Flop Donk check-range contract")
