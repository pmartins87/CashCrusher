#!/usr/bin/env python3
"""Gate07G plain-3BP / squeeze Flop Donk check-range contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_3BP.txt").read_text(encoding="utf-8")
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
    subtype = block(POL, "f$cc_flop_donk_3bp_subtype_id")
    assert "f$cc_pf_rt_plain3bet_proven Return 1 Force" in subtype
    assert "f$cc_pf_rt_squeeze_proven Return 2 Force" in subtype

    origin = block(POL, "f$cc_flop_donk_3bp_hero_origin_id")
    assert "f$cc_pf_rt_hero_is_opener_call_3bet Return 1 Force" in origin
    assert "f$cc_pf_rt_hero_is_pre3bet_coldcaller Return 2 Force" in origin
    assert "f$cc_pf_rt_hero_is_post3bet_coldcaller Return 3 Force" in origin

    base = block(POL, "f$cc_flop_donk_3bp_base_context")
    for token in (
        "f$cc_pot_family_id = 3",
        "f$cc_pf_rt_3bet_order_supported",
        "f$cc_pf_rt_hero_3bet_origin_consistent",
        "f$cc_flop_donk_3bp_hero_origin_id > 0",
        "f$cc_flop_donk_3bp_subtype_id > 0",
        "f$cc_pf_rt_3bettor_live_opponent",
        "!f$cc_pf_rt_final_aggressor_is_hero",
    ):
        assert token in base


def field_contract() -> None:
    hu = block(POL, "f$cc_flop_donk_3bp_hu_context")
    for token in (
        "f$cc_hu",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_oop",
        "f$cc_hu_villain_pos_id = f$cc_pf_rt_final_aggressor_pos_id",
    ):
        assert token in hu

    mw = block(POL, "f$cc_flop_donk_3bp_multiway_context")
    assert "f$cc_multiway" in mw
    assert "f$cc_flop_entry_count >= 3" in mw

    key = block(POL, "f$cc_flop_donk_3bp_parent_key")
    assert "f$cc_flop_donk_3bp_subtype_id * 100" in key
    assert "f$cc_flop_donk_3bp_hero_origin_id * 10" in key
    assert "f$cc_flop_donk_3bp_field_id" in key


def check_only_contract() -> None:
    action = block(POL, "f$cc_flop_donk_3bp_action")
    assert "Return true Force" not in action
    assert "Return false Force" in action

    size = block(POL, "f$cc_flop_donk_3bp_size_id")
    assert "When Others Return 0 Force" in size

    unresolved = block(POL, "f$cc_flop_donk_3bp_unresolved")
    assert "f$cc_pot_family_id = 3" in unresolved
    assert "!f$cc_flop_donk_3bp_covered" in unresolved

    code = executable(POL)
    for forbidden in ("BetMax", "HandPower", "random", "Raise_Committed", "StackOffDraws"):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate07G leak: {forbidden}"


def router_contract() -> None:
    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_3bp_covered Return 6 Force" in family

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_3bp_covered Return f$cc_flop_donk_3bp_action Force" in router

    size = block(ROUTER, "f$cc_flop_donk_size_id")
    assert "f$cc_flop_donk_3bp_covered Return f$cc_flop_donk_3bp_size_id Force" in size

    covered = block(ROUTER, "f$cc_flop_donk_strategy_covered")
    assert "f$cc_flop_donk_3bp_covered" in covered


if __name__ == "__main__":
    chronology_contract()
    field_contract()
    check_only_contract()
    router_contract()
    print("PASS: Gate07G plain-3BP/squeeze Flop Donk check-range contract")
