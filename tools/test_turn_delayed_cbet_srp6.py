#!/usr/bin/env python3
"""Gate12A 4-6h ordinary-SRP Turn Delayed-CBet P-heavy contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_SRP_6Max.txt").read_text(encoding="utf-8")
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


def parent_contract() -> None:
    parent = block(POL, "f$cc_turn_delayed_cbet_srp6_parent")
    for token in (
        "f$cc_turn_delayed_cbet_base_opportunity",
        "f$cc_deal_size >= 4 && f$cc_deal_size <= 6",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_role_pfa",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_single_raiser_pos_id = f$cc_hero_pos_id",
    ):
        assert token in parent
    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base
    assert "f$cc_turn_delayed_cbet_initiative_supported" in base

    hu = block(POL, "f$cc_turn_delayed_cbet_srp6_hu_context")
    assert "f$cc_flop_entry_count = 2" in hu
    assert "f$cc_hu_origin_preflop_reduced" in hu
    ip = block(POL, "f$cc_turn_delayed_cbet_srp6_hu_ip_blind")
    assert "f$cc_hu_ip" in ip and "f$cc_hu_villain_pos_id = 5" in ip and "f$cc_hu_villain_pos_id = 6" in ip
    oop = block(POL, "f$cc_turn_delayed_cbet_srp6_hu_oop_nonblind")
    assert "f$cc_hu_oop" in oop
    assert "f$cc_hu_villain_pos_id >= 1 && f$cc_hu_villain_pos_id <= 4" in oop

    mw = block(POL, "f$cc_turn_delayed_cbet_srp6_mw_context")
    assert "f$cc_flop_entry_count >= 3" in mw
    assert "f$cc_multiway" in mw


def quality_contract() -> None:
    two = block(POL, "f$cc_turn_delayed_cbet_srp6_exact_two_pair")
    assert "HaveTwoPair" in two and "!TwoPairOnBoard" in two and "npcbits > 0" in two
    strong = block(POL, "f$cc_turn_delayed_cbet_srp6_strong_value")
    assert "f$cc_turn_delayed_cbet_two_pair_plus_real" in strong
    assert "!f$cc_turn_delayed_cbet_srp6_exact_two_pair" in strong
    stp = block(POL, "f$cc_turn_delayed_cbet_srp6_strong_tp")
    assert "f$cc_number_better_kickers <= 2" in stp
    mtp = block(POL, "f$cc_turn_delayed_cbet_srp6_medium_tp")
    assert "f$cc_number_better_kickers > 2" in mtp and "<= 4" in mtp
    danger = block(POL, "f$cc_turn_delayed_cbet_srp6_dangerous_runout")
    assert "f$cc_turn_completed" in danger
    assert "f$cc_turn_four_card_straight_or_flush" in danger
    premium = block(POL, "f$cc_turn_delayed_cbet_srp6_premium_draw")
    for token in ("f$cc_real_combo_draw", "f$cc_real_nut_fd", "f$cc_real_oesd", "f$cc_real_fd"):
        assert token in premium


def assert_no_air_parent(code: str) -> None:
    # Avoid the old substring trap: the letters "air" occur inside "pair".
    # We ban actual saved/source AIR strategy tokens instead.
    for token in ("source_air", "quality_air", "flop_air", "air_candidate"):
        assert token not in code, f"pure-air parent leaked into SRP6 action: {token}"


def hu_policy_contract() -> None:
    action = block(POL, "f$cc_turn_delayed_cbet_srp6_hu_action")
    assert "f$cc_turn_delayed_cbet_srp6_strong_value Return true Force" in action
    assert "exact_two_pair && f$cc_turn_delayed_cbet_srp6_dangerous_runout Return false Force" in action
    assert "f$cc_turn_delayed_cbet_overpair_real && f$cc_turn_delayed_cbet_srp6_dangerous_runout Return false Force" in action
    assert "f$cc_turn_delayed_cbet_srp6_strong_tp Return true Force" in action
    assert "f$cc_turn_delayed_cbet_srp6_hu_ip_blind && f$cc_hero_pos_id >= 3" in action
    assert "f$cc_turn_delayed_cbet_srp6_hu_oop_nonblind && f$cc_turn_delayed_cbet_srp6_premium_draw && f$cc_turn_delayed_cbet_srp6_high_pressure_turn Return true Force" in action
    assert "f$cc_hand_no_made Return false Force" in action
    assert_no_air_parent(executable(action).lower())

    size = block(POL, "f$cc_turn_delayed_cbet_srp6_hu_size_id")
    for token in (
        "f$cc_turn_delayed_cbet_size_33_id",
        "f$cc_turn_delayed_cbet_size_50_id",
        "f$cc_turn_delayed_cbet_size_75_id",
    ):
        assert token in size


def mw_policy_contract() -> None:
    action = block(POL, "f$cc_turn_delayed_cbet_srp6_mw_action")
    assert "f$cc_turn_delayed_cbet_srp6_strong_value Return true Force" in action
    assert "exact_two_pair && f$cc_turn_delayed_cbet_srp6_dangerous_runout Return false Force" in action
    assert "f$cc_turn_delayed_cbet_overpair_real && f$cc_relpos_id = 3" in action
    assert "f$cc_turn_delayed_cbet_srp6_strong_tp && f$cc_relpos_id = 3" in action
    assert "f$cc_turn_delayed_cbet_srp6_premium_draw && f$cc_relpos_id = 3" in action
    assert "f$cc_hand_no_made Return false Force" in action
    assert_no_air_parent(executable(action).lower())
    size = block(POL, "f$cc_turn_delayed_cbet_srp6_mw_size_id")
    assert "f$cc_turn_delayed_cbet_size_50_id" in size
    assert "f$cc_turn_delayed_cbet_size_75_id" in size
    assert "f$cc_turn_delayed_cbet_size_33_id" not in executable(size)


def coverage_router_contract() -> None:
    assert "f$cc_turn_delayed_cbet_srp6_hu_covered" in block(POL, "f$cc_turn_delayed_cbet_srp6_covered")
    assert "f$cc_turn_delayed_cbet_srp6_mw_covered" in block(POL, "f$cc_turn_delayed_cbet_srp6_covered")
    unresolved = block(POL, "f$cc_turn_delayed_cbet_srp6_unresolved")
    assert "f$cc_turn_delayed_cbet_srp6_parent && !f$cc_turn_delayed_cbet_srp6_covered" in unresolved

    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_srp6_hu_covered Return 9 Force" in fam
    assert "f$cc_turn_delayed_cbet_srp6_mw_covered Return 10 Force" in fam
    action = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "f$cc_turn_delayed_cbet_srp6_hu_covered Return f$cc_turn_delayed_cbet_srp6_hu_action" in action
    assert "f$cc_turn_delayed_cbet_srp6_mw_covered Return f$cc_turn_delayed_cbet_srp6_mw_action" in action
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert "f$cc_turn_delayed_cbet_srp6_hu_size_id" in size
    assert "f$cc_turn_delayed_cbet_srp6_mw_size_id" in size
    assert "f$cc_turn_delayed_cbet_srp6_covered" in block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_srp6_size_consistent" in block(ROUTER, "f$cc_turn_delayed_cbet_router_consistent")


def provenance_safety_contract() -> None:
    low = POL.lower()
    assert "p-heavy" in low
    assert "no 4-6h" in low
    assert "pure-air turn barrels are deliberately absent" in low
    code = executable(POL + "\n" + ROUTER).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe SRP6 delayed-CBet leak: {forbidden}"


if __name__ == "__main__":
    parent_contract()
    quality_contract()
    hu_policy_contract()
    mw_policy_contract()
    coverage_router_contract()
    provenance_safety_contract()
    print("PASS: Gate12A 4-6h ordinary-SRP delayed-CBet adaptation")
