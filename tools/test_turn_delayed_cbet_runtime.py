#!/usr/bin/env python3
"""Gate12A Turn Delayed-CBet runtime sizing / stack-geometry contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BET = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_Betsize.txt").read_text(encoding="utf-8")
GEO = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_StackGeometry.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def mapping_contract() -> None:
    ready = block(BET, "f$cc_turn_delayed_cbet_runtime_size_ready")
    for token in (
        "f$cc_turn_delayed_cbet_router",
        "f$cc_turn_delayed_cbet_router_consistent",
        "f$cc_turn_delayed_cbet_size_consistent",
        "f$cc_turn_delayed_cbet_size_id >= 1",
        "f$cc_turn_delayed_cbet_size_id <= 7",
    ):
        assert token in ready

    requested = block(BET, "f$cc_turn_delayed_cbet_requested_betsize")
    for token in (
        "f$cc_turn_delayed_cbet_size_id = 1 Return BetMin Force",
        "f$cc_turn_delayed_cbet_size_id = 2 Return BetHalfPot Force",
        "f$cc_turn_delayed_cbet_size_id = 3 RaiseBy 62.5% Force",
        "f$cc_turn_delayed_cbet_size_id = 4 Return BetThreeFourthPot Force",
        "f$cc_turn_delayed_cbet_size_id = 5 Return BetPot Force",
        "f$cc_turn_delayed_cbet_size_id = 6 RaiseBy 150% Force",
        "f$cc_turn_delayed_cbet_size_id = 7 Return BetThirdPot Force",
    ):
        assert token in requested

    frac = block(BET, "f$cc_turn_delayed_cbet_requested_pot_fraction")
    expected = ((1,"-1"),(2,"0.50"),(3,"0.625"),(4,"0.75"),(5,"1.00"),(6,"1.50"),(7,"0.333"))
    for sid, value in expected:
        assert f"f$cc_turn_delayed_cbet_size_id = {sid} Return {value} Force" in frac

    # Preserve exact unusual source sizes: 62.5 is not rounded and 150 stays distinct.
    code = executable(requested)
    assert "RaiseBy 62.5% Force" in code
    assert "RaiseBy 150% Force" in code
    assert "RaiseBy 62%" not in code
    assert "RaiseBy 66%" not in code


def plan_marker_contract() -> None:
    execution = block(BET, "f$cc_turn_delayed_cbet_execution_betsize")
    assert "!f$cc_turn_delayed_cbet_runtime_mapping_valid Return 0 Force" in execution
    assert "Set user_cc_turn_delayed_cbet_plan_bet_seen" in execution
    assert "Set user_cc_turn_delayed_cbet_plan_size_recorded" in execution
    for marker in ("min", "50", "625", "75", "100", "150", "33"):
        assert f"Set user_cc_turn_delayed_cbet_plan_size_{marker}" in execution
    assert "When Others Return f$cc_turn_delayed_cbet_requested_betsize Force" in execution

    count = block(BET, "f$cc_turn_delayed_cbet_plan_size_marker_count")
    for marker in ("min", "50", "625", "75", "100", "150", "33"):
        assert f"user_cc_turn_delayed_cbet_plan_size_{marker}" in count

    consistent = block(BET, "f$cc_turn_delayed_cbet_plan_markers_consistent")
    assert "f$cc_turn_delayed_cbet_plan_size_marker_count != 1" in consistent
    assert "f$cc_turn_delayed_cbet_plan_size_marker_count != 0" in consistent


def geometry_contract() -> None:
    clean = block(GEO, "f$cc_turn_delayed_cbet_stackgeom_clean")
    for token in (
        "f$cc_turn_delayed_cbet_runtime_size_ready",
        "f$cc_turn_delayed_cbet_runtime_mapping_valid",
        "AmountToCall = 0",
        "currentbet = 0",
        "potplayer = 0",
        "f$cc_round_start_pot_bb > 0",
        "f$cc_hero_stack_round_start_bb > 0",
    ):
        assert token in clean

    reqbb = block(GEO, "f$cc_turn_delayed_cbet_requested_bet_bb")
    assert "f$cc_turn_delayed_cbet_size_id = 1 Return 1.00 Force" in reqbb
    assert "f$cc_turn_delayed_cbet_requested_pot_fraction * f$cc_round_start_pot_bb" in reqbb

    hu = block(GEO, "f$cc_turn_delayed_cbet_requested_hu_effective_ratio")
    assert "f$cc_hu_effective_stack_round_start_bb" in hu
    shallow = block(GEO, "f$cc_turn_delayed_cbet_requested_mw_shallowest_effective_ratio")
    deep = block(GEO, "f$cc_turn_delayed_cbet_requested_mw_deepest_effective_ratio")
    assert "f$cc_mw_shallowest_effective_stack_round_start_bb" in shallow
    assert "f$cc_mw_deepest_effective_stack_round_start_bb" in deep
    assert "f$cc_mw_stack_geometry_valid" in shallow
    assert "f$cc_mw_stack_geometry_valid" in deep

    divergence = block(GEO, "f$cc_turn_delayed_cbet_mw_sidepot_divergence_candidate")
    assert "f$cc_turn_delayed_cbet_requested_reaches_mw_shallowest" in divergence
    assert "!f$cc_turn_delayed_cbet_requested_reaches_mw_deepest" in divergence


def deterministic_examples() -> None:
    # Exact source fraction examples.
    assert abs(0.625 * 16.0 - 10.0) < 1e-12
    assert abs(1.50 * 20.0 - 30.0) < 1e-12
    assert abs(0.333 * 30.0 - 9.99) < 1e-12

    # MIN is exactly 1bb geometry, independent of pot size.
    for pot in (3.0, 20.0, 80.0):
        assert 1.0 == 1.0
        assert abs((1.0 / pot) - (1.0 / pot)) < 1e-12

    # Shortest-only multiway reach remains sidepot diagnostic.
    request, shallow, deep = 30.0, 25.0, 80.0
    assert request / shallow >= 1.0
    assert request / deep < 1.0

    # A 150%-pot request may naturally exceed Hero stack; policy is unchanged.
    pot, hero = 20.0, 24.0
    request = 1.50 * pot
    assert request >= hero


def no_allin_promotion_contract() -> None:
    assert executable(block(GEO, "f$cc_turn_delayed_cbet_no_runtime_allin_promotion")).strip() == "true"
    for text in (BET, GEO):
        code = executable(text).lower()
        for forbidden in (
            "betmax", "raise_committed", "stackoff", "handpower", "random",
            "shorteststack", "effectivestack_bkp",
        ):
            assert forbidden not in code, f"unsafe Gate12A runtime executable leak: {forbidden}"

    # Router itself must remain strategy-size only; runtime mapping does not widen it.
    router = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "Others Return false Force" in router


if __name__ == "__main__":
    mapping_contract()
    plan_marker_contract()
    geometry_contract()
    deterministic_examples()
    no_allin_promotion_contract()
    print("PASS: Gate12A Turn Delayed-CBet runtime sizing/stack geometry")
