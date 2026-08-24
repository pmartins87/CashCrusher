#!/usr/bin/env python3
"""Gate06 canonical River Float router/coverage contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Float.txt").read_text(encoding="utf-8")


def block(name: str) -> str:
    marker = f"##{name}##"
    assert marker in POL, f"missing {name}"
    start = POL.index(marker) + len(marker)
    tail = POL[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def family_contract() -> None:
    family = block("f$cc_river_float_family_id")
    assert "f$cc_river_float_source_covered Return 1 Force" in family
    assert "f$cc_river_float_srp_gap_covered Return 2 Force" in family
    assert "When Others Return 0 Force" in family


def router_contract() -> None:
    router = block("f$cc_river_float_router")
    source = "f$cc_river_float_source_covered Return f$cc_river_float_source_action Force"
    srp = "f$cc_river_float_srp_gap_covered Return f$cc_river_float_srp_gap_action Force"
    assert source in router and srp in router
    assert router.index(source) < router.index(srp)
    assert "When Others Return false Force" in router

    size = block("f$cc_river_float_size_id")
    assert "f$cc_river_float_source_covered Return f$cc_river_float_source_size_id Force" in size
    assert "f$cc_river_float_srp_gap_covered Return f$cc_river_float_srp_gap_size_id Force" in size
    assert "When Others Return 0 Force" in size


def coverage_contract() -> None:
    covered = block("f$cc_river_float_strategy_covered")
    assert "f$cc_river_float_source_covered || f$cc_river_float_srp_gap_covered" in covered

    consistency = block("f$cc_river_float_size_consistent")
    assert "!f$cc_river_float_router Return f$cc_river_float_size_id = 0 Force" in consistency
    assert "f$cc_river_float_router Return f$cc_river_float_size_id >= 1 && f$cc_river_float_size_id <= 5 Force" in consistency

    uncovered = block("f$cc_river_float_uncovered_context")
    assert "f$cc_river_float_opportunity && !f$cc_river_float_strategy_covered" in uncovered


def future_family_fail_closed_contract() -> None:
    code = "\n".join(line.split("//", 1)[0] for line in POL.splitlines())
    # Gate06C must not silently route future non-SRP pot families.
    for forbidden in (
        "river_float_iso_covered",
        "river_float_plain3bp_covered",
        "river_float_squeeze_covered",
        "river_float_4bp_covered",
    ):
        assert forbidden not in code


if __name__ == "__main__":
    family_contract()
    router_contract()
    coverage_contract()
    future_family_fail_closed_contract()
    print("PASS: Gate06 canonical River Float source/SRP coverage contract")