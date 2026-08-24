#!/usr/bin/env python3
"""Gate08B direct native `(BBorSB)v2pp` Turn Donk contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELP = (ROOT / "src" / "CashCrusher_Flop_Donk_SourceHistoryHelpers.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_Flop_Donk_ActionHistory.txt").read_text(encoding="utf-8")
SRC = (ROOT / "src" / "CashCrusher_Turn_Donk_Source.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_Donk.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def flop_substate_contract() -> None:
    draw = block(HELP, "f$cc_flop_donk_source_turn_xc_draw_candidate")
    assert "f$cc_flop_donk_source_native_context" in draw
    assert "f$cc_flop_donk_source_draw_check_parent" in draw

    air = block(HELP, "f$cc_flop_donk_source_turn_xc_highair_candidate")
    for token in (
        "!f$cc_hand_no_made Return false Force",
        "f$cc_real_frontdoor_draw Return false Force",
        "rankhiplayer = ace && f$cc_backdoor_sd Return true Force",
        "rankhiplayer != ace && f$cc_backdoor_fd && Overcards > 0 Return true Force",
    ):
        assert token in air
    assert "f$cc_hole_has_ace" not in executable(air)

    wrap = block(HIST, "f$cc_flop_donk_action_with_history")
    assert "Set user_cc_flop_donk_state_source_turn_xc_draw" in wrap
    assert "Set user_cc_flop_donk_state_source_turn_xc_highair" in wrap


def draw_xc_contract() -> None:
    ctx = block(SRC, "f$cc_turn_donk_source_native_draw_xc_context")
    for token in (
        "f$cc_turn_donk_opportunity",
        "f$cc_turn_donk_parent_id = 1",
        "f$cc_hist_flop_donk_family_id = 1",
        "f$cc_hist_flop_donk_source_turn_xc_draw_snapshot",
    ):
        assert token in ctx

    action = block(SRC, "f$cc_turn_donk_source_native_draw_xc_action")
    assert "f$cc_turn_donk_source_native_draw_xc_context" in action
    size = block(SRC, "f$cc_turn_donk_source_native_draw_xc_size_id")
    assert "f$cc_turn_donk_size_75_id" in size


def highair_contract() -> None:
    price = block(SRC, "f$cc_turn_donk_source_native_highair_call_price_proven")
    assert "user_cc_flop_donk_source_highair_called_le33" in price

    ctx = block(SRC, "f$cc_turn_donk_source_native_highair_xc_context")
    assert "f$cc_hist_flop_donk_source_turn_xc_highair_snapshot" in ctx
    assert "f$cc_turn_donk_source_native_highair_call_price_proven" in ctx

    pickup = block(SRC, "f$cc_turn_donk_source_native_highair_2hc_draw_pickup")
    assert "!f$cc_hand_no_made Return false Force" in pickup
    assert "HaveStraightDraw && (nstraightfillcommon - nstraightfill = 2) Return true Force" in pickup
    assert "HaveFlushDraw && SuitsInHand = 1 Return true Force" in pickup

    action = block(SRC, "f$cc_turn_donk_source_native_highair_xc_action")
    assert "f$cc_turn_donk_source_native_highair_2hc_draw_pickup" in action
    assert "f$cc_turn_donk_size_50_id" in block(SRC, "f$cc_turn_donk_source_native_highair_xc_size_id")

    gap = block(SRC, "f$cc_turn_donk_source_native_highair_needs_price_provenance")
    assert "!f$cc_turn_donk_source_native_highair_call_price_proven" in gap


def bc_contract() -> None:
    proof = block(SRC, "f$cc_turn_donk_source_native_bc_defense_proven")
    assert "user_cc_flop_donk_source_medium_draw_bc_eligible" in proof

    ctx = block(SRC, "f$cc_turn_donk_source_native_draw_bc_context")
    for token in (
        "f$cc_turn_donk_parent_id = 2",
        "f$cc_hist_flop_donk_family_id = 1",
        "user_cc_flop_donk_state_source_draw",
        "f$cc_turn_donk_source_native_bc_defense_proven",
    ):
        assert token in ctx

    assert "f$cc_turn_donk_size_75_id" in block(SRC, "f$cc_turn_donk_source_native_draw_bc_size_id")
    gap = block(SRC, "f$cc_turn_donk_source_native_bc_needs_defense_provenance")
    assert "!f$cc_turn_donk_source_native_bc_defense_proven" in gap


def router_and_safety_contract() -> None:
    covered = block(SRC, "f$cc_turn_donk_source_native_covered")
    assert "f$cc_turn_donk_source_native_draw_xc_context" in covered
    assert "f$cc_turn_donk_source_native_highair_xc_context" in covered
    assert "f$cc_turn_donk_source_native_draw_bc_context" in covered

    router = block(ROUTER, "f$cc_turn_donk_router")
    assert "f$cc_turn_donk_source_native_covered Return f$cc_turn_donk_source_native_action Force" in router
    assert "When Others Return false Force" in router

    uncovered = block(ROUTER, "f$cc_turn_donk_uncovered_context")
    assert "f$cc_turn_donk_opportunity && !f$cc_turn_donk_strategy_covered" in uncovered

    code = executable(SRC)
    for forbidden in (
        "HandPower",
        "random",
        "BetMax",
        "Raise_Committed",
        "StackOffDraws",
        "user_TurnShove",
        "f$cc_mw_spr_shallowest_round_start",
        "f$cc_mw_spr_deepest_round_start",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate08B executable leak: {forbidden}"

    # The mature C++ TP+/2P+ high-air reclassification is deliberately not copied.
    highair = block(SRC, "f$cc_turn_donk_source_native_highair_xc_action")
    for forbidden in ("two_pair", "top_pair", "overpair", "f$cc_hand_pair_or_better"):
        assert forbidden.lower() not in executable(highair).lower()


if __name__ == "__main__":
    flop_substate_contract()
    draw_xc_contract()
    highair_contract()
    bc_contract()
    router_and_safety_contract()
    print("PASS: Gate08B direct native Turn Donk source contract")
