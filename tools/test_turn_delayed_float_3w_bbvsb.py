#!/usr/bin/env python3
"""Gate12B.3/4 deterministic tests for native 3wBBvSB delayed float."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_Snapshot.txt").read_text(encoding="utf-8")
SOURCE = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_3W_BBvSB_Source.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing function {name}"
    tail = text.split(marker, 1)[1]
    return tail.split("##", 1)[0]


@dataclass(frozen=True)
class S:
    source_context: bool = True
    saved_second: bool = False
    saved_third: bool = False
    saved_air: bool = False
    two_pair_plus: bool = False
    tpop: bool = False
    second: bool = False
    third: bool = False
    completed: bool = False
    live_draw: bool = False
    no_made: bool = False
    flop_2bw: bool = False
    flop_ahigh: bool = False


def pair_action(s: S) -> tuple[bool, int]:
    if not s.source_context or not (s.saved_second or s.saved_third):
        return False, 0
    if s.two_pair_plus:
        return True, 75
    if s.tpop:
        return True, 50
    if s.saved_second and s.second:
        return True, 50
    if (s.saved_second or s.saved_third) and s.third:
        return True, 50
    return False, 0


def air_action(s: S) -> tuple[bool, int]:
    if not s.source_context or not s.saved_air:
        return False, 0
    if s.two_pair_plus:
        return True, 75
    if s.tpop or s.second:
        return True, 50
    if s.completed and s.no_made and s.live_draw:
        return True, 50
    if (not s.completed) and (not s.flop_2bw) and (not s.flop_ahigh) and s.no_made:
        return True, 50
    return False, 0


def run_truth_table() -> None:
    # Literal pair source: 2nd/3rd pair delay 50; 4th-or-worse checks.
    assert pair_action(S(saved_second=True, second=True)) == (True, 50)
    assert pair_action(S(saved_second=True, third=True)) == (True, 50)
    assert pair_action(S(saved_third=True, third=True)) == (True, 50)
    assert pair_action(S(saved_third=True)) == (False, 0)

    # Current robust value supersedes stale flop class.
    assert pair_action(S(saved_second=True, two_pair_plus=True)) == (True, 75)
    assert pair_action(S(saved_third=True, tpop=True)) == (True, 50)

    # Wet-air source: completed turn needs live draw; blank turn can stab 50.
    assert air_action(S(saved_air=True, completed=True, no_made=True, live_draw=True)) == (True, 50)
    assert air_action(S(saved_air=True, completed=True, no_made=True, live_draw=False)) == (False, 0)
    assert air_action(S(saved_air=True, completed=False, no_made=True)) == (True, 50)

    # 2BW/A-high flops default to Turn check in no-made blank-turn branch.
    assert air_action(S(saved_air=True, completed=False, no_made=True, flop_2bw=True)) == (False, 0)
    assert air_action(S(saved_air=True, completed=False, no_made=True, flop_ahigh=True)) == (False, 0)


def run_source_contract() -> None:
    # Exact native topology and the three source-named origins are preserved.
    ctx = block(SNAPSHOT, "f$cc_turn_delayed_float_snapshot_3w_bbvsb_context")
    for token in (
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = 5",
    ):
        assert token in ctx

    origin = block(SNAPSHOT, "f$cc_turn_delayed_float_3w_bbvsb_flop_origin_id")
    assert "f$cc_pot_family_id = 1 Return 1" in origin
    assert "f$cc_pf_iso_proven Return 2" in origin
    assert "f$cc_pf_one_raise_ordinary_srp Return 3" in origin

    # Source checked-class split: high pair always; low pair only wet; wet air.
    second = block(SNAPSHOT, "f$cc_turn_delayed_float_3w_bbvsb_secondpair_candidate")
    third = block(SNAPSHOT, "f$cc_turn_delayed_float_3w_bbvsb_thirdpair_candidate")
    air = block(SNAPSHOT, "f$cc_turn_delayed_float_3w_bbvsb_wetair_candidate")
    assert "f$cc_flop_float_second_pair_high" in second
    assert "f$cc_flop_float_second_pair_low && f$cc_flop_float_wet_parent" in second
    assert "f$cc_flop_float_bottom_pair_high" in third
    assert "f$cc_flop_float_bottom_pair_low && f$cc_flop_float_wet_parent" in third
    assert "f$cc_flop_float_air" in air and "f$cc_flop_float_wet_parent" in air

    # Snapshot must never be treated as executed check proof by itself.
    valid = block(SNAPSHOT, "f$cc_turn_delayed_float_3w_bbvsb_snapshot_valid")
    assert "f$cc_turn_delayed_float_base_opportunity" in valid
    assert "saved_primary_marker_count != 1" in valid
    assert "unexpected_check_history" in SNAPSHOT

    pair = block(SOURCE, "f$cc_turn_delayed_float_3w_bbvsb_pair_action")
    assert "f$cc_turn_delayed_float_two_pair_plus_real Return true" in pair
    assert "f$cc_turn_delayed_float_tpop_real Return true" in pair
    assert "flop_secondpair_candidate && f$cc_turn_delayed_float_second_pair Return true" in pair
    assert "f$cc_turn_delayed_float_third_pair Return true" in pair
    assert "When Others Return false Force" in pair

    air_action_text = block(SOURCE, "f$cc_turn_delayed_float_3w_bbvsb_air_action")
    assert "f$cc_turn_delayed_float_3w_bbvsb_completed_live_draw Return true" in air_action_text
    assert "!user_cc_turn_delayed_float_3w_bbvsb_flop_wetair_2bw" in air_action_text
    assert "!user_cc_turn_delayed_float_3w_bbvsb_flop_wetair_ahigh" in air_action_text
    assert "When Others Return false Force" in air_action_text

    # Exact strategic sizes are only 50/75 in this source child.
    assert "f$cc_turn_delayed_float_size_50_id" in SOURCE
    assert "f$cc_turn_delayed_float_size_75_id" in SOURCE

    # Future-street source plans are metadata only and preserve AKx skip-BxB.
    assert "f$cc_turn_delayed_float_3w_bbvsb_plan_river50_secondpair" in SOURCE
    assert "f$cc_turn_delayed_float_3w_bbvsb_plan_checkriver_thirdpair" in SOURCE
    assert "f$cc_turn_delayed_float_3w_bbvsb_plan_turncheck_bxb_river50" in SOURCE
    assert "f$cc_turn_delayed_float_3w_bbvsb_plan_turncheck_skip_bxb" in SOURCE

    # Router currently owns exactly this one reviewed family and fails closed.
    family = block(ROUTER, "f$cc_turn_delayed_float_family_id")
    router = block(ROUTER, "f$cc_turn_delayed_float_router")
    assert "f$cc_turn_delayed_float_3w_bbvsb_source_covered Return 1" in family
    assert "f$cc_turn_delayed_float_3w_bbvsb_source_action" in router
    assert "When Others Return false Force" in router

    # No forbidden generic legacy coverage devices in executable source tree.
    executable = "\n".join(line for line in SOURCE.splitlines() if not line.lstrip().startswith("//"))
    for forbidden in ("HandPower", "Random", "random", "BetMax", "Commit", "commit", "Allin", "allin"):
        assert forbidden not in executable, f"forbidden generic token in 12B source executable: {forbidden}"


if __name__ == "__main__":
    run_truth_table()
    run_source_contract()
    print("PASS: Gate12B native 3wBBvSB source contract")
