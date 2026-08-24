#!/usr/bin/env python3
"""Gate05G deterministic Turn Float sizing and natural-all-in contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
BET = (SRC / "CashCrusher_Turn_Float_Betsize.txt").read_text(encoding="utf-8")
STACK = (SRC / "CashCrusher_Turn_Float_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_Turn_Float_AllinEquivalence.txt").read_text(encoding="utf-8")

FRACTIONS = {1: 0.25, 2: 0.333, 3: 0.50, 4: 0.75, 5: 1.00}


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    """Strip // comments so semantic assertions inspect executable OpenPPL only."""
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def natural_allin(*, pot: float, fraction: float, hero: float, hu_eff=None, mw_shallow=None, mw_deep=None):
    bet = pot * fraction
    reaches_hero = bet >= hero
    reaches_hu = hu_eff is not None and bet >= hu_eff
    reaches_mw_shallow = mw_shallow is not None and bet >= mw_shallow
    reaches_mw_deep = mw_deep is not None and bet >= mw_deep
    allin = reaches_hero or reaches_hu or reaches_mw_deep
    return bet, allin, reaches_mw_shallow and not reaches_mw_deep


def mapping_contract() -> None:
    frac = block(BET, "f$cc_turn_float_requested_pot_fraction")
    expected = {1: "0.25", 2: "0.333", 3: "0.50", 4: "0.75", 5: "1.00"}
    for idx, value in expected.items():
        assert f"f$cc_turn_float_size_id = {idx} Return {value} Force" in frac

    native = block(BET, "f$cc_turn_float_requested_betsize")
    assert "f$cc_turn_float_size_id = 1 RaiseBy 25% Force" in native
    assert "f$cc_turn_float_size_id = 2 Return BetThirdPot Force" in native
    assert "f$cc_turn_float_size_id = 3 Return BetHalfPot Force" in native
    assert "f$cc_turn_float_size_id = 4 Return BetThreeFourthPot Force" in native
    assert "f$cc_turn_float_size_id = 5 Return BetPot Force" in native


def deterministic_geometry_contract() -> None:
    # 75% pot consumes 50% of Hero stack: historical near-all-in review, but not
    # natural all-in because both Hero and HU effective remain above the bet.
    bet, ai, side = natural_allin(pot=20, fraction=0.75, hero=30, hu_eff=25)
    assert bet == 15
    assert not ai and not side

    # Requested size exceeds Hero's remaining stack -> natural BetMax.
    bet, ai, _ = natural_allin(pot=20, fraction=0.75, hero=12, hu_eff=25)
    assert bet == 15 and ai

    # Requested size covers exact HU effective stack -> natural BetMax.
    bet, ai, _ = natural_allin(pot=20, fraction=0.50, hero=30, hu_eff=9)
    assert bet == 10 and ai

    # Multiway: reaches only short player, deeper player remains; this is sidepot
    # divergence and MUST NOT promote whole action to BetMax.
    bet, ai, side = natural_allin(pot=20, fraction=0.75, hero=40, mw_shallow=10, mw_deep=30)
    assert bet == 15 and not ai and side

    # Multiway: same request reaches deepest all-live effective relation -> BetMax.
    bet, ai, side = natural_allin(pot=20, fraction=0.75, hero=40, mw_shallow=10, mw_deep=14)
    assert bet == 15 and ai and not side


def source_contract() -> None:
    clean = block(STACK, "f$cc_turn_float_stackgeom_clean")
    for token in ("AmountToCall = 0", "currentbet = 0", "potplayer = 0"):
        assert token in clean

    natural = block(ALLIN, "f$cc_turn_float_natural_allin_equivalent")
    assert "f$cc_turn_float_requested_reaches_hero_stack Return true Force" in natural
    assert "f$cc_turn_float_requested_reaches_all_live_effective Return true Force" in natural
    assert "historical_near_allin" not in natural
    assert "0.50" not in natural and "0.55" not in natural and "0.60" not in natural

    reachall = executable(block(ALLIN, "f$cc_turn_float_requested_reaches_all_live_effective"))
    assert "f$cc_turn_float_requested_reaches_hu_effective" in reachall
    assert "f$cc_turn_float_requested_reaches_mw_deepest" in reachall
    assert "shallowest" not in reachall

    sidepot = block(ALLIN, "f$cc_turn_float_sidepot_divergence_not_promoted")
    assert "f$cc_turn_float_natural_allin_equivalent Return false Force" in sidepot

    execute = block(ALLIN, "f$cc_turn_float_execution_betsize")
    assert "f$cc_turn_float_natural_allin_equivalent Return BetMax Force" in execute
    assert "user_cc_turn_float_plan_expected_allin" in execute
    assert "user_cc_turn_float_plan_giveup_river" in execute
    assert "user_cc_turn_float_plan_barrel_river" in execute

    plans = block(ALLIN, "f$cc_turn_float_plan_markers_consistent")
    assert "f$cc_turn_float_plan_size_marker_count != 1" in plans
    assert "f$cc_turn_float_river_plan_marker_count > 1" in plans


if __name__ == "__main__":
    mapping_contract()
    deterministic_geometry_contract()
    source_contract()
    print("PASS: Gate05G Turn Float runtime sizing + natural all-in equivalence contract")
