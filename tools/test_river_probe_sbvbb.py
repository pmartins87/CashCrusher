#!/usr/bin/env python3
"""Gate11E native 3wSBvBB River Probe source/provenance contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = (ROOT / "src" / "CashCrusher_River_Probe_History.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_River_Probe_SBVBB.txt").read_text(encoding="utf-8")
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


def corrected_owner_contract() -> None:
    base = executable(block(HIST, "f$cc_river_probe_base_opportunity"))
    assert "f$cc_river_probe_preflop_context_supported" in base
    assert "preflop_noinitiative" not in base
    assert "excluded_delayed_cbet" not in base
    assert "f$cc_pf_role_pfa" not in base

    allowed = block(HIST, "f$cc_river_probe_preflop_aggressor_history_allowed")
    assert "f$cc_pf_role_pfa" in allowed
    assert "f$cc_pf_role_3bettor" in allowed
    assert "f$cc_pf_role_4bettor" in allowed


def topology_and_origin_contract() -> None:
    common = block(POL, "f$cc_river_probe_sbvbb_common_context")
    for token in (
        "f$cc_river_probe_hu_opportunity",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 2",
        "f$cc_hu_origin_preflop_reduced",
        "f$cc_hero_pos_id = 5",
        "f$cc_hu_villain_pos_id = 6",
        "headsupchair = bigblindchair",
        "lastraised2 = bigblindchair",
    ):
        assert token in common

    limp = block(POL, "f$cc_river_probe_sbvbb_limped_origin")
    for token in (
        "f$cc_pot_family_id = 1",
        "f$cc_pf_raise_count = 0",
        "f$cc_pf_role_unraised_caller",
        "f$cc_pf_call_sb",
    ):
        assert token in limp

    mnr = block(POL, "f$cc_river_probe_sbvbb_mnr_origin")
    for token in (
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_pfa",
        "f$cc_pf_single_raiser_pos_id = 5",
        "f$cc_pf_call_bb",
    ):
        assert token in mnr

    count = block(POL, "f$cc_river_probe_sbvbb_origin_count")
    assert "f$cc_river_probe_sbvbb_limped_origin" in count
    assert "f$cc_river_probe_sbvbb_mnr_origin" in count
    assert "= 1" in block(POL, "f$cc_river_probe_sbvbb_context")


def price_provenance_contract() -> None:
    for name, marker in (
        ("f$cc_river_probe_sbvbb_limped_mpbp_call_proven", "user_cc_flop_sbvbb_limped_mpbp_called_le100"),
        ("f$cc_river_probe_sbvbb_mnr_mpbp_le50_call_proven", "user_cc_flop_sbvbb_mnr_mpbp_called_le50"),
        ("f$cc_river_probe_sbvbb_mnr_mpbp_bdfd_le75_call_proven", "user_cc_flop_sbvbb_mnr_mpbp_bdfd_called_le75"),
        ("f$cc_river_probe_sbvbb_mnr_medium_draw_call_proven", "user_cc_flop_sbvbb_mnr_medium_draw_called_le100"),
        ("f$cc_river_probe_sbvbb_mnr_weak_draw_call_proven", "user_cc_flop_sbvbb_mnr_weak_draw_called_le33"),
    ):
        assert marker in block(POL, name)

    limp_draw = block(POL, "f$cc_river_probe_sbvbb_limped_draw_call_proven")
    assert "user_cc_flop_sbvbb_limped_medweak_draw_called_le50" in limp_draw
    assert "user_cc_turn_probe_flop_was_9low" in limp_draw

    mp_count = block(POL, "f$cc_river_probe_sbvbb_mpbp_marker_count")
    assert "f$cc_river_probe_sbvbb_limped_mpbp_call_proven" in mp_count
    assert "f$cc_river_probe_sbvbb_mnr_mpbp_le50_call_proven" in mp_count
    assert "f$cc_river_probe_sbvbb_mnr_mpbp_bdfd_le75_call_proven" in mp_count

    mp_parent = block(POL, "f$cc_river_probe_sbvbb_mpbp_parent_proven")
    assert "f$cc_river_probe_sbvbb_mpbp_marker_count != 1 Return false Force" in mp_parent
    assert "f$cc_river_probe_sbvbb_limped_origin" in mp_parent
    assert "f$cc_river_probe_sbvbb_mnr_origin" in mp_parent

    dr_parent = block(POL, "f$cc_river_probe_sbvbb_draw_parent_proven")
    assert "f$cc_river_probe_sbvbb_draw_marker_count != 1 Return false Force" in dr_parent

    pending = block(POL, "f$cc_river_probe_sbvbb_defense_provenance_pending")
    assert "!f$cc_river_probe_sbvbb_source_parent" in pending


def source_action_contract() -> None:
    pending = block(POL, "f$cc_river_probe_sbvbb_straightflush_translation_pending")
    assert "f$cc_river_probe_3w_current_straightflush_pending" in pending

    strong = block(POL, "f$cc_river_probe_sbvbb_strong100")
    assert "f$cc_river_probe_3w_strong_safe" in strong
    two = block(POL, "f$cc_river_probe_sbvbb_exact2p75")
    assert "f$cc_river_probe_contributed_exact_two_pair" in two
    tpop = block(POL, "f$cc_river_probe_sbvbb_tpop50")
    assert "f$cc_river_probe_3w_tp_or_op_real" in tpop

    second = block(POL, "f$cc_river_probe_sbvbb_mpbp_secondpair25")
    assert "f$cc_river_probe_sbvbb_mpbp_parent_proven" in second
    assert "f$cc_hand_second_pair_or_pocket" in second

    air = block(POL, "f$cc_river_probe_sbvbb_draw_air50")
    assert "f$cc_river_probe_sbvbb_draw_parent_proven" in air
    assert "f$cc_river_probe_air" in air

    mp_check = block(POL, "f$cc_river_probe_sbvbb_mpbp_residual_check")
    assert "!f$cc_river_probe_sbvbb_straightflush_translation_pending" in mp_check
    dr_check = block(POL, "f$cc_river_probe_sbvbb_draw_residual_check")
    assert "!f$cc_river_probe_sbvbb_straightflush_translation_pending" in dr_check

    action = block(POL, "f$cc_river_probe_sbvbb_action")
    assert "f$cc_river_probe_sbvbb_mpbp_residual_check Return false Force" in action
    assert "f$cc_river_probe_sbvbb_draw_residual_check Return false Force" in action

    size = block(POL, "f$cc_river_probe_sbvbb_size_id")
    for token in (
        "f$cc_river_probe_sbvbb_strong100 Return f$cc_river_probe_size_100_id",
        "f$cc_river_probe_sbvbb_exact2p75 Return f$cc_river_probe_size_75_id",
        "f$cc_river_probe_sbvbb_tpop50 Return f$cc_river_probe_size_50_id",
        "f$cc_river_probe_sbvbb_mpbp_secondpair25 Return f$cc_river_probe_size_25_id",
        "f$cc_river_probe_sbvbb_draw_air50 Return f$cc_river_probe_size_50_id",
    ):
        assert token in size


def router_and_safety_contract() -> None:
    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_sbvbb_covered Return 3 Force" in fam
    action = block(ROUTER, "f$cc_river_probe_router")
    assert "f$cc_river_probe_sbvbb_covered Return f$cc_river_probe_sbvbb_action Force" in action
    size = block(ROUTER, "f$cc_river_probe_size_id")
    assert "f$cc_river_probe_sbvbb_covered Return f$cc_river_probe_sbvbb_size_id Force" in size
    coverage = block(ROUTER, "f$cc_river_probe_strategy_covered")
    assert "f$cc_river_probe_sbvbb_covered" in coverage

    code = executable(POL).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "f$game_",
        "f$cf7_",
        "effectivestack_bkp",
        "amounttocall",  # River module may consume proven price markers only.
        "potcommon",
    ):
        assert forbidden not in code, f"forbidden SBvBB River Probe leak: {forbidden}"

    consistent = block(POL, "f$cc_river_probe_sbvbb_size_consistent")
    assert "f$cc_river_probe_sbvbb_size_id = 0" in consistent
    assert "f$cc_river_probe_sbvbb_size_id <= 7" in consistent


if __name__ == "__main__":
    corrected_owner_contract()
    topology_and_origin_contract()
    price_provenance_contract()
    source_action_contract()
    router_and_safety_contract()
    print("PASS: Gate11E native 3wSBvBB River Probe source/provenance contract")
