#!/usr/bin/env python3
"""Gate12B.10/11 deterministic tests for 4-6h unraised delayed float."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_Unraised_Snapshot.txt").read_text(encoding="utf-8")
POLICY = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_Unraised_6Max.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    return text.split(marker, 1)[1].split("##", 1)[0]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def snapshot_contract() -> None:
    ctx = block(SNAP, "f$cc_turn_delayed_float_unraised_snapshot_context")
    for token in (
        "IsFlop",
        "BotsActionsOnThisRoundIncludingChecks = 0",
        "AmountToCall = 0",
        "f$cc_relpos_id = 3",
        "f$cc_deal_size >= 4",
        "f$cc_deal_size <= 6",
        "f$cc_pot_family_id = 1",
        "f$cc_turn_delayed_float_preflop_noinitiative",
        "f$cc_pf_role_unraised_caller",
        "f$cc_pf_role_bb_check",
    ):
        assert token in ctx

    writer = block(SNAP, "f$cc_turn_delayed_float_unraised_snapshot_writer")
    for marker in (
        "user_cc_turn_delayed_float_unraised_snapshot_seen",
        "user_cc_turn_delayed_float_unraised_flop_2pplus",
        "user_cc_turn_delayed_float_unraised_flop_overpair",
        "user_cc_turn_delayed_float_unraised_flop_top_pair",
        "user_cc_turn_delayed_float_unraised_flop_lower_pair",
        "user_cc_turn_delayed_float_unraised_flop_no_made",
        "user_cc_turn_delayed_float_unraised_flop_real_draw",
        "user_cc_turn_delayed_float_unraised_flop_air",
    ):
        assert marker in writer

    # PRE-ACTION snapshot is not execution proof: Turn consumption additionally
    # requires the canonical CLOSED X/X base opportunity.
    valid = block(SNAP, "f$cc_turn_delayed_float_unraised_snapshot_valid")
    assert "f$cc_turn_delayed_float_base_opportunity" in valid
    assert "user_cc_turn_delayed_float_unraised_snapshot_seen" in valid
    assert "f$cc_turn_delayed_float_unraised_saved_primary_count != 1" in valid


def policy_contract() -> None:
    ctx = block(POLICY, "f$cc_turn_delayed_float_unraised6_context")
    assert "f$cc_turn_delayed_float_unraised_snapshot_valid" in ctx
    assert "f$cc_pot_family_id = 1" in ctx
    assert "f$cc_deal_size >= 4" in ctx and "f$cc_deal_size <= 6" in ctx

    hu = block(POLICY, "f$cc_turn_delayed_float_unraised6_hu_action")
    for token in (
        "f$cc_turn_delayed_float_two_pair_plus_real Return true",
        "f$cc_turn_delayed_float_tpop_real && f$cc_turn_delayed_float_thin_value_runout Return true",
        "f$cc_turn_delayed_float_unraised6_secondpair_thin Return true",
        "f$cc_turn_delayed_float_semibluff_candidate Return true",
        "f$cc_turn_delayed_float_unraised6_air_bluff Return true",
        "When Others Return false Force",
    ):
        assert token in hu

    thin = block(POLICY, "f$cc_turn_delayed_float_unraised6_secondpair_thin")
    assert "f$cc_turn_delayed_float_unraised_flop_had_lower_pair" in thin
    assert "f$cc_turn_undercard" in thin

    bluff = block(POLICY, "f$cc_turn_delayed_float_unraised6_air_bluff")
    assert "f$cc_turn_delayed_float_unraised_flop_had_air" in bluff
    assert "f$cc_turn_delayed_float_bluff_pressure_card" in bluff

    mw = block(POLICY, "f$cc_turn_delayed_float_unraised6_mw_action")
    assert "f$cc_turn_delayed_float_unraised6_exact_threeway" in mw
    assert "f$cc_real_combo_draw" in mw
    assert "air_bluff" not in mw
    assert "When Others Return false Force" in mw

    sizes = block(POLICY, "f$cc_turn_delayed_float_unraised6_hu_size_id")
    for token in (
        "f$cc_turn_delayed_float_size_33_id",
        "f$cc_turn_delayed_float_size_50_id",
        "f$cc_turn_delayed_float_size_75_id",
    ):
        assert token in sizes


def router_contract() -> None:
    fam = block(ROUTER, "f$cc_turn_delayed_float_family_id")
    assert "When f$cc_turn_delayed_float_unraised6_hu_context Return 12 Force" in fam
    assert "When f$cc_turn_delayed_float_unraised6_mw_context Return 13 Force" in fam
    router = block(ROUTER, "f$cc_turn_delayed_float_router")
    assert "f$cc_turn_delayed_float_unraised6_covered Return f$cc_turn_delayed_float_unraised6_action" in router
    covered = block(ROUTER, "f$cc_turn_delayed_float_strategy_covered")
    assert "f$cc_turn_delayed_float_unraised6_covered" in covered


def safety_contract() -> None:
    code = executable(SNAP + "\n" + POLICY).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe unraised delayed-float token: {forbidden}"


if __name__ == "__main__":
    snapshot_contract()
    policy_contract()
    router_contract()
    safety_contract()
    print("PASS: Gate12B 4-6h unraised delayed-float contract")
