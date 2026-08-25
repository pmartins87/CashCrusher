#!/usr/bin/env python3
"""Gate09F/H clean 4BP + River-Donk runtime contracts."""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
FOUR = (SRC / "CashCrusher_River_Donk_4BP.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_River_Donk.txt").read_text(encoding="utf-8")
BET = (SRC / "CashCrusher_River_Donk_Betsize.txt").read_text(encoding="utf-8")
GEO = (SRC / "CashCrusher_River_Donk_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_River_Donk_AllinEquivalence.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


FRACTIONS = {1: 0.25, 2: 0.30, 3: 0.333, 4: 0.50, 5: 0.75, 6: 1.00}


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


def fourbp_contract() -> None:
    xc = block(FOUR, "f$cc_river_donk_4bp_two_street_xc")
    assert "f$cc_hist_river_donk_flop_checkcall_clean" in xc
    assert "f$cc_hist_river_donk_turn_checkcall_clean" in xc

    parent = block(FOUR, "f$cc_river_donk_4bp_parent_id")
    for n in range(1, 5):
        assert f"Return {n} Force" in parent

    caller = block(FOUR, "f$cc_river_donk_4bp_call4_vs_opener4")
    for token in (
        "f$cc_pf_call4_opener4_vs_hero3bettor_proven",
        "f$cc_hu_call4_vs_opener4_context",
        "f$cc_flop_entry_count = 2",
        "f$cc_river_donk_turn_aggressor_pos_id = f$cc_pf_call4_other_raiser_pos_id",
    ):
        assert token in caller

    review = block(FOUR, "f$cc_river_donk_4bp_low_spr_onepair_review")
    assert "f$cc_river_donk_4bp_spr_below_1" in review
    assert "HaveOverPair || f$cc_river_top_pair" in review

    action = block(FOUR, "f$cc_river_donk_4bp_action")
    assert "f$cc_river_donk_4bp_robust_value Return true Force" in action
    assert "low_spr_onepair_review" not in action
    assert "top_pair" not in action.lower() and "overpair" not in action.lower()

    robust = block(FOUR, "f$cc_river_donk_4bp_robust_value")
    assert "HaveNuts Return true Force" in robust
    assert "f$cc_river_four_card_completion Return false Force" in robust
    assert "f$cc_river_donk_contributed_exact_two_pair || HaveSet Return true Force" in robust

    code = executable(FOUR).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "stackoffdraws", "f$game_"):
        assert forbidden not in code, f"legacy leak: {forbidden}"

    family = block(ROUTER, "f$cc_river_donk_family_id")
    assert "f$cc_river_donk_4bp_covered Return 5 Force" in family
    route = block(ROUTER, "f$cc_river_donk_router")
    assert "f$cc_river_donk_4bp_covered Return f$cc_river_donk_4bp_action Force" in route
    size = block(ROUTER, "f$cc_river_donk_size_id")
    assert "f$cc_river_donk_4bp_covered Return f$cc_river_donk_4bp_size_id Force" in size


def runtime_mapping_contract() -> None:
    mapping = block(BET, "f$cc_river_donk_requested_betsize")
    required = (
        "When f$cc_river_donk_size_id = 1 RaiseBy 25% Force",
        "When f$cc_river_donk_size_id = 2 RaiseBy 30% Force",
        "When f$cc_river_donk_size_id = 3 Return BetThirdPot Force",
        "When f$cc_river_donk_size_id = 4 Return BetHalfPot Force",
        "When f$cc_river_donk_size_id = 5 Return BetThreeFourthPot Force",
        "When f$cc_river_donk_size_id = 6 Return BetPot Force",
    )
    for line in required:
        assert line in mapping, f"missing runtime mapping: {line}"
    assert "BetMax" not in mapping

    clean = block(GEO, "f$cc_river_donk_stackgeom_clean")
    for token in ("AmountToCall = 0", "currentbet = 0", "potplayer = 0"):
        assert token in clean

    natural = block(ALLIN, "f$cc_river_donk_natural_allin_equivalent")
    for token in (
        "f$cc_river_donk_hist_hero_balance_50_trigger",
        "f$cc_river_donk_hist_hero_stack_60_trigger",
        "f$cc_river_donk_hist_hu_effective_50_trigger",
        "f$cc_river_donk_hist_mw_effective_50_trigger",
    ):
        assert token not in natural, f"historical threshold leaked into BetMax: {token}"
    assert "f$cc_river_donk_requested_reaches_hero_stack" in natural
    assert "f$cc_river_donk_requested_reaches_all_live_effective" in natural

    all_live = executable(block(ALLIN, "f$cc_river_donk_requested_reaches_all_live_effective"))
    assert "f$cc_river_donk_requested_reaches_mw_deepest" in all_live
    assert "f$cc_river_donk_requested_reaches_mw_shallowest" not in all_live

    sidepot = block(ALLIN, "f$cc_river_donk_sidepot_divergence_not_promoted")
    assert "f$cc_river_donk_mw_sidepot_divergence_candidate" in sidepot
    assert "f$cc_river_donk_natural_allin_equivalent Return false Force" in sidepot

    execution = block(ALLIN, "f$cc_river_donk_execution_betsize")
    for suffix in ("25", "30", "33", "50", "75", "100"):
        assert f"Set user_cc_river_donk_plan_size_{suffix}" in execution
    assert "When f$cc_river_donk_natural_allin_equivalent Return BetMax Force" in execution
    assert "When Others Return f$cc_river_donk_requested_betsize Force" in execution


def math_contract() -> None:
    # Historical >=50/60% stack ratio alone never creates natural all-in.
    c = Case(size_id=5, pot_bb=40, hero_bb=50, hu_eff_bb=50)
    assert requested(c) == 30
    assert requested(c) / c.hero_bb >= 0.60
    assert not natural_allin(c)

    # Source-specific 30% mapping is exact and remains normal deep.
    c = Case(size_id=2, pot_bb=50, hero_bb=100, hu_eff_bb=100)
    assert requested(c) == 15
    assert not natural_allin(c)

    # Requested pot lead exhausts Hero stack -> natural all-in.
    c = Case(size_id=6, pot_bb=24, hero_bb=24, hu_eff_bb=40)
    assert natural_allin(c)

    # Hero covers shorter HU Villain and selected 75% already covers effective.
    c = Case(size_id=5, pot_bb=40, hero_bb=100, hu_eff_bb=28)
    assert requested(c) == 30
    assert natural_allin(c)

    # Shortest-only MW sidepot reach must not promote.
    c = Case(size_id=4, pot_bb=30, hero_bb=100, mw_shallow_bb=12, mw_deep_bb=55)
    assert requested(c) == 15
    assert requested(c) >= c.mw_shallow_bb
    assert requested(c) < c.mw_deep_bb
    assert not natural_allin(c)

    # Pot lead reaches all current MW effective relations.
    c = Case(size_id=6, pot_bb=60, hero_bb=100, mw_shallow_bb=18, mw_deep_bb=55)
    assert natural_allin(c)


if __name__ == "__main__":
    fourbp_contract()
    runtime_mapping_contract()
    math_contract()
    print("PASS: Gate09F/H clean 4BP + River Donk runtime contract")
