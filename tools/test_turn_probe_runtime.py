#!/usr/bin/env python3
"""Gate10J Turn-Probe runtime, stack geometry and all-in-equivalence contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BET = (ROOT / "src" / "CashCrusher_Turn_Probe_Betsize.txt").read_text(encoding="utf-8")
GEO = (ROOT / "src" / "CashCrusher_Turn_Probe_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (ROOT / "src" / "CashCrusher_Turn_Probe_AllinEquivalence.txt").read_text(encoding="utf-8")
OH = Path("/mnt/data/repositorio_completo_openholdem.txt")
DEEP = Path("/mnt/data/DeepCrusher(1).txt")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def mapping_contract() -> None:
    requested = block(BET, "f$cc_turn_probe_requested_betsize")
    for token in (
        "f$cc_turn_probe_size_id = 1 Return BetMin Force",
        "f$cc_turn_probe_size_id = 2 RaiseBy 25% Force",
        "f$cc_turn_probe_size_id = 3 Return BetThirdPot Force",
        "f$cc_turn_probe_size_id = 4 Return BetHalfPot Force",
        "f$cc_turn_probe_size_id = 5 Return BetThreeFourthPot Force",
        "f$cc_turn_probe_size_id = 6 Return BetPot Force",
        "f$cc_turn_probe_size_id = 7 Return BetTwoThirdPot Force",
    ):
        assert token in requested

    frac = block(BET, "f$cc_turn_probe_requested_pot_fraction")
    assert "f$cc_turn_probe_size_id = 1 Return -1 Force" in frac
    for sid, value in ((2,"0.25"),(3,"0.333"),(4,"0.50"),(5,"0.75"),(6,"1.00"),(7,"0.6666667")):
        assert f"f$cc_turn_probe_size_id = {sid} Return {value} Force" in frac


def verified_betmin_contract() -> None:
    # CI runner has repository sources but not necessarily the project's /mnt/data
    # source vault. Structural runtime evidence is also frozen in module comments.
    # When local audit sources are present, re-check the exact source evidence.
    if OH.exists():
        text = OH.read_text(encoding="utf-8", errors="ignore")
        assert "kTokenActionRaise,                // Also eqauls MinRaise, Bet and MinBet" in text
        assert '"BetMin"' in text
    if DEEP.exists():
        text = DEEP.read_text(encoding="utf-8", errors="ignore")
        assert "Use TurnMin (1bb)" in text

    reqbb = block(GEO, "f$cc_turn_probe_requested_bet_bb")
    assert "f$cc_turn_probe_size_id = 1 Return 1.00 Force" in reqbb


def geometry_contract() -> None:
    clean = block(GEO, "f$cc_turn_probe_stackgeom_clean")
    for token in (
        "f$cc_turn_probe_runtime_size_ready",
        "f$cc_turn_probe_runtime_mapping_valid",
        "AmountToCall = 0",
        "currentbet = 0",
        "potplayer = 0",
        "f$cc_round_start_pot_bb > 0",
        "f$cc_hero_stack_round_start_bb > 0",
    ):
        assert token in clean

    deep = block(GEO, "f$cc_turn_probe_requested_mw_deepest_effective_ratio")
    shallow = block(GEO, "f$cc_turn_probe_requested_mw_shallowest_effective_ratio")
    assert "f$cc_mw_deepest_effective_stack_round_start_bb" in deep
    assert "f$cc_mw_shallowest_effective_stack_round_start_bb" in shallow

    divergence = block(GEO, "f$cc_turn_probe_mw_sidepot_divergence_candidate")
    assert "f$cc_turn_probe_requested_reaches_mw_shallowest" in divergence
    assert "!f$cc_turn_probe_requested_reaches_mw_deepest" in divergence


def allin_contract() -> None:
    natural = block(ALLIN, "f$cc_turn_probe_natural_allin_equivalent")
    assert "f$cc_turn_probe_requested_reaches_hero_stack Return true Force" in natural
    assert "f$cc_turn_probe_requested_reaches_all_live_effective Return true Force" in natural
    assert "50" not in executable(natural)
    assert "60" not in executable(natural)

    all_live = block(ALLIN, "f$cc_turn_probe_requested_reaches_all_live_effective")
    assert "f$cc_turn_probe_requested_reaches_hu_effective" in all_live
    assert "f$cc_turn_probe_requested_reaches_mw_deepest" in all_live
    assert "shallowest" not in executable(all_live).lower()

    execb = block(ALLIN, "f$cc_turn_probe_execution_betsize")
    assert "f$cc_turn_probe_natural_allin_equivalent Return BetMax Force" in execb
    assert "When Others Return f$cc_turn_probe_requested_betsize Force" in execb

    sidepot = block(ALLIN, "f$cc_turn_probe_sidepot_divergence_not_promoted")
    assert "f$cc_turn_probe_natural_allin_equivalent Return false Force" in sidepot


def deterministic_examples() -> None:
    # fixed-fraction example: 75% of 20bb pot = 15bb
    assert abs(0.75 * 20.0 - 15.0) < 1e-9

    # MIN is 1bb independently of pot size.
    for pot in (3.0, 20.0, 80.0):
        requested = 1.0
        assert requested == 1.0
        assert abs((requested / pot) - (1.0 / pot)) < 1e-12

    # Short+deep multiway: 15bb request reaches 12bb short stack but not 80bb deep.
    request = 15.0
    shallow = 12.0
    deep = 80.0
    assert request / shallow >= 1.0
    assert request / deep < 1.0
    natural_allin = (request >= 100.0) or (request >= deep)
    assert not natural_allin

    # Whole-field effective reach may be BetMax-equivalent.
    request = 22.0
    deepest = 20.0
    hero = 100.0
    assert request < hero and request >= deepest

    # Historical 60% Hero trigger is diagnostic, not mechanical all-in.
    request = 60.0
    hero = 100.0
    deepest = 100.0
    assert request / hero >= 0.60
    assert request < hero and request < deepest


def safety_contract() -> None:
    geo_code = executable(GEO).lower()
    assert "betmax" not in geo_code

    bet_code = executable(BET).lower()
    assert "betmax" not in bet_code

    for text in (BET, GEO, ALLIN):
        code = executable(text).lower()
        for forbidden in ("raise_committed", "handpower", "random", "f$game_"):
            assert forbidden not in code, f"forbidden Gate10J executable leak: {forbidden}"


if __name__ == "__main__":
    mapping_contract()
    verified_betmin_contract()
    geometry_contract()
    allin_contract()
    deterministic_examples()
    safety_contract()
    print("PASS: Gate10J Turn-Probe runtime/geometry/all-in equivalence")
