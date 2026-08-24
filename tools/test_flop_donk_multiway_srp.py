#!/usr/bin/env python3
"""Gate07E residual current-multiway ordinary-SRP Flop Donk contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_Multiway_SRP.txt").read_text(encoding="utf-8")
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


def context_contract() -> None:
    ctx = block(POL, "f$cc_flop_donk_mw_srp_check_context")
    for token in (
        "f$cc_flop_donk_opportunity",
        "f$cc_multiway",
        "f$cc_flop_entry_count >= 3",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id > 0",
        "!f$cc_flop_donk_source_covered",
        "!f$cc_flop_donk_6max_covered",
    ):
        assert token in ctx

    # No unrelated pot family may enter this residual SRP owner.
    for forbidden in ("f$cc_pot_family_id = 1", "f$cc_pot_family_id = 3", "f$cc_pot_family_id = 4"):
        assert forbidden not in ctx


def check_only_contract() -> None:
    action = block(POL, "f$cc_flop_donk_mw_srp_action")
    assert "Return true Force" not in action
    assert "Return false Force" in action

    size = block(POL, "f$cc_flop_donk_mw_srp_size_id")
    assert "When Others Return 0 Force" in size

    disjoint = block(POL, "f$cc_flop_donk_mw_srp_disjoint")
    assert "f$cc_flop_donk_source_covered Return false Force" in disjoint
    assert "f$cc_flop_donk_6max_covered Return false Force" in disjoint

    code = executable(POL)
    for forbidden in ("BetMax", "HandPower", "random", "Raise_Committed", "StackOffDraws"):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate07E leak: {forbidden}"


def router_contract() -> None:
    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_mw_srp_covered Return 4 Force" in family

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_mw_srp_covered Return f$cc_flop_donk_mw_srp_action Force" in router

    size = block(ROUTER, "f$cc_flop_donk_size_id")
    assert "f$cc_flop_donk_mw_srp_covered Return f$cc_flop_donk_mw_srp_size_id Force" in size

    covered = block(ROUTER, "f$cc_flop_donk_strategy_covered")
    assert "f$cc_flop_donk_mw_srp_covered" in covered


if __name__ == "__main__":
    context_contract()
    check_only_contract()
    router_contract()
    print("PASS: Gate07E residual multiway ordinary-SRP Flop Donk check-range contract")
