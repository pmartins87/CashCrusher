#!/usr/bin/env python3
"""Gate03C deterministic source-boundary/routing tests for P-heavy SRP River gaps."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
COMMON = (SRC / "CashCrusher_River_CBet_Common.txt").read_text(encoding="utf-8")
GAPS = (SRC / "CashCrusher_River_CBet_SRP_6MaxGaps.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_River_CBet.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def main() -> None:
    # Gate02 family2 must split BB from SB explicitly.
    bb = block(GAPS, "f$cc_river_srp_gap_ip_vs_bb_context")
    sb = block(GAPS, "f$cc_river_srp_gap_ip_vs_sb_context")
    assert "f$cc_river_turn_family_id = 2" in bb and "f$cc_hu_villain_pos_id = 6" in bb
    assert "f$cc_river_turn_family_id = 2" in sb and "f$cc_hu_villain_pos_id = 5" in sb

    # PFA OOP/nonblind must remain family4 and never borrow blind families.
    oop = block(GAPS, "f$cc_river_srp_gap_oop_nonblind_context")
    assert "f$cc_river_turn_family_id = 4" in oop
    assert "f$cc_hu_oop" in oop
    assert "f$cc_hu_villain_pos_id >= 2" in oop and "f$cc_hu_villain_pos_id <= 4" in oop

    # Multiway-origin distinctions must remain explicit on River.
    assert "f$cc_river_turn_family_id = 7" in block(GAPS, "f$cc_river_srp_postflopmw_turnhu_context")
    nowhu = block(GAPS, "f$cc_river_srp_turnmw_nowhu_context")
    stillmw = block(GAPS, "f$cc_river_srp_turnmw_stillmw_context")
    assert "f$cc_river_turn_family_id = 8" in nowhu and "f$cc_river_turn_mw_now_hu" in nowhu
    assert "f$cc_river_turn_family_id = 8" in stillmw and "f$cc_river_turn_mw_still_mw" in stillmw

    # Multiway low-SPR helpers must use deepest-effective River SPR.
    deep2 = block(GAPS, "f$cc_river_mw_all_effective_spr_below_2")
    assert "f$cc_mw_spr_deepest_round_start" in deep2
    exe = executable(GAPS)
    assert "f$cc_mw_spr_shallowest_round_start" not in exe

    # No BetMax/global stackoff shortcut in this strategy gate.
    assert "BetMax" not in exe
    assert "f$Raise_Committed" not in exe
    assert "f$allin_on_betsize_balance_ratio" not in exe

    # Selected ranges: no generic air in SB/OOP/post-multiway/multiway descendants.
    for name in (
        "f$cc_river_srp_gap_ip_vs_sb_action",
        "f$cc_river_srp_gap_oop_nonblind_action",
        "f$cc_river_srp_postflopmw_turnhu_action",
        "f$cc_river_srp_turnmw_nowhu_action",
        "f$cc_river_srp_turnmw_stillmw_action",
    ):
        b = block(GAPS, name)
        assert "f$cc_river_no_made Return false Force" in b, f"{name} missing explicit no-made fail-close"

    # BB receives only a narrow blocker/high-pressure missed-draw bluff selector.
    bbaction = block(GAPS, "f$cc_river_srp_gap_ip_vs_bb_action")
    assert "f$cc_river_turn_had_draw" in bbaction
    assert "f$cc_river_srp_gap_high_pressure" in bbaction
    assert "f$cc_hole_has_ace || f$cc_hole_has_king" in bbaction

    # Router must give source ancestry precedence, then P-heavy gaps.
    action = block(ROUTER, "f$cc_river_cbet_router")
    source_line = "When f$cc_river_srp_source_covered Return f$cc_river_srp_source_action Force"
    gap_line = "When f$cc_river_srp_gap_covered Return f$cc_river_srp_gap_action Force"
    assert source_line in action and gap_line in action
    assert action.index(source_line) < action.index(gap_line)

    assert "f$cc_river_srp_gap_size_id" in block(ROUTER, "f$cc_river_cbet_size_id")
    assert "f$cc_river_srp_gap_covered" in block(ROUTER, "f$cc_river_cbet_strategy_covered")

    print("PASS: Gate03C P-heavy SRP River-CBet provenance/routing contract")


if __name__ == "__main__":
    main()
