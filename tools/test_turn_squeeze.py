#!/usr/bin/env python3
"""Deterministic Gate02H source/routing tests for squeeze Turn CBet."""

from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CTX=(ROOT/"src"/"CashCrusher_Turn_Squeeze_Context.txt").read_text(encoding="utf-8")
POL=(ROOT/"src"/"CashCrusher_Turn_CBet_Squeeze.txt").read_text(encoding="utf-8")
ROUTER=(ROOT/"src"/"CashCrusher_Turn_CBet.txt").read_text(encoding="utf-8")

def block(text,name):
    marker=f"##{name}##"; start=text.index(marker)+len(marker); tail=text[start:]; n=tail.find("##"); return tail if n<0 else tail[:n]

def executable(text): return "\n".join(line.split("//",1)[0] for line in text.splitlines())

def main():
    base=block(CTX,"f$cc_turn_squeeze_context")
    assert "f$cc_pf_squeeze_proven" in base and "!f$cc_pf_3bet_plain_proven" in base
    for name,token in (
        ("f$cc_turn_squeeze_hu_vs_opener","f$cc_hu_3bp_villain_is_opener"),
        ("f$cc_turn_squeeze_hu_vs_pre3bet_coldcaller","f$cc_hu_3bp_villain_is_pre3bet_coldcaller"),
        ("f$cc_turn_squeeze_hu_vs_post3bet_coldcaller","f$cc_hu_3bp_villain_is_post3bet_coldcaller"),
    ):
        assert token in block(CTX,name)
    consistent=block(CTX,"f$cc_turn_squeeze_hu_context_consistent")
    assert "f$cc_turn_squeeze_hu_vs_opener + f$cc_turn_squeeze_hu_vs_pre3bet_coldcaller + f$cc_turn_squeeze_hu_vs_post3bet_coldcaller" in consistent
    mw=block(CTX,"f$cc_turn_squeeze_mw_context_consistent")
    assert "f$cc_mw_spr_bounds_valid" in mw
    assert "f$cc_turn_squeeze_mw_classified_count != (nplayersplaying - 1)" in mw
    exe=executable(POL)
    assert "BetMax" not in exe
    assert "f$cc_mw_spr_shallowest_round_start" not in exe
    pre=block(POL,"f$cc_turn_squeeze_hu_pre3bet_action")
    post=block(POL,"f$cc_turn_squeeze_hu_post3bet_action")
    assert "When f$cc_turn_cbet_air Return false Force" in pre
    assert "When f$cc_turn_cbet_air Return false Force" in post
    mwpol=block(POL,"f$cc_turn_squeeze_mw_action")
    assert "When f$cc_turn_cbet_air Return false Force" in mwpol
    assert "f$cc_turn_squeeze_mw_all_effective_spr_below_4" in mwpol
    route="When f$cc_turn_squeeze_covered Return f$cc_turn_squeeze_action Force"
    plain="When f$cc_turn_plain3bp_covered Return f$cc_turn_plain3bp_action Force"
    hu="When f$cc_turn_srp_ip_source_anchored_covered Return f$cc_turn_srp_ip_source_anchored_action Force"
    assert route in ROUTER and plain in ROUTER and hu in ROUTER
    assert ROUTER.index(route)<ROUTER.index(hu)
    assert "f$cc_turn_squeeze_size_id" in block(ROUTER,"f$cc_turn_cbet_size_id")
    print("PASS: Gate02H squeeze Turn-CBet source/routing contract")

if __name__=="__main__": main()
