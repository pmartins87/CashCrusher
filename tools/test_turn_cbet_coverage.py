#!/usr/bin/env python3
"""Static Gate02J.0 Turn-CBet coverage-boundary contract.

This test proves routing/exclusivity/fail-closed source contracts. It is not an
OpenHoldem replay or solver validation.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ROUTER = (SRC / "CashCrusher_Turn_CBet.txt").read_text(encoding="utf-8")
COMMON = (SRC / "CashCrusher_Turn_CBet_Common.txt").read_text(encoding="utf-8")
FOUR = (SRC / "CashCrusher_Turn_4BP_Context.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def first_executable_line(text: str) -> str:
    """Return first non-empty, non-comment line from a function body."""
    for raw in text.splitlines():
        line = raw.strip()
        if line and not line.startswith("//"):
            return line
    return ""


def all_turn_strategy_files() -> list[Path]:
    names = [
        "CashCrusher_Turn_CBet_SRP_IP.txt",
        "CashCrusher_Turn_CBet_SRP_OOP.txt",
        "CashCrusher_Turn_CBet_SRP_6MaxGaps.txt",
        "CashCrusher_Turn_CBet_SRP_PostMultiwayHU.txt",
        "CashCrusher_Turn_CBet_SRP_Multiway.txt",
        "CashCrusher_Turn_CBet_ISO.txt",
        "CashCrusher_Turn_CBet_3BP.txt",
        "CashCrusher_Turn_CBet_Squeeze.txt",
        "CashCrusher_Turn_CBet_4BP.txt",
    ]
    return [SRC / n for n in names]


def main() -> None:
    # 1) Pot-family selectors are explicit and mutually segregated at the router.
    ordinary = block(ROUTER, "f$cc_turn_cbet_ordinary_srp_context")
    iso = block(ROUTER, "f$cc_turn_cbet_iso_context")
    plain = block(ROUTER, "f$cc_turn_cbet_plain3bp_context")
    squeeze = block(ROUTER, "f$cc_turn_cbet_squeeze_context")
    four = block(ROUTER, "f$cc_turn_cbet_4bp_context")

    assert "f$cc_pot_family_id = 2" in ordinary
    assert "f$cc_pf_one_raise_ordinary_srp" in ordinary
    assert "f$cc_pot_family_id = 2" in iso and "f$cc_pf_iso_proven" in iso
    assert "f$cc_pot_family_id = 3" in plain and "f$cc_pf_3bet_plain_proven" in plain
    assert "!f$cc_pf_squeeze_proven" in plain
    assert "f$cc_pot_family_id = 3" in squeeze and "f$cc_pf_squeeze_proven" in squeeze
    assert "!f$cc_pf_3bet_plain_proven" in squeeze
    assert "f$cc_pot_family_id = 4" in four and "f$cc_pf_role_4bettor" in four

    # 2) Every implemented strategic family has an explicit top-level coverage owner.
    coverage = block(ROUTER, "f$cc_turn_cbet_strategy_covered")
    required_owners = (
        "f$cc_turn_iso_covered",
        "f$cc_turn_plain3bp_covered",
        "f$cc_turn_squeeze_covered",
        "f$cc_turn_4bp_covered",
        "f$cc_turn_srp_postmw_hu_covered",
        "f$cc_turn_mw_srp_covered",
        "f$cc_turn_srp_ip_source_anchored_covered",
        "f$cc_turn_srp_oop_source_anchored_covered",
        "f$cc_turn_srp_6max_gap_covered",
    )
    for token in required_owners:
        assert token in coverage, f"missing Turn-CBet coverage owner: {token}"

    # 3) All those owners must route both action and size, with generic false/0 tails.
    action_router = block(ROUTER, "f$cc_turn_cbet_router")
    size_router = block(ROUTER, "f$cc_turn_cbet_size_id")
    assert "When Others Return false Force" in action_router
    assert "When Others Return 0 Force" in size_router
    for owner in required_owners:
        assert owner in action_router, f"coverage owner not action-routed: {owner}"
        assert owner in size_router, f"coverage owner not size-routed: {owner}"

    # 4) Residual ordinary-SRP diagnostics remain outside strategy coverage.
    for residual in (
        "f$cc_turn_cbet_srp_ip_uncovered_range_context",
        "f$cc_turn_cbet_srp_oop_uncovered_context",
    ):
        assert residual not in coverage, f"residual gap accidentally marked covered: {residual}"
        assert residual not in action_router, f"residual gap accidentally routed: {residual}"
        assert residual not in size_router, f"residual gap accidentally sized: {residual}"

    # 5) Clean 4BP stays HU-only and rejects postflop-reduced/multiway-origin states.
    four_base = block(FOUR, "f$cc_turn_4bp_context")
    assert "f$cc_hu" in four_base
    assert "!f$cc_hu_origin_postflop_reduced" in four_base
    assert "f$cc_hu_4bp_survivor_type_id < 3" in four_base

    # 6) Seven strategic size IDs are the entire common Turn domain.
    expected = {
        "f$cc_turn_size_25_id": "1",
        "f$cc_turn_size_33_id": "2",
        "f$cc_turn_size_40_id": "3",
        "f$cc_turn_size_50_id": "4",
        "f$cc_turn_size_625_id": "5",
        "f$cc_turn_size_75_id": "6",
        "f$cc_turn_size_100_id": "7",
    }
    for name, value in expected.items():
        body = first_executable_line(block(COMMON, name))
        assert body == value, f"unexpected size-ID definition {name}: {body!r}"

    # Strategy files may only return the seven canonical Turn size helpers (or 0).
    allowed_helpers = set(expected)
    size_ref_re = re.compile(r"f\$cc_turn_size_[A-Za-z0-9_]+_id")
    for path in all_turn_strategy_files():
        text = path.read_text(encoding="utf-8")
        for ref in size_ref_re.findall(text):
            assert ref in allowed_helpers, f"noncanonical Turn size helper {ref} in {path.name}"

    # 7) Family IDs 1..12 are explicit. IDs 5/6 remain diagnostic residual gaps;
    # their presence here does NOT make them strategy-covered (asserted above).
    family = block(ROUTER, "f$cc_turn_cbet_family_id")
    assert "When Others Return 0 Force" in family
    for value in range(1, 13):
        assert f"Return {value} Force" in family

    print("PASS: Gate02J.0 Turn-CBet coverage/exclusivity/fail-closed contract")


if __name__ == "__main__":
    main()
