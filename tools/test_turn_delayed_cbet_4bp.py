#!/usr/bin/env python3
"""Gate12A clean 4-6h HU 4BP Turn Delayed-CBet P-heavy contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_4BP.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_History.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def ownership_contract() -> None:
    parent = block(POL, "f$cc_turn_delayed_cbet_4bp_parent")
    for token in (
        "f$cc_turn_delayed_cbet_base_opportunity",
        "f$cc_deal_size >= 4 && f$cc_deal_size <= 6",
        "f$cc_pot_family_id = 4",
        "f$cc_pf_role_4bettor",
        "f$cc_pf_4bet_subtype_id > 0",
        "f$cc_pf_4bet_final_pos_id = f$cc_hero_pos_id",
    ):
        assert token in parent

    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base

    hu = block(POL, "f$cc_turn_delayed_cbet_4bp_hu_context")
    assert "f$cc_flop_entry_count = 2" in hu
    assert "f$cc_hu_origin_preflop_reduced" in hu
    assert "f$cc_hu_4bp_survivor_consistent" in hu
    assert "f$cc_hu_4bp_survivor_type_id > 0" in hu
    assert "f$cc_hu_4bp_survivor_type_id < 3" in hu
    assert "postflop" not in executable(hu).lower()


def family_contract() -> None:
    op4 = block(POL, "f$cc_turn_delayed_cbet_4bp_opener4_vs_threebettor")
    assert "f$cc_pf_4bet_standard_opener4_proven" in op4
    assert "f$cc_hu_4bp_villain_is_threebettor" in op4
    c4o = block(POL, "f$cc_turn_delayed_cbet_4bp_cold4_vs_opener")
    assert "f$cc_pf_4bet_standard_cold4_proven" in c4o
    assert "f$cc_hu_4bp_villain_is_opener" in c4o
    c4t = block(POL, "f$cc_turn_delayed_cbet_4bp_cold4_vs_threebettor")
    assert "f$cc_pf_4bet_standard_cold4_proven" in c4t
    assert "f$cc_hu_4bp_villain_is_threebettor" in c4t

    fid = block(POL, "f$cc_turn_delayed_cbet_4bp_family_id")
    assert "Return 1 Force" in fid and "Return 2 Force" in fid and "Return 3 Force" in fid
    supported = block(POL, "f$cc_turn_delayed_cbet_4bp_supported")
    assert "f$cc_turn_delayed_cbet_4bp_family_id >= 1" in supported
    assert "f$cc_turn_delayed_cbet_4bp_family_id <= 3" in supported


def quality_policy_contract() -> None:
    two = block(POL, "f$cc_turn_delayed_cbet_4bp_exact_two_pair")
    assert "HaveTwoPair" in two and "!TwoPairOnBoard" in two and "npcbits > 0" in two
    strong = block(POL, "f$cc_turn_delayed_cbet_4bp_strong_value")
    assert "f$cc_turn_delayed_cbet_two_pair_plus_real" in strong
    assert "!f$cc_turn_delayed_cbet_4bp_exact_two_pair" in strong
    tp = block(POL, "f$cc_turn_delayed_cbet_4bp_strong_tp")
    assert "f$cc_number_better_kickers <= 2" in tp
    danger = block(POL, "f$cc_turn_delayed_cbet_4bp_dangerous_runout")
    assert "f$cc_turn_completed" in danger
    assert "f$cc_turn_four_card_straight_or_flush" in danger
    draw = block(POL, "f$cc_turn_delayed_cbet_4bp_premium_draw")
    for token in ("f$cc_real_combo_draw", "f$cc_real_nut_fd", "f$cc_real_oesd", "f$cc_real_fd"):
        assert token in draw

    action = block(POL, "f$cc_turn_delayed_cbet_4bp_action")
    assert "f$cc_turn_delayed_cbet_4bp_strong_value Return true Force" in action
    assert "exact_two_pair && f$cc_turn_delayed_cbet_4bp_dangerous_runout Return false Force" in action
    assert "f$cc_turn_delayed_cbet_overpair_real && f$cc_turn_delayed_cbet_4bp_clean_turn Return true Force" in action
    assert "f$cc_turn_delayed_cbet_4bp_strong_tp && f$cc_hu_ip" in action
    assert "f$cc_turn_delayed_cbet_top_pair_real Return false Force" in action
    assert "f$cc_turn_delayed_cbet_4bp_premium_draw && f$cc_hu_ip" in action
    assert "f$cc_hand_no_made Return false Force" in action

    code = executable(action).lower()
    for token in ("source_air", "quality_air", "flop_air", "air_candidate"):
        assert token not in code, f"pure-air delayed parent leaked into 4BP policy: {token}"


def sizing_coverage_contract() -> None:
    size = executable(block(POL, "f$cc_turn_delayed_cbet_4bp_size_id"))
    assert "f$cc_turn_delayed_cbet_size_50_id" in size
    assert "f$cc_turn_delayed_cbet_size_75_id" in size
    for forbidden in (
        "f$cc_turn_delayed_cbet_size_min_id",
        "f$cc_turn_delayed_cbet_size_33_id",
        "f$cc_turn_delayed_cbet_size_625_id",
        "f$cc_turn_delayed_cbet_size_100_id",
        "f$cc_turn_delayed_cbet_size_150_id",
    ):
        assert forbidden not in size

    covered = block(POL, "f$cc_turn_delayed_cbet_4bp_covered")
    assert "f$cc_turn_delayed_cbet_4bp_supported" in covered
    unresolved = block(POL, "f$cc_turn_delayed_cbet_4bp_unresolved")
    assert "f$cc_turn_delayed_cbet_4bp_parent && !f$cc_turn_delayed_cbet_4bp_covered" in unresolved


def router_contract() -> None:
    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_4bp_covered Return 17 Force" in fam
    action = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "f$cc_turn_delayed_cbet_4bp_covered Return f$cc_turn_delayed_cbet_4bp_action Force" in action
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert "f$cc_turn_delayed_cbet_4bp_covered Return f$cc_turn_delayed_cbet_4bp_size_id Force" in size
    assert "f$cc_turn_delayed_cbet_4bp_covered" in block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_4bp_covered" in block(ROUTER, "f$cc_turn_delayed_cbet_child_owner_count")
    assert "f$cc_turn_delayed_cbet_4bp_size_consistent" in block(ROUTER, "f$cc_turn_delayed_cbet_router_consistent")


def provenance_safety_contract() -> None:
    low = POL.lower()
    assert "p-heavy" in low
    assert "no clean 4-6h four-bet delayed-cbet range tree" in low
    assert "multiway 4bp and other-caller survivor remain explicit unresolved gaps" in low
    code = executable(POL + "\n" + ROUTER).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe 4BP delayed-CBet leak: {forbidden}"


if __name__ == "__main__":
    ownership_contract()
    family_contract()
    quality_policy_contract()
    sizing_coverage_contract()
    router_contract()
    provenance_safety_contract()
    print("PASS: Gate12A clean 4-6h HU 4BP delayed-CBet adaptation")
