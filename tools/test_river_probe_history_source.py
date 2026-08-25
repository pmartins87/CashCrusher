#!/usr/bin/env python3
"""Gate11A/B River Probe closed-history and native-source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = (ROOT / "src" / "CashCrusher_River_Probe_History.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_River_Probe_Common.txt").read_text(encoding="utf-8")
SNAP = (ROOT / "src" / "CashCrusher_Turn_Probe_Snapshot.txt").read_text(encoding="utf-8")
SRC = (ROOT / "src" / "CashCrusher_River_Probe_3W_Source.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_River_Probe.txt").read_text(encoding="utf-8")


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
    flop = block(HIST, "f$cc_hist_river_probe_flop_checkcall_clean")
    for token in (
        "didchecround2 <= 0",
        "didcallround2 != 1",
        "didraisround2 != 0",
        "didbetsizeround2 != 0",
        "didalliround2 != 0",
        "f$cc_river_probe_flop_aggressor_valid",
    ):
        assert token in flop

    agg = block(HIST, "f$cc_river_probe_flop_aggressor_valid")
    for token in (
        "f$cc_river_probe_flop_unique_aggressor",
        "lastraised2 < 0 || lastraised2 > 9",
        "lastraised2 = userchair",
        "raisbits2 BitAnd (1 << lastraised2)",
    ):
        assert token in agg

    turn = block(HIST, "f$cc_hist_river_probe_hero_checked_turn_clean")
    for token in (
        "didchecround3 != 1",
        "didcallround3 != 0",
        "didraisround3 != 0",
        "didbetsizeround3 != 0",
        "didalliround3 != 0",
    ):
        assert token in turn
    assert "raisbits3 = 0" in block(HIST, "f$cc_hist_river_probe_no_turn_aggressor")

    opp = block(HIST, "f$cc_river_probe_base_opportunity")
    for token in (
        "f$cc_context_valid",
        "f$cc_river_probe_first_river_action_clean",
        "f$cc_hist_river_probe_flop_checkcall_clean",
        "f$cc_hist_river_probe_turn_checkthrough_clean",
        "f$cc_river_probe_preflop_noinitiative",
        "f$cc_relative_postflop_pos_id != 1 && f$cc_relative_postflop_pos_id != 2",
    ):
        assert token in opp

    hu = block(HIST, "f$cc_river_probe_hu_opportunity")
    assert "f$cc_hu_oop" in hu
    assert "headsupchair = lastraised2" in hu


def snapshot_contract() -> None:
    ctx = block(SNAP, "f$cc_river_probe_snapshot_3w_sbvbtn_context")
    for token in (
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 5",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = 4",
    ):
        assert token in ctx

    draw = block(SNAP, "f$cc_river_probe_snapshot_3w_sbvbtn_nonbest_draw_candidate")
    assert "f$cc_hand_no_made" in draw
    assert "HaveStraightDraw || HaveInsideStraightDraw || HaveFlushDraw || f$cc_real_gutshot" in draw
    assert "HaveFlushDraw && (HaveStraightDraw || HaveInsideStraightDraw) Return false Force" in draw
    assert "Overcards = 2" in draw
    assert "SuitsInHand = 1" in draw

    high = block(SNAP, "f$cc_river_probe_snapshot_3w_sbvbtn_highair_candidate")
    assert "hand$A && HaveBackdoorStraightDraw" in high
    assert "!hand$A && HaveBackdoorFlushDraw && Overcards > 0" in high

    writer = block(SNAP, "f$cc_turn_probe_snapshot_writer")
    assert "Set user_cc_river_probe_flop_3w_sbvbtn_nonbest_draw_candidate" in writer
    assert "Set user_cc_river_probe_flop_3w_sbvbtn_highair_candidate" in writer


def source_contract() -> None:
    valid = block(SRC, "f$cc_river_probe_snapshot_valid")
    assert "f$cc_river_probe_base_opportunity" in valid
    assert "f$cc_hist_river_probe_flop_checkcall_clean" in valid
    assert "f$cc_hist_river_probe_turn_checkthrough_clean" in valid
    assert "user_cc_turn_probe_flop_snapshot_seen" in valid

    ctx = block(SRC, "f$cc_river_probe_3w_sbvbtn_context")
    for token in (
        "f$cc_river_probe_hu_opportunity",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 5",
        "f$cc_pf_single_raiser_pos_id = 4",
        "headsupchair = dealerchair",
        "lastraised2 = dealerchair",
    ):
        assert token in ctx

    parent = block(SRC, "f$cc_river_probe_3w_sbvbtn_source_parent")
    assert "f$cc_river_probe_3w_sbvbtn_draw_parent" in parent
    assert "f$cc_river_probe_3w_sbvbtn_highair_parent" in parent

    resolved = block(SRC, "f$cc_river_probe_3w_sbvbtn_resolved")
    for token in (
        "f$cc_river_probe_literal_nuts",
        "f$cc_river_probe_source_set",
        "f$cc_river_probe_contributed_exact_two_pair",
        "f$cc_river_probe_air",
    ):
        assert token in resolved

    size = block(SRC, "f$cc_river_probe_3w_sbvbtn_size_id")
    assert "f$cc_river_probe_size_100_id" in size
    assert "f$cc_river_probe_size_75_id" in size
    assert "f$cc_river_probe_size_50_id" in size

    pending = block(SRC, "f$cc_river_probe_3w_bbvbtn_provenance_pending")
    assert "f$cc_hero_pos_id = 6" in pending
    # BBvBTN context is labeled but must not leak into coverage yet.
    cov = executable(block(SRC, "f$cc_river_probe_3w_source_covered"))
    assert "f$cc_river_probe_3w_sbvbtn_covered" in cov
    assert "bbvbtn" not in cov.lower()


def common_router_safety_contract() -> None:
    assert "HaveTwoPair && !TwoPairOnBoard" in block(COMMON, "f$cc_river_probe_contributed_exact_two_pair")
    assert "HaveNuts" in block(COMMON, "f$cc_river_probe_literal_nuts")
    for sym in (
        "f$cc_river_probe_size_50_id",
        "f$cc_river_probe_size_75_id",
        "f$cc_river_probe_size_100_id",
    ):
        assert f"##{sym}##" in COMMON

    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_3w_source_covered Return 1 Force" in fam
    assert "When Others Return 0 Force" in fam
    action = block(ROUTER, "f$cc_river_probe_router")
    assert "When Others Return false Force" in action
    uncovered = block(ROUTER, "f$cc_river_probe_uncovered_context")
    assert "!f$cc_river_probe_strategy_covered" in uncovered

    code = executable(HIST + "\n" + COMMON + "\n" + SRC + "\n" + ROUTER).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "f$hand_stackoffdraws",
        "f$effectivestack_bkp",
    ):
        assert forbidden not in code, f"forbidden Gate11 leak: {forbidden}"


if __name__ == "__main__":
    history_contract()
    snapshot_contract()
    source_contract()
    common_router_safety_contract()
    print("PASS: Gate11A/B River Probe history and native-source subset")
