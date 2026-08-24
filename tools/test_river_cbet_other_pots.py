#!/usr/bin/env python3
"""Gate03D-G deterministic River-CBet provenance/routing tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
FILES = {
    "iso_ctx": (SRC / "CashCrusher_River_ISO_Context.txt").read_text(encoding="utf-8"),
    "iso": (SRC / "CashCrusher_River_CBet_ISO.txt").read_text(encoding="utf-8"),
    "p3_ctx": (SRC / "CashCrusher_River_3BP_Context.txt").read_text(encoding="utf-8"),
    "p3": (SRC / "CashCrusher_River_CBet_3BP.txt").read_text(encoding="utf-8"),
    "sq_ctx": (SRC / "CashCrusher_River_Squeeze_Context.txt").read_text(encoding="utf-8"),
    "sq": (SRC / "CashCrusher_River_CBet_Squeeze.txt").read_text(encoding="utf-8"),
    "p4_ctx": (SRC / "CashCrusher_River_4BP_Context.txt").read_text(encoding="utf-8"),
    "p4": (SRC / "CashCrusher_River_CBet_4BP.txt").read_text(encoding="utf-8"),
    "router": (SRC / "CashCrusher_River_CBet.txt").read_text(encoding="utf-8"),
}


def block(text: str, name: str) -> str:
    marker = f"##{name}##"
    start = text.index(marker) + len(marker)
    tail = text[start:]
    nxt = tail.find("##")
    return tail if nxt < 0 else tail[:nxt]


def executable(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def main() -> None:
    # ISO: family9 and exact limper/coldcaller split, HU-from-MW retained.
    assert "f$cc_river_turn_family_id = 9" in block(FILES["iso_ctx"], "f$cc_river_iso_base_context")
    assert "f$cc_pf_pre_raise_limper_mask" in block(FILES["iso_ctx"], "f$cc_river_iso_hu_villain_is_limper")
    assert "f$cc_pf_post_raise_coldcaller_mask" in block(FILES["iso_ctx"], "f$cc_river_iso_hu_villain_is_coldcaller")
    assert "f$cc_river_turn_mw_now_hu" in block(FILES["iso_ctx"], "f$cc_river_iso_hu_from_mw_turn")
    assert "When f$cc_river_no_made Return false Force" in block(FILES["iso"], "f$cc_river_iso_hu_coldcaller_action")
    assert "f$cc_mw_spr_deepest_round_start" in block(FILES["iso_ctx"], "f$cc_river_iso_mw_all_effective_spr_below_1")

    # Plain3BP: family10, squeeze excluded, opener/coldcaller split.
    p3base = block(FILES["p3_ctx"], "f$cc_river_plain3bp_base_context")
    assert "f$cc_river_turn_family_id = 10" in p3base
    assert "!f$cc_pf_squeeze_proven" in p3base
    assert "f$cc_hu_3bp_villain_is_opener" in block(FILES["p3_ctx"], "f$cc_river_plain3bp_hu_vs_opener")
    assert "f$cc_hu_3bp_villain_is_post3bet_coldcaller" in block(FILES["p3_ctx"], "f$cc_river_plain3bp_hu_vs_coldcaller")
    assert "When f$cc_river_no_made Return false Force" in block(FILES["p3"], "f$cc_river_plain3bp_hu_coldcaller_action")

    # Squeeze: family11 and all three survivor origins remain distinct.
    sqbase = block(FILES["sq_ctx"], "f$cc_river_squeeze_base_context")
    assert "f$cc_river_turn_family_id = 11" in sqbase and "f$cc_pf_squeeze_proven" in sqbase
    for name, token in (
        ("f$cc_river_squeeze_hu_vs_opener", "f$cc_hu_3bp_villain_is_opener"),
        ("f$cc_river_squeeze_hu_vs_pre3bet", "f$cc_hu_3bp_villain_is_pre3bet_coldcaller"),
        ("f$cc_river_squeeze_hu_vs_post3bet", "f$cc_hu_3bp_villain_is_post3bet_coldcaller"),
    ):
        assert token in block(FILES["sq_ctx"], name)
    assert "When f$cc_river_no_made Return false Force" in block(FILES["sq"], "f$cc_river_squeeze_hu_pre3bet_action")
    assert "When f$cc_river_no_made Return false Force" in block(FILES["sq"], "f$cc_river_squeeze_hu_post3bet_action")

    # Clean 4BP: only same-HU Turn parent; exact subtype/survivor family preserved.
    p4base = block(FILES["p4_ctx"], "f$cc_river_4bp_base_context")
    assert "f$cc_river_turn_family_id = 12" in p4base
    assert "f$cc_river_turn_hu_still_hu" in p4base
    assert "f$cc_hu_4bp_survivor_type_id < 3" in p4base
    for name in (
        "f$cc_river_4bp_truehu_opener4_vs_threebettor",
        "f$cc_river_4bp_opener4_vs_threebettor",
        "f$cc_river_4bp_cold4_vs_opener",
        "f$cc_river_4bp_cold4_vs_threebettor",
    ):
        assert f"##{name}##" in FILES["p4_ctx"]

    # No strategy module blindly imports BetMax/legacy commitment shortcuts.
    for key in ("iso", "p3", "sq", "p4"):
        exe = executable(FILES[key])
        assert "BetMax" not in exe, f"BetMax leaked into {key} River strategy"
        assert "f$Raise_Committed" not in exe
        assert "f$allin_on_betsize_balance_ratio" not in exe

    # Multiway low-SPR helpers are deepest-effective only.
    for text, name in (
        (FILES["iso_ctx"], "f$cc_river_iso_mw_all_effective_spr_below_1"),
        (FILES["p3_ctx"], "f$cc_river_plain3bp_mw_all_effective_spr_below_1"),
        (FILES["sq_ctx"], "f$cc_river_squeeze_mw_all_effective_spr_below_1"),
    ):
        b = block(text, name)
        assert "f$cc_mw_spr_deepest_round_start" in b
        assert "shallowest" not in b.lower()

    # Router integrates all exact pot families after SRP branches.
    r = block(FILES["router"], "f$cc_river_cbet_router")
    expected = (
        "f$cc_river_iso_covered Return f$cc_river_iso_action Force",
        "f$cc_river_plain3bp_covered Return f$cc_river_plain3bp_action Force",
        "f$cc_river_squeeze_covered Return f$cc_river_squeeze_action Force",
        "f$cc_river_4bp_covered Return f$cc_river_4bp_action Force",
    )
    for token in expected:
        assert token in r

    size = block(FILES["router"], "f$cc_river_cbet_size_id")
    for token in ("f$cc_river_iso_size_id", "f$cc_river_plain3bp_size_id", "f$cc_river_squeeze_size_id", "f$cc_river_4bp_size_id"):
        assert token in size

    print("PASS: Gate03D-G ISO/3BP/squeeze/4BP River-CBet contracts")


if __name__ == "__main__":
    main()
