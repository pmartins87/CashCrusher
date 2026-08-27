#!/usr/bin/env python3
"""Static semantic contract for current Gate02 Turn CBet implementation.

The global linter proves dependency/provenance/flat-WHEN safety. This test adds
high-value anti-leak assertions that encode source-boundary decisions which are
otherwise easy to regress while expanding six-max coverage.

It is not an OpenHoldem replay test.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

COMMON = (SRC / "CashCrusher_Turn_CBet_Common.txt").read_text(encoding="utf-8")
ROUTER = (SRC / "CashCrusher_Turn_CBet.txt").read_text(encoding="utf-8")
IP = (SRC / "CashCrusher_Turn_CBet_SRP_IP.txt").read_text(encoding="utf-8")
OOP = (SRC / "CashCrusher_Turn_CBet_SRP_OOP.txt").read_text(encoding="utf-8")
TEXTURE = (SRC / "CashCrusher_Turn_Texture.txt").read_text(encoding="utf-8")
HISTORY = (SRC / "CashCrusher_Flop_ActionHistory.txt").read_text(encoding="utf-8")


def main() -> int:
    # Turn CBet must be rooted in actual executed-flop history, not initiative alone.
    assert "f$cc_hist_turn_standard_cbet_parent" in COMMON
    assert "f$cc_hist_flop_cbet_runtime_mismatch Return false" in COMMON

    # Stored FLOP plan/provenance exists for source trees that need carried TP/BDSD.
    assert "Set user_cc_flop_cbet_had_top_pair" in HISTORY
    assert "Set user_cc_flop_cbet_had_overpair" in HISTORY
    assert "Set user_cc_flop_cbet_had_bdsd" in HISTORY
    assert "Set user_cc_flop_cbet_texture_dynamic_lowmid" in HISTORY

    # True HU and reduced HU source descendants remain distinct exact contexts.
    assert "f$cc_true_hu" in IP and "f$cc_hu_matchup_id = 56" in IP
    assert "f$cc_hu_origin_preflop_reduced" in IP
    assert "f$cc_hu_matchup_id = 46" in IP  # BTN v BB
    assert "f$cc_hu_matchup_id = 45" in IP  # BTN v SB
    assert "f$cc_hu_origin_preflop_reduced" in OOP
    assert "f$cc_hu_matchup_id = 56" in OOP  # SB v BB, origin disambiguates true HU

    # HUSB source-shaped air pressure card remains exact and mechanical.
    assert "##f$cc_turn_husb_air_pressure_card_source##" in TEXTURE
    assert "f$cc_flop_had_two_cards_2_to_6" in TEXTURE
    assert "!f$cc_turn_new_completion" in TEXTURE

    # BTN-v-SB source explicitly gives up flop draw/air CBet if still no-made.
    assert "user_cc_flop_cbet_had_premium_draw" in IP
    assert "user_cc_flop_cbet_had_quality_air" in IP
    assert "Return false Force" in IP

    # SB-v-BB source architecture: only explicit newly-straight-completing TP+
    # direct barrel is currently implemented; generic TP+ tail must check.
    assert "f$cc_hand_top_pair_or_better && f$cc_turn_new_straight_completion Return true Force" in OOP
    assert "When f$cc_hand_top_pair_or_better Return false Force" in OOP
    assert "f$cc_turn_size_100_id" in OOP

    # Historical short-stack threshold is source evidence, not a blanket Turn rule.
    for text in (IP, OOP, ROUTER):
        assert "f$EffectiveStack_BKP >= 20" not in text
        assert "f$StackPotRatio < 1.6" not in text

    # Current Turn strategy modules contain no silent all-in shortcut. This is a
    # local current-Gate invariant, not a global prohibition on future exact jams.
    for text in (IP, OOP, ROUTER):
        assert "BetMax" not in text
        assert "Return Allin" not in text
        assert "Return allin" not in text

    # Uncovered 6-max ranges/pot families cannot fall through to HUSB/BTN strategy.
    assert "##f$cc_turn_cbet_srp_ip_uncovered_range_context##" in ROUTER
    assert "##f$cc_turn_cbet_srp_oop_uncovered_context##" in ROUTER
    assert "When Others Return false Force" in ROUTER
    assert "When Others Return 0 Force" in ROUTER

    # Current router can only call explicitly covered source-anchored children.
    action_block = ROUTER.split("##f$cc_turn_cbet_router##", 1)[1].split("##", 1)[0]
    assert "f$cc_turn_srp_ip_source_anchored_covered" in action_block
    assert "f$cc_turn_srp_oop_source_anchored_covered" in action_block
    assert "f$cc_turn_cbet_iso_context Return" not in action_block
    assert "f$cc_turn_cbet_plain3bp_context Return" not in action_block
    assert "f$cc_turn_cbet_squeeze_context Return" not in action_block
    assert "f$cc_turn_cbet_4bp_context Return" not in action_block

    print("PASS: Gate02 Turn CBet source-boundary and anti-leak contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
