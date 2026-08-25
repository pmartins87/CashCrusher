#!/usr/bin/env python3
"""Gate11L River-Probe runtime, stack geometry and all-in-equivalence contracts."""

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
BET = (SRC / "CashCrusher_River_Probe_Betsize.txt").read_text(encoding="utf-8")
GEO = (SRC / "CashCrusher_River_Probe_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_River_Probe_AllinEquivalence.txt").read_text(encoding="utf-8")
COMMON = (SRC / "CashCrusher_River_Probe_Common.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


FRACTIONS = {2: 0.25, 3: 0.333, 4: 0.50, 5: 0.75, 6: 1.00, 7: 0.30}


@dataclass(frozen=True)
class Case:
    size_id: int
    pot_bb: float
    hero_bb: float
    hu_eff_bb: float | None = None
    mw_shallow_bb: float | None = None
    mw_deep_bb: float | None = None


def requested(c: Case) -> float:
    if c.size_id == 1:
        return 1.0
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


def palette_contract() -> None:
    ids = {
        "f$cc_river_probe_size_min_id": "1",
        "f$cc_river_probe_size_25_id": "2",
        "f$cc_river_probe_size_33_id": "3",
        "f$cc_river_probe_size_50_id": "4",
        "f$cc_river_probe_size_75_id": "5",
        "f$cc_river_probe_size_100_id": "6",
        "f$cc_river_probe_size_30_id": "7",
    }
    for name, value in ids.items():
        assert block(COMMON, name).strip().startswith(value)


def mapping_contract() -> None:
    ready = block(BET, "f$cc_river_probe_runtime_size_ready")
    assert "f$cc_river_probe_router_consistent" in ready
    assert "f$cc_river_probe_size_consistent" in ready

    requested_action = block(BET, "f$cc_river_probe_requested_betsize")
    for token in (
        "f$cc_river_probe_size_id = 1 Return BetMin Force",
        "f$cc_river_probe_size_id = 2 RaiseBy 25% Force",
        "f$cc_river_probe_size_id = 3 Return BetThirdPot Force",
        "f$cc_river_probe_size_id = 4 Return BetHalfPot Force",
        "f$cc_river_probe_size_id = 5 Return BetThreeFourthPot Force",
        "f$cc_river_probe_size_id = 6 Return BetPot Force",
        "f$cc_river_probe_size_id = 7 RaiseBy 30% Force",
    ):
        assert token in requested_action
    assert "BetMax" not in requested_action

    frac = block(BET, "f$cc_river_probe_requested_pot_fraction")
    assert "f$cc_river_probe_size_id = 1 Return -1 Force" in frac
    for sid, value in ((2, "0.25"), (3, "0.333"), (4, "0.50"), (5, "0.75"), (6, "1.00"), (7, "0.30")):
        assert f"f$cc_river_probe_size_id = {sid} Return {value} Force" in frac

    # Source-specific River30 must remain exact and distinct from third-pot.
    assert "f$cc_river_probe_size_id = 7 RaiseBy 30% Force" in requested_action
    assert "f$cc_river_probe_size_id = 7 Return BetThirdPot" not in requested_action


def geometry_contract() -> None:
    clean = block(GEO, "f$cc_river_probe_stackgeom_clean")
    for token in (
        "f$cc_river_probe_runtime_size_ready",
        "f$cc_river_probe_runtime_mapping_valid",
        "AmountToCall = 0",
        "currentbet = 0",
        "potplayer = 0",
        "f$cc_round_start_pot_bb > 0",
        "f$cc_hero_stack_round_start_bb > 0",
    ):
        assert token in clean

    reqbb = block(GEO, "f$cc_river_probe_requested_bet_bb")
    assert "f$cc_river_probe_size_id = 1 Return 1.00 Force" in reqbb

    deep = block(GEO, "f$cc_river_probe_requested_mw_deepest_effective_ratio")
    shallow = block(GEO, "f$cc_river_probe_requested_mw_shallowest_effective_ratio")
    assert "f$cc_mw_deepest_effective_stack_round_start_bb" in deep
    assert "f$cc_mw_shallowest_effective_stack_round_start_bb" in shallow

    divergence = block(GEO, "f$cc_river_probe_mw_sidepot_divergence_candidate")
    assert "f$cc_river_probe_requested_reaches_mw_shallowest" in divergence
    assert "!f$cc_river_probe_requested_reaches_mw_deepest" in divergence


def allin_contract() -> None:
    natural = block(ALLIN, "f$cc_river_probe_natural_allin_equivalent")
    assert "f$cc_river_probe_requested_reaches_hero_stack Return true Force" in natural
    assert "f$cc_river_probe_requested_reaches_all_live_effective Return true Force" in natural
    for threshold in (
        "f$cc_river_probe_hist_hero_balance_50_trigger",
        "f$cc_river_probe_hist_hero_stack_60_trigger",
        "f$cc_river_probe_hist_hu_effective_50_trigger",
        "f$cc_river_probe_hist_mw_effective_50_trigger",
    ):
        assert threshold not in natural

    all_live = executable(block(ALLIN, "f$cc_river_probe_requested_reaches_all_live_effective"))
    assert "f$cc_river_probe_requested_reaches_hu_effective" in all_live
    assert "f$cc_river_probe_requested_reaches_mw_deepest" in all_live
    assert "shallowest" not in all_live.lower()

    execution = block(ALLIN, "f$cc_river_probe_execution_betsize")
    for suffix in ("min", "25", "33", "50", "75", "100", "30"):
        assert f"Set user_cc_river_probe_plan_size_{suffix}" in execution
    assert "f$cc_river_probe_natural_allin_equivalent Return BetMax Force" in execution
    assert "When Others Return f$cc_river_probe_requested_betsize Force" in execution

    sidepot = block(ALLIN, "f$cc_river_probe_sidepot_divergence_not_promoted")
    assert "f$cc_river_probe_mw_sidepot_divergence_candidate" in sidepot
    assert "f$cc_river_probe_natural_allin_equivalent Return false Force" in sidepot


def deterministic_examples() -> None:
    # MIN is exactly 1bb independently of River pot size.
    for pot in (3.0, 20.0, 80.0):
        c = Case(1, pot, 100.0, hu_eff_bb=100.0)
        assert requested(c) == 1.0
        assert not natural_allin(c)

    # Exact source River30 differs materially from 33%.
    c = Case(7, 30.0, 100.0, hu_eff_bb=100.0)
    assert requested(c) == 9.0
    third = 0.333 * 30.0
    assert abs(third - requested(c)) > 0.9

    # Historical >=60% Hero ratio alone is not mechanical all-in.
    c = Case(5, 40.0, 50.0, hu_eff_bb=50.0)
    assert requested(c) == 30.0
    assert requested(c) / c.hero_bb >= 0.60
    assert not natural_allin(c)

    # Requested pot bet exhausts Hero stack -> execution-equivalent all-in.
    c = Case(6, 24.0, 24.0, hu_eff_bb=40.0)
    assert natural_allin(c)

    # Hero covers shorter HU Villain; selected bet already covers effective stack.
    c = Case(5, 40.0, 100.0, hu_eff_bb=28.0)
    assert requested(c) == 30.0
    assert natural_allin(c)

    # Shortest-only multiway sidepot reach must not promote to BetMax.
    c = Case(4, 30.0, 100.0, mw_shallow_bb=12.0, mw_deep_bb=55.0)
    assert requested(c) == 15.0
    assert requested(c) >= c.mw_shallow_bb
    assert requested(c) < c.mw_deep_bb
    assert not natural_allin(c)

    # Whole-field deepest reach may be execution-equivalent all-in.
    c = Case(6, 60.0, 100.0, mw_shallow_bb=18.0, mw_deep_bb=55.0)
    assert natural_allin(c)


def safety_contract() -> None:
    assert "betmax" not in executable(BET).lower()
    assert "betmax" not in executable(GEO).lower()

    for text in (BET, GEO, ALLIN):
        code = executable(text).lower()
        for forbidden in ("raise_committed", "handpower", "random", "f$game_"):
            assert forbidden not in code, f"forbidden Gate11L executable leak: {forbidden}"


if __name__ == "__main__":
    palette_contract()
    mapping_contract()
    geometry_contract()
    allin_contract()
    deterministic_examples()
    safety_contract()
    print("PASS: Gate11L River-Probe runtime/geometry/all-in equivalence")
