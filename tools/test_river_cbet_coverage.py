#!/usr/bin/env python3
"""Gate03 canonical River-CBet coverage/exclusivity source contract."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ROUTER = (SRC / "CashCrusher_River_CBet.txt").read_text(encoding="utf-8")
COMMON = (SRC / "CashCrusher_River_CBet_Common.txt").read_text(encoding="utf-8")
SOURCE = (SRC / "CashCrusher_River_CBet_SRP_Source.txt").read_text(encoding="utf-8")
GAPS = (SRC / "CashCrusher_River_CBet_SRP_6MaxGaps.txt").read_text(encoding="utf-8")
ISO_CTX = (SRC / "CashCrusher_River_ISO_Context.txt").read_text(encoding="utf-8")
P3_CTX = (SRC / "CashCrusher_River_3BP_Context.txt").read_text(encoding="utf-8")
SQ_CTX = (SRC / "CashCrusher_River_Squeeze_Context.txt").read_text(encoding="utf-8")
P4_CTX = (SRC / "CashCrusher_River_4BP_Context.txt").read_text(encoding="utf-8")

STRATEGY_FILES = [
    SRC / "CashCrusher_River_CBet_SRP_Source.txt",
    SRC / "CashCrusher_River_CBet_SRP_6MaxGaps.txt",
    SRC / "CashCrusher_River_CBet_ISO.txt",
    SRC / "CashCrusher_River_CBet_3BP.txt",
    SRC / "CashCrusher_River_CBet_Squeeze.txt",
    SRC / "CashCrusher_River_CBet_4BP.txt",
]


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def main() -> None:
    # Strict actual-action parent is mandatory.
    assert "f$cc_hist_river_standard_cbet_parent_valid" in block(COMMON, "f$cc_river_cbet_opportunity")

    # Source-anchored SRP contexts consume only source Turn families 1/3.
    source_exe = executable(SOURCE)
    family_ids = set(int(x) for x in re.findall(r"f\$cc_river_turn_family_id\s*=\s*(\d+)", source_exe))
    assert family_ids <= {1, 3}, f"unexpected source-SRP Turn families: {family_ids}"

    # P-heavy SRP gaps own only family 2/4/7/8.
    gap_exe = executable(GAPS)
    gap_ids = set(int(x) for x in re.findall(r"f\$cc_river_turn_family_id\s*=\s*(\d+)", gap_exe))
    assert gap_ids == {2, 4, 7, 8}, f"unexpected/missing P-heavy SRP Turn families: {gap_ids}"

    # Other-pot contexts are exact Gate02 families and cannot overlap.
    assert "f$cc_river_turn_family_id = 9" in block(ISO_CTX, "f$cc_river_iso_base_context")
    assert "f$cc_river_turn_family_id = 10" in block(P3_CTX, "f$cc_river_plain3bp_base_context")
    assert "f$cc_river_turn_family_id = 11" in block(SQ_CTX, "f$cc_river_squeeze_base_context")
    assert "f$cc_river_turn_family_id = 12" in block(P4_CTX, "f$cc_river_4bp_base_context")

    # Turn residual diagnostic families 5/6 had no reviewed Turn bet owner and may
    # never be promoted into canonical River CBet routing.
    router_exe = executable(ROUTER)
    assert "f$cc_river_turn_family_id = 5" not in router_exe
    assert "f$cc_river_turn_family_id = 6" not in router_exe

    # Every supported top-level family has action + size + coverage wiring.
    action = block(ROUTER, "f$cc_river_cbet_router")
    size = block(ROUTER, "f$cc_river_cbet_size_id")
    covered = block(ROUTER, "f$cc_river_cbet_strategy_covered")
    expected = (
        ("f$cc_river_srp_source_covered", "f$cc_river_srp_source_action", "f$cc_river_srp_source_size_id"),
        ("f$cc_river_srp_gap_covered", "f$cc_river_srp_gap_action", "f$cc_river_srp_gap_size_id"),
        ("f$cc_river_iso_covered", "f$cc_river_iso_action", "f$cc_river_iso_size_id"),
        ("f$cc_river_plain3bp_covered", "f$cc_river_plain3bp_action", "f$cc_river_plain3bp_size_id"),
        ("f$cc_river_squeeze_covered", "f$cc_river_squeeze_action", "f$cc_river_squeeze_size_id"),
        ("f$cc_river_4bp_covered", "f$cc_river_4bp_action", "f$cc_river_4bp_size_id"),
    )
    for cov, act, sz in expected:
        assert f"When {cov} Return {act} Force" in action
        assert f"When {cov} Return {sz} Force" in size
        assert cov in covered

    # Positive River strategies may only use the frozen 25/33/50/75/100 IDs.
    allowed = {"25", "33", "50", "75", "100"}
    for path in STRATEGY_FILES:
        text = executable(path.read_text(encoding="utf-8"))
        used = set(re.findall(r"f\$cc_river_size_([0-9]+)_id", text))
        assert used <= allowed, f"{path.name} uses non-frozen River size(s): {used - allowed}"

    # The top-level action/size integrity invariant is present and fail-closed.
    consistent = block(ROUTER, "f$cc_river_cbet_size_consistent")
    assert "When !f$cc_river_cbet_router Return f$cc_river_cbet_size_id = 0 Force" in consistent
    assert "When f$cc_river_cbet_router Return f$cc_river_cbet_size_id > 0 Force" in consistent

    print("PASS: Gate03 canonical River-CBet coverage/exclusivity contract")


if __name__ == "__main__":
    main()
