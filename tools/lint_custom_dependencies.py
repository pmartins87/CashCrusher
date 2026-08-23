#!/usr/bin/env python3
"""Static linter for CashCrusher custom OpenPPL symbols.

Checks only the project namespace ``f$cc_*``. Native OpenHoldem/OpenPPL symbols
and legacy source symbols are intentionally outside this linter's scope.

It detects:
- unresolved ``f$cc_*`` references across src/*.txt;
- duplicate ``##f$cc_*##`` function definitions;
- definitions that are never referenced (warning only).

Exit code 1 means a hard dependency error.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

DEF_RE = re.compile(r"^##(f\$cc_[A-Za-z0-9_]+)##\s*$", re.MULTILINE)
REF_RE = re.compile(r"\bf\$cc_[A-Za-z0-9_]+\b")


def main() -> int:
    files = sorted(SRC.glob("*.txt"))
    if not files:
        print("ERROR: no src/*.txt files found")
        return 1

    definitions: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    references: dict[str, list[tuple[Path, int]]] = defaultdict(list)

    for path in files:
        text = path.read_text(encoding="utf-8", errors="strict")
        lines = text.splitlines()

        for lineno, line in enumerate(lines, 1):
            m = re.fullmatch(r"##(f\$cc_[A-Za-z0-9_]+)##\s*", line.strip())
            if m:
                definitions[m.group(1)].append((path, lineno))

            # Remove comments before collecting references. This prevents a
            # documentation mention from manufacturing a fake dependency.
            code = line.split("//", 1)[0]
            for ref in REF_RE.findall(code):
                references[ref].append((path, lineno))

    duplicate_defs = {k: v for k, v in definitions.items() if len(v) > 1}
    unresolved = {k: v for k, v in references.items() if k not in definitions}

    # A definition line contains its own name, so subtract those self-hits when
    # estimating unused functions.
    referenced_names = set(references)
    unused = sorted(name for name in definitions if name not in referenced_names)

    print(f"CashCrusher custom dependency lint")
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
            preview = ", ".join(
                f"{p.relative_to(ROOT)}:{n}" for p, n in locs[:8]
            )
            if len(locs) > 8:
                preview += f", ... (+{len(locs)-8})"
            print(f"  {name}: {preview}")

    if unused:
        print("\nWARNING: custom definitions with no code reference yet:")
        for name in unused:
            print(f"  {name}")

    if duplicate_defs or unresolved:
        return 1

    print("\nPASS: no duplicate or unresolved f$cc dependencies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
