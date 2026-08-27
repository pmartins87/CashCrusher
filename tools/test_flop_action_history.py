#!/usr/bin/env python3
"""Deterministic Gate01N tests for flop final-action provenance.

These tests cover the closed-street truth table plus source-contract assertions
for the pre-action CBet plan/hand/texture snapshot. They do not replace an
OpenHoldem replay/parser fixture.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY_FILE = ROOT / "src" / "CashCrusher_Flop_ActionHistory.txt"
EXEC_FILE = ROOT / "src" / "CashCrusher_Flop_CBet_AllinEquivalence.txt"


@dataclass(frozen=True)
class H:
    opportunity: bool = True
    planned_bet: bool = False
    size_recorded: bool = False
    expected_allin: bool = False
    checks: int = 0
    calls: int = 0
    raises: int = 0
    betsizes: int = 0
    allins: int = 0
    final_aggressor_hero: bool = False


def initial_cbet(h: H) -> bool:
    return h.opportunity and h.checks == 0 and (h.betsizes > 0 or h.allins > 0)


def direct_allin_cbet(h: H) -> bool:
    return initial_cbet(h) and h.allins > 0 and h.betsizes == 0 and h.raises == 0


def checkthrough(h: H) -> bool:
    return h.opportunity and h.checks > 0 and h.calls == 0 and h.raises == 0 and h.betsizes == 0 and h.allins == 0


def checked_then_called(h: H) -> bool:
    return h.opportunity and h.checks > 0 and h.calls > 0 and h.raises == 0 and h.betsizes == 0 and h.allins == 0


def checked_then_aggressed(h: H) -> bool:
    return h.opportunity and h.checks > 0 and (h.raises > 0 or h.betsizes > 0 or h.allins > 0)


def standard_turn_cbet_parent(h: H) -> bool:
    return h.opportunity and h.checks == 0 and h.calls == 0 and h.raises == 0 and h.betsizes == 1 and h.allins == 0 and h.final_aggressor_hero


def delayed_cbet_parent(h: H) -> bool:
    return checkthrough(h)


def cbet_then_called_raise(h: H) -> bool:
    return initial_cbet(h) and h.calls > 0 and not h.final_aggressor_hero


def cbet_then_reaggressed(h: H) -> bool:
    return initial_cbet(h) and (h.betsizes >= 2 or h.raises > 0 or (h.betsizes > 0 and h.allins > 0))


def unexpected_allin_promotion(h: H) -> bool:
    return h.size_recorded and not h.expected_allin and direct_allin_cbet(h)


def expected_allin_not_executed(h: H) -> bool:
    return h.expected_allin and initial_cbet(h) and h.betsizes > 0 and h.allins == 0


def run_truth_table() -> None:
    h = H(planned_bet=True, size_recorded=True, betsizes=1, final_aggressor_hero=True)
    assert initial_cbet(h) and standard_turn_cbet_parent(h) and not delayed_cbet_parent(h)

    h = H(checks=1)
    assert checkthrough(h) and delayed_cbet_parent(h) and not standard_turn_cbet_parent(h)

    h = H(checks=1, calls=1, final_aggressor_hero=False)
    assert checked_then_called(h) and not delayed_cbet_parent(h) and not standard_turn_cbet_parent(h)

    h = H(checks=1, betsizes=1, final_aggressor_hero=True)
    assert checked_then_aggressed(h) and not initial_cbet(h) and not delayed_cbet_parent(h)

    h = H(planned_bet=True, size_recorded=True, betsizes=1, calls=1, final_aggressor_hero=False)
    assert initial_cbet(h) and cbet_then_called_raise(h) and not standard_turn_cbet_parent(h)

    h = H(planned_bet=True, size_recorded=True, betsizes=2, final_aggressor_hero=True)
    assert initial_cbet(h) and cbet_then_reaggressed(h) and not standard_turn_cbet_parent(h)

    h = H(planned_bet=True, size_recorded=True, expected_allin=True, allins=1, final_aggressor_hero=True)
    assert direct_allin_cbet(h) and not unexpected_allin_promotion(h) and not standard_turn_cbet_parent(h)

    h = H(planned_bet=True, size_recorded=True, expected_allin=False, allins=1, final_aggressor_hero=True)
    assert direct_allin_cbet(h) and unexpected_allin_promotion(h)

    h = H(planned_bet=True, size_recorded=True, expected_allin=True, betsizes=1, final_aggressor_hero=True)
    assert initial_cbet(h) and expected_allin_not_executed(h)

    h = H(planned_bet=True, size_recorded=True, checks=1)
    assert delayed_cbet_parent(h) and not initial_cbet(h)

    h = H(opportunity=False, betsizes=1, final_aggressor_hero=True)
    assert not initial_cbet(h) and not standard_turn_cbet_parent(h) and not delayed_cbet_parent(h)


def run_source_contract() -> None:
    history = HISTORY_FILE.read_text(encoding="utf-8")
    execution = EXEC_FILE.read_text(encoding="utf-8")

    for symbol in ("didchecround2", "didcallround2", "didraisround2", "didbetsizeround2", "didalliround2", "lastraised2", "userchair"):
        assert symbol in history, f"missing OpenHoldem history symbol: {symbol}"

    for name in (
        "##f$cc_flop_cbet_action_with_history##",
        "##f$cc_hist_flop_cbet_primary_class_marker_count##",
        "##f$cc_hist_flop_cbet_snapshot_consistent##",
        "##f$cc_hist_flop_initial_cbet_executed##",
        "##f$cc_hist_flop_skipped_cbet_checkthrough##",
        "##f$cc_hist_turn_standard_cbet_parent##",
        "##f$cc_hist_turn_delayed_cbet_parent##",
        "##f$cc_hist_flop_unexpected_allin_promotion##",
    ):
        assert name in history, f"missing Gate01N function: {name}"

    assert "Set user_cc_flop_cbet_opportunity_seen" in history
    assert "Set user_cc_flop_cbet_executed" not in history

    # Current Turn source needs these FLOP facts after IsFlop becomes false.
    required_snapshot_markers = (
        "Set user_cc_flop_cbet_had_2pplus",
        "Set user_cc_flop_cbet_had_overpair",
        "Set user_cc_flop_cbet_had_top_pair",
        "Set user_cc_flop_cbet_had_below_top_pair",
        "Set user_cc_flop_cbet_had_no_made",
        "Set user_cc_flop_cbet_tp_kicker_below_t",
        "Set user_cc_flop_cbet_tp_kicker_jplus",
        "Set user_cc_flop_cbet_had_bdsd",
        "Set user_cc_flop_cbet_had_bdfd",
        "Set user_cc_flop_cbet_texture_static_high",
        "Set user_cc_flop_cbet_texture_dynamic_lowmid",
        "Set user_cc_flop_cbet_texture_paired",
    )
    for marker in required_snapshot_markers:
        assert marker in history, f"missing flop snapshot marker: {marker}"

    for marker in (
        "Set user_cc_flop_cbet_plan_bet_seen",
        "Set user_cc_flop_cbet_plan_size_recorded",
        "Set user_cc_flop_cbet_plan_size_33",
        "Set user_cc_flop_cbet_plan_size_50",
        "Set user_cc_flop_cbet_plan_size_75",
        "Set user_cc_flop_cbet_plan_size_100",
        "Set user_cc_flop_cbet_plan_expected_allin",
    ):
        assert marker in execution, f"missing CBet plan marker: {marker}"

    assert "When f$cc_cbet_natural_allin_equivalent Return BetMax Force" in execution
    assert "Return BetMax" not in history


if __name__ == "__main__":
    run_truth_table()
    run_source_contract()
    print("PASS: Gate01N flop action-history + strategic snapshot contract")
