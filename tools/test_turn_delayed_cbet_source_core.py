#!/usr/bin/env python3
"""Gate12A core Turn Delayed-CBet ownership/source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
LIMP = (SRC / "CashCrusher_Limped_Initiative_Context.txt").read_text(encoding="utf-8")
HIST = (SRC / "CashCrusher_Turn_DelayedCBet_History.txt").read_text(encoding="utf-8")
PROBE_HIST = (SRC / "CashCrusher_Turn_Probe_History.txt").read_text(encoding="utf-8")
COMMON = (SRC / "CashCrusher_Turn_DelayedCBet_Common.txt").read_text(encoding="utf-8")
SNAP = (SRC / "CashCrusher_Turn_DelayedCBet_Snapshot.txt").read_text(encoding="utf-8")
SOURCE = (SRC / "CashCrusher_Turn_DelayedCBet_Source_Core.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def limped_initiative_contract() -> None:
    husb = block(LIMP, "f$cc_native_limped_init_husb")
    for token in ("f$cc_true_hu", "f$cc_pf_raise_count = 0", "f$cc_pf_role_unraised_caller", "f$cc_hero_pos_id = 5", "f$cc_hu_villain_pos_id = 6"):
        assert token in husb

    btn = block(LIMP, "f$cc_native_limped_init_3w_btn")
    assert "f$cc_deal_size = 3" in btn
    assert "f$cc_hero_pos_id = 4" in btn
    assert "f$cc_pf_role_unraised_caller" in btn

    sbvbb = block(LIMP, "f$cc_native_limped_init_3w_sbvbb")
    assert "f$cc_hero_pos_id = 5" in sbvbb
    assert "f$cc_hu_villain_pos_id = 6" in sbvbb
    assert "f$cc_flop_entry_count = 2" in sbvbb

    union = block(LIMP, "f$cc_native_limped_initiative")
    assert "hubb" not in executable(union).lower()
    assert "f$cc_native_limped_init_husb" in union
    assert "f$cc_native_limped_init_3w_btn" in union
    assert "f$cc_native_limped_init_3w_sbvbb" in union

    # Gate10 Probe must no longer steal the source limped-initiative set.
    noinit = block(PROBE_HIST, "f$cc_turn_probe_preflop_noinitiative")
    assert "f$cc_native_limped_initiative Return false Force" in noinit
    excluded = block(PROBE_HIST, "f$cc_turn_probe_excluded_delayed_cbet")
    assert "f$cc_native_limped_initiative" in excluded


def ownership_contract() -> None:
    parent = block(HIST, "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean")
    assert "f$cc_hist_turn_probe_flop_checkthrough_clean" in parent

    init = block(HIST, "f$cc_turn_delayed_cbet_preflop_initiative")
    assert "f$cc_turn_delayed_cbet_raised_initiative" in init
    assert "f$cc_native_limped_initiative" in init

    first = block(HIST, "f$cc_turn_delayed_cbet_first_turn_action_clean")
    for token in ("IsTurn", "BotsActionsOnThisRoundIncludingChecks = 0", "AmountToCall = 0", "balance > 0", "f$cc_relpos_id >= 1 && f$cc_relpos_id <= 3"):
        assert token in first

    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base
    assert "f$cc_turn_delayed_cbet_initiative_supported" in base
    assert "f$cc_relpos_id = 3 Return false" not in base

    overlap = block(HIST, "f$cc_turn_delayed_cbet_probe_overlap")
    assert "f$cc_turn_probe_base_opportunity" in overlap


def snapshot_contract() -> None:
    eligible = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_capture_eligible")
    for token in ("IsFlop", "BotsActionsOnThisRoundIncludingChecks = 0", "AmountToCall = 0", "f$cc_native_limped_initiative"):
        assert token in eligible

    husb_tp = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_husb_tp_candidate")
    for token in ("board$A || board$K", "rankloplayer < 7", "f$cc_hu_effective_stack_round_start_bb <= 16", "SuitsOnBoard = 3"):
        assert token in husb_tp

    husb_air = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_husb_air_straight_candidate")
    assert "f$cc_air_no_frontdoor" in husb_air
    assert "StraightPossibleOnFlop" in husb_air

    hubb = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_hubb_thirdpair_deldel_candidate")
    assert "f$cc_turn_delayed_cbet_flop_two_7toK" in hubb

    btn_nomade = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnvbb_nomade_candidate")
    assert "f$cc_hand_no_made" in btn_nomade

    writer = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_writer")
    for token in (
        "Set user_cc_turn_delayed_cbet_flop_snapshot_seen",
        "Set user_cc_turn_delayed_cbet_husb_flop_air_straight_candidate",
        "Set user_cc_turn_delayed_cbet_hubb_flop_thirdpair_candidate",
        "Set user_cc_turn_delayed_cbet_3w_btnvbb_flop_nomade_candidate",
    ):
        assert token in writer

    valid = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_valid")
    assert "f$cc_turn_delayed_cbet_base_opportunity" in valid
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in valid


def source_contract() -> None:
    husb_action = block(SOURCE, "f$cc_turn_delayed_cbet_husb_source_action")
    assert "user_cc_turn_delayed_cbet_husb_flop_tpcheck_candidate" in husb_action
    assert "user_cc_turn_delayed_cbet_husb_flop_air_straight_candidate" in husb_action
    assert "f$cc_turn_delayed_cbet_no_made Return true Force" in husb_action

    hubb_third = block(SOURCE, "f$cc_turn_delayed_cbet_hubb_thirdpair_action")
    assert "f$cc_turn_delayed_cbet_third_pair && f$cc_turn_delayed_cbet_turn_under Return true Force" in hubb_third
    assert "user_cc_turn_delayed_cbet_hubb_flop_thirdpair_deldel_candidate" in hubb_third

    hubb_air = block(SOURCE, "f$cc_turn_delayed_cbet_hubb_air_action")
    assert "f$cc_turn_delayed_cbet_turn_completed && f$cc_turn_delayed_cbet_turn_three_8toK Return false Force" in hubb_air
    assert "f$cc_turn_delayed_cbet_no_made Return true Force" in hubb_air

    btn = block(SOURCE, "f$cc_turn_delayed_cbet_3w_btnvbb_source_action")
    assert "nstraightcommon >= 4 || nsuitedcommon >= 4" in btn
    assert "f$cc_turn_delayed_cbet_no_made || f$cc_turn_delayed_cbet_third_pair" in btn

    btn_size = block(SOURCE, "f$cc_turn_delayed_cbet_3w_btnvbb_source_size_id")
    assert "f$cc_turn_delayed_cbet_size_625_id" in btn_size
    assert "rankhiplayer >= 10 Return f$cc_turn_delayed_cbet_size_75_id" in btn_size

    river625 = block(SOURCE, "f$cc_turn_delayed_cbet_3w_btnvbb_plan_river625")
    assert "flop_nomade_candidate" in river625
    assert "f$cc_turn_delayed_cbet_no_made || f$cc_turn_delayed_cbet_third_pair" in river625


def exact_size_contract() -> None:
    assert block(COMMON, "f$cc_turn_delayed_cbet_size_625_id").strip().startswith("3")
    # This gate must preserve the source size as its own ID, never alias 50/66.
    source = block(SOURCE, "f$cc_turn_delayed_cbet_3w_btnvbb_source_size_id")
    assert "f$cc_turn_delayed_cbet_size_625_id" in source
    assert "size_50_id" in source
    assert "size_75_id" in source


def router_and_safety_contract() -> None:
    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_husb_source_context Return 1 Force" in fam
    assert "f$cc_turn_delayed_cbet_hubb_source_context Return 2 Force" in fam
    assert "f$cc_turn_delayed_cbet_3w_btnvbb_source_context Return 3 Force" in fam

    router = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "When Others Return false Force" in router
    cov = block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_core_source_covered" in cov

    for text in (LIMP, HIST, COMMON, SNAP, SOURCE, ROUTER):
        code = executable(text).lower()
        for forbidden in ("handpower", "random", "betmax", "raise_committed", "shorteststack"):
            assert forbidden not in code, f"forbidden Gate12A core executable leak: {forbidden}"


if __name__ == "__main__":
    limped_initiative_contract()
    ownership_contract()
    snapshot_contract()
    source_contract()
    exact_size_contract()
    router_and_safety_contract()
    print("PASS: Gate12A core Turn Delayed-CBet source contract")
