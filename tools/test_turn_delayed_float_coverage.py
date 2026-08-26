#!/usr/bin/env python3
"""Gate12B canonical Turn Delayed-Float coverage / fail-closed audit."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat.txt").read_text(encoding="utf-8")
H = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_History.txt").read_text(encoding="utf-8")
HUSB = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_HUSB_Negative.txt").read_text(encoding="utf-8")
ISO = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_ISO.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def family_ids_contract() -> None:
    fam = block(R, "f$cc_turn_delayed_float_family_id")
    expected = (
        (1, "f$cc_turn_delayed_float_3w_bbvsb_source_covered"),
        (2, "f$cc_turn_delayed_float_srp6_hu_context"),
        (3, "f$cc_turn_delayed_float_srp6_mw_context"),
        (4, "f$cc_turn_delayed_float_iso_hu_limper"),
        (5, "f$cc_turn_delayed_float_iso_hu_coldcaller"),
        (6, "f$cc_turn_delayed_float_iso_mw_context"),
        (7, "f$cc_turn_delayed_float_plain3bp_hu_context"),
        (8, "f$cc_turn_delayed_float_plain3bp_mw_context"),
        (9, "f$cc_turn_delayed_float_squeeze_hu_context"),
        (10, "f$cc_turn_delayed_float_squeeze_mw_context"),
        (11, "f$cc_turn_delayed_float_4bp_covered"),
        (12, "f$cc_turn_delayed_float_unraised6_hu_context"),
        (13, "f$cc_turn_delayed_float_unraised6_mw_context"),
    )
    for fid, owner in expected:
        assert f"When {owner} Return {fid} Force" in fam
    assert "When Others Return 0 Force" in fam


def union_and_owner_contract() -> None:
    covered = block(R, "f$cc_turn_delayed_float_strategy_covered")
    for token in (
        "f$cc_turn_delayed_float_3w_bbvsb_source_covered",
        "f$cc_turn_delayed_float_unraised6_covered",
        "f$cc_turn_delayed_float_srp6_covered",
        "f$cc_turn_delayed_float_iso_covered",
        "f$cc_turn_delayed_float_plain3bp_covered",
        "f$cc_turn_delayed_float_squeeze_covered",
        "f$cc_turn_delayed_float_4bp_covered",
    ):
        assert token in covered

    # HUSB is reviewed source-negative, not a fake positive strategy owner.
    assert "husb" not in executable(covered).lower()
    assert block(HUSB, "f$cc_turn_delayed_float_husb_source_action").strip() == "false"

    owners = block(R, "f$cc_turn_delayed_float_child_owner_count")
    assert owners.count("* 1") == 7
    for token in (
        "f$cc_turn_delayed_float_3w_bbvsb_source_covered",
        "f$cc_turn_delayed_float_unraised6_covered",
        "f$cc_turn_delayed_float_srp6_covered",
        "f$cc_turn_delayed_float_iso_covered",
        "f$cc_turn_delayed_float_plain3bp_covered",
        "f$cc_turn_delayed_float_squeeze_covered",
        "f$cc_turn_delayed_float_4bp_covered",
    ):
        assert token in owners

    # ISO additionally proves exactly one limper/coldcaller/MW child internally.
    iso_owners = block(ISO, "f$cc_turn_delayed_float_iso_owner_count")
    assert iso_owners.count("* 1") == 3


def fail_closed_contract() -> None:
    router = block(R, "f$cc_turn_delayed_float_router")
    size = block(R, "f$cc_turn_delayed_float_size_id")
    assert "When Others Return false Force" in router
    assert "When Others Return 0 Force" in size

    uncovered = block(R, "f$cc_turn_delayed_float_uncovered_context")
    assert "f$cc_turn_delayed_float_base_opportunity" in uncovered
    assert "!f$cc_turn_delayed_float_strategy_covered" in uncovered
    assert "!f$cc_turn_delayed_float_husb_reviewed_negative" in uncovered
    assert "!f$cc_turn_delayed_float_3w_bbvsb_unexpected_check_history" in uncovered

    mismatch = block(R, "f$cc_turn_delayed_float_source_mismatch")
    assert "f$cc_turn_delayed_float_3w_bbvsb_unexpected_check_history" in mismatch
    assert "f$cc_turn_delayed_float_husb_source_mismatch" in mismatch

    # 5bet+ and unknown pot families never become base opportunities.
    noinit = block(H, "f$cc_turn_delayed_float_preflop_noinitiative")
    assert "When f$cc_pot_family_id <= 0 Return false Force" in noinit
    assert "When f$cc_pot_family_id >= 5 Return false Force" in noinit

    # FIRST/MIDDLE remain owned by Probe; delayed float is exact LAST only.
    first = block(H, "f$cc_turn_delayed_float_first_turn_action_clean")
    assert "f$cc_relpos_id = 3" in first
    assert "f$cc_relpos_id = 1" not in first
    assert "f$cc_relpos_id = 2" not in first

    # Short-handed source-silent residues are not widened with 4-6h P policy.
    for text in (
        (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_SRP_6Max.txt").read_text(encoding="utf-8"),
        (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_ISO.txt").read_text(encoding="utf-8"),
        (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_3BP.txt").read_text(encoding="utf-8"),
        (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_4BP.txt").read_text(encoding="utf-8"),
        (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_Unraised_6Max.txt").read_text(encoding="utf-8"),
    ):
        assert "f$cc_deal_size >= 4" in text
        assert "f$cc_deal_size <= 6" in text


def consistency_contract() -> None:
    c = block(R, "f$cc_turn_delayed_float_router_consistent")
    for token in (
        "!f$cc_turn_delayed_float_history_consistent Return false Force",
        "!f$cc_turn_delayed_float_3w_bbvsb_size_consistent Return false Force",
        "!f$cc_turn_delayed_float_unraised6_size_consistent Return false Force",
        "!f$cc_turn_delayed_float_srp6_size_consistent Return false Force",
        "!f$cc_turn_delayed_float_iso_size_consistent Return false Force",
        "!f$cc_turn_delayed_float_plain3bp_size_consistent Return false Force",
        "!f$cc_turn_delayed_float_squeeze_size_consistent Return false Force",
        "!f$cc_turn_delayed_float_4bp_size_consistent Return false Force",
        "f$cc_turn_delayed_float_source_mismatch Return false Force",
        "f$cc_turn_delayed_float_strategy_covered && f$cc_turn_delayed_float_child_owner_count != 1 Return false Force",
    ):
        assert token in c

    sizec = block(R, "f$cc_turn_delayed_float_size_consistent")
    for size_id in ("size_33_id", "size_50_id", "size_75_id"):
        assert f"f$cc_turn_delayed_float_{size_id}" in sizec


def no_generic_leak_contract() -> None:
    code = executable(R).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe Gate12B router leak: {forbidden}"


if __name__ == "__main__":
    family_ids_contract()
    union_and_owner_contract()
    fail_closed_contract()
    consistency_contract()
    no_generic_leak_contract()
    print("PASS: Gate12B canonical coverage / fail-closed audit")
