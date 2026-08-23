#!/usr/bin/env python3
"""Deterministic Gate02D.3 tests for multiway-flop -> HU-turn provenance.

This is a source/truth-table gate, not a substitute for OpenHoldem replay tests.
It protects the exact distinction that legacy dynamic `f$game_*` labels can lose:
a current HU turn after a multiway flop is NOT an ordinary flop-HU range state.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX = ROOT / "src" / "CashCrusher_Turn_PostFlopReducedHU_Context.txt"
POLICY = ROOT / "src" / "CashCrusher_Turn_CBet_SRP_PostMultiwayHU.txt"
ROUTER = ROOT / "src" / "CashCrusher_Turn_CBet.txt"


@dataclass(frozen=True)
class C:
    flop_opp_mask: int
    current_opp_mask: int
    flop_entry_count: int
    hero_pos: int
    villain_pos: int
    villain_called_preflop: bool = True
    origin_postflop_reduced: bool = True
    standard_cbet_parent: bool = True


def bitcount(x: int) -> int:
    return int(x).bit_count()


def mask_consistent(c: C) -> bool:
    return (
        bitcount(c.flop_opp_mask) == c.flop_entry_count - 1
        and (c.current_opp_mask & c.flop_opp_mask) == c.current_opp_mask
    )


def postmw_context(c: C) -> bool:
    return (
        c.origin_postflop_reduced
        and c.standard_cbet_parent
        and mask_consistent(c)
        and bitcount(c.current_opp_mask) == 1
        and (c.flop_opp_mask & c.current_opp_mask) > 0
    )


def ordinary_srp_context(c: C) -> bool:
    return postmw_context(c) and c.villain_called_preflop


def folded_count(c: C) -> int:
    if not postmw_context(c):
        return 0
    return bitcount(c.flop_opp_mask - c.current_opp_mask)


def btn_both_blinds_origin(c: C) -> bool:
    return (
        ordinary_srp_context(c)
        and c.flop_entry_count == 3
        and c.hero_pos == 4
        and c.flop_opp_mask == 48  # SB(16) + BB(32)
        and c.villain_pos in (5, 6)
    )


def run_truth_table() -> None:
    # BTN opened, SB+BB entered flop, BB alone survives flop CBet.
    c = C(flop_opp_mask=48, current_opp_mask=32, flop_entry_count=3, hero_pos=4, villain_pos=6)
    assert mask_consistent(c)
    assert ordinary_srp_context(c)
    assert folded_count(c) == 1
    assert btn_both_blinds_origin(c)

    # Same origin, SB survives instead.
    c = C(flop_opp_mask=48, current_opp_mask=16, flop_entry_count=3, hero_pos=4, villain_pos=5)
    assert ordinary_srp_context(c)
    assert folded_count(c) == 1
    assert btn_both_blinds_origin(c)

    # UTG PFA, BTN + BB reached flop, BB survives: valid but P-heavy other origin.
    c = C(flop_opp_mask=40, current_opp_mask=32, flop_entry_count=3, hero_pos=1, villain_pos=6)
    assert ordinary_srp_context(c)
    assert not btn_both_blinds_origin(c)

    # Four-way flop: CO PFA vs BTN+SB+BB; BTN alone survives.
    c = C(flop_opp_mask=56, current_opp_mask=8, flop_entry_count=4, hero_pos=3, villain_pos=4)
    assert ordinary_srp_context(c)
    assert folded_count(c) == 2
    assert not btn_both_blinds_origin(c)

    # Current opponent was never in the reconstructed flop-entry set -> reject.
    c = C(flop_opp_mask=48, current_opp_mask=8, flop_entry_count=3, hero_pos=4, villain_pos=4)
    assert not mask_consistent(c)
    assert not ordinary_srp_context(c)

    # Wrong entrant count for the mask -> reject.
    c = C(flop_opp_mask=48, current_opp_mask=32, flop_entry_count=4, hero_pos=4, villain_pos=6)
    assert not mask_consistent(c)

    # Current state was ordinary flop-HU, not postflop-reduced -> reject this family.
    c = C(
        flop_opp_mask=32,
        current_opp_mask=32,
        flop_entry_count=2,
        hero_pos=4,
        villain_pos=6,
        origin_postflop_reduced=False,
    )
    assert not postmw_context(c)

    # If actual standard CBet history is absent, turn cannot be Turn-CBet family.
    c = C(
        flop_opp_mask=48,
        current_opp_mask=32,
        flop_entry_count=3,
        hero_pos=4,
        villain_pos=6,
        standard_cbet_parent=False,
    )
    assert not ordinary_srp_context(c)

    # Ordinary SRP requires survivor preflop-call evidence.
    c = C(
        flop_opp_mask=48,
        current_opp_mask=32,
        flop_entry_count=3,
        hero_pos=4,
        villain_pos=6,
        villain_called_preflop=False,
    )
    assert postmw_context(c)
    assert not ordinary_srp_context(c)


def function_block(text: str, function_name: str) -> str:
    marker = f"##{function_name}##"
    start = text.index(marker)
    tail = text[start + len(marker):]
    next_header = tail.find("##")
    return tail if next_header < 0 else tail[:next_header]


def run_source_contract() -> None:
    ctx = CTX.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")
    router = ROUTER.read_text(encoding="utf-8")

    # Exact provenance layer must retain postflop-reduced origin and entrant mask.
    required_ctx = (
        "f$cc_hu_origin_postflop_reduced",
        "f$cc_flop_entry_bits",
        "##f$cc_flop_entry_opp_mask##",
        "##f$cc_turn_postmw_survivor_was_flop_opponent##",
        "##f$cc_turn_postmw_survivor_called_preflop##",
        "##f$cc_turn_srp_postmw_context_consistent##",
    )
    for token in required_ctx:
        assert token in ctx, f"missing post-multiway context token: {token}"

    # Exact nearest source shape must be BTN + both blinds, not current HU label.
    btn_block = function_block(ctx, "f$cc_turn_srp_postmw_btn_both_blinds_origin")
    assert "f$cc_hero_pos_id = 4" in btn_block
    assert "f$cc_flop_entry_opp_mask = 48" in btn_block

    # The dedicated strategy must not call ordinary flop-HU source/gap actions.
    forbidden_policy = (
        "f$cc_turn_srp_ip_source_anchored_action",
        "f$cc_turn_srp_oop_source_anchored_action",
        "f$cc_turn_srp_6max_gap_action",
        "BetMax",
    )
    # BetMax may appear in explanatory comments, so check executable text only.
    executable_policy = "\n".join(line.split("//", 1)[0] for line in policy.splitlines())
    for token in forbidden_policy:
        assert token not in executable_policy, f"forbidden post-multiway policy leak: {token}"

    # Selection pressure must explicitly include 4way+, large flop size, nonblind.
    for token in (
        "f$cc_turn_srp_postmw_flop4plus_origin",
        "f$cc_turn_srp_postmw_large_flop_cbet",
        "f$cc_turn_postmw_survivor_nonblind",
    ):
        assert token in policy, f"missing selected-range modifier: {token}"

    # Router must give origin=3 dedicated family precedence before ordinary HU trees.
    postmw_route = "When f$cc_turn_srp_postmw_hu_covered Return f$cc_turn_srp_postmw_hu_action Force"
    src_ip_route = "When f$cc_turn_srp_ip_source_anchored_covered Return f$cc_turn_srp_ip_source_anchored_action Force"
    gap_route = "When f$cc_turn_srp_6max_gap_covered Return f$cc_turn_srp_6max_gap_action Force"
    assert postmw_route in router
    assert router.index(postmw_route) < router.index(src_ip_route)
    assert router.index(postmw_route) < router.index(gap_route)

    # Residual OOP flop-HU family must explicitly require origin=2.
    oop_residual = function_block(router, "f$cc_turn_cbet_srp_oop_uncovered_context")
    assert "f$cc_hu_origin_preflop_reduced" in oop_residual

    # Coverage and sizing must include the dedicated family.
    assert "f$cc_turn_srp_postmw_hu_covered" in function_block(router, "f$cc_turn_cbet_strategy_covered")
    assert "f$cc_turn_srp_postmw_hu_size_id" in function_block(router, "f$cc_turn_cbet_size_id")


if __name__ == "__main__":
    run_truth_table()
    run_source_contract()
    print("PASS: Gate02D.3 post-multiway HU Turn-CBet provenance and routing contract")
