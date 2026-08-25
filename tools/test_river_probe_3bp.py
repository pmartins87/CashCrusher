#!/usr/bin/env python3
"""Gate11I plain-3BP / squeeze River Probe contracts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Probe_3BP.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_River_Probe.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def provenance() -> None:
    assert "f$cc_pf_role_open_call_3bet" in block(POL, "f$cc_river_probe_3bp_hero_is_opener_call")
    assert "f$cc_pf_pre3bet_coldcaller_mask BitAnd f$cc_river_probe_3bp_hero_pos_bit" in block(POL, "f$cc_river_probe_3bp_hero_is_pre3bet_coldcaller")
    assert "f$cc_pf_post3bet_coldcaller_mask BitAnd f$cc_river_probe_3bp_hero_pos_bit" in block(POL, "f$cc_river_probe_3bp_hero_is_post3bet_coldcaller")
    vorig = block(POL, "f$cc_river_probe_3bp_villain_origin_consistent")
    for token in ("villain_is_opener_call", "villain_is_pre3bet_coldcaller", "villain_is_post3bet_coldcaller"):
        assert f"f$cc_river_probe_3bp_{token}" in vorig


def topology() -> None:
    clean = block(POL, "f$cc_river_probe_3bp_clean_hu_context")
    for token in ("f$cc_river_probe_hu_opportunity", "f$cc_flop_entry_count = 2", "f$cc_pot_family_id = 3", "f$cc_pf_3bet_order_supported"):
        assert token in clean
    caller = block(POL, "f$cc_river_probe_3bp_caller_vs_3bettor_context")
    assert "f$cc_river_probe_3bp_hero_origin_consistent" in caller
    assert "f$cc_hu_villain_pos_id = f$cc_pf_3bet_final_raiser_pos_id" in caller
    reverse = block(POL, "f$cc_river_probe_3bp_3bettor_vs_caller_stab_context")
    for token in ("f$cc_pf_role_3bettor", "f$cc_pf_3bet_final_raiser_pos_id = f$cc_hero_pos_id", "f$cc_river_probe_3bp_villain_origin_consistent", "lastraised2 = headsupchair"):
        assert token in reverse


def families() -> None:
    fam = block(POL, "f$cc_river_probe_3bp_family_id")
    assert "f$cc_pf_3bet_plain_proven" in fam and "f$cc_pf_squeeze_proven" in fam
    for i in range(1, 11):
        assert f"Return {i} Force" in fam
    wider = block(POL, "f$cc_river_probe_3bp_wider_family")
    for i in (1, 3, 6, 8):
        assert f"f$cc_river_probe_3bp_family_id = {i}" in wider


def policy() -> None:
    assert "NumberOfUnknownSuitedOvercards <= 4" in block(POL, "f$cc_river_probe_3bp_strong_flush")
    assert "!HaveUnderStraight" in block(POL, "f$cc_river_probe_3bp_strong_straight")
    medium = block(POL, "f$cc_river_probe_3bp_medium_value")
    for token in ("HaveTrips && !TripsOnBoard && npcbits > 0", "HaveSet", "f$cc_river_probe_contributed_exact_two_pair"):
        assert token in medium
    action = block(POL, "f$cc_river_probe_3bp_action")
    for token in ("f$cc_river_probe_3bp_premium_value Return true Force", "f$cc_river_probe_3bp_medium_value Return true Force", "f$cc_river_probe_3bp_overpair_real && f$cc_river_probe_3bp_thin_value_river Return true Force", "f$cc_river_probe_3bp_wider_family && f$cc_river_probe_3bp_strong_tp"):
        assert token in action
    assert "f$cc_river_probe_air" not in executable(action)
    size = block(POL, "f$cc_river_probe_3bp_size_id")
    assert "f$cc_river_probe_3bp_premium_value Return f$cc_river_probe_size_75_id" in size
    assert "f$cc_river_probe_3bp_medium_value Return f$cc_river_probe_size_50_id" in size
    assert "f$cc_river_probe_3bp_overpair_real Return f$cc_river_probe_size_33_id" in size


def routing() -> None:
    assert "f$cc_river_probe_3bp_context" in block(POL, "f$cc_river_probe_3bp_covered")
    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_3bp_covered Return 7 Force" in fam
    assert fam.index("f$cc_river_probe_iso_covered") < fam.index("f$cc_river_probe_3bp_covered")
    assert "f$cc_river_probe_3bp_covered Return f$cc_river_probe_3bp_action Force" in block(ROUTER, "f$cc_river_probe_router")
    assert "f$cc_river_probe_3bp_covered Return f$cc_river_probe_3bp_size_id Force" in block(ROUTER, "f$cc_river_probe_size_id")
    assert "f$cc_river_probe_3bp_covered" in block(ROUTER, "f$cc_river_probe_strategy_covered")
    code = executable(POL).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "effectivestack_bkp", "shorteststack"):
        assert forbidden not in code


if __name__ == "__main__":
    provenance(); topology(); families(); policy(); routing()
    print("PASS: Gate11I plain-3BP / squeeze River Probe adaptation")
