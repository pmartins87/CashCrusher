#!/usr/bin/env python3
"""Gate12A reviewed 3wBTNv2p delayed-CBet gap contract."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3W_BTNv2p_Snapshot.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3W_BTNv2p_Source.txt").read_text(encoding="utf-8")
COMMON = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_Common.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet.txt").read_text(encoding="utf-8")
HIST = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_History.txt").read_text(encoding="utf-8")
SOURCEAIR = (ROOT / "src" / "CashCrusher_Turn_DelayedCBet_3W_Snapshot.txt").read_text(encoding="utf-8")


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    assert marker in text, f"missing {name}"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def normalized_comments(text: str) -> str:
    """Collapse comment line wrapping so provenance tests check meaning, not layout."""
    pieces = []
    for line in text.splitlines():
        if "//" in line:
            pieces.append(line.split("//", 1)[1].strip().lower())
    return " ".join(pieces)


def snapshot_contract() -> None:
    ctx = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnv2p_context")
    for token in (
        "f$cc_turn_delayed_cbet_snapshot_capture_eligible",
        "f$cc_deal_size = 3",
        "f$cc_flop_entry_count = 3",
        "f$cc_multiway",
        "f$cc_hero_pos_id = 4",
    ):
        assert token in ctx
    assert "f$cc_hu" not in executable(ctx)
    assert "f$cc_hu_villain_pos_id" not in executable(ctx)

    source_air = block(SOURCEAIR, "f$cc_turn_delayed_cbet_source_air")
    assert "f$cc_hand_no_made" in source_air
    assert "!f$cc_turn_delayed_cbet_source_gutshot_or_better_draw" in source_air

    cand = block(SNAP, "f$cc_turn_delayed_cbet_snapshot_3w_btnv2p_air_candidate")
    assert "f$cc_turn_delayed_cbet_snapshot_3w_btnv2p_context" in cand
    assert "f$cc_turn_delayed_cbet_source_air" in cand

    writer = block(SNAP, "f$cc_turn_delayed_cbet_3w_btnv2p_snapshot_writer")
    assert "Set user_cc_turn_delayed_cbet_flop_snapshot_seen" in writer
    assert "Set user_cc_turn_delayed_cbet_3w_btnv2p_flop_air_candidate" in writer


def action_and_size_contract() -> None:
    ctx = block(POL, "f$cc_turn_delayed_cbet_3w_btnv2p_context")
    assert "f$cc_turn_delayed_cbet_snapshot_valid" in ctx
    assert "f$cc_deal_size = 3" in ctx
    assert "f$cc_flop_entry_count = 3" in ctx
    assert "f$cc_multiway" in ctx
    assert "f$cc_hero_pos_id = 4" in ctx

    action = block(POL, "f$cc_turn_delayed_cbet_3w_btnv2p_action")
    assert "user_cc_turn_delayed_cbet_3w_btnv2p_flop_air_candidate" in action
    action_code = executable(action).lower()
    for forbidden in ("top_pair", "tpop", "second_pair", "third_pair", "draw"):
        assert forbidden not in action_code, f"adjacent class leaked into BTNv2p action: {forbidden}"

    size = block(POL, "f$cc_turn_delayed_cbet_3w_btnv2p_size_id")
    assert "PotSize > 3 Return f$cc_turn_delayed_cbet_size_33_id" in size
    assert "When Others Return f$cc_turn_delayed_cbet_size_50_id" in size
    size33 = block(COMMON, "f$cc_turn_delayed_cbet_size_33_id")
    assert executable(size33).strip() == "7"

    covered = block(POL, "f$cc_turn_delayed_cbet_3w_btnv2p_covered")
    assert executable(covered).strip() == "f$cc_turn_delayed_cbet_3w_btnv2p_context"
    unresolved = block(POL, "f$cc_turn_delayed_cbet_3w_btnv2p_unresolved")
    assert executable(unresolved).strip() == "false"


def closed_history_contract() -> None:
    valid = block((ROOT / "src" / "CashCrusher_Turn_DelayedCBet_Snapshot.txt").read_text(encoding="utf-8"), "f$cc_turn_delayed_cbet_snapshot_valid")
    assert "f$cc_turn_delayed_cbet_base_opportunity" in valid
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in valid
    assert "user_cc_turn_delayed_cbet_flop_snapshot_seen" in valid
    base = block(HIST, "f$cc_turn_delayed_cbet_base_opportunity")
    assert "f$cc_hist_turn_delayed_cbet_flop_checkthrough_clean" in base


def router_contract() -> None:
    fam = block(ROUTER, "f$cc_turn_delayed_cbet_family_id")
    assert "f$cc_turn_delayed_cbet_3w_btnv2p_covered Return 7 Force" in fam
    action = block(ROUTER, "f$cc_turn_delayed_cbet_router")
    assert "f$cc_turn_delayed_cbet_3w_btnv2p_covered Return f$cc_turn_delayed_cbet_3w_btnv2p_action" in action
    size = block(ROUTER, "f$cc_turn_delayed_cbet_size_id")
    assert "f$cc_turn_delayed_cbet_3w_btnv2p_size_id" in size
    cov = block(ROUTER, "f$cc_turn_delayed_cbet_strategy_covered")
    assert "f$cc_turn_delayed_cbet_3w_btnv2p_covered" in cov
    owners = block(ROUTER, "f$cc_turn_delayed_cbet_child_owner_count")
    assert "f$cc_turn_delayed_cbet_3w_btnv2p_covered" in owners
    consistency = block(ROUTER, "f$cc_turn_delayed_cbet_router_consistent")
    assert "f$cc_turn_delayed_cbet_3w_btnv2p_size_consistent" in consistency


def provenance_and_safety_contract() -> None:
    comments = normalized_comments(SNAP + "\n" + POL)
    assert "starting strategy is silent" in comments or "no dedicated starting strategy" in comments
    assert "no exact source/tbp size" in comments
    assert "a/p" in comments
    assert "scenario-wide" in comments

    code = executable(SNAP + "\n" + POL + "\n" + ROUTER).lower()
    for forbidden in (
        "handpower",
        "random",
        "betmax",
        "raise_committed",
        "stackoff",
        "shorteststack",
        "effectivestack_bkp",
    ):
        assert forbidden not in code, f"unsafe BTNv2p leak: {forbidden}"


if __name__ == "__main__":
    snapshot_contract()
    action_and_size_contract()
    closed_history_contract()
    router_contract()
    provenance_and_safety_contract()
    print("PASS: Gate12A reviewed 3wBTNv2p delayed-CBet gap")
