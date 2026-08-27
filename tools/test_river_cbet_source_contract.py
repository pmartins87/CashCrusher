#!/usr/bin/env python3
"""Gate03A/03B deterministic source/routing contract tests.

This protects source ancestry, Turn->River provenance and the deliberate cash
adaptation of historical RiverMax. It is not an OpenHoldem replay fixture.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TEXTURE = (SRC / "CashCrusher_River_Texture.txt").read_text(encoding="utf-8")
COMMON = (SRC / "CashCrusher_River_CBet_Common.txt").read_text(encoding="utf-8")
SOURCE = (SRC / "CashCrusher_River_CBet_SRP_Source.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_River_CBet.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def main() -> None:
    # Canonical River CBet must consume the STRICT closed-Turn parent.
    opp = block(COMMON, "f$cc_river_cbet_opportunity")
    assert "f$cc_hist_river_standard_cbet_parent_valid" in opp
    assert "AmountToCall > 0 Return false Force" in opp

    # Portable River texture reconstructs the exact source ingredients.
    for name in (
        "f$cc_river_completed",
        "f$cc_river_super_completed",
        "f$cc_river_new_completion",
        "f$cc_river_meaningful_overcard",
        "f$cc_river_pairs_previous_board",
        "f$cc_river_four_card_completion",
        "f$cc_river_turn_was_meaningful_overcard",
        "f$cc_river_husb_completed_moc_pressure",
    ):
        assert f"##{name}##" in TEXTURE, f"missing River texture helper: {name}"

    # Turn-MW -> River-HU is explicit and can never be mistaken for Turn-HU.
    postmw = block(COMMON, "f$cc_river_turn_mw_now_hu")
    assert "user_cc_turn_state_was_multiway" in postmw
    assert "BitCount(f$cc_opp_live_mask) = 1" in postmw
    turnhu = block(COMMON, "f$cc_river_turn_hu_still_hu")
    assert "user_cc_turn_state_was_hu" in turnhu
    assert "f$cc_opp_live_mask = f$cc_river_turn_live_opp_mask" in turnhu

    # Exact source descendant contexts remain distinct.
    expected_contexts = {
        "f$cc_river_srp_husb_context": ("f$cc_deal_size = 2", "f$cc_hero_pos_id = 5", "f$cc_river_turn_live_opp_mask = 32"),
        "f$cc_river_srp_btn_vs_bb_context": ("f$cc_hero_pos_id = 4", "f$cc_river_turn_live_opp_mask = 32"),
        "f$cc_river_srp_btn_vs_sb_context": ("f$cc_hero_pos_id = 4", "f$cc_river_turn_live_opp_mask = 16"),
        "f$cc_river_srp_hubb_context": ("f$cc_deal_size = 2", "f$cc_hero_pos_id = 6", "f$cc_river_turn_live_opp_mask = 16"),
        "f$cc_river_srp_sb_vs_bb_context": ("f$cc_hero_pos_id = 5", "f$cc_river_turn_live_opp_mask = 32"),
    }
    for name, tokens in expected_contexts.items():
        b = block(SOURCE, name)
        for token in tokens:
            assert token in b, f"{name} missing {token}"

    # HUSB source default must give up missed draw and air River barrels.
    husb = block(SOURCE, "f$cc_river_srp_husb_action")
    assert "When f$cc_river_turn_had_draw Return false Force" in husb
    assert "When f$cc_river_turn_had_air Return false Force" in husb
    assert "f$cc_river_husb_completed_moc_pressure Return false Force" in husb

    # BTN-v-BB exact source table: TPGK threshold and completed-River check.
    btnbb = block(SOURCE, "f$cc_river_srp_btn_vs_bb_action")
    assert "f$cc_river_top_pair && !f$cc_river_tpgk_source Return false Force" in btnbb
    assert "f$cc_river_top_pair && f$cc_river_completed Return false Force" in btnbb
    tpgk = block(COMMON, "f$cc_river_tpgk_source")
    assert "f$cc_number_better_kickers <= 3" in tpgk

    # Weak BTN-v-SB Turn50 is a two-street line unless River improves to 2P+.
    btnsb = block(SOURCE, "f$cc_river_srp_btn_vs_sb_action")
    assert "When f$cc_river_two_pair_plus Return true Force" in btnsb
    assert "When f$cc_river_btn_vs_sb_weak_tp_two_street_line Return false Force" in btnsb

    # Historical RiverMax must not be blindly imported in canonical source module.
    exe = executable(SOURCE)
    assert "BetMax" not in exe
    assert "RiverMax" not in exe

    # HUBB no-made TBP continuation is deliberately quarantined for blocker-aware audit.
    hubb = block(SOURCE, "f$cc_river_srp_hubb_action")
    assert "f$cc_river_turn_had_draw && f$cc_river_no_made Return false Force" in hubb

    # SB-v-BB only consumes the exact reconstructible Turn100 straight-completion line.
    sbline = block(SOURCE, "f$cc_river_sb_vs_bb_straightcompleted_turn100_line")
    assert "f$cc_river_turn_plan_size_id = 7" in sbline
    assert "!StraightPossibleOnFlop && StraightPossibleOnTurn" in sbline

    # Top-level router has a source-only positive child and explicit residual recognition.
    action = block(ROUTER, "f$cc_river_cbet_router")
    assert "When f$cc_river_srp_source_covered Return f$cc_river_srp_source_action Force" in action
    assert "When Others Return false Force" in action
    residual = block(ROUTER, "f$cc_river_srp_residual_context")
    assert "!f$cc_river_srp_source_covered" in residual

    print("PASS: Gate03A/03B River-CBet source/provenance contract")


if __name__ == "__main__":
    main()
