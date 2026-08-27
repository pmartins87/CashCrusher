#!/usr/bin/env python3
"""Gate13A exact Framework River no-action ownership/history contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = (ROOT / "src" / "CashCrusher_River_Delayed_History.txt").read_text(encoding="utf-8")


def block(name: str) -> str:
    marker = f"##{name}##"
    assert marker in H, f"missing {name}"
    tail = H.split(marker, 1)[1]
    return tail.split("##", 1)[0]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def clean_and_checkthrough_contract() -> None:
    clean = block("f$cc_river_delayed_first_action_clean")
    for token in ("IsRiver", "f$cc_context_valid", "BotsActionsOnThisRoundIncludingChecks = 0", "AmountToCall = 0"):
        assert token in clean

    turn = block("f$cc_river_delayed_turn_checkthrough")
    for token in ("didchecround3 > 0", "didcallround3 = 0", "didraisround3 = 0", "didbetsizeround3 = 0", "didalliround3 = 0"):
        assert token in turn


def framework_owner_contract() -> None:
    owner = block("f$cc_river_delayed_framework_position_owner")
    assert "f$cc_relpos_id = 3 Return true Force" in owner
    assert "(f$cc_relpos_id = 1 || f$cc_relpos_id = 2) && didcallround2 = 0 Return true Force" in owner
    assert "When Others Return false Force" in owner

    probe = block("f$cc_river_delayed_oop_flopcall_owned_by_probe")
    assert "(f$cc_relpos_id = 1 || f$cc_relpos_id = 2)" in probe
    assert "didcallround2 > 0" in probe

    base = block("f$cc_river_delayed_base_opportunity")
    for token in ("f$cc_river_delayed_first_action_clean", "f$Init_Nobody", "f$cc_river_delayed_turn_checkthrough", "f$cc_river_delayed_framework_position_owner", "f$cc_river_delayed_supported_pot_family"):
        assert token in base


def parent_bridge_contract() -> None:
    standard = block("f$cc_river_delayed_after_standard_turncheck_valid")
    assert "f$cc_hist_river_after_turn_checkthrough_parent" in standard
    assert "f$cc_hist_turn_state_snapshot_consistent" in standard
    assert "!f$cc_hist_turn_cbet_runtime_mismatch" in standard

    a = block("f$cc_river_delayed_after_gate12a_check_valid")
    assert "f$cc_hist_river_delayed_cbet_check_parent_valid" in a
    b = block("f$cc_river_delayed_after_gate12b_check_valid")
    assert "f$cc_hist_river_delayed_float_check_parent_valid" in b

    count = block("f$cc_river_delayed_known_parent_count")
    assert count.count("* 1") == 3
    assert "f$cc_river_delayed_known_parent_count > 1" in block("f$cc_river_delayed_parent_conflict")
    unresolved = block("f$cc_river_delayed_parent_unresolved")
    assert "f$cc_river_delayed_known_parent_count = 0" in unresolved


def fail_closed_contract() -> None:
    pots = block("f$cc_river_delayed_supported_pot_family")
    assert ">= 1" in pots and "<= 4" in pots
    code = executable(H).lower()
    for forbidden in ("handpower", "random", "betmax", "stackoff", "raise_committed"):
        assert forbidden not in code, forbidden


if __name__ == "__main__":
    clean_and_checkthrough_contract()
    framework_owner_contract()
    parent_bridge_contract()
    fail_closed_contract()
    print("PASS: Gate13A exact Framework no-action River ownership/history")
