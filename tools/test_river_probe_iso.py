#!/usr/bin/env python3
"""Gate11H isolation-pot River Probe professional adaptation contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Probe_ISO.txt").read_text(encoding="utf-8")
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


def provenance_contract() -> None:
    hero_limp = block(POL, "f$cc_river_probe_iso_hero_was_limper")
    assert "f$cc_pf_pre_raise_limper_mask BitAnd f$cc_river_probe_iso_hero_pos_bit" in hero_limp
    hero_cold = block(POL, "f$cc_river_probe_iso_hero_was_postraise_coldcaller")
    assert "f$cc_pf_post_raise_coldcaller_mask BitAnd f$cc_river_probe_iso_hero_pos_bit" in hero_cold

    vill_limp = block(POL, "f$cc_river_probe_iso_villain_was_limper")
    assert "f$cc_pf_pre_raise_limper_mask BitAnd f$cc_river_probe_iso_villain_pos_bit" in vill_limp
    vill_cold = block(POL, "f$cc_river_probe_iso_villain_was_postraise_coldcaller")
    assert "f$cc_pf_post_raise_coldcaller_mask BitAnd f$cc_river_probe_iso_villain_pos_bit" in vill_cold

    for name in (
        "f$cc_river_probe_iso_hero_caller_origin_consistent",
        "f$cc_river_probe_iso_villain_caller_origin_consistent",
    ):
        b = block(POL, name)
        assert "Return false Force" in b
        assert "Return true Force" in b


def topology_contract() -> None:
    clean = block(POL, "f$cc_river_probe_iso_clean_hu_context")
    for token in (
        "f$cc_river_probe_hu_opportunity",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_iso_proven",
    ):
        assert token in clean

    caller = block(POL, "f$cc_river_probe_iso_caller_vs_isolator_context")
    assert "f$cc_pf_role_srp_caller" in caller
    assert "f$cc_river_probe_iso_hero_caller_origin_consistent" in caller
    assert "f$cc_hu_villain_pos_id = f$cc_pf_single_raiser_pos_id" in caller

    pfa = block(POL, "f$cc_river_probe_iso_pfa_vs_caller_stab_context")
    assert "f$cc_pf_role_pfa" in pfa
    assert "f$cc_pf_single_raiser_pos_id = f$cc_hero_pos_id" in pfa
    assert "f$cc_river_probe_iso_villain_caller_origin_consistent" in pfa
    assert "lastraised2 = headsupchair" in pfa

    fam = block(POL, "f$cc_river_probe_iso_family_id")
    for i in range(1, 5):
        assert f"Return {i} Force" in fam


def value_contract() -> None:
    flush = block(POL, "f$cc_river_probe_iso_strong_flush")
    assert "NumberOfUnknownSuitedOvercards <= 4" in flush
    straight = block(POL, "f$cc_river_probe_iso_strong_straight")
    assert "!HaveUnderStraight" in straight

    premium = block(POL, "f$cc_river_probe_iso_premium_value")
    for token in (
        "f$cc_river_probe_literal_nuts",
        "HaveQuads",
        "HaveFullHouse",
        "f$cc_river_probe_iso_strong_flush",
        "f$cc_river_probe_iso_strong_straight",
    ):
        assert token in premium

    medium = block(POL, "f$cc_river_probe_iso_medium_value")
    assert "HaveTrips && !TripsOnBoard && npcbits > 0" in medium
    assert "HaveSet" in medium
    assert "f$cc_river_probe_contributed_exact_two_pair" in medium

    tp = block(POL, "f$cc_river_probe_iso_strong_tp")
    assert "f$cc_number_better_kickers <= 2" in tp
    thin = block(POL, "f$cc_river_probe_iso_thin_value_river")
    assert "!f$cc_river_probe_paired" in thin
    assert "!f$cc_river_probe_completed" in thin


def bluff_contract() -> None:
    snap = block(POL, "f$cc_river_probe_iso_caller_snapshot_valid")
    assert "f$cc_river_probe_iso_caller_vs_isolator_context" in snap
    assert "f$cc_river_probe_snapshot_valid" in snap

    draw = block(POL, "f$cc_river_probe_iso_flop_frontdoor_draw_proven")
    for token in (
        "user_cc_turn_probe_flop_had_real_fd",
        "user_cc_turn_probe_flop_had_real_oesd",
        "user_cc_turn_probe_flop_had_real_gutshot",
    ):
        assert token in draw

    bluff = block(POL, "f$cc_river_probe_iso_limper_missed_draw_bluff")
    for token in (
        "f$cc_river_probe_iso_family_id = 1",
        "f$cc_river_probe_iso_late_isolator",
        "f$cc_river_probe_iso_flop_frontdoor_draw_proven",
        "f$cc_river_probe_air",
        "f$cc_river_probe_iso_good_bluff_river",
    ):
        assert token in bluff

    blocked = block(POL, "f$cc_river_probe_iso_air_bluff_blocked")
    assert "!f$cc_river_probe_iso_limper_missed_draw_bluff" in blocked

    # Only family 1 may contain a bluff trigger.
    for family in (2, 3, 4):
        code = executable(block(POL, f"f$cc_river_probe_iso_f{family}_action")).lower()
        assert "bluff" not in code
        assert "f$cc_river_probe_air" not in code


def action_size_contract() -> None:
    f1 = block(POL, "f$cc_river_probe_iso_f1_action")
    assert "f$cc_river_probe_iso_strong_tp && f$cc_river_probe_iso_thin_value_river && f$cc_river_probe_iso_late_isolator" in f1
    assert "f$cc_river_probe_iso_limper_missed_draw_bluff Return true Force" in f1

    f2 = block(POL, "f$cc_river_probe_iso_f2_action")
    assert "f$cc_river_probe_iso_overpair_real && f$cc_river_probe_iso_thin_value_river" in f2
    assert "f$cc_river_probe_iso_strong_tp" not in executable(f2)

    f3 = block(POL, "f$cc_river_probe_iso_f3_action")
    assert "f$cc_river_probe_iso_strong_tp && f$cc_river_probe_iso_thin_value_river" in f3

    f4 = block(POL, "f$cc_river_probe_iso_f4_action")
    assert "f$cc_river_probe_iso_overpair_real && f$cc_river_probe_iso_thin_value_river" in f4
    assert "f$cc_river_probe_iso_strong_tp" not in executable(f4)

    size = block(POL, "f$cc_river_probe_iso_size_for_action")
    assert "f$cc_river_probe_iso_premium_value Return f$cc_river_probe_size_75_id" in size
    assert "f$cc_river_probe_iso_medium_value Return f$cc_river_probe_size_50_id" in size
    assert "f$cc_river_probe_iso_overpair_real Return f$cc_river_probe_size_33_id" in size
    assert "f$cc_river_probe_iso_strong_tp Return f$cc_river_probe_size_33_id" in size
    assert "f$cc_river_probe_iso_limper_missed_draw_bluff Return f$cc_river_probe_size_50_id" in size

    cov = block(POL, "f$cc_river_probe_iso_covered")
    assert "f$cc_river_probe_iso_context" in cov
    unresolved = block(POL, "f$cc_river_probe_iso_unresolved")
    assert "f$cc_pf_iso_proven" in unresolved
    assert "!f$cc_river_probe_iso_covered" in unresolved


def router_and_safety_contract() -> None:
    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_iso_covered Return 6 Force" in fam
    assert fam.index("f$cc_river_probe_srp_gap_covered") < fam.index("f$cc_river_probe_iso_covered")

    action = block(ROUTER, "f$cc_river_probe_router")
    assert "f$cc_river_probe_iso_covered Return f$cc_river_probe_iso_action Force" in action
    size = block(ROUTER, "f$cc_river_probe_size_id")
    assert "f$cc_river_probe_iso_covered Return f$cc_river_probe_iso_size_id Force" in size
    covered = block(ROUTER, "f$cc_river_probe_strategy_covered")
    assert "f$cc_river_probe_iso_covered" in covered

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
        assert forbidden not in code, f"forbidden ISO River-Probe leak: {forbidden}"


if __name__ == "__main__":
    provenance_contract()
    topology_contract()
    value_contract()
    bluff_contract()
    action_size_contract()
    router_and_safety_contract()
    print("PASS: Gate11H isolation-pot River Probe adaptation")
