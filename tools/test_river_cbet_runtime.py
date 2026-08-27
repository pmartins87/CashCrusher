#!/usr/bin/env python3
"""Gate03H deterministic River-CBet execution contract tests.

These tests validate the five-size OpenPPL mapping and mechanical stack/all-in
geometry. They do not certify a global f$BestBetsize callback or table replay.
"""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
BET = (SRC / "CashCrusher_River_CBet_Betsize.txt").read_text(encoding="utf-8")
GEO = (SRC / "CashCrusher_River_CBet_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_River_CBet_AllinEquivalence.txt").read_text(encoding="utf-8")


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
    # 75% River bet can cross a historical 50%-stack diagnostic while remaining
    # a normal bet if neither Hero nor the effective stack is reached.
    c = Case(size_id=4, pot_bb=40, hero_bb=50, hu_eff_bb=50)
    assert requested(c) == 30
    assert requested(c) / c.hero_bb >= 0.50
    assert not natural_allin(c)

    # Pot-sized River value bet exactly exhausts Hero's remaining stack.
    c = Case(size_id=5, pot_bb=24, hero_bb=24, hu_eff_bb=40)
    assert requested(c) == 24
    assert natural_allin(c)

    # Hero covers a shorter HU Villain; reviewed 75% already covers effective.
    c = Case(size_id=4, pot_bb=40, hero_bb=100, hu_eff_bb=28)
    assert requested(c) == 30
    assert natural_allin(c)

    # Shortest-only multiway reach: 15 covers 12bb sidepot player but not 55bb
    # deepest live relationship, therefore no whole-bet BetMax promotion.
    c = Case(size_id=3, pot_bb=30, hero_bb=100, mw_shallow_bb=12, mw_deep_bb=55)
    assert requested(c) == 15
    assert requested(c) >= c.mw_shallow_bb
    assert requested(c) < c.mw_deep_bb
    assert not natural_allin(c)

    # Pot bet reaches every live multiway effective relationship.
    c = Case(size_id=5, pot_bb=60, hero_bb=100, mw_shallow_bb=18, mw_deep_bb=55)
    assert requested(c) == 60
    assert natural_allin(c)

    # Quarter-pot mapping remains normal at deep River geometry.
    c = Case(size_id=1, pot_bb=40, hero_bb=100, hu_eff_bb=100)
    assert requested(c) == 10
    assert not natural_allin(c)


def run_source_contract() -> None:
    mapping = block(BET, "f$cc_river_cbet_requested_betsize")
    required = (
        "When f$cc_river_cbet_size_id = 1 RaiseBy 25% Force",
        "When f$cc_river_cbet_size_id = 2 Return BetThirdPot Force",
        "When f$cc_river_cbet_size_id = 3 Return BetHalfPot Force",
        "When f$cc_river_cbet_size_id = 4 Return BetThreeFourthPot Force",
        "When f$cc_river_cbet_size_id = 5 Return BetPot Force",
    )
    for line in required:
        assert line in mapping, f"missing River runtime mapping: {line}"
    assert "BetMax" not in mapping

    clean = block(GEO, "f$cc_river_cbet_stackgeom_clean")
    for token in ("AmountToCall = 0", "currentbet = 0", "potplayer = 0"):
        assert token in clean

    # Historical thresholds are diagnostic only.
    natural = block(ALLIN, "f$cc_river_cbet_natural_allin_equivalent")
    for token in (
        "f$cc_river_cbet_hist_hero_balance_50_trigger",
        "f$cc_river_cbet_hist_hero_stack_60_trigger",
        "f$cc_river_cbet_hist_hu_effective_50_trigger",
        "f$cc_river_cbet_hist_mw_effective_50_trigger",
    ):
        assert token not in natural, f"historical threshold leaked into River BetMax: {token}"
    assert "f$cc_river_cbet_requested_reaches_hero_stack" in natural
    assert "f$cc_river_cbet_requested_reaches_all_live_effective" in natural

    # Whole-field MW equivalence uses deepest effective, never shortest-only.
    all_live = block(ALLIN, "f$cc_river_cbet_requested_reaches_all_live_effective")
    assert "f$cc_river_cbet_requested_reaches_mw_deepest" in all_live
    assert "f$cc_river_cbet_requested_reaches_mw_shallowest" not in all_live

    sidepot = block(ALLIN, "f$cc_river_cbet_sidepot_divergence_not_promoted")
    assert "f$cc_river_cbet_mw_sidepot_divergence_candidate" in sidepot
    assert "f$cc_river_cbet_natural_allin_equivalent Return false Force" in sidepot

    # Execution stores five exact plan sizes and only local natural equivalence
    # may turn them into BetMax.
    execution = block(ALLIN, "f$cc_river_cbet_execution_betsize")
    for suffix in ("25", "33", "50", "75", "100"):
        assert f"Set user_cc_river_cbet_plan_size_{suffix}" in execution
    assert "When f$cc_river_cbet_natural_allin_equivalent Return BetMax Force" in execution
    assert "When Others Return f$cc_river_cbet_requested_betsize Force" in execution

    # Marker validation never recomputes geometry after the action.
    markers = block(ALLIN, "f$cc_river_cbet_plan_markers_consistent")
    assert "f$cc_river_cbet_natural_allin_equivalent" not in markers
    assert "f$cc_river_cbet_plan_size_marker_count != 1" in markers


if __name__ == "__main__":
    run_math_cases()
    run_source_contract()
    print("PASS: Gate03H River-CBet runtime sizing + natural all-in equivalence contract")
