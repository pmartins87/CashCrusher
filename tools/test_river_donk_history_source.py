#!/usr/bin/env python3
"""Gate09A/B River Donk ownership and true-HU HUBB source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HIST = (SRC / "CashCrusher_River_Donk_History.txt").read_text(encoding="utf-8")
HUBB = (SRC / "CashCrusher_River_Donk_HUBB.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_River_Donk.txt").read_text(encoding="utf-8")
TURN_HIST = (SRC / "CashCrusher_Turn_Donk_ActionHistory.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def history_contract() -> None:
    # Cross-node correction: normal executed Turn Donk is not River Donk.
    alias = block(HIST, "f$cc_hist_river_after_turn_donk_standard_parent_valid")
    assert "f$cc_hist_river_donk_standard_parent_valid" in alias
    firewall = block(HIST, "f$cc_river_donk_excluded_turn_donk_continuation")
    assert "f$cc_hist_river_after_turn_donk_standard_parent_valid" in firewall
    assert "f$cc_hist_river_donk_standard_parent_valid" in TURN_HIST

    flop = block(HIST, "f$cc_hist_river_donk_flop_checkcall_clean")
    for token in (
        "didchecround2 <= 0",
        "didcallround2 != 1",
        "didraisround2 != 0",
        "didbetsizeround2 != 0",
        "didalliround2 != 0",
        "f$cc_river_donk_flop_aggressor_crosscheck",
    ):
        assert token in flop

    turn = block(HIST, "f$cc_hist_river_donk_turn_checkcall_clean")
    for token in (
        "didchecround3 <= 0",
        "didcallround3 != 1",
        "didraisround3 != 0",
        "didbetsizeround3 != 0",
        "didalliround3 != 0",
        "f$cc_river_donk_turn_aggressor_crosscheck",
    ):
        assert token in turn

    # Independent OH history fields must agree.
    assert "BitCount(raisbits2) = 1" in block(HIST, "f$cc_river_donk_flop_unique_aggressor")
    assert "BitCount(raisbits3) = 1" in block(HIST, "f$cc_river_donk_turn_unique_aggressor")
    assert "raisbits2 BitAnd (1 << lastraised2)" in block(HIST, "f$cc_river_donk_flop_aggressor_crosscheck")
    assert "raisbits3 BitAnd (1 << lastraised3)" in block(HIST, "f$cc_river_donk_turn_aggressor_crosscheck")

    base = block(HIST, "f$cc_river_donk_base_opportunity")
    for token in (
        "IsRiver",
        "BotsActionsOnThisRoundIncludingChecks != 0",
        "AmountToCall != 0",
        "f$cc_river_donk_excluded_turn_donk_continuation",
        "f$cc_hist_river_donk_turn_checkcall_clean",
        "f$cc_relative_postflop_pos_id = 3",
    ):
        assert token in base

    source = block(HIST, "f$cc_river_donk_hubb_source_context")
    for token in (
        "f$cc_true_hu",
        "f$cc_hero_pos_id = 6",
        "f$cc_flop_entry_count = 2",
        "f$cc_hist_river_donk_flop_checkcall_clean",
        "f$cc_hist_river_donk_same_aggressor_flop_turn",
        "f$cc_river_donk_turn_aggressor_pos_id = 5",
        "f$cc_pot_family_id = 1 || f$cc_pot_family_id = 2",
    ):
        assert token in source


def source_strategy_contract() -> None:
    # Portable exact source categories.
    assert "HaveStraight && (nstraightfillcommon - nstraightfill = 2)" in block(HUBB, "f$cc_river_donk_2hc_straight")
    assert "HaveFlush && SuitsInHand = 1 && nsuitedcommon = 3" in block(HUBB, "f$cc_river_donk_2hc_flush")
    assert "HaveUnderStraight" in block(HUBB, "f$cc_river_donk_1hc_understraight")
    assert "!HaveUnderStraight" in block(HUBB, "f$cc_river_donk_1hc_straight_not_under")
    assert "FlushPossible || StraightPossible" in block(HUBB, "f$cc_river_donk_completed")

    # All historical Turn-call facts are deliberately unavailable until defense.
    for name in (
        "f$cc_river_donk_hubb_turn_tp_call_proven",
        "f$cc_river_donk_hubb_turn_2pplus_call_proven",
        "f$cc_river_donk_hubb_turn_good_draw_call_proven",
        "f$cc_river_donk_hubb_turn_lower_pair_draw_call_proven",
        "f$cc_river_donk_hubb_turn_below50_call_proven",
    ):
        assert block(HUBB, name).strip().startswith("0"), f"{name} must stay blocked before defense writer"

    action = block(HUBB, "f$cc_river_donk_hubb_action")
    size = block(HUBB, "f$cc_river_donk_hubb_size_id")
    # Source 2HC and high one-card flush/straight sizes.
    assert "f$cc_river_donk_2hc_straight || f$cc_river_donk_2hc_flush Return true Force" in action
    assert "f$cc_river_donk_2hc_straight || f$cc_river_donk_2hc_flush Return 6 Force" in size
    assert "f$cc_river_donk_1hc_flush_khigh_or_better Return 6 Force" in size
    assert "f$cc_river_donk_1hc_flush_9_to_q Return 4 Force" in size
    assert "f$cc_river_donk_1hc_flush_low Return 2 Force" in size
    assert "f$cc_river_donk_1hc_understraight Return 2 Force" in size
    assert "f$cc_river_donk_1hc_straight_not_under Return 4 Force" in size
    assert "f$cc_river_donk_source_set && f$cc_river_donk_completed Return 6 Force" in size
    assert "f$cc_river_donk_contributed_exact_two_pair && f$cc_river_donk_completed Return 5 Force" in size

    # No generic missed-draw/air bluff is active before provenance exists.
    code = executable(HUBB).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "stackoffdraws", "f$game_"):
        assert forbidden not in code, f"forbidden source leak: {forbidden}"
    assert "good_draw_call_proven Return true" not in code


def router_contract() -> None:
    family = block(ROUTER, "f$cc_river_donk_family_id")
    assert "f$cc_river_donk_hubb_covered Return 1 Force" in family
    route = block(ROUTER, "f$cc_river_donk_router")
    assert "f$cc_river_donk_hubb_covered Return f$cc_river_donk_hubb_action Force" in route
    assert "When Others Return false Force" in route
    sizes = block(ROUTER, "f$cc_river_donk_size_id")
    assert "f$cc_river_donk_hubb_covered Return f$cc_river_donk_hubb_size_id Force" in sizes
    assert "f$cc_river_donk_uncovered_context" in ROUTER


if __name__ == "__main__":
    history_contract()
    source_strategy_contract()
    router_contract()
    print("PASS: Gate09A/B River Donk history + true-HU HUBB source contract")
