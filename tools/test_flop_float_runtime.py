#!/usr/bin/env python3
"""Gate04G deterministic Flop Float sizing/mechanical-all-in tests."""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
BET = (SRC / "CashCrusher_Flop_Float_Betsize.txt").read_text(encoding="utf-8")
GEO = (SRC / "CashCrusher_Flop_Float_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_Flop_Float_AllinEquivalence.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


FRACTIONS = {1: 0.25, 2: 0.333, 3: 0.50, 4: 0.75, 5: 1.00}


@dataclass(frozen=True)
class Case:
    size_id: int
    pot_bb: float
    hero_bb: float
    hu_eff_bb: float | None = None
    mw_shallow_bb: float | None = None
    mw_deep_bb: float | None = None


def requested(c: Case) -> float:
    return FRACTIONS[c.size_id] * c.pot_bb


def natural_allin(c: Case) -> bool:
    bet = requested(c)
    if bet >= c.hero_bb:
        return True
    if c.hu_eff_bb is not None:
        return bet >= c.hu_eff_bb
    if c.mw_deep_bb is not None:
        return bet >= c.mw_deep_bb
    return False


def run_math_cases() -> None:
    # 75% can be a large fraction of remaining stack without being all-in.
    c = Case(size_id=4, pot_bb=40, hero_bb=50, hu_eff_bb=50)
    assert requested(c) == 30
    assert requested(c) / c.hero_bb >= 0.50
    assert not natural_allin(c)

    # Natural Hero-stack exhaustion.
    c = Case(size_id=5, pot_bb=25, hero_bb=25, hu_eff_bb=40)
    assert natural_allin(c)

    # Hero covers a shorter sole HU Villain.
    c = Case(size_id=4, pot_bb=40, hero_bb=100, hu_eff_bb=28)
    assert requested(c) == 30
    assert natural_allin(c)

    # Short multiway sidepot alone must not promote whole action.
    c = Case(size_id=3, pot_bb=30, hero_bb=100, mw_shallow_bb=12, mw_deep_bb=55)
    assert requested(c) == 15
    assert requested(c) >= c.mw_shallow_bb
    assert requested(c) < c.mw_deep_bb
    assert not natural_allin(c)

    # Deepest/all-live multiway relation reached.
    c = Case(size_id=5, pot_bb=60, hero_bb=100, mw_shallow_bb=18, mw_deep_bb=55)
    assert natural_allin(c)


def run_source_contract() -> None:
    mapping = block(BET, "f$cc_flop_float_requested_betsize")
    required = (
        "When f$cc_flop_float_size_id = 1 RaiseBy 25% Force",
        "When f$cc_flop_float_size_id = 2 Return BetThirdPot Force",
        "When f$cc_flop_float_size_id = 3 Return BetHalfPot Force",
        "When f$cc_flop_float_size_id = 4 Return BetThreeFourthPot Force",
        "When f$cc_flop_float_size_id = 5 Return BetPot Force",
    )
    for line in required:
        assert line in mapping, f"missing Float size mapping: {line}"
    assert "BetMax" not in mapping

    clean = block(GEO, "f$cc_flop_float_stackgeom_clean")
    for token in ("AmountToCall = 0", "currentbet = 0", "potplayer = 0"):
        assert token in clean

    natural = block(ALLIN, "f$cc_flop_float_natural_allin_equivalent")
    assert "f$cc_flop_float_historical_near_allin_review" not in natural
    assert "f$cc_flop_float_requested_reaches_hero_stack" in natural
    assert "f$cc_flop_float_requested_reaches_all_live_effective" in natural

    all_live = block(ALLIN, "f$cc_flop_float_requested_reaches_all_live_effective")
    assert "f$cc_flop_float_requested_reaches_mw_deepest" in all_live
    assert "f$cc_flop_float_requested_reaches_mw_shallowest" not in all_live

    sidepot = block(ALLIN, "f$cc_flop_float_sidepot_divergence_not_promoted")
    assert "f$cc_flop_float_mw_sidepot_divergence_candidate" in sidepot
    assert "f$cc_flop_float_natural_allin_equivalent Return false Force" in sidepot

    execution = block(ALLIN, "f$cc_flop_float_execution_betsize")
    for suffix in ("25", "33", "50", "75", "100"):
        assert f"Set user_cc_flop_float_plan_size_{suffix}" in execution
    assert "When f$cc_flop_float_natural_allin_equivalent Return BetMax Force" in execution
    assert "When Others Return f$cc_flop_float_requested_betsize Force" in execution

    marker_check = block(ALLIN, "f$cc_flop_float_plan_markers_consistent")
    assert "f$cc_flop_float_natural_allin_equivalent" not in marker_check
    assert "f$cc_flop_float_plan_size_marker_count != 1" in marker_check


if __name__ == "__main__":
    run_math_cases()
    run_source_contract()
    print("PASS: Gate04G Flop Float runtime + natural all-in equivalence contract")
