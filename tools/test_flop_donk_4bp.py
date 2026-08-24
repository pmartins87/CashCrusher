#!/usr/bin/env python3
"""Gate07I clean caller-side HU 4BP Flop Donk contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN = (ROOT / "src" / "CashCrusher_4BP_Caller_Context.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_4BP.txt").read_text(encoding="utf-8")
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


def chronology_contract() -> None:
    other = block(GEN, "f$cc_pf_call4_other_raiser_pos_id")
    for token in (
        "f$cc_pf_raise_count != 3",
        "!f$cc_pf_role_call_4bet",
        "!f$cc_pf_hero_ever_raised",
        "f$cc_pf_unique_raiser_count != 2",
    ):
        assert token in other

    proven = block(GEN, "f$cc_pf_call4_opener4_vs_hero3bettor_proven")
    assert "f$cc_pf_call4_other_raiser_pos_id < f$cc_hero_pos_id" in proven
    assert "f$cc_pf_unique_raiser_count = 2" in proven

    hu = block(GEN, "f$cc_hu_call4_vs_opener4_context")
    assert "f$cc_hu_villain_pos_id = f$cc_pf_call4_other_raiser_pos_id" in hu


def ownership_and_policy_contract() -> None:
    ctx = block(POL, "f$cc_flop_donk_4bp_hu_context")
    for token in (
        "f$cc_flop_donk_opportunity",
        "f$cc_hu",
        "f$cc_pot_family_id = 4",
        "f$cc_pf_call4_opener4_vs_hero3bettor_proven",
        "f$cc_hu_villain_pos_id = f$cc_pf_call4_other_raiser_pos_id",
        "f$cc_relpos_id != 3",
    ):
        assert token in ctx

    action = block(POL, "f$cc_flop_donk_4bp_hu_action")
    assert "When Others Return false Force" in action
    assert "Return true Force" not in action

    size = block(POL, "f$cc_flop_donk_4bp_hu_size_id")
    assert "When Others Return 0 Force" in size
    assert "Return 1 Force" not in size
    assert "Return 2 Force" not in size
    assert "Return 3 Force" not in size

    unresolved = block(POL, "f$cc_flop_donk_4bp_unresolved")
    assert "f$cc_pot_family_id = 4" in unresolved
    assert "!f$cc_flop_donk_4bp_covered" in unresolved


def safety_contract() -> None:
    code = executable(POL)
    for forbidden in (
        "BetMax",
        "HandPower",
        "random",
        "Raise_Committed",
        "StackOffDraws",
        "user_TurnShove",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate07I leak: {forbidden}"

    # This gate must not silently claim multiway or 5bet+ 4BP strategy.
    ctx = executable(block(POL, "f$cc_flop_donk_4bp_hu_context"))
    assert "f$cc_hu" in ctx
    assert "f$cc_multiway" not in ctx
    assert "f$cc_pot_family_id = 5" not in code


def router_contract() -> None:
    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_4bp_covered Return 8 Force" in family

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_4bp_covered Return f$cc_flop_donk_4bp_hu_action Force" in router

    size = block(ROUTER, "f$cc_flop_donk_size_id")
    assert "f$cc_flop_donk_4bp_covered Return f$cc_flop_donk_4bp_hu_size_id Force" in size

    covered = block(ROUTER, "f$cc_flop_donk_strategy_covered")
    assert "f$cc_flop_donk_4bp_covered" in covered


if __name__ == "__main__":
    chronology_contract()
    ownership_and_policy_contract()
    safety_contract()
    router_contract()
    print("PASS: Gate07I clean caller-side HU 4BP Flop Donk contract")
