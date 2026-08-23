#!/usr/bin/env python3
"""Deterministic Gate01N tests for flop final-action provenance.

These tests are intentionally split into two layers:

1. a truth-table model of the OpenHoldem history signals consumed by
   CashCrusher_Flop_ActionHistory.txt; and
2. source-contract assertions that protect the exact OpenPPL symbols and the
   history-aware CBet entrypoint from accidental removal.

This does NOT replace an OpenHoldem replay/parser fixture. It catches routing
logic regressions before that runtime gate exists.
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
    return (
        h.opportunity
        and h.checks > 0
        and h.calls == 0
        and h.raises == 0
        and h.betsizes == 0
        and h.allins == 0
    )


def checked_then_called(h: H) -> bool:
    return (
        h.opportunity
        and h.checks > 0
        and h.calls > 0
        and h.raises == 0
        and h.betsizes == 0
        and h.allins == 0
    )


def checked_then_aggressed(h: H) -> bool:
    return h.opportunity and h.checks > 0 and (h.raises > 0 or h.betsizes > 0 or h.allins > 0)


def standard_turn_cbet_parent(h: H) -> bool:
    return (
        h.opportunity
        and h.checks == 0
        and h.calls == 0
        and h.raises == 0
        and h.betsizes == 1
        and h.allins == 0
        and h.final_aggressor_hero
    )


def delayed_cbet_parent(h: H) -> bool:
    return checkthrough(h)


def cbet_then_called_raise(h: H) -> bool:
    return initial_cbet(h) and h.calls > 0 and not h.final_aggressor_hero


def cbet_then_reaggressed(h: H) -> bool:
    return initial_cbet(h) and (
        h.betsizes >= 2 or h.raises > 0 or (h.betsizes > 0 and h.allins > 0)
    )


def unexpected_allin_promotion(h: H) -> bool:
    return h.size_recorded and not h.expected_allin and direct_allin_cbet(h)


def expected_allin_not_executed(h: H) -> bool:
    return h.expected_allin and initial_cbet(h) and h.betsizes > 0 and h.allins == 0


def run_truth_table() -> None:
    # Standard CBet -> Villain call -> Turn CBet parent.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, final_aggressor_hero=True)
    assert initial_cbet(h)
    assert standard_turn_cbet_parent(h)
    assert not delayed_cbet_parent(h)

    # Hero had CBet opportunity, checked, everybody checked -> Delayed CBet.
    h = H(checks=1)
    assert checkthrough(h)
    assert delayed_cbet_parent(h)
    assert not standard_turn_cbet_parent(h)

    # Check-call is defense history, never delayed CBet.
    h = H(checks=1, calls=1, final_aggressor_hero=False)
    assert checked_then_called(h)
    assert not delayed_cbet_parent(h)
    assert not standard_turn_cbet_parent(h)

    # Check-raise is a raised-flop line, never an initial CBet.
    h = H(checks=1, betsizes=1, final_aggressor_hero=True)
    assert checked_then_aggressed(h)
    assert not initial_cbet(h)
    assert not delayed_cbet_parent(h)

    # CBet -> Villain raise -> Hero call. Villain owns turn initiative.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, calls=1, final_aggressor_hero=False)
    assert initial_cbet(h)
    assert cbet_then_called_raise(h)
    assert not standard_turn_cbet_parent(h)

    # CBet -> Villain raise -> Hero re-raises. Raised-flop continuation family.
    h = H(planned_bet=True, size_recorded=True, betsizes=2, final_aggressor_hero=True)
    assert initial_cbet(h)
    assert cbet_then_reaggressed(h)
    assert not standard_turn_cbet_parent(h)

    # Natural/mechanical BetMax was intended and executed.
    h = H(
        planned_bet=True,
        size_recorded=True,
        expected_allin=True,
        allins=1,
        final_aggressor_hero=True,
    )
    assert direct_allin_cbet(h)
    assert not unexpected_allin_promotion(h)
    assert not standard_turn_cbet_parent(h)  # Hero has no ordinary turn barrel.

    # Planned 50/75/etc was silently promoted by some global callback.
    h = H(
        planned_bet=True,
        size_recorded=True,
        expected_allin=False,
        allins=1,
        final_aggressor_hero=True,
    )
    assert direct_allin_cbet(h)
    assert unexpected_allin_promotion(h)

    # Gate01K expected BetMax but execution remained a normal betsize.
    h = H(
        planned_bet=True,
        size_recorded=True,
        expected_allin=True,
        betsizes=1,
        final_aggressor_hero=True,
    )
    assert initial_cbet(h)
    assert expected_allin_not_executed(h)

    # A stale strategy plan must not redefine what actually happened.
    h = H(planned_bet=True, size_recorded=True, checks=1)
    assert delayed_cbet_parent(h)
    assert not initial_cbet(h)

    # No CBet opportunity means no CBet/delayed-CBet parent even if Hero made a bet
    # from another node (float/donk/probe etc.).
    h = H(opportunity=False, betsizes=1, final_aggressor_hero=True)
    assert not initial_cbet(h)
    assert not standard_turn_cbet_parent(h)
    assert not delayed_cbet_parent(h)


def run_source_contract() -> None:
    history = HISTORY_FILE.read_text(encoding="utf-8")
    execution = EXEC_FILE.read_text(encoding="utf-8")

    required_history_symbols = (
        "didchecround2",
        "didcallround2",
        "didraisround2",
        "didbetsizeround2",
        "didalliround2",
        "lastraised2",
        "userchair",
    )
    for symbol in required_history_symbols:
        assert symbol in history, f"missing OpenHoldem history symbol: {symbol}"

    required_functions = (
        "##f$cc_flop_cbet_action_with_history##",
        "##f$cc_hist_flop_initial_cbet_executed##",
        "##f$cc_hist_flop_skipped_cbet_checkthrough##",
        "##f$cc_hist_turn_standard_cbet_parent##",
        "##f$cc_hist_turn_delayed_cbet_parent##",
        "##f$cc_hist_flop_unexpected_allin_promotion##",
    )
    for name in required_functions:
        assert name in history, f"missing Gate01N function: {name}"

    # The history-aware action wrapper must store opportunity but never claim that
    # an action executed before OpenHoldem's history confirms it.
    assert "Set user_cc_flop_cbet_opportunity_seen" in history
    assert "Set user_cc_flop_cbet_executed" not in history

    # The size execution owner records the plan and expected mechanical BetMax.
    required_plan_markers = (
        "Set user_cc_flop_cbet_plan_bet_seen",
        "Set user_cc_flop_cbet_plan_size_recorded",
        "Set user_cc_flop_cbet_plan_size_33",
        "Set user_cc_flop_cbet_plan_size_50",
        "Set user_cc_flop_cbet_plan_size_75",
        "Set user_cc_flop_cbet_plan_size_100",
        "Set user_cc_flop_cbet_plan_expected_allin",
    )
    for marker in required_plan_markers:
        assert marker in execution, f"missing CBet plan marker: {marker}"

    # Direct CBet execution remains the only place where local mechanical BetMax
    # is selected. No historical 50/55/60 threshold is smuggled into Gate01N.
    assert "When f$cc_cbet_natural_allin_equivalent Return BetMax Force" in execution
    assert "Return BetMax" not in history


if __name__ == "__main__":
    run_truth_table()
    run_source_contract()
    print("PASS: Gate01N flop action-history truth table and source contract")
