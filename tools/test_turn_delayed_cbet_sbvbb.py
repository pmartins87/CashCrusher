#!/usr/bin/env python3
"""Gate12A native 3wSBvBB Turn Delayed-CBet source contracts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_SBVBB_Snapshot.txt").read_text(encoding="utf-8")
VAL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_SBVBB_Value.txt").read_text(encoding="utf-8")
DA = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_SBVBB_DrawAir.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_SBVBB.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_History.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_Common.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def snapshot_contract() -> None:
    ctx = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_sbvbb_context")
    for token in ("f$cc_turn_delayed_cbet_snapshot_capture_eligible", "f$cc_deal_size = 3", "f$cc_flop_entry_count = 2", "f$cc_hero_pos_id = 5", "f$cc_hu_villain_pos_id = 6"):
        assert token in ctx

    tp = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_sbvbb_tpplus_candidate")
    for token in ("HaveNuts", "HaveTwoPair && !TwoPairOnBoard && npcbits > 0", "HaveOverPair && PairInHand && npcbits > 0", "f$cc_hand_just_top_pair && !TwoPairOnBoard && npcbits > 0"):
        assert token in tp
    low = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_sbvbb_lowpair_candidate")
    assert "f$cc_hand_third_pair_or_pocket" in low and "f$cc_hand_fourth_pair_or_pocket" in low
    assert "fifth" not in executable(low).lower()

    draw = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_sbvbb_draw_candidate")
    assert "f$cc_hand_no_made" in draw
    assert "f$cc_turn_delayed_cbet_source_gutshot_or_better_fdsd" in draw
    gm = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_sbvbb_draw_goodmedium_candidate")
    assert "f$cc_turn_delayed_cbet_source_draw_live_safe" in gm
    assert "HaveStraightDraw || HaveFlushDraw" in gm
    assert "Overcards > 0 || f$cc_turn_delayed_cbet_source_two_meaningful_overcards" in gm
    air = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_sbvbb_air_straight_candidate")
    assert "f$cc_turn_delayed_cbet_source_air" in air and "StraightPossibleOnFlop" in air
    wet = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_sbvbb_flop_wet_candidate")
    assert "!f$cc_turn_delayed_cbet_source_3w_bbvsb_flop_dry" in wet

    writer = block(SNAP, "f$cc_turn_delayed_cbet_3w_sbvbb_snapshot_writer")
    for token in ("Set user_cc_turn_delayed_cbet_flop_snapshot_seen", "Set user_cc_turn_delayed_cbet_3w_sbvbb_flop_tpplus_candidate", "Set user_cc_turn_delayed_cbet_3w_sbvbb_flop_draw_goodmedium_candidate", "Set user_cc_turn_delayed_cbet_3w_sbvbb_flop_wet_source"):
        assert token in writer


def value_contract() -> None:
    ctx = block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_source_context")
    assert "f$cc_turn_delayed_cbet_snapshot_valid" in ctx
    assert "f$cc_hero_pos_id = 5" in ctx and "f$cc_hu_villain_pos_id = 6" in ctx
    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base

    dry = block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_turn_board_dry")
    assert "FlushDrawPossible && OpenEndedStraightDrawPossibleOnFlop Return false Force" in dry
    assert "user_cc_turn_delayed_cbet_3w_sbvbb_flop_wet_source Return false Force" in dry
    assert "SuitsOnBoard <= 2 Return false Force" in dry
    assert "f$cc_turn_delayed_cbet_source_hand_zombie Return false Force" in dry
    assert "nstraightcommon >= 3 Return false Force" in dry

    action = block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_2p_action")
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_2p_checkxr_overcard Return false Force" in action
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_2p_checkxr_heavy Return false Force" in action
    assert "f$cc_turn_delayed_cbet_turn_completed Return true Force" in action
    assert "f$cc_turn_delayed_cbet_turn_under" in action
    size = block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_2p_size_id")
    assert "f$cc_turn_delayed_cbet_size_100_id" in size
    assert "f$cc_turn_delayed_cbet_size_50_id" in size
    assert "f$cc_turn_delayed_cbet_size_150_id" in size
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_limped_pot" in size

    second = block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_tp_to_second_action")
    assert "f$cc_turn_delayed_cbet_second_pair" in second
    assert "TurnCardIsOvercardToBoard > 0" in second
    tpop_size = block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_tpop_size_id")
    for token in ("f$cc_turn_delayed_cbet_size_75_id", "f$cc_turn_delayed_cbet_size_100_id", "TurnCard = 14", "f$cc_turn_delayed_cbet_size_50_id"):
        assert token in tpop_size
    lower = block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_secondpair_action")
    assert "f$cc_turn_delayed_cbet_turn_under" in lower
    assert "f$cc_turn_delayed_cbet_size_75_id" in block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_secondpair_size_id")
    assert "user_cc_turn_delayed_cbet_3w_sbvbb_flop_lowpair_candidate" in block(VAL, "f$cc_turn_delayed_cbet_3w_sbvbb_lowpair_check")


def draw_air_contract() -> None:
    draw = block(DA, "f$cc_turn_delayed_cbet_3w_sbvbb_draw_action")
    assert "!f$cc_turn_delayed_cbet_source_draw_live_safe Return false Force" in draw
    assert "StraightPossibleOnFlop && user_cc_turn_delayed_cbet_3w_sbvbb_flop_draw_goodmedium_candidate Return true Force" in draw
    assert "StraightPossibleOnFlop Return false Force" in draw
    assert "f$cc_turn_delayed_cbet_source_gutshot_or_better_fdsd Return true Force" in draw
    dsize = block(DA, "f$cc_turn_delayed_cbet_3w_sbvbb_draw_size_id")
    assert "f$cc_turn_delayed_cbet_size_75_id" in dsize and "f$cc_turn_delayed_cbet_size_50_id" in dsize

    air = block(DA, "f$cc_turn_delayed_cbet_3w_sbvbb_air_action")
    assert "f$cc_turn_delayed_cbet_source_gutshot_or_better_fdsd && f$cc_turn_delayed_cbet_source_draw_live_safe Return true Force" in air
    assert "f$cc_turn_delayed_cbet_source_air && (hand$A || hand$K) Return false Force" in air
    assert "f$cc_turn_delayed_cbet_turn_completed || !f$cc_turn_delayed_cbet_3w_sbvbb_turn_board_dry" in air
    asize = block(DA, "f$cc_turn_delayed_cbet_3w_sbvbb_air_size_id")
    assert "f$cc_turn_delayed_cbet_size_50_id" in asize
    assert "f$cc_turn_delayed_cbet_size_75_id" in asize

    for plan in ("f$cc_turn_delayed_cbet_3w_sbvbb_plan_draw_connected_river50", "f$cc_turn_delayed_cbet_3w_sbvbb_plan_draw_connected_deldel", "f$cc_turn_delayed_cbet_3w_sbvbb_plan_draw75_giveup", "f$cc_turn_delayed_cbet_3w_sbvbb_plan_air_draw_checkriver", "f$cc_turn_delayed_cbet_3w_sbvbb_plan_air_ak_showdown", "f$cc_turn_delayed_cbet_3w_sbvbb_plan_air_wet_river50", "f$cc_turn_delayed_cbet_3w_sbvbb_plan_air_dry_giveup"):
        block(DA, plan)


def dispatcher_contract() -> None:
    action = block(POL, "f$cc_turn_delayed_cbet_3w_sbvbb_source_action")
    order = ["flop_tpplus_candidate", "flop_secondpair_candidate", "flop_lowpair_candidate", "flop_draw_candidate", "flop_air_straight_candidate"]
    positions = [action.index(x) for x in order]
    assert positions == sorted(positions)
    assert "flop_lowpair_candidate Return false Force" in action
    covered = block(POL, "f$cc_turn_delayed_cbet_3w_sbvbb_source_covered")
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_source_context" in covered
    assert executable(block(POL, "f$cc_turn_delayed_cbet_3w_sbvbb_unresolved")).strip() == "false"
    consistency = block(POL, "f$cc_turn_delayed_cbet_3w_sbvbb_size_consistent")
    assert "<= 6" in consistency

    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_source_covered Return 6 Force" in fam
    route = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_source_covered Return f$cc_turn_delayed_cbet_3w_sbvbb_source_action" in route
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_source_size_id" in size
    cov = block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_source_covered" in cov
    assert "<= 6" in block(ROUTER, "f$cc_turn_delayed_cbet_size_consistent")
    assert "f$cc_turn_delayed_cbet_3w_sbvbb_size_consistent" in block(ROUTER, "f$cc_turn_delayed_cbet_router_consistent")

    common150 = block(COMMON, "f$cc_turn_delayed_cbet_size_150_id")
    assert executable(common150).strip() == "6"


def safety_contract() -> None:
    code = executable(SNAP + "\n" + VAL + "\n" + DA + "\n" + POL + "\n" + ROUTER).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "stackoff", "shorteststack", "effectivestack_bkp"):
        assert forbidden not in code, f"forbidden 3wSBvBB delayed-CBet leak: {forbidden}"
    # Source defensive plans stay markers, never action promotion.
    assert "return betmax" not in code
    assert "return raise" not in code


if __name__ == "__main__":
    snapshot_contract()
    value_contract()
    draw_air_contract()
    dispatcher_contract()
    safety_contract()
    print("PASS: Gate12A native 3wSBvBB delayed-CBet source")
