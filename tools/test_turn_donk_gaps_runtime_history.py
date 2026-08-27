#!/usr/bin/env python3
"""Gate08D-G/H/N residual Turn Donk strategy/runtime/history contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
HU = (SRC / "CashCrusher_Turn_Donk_SRP_ResidualHU.txt").read_text(encoding="utf-8")
MW = (SRC / "CashCrusher_Turn_Donk_SRP_ResidualMW.txt").read_text(encoding="utf-8")
ISO = (SRC / "CashCrusher_Turn_Donk_ISO.txt").read_text(encoding="utf-8")
P3 = (SRC / "CashCrusher_Turn_Donk_3BP.txt").read_text(encoding="utf-8")
P4 = (SRC / "CashCrusher_Turn_Donk_4BP.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_Turn_Donk.txt").read_text(encoding="utf-8")
BET = (SRC / "CashCrusher_Turn_Donk_Betsize.txt").read_text(encoding="utf-8")
GEO = (SRC / "CashCrusher_Turn_Donk_StackGeometry.txt").read_text(encoding="utf-8")
ALLIN = (SRC / "CashCrusher_Turn_Donk_AllinEquivalence.txt").read_text(encoding="utf-8")
HIST = (SRC / "CashCrusher_Turn_Donk_ActionHistory.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def residual_srp_contract() -> None:
    hu = block(HU, "f$cc_turn_donk_srp_residual_hu_context")
    for token in (
        "f$cc_turn_donk_opportunity",
        "f$cc_hu",
        "f$cc_hu_oop",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "!f$cc_turn_donk_srp_hu_source_ancestry",
    ):
        assert token in hu
    assert "Return false Force" in block(HU, "f$cc_turn_donk_srp_residual_hu_action")
    assert block(HU, "f$cc_turn_donk_srp_residual_hu_size_id").strip().startswith("0")

    mw = block(MW, "f$cc_turn_donk_srp_residual_mw_context")
    for token in (
        "f$cc_turn_donk_opportunity",
        "f$cc_multiway",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "!f$cc_turn_donk_srp_mw_source_ancestry",
    ):
        assert token in mw
    stack = block(MW, "f$cc_turn_donk_srp_residual_mw_stack_valid")
    assert "f$cc_mw_spr_bounds_valid" in stack
    assert "f$cc_mw_spr_shallowest" not in stack
    assert "Return false Force" in block(MW, "f$cc_turn_donk_srp_residual_mw_action")

    # A P CHECK family must never swallow known source ancestry.
    for text, name in ((HU, "f$cc_turn_donk_srp_hu_source_ancestry"), (MW, "f$cc_turn_donk_srp_mw_source_ancestry")):
        b = block(text, name)
        assert "native_source_ancestry" in b or "dedicated_source_ancestry" in b


def iso_contract() -> None:
    origin = block(ISO, "f$cc_turn_donk_iso_hero_origin_id")
    assert "Return 1 Force" in origin and "Return 2 Force" in origin and "Return 3 Force" in origin
    base = block(ISO, "f$cc_turn_donk_iso_base_context")
    assert "f$cc_pf_iso_proven" in base
    assert "!f$cc_true_hu" in base
    assert "f$cc_turn_donk_iso_hero_origin_consistent" in base
    assert "f$cc_turn_donk_hu_aggressor_is_current_villain" in block(ISO, "f$cc_turn_donk_iso_hu_context")
    assert "f$cc_mw_spr_bounds_valid" in block(ISO, "f$cc_turn_donk_iso_mw_context")
    action = block(ISO, "f$cc_turn_donk_iso_action")
    assert "Return false Force" in action and "Return true Force" not in action


def threebet_contract() -> None:
    origin = block(P3, "f$cc_turn_donk_3bp_hero_origin_id")
    for n in range(1, 5):
        assert f"Return {n} Force" in origin
    plain = block(P3, "f$cc_turn_donk_plain3bp_context")
    sq = block(P3, "f$cc_turn_donk_squeeze_context")
    assert "f$cc_pf_rt_plain3bet_proven" in plain
    assert "f$cc_pf_rt_squeeze_proven" in sq
    subtype = block(P3, "f$cc_turn_donk_3bp_subtype_id")
    assert "Return 1 Force" in subtype and "Return 2 Force" in subtype
    assert "f$cc_turn_donk_hu_aggressor_is_current_villain" in block(P3, "f$cc_turn_donk_3bp_hu_context")
    assert "f$cc_mw_spr_bounds_valid" in block(P3, "f$cc_turn_donk_3bp_mw_context")
    action = block(P3, "f$cc_turn_donk_3bp_action")
    assert "Return false Force" in action and "Return true Force" not in action


def fourbet_contract() -> None:
    for name in (
        "f$cc_turn_donk_4bp_opener4_vs_threebettor",
        "f$cc_turn_donk_4bp_cold4_vs_opener",
        "f$cc_turn_donk_4bp_cold4_vs_threebettor",
        "f$cc_turn_donk_4bp_call4_vs_opener4",
    ):
        assert block(P4, name).strip()
    base = block(P4, "f$cc_turn_donk_4bp_hero4_base")
    assert "f$cc_hu" in base and "f$cc_hu_oop" in base and "f$cc_flop_entry_count = 2" in base
    assert "f$cc_hu_4bp_survivor_type_id = 1 || f$cc_hu_4bp_survivor_type_id = 2" in base
    count = block(P4, "f$cc_turn_donk_4bp_parent_count")
    assert count.count("* 1") == 4
    action = block(P4, "f$cc_turn_donk_4bp_action")
    assert "Return false Force" in action and "Return true Force" not in action
    code = executable(P4).lower()
    assert "spr <" not in code and "betmax" not in code and "stackoff" not in code


def router_contract() -> None:
    family = block(ROUTER, "f$cc_turn_donk_family_id")
    expected = {
        6: "f$cc_turn_donk_srp_residual_hu_covered",
        7: "f$cc_turn_donk_srp_residual_mw_covered",
        8: "f$cc_turn_donk_iso_covered",
        9: "f$cc_turn_donk_3bp_covered",
        10: "f$cc_turn_donk_4bp_covered",
    }
    for fid, owner in expected.items():
        assert f"When {owner} Return {fid} Force" in family
        assert owner in block(ROUTER, "f$cc_turn_donk_router")
        assert owner in block(ROUTER, "f$cc_turn_donk_size_id")
        assert owner in block(ROUTER, "f$cc_turn_donk_strategy_covered")
    count = block(ROUTER, "f$cc_turn_donk_reviewed_family_count")
    for owner in expected.values():
        assert owner in count
    exclusive = block(ROUTER, "f$cc_turn_donk_family_exclusive")
    assert "f$cc_turn_donk_reviewed_family_count = 1" in exclusive
    assert "f$cc_turn_donk_reviewed_family_count = 0" in exclusive


def runtime_contract() -> None:
    mapping = block(BET, "f$cc_turn_donk_requested_betsize")
    for action in ("BetFourthPot", "BetHalfPot", "BetThreeFourthPot", "BetPot", "BetMin"):
        assert action in mapping
    frac = block(BET, "f$cc_turn_donk_requested_pot_fraction")
    for value in ("0.25", "0.50", "0.75", "1.00"):
        assert value in frac
    assert "1.00 / f$cc_round_start_pot_bb" in frac

    clean = block(GEO, "f$cc_turn_donk_stackgeom_clean")
    for token in ("AmountToCall = 0", "currentbet = 0", "potplayer = 0"):
        assert token in clean
    betbb = block(GEO, "f$cc_turn_donk_requested_bet_bb")
    assert "f$cc_turn_donk_size_id = 5 Return 1.00 Force" in betbb
    assert "f$cc_mw_shallowest_effective_stack_round_start_bb" in block(GEO, "f$cc_turn_donk_requested_mw_shallowest_ratio")
    assert "f$cc_mw_deepest_effective_stack_round_start_bb" in block(GEO, "f$cc_turn_donk_requested_mw_deepest_ratio")

    all_live = executable(block(ALLIN, "f$cc_turn_donk_requested_reaches_all_live_effective"))
    assert "requested_reaches_mw_deepest" in all_live
    assert "requested_reaches_mw_shallowest" not in all_live
    natural = block(ALLIN, "f$cc_turn_donk_natural_allin_equivalent")
    assert "f$cc_turn_donk_requested_reaches_hero_stack" in natural
    assert "f$cc_turn_donk_requested_reaches_all_live_effective" in natural
    execution = block(ALLIN, "f$cc_turn_donk_execution_betsize")
    assert "Return BetMax Force" in execution
    assert "Return f$cc_turn_donk_requested_betsize Force" in execution
    sidepot = block(ALLIN, "f$cc_turn_donk_sidepot_divergence_not_promoted")
    assert "f$cc_turn_donk_mw_sidepot_divergence_candidate" in sidepot


def history_contract() -> None:
    wrapper = block(HIST, "f$cc_turn_donk_action_with_history")
    assert "Set user_cc_turn_donk_opportunity_seen" in wrapper
    assert "Set user_cc_turn_donk_state_snapshot_recorded" in wrapper
    for fid in range(1, 11):
        assert f"f$cc_turn_donk_family_id = {fid} Set user_cc_turn_donk_state_family_{fid}" in wrapper
    assert "f$cc_turn_donk_router Return true Force" in wrapper

    executed = block(HIST, "f$cc_hist_turn_donk_initial_bet_executed")
    for token in ("didchecround3 = 0", "didbetsizeround3 > 0", "didalliround3 > 0"):
        assert token in executed
    standard = block(HIST, "f$cc_hist_turn_donk_standard_parent")
    for token in ("didbetsizeround3 = 1", "didcallround3 = 0", "lastraised3 = userchair"):
        assert token in standard
    river_parent = block(HIST, "f$cc_hist_river_donk_standard_parent_valid")
    assert "f$cc_hist_turn_donk_snapshot_consistent" in river_parent
    assert "f$cc_turn_donk_plan_markers_consistent" in river_parent
    assert "!f$cc_hist_turn_donk_runtime_mismatch" in river_parent
    mismatch = block(HIST, "f$cc_hist_turn_donk_runtime_mismatch")
    for token in (
        "planned_bet_but_checked",
        "executed_without_plan",
        "unexpected_allin_promotion",
        "expected_allin_not_executed",
    ):
        assert token in mismatch


def p_policy_safety_contract() -> None:
    for name, text in (("HU", HU), ("MW", MW), ("ISO", ISO), ("3BP", P3), ("4BP", P4)):
        code = executable(text).lower()
        for forbidden in ("handpower", "random", "raise_committed", "stackoffdraws", "f$game_"):
            assert forbidden not in code, f"{name}: forbidden executable legacy leak {forbidden}"
        # These gap policies are CHECK-only; all BetMax behavior belongs runtime geometry.
        assert "betmax" not in code, f"{name}: gap policy must not contain BetMax"


if __name__ == "__main__":
    residual_srp_contract()
    iso_contract()
    threebet_contract()
    fourbet_contract()
    router_contract()
    runtime_contract()
    history_contract()
    p_policy_safety_contract()
    print("PASS: Gate08D-G/H/N Turn Donk gaps + runtime + closed-history contract")
