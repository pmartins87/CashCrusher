#!/usr/bin/env python3
"""Gate12B runtime sizing / stack-geometry contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BET = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_Betsize.txt").read_text(encoding="utf-8")
GEO = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_StackGeometry.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def mapping_contract() -> None:
    ready = block(BET, "f$cc_turn_delayed_float_runtime_size_ready")
    for token in (
        "f$cc_turn_delayed_float_router",
        "f$cc_turn_delayed_float_router_consistent",
        "f$cc_turn_delayed_float_size_consistent",
        "f$cc_turn_delayed_float_size_33_id",
        "f$cc_turn_delayed_float_size_50_id",
        "f$cc_turn_delayed_float_size_75_id",
    ):
        assert token in ready

    frac = block(BET, "f$cc_turn_delayed_float_requested_pot_fraction")
    for size, fraction in (("33", "0.333"), ("50", "0.50"), ("75", "0.75")):
        assert f"f$cc_turn_delayed_float_size_id = f$cc_turn_delayed_float_size_{size}_id Return {fraction} Force" in frac

    req = block(BET, "f$cc_turn_delayed_float_requested_betsize")
    assert "f$cc_turn_delayed_float_size_33_id Return BetThirdPot Force" in req
    assert "f$cc_turn_delayed_float_size_50_id Return BetHalfPot Force" in req
    assert "f$cc_turn_delayed_float_size_75_id Return BetThreeFourthPot Force" in req
    assert "When Others Return 0 Force" in req

    mapping = block(BET, "f$cc_turn_delayed_float_runtime_mapping_valid")
    for fraction in ("0.333", "0.50", "0.75"):
        assert fraction in mapping


def plan_marker_contract() -> None:
    execution = block(BET, "f$cc_turn_delayed_float_execution_betsize")
    assert "!f$cc_turn_delayed_float_runtime_mapping_valid Return 0 Force" in execution
    assert "Set user_cc_turn_delayed_float_plan_bet_seen" in execution
    assert "Set user_cc_turn_delayed_float_plan_size_recorded" in execution
    for marker in ("33", "50", "75"):
        assert f"Set user_cc_turn_delayed_float_plan_size_{marker}" in execution
    assert "Set user_cc_turn_delayed_float_plan_reaches_hero_stack" in execution
    assert "Set user_cc_turn_delayed_float_plan_stack_reach_review" in execution
    assert "When Others Return f$cc_turn_delayed_float_requested_betsize Force" in execution

    count = block(BET, "f$cc_turn_delayed_float_plan_size_marker_count")
    assert count.count("* 1") == 3
    consistent = block(BET, "f$cc_turn_delayed_float_plan_markers_consistent")
    assert "f$cc_turn_delayed_float_plan_size_marker_count != 1" in consistent
    assert "f$cc_turn_delayed_float_plan_size_marker_count != 0" in consistent
    assert "user_cc_turn_delayed_float_plan_reaches_hero_stack" in consistent


def geometry_contract() -> None:
    clean = block(GEO, "f$cc_turn_delayed_float_stackgeom_clean")
    for token in (
        "f$cc_turn_delayed_float_runtime_size_ready",
        "f$cc_turn_delayed_float_runtime_mapping_valid",
        "AmountToCall = 0",
        "currentbet = 0",
        "potplayer = 0",
        "f$cc_round_start_pot_bb > 0",
        "f$cc_hero_stack_round_start_bb > 0",
    ):
        assert token in clean

    reqbb = block(GEO, "f$cc_turn_delayed_float_requested_bet_bb")
    assert "f$cc_turn_delayed_float_requested_pot_fraction * f$cc_round_start_pot_bb" in reqbb

    hu = block(GEO, "f$cc_turn_delayed_float_requested_hu_effective_ratio")
    shallow = block(GEO, "f$cc_turn_delayed_float_requested_mw_shallowest_effective_ratio")
    deep = block(GEO, "f$cc_turn_delayed_float_requested_mw_deepest_effective_ratio")
    assert "f$cc_hu_effective_stack_round_start_bb" in hu
    assert "f$cc_mw_shallowest_effective_stack_round_start_bb" in shallow
    assert "f$cc_mw_deepest_effective_stack_round_start_bb" in deep
    assert "f$cc_mw_stack_geometry_valid" in shallow and "f$cc_mw_stack_geometry_valid" in deep

    all_live = block(GEO, "f$cc_turn_delayed_float_requested_reaches_all_live_effective")
    assert "f$cc_turn_delayed_float_requested_reaches_hu_effective" in all_live
    assert "f$cc_turn_delayed_float_requested_reaches_mw_deepest" in all_live

    divergence = block(GEO, "f$cc_turn_delayed_float_mw_sidepot_divergence_candidate")
    assert "f$cc_turn_delayed_float_requested_reaches_mw_shallowest" in divergence
    assert "!f$cc_turn_delayed_float_requested_reaches_mw_deepest" in divergence


def deterministic_examples() -> None:
    assert abs(0.333 * 30.0 - 9.99) < 1e-12
    assert abs(0.50 * 18.0 - 9.0) < 1e-12
    assert abs(0.75 * 20.0 - 15.0) < 1e-12

    # Shortest-only multiway reach remains a sidepot diagnostic.
    request, shallow, deep = 15.0, 12.0, 40.0
    assert request / shallow >= 1.0
    assert request / deep < 1.0

    # A normal 75% request can touch Hero stack; policy still requests 75%, not jam.
    pot, hero = 20.0, 14.0
    request = 0.75 * pot
    assert request >= hero


def no_allin_promotion_contract() -> None:
    assert executable(block(BET, "f$cc_turn_delayed_float_no_runtime_allin_promotion")).strip() == "true"
    assert executable(block(GEO, "f$cc_turn_delayed_float_stackgeom_no_strategic_allin_promotion")).strip() == "true"
    code = executable(BET + "\n" + GEO).lower()
    for forbidden in (
        "betmax", "raise_committed", "stackoff", "handpower", "random",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe Gate12B runtime executable leak: {forbidden}"

    router = block(ROUTER, "f$cc_turn_delayed_float_router")
    assert "When Others Return false Force" in router


if __name__ == "__main__":
    mapping_contract()
    plan_marker_contract()
    geometry_contract()
    deterministic_examples()
    no_allin_promotion_contract()
    print("PASS: Gate12B runtime sizing / stack geometry")
