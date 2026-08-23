#!/usr/bin/env python3
"""Deterministic Gate02I source/routing tests for clean HU 4BP Turn CBet."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = (ROOT / "src" / "CashCrusher_Turn_4BP_Context.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_Turn_CBet_4BP.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_CBet.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def main() -> None:
    # Gate02I is intentionally clean HU only. Postflop-reduced HU from a multiway
    # 4BP flop must remain outside this policy until multiway-4BP flop itself exists.
    base = block(CTX, "f$cc_turn_4bp_context")
    assert "f$cc_hu" in base
    assert "!f$cc_hu_origin_postflop_reduced" in base
    assert "f$cc_hu_4bp_survivor_consistent" in base
    assert "f$cc_hu_4bp_survivor_type_id < 3" in base
    assert "f$cc_turn_cbet_hu_spr_valid" in base

    # All four supported clean families must be explicit and mutually owned.
    for fn in (
        "f$cc_turn_4bp_truehu_opener4_vs_threebettor",
        "f$cc_turn_4bp_opener4_vs_threebettor",
        "f$cc_turn_4bp_cold4_vs_opener",
        "f$cc_turn_4bp_cold4_vs_threebettor",
    ):
        assert f"##{fn}##" in CTX, f"missing clean 4BP turn family: {fn}"

    consistent = block(CTX, "f$cc_turn_4bp_context_consistent")
    assert "!= 1 Return false Force" in consistent

    # Natural low-SPR descriptors are allowed, but they are geometry facts only.
    for fn in (
        "f$cc_turn_4bp_spr_below_1",
        "f$cc_turn_4bp_spr_below_15",
        "f$cc_turn_4bp_spr_below_2",
    ):
        assert f"##{fn}##" in CTX

    exe = executable(POL)
    assert "BetMax" not in exe, "Turn 4BP policy must not embed blanket strategic jam"
    assert "f$Raise_Committed" not in exe

    # Cold4-v-opener must remain tighter than opener4 family: first baseline has
    # explicit pure-air refusal rather than inheriting opener4 air tail.
    cold_open = block(POL, "f$cc_turn_4bp_cold4_vs_opener_action")
    assert "When f$cc_turn_cbet_air Return false Force" in cold_open

    # Size map may request 75 at low SPR, but execution ownership stays downstream.
    opener_size = block(POL, "f$cc_turn_4bp_opener4_size_id")
    assert "f$cc_turn_4bp_spr_below_1" in opener_size
    assert "f$cc_turn_size_75_id" in opener_size

    # Router must own clean 4BP explicitly and before ordinary SRP fallbacks.
    route = "When f$cc_turn_4bp_covered Return f$cc_turn_4bp_action Force"
    srp = "When f$cc_turn_srp_ip_source_anchored_covered Return f$cc_turn_srp_ip_source_anchored_action Force"
    assert route in ROUTER and srp in ROUTER
    assert ROUTER.index(route) < ROUTER.index(srp)
    assert "f$cc_turn_4bp_size_id" in block(ROUTER, "f$cc_turn_cbet_size_id")
    assert "f$cc_turn_4bp_covered" in block(ROUTER, "f$cc_turn_cbet_strategy_covered")

    print("PASS: Gate02I clean HU 4BP Turn-CBet source/routing contract")


if __name__ == "__main__":
    main()
