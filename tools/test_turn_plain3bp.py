#!/usr/bin/env python3
"""Deterministic Gate02G source/routing tests for plain-3BP Turn CBet."""

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CTX = (ROOT / "src" / "CashCrusher_Turn_3BP_Context.txt").read_text(encoding="utf-8")
POL = (ROOT / "src" / "CashCrusher_Turn_CBet_3BP.txt").read_text(encoding="utf-8")
ROUTER = (ROOT / "src" / "CashCrusher_Turn_CBet.txt").read_text(encoding="utf-8")

def block(text, name):
    marker=f"##{name}##"; start=text.index(marker)+len(marker); tail=text[start:]; nxt=tail.find("##"); return tail if nxt<0 else tail[:nxt]

def executable(text): return "\n".join(x.split("//",1)[0] for x in text.splitlines())

def main():
    assert "!f$cc_pf_squeeze_proven" in block(CTX,"f$cc_turn_plain3bp_context")
    assert "f$cc_hu_3bp_villain_is_opener" in block(CTX,"f$cc_turn_plain3bp_hu_vs_opener")
    assert "f$cc_hu_3bp_villain_is_post3bet_coldcaller" in block(CTX,"f$cc_turn_plain3bp_hu_vs_coldcaller")
    assert "f$cc_hu_origin_postflop_reduced" in block(CTX,"f$cc_turn_plain3bp_hu_postmw_origin")
    mw=block(CTX,"f$cc_turn_plain3bp_mw_context_consistent")
    assert "f$cc_mw_spr_bounds_valid" in mw
    exe=executable(POL)
    assert "BetMax" not in exe
    assert "f$cc_mw_spr_shallowest_round_start" not in exe
    cold=block(POL,"f$cc_turn_plain3bp_hu_coldcaller_action")
    assert "When f$cc_turn_cbet_air Return false Force" in cold
    mwpol=block(POL,"f$cc_turn_plain3bp_mw_action")
    assert "When f$cc_turn_cbet_air Return false Force" in mwpol
    route="When f$cc_turn_plain3bp_covered Return f$cc_turn_plain3bp_action Force"
    iso="When f$cc_turn_iso_covered Return f$cc_turn_iso_action Force"
    hu="When f$cc_turn_srp_ip_source_anchored_covered Return f$cc_turn_srp_ip_source_anchored_action Force"
    assert route in ROUTER and iso in ROUTER and hu in ROUTER
    assert ROUTER.index(route) < ROUTER.index(hu)
    assert "f$cc_turn_plain3bp_size_id" in block(ROUTER,"f$cc_turn_cbet_size_id")
    print("PASS: Gate02G plain-3BP Turn-CBet source/routing contract")

if __name__ == "__main__": main()
