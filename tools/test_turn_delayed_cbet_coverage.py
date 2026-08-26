#!/usr/bin/env python3
"""Gate12A canonical Turn Delayed-CBet coverage / fail-closed audit."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")
ISO = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_ISO.txt").read_text(encoding="utf-8")
BP3 = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3BP.txt").read_text(encoding="utf-8")
BP4 = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_4BP.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def family_ids_contract() -> None:
    fam = block(R, "f$cc_turn_delayed_cbet_family_id")
    expected = (
        (1, "f$cc_turn_delayed_cbet_husb_source_context"),
        (2, "f$cc_turn_delayed_cbet_hubb_source_context"),
        (3, "f$cc_turn_delayed_cbet_3w_btnvbb_source_context"),
        (4, "f$cc_turn_delayed_cbet_3w_btnvsb_source_covered"),
        (5, "f$cc_turn_delayed_cbet_3w_bbvsb_source_covered"),
        (6, "f$cc_turn_delayed_cbet_3w_sbvbb_source_covered"),
        (7, "f$cc_turn_delayed_cbet_3w_btnv2p_covered"),
        (8, "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered"),
        (9, "f$cc_turn_delayed_cbet_srp6_hu_covered"),
        (10, "f$cc_turn_delayed_cbet_srp6_mw_covered"),
        (11, "f$cc_turn_delayed_cbet_iso_hu_covered"),
        (12, "f$cc_turn_delayed_cbet_iso_mw_covered"),
        (13, "f$cc_turn_delayed_cbet_plain3bp_hu_covered"),
        (14, "f$cc_turn_delayed_cbet_plain3bp_mw_covered"),
        (15, "f$cc_turn_delayed_cbet_squeeze_hu_covered"),
        (16, "f$cc_turn_delayed_cbet_squeeze_mw_covered"),
        (17, "f$cc_turn_delayed_cbet_4bp_covered"),
    )
    for fid, owner in expected:
        assert f"{owner} Return {fid} Force" in fam
    assert fam.count("Return 0 Force") >= 2


def union_and_exclusivity_contract() -> None:
    covered = block(R, "f$cc_turn_delayed_cbet_strategy_covered")
    for token in (
        "f$cc_turn_delayed_cbet_core_source_covered",
        "f$cc_turn_delayed_cbet_3w_extra_source_covered",
        "f$cc_turn_delayed_cbet_3w_sbvbb_source_covered",
        "f$cc_turn_delayed_cbet_3w_btnv2p_covered",
        "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered",
        "f$cc_turn_delayed_cbet_srp6_covered",
        "f$cc_turn_delayed_cbet_iso_covered",
        "f$cc_turn_delayed_cbet_3bp_covered",
        "f$cc_turn_delayed_cbet_4bp_covered",
    ):
        assert token in covered

    owners = block(R, "f$cc_turn_delayed_cbet_child_owner_count")
    assert owners.count("? 1 : 0") == 17

    consistent = block(R, "f$cc_turn_delayed_cbet_router_consistent")
    assert "f$cc_turn_delayed_cbet_strategy_covered && f$cc_turn_delayed_cbet_child_owner_count != 1 Return false Force" in consistent
    assert "!f$cc_turn_delayed_cbet_strategy_covered && f$cc_turn_delayed_cbet_family_id != 0 Return false Force" in consistent
    assert "f$cc_turn_delayed_cbet_strategy_covered && f$cc_turn_delayed_cbet_family_id <= 0 Return false Force" in consistent


def fail_closed_contract() -> None:
    uncovered = block(R, "f$cc_turn_delayed_cbet_uncovered_context")
    assert "f$cc_turn_delayed_cbet_base_opportunity && !f$cc_turn_delayed_cbet_strategy_covered" in uncovered

    router = executable(block(R, "f$cc_turn_delayed_cbet_router"))
    assert "When Others Return false Force" in router
    sizing = executable(block(R, "f$cc_turn_delayed_cbet_size_id"))
    assert "When Others Return 0 Force" in sizing

    iso_gap = block(ISO, "f$cc_turn_delayed_cbet_iso_unresolved")
    assert "f$cc_turn_delayed_cbet_iso_parent && !f$cc_turn_delayed_cbet_iso_covered" in iso_gap
    bp3_gap = block(BP3, "f$cc_turn_delayed_cbet_3bp_unresolved")
    assert "f$cc_turn_delayed_cbet_3bp_parent && !f$cc_turn_delayed_cbet_3bp_covered" in bp3_gap
    bp4_gap = block(BP4, "f$cc_turn_delayed_cbet_4bp_unresolved")
    assert "f$cc_turn_delayed_cbet_4bp_parent && !f$cc_turn_delayed_cbet_4bp_covered" in bp4_gap


def fourbet_boundary_contract() -> None:
    # Supported 4BP is explicitly clean HU only; multiway and othercaller do not inherit it.
    hu = block(BP4, "f$cc_turn_delayed_cbet_4bp_hu_context")
    assert "f$cc_flop_entry_count = 2" in hu
    assert "f$cc_hu && f$cc_hu_origin_preflop_reduced" in hu
    assert "f$cc_hu_4bp_survivor_type_id > 0" in hu
    assert "f$cc_hu_4bp_survivor_type_id < 3" in hu
    supported = block(BP4, "f$cc_turn_delayed_cbet_4bp_supported")
    assert "f$cc_turn_delayed_cbet_4bp_hu_context" in supported
    assert "f$cc_multiway" not in executable(supported)
    assert "othercaller" not in executable(supported).lower()


def no_generic_leak_contract() -> None:
    code = executable(R + "\n" + ISO + "\n" + BP3 + "\n" + BP4).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe Gate12A coverage leak: {forbidden}"


if __name__ == "__main__":
    family_ids_contract()
    union_and_exclusivity_contract()
    fail_closed_contract()
    fourbet_boundary_contract()
    no_generic_leak_contract()
    print("PASS: Gate12A canonical coverage / fail-closed audit")
