#!/usr/bin/env python3
"""Gate04/04R deterministic coverage/exclusivity/fail-closed source tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ROUTER = (SRC / "CashCrusher_Flop_Float.txt").read_text(encoding="utf-8")
COMMON = (SRC / "CashCrusher_Flop_Float_Common.txt").read_text(encoding="utf-8")
SOURCE = (SRC / "CashCrusher_Flop_Float_Source.txt").read_text(encoding="utf-8")
SRP = (SRC / "CashCrusher_Flop_Float_SRP_6Max.txt").read_text(encoding="utf-8")
ISO = (SRC / "CashCrusher_Flop_Float_ISO.txt").read_text(encoding="utf-8")
THREE = (SRC / "CashCrusher_Flop_Float_3BP.txt").read_text(encoding="utf-8")
REPAIR = (SRC / "CashCrusher_Flop_Float_3BP_CallerRepair.txt").read_text(encoding="utf-8")
FOUR = (SRC / "CashCrusher_Flop_Float_4BP.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def run_router_contract() -> None:
    router = block(ROUTER, "f$cc_flop_float_router")
    expected_order = [
        "f$cc_flop_float_source_covered",
        "f$cc_flop_float_srp_gap_covered",
        "f$cc_flop_float_iso_covered",
        "f$cc_flop_float_plain3bp_covered_final",
        "f$cc_flop_float_squeeze_covered_final",
        "f$cc_flop_float_4bp_covered",
    ]
    offsets = [router.index(x) for x in expected_order]
    assert offsets == sorted(offsets), "Float router family precedence changed"
    assert "When Others Return false Force" in router

    size = block(ROUTER, "f$cc_flop_float_size_id")
    for owner in expected_order:
        assert owner in size
    assert "When Others Return 0 Force" in size

    family = block(ROUTER, "f$cc_flop_float_family_id")
    for idx, owner in enumerate(expected_order, start=1):
        assert f"When {owner} Return {idx} Force" in family

    count = block(ROUTER, "f$cc_flop_float_family_owner_count")
    for owner in expected_order:
        assert owner in count

    exclusive = block(ROUTER, "f$cc_flop_float_family_exclusive")
    assert "f$cc_flop_float_family_owner_count = 1" in exclusive

    consistency = block(ROUTER, "f$cc_flop_float_size_consistent")
    assert "f$cc_flop_float_size_id = 0" in consistency
    assert "f$cc_flop_float_size_id >= 1 && f$cc_flop_float_size_id <= 5" in consistency

    combined_plain = block(ROUTER, "f$cc_flop_float_plain3bp_covered_final")
    assert "f$cc_flop_float_plain3bp_covered" in combined_plain
    assert "f$cc_flop_float_rt3bp_plain_covered" in combined_plain

    combined_squeeze = block(ROUTER, "f$cc_flop_float_squeeze_covered_final")
    assert "f$cc_flop_float_squeeze_covered" in combined_squeeze
    assert "f$cc_flop_float_rt3bp_squeeze_covered" in combined_squeeze


def run_fail_closed_contract() -> None:
    uncovered = block(ROUTER, "f$cc_flop_float_uncovered_recognized")
    assert "f$cc_pot_family_id >= 5" in uncovered
    assert "f$cc_flop_float_plain3bp_uncovered" in uncovered
    assert "f$cc_flop_float_squeeze_uncovered" in uncovered
    assert "f$cc_flop_float_4bp_uncovered" in uncovered

    # The canonical opportunity itself excludes MIDDLE and preflop aggressor roles.
    opp = block(COMMON, "f$cc_flop_float_opportunity")
    assert "f$cc_relpos_id != 3 Return false Force" in opp
    caller = block(COMMON, "f$cc_flop_float_caller_role")
    assert "f$cc_pf_role_pfa" not in caller
    assert "f$cc_pf_role_3bettor" not in caller
    assert "f$cc_pf_role_4bettor" not in caller

    # Ordinary SRP explicitly excludes ISO/true-HU-limp-raise through its parent.
    srp_hu = block(SRP, "f$cc_flop_float_srp_6max_hu_context")
    assert "f$cc_pf_one_raise_ordinary_srp" in srp_hu

    # Multi-handed ISO does not steal the true-HU HUSB source family.
    iso_hu = block(ISO, "f$cc_flop_float_iso_hu_context")
    assert "f$cc_hu_origin_preflop_reduced" in iso_hu
    assert "f$cc_pf_iso_proven" in iso_hu

    # Gate04R must use actual-final-aggressor chronology and still fail closed.
    repaired_plain = block(REPAIR, "f$cc_flop_float_rt3bp_plain_postcold_hu_context")
    assert "f$cc_pf_rt_plain3bet_proven" in repaired_plain
    assert "f$cc_pf_rt_hero_is_post3bet_coldcaller" in repaired_plain
    repaired_mw = block(REPAIR, "f$cc_flop_float_rt3bp_multiway_context")
    assert "f$cc_pf_rt_3bettor_live_opponent" in repaired_mw
    assert "f$cc_relpos_id = 3" in repaired_mw

    # 4BP coverage is exactly one clean caller chronology.
    covered4 = block(FOUR, "f$cc_flop_float_4bp_covered")
    assert "f$cc_flop_float_4bp_hu_context" in covered4
    assert "multiway" not in covered4.lower()


def run_strategy_no_broad_tail() -> None:
    # Every child action has an explicit false tail; this catches accidental
    # reintroduction of old generic HandPower/random coverage.
    action_names = [
        (SOURCE, "f$cc_flop_float_true_hu_husb_action"),
        (SOURCE, "f$cc_flop_float_bb_vs_sb_action"),
        (SRP, "f$cc_flop_float_srp_6max_hu_action"),
        (SRP, "f$cc_flop_float_srp_multiway_action"),
        (ISO, "f$cc_flop_float_iso_hu_limper_action"),
        (ISO, "f$cc_flop_float_iso_hu_coldcaller_action"),
        (ISO, "f$cc_flop_float_iso_multiway_action"),
        (THREE, "f$cc_flop_float_plain3bp_opener_hu_action"),
        (THREE, "f$cc_flop_float_plain3bp_postcold_hu_action"),
        (THREE, "f$cc_flop_float_squeeze_opener_hu_action"),
        (THREE, "f$cc_flop_float_squeeze_coldcaller_hu_action"),
        (THREE, "f$cc_flop_float_3bp_multiway_action"),
        (REPAIR, "f$cc_flop_float_rt3bp_plain_postcold_hu_action"),
        (REPAIR, "f$cc_flop_float_rt3bp_squeeze_coldcaller_hu_action"),
        (REPAIR, "f$cc_flop_float_rt3bp_multiway_action"),
        (FOUR, "f$cc_flop_float_4bp_hu_action"),
    ]
    for text, name in action_names:
        b = block(text, name)
        assert "When Others Return false Force" in b, f"missing fail-closed tail: {name}"
        assert "HandPower" not in b, f"generic HandPower leaked into {name}"

    # Initial strategy modules must not own explicit all-in execution.
    for text in (SOURCE, SRP, ISO, THREE, REPAIR, FOUR, ROUTER):
        executable = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
        assert "BetMax" not in executable
        assert "Allin" not in executable


if __name__ == "__main__":
    run_router_contract()
    run_fail_closed_contract()
    run_strategy_no_broad_tail()
    print("PASS: Gate04/04R Flop Float coverage/exclusivity/fail-closed contract")
