#!/usr/bin/env python3
"""Gate11J clean-HU 4BP River Probe adaptation contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Probe_4BP.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_River_Probe.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_River_Probe_History.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def topology_contract() -> None:
    clean = block(POL, "f$cc_river_probe_4bp_clean_hu_context")
    for token in (
        "f$cc_river_probe_hu_opportunity",
        "f$cc_flop_entry_count = 2",
        "f$cc_pot_family_id = 4",
    ):
        assert token in clean

    caller = block(POL, "f$cc_river_probe_4bp_caller_vs_opener4_context")
    for token in (
        "f$cc_pf_call4_opener4_vs_hero3bettor_proven",
        "f$cc_hu_call4_vs_opener4_context",
        "f$cc_hu_villain_pos_id = f$cc_pf_call4_other_raiser_pos_id",
    ):
        assert token in caller

    hero4 = block(POL, "f$cc_river_probe_4bp_hero4_vs_proven_caller_context")
    for token in (
        "f$cc_pf_role_4bettor",
        "f$cc_pf_4bet_subtype_id > 0",
        "f$cc_hu_4bp_survivor_consistent",
        "f$cc_hu_4bp_survivor_type_id >= 1",
        "f$cc_hu_4bp_survivor_type_id <= 2",
    ):
        assert token in hero4

    topo = block(POL, "f$cc_river_probe_4bp_topology_id")
    assert "f$cc_river_probe_4bp_caller_vs_opener4_context Return 1 Force" in topo
    assert "f$cc_river_probe_4bp_opener4_vs_threebettor_context Return 2 Force" in topo
    assert "f$cc_river_probe_4bp_cold4_vs_opener_context Return 3 Force" in topo
    assert "f$cc_river_probe_4bp_cold4_vs_threebettor_context Return 4 Force" in topo

    # Gate11 parent must still prove the actual flop X/C actor and Turn X/X.
    hu = block(HIST, "f$cc_river_probe_hu_opportunity")
    assert "headsupchair = lastraised2" in hu
    base = block(HIST, "f$cc_river_probe_base_opportunity")
    assert "f$cc_hist_river_probe_flop_checkcall_clean" in base
    assert "f$cc_hist_river_probe_turn_checkthrough_clean" in base


def value_contract() -> None:
    flush = block(POL, "f$cc_river_probe_4bp_strong_flush")
    assert "pokerval > pokervalcommon" in flush
    assert "NumberOfUnknownSuitedOvercards <= 4" in flush

    straight = block(POL, "f$cc_river_probe_4bp_strong_straight")
    assert "pokerval > pokervalcommon" in straight
    assert "!HaveUnderStraight" in straight

    premium = block(POL, "f$cc_river_probe_4bp_premium_value")
    for token in (
        "f$cc_river_probe_literal_nuts",
        "HaveQuads",
        "HaveFullHouse",
        "f$cc_river_probe_4bp_strong_flush",
        "f$cc_river_probe_4bp_strong_straight",
    ):
        assert token in premium

    medium = block(POL, "f$cc_river_probe_4bp_medium_value")
    assert "HaveTrips && !TripsOnBoard && npcbits > 0" in medium
    assert "HaveSet" in medium
    assert "f$cc_river_probe_contributed_exact_two_pair" in medium

    overpair = block(POL, "f$cc_river_probe_4bp_overpair_real")
    assert "HaveOverPair && PairInHand && npcbits > 0" in overpair

    thin = block(POL, "f$cc_river_probe_4bp_thin_value_river")
    assert "!f$cc_river_probe_paired" in thin
    assert "!f$cc_river_probe_completed" in thin


def action_contract() -> None:
    action = block(POL, "f$cc_river_probe_4bp_action")
    assert "f$cc_river_probe_4bp_premium_value Return true Force" in action
    assert "f$cc_river_probe_4bp_medium_value Return true Force" in action
    assert "f$cc_river_probe_4bp_overpair_real && f$cc_river_probe_4bp_thin_value_river Return true Force" in action
    assert "strong_tp" not in executable(action).lower()
    assert "air" not in executable(action).lower()

    size = block(POL, "f$cc_river_probe_4bp_size_id")
    assert "f$cc_river_probe_4bp_premium_value Return f$cc_river_probe_size_75_id" in size
    assert "f$cc_river_probe_4bp_medium_value Return f$cc_river_probe_size_50_id" in size
    assert "f$cc_river_probe_4bp_overpair_real Return f$cc_river_probe_size_33_id" in size

    tpcheck = block(POL, "f$cc_river_probe_4bp_top_pair_check")
    assert "f$cc_hand_just_top_pair" in tpcheck
    aircheck = block(POL, "f$cc_river_probe_4bp_air_check")
    assert "f$cc_river_probe_air" in aircheck

    covered = block(POL, "f$cc_river_probe_4bp_covered")
    assert "f$cc_river_probe_4bp_context" in covered

    unresolved = block(POL, "f$cc_river_probe_4bp_unresolved")
    assert "f$cc_pot_family_id = 4" in unresolved
    assert "!f$cc_river_probe_4bp_covered" in unresolved
    five = block(POL, "f$cc_river_probe_5betplus_unresolved")
    assert "f$cc_pot_family_id = 5" in five


def router_contract() -> None:
    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_4bp_covered Return 8 Force" in fam
    action = block(ROUTER, "f$cc_river_probe_router")
    assert "f$cc_river_probe_4bp_covered Return f$cc_river_probe_4bp_action Force" in action
    size = block(ROUTER, "f$cc_river_probe_size_id")
    assert "f$cc_river_probe_4bp_covered Return f$cc_river_probe_4bp_size_id Force" in size
    cov = block(ROUTER, "f$cc_river_probe_strategy_covered")
    assert "f$cc_river_probe_4bp_covered" in cov

    # Direct/native families and earlier audited P families keep priority.
    assert fam.index("f$cc_river_probe_3w_source_covered") < fam.index("f$cc_river_probe_4bp_covered")
    assert fam.index("f$cc_river_probe_3bp_covered") < fam.index("f$cc_river_probe_4bp_covered")


def safety_contract() -> None:
    consistency = block(POL, "f$cc_river_probe_4bp_size_consistent")
    assert "f$cc_river_probe_4bp_size_id = 0" in consistency
    assert "f$cc_river_probe_4bp_size_id >= 1 && f$cc_river_probe_4bp_size_id <= 7" in consistency

    code = executable(POL).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "stackoff",
        "shorteststack",
        "effectivestack_bkp",
        "user_faced_lowbet",
    ):
        assert forbidden not in code, f"forbidden 4BP River-Probe leak: {forbidden}"


if __name__ == "__main__":
    topology_contract()
    value_contract()
    action_contract()
    router_contract()
    safety_contract()
    print("PASS: Gate11J clean-HU 4BP River Probe adaptation")
