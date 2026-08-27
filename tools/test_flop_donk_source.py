#!/usr/bin/env python3
"""Gate07A/B direct `(BBorSB)v2pp` Flop Donk contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = (ROOT / "src" / "CashCrusher_Flop_Donk_Context.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_Flop_Donk_Source.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Flop_Donk.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def ownership_contract() -> None:
    opp = block(CTX, "f$cc_flop_donk_opportunity")
    for token in (
        "f$cc_flop_donk_first_hero_action",
        "AmountToCall > 0 Return false Force",
        "f$cc_relpos_id = 3 Return false Force",
        "f$cc_pf_rt_final_aggressor_is_hero Return false Force",
    ):
        assert token in opp

    shape = block(CTX, "f$cc_flop_donk_btn_both_blinds_live_shape")
    assert "nplayersplaying != 3" in shape
    assert "f$cc_flop_entry_count != 3" in shape
    assert "f$cc_hero_pos_id = 5 && f$cc_opp_live_mask = 40" in shape
    assert "f$cc_hero_pos_id = 6 && f$cc_opp_live_mask = 24" in shape

    limp = block(CTX, "f$cc_flop_donk_source_btn_limp_shape")
    assert "f$cc_deal_size = 3" in limp
    assert "f$cc_pot_family_id = 1" in limp
    assert "f$cc_pf_call_btn" in limp and "f$cc_pf_call_sb" in limp

    srp = block(CTX, "f$cc_flop_donk_source_btn_raise_shape")
    assert "f$cc_deal_size = 3" in srp
    assert "f$cc_pot_family_id = 2" in srp
    assert "f$cc_pf_single_raiser_pos_id = 4" in srp
    assert "f$cc_pf_call_sb" in srp and "f$cc_pf_call_bb" in srp

    six = block(CTX, "f$cc_flop_donk_sixmax_btn_blinds_ancestry_context")
    assert "f$cc_deal_size >= 4 && f$cc_deal_size <= 6" in six


def source_value_contract() -> None:
    action = block(POL, "f$cc_flop_donk_source_value_action")
    assert "f$cc_flop_donk_source_top_pair_plus" in action
    assert "AcePresentOnFlop Return false Force" in action
    assert "When Others Return true Force" in action

    size = block(POL, "f$cc_flop_donk_source_value_size_id")
    assert "f$cc_flop_donk_source_draw_heavy && f$cc_flop_donk_source_drawheavy_low_spr Return f$cc_flop_donk_size_100_id Force" in size
    assert "f$cc_flop_donk_source_draw_heavy Return f$cc_flop_donk_size_75_id Force" in size
    assert "f$cc_flop_donk_source_two_plus_bw Return f$cc_flop_donk_size_75_id Force" in size
    assert "f$cc_flop_donk_source_one_bw Return f$cc_flop_donk_size_50_id Force" in size
    assert "f$cc_flop_donk_source_zero_bw Return f$cc_flop_donk_size_75_id Force" in size

    spr = block(POL, "f$cc_flop_donk_source_drawheavy_low_spr")
    assert "f$cc_mw_spr_deepest_round_start" in spr
    assert "<= 1.25" in spr
    assert "shallowest" not in executable(spr).lower()


def pair_and_draw_contract() -> None:
    low = block(POL, "f$cc_flop_donk_source_lowpair_action")
    assert "f$cc_flop_donk_source_low_pair" in low
    assert "!f$cc_flop_donk_source_completed" in low
    assert "f$cc_flop_donk_size_50_id" in block(POL, "f$cc_flop_donk_source_lowpair_size_id")

    check = block(POL, "f$cc_flop_donk_source_draw_check_parent")
    assert "AcePresentOnFlop" in check
    assert "f$cc_flop_donk_source_completed" in check
    assert "f$cc_flop_donk_source_two_plus_bw" in check

    bet = block(POL, "f$cc_flop_donk_source_draw_bet_parent")
    assert "!f$cc_flop_donk_source_draw_check_parent" in bet
    assert "f$cc_flop_donk_source_one_bw" in bet
    assert "f$cc_flop_donk_source_zero_bw" in bet
    assert "PairOnFlop" in bet
    assert "f$cc_flop_donk_size_75_id" in block(POL, "f$cc_flop_donk_source_draw_size_id")


def safety_and_router_contract() -> None:
    code = executable(POL)
    for forbidden in (
        "HandPower",
        "random",
        "BetMax",
        "Raise_Committed",
        "StackOffDraws",
        "user_TurnShove",
    ):
        assert forbidden.lower() not in code.lower(), f"forbidden Gate07B executable leak: {forbidden}"

    covered = block(POL, "f$cc_flop_donk_source_covered")
    assert "f$cc_flop_donk_source_native_context" in covered

    family = block(ROUTER, "f$cc_flop_donk_family_id")
    assert "f$cc_flop_donk_source_covered Return 1 Force" in family

    router = block(ROUTER, "f$cc_flop_donk_router")
    assert "f$cc_flop_donk_source_covered Return f$cc_flop_donk_source_action Force" in router
    assert "When Others Return false Force" in router

    uncovered = block(ROUTER, "f$cc_flop_donk_uncovered_context")
    assert "f$cc_flop_donk_opportunity && !f$cc_flop_donk_strategy_covered" in uncovered

    # Same-shape 4-6h ancestry is not direct source coverage yet.
    assert "f$cc_flop_donk_sixmax_btn_blinds_ancestry_context" not in block(
        ROUTER, "f$cc_flop_donk_strategy_covered"
    )


if __name__ == "__main__":
    ownership_contract()
    source_value_contract()
    pair_and_draw_contract()
    safety_and_router_contract()
    print("PASS: Gate07A/B Flop Donk ownership + direct-source contract")
