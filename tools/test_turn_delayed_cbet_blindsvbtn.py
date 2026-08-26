#!/usr/bin/env python3
"""Gate12A native 3wBlinds-v-BTN delayed-CBet reviewed CHECK contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3W_BlindsVBTN_Check.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_History.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    tail = text[text.index(marker) + len(marker):]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def context_contract() -> None:
    ctx = block(POL, "f$cc_turn_delayed_cbet_3w_blindsvbtn_context")
    for token in (
        "f$cc_turn_delayed_cbet_base_opportunity",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 3",
        "f$cc_multiway",
        "f$cc_hero_pos_id = 5 || f$cc_hero_pos_id = 6",
    ):
        assert token in ctx
    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base
    assert "f$cc_turn_delayed_cbet_initiative_supported" in base


def negative_source_contract() -> None:
    assert executable(block(POL, "f$cc_turn_delayed_cbet_3w_blindsvbtn_action")).strip() == "false"
    assert executable(block(POL, "f$cc_turn_delayed_cbet_3w_blindsvbtn_size_id")).strip() == "0"
    covered = block(POL, "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered")
    assert executable(covered).strip() == "f$cc_turn_delayed_cbet_3w_blindsvbtn_context"
    consistent = block(POL, "f$cc_turn_delayed_cbet_3w_blindsvbtn_size_consistent")
    assert "!f$cc_turn_delayed_cbet_3w_blindsvbtn_action" in consistent
    assert "f$cc_turn_delayed_cbet_3w_blindsvbtn_size_id = 0" in consistent
    low = POL.lower()
    assert "scenario-wide `return false`" in low
    assert "no hero-initiative delayed-cbet family" in low


def router_contract() -> None:
    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered Return 8 Force" in fam
    action = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered Return f$cc_turn_delayed_cbet_3w_blindsvbtn_action" in action
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered Return f$cc_turn_delayed_cbet_3w_blindsvbtn_size_id" in size
    cov = block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered" in cov
    owners = block(ROUTER, "f$cc_turn_delayed_cbet_child_owner_count")
    assert "f$cc_turn_delayed_cbet_3w_blindsvbtn_covered" in owners
    consistency = block(ROUTER, "f$cc_turn_delayed_cbet_router_consistent")
    assert "f$cc_turn_delayed_cbet_3w_blindsvbtn_size_consistent" in consistency


def safety_contract() -> None:
    code = executable(POL + "\n" + ROUTER).lower()
    for forbidden in (
        "handpower", "random", "betmax", "raise_committed", "stackoff",
        "shorteststack", "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe blindsvbtn delayed-CBet leak: {forbidden}"


if __name__ == "__main__":
    context_contract()
    negative_source_contract()
    router_contract()
    safety_contract()
    print("PASS: Gate12A native 3wBlinds-v-BTN reviewed CHECK")
