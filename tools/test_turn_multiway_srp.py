#!/usr/bin/env python3
"""Deterministic Gate02E source/routing tests for ordinary-SRP MW Turn CBet."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "src" / "CashCrusher_Turn_Multiway_SRP_Context.txt"
POLICY = ROOT / "src" / "CashCrusher_Turn_CBet_SRP_Multiway.txt"
ROUTER = ROOT / "src" / "CashCrusher_Turn_CBet.txt"


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def run_source_contract() -> None:
    ctx = CTX.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")
    router = ROUTER.read_text(encoding="utf-8")
    exe = executable(policy)

    # Exact source-adjacent shape must retain BTN + both blinds + still3 + LAST.
    srcshape = block(ctx, "f$cc_turn_mw_srp_btn_both_blinds_source_shape")
    for token in (
        "f$cc_turn_mw_srp_true3_still3",
        "f$cc_hero_pos_id = 4",
        "f$cc_flop_entry_opp_mask = 48",
        "f$cc_opp_live_mask = 48",
        "f$cc_multiway_rel_last",
    ):
        assert token in srcshape, f"missing exact source-shape condition: {token}"

    # 4way+ origin reduced to three and current4plus must be distinct functions.
    assert "##f$cc_turn_mw_srp_flop4plus_now3##" in ctx
    assert "##f$cc_turn_mw_srp_current4plus##" in ctx

    # Multiway policy must use corrected DEEPEST SPR, never generic HU/shallow SPR.
    assert "f$cc_mw_spr_deepest_round_start" in ctx
    forbidden_depth = (
        "f$cc_spr_round_start",
        "f$cc_spr_bucket_id",
        "f$cc_mw_spr_shallowest_round_start",
    )
    for token in forbidden_depth:
        assert token not in exe, f"forbidden MW Turn depth helper: {token}"

    # No all-in or HU-policy leakage in multiway strategy.
    for token in (
        "BetMax",
        "f$cc_turn_srp_ip_source_anchored_action",
        "f$cc_turn_srp_oop_source_anchored_action",
        "f$cc_turn_srp_6max_gap_action",
        "f$cc_turn_srp_postmw_hu_action",
    ):
        assert token not in exe, f"forbidden MW strategy leak: {token}"

    # 4+ current baseline must explicitly reject frontdoor draws and air.
    fourplus = block(policy, "f$cc_turn_mw_srp_current4plus_action")
    assert "When f$cc_real_frontdoor_draw Return false Force" in fourplus
    assert "When f$cc_turn_cbet_air Return false Force" in fourplus

    # The exact source-adjacent v2p descendant may barrel selected lower value and
    # equity, but must not end in a generic true tail.
    source_action = block(policy, "f$cc_turn_mw_srp_btn_blinds_last_action")
    assert "f$cc_turn_cbet_second_pair" in source_action
    assert "f$cc_turn_cbet_premium_draw" in source_action
    assert "When Others Return false Force" in source_action

    # Router must dispatch both post-multiway-HU and current-MW before HU families.
    postmw = "When f$cc_turn_srp_postmw_hu_covered Return f$cc_turn_srp_postmw_hu_action Force"
    mw = "When f$cc_turn_mw_srp_covered Return f$cc_turn_mw_srp_action Force"
    hu = "When f$cc_turn_srp_ip_source_anchored_covered Return f$cc_turn_srp_ip_source_anchored_action Force"
    assert postmw in router and mw in router and hu in router
    assert router.index(postmw) < router.index(hu)
    assert router.index(mw) < router.index(hu)

    # Multiway top-level context must require Gate02E consistency, not just player count.
    mw_top = block(router, "f$cc_turn_cbet_srp_multiway_context")
    assert "f$cc_turn_mw_srp_context_consistent" in mw_top

    # Coverage and sizing are wired.
    assert "f$cc_turn_mw_srp_covered" in block(router, "f$cc_turn_cbet_strategy_covered")
    assert "f$cc_turn_mw_srp_size_id" in block(router, "f$cc_turn_cbet_size_id")


if __name__ == "__main__":
    run_source_contract()
    print("PASS: Gate02E ordinary-SRP multiway Turn-CBet source/routing contract")
