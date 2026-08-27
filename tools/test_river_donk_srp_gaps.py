#!/usr/bin/env python3
"""Gate09C ordinary-SRP River Donk source/gap contracts."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TEXT = (SRC / "CashCrusher_River_Donk_SRP_Gaps.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_River_Donk.txt").read_text(encoding="utf-8")


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
    ctx = block(TEXT, "f$cc_river_donk_srp_context")
    for token in (
        "f$cc_river_donk_base_opportunity",
        "f$cc_pot_family_id = 2",
        "f$cc_pf_one_raise_ordinary_srp",
        "f$cc_pf_role_pfa || f$cc_pf_role_srp_caller",
    ):
        assert token in ctx

    exact = block(TEXT, "f$cc_river_donk_srp_exact_3w_sbvbb")
    for token in (
        "f$cc_deal_size = 3",
        "f$cc_hero_pos_id = 5",
        "f$cc_river_donk_turn_aggressor_pos_id = 6",
        "headsupchair = bigblindchair",
        "f$cc_flop_entry_count = 2",
    ):
        assert token in exact

    topo = block(TEXT, "f$cc_river_donk_srp_topology_id")
    for n in range(1, 5):
        assert f"Return {n} Force" in topo


def source_contract() -> None:
    assert "SecondTopFlopCard < RiverCard" in block(TEXT, "f$cc_river_donk_srp_river_moc")
    assert "RiverCardIsOvercardToBoard > 0" in block(TEXT, "f$cc_river_donk_srp_river_moc")
    assert "TopFlopCardPairedOnRiver" in block(TEXT, "f$cc_river_donk_srp_paired_top_card")
    assert "TurnCardPaired" in block(TEXT, "f$cc_river_donk_srp_paired_fourth_card")
    assert "!FlushPossibleOnTurn && FlushPossible" in block(TEXT, "f$cc_river_donk_srp_new_flush_possible")

    # Exact mature DeepCrusher negative source stays negative.
    neg = block(TEXT, "f$cc_river_donk_srp_source_negative_action")
    assert "f$cc_river_donk_srp_exact_3w_sbvbb Return false Force" in neg

    # Reconstructible TBP mOC branch has exact 50% source sizing.
    moc = block(TEXT, "f$cc_river_donk_srp_tbp_moc_value")
    assert "f$cc_river_donk_srp_contributed_2pplus" in moc
    assert "!f$cc_river_donk_srp_river_paired" in moc
    assert "!f$cc_river_donk_srp_new_flush_possible" in moc
    assert "f$cc_river_donk_srp_river_moc" in moc
    size = block(TEXT, "f$cc_river_donk_srp_gap_size_id")
    assert "f$cc_river_donk_srp_tbp_moc_value Return 4 Force" in size

    # Missing Turn-price provenance must remain visible and not guessed.
    price = block(TEXT, "f$cc_river_donk_srp_tbp_price_provenance_missing")
    assert "f$cc_river_donk_srp_river_paired || f$cc_river_donk_srp_new_flush_possible" in price
    action = block(TEXT, "f$cc_river_donk_srp_gap_action")
    assert "f$cc_river_donk_srp_tbp_price_provenance_missing Return false Force" in action


def professional_gap_contract() -> None:
    hu = block(TEXT, "f$cc_river_donk_srp_hu_robust_value")
    assert "HaveNuts Return true Force" in hu
    assert "f$cc_river_four_card_completion" in hu
    assert "f$cc_river_donk_contributed_exact_two_pair || HaveSet Return true Force" in hu

    mw = block(TEXT, "f$cc_river_donk_srp_multiway_origin_robust_value")
    assert "HaveNuts Return true Force" in mw
    assert "f$cc_river_four_card_completion Return false Force" in mw
    assert "HaveSet Return true Force" in mw

    # One-pair and no-made never get an unconditional generic positive line.
    action = block(TEXT, "f$cc_river_donk_srp_gap_action")
    low = action.lower()
    assert "top_pair" not in low and "overpair" not in low
    assert "no_made" not in low

    code = executable(TEXT).lower()
    for forbidden in ("handpower", "random", "betmax", "raise_committed", "stackoffdraws", "f$game_"):
        assert forbidden not in code, f"legacy leak: {forbidden}"


def router_contract() -> None:
    family = block(ROUTER, "f$cc_river_donk_family_id")
    assert "f$cc_river_donk_srp_gap_covered Return 2 Force" in family
    route = block(ROUTER, "f$cc_river_donk_router")
    assert "f$cc_river_donk_srp_gap_covered Return f$cc_river_donk_srp_gap_action Force" in route
    size = block(ROUTER, "f$cc_river_donk_size_id")
    assert "f$cc_river_donk_srp_gap_covered Return f$cc_river_donk_srp_gap_size_id Force" in size
    count = block(ROUTER, "f$cc_river_donk_reviewed_family_count")
    assert "f$cc_river_donk_hubb_covered" in count and "f$cc_river_donk_srp_gap_covered" in count


if __name__ == "__main__":
    topology_contract()
    source_contract()
    professional_gap_contract()
    router_contract()
    print("PASS: Gate09C ordinary-SRP River Donk gaps")
