#!/usr/bin/env python3
"""Gate11G ordinary-SRP 4-6h River Probe adaptation contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Probe_SRP_Gaps.txt").read_text(encoding="utf-8")
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
    common = block(POL, "f$cc_river_probe_srp_4to6_clean_hu_context")
    for token in (
        "f$cc_river_probe_hu_opportunity",
        "f$cc_deal_size >= 4 && f$cc_deal_size <= 6",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
    ):
        assert token in common

    caller = block(POL, "f$cc_river_probe_srp_caller_vs_pfa_context")
    for token in (
        "f$cc_pf_role_srp_caller",
        "f$cc_hero_pos_id = 5 || f$cc_hero_pos_id = 6",
        "f$cc_hu_villain_pos_id = f$cc_pf_single_raiser_pos_id",
        "f$cc_river_probe_srp_flop_aggressor_is_pfa",
    ):
        assert token in caller

    pfa = block(POL, "f$cc_river_probe_srp_pfa_vs_stab_context")
    for token in (
        "f$cc_pf_role_pfa",
        "f$cc_pf_single_raiser_pos_id = f$cc_hero_pos_id",
        "lastraised2 = headsupchair",
        "!f$cc_river_probe_srp_flop_aggressor_is_pfa",
    ):
        assert token in pfa

    # Gate11A.1 must allow a source child to own PFA-vs-stab after actual flop X/C.
    base = executable(block(HIST, "f$cc_river_probe_base_opportunity")).lower()
    assert "f$cc_pf_role_pfa return false" not in base
    assert "f$cc_river_probe_preflop_context_supported" in base


def range_partition_contract() -> None:
    band = block(POL, "f$cc_river_probe_srp_caller_opener_band_id")
    assert "f$cc_pf_single_raiser_pos_id = 4 Return 1 Force" in band
    assert "f$cc_pf_single_raiser_pos_id = 3 Return 2 Force" in band
    assert "f$cc_pf_single_raiser_pos_id = 1 || f$cc_pf_single_raiser_pos_id = 2 Return 3 Force" in band

    fam = block(POL, "f$cc_river_probe_srp_pfa_family_id")
    assert "f$cc_hero_pos_id = 5 && f$cc_hu_villain_pos_id = 6 Return 1 Force" in fam
    assert "f$cc_hero_pos_id >= 1 && f$cc_hero_pos_id <= 3 Return 2 Force" in fam


def value_contract() -> None:
    flush = block(POL, "f$cc_river_probe_srp_strong_flush")
    assert "pokerval > pokervalcommon" in flush
    assert "NumberOfUnknownSuitedOvercards <= 4" in flush

    straight = block(POL, "f$cc_river_probe_srp_strong_straight")
    assert "pokerval > pokervalcommon" in straight
    assert "!HaveUnderStraight" in straight

    premium = block(POL, "f$cc_river_probe_srp_premium_value")
    for token in (
        "HaveNuts",
        "HaveQuads",
        "HaveFullHouse",
        "f$cc_river_probe_srp_strong_flush",
        "f$cc_river_probe_srp_strong_straight",
    ):
        assert token in premium

    medium = block(POL, "f$cc_river_probe_srp_medium_value")
    assert "HaveTrips && !TripsOnBoard && npcbits > 0" in medium
    assert "HaveSet" in medium
    assert "f$cc_river_probe_contributed_exact_two_pair" in medium

    tp = block(POL, "f$cc_river_probe_srp_strong_tp")
    assert "f$cc_number_better_kickers <= 2" in tp
    assert "npcbits > 0" in tp

    thin = block(POL, "f$cc_river_probe_srp_thin_value_river")
    assert "!f$cc_river_probe_paired" in thin
    assert "!f$cc_river_probe_completed" in thin


def bluff_provenance_contract() -> None:
    snap = block(POL, "f$cc_river_probe_srp_caller_snapshot_valid")
    assert "f$cc_river_probe_srp_caller_vs_pfa_context" in snap
    assert "f$cc_river_probe_snapshot_valid" in snap

    draw = block(POL, "f$cc_river_probe_srp_flop_frontdoor_draw_proven")
    for token in (
        "user_cc_turn_probe_flop_had_real_fd",
        "user_cc_turn_probe_flop_had_real_oesd",
        "user_cc_turn_probe_flop_had_real_gutshot",
    ):
        assert token in draw

    good = block(POL, "f$cc_river_probe_srp_good_bluff_river")
    assert "!f$cc_river_probe_bad_to_bluff_board" in good
    assert "!f$cc_river_probe_completed" in good

    bluff = block(POL, "f$cc_river_probe_srp_btn_missed_draw_bluff")
    assert "f$cc_river_probe_srp_caller_opener_band_id = 1" in bluff
    assert "f$cc_river_probe_srp_flop_frontdoor_draw_proven" in bluff
    assert "f$cc_river_probe_air" in bluff
    assert "f$cc_river_probe_srp_good_bluff_river" in bluff

    missing = block(POL, "f$cc_river_probe_srp_pfa_bluff_provenance_missing")
    assert "f$cc_river_probe_srp_pfa_vs_stab_context" in missing
    assert "f$cc_river_probe_air" in missing

    # PFA-vs-stab action is value-only until its own call-time snapshot exists.
    pfa_action = executable(block(POL, "f$cc_river_probe_srp_pfa_action"))
    assert "bluff" not in pfa_action.lower()
    assert "f$cc_river_probe_air" not in pfa_action


def action_size_contract() -> None:
    caller = block(POL, "f$cc_river_probe_srp_caller_action")
    assert "f$cc_river_probe_srp_premium_value Return true Force" in caller
    assert "f$cc_river_probe_srp_medium_value Return true Force" in caller
    assert "f$cc_river_probe_srp_overpair_real && f$cc_river_probe_srp_thin_value_river Return true Force" in caller
    assert "f$cc_river_probe_srp_caller_opener_band_id = 1 && f$cc_river_probe_srp_strong_tp" in caller
    assert "f$cc_river_probe_srp_btn_missed_draw_bluff Return true Force" in caller

    csize = block(POL, "f$cc_river_probe_srp_caller_size_id")
    assert "f$cc_river_probe_srp_premium_value Return f$cc_river_probe_size_75_id" in csize
    assert "f$cc_river_probe_srp_medium_value Return f$cc_river_probe_size_50_id" in csize
    assert "f$cc_river_probe_srp_overpair_real Return f$cc_river_probe_size_33_id" in csize
    assert "f$cc_river_probe_srp_strong_tp Return f$cc_river_probe_size_33_id" in csize
    assert "f$cc_river_probe_srp_btn_missed_draw_bluff Return f$cc_river_probe_size_50_id" in csize

    psize = block(POL, "f$cc_river_probe_srp_pfa_size_id")
    assert "f$cc_river_probe_srp_premium_value Return f$cc_river_probe_size_75_id" in psize
    assert "f$cc_river_probe_srp_medium_value Return f$cc_river_probe_size_50_id" in psize
    assert "f$cc_river_probe_srp_overpair_real Return f$cc_river_probe_size_33_id" in psize
    assert "f$cc_river_probe_srp_strong_tp Return f$cc_river_probe_size_33_id" in psize

    covered = block(POL, "f$cc_river_probe_srp_gap_covered")
    assert "f$cc_river_probe_srp_gap_context" in covered

    consistency = block(POL, "f$cc_river_probe_srp_gap_size_consistent")
    assert "f$cc_river_probe_srp_gap_size_id = 0" in consistency
    assert "f$cc_river_probe_srp_gap_size_id >= 1 && f$cc_river_probe_srp_gap_size_id <= 7" in consistency


def router_and_safety_contract() -> None:
    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_srp_gap_covered Return 5 Force" in fam
    # Direct source descendants must retain precedence over the professional fill.
    assert fam.index("f$cc_river_probe_3w_source_covered") < fam.index("f$cc_river_probe_srp_gap_covered")

    action = block(ROUTER, "f$cc_river_probe_router")
    assert "f$cc_river_probe_srp_gap_covered Return f$cc_river_probe_srp_gap_action Force" in action
    size = block(ROUTER, "f$cc_river_probe_size_id")
    assert "f$cc_river_probe_srp_gap_covered Return f$cc_river_probe_srp_gap_size_id Force" in size
    cov = block(ROUTER, "f$cc_river_probe_strategy_covered")
    assert "f$cc_river_probe_srp_gap_covered" in cov

    code = executable(POL).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "stackoff",
        "effectivestack_bkp",
        "shorteststack",
        "user_faced_lowbet",
    ):
        assert forbidden not in code, f"forbidden SRP River-Probe leak: {forbidden}"


if __name__ == "__main__":
    topology_contract()
    range_partition_contract()
    value_contract()
    bluff_provenance_contract()
    action_size_contract()
    router_and_safety_contract()
    print("PASS: Gate11G ordinary-SRP 4-6h River Probe adaptation")
