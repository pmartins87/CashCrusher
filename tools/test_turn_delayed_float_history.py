#!/usr/bin/env python3
"""Gate12B.1 deterministic tests for Turn Delayed-Float ownership/history."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat_History.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedFloat.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing function {name}"
    tail = text.split(marker, 1)[1]
    return tail.split("##", 1)[0]


@dataclass(frozen=True)
class H:
    context_valid: bool = True
    first_turn_action: bool = True
    flop_checkthrough: bool = True
    noinitiative: bool = True
    relpos: int = 3
    postflop_reduced_hu: bool = False
    probe: bool = False
    delayed_cbet: bool = False
    field_origin: int = 2


def base(h: H) -> bool:
    return (
        h.context_valid
        and h.first_turn_action
        and h.flop_checkthrough
        and h.noinitiative
        and h.relpos == 3
    )


def consistent(h: H) -> bool:
    if h.postflop_reduced_hu or h.probe or h.delayed_cbet:
        return False
    if base(h) and h.field_origin <= 0:
        return False
    if base(h) and not h.noinitiative:
        return False
    return True


def run_truth_table() -> None:
    # Exact LAST, no initiative, closed X/X -> Gate12B owner.
    h = H()
    assert base(h) and consistent(h)

    # Framework first ternary consumes MIDDLE into Probe, never delayed float.
    assert not base(H(relpos=2))

    # FIRST is Probe ownership, not 12B.
    assert not base(H(relpos=1))

    # Any real initiative belongs Gate12A.
    assert not base(H(noinitiative=False))

    # Flop aggression or missing actual Hero check invalidates delayed history.
    assert not base(H(flop_checkthrough=False))

    # Current HU cannot have become HU postflop after an aggression-free X/X flop.
    assert not consistent(H(postflop_reduced_hu=True))

    # Explicit node overlaps are impossible by contract.
    assert not consistent(H(probe=True))
    assert not consistent(H(delayed_cbet=True))


def run_source_contract() -> None:
    for name in (
        "f$cc_turn_delayed_float_preflop_noinitiative",
        "f$cc_turn_delayed_float_first_turn_action_clean",
        "f$cc_turn_delayed_float_base_opportunity",
        "f$cc_turn_delayed_float_field_origin_id",
        "f$cc_turn_delayed_float_history_consistent",
    ):
        assert f"##{name}##" in HISTORY

    noinit = block(HISTORY, "f$cc_turn_delayed_float_preflop_noinitiative")
    for allowed in (
        "f$cc_pf_role_srp_caller",
        "f$cc_pf_role_open_call_3bet",
        "f$cc_pf_role_cold_call_3bet",
        "f$cc_pf_role_call_4bet",
        "f$cc_pf_role_unraised_caller",
        "f$cc_pf_role_bb_check",
    ):
        assert allowed in noinit, f"missing no-initiative role: {allowed}"
    for forbidden in (
        "f$cc_pf_role_pfa Return true",
        "f$cc_pf_role_3bettor Return true",
        "f$cc_pf_role_4bettor Return true",
        "f$cc_native_limped_initiative Return true",
    ):
        assert forbidden not in noinit

    first = block(HISTORY, "f$cc_turn_delayed_float_first_turn_action_clean")
    assert "BotsActionsOnThisRoundIncludingChecks = 0" in first
    assert "AmountToCall = 0" in first
    assert "f$cc_relpos_id = 3" in first
    assert "f$cc_relpos_id = 2" not in first

    opportunity = block(HISTORY, "f$cc_turn_delayed_float_base_opportunity")
    assert "f$cc_hist_turn_probe_flop_checkthrough_clean" in opportunity
    assert "f$cc_turn_delayed_float_preflop_noinitiative" in opportunity

    # Explicit anti-overlap with adjacent attack nodes is mandatory.
    assert "f$cc_turn_probe_base_opportunity" in HISTORY
    assert "f$cc_turn_delayed_cbet_base_opportunity" in HISTORY
    assert "f$cc_turn_delayed_float_postflop_reduced_hu_impossible" in HISTORY

    # Router must fail closed outside reviewed children.
    router = block(ROUTER, "f$cc_turn_delayed_float_router")
    assert "When Others Return false Force" in router


if __name__ == "__main__":
    run_truth_table()
    run_source_contract()
    print("PASS: Gate12B delayed-float ownership/history contract")
