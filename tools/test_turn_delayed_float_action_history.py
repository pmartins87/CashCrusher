#!/usr/bin/env python3
"""Gate12B.14 deterministic tests for closed Turn delayed-float execution history."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_ActionHistory.txt").read_text(encoding="utf-8")
BET = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_Betsize.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


@dataclass(frozen=True)
class H:
    opportunity: bool = True
    planned_bet: bool = False
    size_recorded: bool = False
    family_markers: int = 1
    snapshot_ok: bool = True
    source_plan_ok: bool = True
    checks: int = 0
    calls: int = 0
    raises: int = 0
    betsizes: int = 0
    allins: int = 0
    final_aggressor_hero: bool = False
    reaches_hero_stack: bool = False


def initial_bet(h: H) -> bool:
    return h.opportunity and h.checks == 0 and (h.betsizes > 0 or h.allins > 0)


def direct_allin(h: H) -> bool:
    return initial_bet(h) and h.allins > 0 and h.betsizes == 0 and h.raises == 0


def checked_back(h: H) -> bool:
    return h.opportunity and h.checks > 0 and h.calls == 0 and h.raises == 0 and h.betsizes == 0 and h.allins == 0


def standard_parent(h: H) -> bool:
    return (
        h.opportunity
        and h.checks == 0
        and h.calls == 0
        and h.raises == 0
        and h.betsizes == 1
        and h.allins == 0
        and h.final_aggressor_hero
    )


def mismatch(h: H) -> bool:
    plan_ok = (not h.planned_bet and not h.size_recorded) or (h.planned_bet and h.size_recorded)
    if not plan_ok or not h.snapshot_ok or not h.source_plan_ok:
        return True
    if h.planned_bet and checked_back(h):
        return True
    if initial_bet(h) and not h.planned_bet:
        return True
    if direct_allin(h) and not h.reaches_hero_stack:
        return True
    return False


def bet_parent_valid(h: H) -> bool:
    return standard_parent(h) and h.planned_bet and h.size_recorded and h.family_markers == 1 and not mismatch(h)


def check_parent_valid(h: H) -> bool:
    return checked_back(h) and not h.planned_bet and h.family_markers == 1 and not mismatch(h)


def run_truth_table() -> None:
    h = H(planned_bet=True, size_recorded=True, betsizes=1, final_aggressor_hero=True)
    assert standard_parent(h) and bet_parent_valid(h)

    h = H(planned_bet=False, checks=1)
    assert checked_back(h) and check_parent_valid(h)

    # Planned bet but actual check is runtime drift, not a BxB parent.
    h = H(planned_bet=True, size_recorded=True, checks=1)
    assert checked_back(h) and mismatch(h) and not check_parent_valid(h)

    # Runtime aggression without reviewed plan is rejected.
    h = H(planned_bet=False, betsizes=1, final_aggressor_hero=True)
    assert initial_bet(h) and mismatch(h) and not bet_parent_valid(h)

    # Normal request may be physically capped by Hero stack; this is explained
    # execution evidence only and never a River action parent.
    h = H(planned_bet=True, size_recorded=True, allins=1, reaches_hero_stack=True)
    assert direct_allin(h) and not mismatch(h) and not bet_parent_valid(h)

    # Direct all-in without pre-action Hero-stack reach is mismatch.
    h = H(planned_bet=True, size_recorded=True, allins=1, reaches_hero_stack=False)
    assert direct_allin(h) and mismatch(h)

    # Bet -> raise -> Hero call is not the standard continuation parent.
    h = H(planned_bet=True, size_recorded=True, betsizes=1, calls=1, final_aggressor_hero=False)
    assert initial_bet(h) and not standard_parent(h) and not bet_parent_valid(h)

    # Deliberate fail-closed uncovered family may check without being runtime drift,
    # but family=0 prevents Gate13 from treating it as reviewed parent.
    h = H(planned_bet=False, family_markers=0, checks=1)
    assert checked_back(h) and not mismatch(h) and not check_parent_valid(h)


def run_snapshot_contract() -> None:
    wrapper = block(HIST, "f$cc_turn_delayed_float_action_with_history")
    assert "Set user_cc_turn_delayed_float_opportunity_seen" in wrapper
    assert "Set user_cc_turn_delayed_float_state_snapshot_recorded" in wrapper
    for fid in range(1, 14):
        assert f"Set user_cc_turn_delayed_float_state_family_{fid}" in wrapper
    for cls in ("2pplus", "tpop", "second_pair", "third_pair", "no_made", "residual"):
        assert f"Set user_cc_turn_delayed_float_state_had_{cls}" in wrapper
    for n in range(2, 7):
        assert f"Set user_cc_turn_delayed_float_state_players_{n}" in wrapper
    for pos in ("utg", "hj", "co", "btn", "sb", "bb"):
        assert f"Set user_cc_turn_delayed_float_state_live_{pos}" in wrapper

    fam_count = block(HIST, "f$cc_hist_turn_delayed_float_family_marker_count")
    assert fam_count.count("* 1") == 13
    primary = block(HIST, "f$cc_hist_turn_delayed_float_primary_class_marker_count")
    assert primary.count("* 1") == 6

    snapshot = block(HIST, "f$cc_hist_turn_delayed_float_snapshot_consistent")
    assert "f$cc_hist_turn_delayed_float_primary_class_marker_count != 1" in snapshot
    assert "f$cc_hist_turn_delayed_float_player_count_marker_count != 1" in snapshot
    assert "BitCount(f$cc_hist_turn_delayed_float_live_opp_mask)" in snapshot
    assert "f$cc_hist_turn_delayed_float_family_marker_count > 1" in snapshot
    reviewed = block(HIST, "f$cc_hist_turn_delayed_float_reviewed_snapshot_consistent")
    assert "f$cc_hist_turn_delayed_float_family_marker_count = 1" in reviewed


def run_execution_contract() -> None:
    for symbol in (
        "didchecround3", "didcallround3", "didraisround3", "didbetsizeround3",
        "didalliround3", "lastraised3", "userchair",
    ):
        assert symbol in HIST

    initial = block(HIST, "f$cc_hist_turn_delayed_float_initial_bet_executed")
    assert "didchecround3 = 0" in initial
    assert "didbetsizeround3 > 0 || didalliround3 > 0" in initial

    standard = block(HIST, "f$cc_hist_turn_delayed_float_standard_parent")
    for token in (
        "didchecround3 = 0", "didcallround3 = 0", "didraisround3 = 0",
        "didbetsizeround3 = 1", "didalliround3 = 0", "lastraised3 = userchair",
    ):
        assert token in standard

    check = block(HIST, "f$cc_hist_turn_delayed_float_checked_back")
    assert "didchecround3 > 0" in check
    for token in ("didcallround3 = 0", "didraisround3 = 0", "didbetsizeround3 = 0", "didalliround3 = 0"):
        assert token in check

    cap = block(HIST, "f$cc_hist_turn_delayed_float_mechanical_hero_stack_cap")
    assert "user_cc_turn_delayed_float_plan_reaches_hero_stack" in cap
    unexpected = block(HIST, "f$cc_hist_turn_delayed_float_unexpected_allin_execution")
    assert "!user_cc_turn_delayed_float_plan_reaches_hero_stack" in unexpected


def run_source_plan_contract() -> None:
    wrapper = block(HIST, "f$cc_turn_delayed_float_action_with_history")
    markers = (
        "source_plan_bet_river50_secondpair",
        "source_plan_bet_checkriver_thirdpair",
        "source_plan_bet_air_checkriver",
        "source_plan_check_bxb_river50",
        "source_plan_check_skip_bxb",
    )
    for marker in markers:
        assert f"user_cc_turn_delayed_float_{marker}" in wrapper

    count = block(HIST, "f$cc_hist_turn_delayed_float_source_plan_marker_count")
    assert count.count("* 1") == 5
    consistent = block(HIST, "f$cc_hist_turn_delayed_float_source_plan_consistent")
    assert "f$cc_hist_turn_delayed_float_source_plan_marker_count > 1" in consistent
    assert "f$cc_hist_turn_delayed_float_family_id != 1" in consistent

    betparent = block(HIST, "f$cc_hist_river_delayed_float_bet_parent_valid")
    checkparent = block(HIST, "f$cc_hist_river_delayed_float_check_parent_valid")
    assert "f$cc_hist_turn_delayed_float_standard_parent" in betparent
    assert "f$cc_hist_turn_delayed_float_reviewed_snapshot_consistent" in betparent
    assert "f$cc_hist_turn_delayed_float_checked_back" in checkparent
    assert "!user_cc_turn_delayed_float_plan_bet_seen" in checkparent

    for name, marker in (
        ("f$cc_hist_river_delayed_float_source_secondpair_river50_valid", "source_plan_bet_river50_secondpair"),
        ("f$cc_hist_river_delayed_float_source_thirdpair_checkriver_valid", "source_plan_bet_checkriver_thirdpair"),
        ("f$cc_hist_river_delayed_float_source_air_checkriver_valid", "source_plan_bet_air_checkriver"),
        ("f$cc_hist_river_delayed_float_source_bxb_river50_valid", "source_plan_check_bxb_river50"),
        ("f$cc_hist_river_delayed_float_source_skip_bxb_valid", "source_plan_check_skip_bxb"),
    ):
        b = block(HIST, name)
        assert f"user_cc_turn_delayed_float_{marker}" in b


def run_plan_integration_contract() -> None:
    # Boolean wrapper records intended action; numeric betsize adapter must still
    # record one legal size. Missing numeric execution becomes history mismatch.
    wrapper = block(HIST, "f$cc_turn_delayed_float_action_with_history")
    assert "When f$cc_turn_delayed_float_router Set user_cc_turn_delayed_float_plan_bet_seen" in wrapper
    execution = block(BET, "f$cc_turn_delayed_float_execution_betsize")
    assert "Set user_cc_turn_delayed_float_plan_size_recorded" in execution

    mismatch = block(HIST, "f$cc_hist_turn_delayed_float_runtime_mismatch")
    assert "!f$cc_turn_delayed_float_plan_markers_consistent Return true Force" in mismatch
    assert "f$cc_hist_turn_delayed_float_planned_bet_but_checked Return true Force" in mismatch
    assert "f$cc_hist_turn_delayed_float_executed_without_plan Return true Force" in mismatch
    assert "f$cc_hist_turn_delayed_float_unexpected_allin_execution Return true Force" in mismatch

    # No strategic BetMax/all-in command is present in the execution adapter.
    exec_code = "\n".join(line.split("//", 1)[0] for line in BET.splitlines()).lower()
    assert "betmax" not in exec_code
    assert "return allin" not in exec_code


if __name__ == "__main__":
    run_truth_table()
    run_snapshot_contract()
    run_execution_contract()
    run_source_plan_contract()
    run_plan_integration_contract()
    print("PASS: Gate12B closed Turn delayed-float action history")
