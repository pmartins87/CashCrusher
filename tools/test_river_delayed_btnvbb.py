#!/usr/bin/env python3
"""Gate13E native 3wBTNvBB River Delayed direct-source contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = (ROOT / "src" / "CashCrusher_River_Delayed_BTNvBB_Source.txt").read_text(encoding="utf-8")
R = (ROOT / "src" / "CashCrusher_River_Delayed.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text.split(marker, 1)[1]
    return tail.split("##", 1)[0]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def context_contract() -> None:
    ctx = block(S, "f$cc_river_delayed_3w_btnvbb_context")
    for token in (
        "f$cc_river_delayed_after_standard_turncheck_valid",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_hero_pos_id = 4",
        "f$cc_hu_villain_pos_id = 6",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_role_pfa",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_hist_turn_state_family_id = 1",
    ):
        assert token in ctx, token

    snap = block(S, "f$cc_river_delayed_3w_btnvbb_flop_snapshot_valid")
    for token in (
        "f$cc_hist_flop_initial_cbet_executed",
        "f$cc_hist_flop_cbet_snapshot_consistent",
        "!f$cc_hist_flop_cbet_runtime_mismatch",
    ):
        assert token in snap, token


def flop_plan_contract() -> None:
    bw = block(S, "f$cc_river_delayed_3w_btnvbb_flop_bw_count")
    for card in ("FirstFlopCard", "SecondFlopCard", "ThirdFlopCard"):
        assert f"{card} >= 10" in bw and f"{card} <= 14" in bw

    one = executable(block(S, "f$cc_river_delayed_3w_btnvbb_flop_1bw")).strip()
    assert one == "f$cc_river_delayed_3w_btnvbb_flop_bw_count = 1"
    two = executable(block(S, "f$cc_river_delayed_3w_btnvbb_flop_2bw_or_more")).strip()
    assert two == "f$cc_river_delayed_3w_btnvbb_flop_bw_count >= 2"

    low = block(S, "f$cc_river_delayed_3w_btnvbb_flop_2verylow")
    assert low.count(">= 2") == 6
    assert low.count("<= 5") == 6

    ace = block(S, "f$cc_river_delayed_3w_btnvbb_flop_had_ace")
    assert "FirstFlopCard = 14" in ace
    assert "SecondFlopCard = 14" in ace
    assert "ThirdFlopCard = 14" in ace

    nonrainbow = executable(block(S, "f$cc_river_delayed_3w_btnvbb_flop_nonrainbow")).strip()
    assert nonrainbow == "user_cc_flop_cbet_flop_monotone || user_cc_flop_cbet_flop_twotone"

    r50 = block(S, "f$cc_river_delayed_3w_btnvbb_gu_r50_plan")
    for token in (
        "user_cc_flop_cbet_had_no_made",
        "!f$cc_river_delayed_3w_btnvbb_flop_had_ace",
        "f$cc_river_delayed_3w_btnvbb_flop_1bw",
        "f$cc_river_delayed_3w_btnvbb_flop_nonrainbow || f$cc_river_delayed_3w_btnvbb_flop_2verylow",
    ):
        assert token in r50, token

    r75 = block(S, "f$cc_river_delayed_3w_btnvbb_gu_r75_plan")
    assert "user_cc_flop_cbet_had_no_made" in r75
    assert "!f$cc_river_delayed_3w_btnvbb_flop_had_ace" in r75
    assert "f$cc_river_delayed_3w_btnvbb_flop_2bw_or_more" in r75


def turn_and_river_contract() -> None:
    tx = block(S, "f$cc_river_delayed_3w_btnvbb_turnx_r75_parent")
    for token in (
        "user_cc_flop_cbet_had_top_pair",
        "user_cc_flop_cbet_tp_kicker_below_t",
        "!user_cc_flop_cbet_had_bdsd",
        "user_cc_turn_state_had_top_pair",
    ):
        assert token in tx, token

    for name in (
        "f$cc_river_delayed_3w_btnvbb_gu_r50_parent",
        "f$cc_river_delayed_3w_btnvbb_gu_r75_parent",
    ):
        assert "f$cc_river_delayed_no_made" in block(S, name)

    value = block(S, "f$cc_river_delayed_3w_btnvbb_overcard_value_parent")
    assert "f$cc_river_delayed_3w_btnvbb_tpplus_real" in value
    assert "RiverCardIsOvercardToBoard" in value

    action = block(S, "f$cc_river_delayed_3w_btnvbb_source_action")
    ordered = [
        "f$cc_river_delayed_3w_btnvbb_turnx_r75_parent",
        "f$cc_river_delayed_3w_btnvbb_gu_r50_parent",
        "f$cc_river_delayed_3w_btnvbb_gu_r75_parent",
        "f$cc_river_delayed_3w_btnvbb_overcard_value_parent",
    ]
    positions = [action.index(x) for x in ordered]
    assert positions == sorted(positions)

    size = block(S, "f$cc_river_delayed_3w_btnvbb_source_size_id")
    exact = (
        (ordered[0], "f$cc_river_delayed_size_75_id"),
        (ordered[1], "f$cc_river_delayed_size_50_id"),
        (ordered[2], "f$cc_river_delayed_size_75_id"),
        (ordered[3], "f$cc_river_delayed_size_100_id"),
    )
    for parent, size_id in exact:
        assert f"When {parent} Return {size_id} Force" in size

    covered = executable(block(S, "f$cc_river_delayed_3w_btnvbb_source_covered")).strip()
    assert covered == "f$cc_river_delayed_3w_btnvbb_source_action"
    pending = block(S, "f$cc_river_delayed_3w_btnvbb_source_pending")
    assert "f$cc_river_delayed_3w_btnvbb_context" in pending
    assert "!f$cc_river_delayed_3w_btnvbb_source_covered" in pending


def router_contract() -> None:
    fam = block(R, "f$cc_river_delayed_family_id")
    assert "When f$cc_river_delayed_3w_btnvbb_source_covered Return 6 Force" in fam

    action = block(R, "f$cc_river_delayed_router")
    assert "When f$cc_river_delayed_3w_btnvbb_source_covered Return f$cc_river_delayed_3w_btnvbb_source_action Force" in action
    size = block(R, "f$cc_river_delayed_size_id")
    assert "When f$cc_river_delayed_3w_btnvbb_source_covered Return f$cc_river_delayed_3w_btnvbb_source_size_id Force" in size
    coverage = block(R, "f$cc_river_delayed_strategy_covered")
    assert "f$cc_river_delayed_3w_btnvbb_source_covered" in coverage
    owners = block(R, "f$cc_river_delayed_child_owner_count")
    assert owners.count("* 1") == 6
    assert "f$cc_river_delayed_3w_btnvbb_source_covered" in owners
    consistent = block(R, "f$cc_river_delayed_router_consistent")
    assert "!f$cc_river_delayed_3w_btnvbb_source_size_consistent Return false Force" in consistent


def safety_contract() -> None:
    code = executable(S + "\n" + R).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "rivermax",
        "stackoff",
        "raise_committed",
    ):
        assert forbidden not in code, forbidden
    # Prevent the common semantic regression: source 2BW is >=2, not exactly two.
    assert "f$cc_flop_2bw" not in executable(S)
    # Source `SuitsOnFlop = 3` is rainbow; the GU_R50 reconstruction must use
    # persisted non-rainbow markers instead of reversing this meaning.
    assert "SuitsOnFlop = 3" not in executable(S)


if __name__ == "__main__":
    context_contract()
    flop_plan_contract()
    turn_and_river_contract()
    router_contract()
    safety_contract()
    print("PASS: Gate13 native 3wBTNvBB River Delayed source contract")
