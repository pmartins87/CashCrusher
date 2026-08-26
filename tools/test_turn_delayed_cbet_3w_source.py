#!/usr/bin/env python3
"""Gate12A native 3wBTNvSB / 3wBBvSB delayed-CBet source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3W_Snapshot.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3W_Source.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_Common.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_History.txt").read_text(encoding="utf-8")


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
    source_fd = block(SNAP, "f$cc_turn_delayed_cbet_source_fd")
    assert "HaveFlushDraw && SuitsInHand = 1" in source_fd
    assert "SuitsInHand = 2 && NumberOfUnknownSuitedOvercards <= 2" in source_fd
    source_sd = block(SNAP, "f$cc_turn_delayed_cbet_source_sd")
    assert "nstraightfillcommon - nstraightfill = 2" in source_sd
    assert "HaveNutStraightDraw" in source_sd
    broader = block(SNAP, "f$cc_turn_delayed_cbet_source_gutshot_or_better_draw")
    assert "Overcards = 2 && (HaveBackdoorFlushDraw || HaveBackdoorStraightDraw)" in broader
    assert "(hand$A || hand$K) && Overcards >= 1" in broader
    source_air = block(SNAP, "f$cc_turn_delayed_cbet_source_air")
    assert "f$cc_hand_no_made" in source_air
    assert "!f$cc_turn_delayed_cbet_source_gutshot_or_better_draw" in source_air

    btn = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnvsb_context")
    for token in ("f$cc_deal_size = 3", "f$cc_flop_entry_count = 2", "f$cc_hero_pos_id = 4", "f$cc_hu_villain_pos_id = 5"):
        assert token in btn
    mpbp = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnvsb_mpbp_candidate")
    assert "f$cc_hand_second_pair_or_pocket" in mpbp
    assert "f$cc_hand_third_pair_or_pocket" in mpbp
    assert "f$cc_flop_2bw" in block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnvsb_2bw_candidate")
    assert "f$cc_flop_1bw" in block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnvsb_1bw_candidate")
    pair9 = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnvsb_pair9plus_candidate")
    assert "SecondBestBoardCard >= 9" in pair9
    assert "ThirdBestBoardCard >= 9" in pair9
    assert "rankhiplayer >= 9" in pair9

    bb = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_bbvsb_context")
    for token in ("f$cc_deal_size = 3", "f$cc_flop_entry_count = 2", "f$cc_hero_pos_id = 6", "f$cc_hu_villain_pos_id = 5"):
        assert token in bb
    dry = block(SNAP, "f$cc_turn_delayed_cbet_source_3w_bbvsb_flop_dry")
    assert "FlushDrawPossible && OpenEndedStraightDrawPossibleOnFlop Return false Force" in dry
    assert "f$cc_turn_delayed_cbet_source_flop_drawheavy Return false Force" in dry
    assert "f$cc_turn_delayed_cbet_source_flop_spreaded Return true Force" in dry
    assert "!StraightPossibleOnFlop Return true Force" in dry
    wetair = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_bbvsb_wetair_candidate")
    assert "f$cc_turn_delayed_cbet_source_air" in wetair
    assert "f$cc_air_no_frontdoor" not in executable(wetair)
    assert "f$cc_turn_delayed_cbet_source_3w_bbvsb_flop_wet" in wetair
    special = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_bbvsb_air_2bworA_candidate")
    assert "f$cc_flop_2bw || AcePresentOnFlop" in special

    writer = block(SNAP, "f$cc_turn_delayed_cbet_3w_extra_snapshot_writer")
    for token in (
        "Set user_cc_turn_delayed_cbet_flop_snapshot_seen",
        "Set user_cc_turn_delayed_cbet_3w_btnvsb_flop_mpbp_candidate",
        "Set user_cc_turn_delayed_cbet_3w_bbvsb_flop_secondpair_candidate",
        "Set user_cc_turn_delayed_cbet_3w_bbvsb_flop_thirdpair_candidate",
        "Set user_cc_turn_delayed_cbet_3w_bbvsb_flop_wetair_candidate",
    ):
        assert token in writer


def dead_zombie_contract() -> None:
    dead = block(COMMON, "f$cc_turn_delayed_cbet_source_hand_dead")
    assert "f$cc_turn_delayed_cbet_source_fullhouse_or_better Return false Force" in dead
    assert "f$cc_turn_delayed_cbet_source_jhigh_onecard_fd Return false Force" in dead
    assert "nsuitedcommon >= 4 Return true Force" in dead
    zombie = block(COMMON, "f$cc_turn_delayed_cbet_source_hand_zombie")
    assert "MoreThanOneOneCardStraightPossible" in zombie
    assert "board$KQJT" in zombie
    assert "board$KJT9" in zombie
    assert "nstraightfillcommon = 1" in zombie
    assert "f$cc_turn_delayed_cbet_source_board_2bw" in zombie
    safe = block(COMMON, "f$cc_turn_delayed_cbet_source_draw_live_safe")
    assert "!f$cc_turn_delayed_cbet_source_hand_dead" in safe
    assert "!f$cc_turn_delayed_cbet_source_hand_zombie" in safe


def btnvsb_contract() -> None:
    ctx = block(POL, "f$cc_turn_delayed_cbet_3w_btnvsb_source_context")
    assert "f$cc_turn_delayed_cbet_snapshot_valid" in ctx
    assert "f$cc_hero_pos_id = 4" in ctx
    assert "f$cc_hu_villain_pos_id = 5" in ctx
    action = block(POL, "f$cc_turn_delayed_cbet_3w_btnvsb_source_action")
    assert "flop_mpbp_candidate && f$cc_turn_delayed_cbet_two_pair_plus_real Return true Force" in action
    assert "flop_mpbp_candidate && f$cc_turn_delayed_cbet_tpop_real Return true Force" in action
    assert "flop_2bw_candidate" in action
    assert "flop_1bw_candidate && user_cc_turn_delayed_cbet_3w_btnvsb_flop_pair9plus_candidate" in action
    code = executable(action).lower()
    assert "flop_tpplus" not in code
    assert "flop_nomade" not in code
    assert "air" not in code
    size = block(POL, "f$cc_turn_delayed_cbet_3w_btnvsb_source_size_id")
    assert "f$cc_turn_delayed_cbet_size_75_id" in size
    assert "f$cc_turn_delayed_cbet_size_50_id" in size
    assert "625" not in executable(size)
    plan = block(POL, "f$cc_turn_delayed_cbet_3w_btnvsb_plan_check_river")
    assert "flop_2bw_candidate" in plan
    assert "flop_1bw_candidate" in plan


def bbvsb_contract() -> None:
    ctx = block(POL, "f$cc_turn_delayed_cbet_3w_bbvsb_source_context")
    assert "f$cc_turn_delayed_cbet_snapshot_valid" in ctx
    assert "f$cc_hero_pos_id = 6" in ctx
    assert "f$cc_hu_villain_pos_id = 5" in ctx
    pair = block(POL, "f$cc_turn_delayed_cbet_3w_bbvsb_pair_action")
    assert "flop_secondpair_candidate || user_cc_turn_delayed_cbet_3w_bbvsb_flop_thirdpair_candidate" in pair
    assert "f$cc_turn_delayed_cbet_two_pair_plus_real Return true Force" in pair
    assert "f$cc_turn_delayed_cbet_tpop_real Return true Force" in pair
    assert "flop_secondpair_candidate && f$cc_hand_second_pair_or_pocket" in pair
    assert "f$cc_turn_delayed_cbet_third_pair Return true Force" in pair
    psize = block(POL, "f$cc_turn_delayed_cbet_3w_bbvsb_pair_size_id")
    assert "f$cc_turn_delayed_cbet_two_pair_plus_real Return f$cc_turn_delayed_cbet_size_75_id" in psize
    assert "When Others Return f$cc_turn_delayed_cbet_size_50_id" in psize

    live = block(POL, "f$cc_turn_delayed_cbet_3w_bbvsb_completed_live_draw")
    assert "f$cc_turn_delayed_cbet_turn_completed" in live
    assert "f$cc_turn_delayed_cbet_source_gutshot_or_better_fdsd" in live
    assert "f$cc_turn_delayed_cbet_source_draw_live_safe" in live
    air = block(POL, "f$cc_turn_delayed_cbet_3w_bbvsb_air_action")
    assert "f$cc_turn_delayed_cbet_3w_bbvsb_completed_live_draw Return true Force" in air
    assert "!f$cc_turn_delayed_cbet_turn_completed" in air
    assert "!user_cc_turn_delayed_cbet_3w_bbvsb_flop_air_2bworA_candidate" in air
    assert "f$cc_turn_delayed_cbet_no_made Return true Force" in air
    covered = block(POL, "f$cc_turn_delayed_cbet_3w_bbvsb_source_covered")
    assert "f$cc_turn_delayed_cbet_3w_bbvsb_source_context" in covered
    assert "translation_pending" not in executable(covered)
    assert executable(block(POL, "f$cc_turn_delayed_cbet_3w_extra_unresolved")).strip() == "false"


def history_and_router_contract() -> None:
    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base
    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_3w_btnvsb_source_covered Return 4 Force" in fam
    assert "f$cc_turn_delayed_cbet_3w_bbvsb_source_covered Return 5 Force" in fam
    action = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "f$cc_turn_delayed_cbet_3w_btnvsb_source_covered Return f$cc_turn_delayed_cbet_3w_btnvsb_source_action" in action
    assert "f$cc_turn_delayed_cbet_3w_bbvsb_source_covered Return f$cc_turn_delayed_cbet_3w_bbvsb_source_action" in action
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert "f$cc_turn_delayed_cbet_3w_btnvsb_source_size_id" in size
    assert "f$cc_turn_delayed_cbet_3w_bbvsb_source_size_id" in size
    cov = block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_core_source_covered" in cov
    assert "f$cc_turn_delayed_cbet_3w_extra_source_covered" in cov
    owners = block(ROUTER, "f$cc_turn_delayed_cbet_child_owner_count")
    assert "f$cc_turn_delayed_cbet_3w_btnvsb_source_covered" in owners
    assert "f$cc_turn_delayed_cbet_3w_bbvsb_source_covered" in owners


def safety_contract() -> None:
    code = executable(SNAP + "\n" + POL + "\n" + COMMON + "\n" + ROUTER).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "stackoff", "shorteststack", "effectivestack_bkp"):
        assert forbidden not in code, f"forbidden delayed-CBet leak: {forbidden}"
    assert "f$hand_dead" not in code
    assert "f$hand_zombie" not in code
    assert "translation_pending" not in executable(POL).lower()


if __name__ == "__main__":
    snapshot_contract()
    dead_zombie_contract()
    btnvsb_contract()
    bbvsb_contract()
    history_and_router_contract()
    safety_contract()
    print("PASS: Gate12A native 3wBTNvSB / 3wBBvSB delayed-CBet source")
