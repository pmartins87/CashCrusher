#!/usr/bin/env python3
"""Gate05C-F Turn Float coverage, provenance and fail-closed source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ROUTER = (SRC / "CashCrusher_Turn_Float.txt").read_text(encoding="utf-8")
COV = (SRC / "CashCrusher_Turn_Float_SourceCoverageRepair.txt").read_text(encoding="utf-8")
SRP = (SRC / "CashCrusher_Turn_Float_SRP_Gaps.txt").read_text(encoding="utf-8")
ISO = (SRC / "CashCrusher_Turn_Float_ISO.txt").read_text(encoding="utf-8")
THREE = (SRC / "CashCrusher_Turn_Float_3BP.txt").read_text(encoding="utf-8")
FOUR = (SRC / "CashCrusher_Turn_Float_4BP.txt").read_text(encoding="utf-8")
POLICY = (SRC / "CashCrusher_Turn_Float_PolicyCommon.txt").read_text(encoding="utf-8")
VALUE = (SRC / "CashCrusher_Turn_Float_ValueQuality.txt").read_text(encoding="utf-8")
TEXTS = (ROUTER, COV, SRP, ISO, THREE, FOUR, POLICY, VALUE)


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def router_contract() -> None:
    owners = [
        "f$cc_turn_float_source_exact_covered",
        "f$cc_turn_float_srp_gap_covered",
        "f$cc_turn_float_iso_gap_covered",
        "f$cc_turn_float_plain3bp_gap_covered",
        "f$cc_turn_float_squeeze_gap_covered",
        "f$cc_turn_float_4bp_gap_covered",
    ]
    family = block(ROUTER, "f$cc_turn_float_family_id")
    for idx, owner in enumerate(owners, start=1):
        assert f"When {owner} Return {idx} Force" in family

    router = block(ROUTER, "f$cc_turn_float_router")
    assert router.index("f$cc_turn_float_source_exact_locked_check") < router.index(
        "f$cc_turn_float_source_exact_positive"
    )
    for owner in owners[1:]:
        assert owner in router
    assert "When Others Return false Force" in router

    count = block(ROUTER, "f$cc_turn_float_family_owner_count")
    for owner in owners:
        assert owner in count
    exclusive = block(ROUTER, "f$cc_turn_float_family_exclusive")
    assert "f$cc_turn_float_family_owner_count = 1" in exclusive

    consistency = block(ROUTER, "f$cc_turn_float_size_consistent")
    assert "f$cc_turn_float_size_id = 0" in consistency
    assert "f$cc_turn_float_size_id >= 1 && f$cc_turn_float_size_id <= 5" in consistency

    uncovered = block(ROUTER, "f$cc_turn_float_uncovered_recognized")
    for owner in owners:
        assert f"!{owner}" in uncovered
    assert "f$cc_turn_float_5betplus_uncovered" in ROUTER


def source_precedence_contract() -> None:
    exact = block(COV, "f$cc_turn_float_source_exact_covered")
    # BB-v-SB direct source owns its no-made ACTION, not every made-hand context.
    assert "f$cc_turn_float_source_bbv_sb_action" in exact
    assert "f$cc_turn_float_source_bbv_sb_context" not in exact
    assert "f$cc_turn_float_source_btnadv_context" in exact
    assert "f$cc_turn_float_source_btnv_sb_nomade_lock" in exact

    for text in (SRP, ISO, THREE, FOUR):
        # Every strategic context file must visibly yield to exact source coverage.
        assert "!f$cc_turn_float_source_exact_covered" in text


def pot_family_contract() -> None:
    # SRP cannot steal ISO or HU-limp-raised states.
    for name in (
        "f$cc_turn_float_srp_parent1_hu_context",
        "f$cc_turn_float_srp_parent2_hu_context",
        "f$cc_turn_float_srp_parent3_hu_context",
        "f$cc_turn_float_srp_postmultiway_hu_context",
        "f$cc_turn_float_srp_multiway_context",
    ):
        b = block(SRP, name)
        assert "f$cc_pf_one_raise_ordinary_srp" in b

    truehu = block(ISO, "f$cc_turn_float_truehu_limpraised_parent1_context")
    assert "f$cc_true_hu" in truehu
    assert "f$cc_pf_hu_limp_raise_proven" in truehu
    assert "f$cc_hero_pos_id = 5" in truehu
    assert "f$cc_pf_rt_final_aggressor_pos_id = 6" in truehu

    isohu = block(ISO, "f$cc_turn_float_iso_parent1_hu_context")
    assert "f$cc_pf_iso_proven" in isohu
    assert "f$cc_turn_float_iso_hero_origin_consistent" in isohu

    plain1 = block(THREE, "f$cc_turn_float_plain3bp_parent1_hu_context")
    sq1 = block(THREE, "f$cc_turn_float_squeeze_parent1_hu_context")
    assert "f$cc_pf_rt_plain3bet_proven" in plain1
    assert "f$cc_pf_rt_squeeze_proven" in sq1

    fourcov = block(FOUR, "f$cc_turn_float_4bp_gap_covered")
    assert "multiway" not in fourcov.lower()
    unsupported4 = block(FOUR, "f$cc_turn_float_4bp_uncovered")
    assert "f$cc_pot_family_id = 4" in unsupported4


def history_selection_contract() -> None:
    assert "f$cc_turn_float_parent_id = 1" in block(SRP, "f$cc_turn_float_srp_parent1_hu_context")
    assert "f$cc_turn_float_parent_id = 2" in block(SRP, "f$cc_turn_float_srp_parent2_hu_context")
    assert "f$cc_turn_float_parent_id = 3" in block(SRP, "f$cc_turn_float_srp_parent3_hu_context")

    opener = block(THREE, "f$cc_turn_float_3bp_parent1_opener_origin")
    precold = block(THREE, "f$cc_turn_float_3bp_parent1_precold_origin")
    postcold = block(THREE, "f$cc_turn_float_3bp_parent1_postcold_origin")
    assert "f$cc_pf_rt_hero_is_opener_call_3bet" in opener
    assert "f$cc_pf_rt_hero_is_pre3bet_coldcaller" in precold
    assert "f$cc_pf_rt_hero_is_post3bet_coldcaller" in postcold


def multiway_and_stack_contract() -> None:
    for text, name in (
        (SRP, "f$cc_turn_float_srp_multiway_action"),
        (ISO, "f$cc_turn_float_iso_multiway_action"),
        (THREE, "f$cc_turn_float_3bp_multiway_action"),
    ):
        b = block(text, name)
        assert "f$cc_mw_spr_deepest_round_start" in b
        assert "nplayersplaying >= 4" in b
        assert "f$cc_real_combo_draw" in b
        assert "f$cc_turn_float_current_air Return false Force" in b

    # Low SPR is a condition inside exact branches, never an action by itself.
    for text in (SRP, ISO, THREE, FOUR):
        executable = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
        assert "BetMax" not in executable
        assert "Raise_Committed" not in executable
        assert "StackOffDraws" not in executable


def strategy_tail_contract() -> None:
    # P-heavy action functions must end fail-closed and never restore HandPower/random.
    for text in (SRP, ISO, THREE, FOUR):
        executable = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
        assert "HandPower" not in executable
        assert "random" not in executable.lower()

    action_names = [
        (SRP, "f$cc_turn_float_srp_parent1_hu_action"),
        (SRP, "f$cc_turn_float_srp_parent2_hu_action"),
        (SRP, "f$cc_turn_float_srp_parent3_hu_action"),
        (SRP, "f$cc_turn_float_srp_postmultiway_hu_action"),
        (SRP, "f$cc_turn_float_srp_multiway_action"),
        (ISO, "f$cc_turn_float_iso_parent1_limper_hu_action"),
        (ISO, "f$cc_turn_float_iso_parent1_coldcaller_hu_action"),
        (ISO, "f$cc_turn_float_truehu_limpraised_parent1_action"),
        (ISO, "f$cc_turn_float_iso_parent2_hu_action"),
        (ISO, "f$cc_turn_float_iso_parent3_hu_action"),
        (ISO, "f$cc_turn_float_iso_postmultiway_hu_action"),
        (ISO, "f$cc_turn_float_iso_multiway_action"),
        (THREE, "f$cc_turn_float_3bp_parent1_opener_hu_action"),
        (THREE, "f$cc_turn_float_3bp_parent1_coldcaller_hu_action"),
        (THREE, "f$cc_turn_float_3bp_parent2_hu_action"),
        (THREE, "f$cc_turn_float_3bp_parent3_hu_action"),
        (THREE, "f$cc_turn_float_3bp_postmultiway_hu_action"),
        (THREE, "f$cc_turn_float_3bp_multiway_action"),
        (FOUR, "f$cc_turn_float_4bp_parent1_hu_action"),
        (FOUR, "f$cc_turn_float_4bp_parent2_hu_action"),
        (FOUR, "f$cc_turn_float_4bp_parent3_hu_action"),
    ]
    for text, name in action_names:
        assert "When Others Return false Force" in block(text, name), name


if __name__ == "__main__":
    router_contract()
    source_precedence_contract()
    pot_family_contract()
    history_selection_contract()
    multiway_and_stack_contract()
    strategy_tail_contract()
    print("PASS: Gate05C-F Turn Float coverage/provenance/fail-closed contract")
