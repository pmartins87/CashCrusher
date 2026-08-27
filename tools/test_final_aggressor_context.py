#!/usr/bin/env python3
"""Gate04R/Gate05A final-aggressor chronology contract tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

CTX = (SRC / "CashCrusher_FinalAggressor_Context.txt").read_text(encoding="utf-8")
REPAIR = (SRC / "CashCrusher_Flop_Float_3BP_CallerRepair.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_Flop_Float.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def run_final_aggressor_contract() -> None:
    valid = block(CTX, "f$cc_pf_rt_final_aggressor_history_valid")
    assert "lastraised1" in valid
    assert "raisbits1 >> lastraised1" in valid
    assert "f$cc_pf_raise_count <= 0" in valid

    pos = block(CTX, "f$cc_pf_rt_final_aggressor_pos_id")
    assert "f$cc_deal_size = 2" not in pos  # SB branch is generic after BTN>=3 guard
    assert "f$cc_deal_size >= 3 && lastraised1 = dealerchair Return 4 Force" in pos
    assert "lastraised1 = smallblindchair Return 5 Force" in pos
    # True HU dealer=SB must not be mapped to BTN; BTN line is explicitly >=3h.
    assert pos.index("dealerchair Return 4") < pos.index("smallblindchair Return 5")

    first = block(CTX, "f$cc_pf_rt_3bet_first_raiser_pos_id")
    assert "f$cc_pf_unique_raiser_count != 2" in first
    assert "f$cc_pf_rt_final_aggressor_pos_id" in first
    assert "f$cc_pf_hero_ever_raised" not in first
    assert "f$cc_pf_other_raiser_pos_id" not in first

    order = block(CTX, "f$cc_pf_rt_3bet_order_supported")
    assert "f$cc_pf_rt_3bet_first_raiser_pos_id < f$cc_pf_rt_final_aggressor_pos_id" in order
    assert "f$cc_pf_hero_ever_raised" not in order

    pre = block(CTX, "f$cc_pf_rt_hero_is_pre3bet_coldcaller")
    assert "f$cc_pf_role_cold_call_3bet" in pre
    assert "f$cc_hero_pos_id > f$cc_pf_rt_3bet_first_raiser_pos_id" in pre
    assert "f$cc_hero_pos_id < f$cc_pf_rt_final_aggressor_pos_id" in pre

    post = block(CTX, "f$cc_pf_rt_hero_is_post3bet_coldcaller")
    assert "f$cc_hero_pos_id > f$cc_pf_rt_final_aggressor_pos_id" in post


def run_repair_contract() -> None:
    plain = block(REPAIR, "f$cc_flop_float_rt3bp_plain_postcold_hu_context")
    for token in (
        "f$cc_pf_rt_plain3bet_proven",
        "f$cc_pf_rt_hero_is_post3bet_coldcaller",
        "f$cc_hu_villain_pos_id = f$cc_pf_rt_final_aggressor_pos_id",
    ):
        assert token in plain

    precold = block(REPAIR, "f$cc_flop_float_rt3bp_squeeze_precold_hu_context")
    assert "f$cc_pf_rt_squeeze_proven" in precold
    assert "f$cc_pf_rt_hero_is_pre3bet_coldcaller" in precold

    postcold = block(REPAIR, "f$cc_flop_float_rt3bp_squeeze_postcold_hu_context")
    assert "f$cc_pf_rt_hero_is_post3bet_coldcaller" in postcold

    mw = block(REPAIR, "f$cc_flop_float_rt3bp_multiway_context")
    assert "f$cc_pf_role_cold_call_3bet" in mw
    assert "f$cc_pf_rt_3bettor_live_opponent" in mw
    assert "f$cc_relpos_id = 3" in mw

    # Gate04R repairs chronology only: preserve the old conservative coldcaller policy.
    sq_action = block(REPAIR, "f$cc_flop_float_rt3bp_squeeze_coldcaller_hu_action")
    assert "f$cc_flop_float_premium_draw Return true Force" in sq_action
    assert "f$cc_flop_float_good_draw Return false Force" in sq_action
    assert "f$cc_flop_float_air Return false Force" in sq_action

    combined_plain = block(ROUTER, "f$cc_flop_float_plain3bp_covered_final")
    assert "f$cc_flop_float_plain3bp_covered" in combined_plain
    assert "f$cc_flop_float_rt3bp_plain_covered" in combined_plain

    combined_sq = block(ROUTER, "f$cc_flop_float_squeeze_covered_final")
    assert "f$cc_flop_float_squeeze_covered" in combined_sq
    assert "f$cc_flop_float_rt3bp_squeeze_covered" in combined_sq

    router = block(ROUTER, "f$cc_flop_float_router")
    assert "f$cc_flop_float_plain3bp_covered_final" in router
    assert "f$cc_flop_float_squeeze_covered_final" in router
    assert "When Others Return false Force" in router


def run_semantic_fixtures() -> None:
    # Canonical first-orbit examples for the contract itself.
    # first, final, hero, has-between-call -> expected caller origin.
    cases = [
        (1, 4, 1, False, "opener"),      # UTG open, BTN 3bet, UTG call
        (1, 4, 2, True, "pre-cold"),     # UTG open, HJ call, BTN squeeze
        (1, 4, 6, False, "post-cold"),   # UTG open, BTN 3bet, BB coldcall
        (4, 1, 6, True, "unsupported"),  # reversed final aggression
    ]
    for first, final, hero, between, expected in cases:
        if first >= final:
            got = "unsupported"
        elif hero == first:
            got = "opener"
        elif between and first < hero < final:
            got = "pre-cold"
        elif hero > final:
            got = "post-cold"
        else:
            got = "unsupported"
        assert got == expected, (first, final, hero, between, got, expected)


if __name__ == "__main__":
    run_final_aggressor_contract()
    run_repair_contract()
    run_semantic_fixtures()
    print("PASS: lastraised1 final-aggressor and Gate04R caller-side 3BP contract")
