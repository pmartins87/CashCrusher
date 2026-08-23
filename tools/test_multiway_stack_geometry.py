#!/usr/bin/env python3
"""Deterministic contract tests for CashCrusher multiway stack geometry.

These tests do NOT pretend to execute OpenPPL/OpenHoldem. They validate the
mathematical contract that the OpenPPL implementation is required to preserve:

    shallowest effective = min(Hero, min(live opponent stacks))
    deepest effective    = min(Hero, max(live opponent stacks))

They also validate the narrow Gate 01K.3B distinction between:
- mechanically forced/equivalent all-in execution; and
- strategic near-all-in promotion, which remains a separate audit.

DeepCrusher's f$EffectiveStack_BKP uses the biggest active opponent, therefore
its multiway effective-stack ancestry maps to the *deepest* relation.
"""

from __future__ import annotations

from dataclasses import dataclass

EPS = 1e-9


@dataclass(frozen=True)
class Case:
    name: str
    hero: float
    opponents: tuple[float, ...]
    pot: float
    expected_shallow: float
    expected_deep: float
    expected_shallow_spr: float
    expected_deep_spr: float


def close(a: float, b: float) -> bool:
    return abs(a - b) <= EPS


def geometry(hero: float, opponents: tuple[float, ...], pot: float):
    assert hero >= 0
    assert opponents
    assert all(v >= 0 for v in opponents)
    assert pot > 0
    shallow = min(hero, min(opponents))
    deep = min(hero, max(opponents))
    return shallow, deep, shallow / pot, deep / pot


def requested_bet(pot: float, fraction: float) -> float:
    assert pot > 0
    assert fraction > 0
    return pot * fraction


def natural_allin_equivalent(
    hero: float,
    opponents: tuple[float, ...],
    requested: float,
) -> bool:
    """Mirror Gate 01K.3B mechanical/effective equivalence only."""
    assert hero > 0
    assert opponents
    assert requested >= 0
    deepest_effective = min(hero, max(opponents))
    reaches_hero = requested >= hero
    reaches_all_live_effective = requested >= deepest_effective
    return reaches_hero or reaches_all_live_effective


def sidepot_divergence(
    hero: float,
    opponents: tuple[float, ...],
    requested: float,
) -> bool:
    shallow = min(hero, min(opponents))
    deep = min(hero, max(opponents))
    return requested >= shallow and requested < deep


def main() -> int:
    cases = [
        Case(
            "equal_100bb",
            100,
            (100, 100),
            10,
            100,
            100,
            10,
            10,
        ),
        Case(
            "one_short_one_deep",
            100,
            (18, 100),
            10,
            18,
            100,
            1.8,
            10,
        ),
        Case(
            "hero_caps_deep_relation",
            40,
            (20, 100),
            10,
            20,
            40,
            2,
            4,
        ),
        Case(
            "hero_shorter_than_everyone",
            20,
            (100, 100),
            10,
            20,
            20,
            2,
            2,
        ),
        Case(
            "three_opponents_wide_span",
            80,
            (12, 45, 120),
            16,
            12,
            80,
            0.75,
            5,
        ),
        Case(
            "raised_pot_short_plus_deep",
            70,
            (20, 70),
            30,
            20,
            70,
            2 / 3,
            7 / 3,
        ),
    ]

    for case in cases:
        shallow, deep, shallow_spr, deep_spr = geometry(
            case.hero, case.opponents, case.pot
        )
        assert close(shallow, case.expected_shallow), case
        assert close(deep, case.expected_deep), case
        assert close(shallow_spr, case.expected_shallow_spr), case
        assert close(deep_spr, case.expected_deep_spr), case
        assert shallow <= deep + EPS, case
        assert deep <= case.hero + EPS, case

    # Invariant: if Hero is shortest, every effective relationship is identical.
    shallow, deep, *_ = geometry(15, (40, 100, 200), 10)
    assert close(shallow, 15)
    assert close(deep, 15)

    # Invariant: one short Villain must not lower the DeepCrusher-ancestry
    # deepest-effective denominator while another deeper Villain remains.
    shallow, deep, *_ = geometry(100, (20, 100), 50)
    bet = requested_bet(50, 0.75)  # 37.5bb
    assert bet / shallow >= 0.50  # shortest relation would falsely look committed
    assert bet / deep < 0.50      # deepest relation correctly does not trigger

    # Sidepot-divergence candidate: requested bet can cover the short opponent
    # while still being small relative to the deep opponent.
    hero = 100
    opponents = (5, 100)
    bet = requested_bet(10, 0.75)  # 7.5bb
    assert sidepot_divergence(hero, opponents, bet)
    assert not natural_allin_equivalent(hero, opponents, bet)

    # Reaching the deepest effective opponent makes the requested action already
    # effective-all-in versus the whole live field, even if Hero covers everyone.
    hero = 100
    opponents = (15, 35)
    bet = 35
    assert not sidepot_divergence(hero, opponents, bet)
    assert natural_allin_equivalent(hero, opponents, bet)

    # Hero-balance reach is mechanically all-in even when all opponents cover Hero.
    hero = 40
    opponents = (100, 120)
    bet = 40
    assert natural_allin_equivalent(hero, opponents, bet)

    # Near-all-in is deliberately NOT equivalent. A 60%-of-Hero-stack bet remains
    # a strategic promotion candidate, not a mechanical BetMax requirement.
    hero = 100
    opponents = (100, 100)
    bet = 60
    assert not natural_allin_equivalent(hero, opponents, bet)

    # Low-SPR relaxation must mean ALL live effective relations are low. Testing
    # deepest SPR is sufficient because it is the maximum of individual effective
    # SPRs under the common-pot denominator.
    _, _, shallow_spr, deep_spr = geometry(100, (15, 100), 10)
    assert shallow_spr < 2
    assert deep_spr >= 4
    assert not (deep_spr < 4)

    print(f"PASS: {len(cases)} deterministic multiway stack cases + all-in invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
