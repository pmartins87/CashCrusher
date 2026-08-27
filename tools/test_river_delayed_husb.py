#!/usr/bin/env python3
"""Gate13D newest-source true-HU HUSB River BxB100 contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = (ROOT / "src" / "CashCrusher_River_Delayed_HUSB_Source.txt").read_text(encoding="utf-8")
R = (ROOT / "src" / "CashCrusher_River_Delayed.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text.split(marker, 1)[1]
    return tail.split("##", 1)[0]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def context_contract() -> None:
    ctx = block(S, "f$cc_river_delayed_husb_cbet_turncheck_context")
    for token in (
        "f$cc_river_delayed_base_opportunity",
        "f$cc_true_hu",
        "f$cc_hu",
        "f$cc_hero_pos_id = 5",
        "f$cc_hu_villain_pos_id = 6",
        "f$cc_pot_family_id >= 1",
        "f$cc_pot_family_id <= 2",
        "f$cc_river_delayed_after_standard_turncheck_valid",
        "f$cc_hist_flop_initial_cbet_executed",
        "f$cc_hist_flop_cbet_snapshot_consistent",
        "!f$cc_hist_flop_cbet_runtime_mismatch",
    ):
        assert token in ctx, token


def lineage_contract() -> None:
    lineage = block(S, "f$cc_river_delayed_husb_flop_air_bxb_lineage")
    assert "user_cc_flop_cbet_had_no_made" in lineage
    for draw in (
        "user_cc_flop_cbet_had_premium_draw",
        "user_cc_flop_cbet_had_good_draw",
        "user_cc_flop_cbet_had_weak_draw",
    ):
        assert f"!{draw}" in lineage

    action = executable(block(S, "f$cc_river_delayed_husb_air_bxb100_action"))
    assert "f$cc_river_delayed_husb_flop_air_bxb_lineage" in action
    assert "f$cc_river_delayed_no_made" in action

    size = block(S, "f$cc_river_delayed_husb_air_bxb100_size_id")
    assert "Return f$cc_river_delayed_size_100_id Force" in size
    assert "When Others Return 0 Force" in size

    covered = executable(block(S, "f$cc_river_delayed_husb_source_covered")).strip()
    assert covered == "f$cc_river_delayed_husb_air_bxb100_action"
    pending = block(S, "f$cc_river_delayed_husb_source_pending")
    assert "f$cc_river_delayed_husb_cbet_turncheck_context" in pending
    assert "!f$cc_river_delayed_husb_source_covered" in pending


def router_contract() -> None:
    fam = block(R, "f$cc_river_delayed_family_id")
    assert "When f$cc_river_delayed_husb_source_covered Return 5 Force" in fam

    action = block(R, "f$cc_river_delayed_router")
    native_i = action.index("f$cc_river_delayed_native_source_covered")
    husb_i = action.index("f$cc_river_delayed_husb_source_covered")
    assert native_i < husb_i
    assert "Return f$cc_river_delayed_husb_air_bxb100_action Force" in action

    size = block(R, "f$cc_river_delayed_size_id")
    assert "When f$cc_river_delayed_husb_source_covered Return f$cc_river_delayed_husb_air_bxb100_size_id Force" in size
    coverage = block(R, "f$cc_river_delayed_strategy_covered")
    assert "f$cc_river_delayed_native_source_covered" in coverage
    assert "f$cc_river_delayed_husb_source_covered" in coverage
    owners = block(R, "f$cc_river_delayed_child_owner_count")
    assert owners.count("* 1") == 5
    assert "f$cc_river_delayed_husb_source_covered" in owners
    consistent = block(R, "f$cc_river_delayed_router_consistent")
    assert "!f$cc_river_delayed_husb_source_size_consistent Return false Force" in consistent


def no_unsafe_generalization() -> None:
    code = executable(S + "\n" + R).lower()
    for forbidden in ("handpower", "random", "betmax", "rivermax", "stackoff", "raise_committed"):
        assert forbidden not in code, forbidden
    # This exact child is not allowed to grant frontdoor-draw or improved-made action.
    action = executable(block(S, "f$cc_river_delayed_husb_air_bxb100_action"))
    assert "premium_draw" not in action and "good_draw" not in action and "weak_draw" not in action
    assert "two_pair" not in action and "top_pair" not in action and "overpair" not in action


if __name__ == "__main__":
    context_contract()
    lineage_contract()
    router_contract()
    no_unsafe_generalization()
    print("PASS: Gate13 HUSB newest-source BxB100 contract")
