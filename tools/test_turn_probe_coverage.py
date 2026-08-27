#!/usr/bin/env python3
"""Gate10F-I canonical Turn-Probe routing/coverage contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "src" / "CashCrusher_Turn_Probe.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def ordered_router_contract() -> None:
    family = block(ROUTER, "f$cc_turn_probe_family_id")
    expected = [
        "f$cc_turn_probe_hubb_covered Return 1 Force",
        "f$cc_turn_probe_3w_source_covered Return 2 Force",
        "f$cc_turn_probe_sbvbtn_gap_covered Return 3 Force",
        "f$cc_turn_probe_mw_gap_covered Return 4 Force",
        "f$cc_turn_probe_srp_gap_covered Return 5 Force",
        "f$cc_turn_probe_iso_covered Return 6 Force",
        "f$cc_turn_probe_3bp_covered Return 7 Force",
        "f$cc_turn_probe_4bp_covered Return 8 Force",
    ]
    positions = [family.index(x) for x in expected]
    assert positions == sorted(positions), "source/gap family precedence changed"

    router = block(ROUTER, "f$cc_turn_probe_router")
    for token in (
        "!f$cc_turn_probe_base_opportunity Return false Force",
        "f$cc_turn_probe_hubb_covered Return f$cc_turn_probe_hubb_action Force",
        "f$cc_turn_probe_3w_source_covered Return f$cc_turn_probe_3w_source_action Force",
        "f$cc_turn_probe_sbvbtn_gap_covered Return f$cc_turn_probe_sbvbtn_gap_action Force",
        "f$cc_turn_probe_mw_gap_covered Return f$cc_turn_probe_mw_gap_action Force",
        "f$cc_turn_probe_srp_gap_covered Return f$cc_turn_probe_srp_gap_action Force",
        "f$cc_turn_probe_iso_covered Return f$cc_turn_probe_iso_action Force",
        "f$cc_turn_probe_3bp_covered Return f$cc_turn_probe_3bp_action Force",
        "f$cc_turn_probe_4bp_covered Return f$cc_turn_probe_4bp_action Force",
        "When Others Return false Force",
    ):
        assert token in router


def coverage_contract() -> None:
    covered = block(ROUTER, "f$cc_turn_probe_strategy_covered")
    for token in (
        "f$cc_turn_probe_hubb_covered",
        "f$cc_turn_probe_3w_source_covered",
        "f$cc_turn_probe_sbvbtn_gap_covered",
        "f$cc_turn_probe_mw_gap_covered",
        "f$cc_turn_probe_srp_gap_covered",
        "f$cc_turn_probe_iso_covered",
        "f$cc_turn_probe_3bp_covered",
        "f$cc_turn_probe_4bp_covered",
    ):
        assert token in covered

    uncovered = block(ROUTER, "f$cc_turn_probe_uncovered_context")
    assert "f$cc_turn_probe_base_opportunity && !f$cc_turn_probe_strategy_covered" in uncovered

    pot = block(ROUTER, "f$cc_turn_probe_uncovered_pot_family_id")
    for n in range(1, 5):
        assert f"f$cc_pot_family_id = {n}" in pot
    assert "f$cc_pot_family_id >= 5" in pot


def provenance_and_exclusivity_contract() -> None:
    prov = block(ROUTER, "f$cc_turn_probe_provenance_id")
    assert "f$cc_turn_probe_hubb_covered Return 1 Force" in prov
    assert "f$cc_turn_probe_3w_source_covered Return 1 Force" in prov
    assert "f$cc_turn_probe_sbvbtn_gap_covered Return 2 Force" in prov
    assert "f$cc_turn_probe_mw_gap_covered Return 2 Force" in prov
    assert "f$cc_turn_probe_srp_gap_covered Return 3 Force" in prov
    assert "f$cc_turn_probe_iso_covered Return 3 Force" in prov
    assert "f$cc_turn_probe_3bp_covered Return 3 Force" in prov
    assert "f$cc_turn_probe_4bp_covered Return 3 Force" in prov

    count = block(ROUTER, "f$cc_turn_probe_child_owner_count")
    assert count.count("? 1 : 0") == 8

    consistent = block(ROUTER, "f$cc_turn_probe_router_consistent")
    assert "f$cc_turn_probe_history_consistent" in consistent
    assert "f$cc_turn_probe_child_owner_count != 1" in consistent
    assert "f$cc_turn_probe_size_consistent" in consistent


def sizing_and_safety_contract() -> None:
    size = block(ROUTER, "f$cc_turn_probe_size_id")
    for token in (
        "f$cc_turn_probe_hubb_size_id",
        "f$cc_turn_probe_3w_source_size_id",
        "f$cc_turn_probe_sbvbtn_gap_size_id",
        "f$cc_turn_probe_mw_gap_size_id",
        "f$cc_turn_probe_srp_gap_size_id",
        "f$cc_turn_probe_iso_size_id",
        "f$cc_turn_probe_3bp_size_id",
        "f$cc_turn_probe_4bp_size_id",
    ):
        assert token in size

    consistency = block(ROUTER, "f$cc_turn_probe_size_consistent")
    assert "f$cc_turn_probe_size_id >= 1 && f$cc_turn_probe_size_id <= 7" in consistency

    code = executable(ROUTER).lower()
    for forbidden in (
        "betmax",
        "raise_committed",
        "random",
        "handpower",
        "user_river",
        "user_turn",
        "f$game_",
    ):
        assert forbidden not in code, f"forbidden Gate10F-I executable leak: {forbidden}"


if __name__ == "__main__":
    ordered_router_contract()
    coverage_contract()
    provenance_and_exclusivity_contract()
    sizing_and_safety_contract()
    print("PASS: Gate10F-I canonical Turn-Probe routing/coverage")
