#!/usr/bin/env python3
"""Static linter for CashCrusher OpenPPL source.

Hard checks:
- unresolved ``f$cc_*`` references across src/*.txt;
- duplicate ``##f$cc_*##`` definitions;
- legacy positional game-router dependencies (``f$game_*``) in executable
  CashCrusher code;
- reintroduction of the inherited ``f$hand_StackOffDraws`` shortcut;
- accidental BetMax use in the current flop-CBet modules, where Gate01 policy
  is explicitly sizing-family based and must not auto-jam.

Warnings:
- custom definitions not referenced by other executable lines yet.

Native OpenHoldem/OpenPPL symbols are outside dependency resolution by design.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

DEF_RE = re.compile(r"^##(f\$cc_[A-Za-z0-9_]+)##\s*$")
REF_RE = re.compile(r"\bf\$cc_[A-Za-z0-9_]+\b")
LEGACY_GAME_RE = re.compile(r"\bf\$game_[A-Za-z0-9_]+\b")
STACKOFF_RE = re.compile(r"\bf\$hand_StackOffDraws\b")
BETMAX_RE = re.compile(r"\bBetMax\b")


def executable_part(line: str) -> str:
    """Drop // comments before policy/dependency checks."""
    return line.split("//", 1)[0]


def main() -> int:
    files = sorted(SRC.glob("*.txt"))
    if not files:
        print("ERROR: no src/*.txt files found")
        return 1

    definitions: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    references: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    legacy_game_hits: list[tuple[Path, int, str]] = []
    stackoff_hits: list[tuple[Path, int, str]] = []
    cbet_betmax_hits: list[tuple[Path, int, str]] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="strict")
        lines = text.splitlines()

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            m = DEF_RE.fullmatch(stripped)
            if m:
                definitions[m.group(1)].append((path, lineno))
                # Function markers are definitions, not references.
                continue

            code = executable_part(line)
            for ref in REF_RE.findall(code):
                references[ref].append((path, lineno))

            if LEGACY_GAME_RE.search(code):
                legacy_game_hits.append((path, lineno, code.strip()))
            if STACKOFF_RE.search(code):
                stackoff_hits.append((path, lineno, code.strip()))
            if path.name.startswith("CashCrusher_Flop_CBet") and BETMAX_RE.search(code):
                cbet_betmax_hits.append((path, lineno, code.strip()))

    duplicate_defs = {k: v for k, v in definitions.items() if len(v) > 1}
    unresolved = {k: v for k, v in references.items() if k not in definitions}
    unused = sorted(name for name in definitions if name not in references)

    print("CashCrusher static strategy lint")
    print(f"files: {len(files)}")
    print(f"custom definitions: {len(definitions)}")
    print(f"custom referenced names: {len(references)}")

    if duplicate_defs:
        print("\nERROR: duplicate f$cc definitions:")
        for name, locs in sorted(duplicate_defs.items()):
            joined = ", ".join(f"{p.relative_to(ROOT)}:{n}" for p, n in locs)
            print(f"  {name}: {joined}")

    if unresolved:
        print("\nERROR: unresolved f$cc references:")
        for name, locs in sorted(unresolved.items()):
            preview = ", ".join(f"{p.relative_to(ROOT)}:{n}" for p, n in locs[:8])
            if len(locs) > 8:
                preview += f", ... (+{len(locs)-8})"
            print(f"  {name}: {preview}")

    if legacy_game_hits:
        print("\nERROR: legacy f$game_* dependency in executable CashCrusher code:")
        for path, lineno, code in legacy_game_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {code}")

    if stackoff_hits:
        print("\nERROR: inherited StackOffDraws shortcut reintroduced:")
        for path, lineno, code in stackoff_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {code}")

    if cbet_betmax_hits:
        print("\nERROR: BetMax found inside current flop-CBet strategy module:")
        for path, lineno, code in cbet_betmax_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {code}")

    if unused:
        print("\nWARNING: custom definitions with no executable reference yet:")
        for name in unused:
            print(f"  {name}")

    hard_error = bool(
        duplicate_defs
        or unresolved
        or legacy_game_hits
        or stackoff_hits
        or cbet_betmax_hits
    )
    if hard_error:
        return 1

    print("\nPASS: dependency and current strategy-safety checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
