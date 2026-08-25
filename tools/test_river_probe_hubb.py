#!/usr/bin/env python3
"""Gate11C true-HU BB River Probe direct-source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = (ROOT / "src" / "CashCrusher_River_Probe_History.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_River_Probe_Common.txt").read_text(encoding="utf-8")
HUBB = (ROOT / "src" / "CashCrusher_River_Probe_HUBB.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_River_Probe.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def ancestry_contract() -> None:
    srp = block(HUBB, "f$cc_river_probe_hubb_truehu_srp_context")
    for token in (
        "f$cc_river_probe_hu_opportunity",
        "f$cc_true_hu",
        "f$cc_flop_entry_count = 2",
        "f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = 5",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_single_raiser_pos_id = 5",
        "lastraised2 = smallblindchair",
    ):
        assert token in srp

    limp = block(HUBB, "f$cc_river_probe_hubb_truehu_limped_context")
    for token in (
        "f$cc_true_hu",
        "f$cc_pot_family_id = 1",
        "f$cc_pf_raise_count = 0",
        "f$cc_pf_role_bb_check",
        "f$cc_pf_call_sb",
        "lastraised2 = smallblindchair",
    ):
        assert token in limp

    context = executable(block(HUBB, "f$cc_river_probe_hubb_context"))
    assert "reduced" not in context.lower()
    assert "f$cc_river_probe_hubb_truehu_srp_context" in context
    assert "f$cc_river_probe_hubb_truehu_limped_context" in context


def hand_translation_contract() -> None:
    tp = block(HUBB, "f$cc_river_probe_hubb_top_pair_real")
    assert "f$cc_hand_just_top_pair" in tp
    assert "!TwoPairOnBoard" in tp
    assert "npcbits > 0" in tp

    op = block(HUBB, "f$cc_river_probe_hubb_overpair_real")
    assert "HaveOverPair" in op
    assert "PairInHand" in op

    strong = block(HUBB, "f$cc_river_probe_hubb_tripsplus_safe")
    assert "f$cc_river_probe_literal_nuts" in strong
    assert "HaveQuads" in strong
    assert "HaveFullHouse" in strong
    assert "HaveTrips && !TripsOnBoard" in strong
    # Non-nut straight/flush must not be generically promoted to pot.
    code = executable(strong)
    assert "HaveFlush" not in code
    assert "HaveStraight" not in code

    weak = block(HUBB, "f$cc_river_probe_hubb_weak_pair_check")
    assert "f$cc_hand_fourth_pair_or_pocket" in weak
    assert "f$cc_hand_fifth_pair_or_pocket" in weak
    assert "HaveUnderPair" in weak
    assert "f$cc_hand_third_pair_or_pocket" not in weak


def source_action_contract() -> None:
    two = block(HUBB, "f$cc_river_probe_hubb_exact2p_action")
    assert "f$cc_river_probe_contributed_exact_two_pair" in two
    assert "f$cc_river_probe_completed Return true Force" in two
    assert "When Others Return false Force" in two

    tpop = block(HUBB, "f$cc_river_probe_hubb_tpop_action")
    assert "f$cc_river_probe_hubb_tp_or_op_real" in tpop
    assert "f$cc_river_probe_completed Return true Force" in tpop
    assert "When Others Return false Force" in tpop

    second = block(HUBB, "f$cc_river_probe_hubb_secondpair_action")
    assert "f$cc_river_probe_hubb_second_pair" in second

    air = block(HUBB, "f$cc_river_probe_hubb_air_action")
    assert "f$cc_river_probe_air" in air

    size = block(HUBB, "f$cc_river_probe_hubb_size_id")
    for token in (
        "f$cc_river_probe_size_100_id",
        "f$cc_river_probe_size_75_id",
        "f$cc_river_probe_size_25_id",
        "f$cc_river_probe_size_50_id",
    ):
        assert token in size
    assert "f$cc_river_probe_hubb_exact2p_action Return f$cc_river_probe_size_75_id" in size
    assert "f$cc_river_probe_hubb_tpop_action Return f$cc_river_probe_size_25_id" in size
    assert "f$cc_river_probe_hubb_air_action Return f$cc_river_probe_size_75_id" in size

    cov = block(HUBB, "f$cc_river_probe_hubb_covered")
    assert "f$cc_river_probe_hubb_exact2p_covered" in cov
    assert "f$cc_river_probe_hubb_tpop_covered" in cov
    assert "f$cc_river_probe_hubb_weakpair_covered" in cov


def gap_and_router_contract() -> None:
    third = block(HUBB, "f$cc_river_probe_hubb_thirdpair_translation_pending")
    assert "f$cc_hand_third_pair_or_pocket" in third
    sf = block(HUBB, "f$cc_river_probe_hubb_straightflush_translation_pending")
    assert "HaveFlush" in sf and "HaveStraight" in sf
    assert "!f$cc_river_probe_literal_nuts" in sf

    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_hubb_covered Return 2 Force" in fam
    action = block(ROUTER, "f$cc_river_probe_router")
    assert "f$cc_river_probe_hubb_covered Return f$cc_river_probe_hubb_action Force" in action
    size = block(ROUTER, "f$cc_river_probe_size_id")
    assert "f$cc_river_probe_hubb_covered Return f$cc_river_probe_hubb_size_id Force" in size


def safety_contract() -> None:
    # Closed X/C-X/X must still be the universal parent.
    assert "didcallround2 != 1" in block(HIST, "f$cc_hist_river_probe_flop_checkcall_clean")
    assert "raisbits3 = 0" in block(HIST, "f$cc_hist_river_probe_no_turn_aggressor")
    assert "f$cc_river_probe_completed" in COMMON

    code = executable(HUBB).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "stackoff",
        "effectivestack_bkp",
        "numberofbetterkickers",
        "1hc_flush",
        "onecardunderstraight",
    ):
        assert forbidden not in code, f"forbidden/untranslated HUBB leak: {forbidden}"

    consistency = block(HUBB, "f$cc_river_probe_hubb_size_consistent")
    assert "f$cc_river_probe_hubb_size_id = 0" in consistency


if __name__ == "__main__":
    ancestry_contract()
    hand_translation_contract()
    source_action_contract()
    gap_and_router_contract()
    safety_contract()
    print("PASS: Gate11C true-HU HUBB River Probe source contract")
