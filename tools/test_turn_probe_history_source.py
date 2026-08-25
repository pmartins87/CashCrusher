#!/usr/bin/env python3
"""Gate10A/B.1 Turn Probe ownership, snapshot, and HUBB source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = (ROOT / "src" / "CashCrusher_Turn_Probe_History.txt").read_text(encoding="utf-8")
SNAP = (ROOT / "src" / "CashCrusher_Turn_Probe_Snapshot.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_Turn_Probe_Common.txt").read_text(encoding="utf-8")
HUBB = (ROOT / "src" / "CashCrusher_Turn_Probe_HUBB.txt").read_text(encoding="utf-8")
DONK = (ROOT / "src" / "CashCrusher_Flop_Donk.txt").read_text(encoding="utf-8")


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
    clean = block(HIST, "f$cc_hist_turn_probe_hero_checked_flop_clean")
    for token in ("didchecround2 = 1", "didcallround2 = 0", "didraisround2 = 0", "didbetsizeround2 = 0", "didswaground2 = 0"):
        assert token in clean

    field = block(HIST, "f$cc_hist_turn_probe_flop_field_unchanged")
    assert "nplayersplaying = f$cc_flop_entry_count" in field

    base = block(HIST, "f$cc_turn_probe_base_opportunity")
    for token in (
        "f$cc_context_valid",
        "f$cc_turn_probe_first_turn_action_clean",
        "f$cc_hist_turn_probe_flop_checkthrough_clean",
        "f$cc_turn_probe_preflop_noinitiative",
        "!f$cc_turn_probe_excluded_delayed_cbet",
        "!f$cc_turn_probe_excluded_delayed_float",
        "f$cc_relpos_id = 1 || f$cc_relpos_id = 2",
    ):
        assert token in base

    first = block(HIST, "f$cc_turn_probe_first_turn_action_clean")
    assert "BotsActionsOnThisRoundIncludingChecks = 0" in first
    assert "AmountToCall = 0" in first

    impossible = block(HIST, "f$cc_turn_probe_postflop_reduced_hu_impossible")
    assert "f$cc_hu_origin_postflop_reduced" in impossible


def snapshot_contract() -> None:
    eligible = block(SNAP, "f$cc_turn_probe_snapshot_capture_eligible")
    assert "f$cc_flop_donk_opportunity" in eligible
    assert "BotsActionsOnThisRoundIncludingChecks = 0" in eligible
    assert "AmountToCall = 0" in eligible
    assert "!f$cc_pf_role_pfa" in eligible
    assert "!f$cc_pf_role_3bettor" in eligible
    assert "!f$cc_pf_role_4bettor" in eligible

    writer = block(SNAP, "f$cc_turn_probe_snapshot_writer")
    for flag in (
        "user_cc_turn_probe_flop_snapshot_seen",
        "user_cc_turn_probe_flop_had_tpplus",
        "user_cc_turn_probe_flop_had_second_pair",
        "user_cc_turn_probe_flop_had_low_pair",
        "user_cc_turn_probe_flop_had_air",
        "user_cc_turn_probe_flop_had_1bw",
        "user_cc_turn_probe_flop_had_2plusbw",
    ):
        assert flag in writer

    valid = block(SNAP, "f$cc_turn_probe_snapshot_valid")
    assert "f$cc_hist_turn_probe_flop_checkthrough_clean" in valid
    assert "user_cc_turn_probe_flop_snapshot_seen" in valid

    # Snapshot writer is hooked into the Flop Donk decision path, but is not an action.
    assert "f$cc_turn_probe_snapshot_writer" in DONK


def common_contract() -> None:
    low = block(COMMON, "f$cc_turn_probe_low_pair")
    assert "f$cc_hand_third_pair_or_pocket" in low
    assert "f$cc_hand_fourth_pair_or_pocket" in low
    assert "f$cc_hand_fifth_pair_or_pocket" in low

    draw = block(COMMON, "f$cc_turn_probe_live_frontdoor_draw")
    assert "f$cc_hand_no_made" in draw
    assert "f$cc_real_frontdoor_draw" in draw

    ids = {
        "f$cc_turn_probe_size_min_id": "1",
        "f$cc_turn_probe_size_25_id": "2",
        "f$cc_turn_probe_size_33_id": "3",
        "f$cc_turn_probe_size_50_id": "4",
        "f$cc_turn_probe_size_75_id": "5",
        "f$cc_turn_probe_size_100_id": "6",
    }
    for name, value in ids.items():
        assert executable(block(COMMON, name)).strip() == value


def hubb_contract() -> None:
    ctx = block(HUBB, "f$cc_turn_probe_hubb_context")
    for token in (
        "f$cc_turn_probe_hu_opportunity",
        "f$cc_true_hu",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = 5",
        "f$cc_pot_family_id = 1 || f$cc_pot_family_id = 2",
    ):
        assert token in ctx

    action = block(HUBB, "f$cc_turn_probe_hubb_action")
    assert "f$cc_turn_probe_hubb_tpplus_completed Return true Force" in action
    assert "f$cc_turn_probe_hubb_tpplus_check Return false Force" in action
    assert "f$cc_turn_probe_second_pair Return true Force" in action
    assert "f$cc_turn_probe_low_pair Return true Force" in action
    assert "f$cc_turn_probe_live_frontdoor_draw Return true Force" in action
    assert "f$cc_turn_probe_hubb_air_check Return false Force" in action
    assert "f$cc_turn_probe_hubb_air_probe Return true Force" in action

    size = block(HUBB, "f$cc_turn_probe_hubb_size_id")
    assert "f$cc_turn_probe_size_min_id" in size
    assert size.count("f$cc_turn_probe_size_50_id") >= 4

    aircheck = block(HUBB, "f$cc_turn_probe_hubb_air_check")
    for token in (
        "f$cc_turn_probe_hubb_air_check_completed",
        "f$cc_turn_probe_hubb_air_check_low_unpaired",
        "f$cc_turn_probe_hubb_air_check_overcard",
    ):
        assert token in aircheck

    assert executable(block(HUBB, "f$cc_turn_probe_hubb_covered")).strip() == "f$cc_turn_probe_hubb_context"


def safety_contract() -> None:
    code = executable(HIST + "\n" + SNAP + "\n" + COMMON + "\n" + HUBB).lower()
    for forbidden in ("handpower", "random", "raise_committed", "betmax"):
        assert forbidden not in code, f"forbidden Turn Probe executable leak: {forbidden}"


if __name__ == "__main__":
    history_contract()
    snapshot_contract()
    common_contract()
    hubb_contract()
    safety_contract()
    print("PASS: Gate10A/B.1 Turn Probe history + snapshot + HUBB source contracts")
