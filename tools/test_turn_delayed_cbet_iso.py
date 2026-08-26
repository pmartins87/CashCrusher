#!/usr/bin/env python3
"""Gate12A proven-ISO Turn Delayed-CBet P-heavy contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_ISO.txt").read_text(encoding="utf-8")
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
    parent = block(POL, "f$cc_turn_delayed_cbet_iso_parent")
    for token in (
        "f$cc_turn_delayed_cbet_base_opportunity",
        "f$cc_deal_size >= 3 && f$cc_deal_size <= 6",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_role_pfa",
        "f$cc_pf_iso_proven",
        "f$cc_pf_single_raiser_pos_id = f$cc_hero_pos_id",
    ):
        assert token in parent

    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base
    assert "f$cc_turn_delayed_cbet_initiative_supported" in base

    hu = block(POL, "f$cc_turn_delayed_cbet_iso_hu_context")
    assert "f$cc_flop_entry_count = 2" in hu
    assert "f$cc_hu_origin_preflop_reduced" in hu
    assert "postflop" not in executable(hu).lower()


def survivor_contract() -> None:
    limper = block(POL, "f$cc_turn_delayed_cbet_iso_hu_limper")
    cold = block(POL, "f$cc_turn_delayed_cbet_iso_hu_coldcaller")
    assert "f$cc_hu_iso_villain_was_limper" in limper
    assert "!f$cc_hu_iso_villain_was_postraise_coldcaller" in limper
    assert "f$cc_hu_iso_villain_was_postraise_coldcaller" in cold
    assert "!f$cc_hu_iso_villain_was_limper" in cold

    sup = block(POL, "f$cc_turn_delayed_cbet_iso_hu_supported")
    assert "f$cc_turn_delayed_cbet_iso_hu_limper" in sup
    assert "f$cc_turn_delayed_cbet_iso_hu_coldcaller" in sup

    mw = block(POL, "f$cc_turn_delayed_cbet_iso_mw_context")
    assert "f$cc_flop_entry_count >= 3" in mw and "f$cc_multiway" in mw
    complete = block(POL, "f$cc_turn_delayed_cbet_iso_mw_origin_complete")
    assert "f$cc_turn_delayed_cbet_iso_mw_limper_count" in complete
    assert "f$cc_turn_delayed_cbet_iso_mw_coldcaller_count" in complete
    assert "= (nplayersplaying - 1)" in complete

    comp = block(POL, "f$cc_turn_delayed_cbet_iso_mw_comp_id")
    assert "Return 1 Force" in comp
    assert "Return 2 Force" in comp
    assert "Return 3 Force" in comp
    assert "f$cc_turn_delayed_cbet_iso_mw_origin_complete" in comp


def quality_contract() -> None:
    two = block(POL, "f$cc_turn_delayed_cbet_iso_exact_two_pair")
    assert "HaveTwoPair" in two and "!TwoPairOnBoard" in two and "npcbits > 0" in two
    strong = block(POL, "f$cc_turn_delayed_cbet_iso_strong_value")
    assert "f$cc_turn_delayed_cbet_two_pair_plus_real" in strong
    assert "!f$cc_turn_delayed_cbet_iso_exact_two_pair" in strong
    tp = block(POL, "f$cc_turn_delayed_cbet_iso_strong_tp")
    assert "f$cc_number_better_kickers <= 2" in tp
    medium = block(POL, "f$cc_turn_delayed_cbet_iso_medium_tp")
    assert "f$cc_number_better_kickers > 2" in medium and "<= 4" in medium
    danger = block(POL, "f$cc_turn_delayed_cbet_iso_dangerous_runout")
    for token in ("f$cc_turn_completed", "f$cc_turn_four_card_straight_or_flush", "f$cc_turn_super_completed"):
        assert token in danger
    draw = block(POL, "f$cc_turn_delayed_cbet_iso_premium_draw")
    for token in ("f$cc_real_combo_draw", "f$cc_real_nut_fd", "f$cc_real_oesd", "f$cc_real_fd"):
        assert token in draw


def policy_contract() -> None:
    limper = block(POL, "f$cc_turn_delayed_cbet_iso_hu_limper_action")
    assert "f$cc_turn_delayed_cbet_iso_strong_value Return true Force" in limper
    assert "exact_two_pair && f$cc_turn_delayed_cbet_iso_dangerous_runout Return false Force" in limper
    assert "f$cc_turn_delayed_cbet_overpair_real Return true Force" in limper
    assert "f$cc_turn_delayed_cbet_iso_strong_tp Return true Force" in limper
    assert "f$cc_turn_delayed_cbet_iso_medium_tp && f$cc_hu_ip" in limper
    assert "f$cc_turn_delayed_cbet_iso_premium_draw && f$cc_hu_oop && f$cc_turn_delayed_cbet_iso_high_pressure_turn" in limper
    assert "f$cc_hand_no_made Return false Force" in limper

    cold = block(POL, "f$cc_turn_delayed_cbet_iso_hu_coldcaller_action")
    assert "f$cc_turn_delayed_cbet_overpair_real && f$cc_hu_ip" in cold
    assert "f$cc_turn_delayed_cbet_overpair_real Return false Force" in cold
    assert "f$cc_turn_delayed_cbet_iso_strong_tp && f$cc_hu_ip" in cold
    assert "f$cc_turn_delayed_cbet_top_pair_real Return false Force" in cold
    assert "medium_tp" not in executable(cold)
    assert "f$cc_hand_no_made Return false Force" in cold

    mw = block(POL, "f$cc_turn_delayed_cbet_iso_mw_action")
    assert "f$cc_turn_delayed_cbet_iso_strong_value Return true Force" in mw
    assert "exact_two_pair && f$cc_turn_delayed_cbet_iso_dangerous_runout Return false Force" in mw
    assert "f$cc_turn_delayed_cbet_overpair_real && f$cc_relpos_id = 3 && f$cc_turn_delayed_cbet_iso_mw_all_limpers" in mw
    assert "f$cc_turn_delayed_cbet_iso_strong_tp && f$cc_relpos_id = 3 && f$cc_turn_delayed_cbet_iso_mw_all_limpers" in mw
    assert "f$cc_turn_delayed_cbet_iso_premium_draw && f$cc_relpos_id = 3 && f$cc_turn_delayed_cbet_iso_mw_all_limpers" in mw
    assert "f$cc_hand_no_made Return false Force" in mw

    # No executable saved/source AIR parent is allowed to manufacture a delayed bluff.
    code = executable(limper + "\n" + cold + "\n" + mw).lower()
    for token in ("source_air", "quality_air", "flop_air", "air_candidate"):
        assert token not in code, f"pure-air delayed parent leaked into ISO policy: {token}"


def sizing_contract() -> None:
    for name in (
        "f$cc_turn_delayed_cbet_iso_hu_limper_size_id",
        "f$cc_turn_delayed_cbet_iso_hu_coldcaller_size_id",
        "f$cc_turn_delayed_cbet_iso_mw_size_id",
    ):
        text = executable(block(POL, name))
        for forbidden in (
            "f$cc_turn_delayed_cbet_size_min_id",
            "f$cc_turn_delayed_cbet_size_625_id",
            "f$cc_turn_delayed_cbet_size_100_id",
            "f$cc_turn_delayed_cbet_size_150_id",
        ):
            assert forbidden not in text
        assert "f$cc_turn_delayed_cbet_size_50_id" in text
        assert "f$cc_turn_delayed_cbet_size_75_id" in text

    limper = block(POL, "f$cc_turn_delayed_cbet_iso_hu_limper_size_id")
    assert "f$cc_turn_delayed_cbet_size_33_id" in limper
    cold = executable(block(POL, "f$cc_turn_delayed_cbet_iso_hu_coldcaller_size_id"))
    mw = executable(block(POL, "f$cc_turn_delayed_cbet_iso_mw_size_id"))
    assert "f$cc_turn_delayed_cbet_size_33_id" not in cold
    assert "f$cc_turn_delayed_cbet_size_33_id" not in mw


def coverage_router_contract() -> None:
    assert "f$cc_turn_delayed_cbet_iso_hu_supported" in block(POL, "f$cc_turn_delayed_cbet_iso_hu_covered")
    assert "f$cc_turn_delayed_cbet_iso_mw_supported" in block(POL, "f$cc_turn_delayed_cbet_iso_mw_covered")
    unresolved = block(POL, "f$cc_turn_delayed_cbet_iso_unresolved")
    assert "f$cc_turn_delayed_cbet_iso_parent && !f$cc_turn_delayed_cbet_iso_covered" in unresolved

    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_iso_hu_covered Return 11 Force" in fam
    assert "f$cc_turn_delayed_cbet_iso_mw_covered Return 12 Force" in fam
    action = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert action.count("Return f$cc_turn_delayed_cbet_iso_action Force") == 2
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert size.count("Return f$cc_turn_delayed_cbet_iso_size_id Force") == 2
    assert "f$cc_turn_delayed_cbet_iso_covered" in block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    owners = block(ROUTER, "f$cc_turn_delayed_cbet_child_owner_count")
    assert "f$cc_turn_delayed_cbet_iso_hu_covered" in owners
    assert "f$cc_turn_delayed_cbet_iso_mw_covered" in owners
    assert "f$cc_turn_delayed_cbet_iso_size_consistent" in block(ROUTER, "f$cc_turn_delayed_cbet_router_consistent")


def provenance_safety_contract() -> None:
    low = POL.lower()
    assert "p-heavy" in low
    assert "no clean dedicated iso delayed-cbet range tree" in low
    assert "no pure-air delayed barrel" in low
    code = executable(POL + "\n" + ROUTER).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe ISO delayed-CBet leak: {forbidden}"


if __name__ == "__main__":
    ownership_contract()
    survivor_contract()
    quality_contract()
    policy_contract()
    sizing_contract()
    coverage_router_contract()
    provenance_safety_contract()
    print("PASS: Gate12A isolation-pot delayed-CBet adaptation")
