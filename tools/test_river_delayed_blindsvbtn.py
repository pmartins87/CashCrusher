#!/usr/bin/env python3
"""Gate13F true-multiway 3wBlinds-v-BTN direct-source contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = (ROOT / "src" / "CashCrusher_River_Delayed_BlindsVBTN_Source.txt").read_text(encoding="utf-8")
R = (ROOT / "src" / "CashCrusher_River_Delayed.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text.split(marker, 1)[1]
    return tail.split("##", 1)[0]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def context_contract() -> None:
    ctx = block(S, "f$cc_river_delayed_3w_blindsvbtn_context")
    for token in (
        "f$cc_river_delayed_base_opportunity",
        "f$cc_hist_river_delayed_cbet_check_parent_valid",
        "f$cc_hist_turn_delayed_cbet_family_id = 8",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 3",
        "f$cc_multiway",
        "f$cc_hist_turn_delayed_cbet_player_count = 3",
        "f$cc_opp_live_mask = f$cc_hist_turn_delayed_cbet_live_opp_mask",
        "f$cc_hero_pos_id = 5 || f$cc_hero_pos_id = 6",
    ):
        assert token in ctx, token


def source_contract() -> None:
    air = executable(block(S, "f$cc_river_delayed_3w_blindsvbtn_source_air"))
    assert "f$cc_river_delayed_3w_blindsvbtn_context" in air
    assert "f$cc_river_delayed_no_made" in air

    third = executable(block(S, "f$cc_river_delayed_3w_blindsvbtn_source_thirdpair"))
    assert "f$cc_river_delayed_3w_blindsvbtn_context" in third
    assert "f$cc_river_delayed_third_pair" in third

    action = block(S, "f$cc_river_delayed_3w_blindsvbtn_source_action")
    air_i = action.index("f$cc_river_delayed_3w_blindsvbtn_source_air")
    pair_i = action.index("f$cc_river_delayed_3w_blindsvbtn_source_thirdpair")
    assert air_i < pair_i
    assert "When Others Return false Force" in action

    size = block(S, "f$cc_river_delayed_3w_blindsvbtn_source_size_id")
    assert "When f$cc_river_delayed_3w_blindsvbtn_source_air Return f$cc_river_delayed_size_75_id Force" in size
    assert "When f$cc_river_delayed_3w_blindsvbtn_source_thirdpair Return f$cc_river_delayed_size_25_id Force" in size
    assert "When Others Return 0 Force" in size

    covered = executable(block(S, "f$cc_river_delayed_3w_blindsvbtn_source_covered")).strip()
    assert covered == "f$cc_river_delayed_3w_blindsvbtn_context"


def ancestry_firewall() -> None:
    code = executable(S)
    # Draw-donk is explicitly separate source ancestry and may not be executable here.
    assert "user_DC7_MW_DrawDonk" not in code
    for forbidden in ("HandPower", "Random", "BetMax", "RiverMax", "StackOff", "Raise_Committed"):
        assert forbidden not in code, forbidden


def router_contract() -> None:
    fam = block(R, "f$cc_river_delayed_family_id")
    assert "When f$cc_river_delayed_3w_blindsvbtn_source_covered Return 7 Force" in fam

    action = block(R, "f$cc_river_delayed_router")
    assert "When f$cc_river_delayed_3w_blindsvbtn_source_covered Return f$cc_river_delayed_3w_blindsvbtn_source_action Force" in action
    size = block(R, "f$cc_river_delayed_size_id")
    assert "When f$cc_river_delayed_3w_blindsvbtn_source_covered Return f$cc_river_delayed_3w_blindsvbtn_source_size_id Force" in size
    coverage = block(R, "f$cc_river_delayed_strategy_covered")
    assert "f$cc_river_delayed_3w_blindsvbtn_source_covered" in coverage
    owners = block(R, "f$cc_river_delayed_child_owner_count")
    assert owners.count("* 1") == 7
    consistent = block(R, "f$cc_river_delayed_router_consistent")
    assert "!f$cc_river_delayed_3w_blindsvbtn_source_size_consistent Return false Force" in consistent


if __name__ == "__main__":
    context_contract()
    source_contract()
    ancestry_firewall()
    router_contract()
    print("PASS: Gate13 true-multiway 3wBlinds-v-BTN source contract")
