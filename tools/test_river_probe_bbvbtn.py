#!/usr/bin/env python3
"""Gate11D native 3wBBvBTN River Probe provenance/strategy contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = (ROOT / "src" / "CashCrusher_Turn_Probe_Snapshot.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_River_Probe_History.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_River_Probe_Common.txt").read_text(encoding="utf-8")
PRIM = (ROOT / "src" / "CashCrusher_Postflop_Primitives.txt").read_text(encoding="utf-8")
SRC = (ROOT / "src" / "CashCrusher_River_Probe_3W_Source.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def snapshot_contract() -> None:
    ctx = block(SNAP, "f$cc_river_probe_snapshot_3w_bbvbtn_context")
    for token in (
        "f$cc_turn_probe_snapshot_capture_eligible",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 6",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = 4",
    ):
        assert token in ctx

    made = block(SNAP, "f$cc_river_probe_snapshot_3w_bbvbtn_made_candidate")
    for token in (
        "HaveNuts",
        "HaveSet",
        "HaveTrips && !TripsOnBoard && npcbits > 0",
        "HaveTwoPair && !TwoPairOnBoard",
        "HaveOverPair && PairInHand && npcbits > 0",
        "f$cc_hand_just_top_pair && !TwoPairOnBoard && npcbits > 0",
    ):
        assert token in made

    mpbp = block(SNAP, "f$cc_river_probe_snapshot_3w_bbvbtn_mpbp_candidate")
    for token in (
        "f$cc_hand_second_pair_or_pocket",
        "f$cc_hand_third_pair_or_pocket",
        "f$cc_hand_fourth_pair_or_pocket",
        "f$cc_hand_fifth_pair_or_pocket",
    ):
        assert token in mpbp

    draw = block(SNAP, "f$cc_river_probe_snapshot_3w_bbvbtn_nonbest_draw_candidate")
    assert "!f$cc_hand_no_made" in draw
    assert "Overcards = 2" in draw
    assert "SuitsInHand = 1" in draw

    air = block(SNAP, "f$cc_river_probe_snapshot_3w_bbvbtn_highair_candidate")
    assert "hand$A && HaveBackdoorStraightDraw" in air
    assert "!hand$A && HaveBackdoorFlushDraw && Overcards > 0" in air

    writer = block(SNAP, "f$cc_turn_probe_snapshot_writer")
    for flag in (
        "user_cc_river_probe_flop_3w_bbvbtn_made_candidate",
        "user_cc_river_probe_flop_3w_bbvbtn_mpbp_candidate",
        "user_cc_river_probe_flop_3w_bbvbtn_nonbest_draw_candidate",
        "user_cc_river_probe_flop_3w_bbvbtn_highair_candidate",
    ):
        assert f"Set {flag}" in writer


def history_and_context_contract() -> None:
    assert "didcallround2 != 1" in block(HIST, "f$cc_hist_river_probe_flop_checkcall_clean")
    assert "raisbits3 = 0" in block(HIST, "f$cc_hist_river_probe_no_turn_aggressor")

    ctx = block(SRC, "f$cc_river_probe_3w_bbvbtn_context")
    for token in (
        "f$cc_river_probe_hu_opportunity",
        "f$cc_river_probe_snapshot_valid",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 6",
        "f$cc_pf_single_raiser_pos_id = 4",
        "headsupchair = dealerchair",
        "lastraised2 = dealerchair",
    ):
        assert token in ctx

    parent = block(SRC, "f$cc_river_probe_3w_bbvbtn_source_parent")
    for child in (
        "f$cc_river_probe_3w_bbvbtn_made_parent",
        "f$cc_river_probe_3w_bbvbtn_mpbp_parent",
        "f$cc_river_probe_3w_bbvbtn_draw_parent",
        "f$cc_river_probe_3w_bbvbtn_highair_parent",
    ):
        assert child in parent


def board_and_kicker_contract() -> None:
    bw = block(COMMON, "f$cc_river_probe_board_broadway_count")
    for card in ("FirstFlopCard", "SecondFlopCard", "ThirdFlopCard", "TurnCard", "RiverCard"):
        assert f"{card} >= 10" in bw

    bad = block(COMMON, "f$cc_river_probe_bad_to_bluff_board")
    assert "PairOnBoard" in bad
    assert "board$A" in bad
    assert "f$cc_river_probe_board_broadway_count >= 2" in bad

    kicker = block(PRIM, "f$cc_number_better_kickers")
    assert "BitCount(rankbitspoker >> (f$cc_my_kicker + 1))" in kicker


def current_strategy_contract() -> None:
    strong = block(SRC, "f$cc_river_probe_3w_bbvbtn_strong100")
    assert "f$cc_river_probe_3w_strong_safe" in strong
    assert "f$cc_river_probe_contributed_exact_two_pair" in strong

    third = block(SRC, "f$cc_river_probe_3w_bbvbtn_thirdpair33")
    assert "f$cc_hand_third_pair_or_pocket" in third
    assert "f$cc_number_better_kickers <= 3" in third
    assert "!f$cc_river_probe_completed" in third
    assert "!f$cc_river_probe_paired" in third

    high = block(SRC, "f$cc_river_probe_3w_bbvbtn_highair_action")
    assert "!f$cc_river_probe_bad_to_bluff_board" in high
    high_bad = block(SRC, "f$cc_river_probe_3w_bbvbtn_highair_badboard_check")
    assert "f$cc_river_probe_bad_to_bluff_board" in high_bad

    pair_check = block(SRC, "f$cc_river_probe_3w_bbvbtn_pair_check")
    assert "f$cc_river_probe_3w_bbvbtn_weak_pair" in pair_check
    assert "!f$cc_river_probe_3w_bbvbtn_thirdpair33" in pair_check

    size = block(SRC, "f$cc_river_probe_3w_bbvbtn_size_id")
    for token in (
        "f$cc_river_probe_3w_bbvbtn_strong100 Return f$cc_river_probe_size_100_id",
        "f$cc_river_probe_3w_bbvbtn_tpop_action && f$cc_river_probe_completed Return f$cc_river_probe_size_75_id",
        "f$cc_river_probe_3w_bbvbtn_tpop_action && !f$cc_river_probe_completed Return f$cc_river_probe_size_100_id",
        "f$cc_river_probe_3w_bbvbtn_secondpair_action && f$cc_river_probe_completed Return f$cc_river_probe_size_50_id",
        "f$cc_river_probe_3w_bbvbtn_secondpair_action && !f$cc_river_probe_completed Return f$cc_river_probe_size_75_id",
        "f$cc_river_probe_3w_bbvbtn_thirdpair33 Return f$cc_river_probe_size_33_id",
        "f$cc_river_probe_3w_bbvbtn_draw_air_action Return f$cc_river_probe_size_50_id",
        "f$cc_river_probe_3w_bbvbtn_highair_action Return f$cc_river_probe_size_50_id",
    ):
        assert token in size

    covered = block(SRC, "f$cc_river_probe_3w_bbvbtn_covered")
    assert "f$cc_river_probe_3w_bbvbtn_highair_badboard_check" in covered
    assert "f$cc_river_probe_3w_bbvbtn_pair_check" in covered

    action = block(SRC, "f$cc_river_probe_3w_bbvbtn_action")
    assert "f$cc_river_probe_3w_bbvbtn_highair_badboard_check Return false Force" in action
    assert "f$cc_river_probe_3w_bbvbtn_pair_check Return false Force" in action


def translation_and_dispatch_contract() -> None:
    pending = block(SRC, "f$cc_river_probe_3w_bbvbtn_translation_pending")
    assert "f$cc_river_probe_3w_current_straightflush_pending" in pending

    # SBvBTN TP/OP is now mechanically translated too; only CF7-only S/F remains.
    sb_pending = block(SRC, "f$cc_river_probe_3w_sbvbtn_value_translation_pending")
    assert "f$cc_river_probe_3w_current_straightflush_pending" in sb_pending
    sb_size = block(SRC, "f$cc_river_probe_3w_sbvbtn_size_id")
    assert "f$cc_river_probe_3w_tp_or_op_real Return f$cc_river_probe_size_50_id" in sb_size

    cov = block(SRC, "f$cc_river_probe_3w_source_covered")
    assert "f$cc_river_probe_3w_sbvbtn_covered" in cov
    assert "f$cc_river_probe_3w_bbvbtn_covered" in cov
    dispatch = block(SRC, "f$cc_river_probe_3w_source_action")
    assert "f$cc_river_probe_3w_bbvbtn_covered Return f$cc_river_probe_3w_bbvbtn_action Force" in dispatch


def safety_contract() -> None:
    code = executable(SRC).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "f$game_",
        "f$cf7_",
        "effectivestack_bkp",
    ):
        assert forbidden not in code, f"forbidden Gate11D leak: {forbidden}"

    consistency = block(SRC, "f$cc_river_probe_3w_source_size_consistent")
    assert "f$cc_river_probe_3w_source_size_id = 0" in consistency
    assert "f$cc_river_probe_3w_source_size_id <= 7" in consistency


if __name__ == "__main__":
    snapshot_contract()
    history_and_context_contract()
    board_and_kicker_contract()
    current_strategy_contract()
    translation_and_dispatch_contract()
    safety_contract()
    print("PASS: Gate11D native 3wBBvBTN River Probe source contract")
