#!/usr/bin/env python3
"""Gate11F native true-multiway River Probe source contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_River_Probe_Multiway_Source.txt").read_text(encoding="utf-8")
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
    ctx = block(POL, "f$cc_river_probe_native_mw_context")
    for token in (
        "f$cc_river_probe_base_opportunity",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 3",
        "f$cc_hero_pos_id = 5 || f$cc_hero_pos_id = 6",
        "f$cc_pot_family_id = 1 || f$cc_pot_family_id = 2",
        "!f$cc_pf_role_pfa",
        "!f$cc_pf_role_3bettor",
        "!f$cc_pf_role_4bettor",
        "f$cc_river_probe_field_origin_id = 3 || f$cc_river_probe_field_origin_id = 4",
    ):
        assert token in ctx

    field = block(HIST, "f$cc_river_probe_field_origin_id")
    assert "f$cc_hu_origin_postflop_reduced Return 3 Force" in field
    assert "f$cc_river_probe_multiway_opportunity Return 4 Force" in field


def provenance_contract() -> None:
    proven = block(POL, "f$cc_river_probe_native_mw_highair_call_proven")
    assert "user_cc_flop_mw_highair_called_le33_sourcelegal" in proven

    parent = block(POL, "f$cc_river_probe_native_mw_source_parent")
    assert "f$cc_river_probe_native_mw_context" in parent
    assert "f$cc_river_probe_native_mw_highair_call_proven" in parent

    pending = block(POL, "f$cc_river_probe_native_mw_defense_provenance_pending")
    assert "f$cc_river_probe_native_mw_context" in pending
    assert "!f$cc_river_probe_native_mw_highair_call_proven" in pending


def source_action_contract() -> None:
    sf = block(POL, "f$cc_river_probe_native_mw_straightflush_translation_pending")
    assert "f$cc_river_probe_3w_current_straightflush_pending" in sf

    strong = block(POL, "f$cc_river_probe_native_mw_strong100")
    assert "f$cc_river_probe_3w_strong_safe" in strong
    two = block(POL, "f$cc_river_probe_native_mw_exact2p75")
    assert "f$cc_river_probe_contributed_exact_two_pair" in two
    tpop = block(POL, "f$cc_river_probe_native_mw_tpop50")
    assert "f$cc_river_probe_3w_tp_or_op_real" in tpop
    air = block(POL, "f$cc_river_probe_native_mw_air50")
    assert "f$cc_river_probe_air" in air

    residual = block(POL, "f$cc_river_probe_native_mw_residual_check")
    assert "!f$cc_river_probe_native_mw_straightflush_translation_pending" in residual
    assert "!f$cc_river_probe_native_mw_strong100" in residual
    assert "!f$cc_river_probe_native_mw_exact2p75" in residual
    assert "!f$cc_river_probe_native_mw_tpop50" in residual
    assert "!f$cc_river_probe_native_mw_air50" in residual

    action = block(POL, "f$cc_river_probe_native_mw_action")
    assert "f$cc_river_probe_native_mw_residual_check Return false Force" in action

    size = block(POL, "f$cc_river_probe_native_mw_size_id")
    for token in (
        "f$cc_river_probe_native_mw_strong100 Return f$cc_river_probe_size_100_id",
        "f$cc_river_probe_native_mw_exact2p75 Return f$cc_river_probe_size_75_id",
        "f$cc_river_probe_native_mw_tpop50 Return f$cc_river_probe_size_50_id",
        "f$cc_river_probe_native_mw_air50 Return f$cc_river_probe_size_50_id",
    ):
        assert token in size


def router_and_safety_contract() -> None:
    fam = block(ROUTER, "f$cc_river_probe_family_id")
    assert "f$cc_river_probe_native_mw_covered Return 4 Force" in fam
    action = block(ROUTER, "f$cc_river_probe_router")
    assert "f$cc_river_probe_native_mw_covered Return f$cc_river_probe_native_mw_action Force" in action
    size = block(ROUTER, "f$cc_river_probe_size_id")
    assert "f$cc_river_probe_native_mw_covered Return f$cc_river_probe_native_mw_size_id Force" in size
    cov = block(ROUTER, "f$cc_river_probe_strategy_covered")
    assert "f$cc_river_probe_native_mw_covered" in cov

    code = executable(POL).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "f$game_",
        "f$cf7_",
        "amounttocall",
        "potcommon",
        "effectivestack_bkp",
    ):
        assert forbidden not in code, f"forbidden native-MW River Probe leak: {forbidden}"

    consistency = block(POL, "f$cc_river_probe_native_mw_size_consistent")
    assert "f$cc_river_probe_native_mw_size_id = 0" in consistency
    assert "f$cc_river_probe_native_mw_size_id <= 7" in consistency


if __name__ == "__main__":
    topology_contract()
    provenance_contract()
    source_action_contract()
    router_and_safety_contract()
    print("PASS: Gate11F native true-multiway River Probe source contract")
