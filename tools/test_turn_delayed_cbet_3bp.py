#!/usr/bin/env python3
"""Gate12A 4-6h plain3BP/squeeze Turn Delayed-CBet P-heavy contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3BP.txt").read_text(encoding="utf-8")
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
    parent = block(POL, "f$cc_turn_delayed_cbet_3bp_parent")
    for token in (
        "f$cc_turn_delayed_cbet_base_opportunity",
        "f$cc_deal_size >= 4 && f$cc_deal_size <= 6",
        "f$cc_pot_family_id = 3",
        "f$cc_pf_role_3bettor",
        "f$cc_pf_3bet_order_supported",
        "f$cc_pf_3bet_final_raiser_pos_id = f$cc_hero_pos_id",
    ):
        assert token in parent

    plain = block(POL, "f$cc_turn_delayed_cbet_plain3bp_parent")
    assert "f$cc_pf_3bet_plain_proven" in plain and "!f$cc_pf_squeeze_proven" in plain
    squeeze = block(POL, "f$cc_turn_delayed_cbet_squeeze_parent")
    assert "f$cc_pf_squeeze_proven" in squeeze and "!f$cc_pf_3bet_plain_proven" in squeeze

    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base

    for name in ("f$cc_turn_delayed_cbet_plain3bp_hu_context", "f$cc_turn_delayed_cbet_squeeze_hu_context"):
        hu = block(POL, name)
        assert "f$cc_flop_entry_count = 2" in hu
        assert "f$cc_hu_origin_preflop_reduced" in hu
        assert "postflop" not in executable(hu).lower()


def plain_survivor_contract() -> None:
    opener = block(POL, "f$cc_turn_delayed_cbet_plain3bp_hu_vs_opener")
    cold = block(POL, "f$cc_turn_delayed_cbet_plain3bp_hu_vs_coldcaller")
    assert "f$cc_hu_3bp_villain_is_opener" in opener
    assert "!f$cc_hu_3bp_villain_is_post3bet_coldcaller" in opener
    assert "f$cc_hu_3bp_villain_is_post3bet_coldcaller" in cold
    assert "!f$cc_hu_3bp_villain_is_opener" in cold

    mw = block(POL, "f$cc_turn_delayed_cbet_plain3bp_mw_supported")
    assert "f$cc_turn_delayed_cbet_plain3bp_mw_opener_count <= 1" in mw
    assert "f$cc_turn_delayed_cbet_plain3bp_mw_coldcaller_count" in mw
    assert "= (nplayersplaying - 1)" in mw


def squeeze_survivor_contract() -> None:
    sid = block(POL, "f$cc_turn_delayed_cbet_squeeze_hu_survivor_type_id")
    assert "f$cc_hu_3bp_villain_is_opener Return 1 Force" in sid
    assert "f$cc_hu_3bp_villain_is_pre3bet_coldcaller Return 2 Force" in sid
    assert "f$cc_hu_3bp_villain_is_post3bet_coldcaller Return 3 Force" in sid
    sup = block(POL, "f$cc_turn_delayed_cbet_squeeze_hu_supported")
    assert "f$cc_hu_3bp_survivor_consistent" in sup

    mw = block(POL, "f$cc_turn_delayed_cbet_squeeze_mw_supported")
    for token in (
        "f$cc_turn_delayed_cbet_squeeze_mw_opener_count",
        "f$cc_turn_delayed_cbet_squeeze_mw_pre3bet_count",
        "f$cc_turn_delayed_cbet_squeeze_mw_post3bet_count",
        "= (nplayersplaying - 1)",
    ):
        assert token in mw


def quality_contract() -> None:
    two = block(POL, "f$cc_turn_delayed_cbet_3bp_exact_two_pair")
    assert "HaveTwoPair" in two and "!TwoPairOnBoard" in two and "npcbits > 0" in two
    strong = block(POL, "f$cc_turn_delayed_cbet_3bp_strong_value")
    assert "f$cc_turn_delayed_cbet_two_pair_plus_real" in strong
    assert "!f$cc_turn_delayed_cbet_3bp_exact_two_pair" in strong
    tp = block(POL, "f$cc_turn_delayed_cbet_3bp_strong_tp")
    assert "f$cc_number_better_kickers <= 2" in tp
    danger = block(POL, "f$cc_turn_delayed_cbet_3bp_dangerous_runout")
    assert "f$cc_turn_completed" in danger
    assert "f$cc_turn_four_card_straight_or_flush" in danger
    draw = block(POL, "f$cc_turn_delayed_cbet_3bp_premium_draw")
    for token in ("f$cc_real_combo_draw", "f$cc_real_nut_fd", "f$cc_real_oesd", "f$cc_real_fd"):
        assert token in draw


def policy_contract() -> None:
    phu = block(POL, "f$cc_turn_delayed_cbet_plain3bp_hu_action")
    assert "f$cc_turn_delayed_cbet_3bp_strong_value Return true Force" in phu
    assert "exact_two_pair && f$cc_turn_delayed_cbet_3bp_dangerous_runout Return false Force" in phu
    assert "f$cc_turn_delayed_cbet_overpair_real && f$cc_turn_delayed_cbet_plain3bp_hu_vs_opener" in phu
    assert "f$cc_turn_delayed_cbet_overpair_real && f$cc_hu_ip" in phu
    assert "f$cc_turn_delayed_cbet_3bp_strong_tp && f$cc_turn_delayed_cbet_plain3bp_hu_vs_opener" in phu
    assert "f$cc_turn_delayed_cbet_3bp_premium_draw && f$cc_hu_ip" in phu
    assert "f$cc_hand_no_made Return false Force" in phu

    pmw = block(POL, "f$cc_turn_delayed_cbet_plain3bp_mw_action")
    assert "f$cc_turn_delayed_cbet_3bp_strong_value Return true Force" in pmw
    assert "f$cc_turn_delayed_cbet_overpair_real Return false Force" in pmw
    assert "f$cc_turn_delayed_cbet_top_pair_real Return false Force" in pmw
    assert "f$cc_turn_delayed_cbet_3bp_premium_draw && f$cc_relpos_id = 3" in pmw

    shu = block(POL, "f$cc_turn_delayed_cbet_squeeze_hu_action")
    assert "f$cc_turn_delayed_cbet_squeeze_hu_survivor_type_id = 1" in shu
    assert "f$cc_turn_delayed_cbet_overpair_real Return false Force" in shu
    assert "f$cc_turn_delayed_cbet_top_pair_real Return false Force" in shu
    assert "f$cc_turn_delayed_cbet_3bp_premium_draw && f$cc_hu_ip" in shu

    smw = block(POL, "f$cc_turn_delayed_cbet_squeeze_mw_action")
    assert "f$cc_turn_delayed_cbet_3bp_strong_value Return true Force" in smw
    assert "f$cc_turn_delayed_cbet_overpair_real Return false Force" in smw
    assert "f$cc_turn_delayed_cbet_top_pair_real Return false Force" in smw
    assert "f$cc_turn_delayed_cbet_3bp_premium_draw Return false Force" in smw

    code = executable(phu + "\n" + pmw + "\n" + shu + "\n" + smw).lower()
    for token in ("source_air", "quality_air", "flop_air", "air_candidate"):
        assert token not in code, f"pure-air delayed parent leaked into 3BP policy: {token}"


def sizing_contract() -> None:
    for name in (
        "f$cc_turn_delayed_cbet_plain3bp_hu_size_id",
        "f$cc_turn_delayed_cbet_plain3bp_mw_size_id",
        "f$cc_turn_delayed_cbet_squeeze_hu_size_id",
        "f$cc_turn_delayed_cbet_squeeze_mw_size_id",
    ):
        text = executable(block(POL, name))
        assert "f$cc_turn_delayed_cbet_size_50_id" in text
        assert "f$cc_turn_delayed_cbet_size_75_id" in text or name.endswith("squeeze_mw_size_id")
        for forbidden in (
            "f$cc_turn_delayed_cbet_size_min_id",
            "f$cc_turn_delayed_cbet_size_33_id",
            "f$cc_turn_delayed_cbet_size_625_id",
            "f$cc_turn_delayed_cbet_size_100_id",
            "f$cc_turn_delayed_cbet_size_150_id",
        ):
            assert forbidden not in text


def coverage_router_contract() -> None:
    for name in (
        "f$cc_turn_delayed_cbet_plain3bp_hu_covered",
        "f$cc_turn_delayed_cbet_plain3bp_mw_covered",
        "f$cc_turn_delayed_cbet_squeeze_hu_covered",
        "f$cc_turn_delayed_cbet_squeeze_mw_covered",
    ):
        assert name in block(POL, "f$cc_turn_delayed_cbet_3bp_covered")
    unresolved = block(POL, "f$cc_turn_delayed_cbet_3bp_unresolved")
    assert "f$cc_turn_delayed_cbet_3bp_parent && !f$cc_turn_delayed_cbet_3bp_covered" in unresolved

    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    for fid, name in enumerate((
        "f$cc_turn_delayed_cbet_plain3bp_hu_covered",
        "f$cc_turn_delayed_cbet_plain3bp_mw_covered",
        "f$cc_turn_delayed_cbet_squeeze_hu_covered",
        "f$cc_turn_delayed_cbet_squeeze_mw_covered",
    ), start=13):
        assert f"{name} Return {fid} Force" in fam
    action = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert action.count("Return f$cc_turn_delayed_cbet_3bp_action Force") == 4
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert size.count("Return f$cc_turn_delayed_cbet_3bp_size_id Force") == 4
    assert "f$cc_turn_delayed_cbet_3bp_covered" in block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_3bp_size_consistent" in block(ROUTER, "f$cc_turn_delayed_cbet_router_consistent")


def provenance_safety_contract() -> None:
    low = POL.lower()
    assert "p-heavy" in low
    assert "no clean 4-6h plain-3bp or squeeze delayed-cbet range tree" in low
    assert "no pure-air barrel" in low
    code = executable(POL + "\n" + ROUTER).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe 3BP delayed-CBet leak: {forbidden}"


if __name__ == "__main__":
    ownership_contract()
    plain_survivor_contract()
    squeeze_survivor_contract()
    quality_contract()
    policy_contract()
    sizing_contract()
    coverage_router_contract()
    provenance_safety_contract()
    print("PASS: Gate12A 4-6h plain3BP/squeeze delayed-CBet adaptation")
