#!/usr/bin/env python3
"""Deterministic Gate02F tests for isolation-pot Turn-CBet boundaries."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = (ROOT / "src" / "CashCrusher_Turn_ISO_Context.txt").read_text(encoding="utf-8")
POLICY = (ROOT / "src" / "CashCrusher_Turn_CBet_ISO.txt").read_text(encoding="utf-8")
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
    # HU Turn ISO must classify limper vs post-raise coldcaller independently of
    # whether HU existed on flop or arose after a multiway flop.
    for token in (
        "##f$cc_turn_iso_hu_villain_was_limper##",
        "##f$cc_turn_iso_hu_villain_was_coldcaller##",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_hu_origin_postflop_reduced",
    ):
        assert token in CTX, f"missing ISO HU provenance token: {token}"

    consistent = block(CTX, "f$cc_turn_iso_hu_context_consistent")
    assert "(f$cc_turn_iso_hu_villain_was_limper + f$cc_turn_iso_hu_villain_was_coldcaller) != 1" in consistent

    # MW field must be exhaustively explained by limper/coldcaller masks.
    mw = block(CTX, "f$cc_turn_iso_mw_context_consistent")
    assert "f$cc_turn_iso_mw_live_limper_count + f$cc_turn_iso_mw_live_coldcaller_count" in mw
    assert "nplayersplaying - 1" in mw
    assert "f$cc_mw_spr_bounds_valid" in mw

    exe = executable(POLICY)
    assert "BetMax" not in exe
    assert "f$cc_spr_round_start" not in exe, "MW/HU ISO policy should use exact helper boundaries, not generic leak"
    assert "f$cc_mw_spr_shallowest_round_start" not in exe

    # Coldcaller policy must be visibly separate and must not include pure-air barrel.
    cold = block(POLICY, "f$cc_turn_iso_hu_coldcaller_action")
    assert "f$cc_turn_iso_hu_villain_was_coldcaller" in cold
    assert "When f$cc_turn_cbet_air Return false Force" in cold

    # Multiway ISO baseline must use deepest-effective-derived helpers and no air.
    mwpol = block(POLICY, "f$cc_turn_iso_mw_action")
    assert "f$cc_turn_iso_mw_all_effective_spr_below_4" in mwpol
    assert "When f$cc_turn_cbet_air Return false Force" in mwpol

    # Router must dispatch ISO before ordinary SRP families.
    iso = "When f$cc_turn_iso_covered Return f$cc_turn_iso_action Force"
    srp = "When f$cc_turn_srp_ip_source_anchored_covered Return f$cc_turn_srp_ip_source_anchored_action Force"
    assert iso in ROUTER and srp in ROUTER
    assert ROUTER.index(iso) < ROUTER.index(srp)
    assert "f$cc_turn_iso_size_id" in block(ROUTER, "f$cc_turn_cbet_size_id")
    assert "f$cc_turn_iso_covered" in block(ROUTER, "f$cc_turn_cbet_strategy_covered")

    print("PASS: Gate02F ISO Turn-CBet provenance/source-boundary contract")


if __name__ == "__main__":
    main()
