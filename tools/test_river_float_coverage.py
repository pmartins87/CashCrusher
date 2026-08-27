#!/usr/bin/env python3
"""Gate06 canonical River Float router/coverage contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Float.txt").read_text(encoding="utf-8")
FOUR = (ROOT / "src" / "CashCrusher_River_Float_4BP.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def family_contract() -> None:
    family = block(POL, "f$cc_river_float_family_id")
    assert "f$cc_river_float_source_covered Return 1 Force" in family
    assert "f$cc_river_float_srp_gap_covered Return 2 Force" in family
    assert "f$cc_river_float_iso_covered Return 3 Force" in family
    assert "f$cc_river_float_plain3bp_covered Return 4 Force" in family
    assert "f$cc_river_float_squeeze_covered Return 5 Force" in family
    assert "f$cc_river_float_4bp_covered Return 6 Force" in family
    assert "When Others Return 0 Force" in family


def router_contract() -> None:
    router = block(POL, "f$cc_river_float_router")
    ordered = [
        "f$cc_river_float_source_covered Return f$cc_river_float_source_action Force",
        "f$cc_river_float_srp_gap_covered Return f$cc_river_float_srp_gap_action Force",
        "f$cc_river_float_iso_covered Return f$cc_river_float_iso_action Force",
        "f$cc_river_float_plain3bp_covered Return f$cc_river_float_plain3bp_action Force",
        "f$cc_river_float_squeeze_covered Return f$cc_river_float_squeeze_action Force",
        "f$cc_river_float_4bp_covered Return f$cc_river_float_4bp_action Force",
    ]
    for item in ordered:
        assert item in router
    assert [router.index(item) for item in ordered] == sorted(router.index(item) for item in ordered)
    assert "When Others Return false Force" in router

    size = block(POL, "f$cc_river_float_size_id")
    for item in (
        "f$cc_river_float_source_covered Return f$cc_river_float_source_size_id Force",
        "f$cc_river_float_srp_gap_covered Return f$cc_river_float_srp_gap_size_id Force",
        "f$cc_river_float_iso_covered Return f$cc_river_float_iso_size_id Force",
        "f$cc_river_float_plain3bp_covered Return f$cc_river_float_plain3bp_size_id Force",
        "f$cc_river_float_squeeze_covered Return f$cc_river_float_squeeze_size_id Force",
        "f$cc_river_float_4bp_covered Return f$cc_river_float_4bp_size_id Force",
    ):
        assert item in size
    assert "When Others Return 0 Force" in size


def coverage_contract() -> None:
    covered = block(POL, "f$cc_river_float_strategy_covered")
    for token in (
        "f$cc_river_float_source_covered",
        "f$cc_river_float_srp_gap_covered",
        "f$cc_river_float_iso_covered",
        "f$cc_river_float_plain3bp_covered",
        "f$cc_river_float_squeeze_covered",
        "f$cc_river_float_4bp_covered",
    ):
        assert token in covered

    consistency = block(POL, "f$cc_river_float_size_consistent")
    assert "!f$cc_river_float_router Return f$cc_river_float_size_id = 0 Force" in consistency
    assert "f$cc_river_float_router Return f$cc_river_float_size_id >= 1 && f$cc_river_float_size_id <= 5 Force" in consistency

    uncovered = block(POL, "f$cc_river_float_uncovered_context")
    assert "f$cc_river_float_opportunity && !f$cc_river_float_strategy_covered" in uncovered


def unsupported_boundary_contract() -> None:
    # Even after clean 4BP review, 5bet+ and unresolved 4BP remain visible fail-closed.
    four_uncovered = block(FOUR, "f$cc_river_float_4bp_uncovered")
    assert "f$cc_pot_family_id = 4" in four_uncovered
    assert "!f$cc_river_float_4bp_covered" in four_uncovered

    five = block(FOUR, "f$cc_river_float_5betplus_uncovered")
    assert "f$cc_pot_family_id = 5" in five


if __name__ == "__main__":
    family_contract()
    router_contract()
    coverage_contract()
    unsupported_boundary_contract()
    print("PASS: Gate06 canonical River Float source/SRP/ISO/3BP/squeeze/clean4BP coverage contract")
