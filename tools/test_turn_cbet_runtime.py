#!/usr/bin/env python3
"""Gate02J.1/J.2 deterministic Turn-CBet execution contract tests.

These tests validate mapping and mechanical stack geometry. They deliberately do
not certify a global f$BestBetsize callback or OpenHoldem replay execution.
"""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
BET = (SRC / "CashCrusher_Turn_CBet_Betsize.txt").read_text(encoding="utf-8")
GEO = (SRC / "CashCrusher_Turn_CBet_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_Turn_CBet_AllinEquivalence.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


FRACTIONS = {1: 0.25, 2: 0.333, 3: 0.40, 4: 0.50, 5: 0.625, 6: 0.75, 7: 1.00}


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
    # Ordinary deep HU: 75% pot may cross historical 50%-stack diagnostics yet
    # still must remain a normal bet if it does not reach Hero/effective stack.
    c = Case(size_id=6, pot_bb=40, hero_bb=50, hu_eff_bb=50)
    assert requested(c) == 30
    assert requested(c) / c.hero_bb >= 0.50
    assert not natural_allin(c)

    # Natural Hero-stack exhaustion: pot bet 30 into 30 remaining.
    c = Case(size_id=7, pot_bb=30, hero_bb=30, hu_eff_bb=45)
    assert natural_allin(c)

    # Hero covers short HU Villain: requested size reaches Villain effective stack.
    c = Case(size_id=6, pot_bb=40, hero_bb=100, hu_eff_bb=28)
    assert requested(c) == 30
    assert natural_allin(c)

    # Multiway shortest-only reach: one 12bb sidepot player, another 55bb deep.
    c = Case(size_id=4, pot_bb=30, hero_bb=100, mw_shallow_bb=12, mw_deep_bb=55)
    assert requested(c) == 15
    assert requested(c) >= c.mw_shallow_bb
    assert requested(c) < c.mw_deep_bb
    assert not natural_allin(c)

    # Multiway reaches the deepest/all-live effective relation -> equivalent.
    c = Case(size_id=7, pot_bb=60, hero_bb=100, mw_shallow_bb=18, mw_deep_bb=55)
    assert requested(c) == 60
    assert natural_allin(c)

    # Exact non-native 62.5% arithmetic.
    c = Case(size_id=5, pot_bb=24, hero_bb=100, hu_eff_bb=100)
    assert requested(c) == 15
    assert not natural_allin(c)


def run_source_contract() -> None:
    # Exact OpenPPL mapping. Non-native fractions use verified RaiseBy X% syntax.
    mapping = block(BET, "f$cc_turn_cbet_requested_betsize")
    required = (
        "When f$cc_turn_cbet_size_id = 1 RaiseBy 25% Force",
        "When f$cc_turn_cbet_size_id = 2 Return BetThirdPot Force",
        "When f$cc_turn_cbet_size_id = 3 RaiseBy 40% Force",
        "When f$cc_turn_cbet_size_id = 4 Return BetHalfPot Force",
        "When f$cc_turn_cbet_size_id = 5 RaiseBy 62.5% Force",
        "When f$cc_turn_cbet_size_id = 6 Return BetThreeFourthPot Force",
        "When f$cc_turn_cbet_size_id = 7 Return BetPot Force",
    )
    for line in required:
        assert line in mapping, f"missing Turn runtime size mapping: {line}"
    assert "BetMax" not in mapping

    # Clean geometry must be initial-bet only.
    clean = block(GEO, "f$cc_turn_cbet_stackgeom_clean")
    for token in ("AmountToCall = 0", "currentbet = 0", "potplayer = 0"):
        assert token in clean

    # Historical thresholds are diagnostics only; natural equivalence must not
    # reference them.
    natural = block(ALLIN, "f$cc_turn_cbet_natural_allin_equivalent")
    assert "f$cc_turn_cbet_hist_hero_balance_50_trigger" not in natural
    assert "f$cc_turn_cbet_hist_hero_stack_60_trigger" not in natural
    assert "f$cc_turn_cbet_hist_hu_effective_50_trigger" not in natural
    assert "f$cc_turn_cbet_hist_mw_effective_50_trigger" not in natural
    assert "f$cc_turn_cbet_requested_reaches_hero_stack" in natural
    assert "f$cc_turn_cbet_requested_reaches_all_live_effective" in natural

    # Whole-field MW equivalence must use deepest, not shortest.
    all_live = block(ALLIN, "f$cc_turn_cbet_requested_reaches_all_live_effective")
    assert "f$cc_turn_cbet_requested_reaches_mw_deepest" in all_live
    assert "f$cc_turn_cbet_requested_reaches_mw_shallowest" not in all_live

    sidepot = block(ALLIN, "f$cc_turn_cbet_sidepot_divergence_not_promoted")
    assert "f$cc_turn_cbet_mw_sidepot_divergence_candidate" in sidepot
    assert "f$cc_turn_cbet_natural_allin_equivalent Return false Force" in sidepot

    # Execution stores exactly seven plan-size markers and only then chooses
    # natural BetMax or the requested strategic size.
    execution = block(ALLIN, "f$cc_turn_cbet_execution_betsize")
    for suffix in ("25", "33", "40", "50", "625", "75", "100"):
        assert f"Set user_cc_turn_cbet_plan_size_{suffix}" in execution
    assert "When f$cc_turn_cbet_natural_allin_equivalent Return BetMax Force" in execution
    assert "When Others Return f$cc_turn_cbet_requested_betsize Force" in execution

    # Stored marker validation must be cross-street stable: it cannot recompute
    # current Turn natural-allin geometry after cards/pot/SPR changed on River.
    markers = block(ALLIN, "f$cc_turn_cbet_plan_markers_consistent")
    assert "f$cc_turn_cbet_natural_allin_equivalent" not in markers
    assert "f$cc_turn_cbet_plan_size_marker_count != 1" in markers


if __name__ == "__main__":
    run_math_cases()
    run_source_contract()
    print("PASS: Gate02J Turn-CBet runtime sizing + natural all-in equivalence contract")
