#!/usr/bin/env python3
"""Gate13B/C current River vocabulary + first native direct-source contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = (ROOT / "src" / "CashCrusher_River_Delayed_Common.txt").read_text(encoding="utf-8")
S = (ROOT / "src" / "CashCrusher_River_Delayed_Native_Source.txt").read_text(encoding="utf-8")
R = (ROOT / "src" / "CashCrusher_River_Delayed.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text.split(marker, 1)[1]
    return tail.split("##", 1)[0]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def common_contract() -> None:
    value = block(C, "f$cc_river_delayed_two_pair_plus_real")
    for token in ("HaveNuts", "pokerval > pokervalcommon", "!TripsOnBoard", "!TwoPairOnBoard", "npcbits > 0"):
        assert token in value
    assert "FlushPossible || StraightPossible" in block(C, "f$cc_river_delayed_completed")
    ak = block(C, "f$cc_river_delayed_flop_had_ak")
    for card in ("FirstFlopCard", "SecondFlopCard", "ThirdFlopCard"):
        assert card in ak
    for name, val in (("min", 1), ("25", 2), ("33", 3), ("50", 4), ("75", 5), ("100", 6)):
        assert executable(block(C, f"f$cc_river_delayed_size_{name}_id")).strip() == str(val)


def hubb_contract() -> None:
    ctx = block(S, "f$cc_river_delayed_hubb_deldel_context")
    for token in ("f$cc_river_delayed_base_opportunity", "f$cc_true_hu", "f$cc_hero_pos_id = 6", "f$cc_hu_villain_pos_id = 5", "f$cc_hist_river_delayed_cbet_hubb_deldel_valid"):
        assert token in ctx

    action = block(S, "f$cc_river_delayed_hubb_deldel_action")
    for token in ("f$cc_river_delayed_two_pair_plus_real Return true", "f$cc_river_delayed_tpop_real Return true", "f$cc_river_delayed_second_pair Return true", "f$cc_river_delayed_third_pair Return true", "f$cc_hist_river_delayed_cbet_hubb_air_deldel_valid && f$cc_river_delayed_no_made Return true"):
        assert token in action
    assert "When Others Return false Force" in action

    size = block(S, "f$cc_river_delayed_hubb_deldel_size_id")
    for token in ("f$cc_river_delayed_completed Return f$cc_river_delayed_size_50_id", "Return f$cc_river_delayed_size_100_id", "f$cc_river_delayed_second_pair && f$cc_river_delayed_completed Return f$cc_river_delayed_size_25_id", "f$cc_river_delayed_third_pair Return f$cc_river_delayed_size_min_id", "f$cc_river_delayed_no_made Return f$cc_river_delayed_size_50_id"):
        assert token in size


def bbvsb_contract() -> None:
    ctx = block(S, "f$cc_river_delayed_3w_bbvsb_context")
    for token in ("f$cc_deal_size = 3", "f$cc_flop_entry_count = 2", "f$cc_hero_pos_id = 6", "f$cc_hu_villain_pos_id = 5"):
        assert token in ctx
    parent = block(S, "f$cc_river_delayed_3w_bbvsb_bxb50_parent")
    assert "f$cc_hist_river_delayed_cbet_bbvsb_bxb50_valid" in parent
    assert "f$cc_hist_river_delayed_float_source_bxb_river50_valid" in parent
    skip = block(S, "f$cc_river_delayed_3w_bbvsb_skip_parent")
    assert "f$cc_hist_river_delayed_float_source_skip_bxb_valid" in skip

    action = block(S, "f$cc_river_delayed_3w_bbvsb_source_action")
    assert "f$cc_river_delayed_3w_bbvsb_skip_parent Return false Force" in action
    assert "f$cc_hist_river_delayed_cbet_bbvsb_bxb50_valid && f$cc_river_delayed_flop_had_ak && f$cc_river_delayed_no_made Return false Force" in action
    assert "f$cc_river_delayed_3w_bbvsb_bxb50_parent && f$cc_river_delayed_no_made Return true Force" in action
    assert "f$cc_river_delayed_size_50_id" in block(S, "f$cc_river_delayed_3w_bbvsb_source_size_id")


def sbvbb_and_negative_contract() -> None:
    sb = block(S, "f$cc_river_delayed_3w_sbvbb_deldel50_parent")
    assert "f$cc_hist_river_delayed_cbet_sbvbb_lowpair_deldel50_valid" in sb
    assert "f$cc_hist_river_delayed_cbet_sbvbb_draw_deldel50_valid" in sb
    assert executable(block(S, "f$cc_river_delayed_3w_sbvbb_deldel_action")).strip() == "f$cc_river_delayed_3w_sbvbb_deldel50_parent"
    assert "f$cc_river_delayed_size_50_id" in block(S, "f$cc_river_delayed_3w_sbvbb_deldel_size_id")

    expected = {
        "f$cc_river_delayed_3w_btnvsb_negative_context": (4, 5),
        "f$cc_river_delayed_3w_bbvbtn_negative_context": (6, 4),
        "f$cc_river_delayed_3w_sbvbtn_negative_context": (5, 4),
    }
    for name, (hero, villain) in expected.items():
        b = block(S, name)
        assert "f$cc_deal_size = 3" in b and "f$cc_flop_entry_count = 2" in b
        assert f"f$cc_hero_pos_id = {hero}" in b
        assert f"f$cc_hu_villain_pos_id = {villain}" in b
    neg = block(S, "f$cc_river_delayed_native_negative_covered")
    for name in expected:
        assert name in neg


def router_contract() -> None:
    fam = block(R, "f$cc_river_delayed_family_id")
    for fid, owner in (
        (1, "f$cc_river_delayed_hubb_deldel_context"),
        (2, "f$cc_river_delayed_3w_bbvsb_source_covered"),
        (3, "f$cc_river_delayed_3w_sbvbb_deldel50_parent"),
        (4, "f$cc_river_delayed_native_negative_covered"),
    ):
        assert f"When {owner} Return {fid} Force" in fam
    assert "When Others Return false Force" in block(R, "f$cc_river_delayed_router")
    assert "When Others Return 0 Force" in block(R, "f$cc_river_delayed_size_id")
    assert "!f$cc_river_delayed_strategy_covered" in block(R, "f$cc_river_delayed_uncovered_context")
    owners = block(R, "f$cc_river_delayed_child_owner_count")
    assert owners.count("* 1") == 4


def no_generic_leak_contract() -> None:
    code = executable(C + "\n" + S + "\n" + R).lower()
    for forbidden in ("handpower", "random", "betmax", "rivermax", "stackoff", "raise_committed"):
        assert forbidden not in code, forbidden


if __name__ == "__main__":
    common_contract()
    hubb_contract()
    bbvsb_contract()
    sbvbb_and_negative_contract()
    router_contract()
    no_generic_leak_contract()
    print("PASS: Gate13 first native direct-source checkpoint")
