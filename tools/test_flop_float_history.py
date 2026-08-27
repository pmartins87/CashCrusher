#!/usr/bin/env python3
"""Gate04H deterministic tests for closed-Flop Float provenance."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = (ROOT / "src" / "CashCrusher_Flop_Float_ActionHistory.txt").read_text(encoding="utf-8")
ALLIN = (ROOT / "src" / "CashCrusher_Flop_Float_AllinEquivalence.txt").read_text(encoding="utf-8")


@dataclass(frozen=True)
class H:
    opportunity: bool = True
    planned_bet: bool = False
    size_recorded: bool = False
    expected_allin: bool = False
    snapshot_ok: bool = True
    plan_ok: bool = True
    checks: int = 0
    calls: int = 0
    raises: int = 0
    betsizes: int = 0
    allins: int = 0
    final_aggressor_hero: bool = False


def initial_float(h: H) -> bool:
    return h.opportunity and h.checks == 0 and (h.betsizes > 0 or h.allins > 0)


def direct_allin(h: H) -> bool:
    return initial_float(h) and h.allins > 0 and h.betsizes == 0 and h.raises == 0


def checked_back(h: H) -> bool:
    return h.opportunity and h.checks > 0 and h.calls == 0 and h.raises == 0 and h.betsizes == 0 and h.allins == 0


def standard_parent(h: H) -> bool:
    return h.opportunity and h.checks == 0 and h.calls == 0 and h.raises == 0 and h.betsizes == 1 and h.allins == 0 and h.final_aggressor_hero


def unexpected_allin(h: H) -> bool:
    return h.size_recorded and not h.expected_allin and direct_allin(h)


def expected_allin_not_executed(h: H) -> bool:
    return h.expected_allin and initial_float(h) and h.betsizes > 0 and h.allins == 0


def mismatch(h: H) -> bool:
    if not h.snapshot_ok or not h.plan_ok:
        return True
    if h.planned_bet and h.checks > 0:
        return True
    if initial_float(h) and not h.planned_bet:
        return True
    if unexpected_allin(h) or expected_allin_not_executed(h):
        return True
    return False


def run_truth_table() -> None:
    # Reviewed Float executes as one normal size and remains final flop aggression.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, final_aggressor_hero=True)
    assert initial_float(h) and standard_parent(h) and not mismatch(h)

    # Strategy declines Float: exact-LAST Hero check is a true check-back parent.
    h = H(planned_bet=False, checks=1)
    assert checked_back(h) and not standard_parent(h) and not mismatch(h)

    # Planned bet but runtime checks is mismatch, not a valid delayed-history fact.
    h = H(planned_bet=True, size_recorded=True, checks=1)
    assert checked_back(h) and mismatch(h)

    # Float -> raise -> Hero call: not standard Float continuation parent.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, calls=1, final_aggressor_hero=False)
    assert initial_float(h) and not standard_parent(h)

    # Float then re-aggression: not one-size standard parent.
    h = H(planned_bet=True, size_recorded=True, betsizes=2, final_aggressor_hero=True)
    assert initial_float(h) and not standard_parent(h)

    # Expected mechanical all-in and direct all-in agree; no normal next-street parent.
    h = H(planned_bet=True, size_recorded=True, expected_allin=True, allins=1, final_aggressor_hero=True)
    assert direct_allin(h) and not unexpected_allin(h) and not standard_parent(h)

    # External/global promotion is diagnosed.
    h = H(planned_bet=True, size_recorded=True, expected_allin=False, allins=1, final_aggressor_hero=True)
    assert unexpected_allin(h) and mismatch(h)

    # Local plan expected BetMax but runtime records normal size.
    h = H(planned_bet=True, size_recorded=True, expected_allin=True, betsizes=1, final_aggressor_hero=True)
    assert standard_parent(h) and expected_allin_not_executed(h) and mismatch(h)

    # Runtime aggression without strategy plan capture is rejected.
    h = H(planned_bet=False, betsizes=1, final_aggressor_hero=True)
    assert initial_float(h) and mismatch(h)


def run_source_contract() -> None:
    for symbol in ("didchecround2", "didcallround2", "didraisround2", "didbetsizeround2", "didalliround2", "lastraised2", "userchair"):
        assert symbol in HISTORY, f"missing flop history symbol: {symbol}"

    for name in (
        "##f$cc_flop_float_action_with_history##",
        "##f$cc_hist_flop_float_initial_bet_executed##",
        "##f$cc_hist_flop_float_checked_back##",
        "##f$cc_hist_flop_float_then_called_raise##",
        "##f$cc_hist_flop_float_then_reaggressed##",
        "##f$cc_hist_flop_float_standard_parent##",
        "##f$cc_hist_flop_float_runtime_mismatch##",
        "##f$cc_hist_flop_float_standard_parent_valid##",
        "##f$cc_hist_flop_float_checkback_parent_valid##",
    ):
        assert name in HISTORY, f"missing Gate04H function: {name}"

    # Opportunity is captured independently from whether strategy plans to bet.
    assert "When f$cc_flop_float_opportunity Set user_cc_flop_float_opportunity_seen" in HISTORY
    assert "Set user_cc_flop_float_executed" not in HISTORY

    # Disappearing state required by future streets is snapshotted.
    for marker in (
        "Set user_cc_flop_float_state_had_2pplus",
        "Set user_cc_flop_float_state_had_top_pair",
        "Set user_cc_flop_float_state_had_no_made",
        "Set user_cc_flop_float_state_texture_static_high",
        "Set user_cc_flop_float_state_texture_dynamic_lowmid",
        "Set user_cc_flop_float_state_family_6",
        "Set user_cc_flop_float_state_players_6",
        "Set user_cc_flop_float_state_live_utg",
        "Set user_cc_flop_float_state_live_bb",
    ):
        assert marker in HISTORY, f"missing Float snapshot marker: {marker}"

    # Source HUSB no-forced-followup plan is persisted without being action proof.
    assert "Set user_cc_flop_float_plan_no_forced_2bar" in HISTORY
    assert "Set user_cc_flop_float_plan_no_bxb" in HISTORY

    # Size/all-in markers remain in execution adapter.
    for marker in ("Set user_cc_flop_float_plan_size_recorded", "Set user_cc_flop_float_plan_expected_allin"):
        assert marker in ALLIN


if __name__ == "__main__":
    run_truth_table()
    run_source_contract()
    print("PASS: Gate04H closed Flop Float action-history contract")
