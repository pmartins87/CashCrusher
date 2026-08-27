#!/usr/bin/env python3
"""Gate09D/E ISO + plain-3BP/squeeze River Donk contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ISO = (SRC / "CashCrusher_River_Donk_ISO.txt").read_text(encoding="utf-8")
THREE = (SRC / "CashCrusher_River_Donk_3BP.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_River_Donk.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def iso_contract() -> None:
    ctx = block(ISO, "f$cc_river_donk_iso_context")
    for token in (
        "f$cc_river_donk_base_opportunity",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_iso_proven",
        "!f$cc_true_hu",
        "f$cc_river_donk_iso_hero_origin_count = 1",
    ):
        assert token in ctx

    origins = block(ISO, "f$cc_river_donk_iso_hero_origin_id")
    assert "f$cc_river_donk_iso_hero_is_isolator Return 1 Force" in origins
    assert "f$cc_river_donk_iso_hero_is_original_limper Return 2 Force" in origins
    assert "f$cc_river_donk_iso_hero_is_postraise_coldcaller Return 3 Force" in origins

    topo = block(ISO, "f$cc_river_donk_iso_topology_id")
    for n in (2, 3, 4):
        assert f"Return {n} Force" in topo

    isolator = block(ISO, "f$cc_river_donk_iso_isolator_value")
    caller = block(ISO, "f$cc_river_donk_iso_caller_value")
    mw = block(ISO, "f$cc_river_donk_iso_multiway_origin_value")
    assert "HaveNuts Return true Force" in isolator
    assert "f$cc_river_donk_contributed_exact_two_pair || HaveSet Return true Force" in isolator
    assert "HaveSet Return true Force" in caller
    assert "f$cc_river_four_card_completion Return false Force" in mw

    action = block(ISO, "f$cc_river_donk_iso_action").lower()
    assert "top_pair" not in action and "overpair" not in action and "no_made" not in action
    assert "f$cc_river_donk_iso_nomade_bluff_blocked" in ISO


def threebp_contract() -> None:
    ctx = block(THREE, "f$cc_river_donk_3bp_context")
    for token in (
        "f$cc_river_donk_base_opportunity",
        "f$cc_pot_family_id = 3",
        "f$cc_pf_rt_3bet_order_supported",
        "f$cc_river_donk_3bp_hero_origin_count = 1",
        "f$cc_river_donk_3bp_subtype_id > 0",
    ):
        assert token in ctx

    origins = block(THREE, "f$cc_river_donk_3bp_hero_origin_id")
    assert "f$cc_river_donk_3bp_hero_is_3bettor Return 1 Force" in origins
    assert "f$cc_river_donk_3bp_hero_is_opener_call Return 2 Force" in origins
    assert "f$cc_river_donk_3bp_hero_is_pre3bet_coldcaller Return 3 Force" in origins
    assert "f$cc_river_donk_3bp_hero_is_post3bet_coldcaller Return 4 Force" in origins

    subtype = block(THREE, "f$cc_river_donk_3bp_subtype_id")
    assert "f$cc_pf_rt_plain3bet_proven && !f$cc_pf_rt_squeeze_proven Return 1 Force" in subtype
    assert "f$cc_pf_rt_squeeze_proven && !f$cc_pf_rt_plain3bet_proven Return 2 Force" in subtype

    value3 = block(THREE, "f$cc_river_donk_3bp_threebettor_value")
    caller = block(THREE, "f$cc_river_donk_3bp_caller_value")
    mw = block(THREE, "f$cc_river_donk_3bp_multiway_origin_value")
    assert "HaveNuts Return true Force" in value3
    assert "f$cc_river_donk_contributed_exact_two_pair || HaveSet Return true Force" in value3
    assert "f$cc_river_donk_3bp_hero_origin_id = 2 && f$cc_river_donk_contributed_exact_two_pair Return true Force" in caller
    assert "f$cc_river_four_card_completion Return false Force" in mw

    action = block(THREE, "f$cc_river_donk_3bp_action").lower()
    assert "top_pair" not in action and "overpair" not in action and "no_made" not in action
    assert "f$cc_river_donk_3bp_nomade_bluff_blocked" in THREE


def safety_and_router_contract() -> None:
    code = (executable(ISO) + "\n" + executable(THREE)).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "stackoffdraws", "f$game_"):
        assert forbidden not in code, f"legacy leak: {forbidden}"

    family = block(ROUTER, "f$cc_river_donk_family_id")
    assert "f$cc_river_donk_iso_covered Return 3 Force" in family
    assert "f$cc_river_donk_3bp_covered Return 4 Force" in family

    route = block(ROUTER, "f$cc_river_donk_router")
    assert "f$cc_river_donk_iso_covered Return f$cc_river_donk_iso_action Force" in route
    assert "f$cc_river_donk_3bp_covered Return f$cc_river_donk_3bp_action Force" in route

    sizes = block(ROUTER, "f$cc_river_donk_size_id")
    assert "f$cc_river_donk_iso_covered Return f$cc_river_donk_iso_size_id Force" in sizes
    assert "f$cc_river_donk_3bp_covered Return f$cc_river_donk_3bp_size_id Force" in sizes

    count = block(ROUTER, "f$cc_river_donk_reviewed_family_count")
    for token in (
        "f$cc_river_donk_hubb_covered",
        "f$cc_river_donk_srp_gap_covered",
        "f$cc_river_donk_iso_covered",
        "f$cc_river_donk_3bp_covered",
    ):
        assert token in count


if __name__ == "__main__":
    iso_contract()
    threebp_contract()
    safety_and_router_contract()
    print("PASS: Gate09D/E ISO + 3BP/squeeze River Donk contracts")
