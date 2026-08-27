#!/usr/bin/env python3
"""Gate07J Flop Donk runtime sizing / all-in-equivalence contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BET = (ROOT / "src" / "CashCrusher_Flop_Donk_Betsize.txt").read_text(encoding="utf-8")
GEO = (ROOT / "src" / "CashCrusher_Flop_Donk_StackGeometry.txt").read_text(encoding="utf-8")
ALL = (ROOT / "src" / "CashCrusher_Flop_Donk_AllinEquivalence.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def native_map_contract() -> None:
    frac = block(BET, "f$cc_flop_donk_requested_pot_fraction")
    assert "f$cc_flop_donk_size_id = 1 Return 0.50 Force" in frac
    assert "f$cc_flop_donk_size_id = 2 Return 0.75 Force" in frac
    assert "f$cc_flop_donk_size_id = 3 Return 1.00 Force" in frac

    size = block(BET, "f$cc_flop_donk_requested_betsize")
    assert "f$cc_flop_donk_size_id = 1 Return BetHalfPot Force" in size
    assert "f$cc_flop_donk_size_id = 2 Return BetThreeFourthPot Force" in size
    assert "f$cc_flop_donk_size_id = 3 Return BetPot Force" in size


def geometry_contract() -> None:
    clean = block(GEO, "f$cc_flop_donk_stackgeom_clean")
    for token in ("AmountToCall = 0", "currentbet = 0", "potplayer = 0"):
        assert token in clean

    deep = executable(block(GEO, "f$cc_flop_donk_requested_mw_deepest_ratio"))
    shallow = executable(block(GEO, "f$cc_flop_donk_requested_mw_shallowest_ratio"))
    assert "f$cc_mw_deepest_effective_stack_round_start_bb" in deep
    assert "f$cc_mw_shallowest_effective_stack_round_start_bb" in shallow

    sidepot = block(GEO, "f$cc_flop_donk_mw_sidepot_divergence_candidate")
    assert "f$cc_flop_donk_requested_reaches_mw_shallowest" in sidepot
    assert "!f$cc_flop_donk_requested_reaches_mw_deepest" in sidepot

    hist = executable(block(GEO, "f$cc_flop_donk_historical_near_allin_review"))
    assert ">= 0.50" in hist
    assert "Return true Force" in hist
    assert "BetMax" not in hist


def allin_contract() -> None:
    nat = block(ALL, "f$cc_flop_donk_natural_allin_equivalent")
    assert "f$cc_flop_donk_requested_reaches_hero_stack Return true Force" in nat
    assert "f$cc_flop_donk_requested_reaches_all_live_effective Return true Force" in nat
    assert "historical_near_allin" not in nat
    assert "shallowest" not in nat.lower()

    live = block(ALL, "f$cc_flop_donk_requested_reaches_all_live_effective")
    assert "f$cc_flop_donk_requested_reaches_hu_effective" in live
    assert "f$cc_flop_donk_requested_reaches_mw_deepest" in live
    assert "shallowest" not in live.lower()

    execution = block(ALL, "f$cc_flop_donk_execution_betsize")
    assert "f$cc_flop_donk_natural_allin_equivalent Return BetMax Force" in execution
    assert "When Others Return f$cc_flop_donk_requested_betsize Force" in execution
    for token in (
        "user_cc_flop_donk_plan_size_50",
        "user_cc_flop_donk_plan_size_75",
        "user_cc_flop_donk_plan_size_100",
        "user_cc_flop_donk_plan_expected_allin",
    ):
        assert token in execution

    side = block(ALL, "f$cc_flop_donk_sidepot_divergence_not_promoted")
    assert "f$cc_flop_donk_natural_allin_equivalent Return false Force" in side


def prohibited_generic_commitment_contract() -> None:
    code = executable(BET + "\n" + GEO + "\n" + ALL)
    for forbidden in ("Raise_Committed", "StackOffDraws", "user_TurnShove"):
        assert forbidden.lower() not in code.lower(), f"forbidden runtime leak: {forbidden}"


if __name__ == "__main__":
    native_map_contract()
    geometry_contract()
    allin_contract()
    prohibited_generic_commitment_contract()
    print("PASS: Gate07J Flop Donk runtime sizing contract")
