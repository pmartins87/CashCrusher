#!/usr/bin/env python3
"""Static linter for CashCrusher OpenPPL source.

This linter intentionally encodes project-level OpenPPL safety rules learned
from the DeepCrusher audit.  The most important one is that CashCrusher strategy
must be written as FLAT, COMPLETE WHEN rules.  OpenPPL does not create logical
scope from indentation.  Therefore a visually indented ``WHEN parent`` followed
by child WHENs is dangerous: the parser treats the first WHEN as an open-ended
condition and its scope is determined by token order/back-patching, not by tabs
or spaces.

Hard checks
===========
- unresolved ``f$cc_*`` references across ``src/*.txt``;
- duplicate ``##f$cc_*##`` definitions;
- legacy positional game-router dependencies (``f$game_*``) in executable
  CashCrusher code;
- reintroduction of the inherited ``f$hand_StackOffDraws`` shortcut;
- accidental ``BetMax`` use in current flop-CBet modules, where Gate01 policy
  is explicitly sizing-family based and must not auto-jam;
- **open-ended WHEN conditions** in CashCrusher source.  Every WHEN must own an
  explicit action before the next WHEN/function boundary.  Strategic scope must
  be expressed by repeating/combining the full predicate on each rule, never by
  indentation.

Warnings
========
- custom definitions not referenced by other executable lines yet;
- function headers without a nearby provenance comment.  This remains warning
  only while the first modules are being retrofitted, but all newly reviewed
  strategy functions are expected to carry explicit source/provenance comments.

Native OpenHoldem/OpenPPL symbols are outside dependency resolution by design.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

DEF_RE = re.compile(r"^##(f\$cc_[A-Za-z0-9_]+)##\s*$")
ANY_FUNC_RE = re.compile(r"^##([^#]+)##\s*$")
REF_RE = re.compile(r"\bf\$cc_[A-Za-z0-9_]+\b")
LEGACY_GAME_RE = re.compile(r"\bf\$game_[A-Za-z0-9_]+\b")
STACKOFF_RE = re.compile(r"\bf\$hand_StackOffDraws\b")
BETMAX_RE = re.compile(r"\bBetMax\b")
WHEN_RE = re.compile(r"\bWhen\b", re.IGNORECASE)

# Every CashCrusher WHEN is required to be terminal on its own rule.  The action
# may live on the following physical line, therefore the scanner works on the
# token span between this WHEN and the next WHEN/function boundary.
#
# ``Set`` is an action in OpenPPL even though execution continues afterwards.
# Direct poker actions are included for future top-level formula integration.
ACTION_RE = re.compile(
    r"\b(?:Return|Set|Check|Call|Fold|RaiseTo|RaiseBy|Raise|BetMax|Bet|Allin|"
    r"MinRaise|SitIn|SitOut|Leave|Prefold)\b",
    re.IGNORECASE,
)

PROVENANCE_RE = re.compile(r"\b(?:Provenance|Source|Fonte|Legacy parent|Source anchor)\b", re.IGNORECASE)


def executable_part(line: str) -> str:
    """Drop ``//`` comments before policy/dependency checks."""
    return line.split("//", 1)[0]


def function_blocks(lines: list[str]):
    """Yield ``(name, header_line, body_lines)`` for every function/list block."""
    current_name: str | None = None
    current_header = 0
    current_body: list[tuple[int, str]] = []

    for lineno, line in enumerate(lines, 1):
        m = ANY_FUNC_RE.fullmatch(line.strip())
        if m:
            if current_name is not None:
                yield current_name, current_header, current_body
            current_name = m.group(1)
            current_header = lineno
            current_body = []
            continue
        if current_name is not None:
            current_body.append((lineno, line))

    if current_name is not None:
        yield current_name, current_header, current_body


def open_ended_when_hits(path: Path, lines: list[str]):
    """Find WHENs that have no explicit action before the next WHEN/boundary.

    This intentionally rejects valid-but-risky OpenPPL open-ended WHEN syntax.
    CashCrusher's coding contract is stricter than the parser: conditions are
    flattened so indentation can never change or obscure logical ownership.
    """
    hits: list[tuple[Path, int, str, str]] = []

    for func_name, _header, body in function_blocks(lines):
        # Build one executable string while retaining source-line ownership for
        # the first token on each physical line.
        chunks: list[tuple[int, str]] = []
        for lineno, raw in body:
            code = executable_part(raw).strip()
            if code:
                chunks.append((lineno, code))

        # Each physical code line becomes a sentinel-separated segment.  We do
        # not treat newlines as scope; they only help report the offending line.
        if not chunks:
            continue

        joined_parts: list[str] = []
        offset_to_line: list[tuple[int, int]] = []
        offset = 0
        for lineno, code in chunks:
            offset_to_line.append((offset, lineno))
            joined_parts.append(code)
            offset += len(code) + 1
        joined = " ".join(joined_parts)

        whens = list(WHEN_RE.finditer(joined))
        for idx, match in enumerate(whens):
            start = match.start()
            end = whens[idx + 1].start() if idx + 1 < len(whens) else len(joined)
            span = joined[start:end]
            if ACTION_RE.search(span):
                continue

            # Find the closest physical source line whose offset is <= token.
            source_line = chunks[0][0]
            for off, lineno in offset_to_line:
                if off <= start:
                    source_line = lineno
                else:
                    break
            hits.append((path, source_line, func_name, span.strip()[:220]))

    return hits


def nearby_provenance(lines: list[str], header_lineno: int) -> bool:
    """Return true when the immediately preceding comment neighborhood names source/provenance.

    Mechanical one-line aliases can share a section-level source comment, so the
    search window is intentionally small but not restricted to the adjacent line.
    """
    start = max(0, header_lineno - 9)
    neighborhood = "\n".join(lines[start : header_lineno - 1])
    return bool(PROVENANCE_RE.search(neighborhood))


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
    open_when_hits: list[tuple[Path, int, str, str]] = []
    provenance_warnings: list[tuple[Path, int, str]] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="strict")
        lines = text.splitlines()

        open_when_hits.extend(open_ended_when_hits(path, lines))

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            m = DEF_RE.fullmatch(stripped)
            if m:
                name = m.group(1)
                definitions[name].append((path, lineno))
                if not nearby_provenance(lines, lineno):
                    provenance_warnings.append((path, lineno, name))
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

    if open_when_hits:
        print("\nERROR: open-ended WHEN found (CashCrusher requires flat complete rules):")
        for path, lineno, func_name, span in open_when_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno} [{func_name}]: {span}")

    if provenance_warnings:
        print("\nWARNING: function header without nearby Source/Provenance comment:")
        for path, lineno, name in provenance_warnings:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {name}")

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
        or open_when_hits
    )
    if hard_error:
        return 1

    print("\nPASS: dependency, flat-WHEN and current strategy-safety checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
