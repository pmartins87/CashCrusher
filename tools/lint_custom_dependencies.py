#!/usr/bin/env python3
"""Static linter for CashCrusher OpenPPL source.

The linter encodes project-level OpenPPL safety rules carried from the audited
DeepCrusher work. CashCrusher deliberately uses a stricter coding subset than
OpenPPL technically permits so visual indentation or shallow-stack inheritance
cannot silently change strategy.

Hard checks
===========
- unresolved ``f$cc_*`` references across ``src/*.txt``;
- duplicate ``##f$cc_*##`` definitions;
- legacy ``f$game_*`` dependencies in executable CashCrusher code;
- reintroduction of ``f$hand_StackOffDraws``;
- reintroduction of legacy ``f$Raise_Committed`` call-to-shove promotion;
- any executable ``BetMax`` without a local ``ALLIN_OWNER_REVIEWED`` marker;
- any ``BetMax`` in current flop-CBet modules (Gate01 owns bet-size families,
  never an implicit flop jam);
- nonzero/rewritten ``f$allin_on_betsize_balance_ratio`` callback;
- **open-ended WHEN conditions**. Every WHEN must own an explicit action before
  the next WHEN/function boundary; indentation never creates scope;
- missing nearby Source/Provenance comment in reviewed strategic modules whose
  filename begins ``CashCrusher_Flop_CBet``.

Warnings
========
- function headers without nearby provenance comment in mechanical/supporting
  modules still undergoing retrofit;
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
ANY_FUNC_RE = re.compile(r"^##([^#]+)##\s*$")
REF_RE = re.compile(r"\bf\$cc_[A-Za-z0-9_]+\b")
LEGACY_GAME_RE = re.compile(r"\bf\$game_[A-Za-z0-9_]+\b")
STACKOFF_RE = re.compile(r"\bf\$hand_StackOffDraws\b")
RAISE_COMMITTED_RE = re.compile(r"\bf\$Raise_Committed\b")
BETMAX_RE = re.compile(r"\bBetMax\b")
WHEN_RE = re.compile(r"\bWhen\b", re.IGNORECASE)
ALLIN_OWNER_RE = re.compile(r"\bALLIN_OWNER_REVIEWED\b", re.IGNORECASE)

ACTION_RE = re.compile(
    r"\b(?:Return|Set|Check|Call|Fold|RaiseTo|RaiseBy|Raise|BetMax|Bet|Allin|"
    r"MinRaise|SitIn|SitOut|Leave|Prefold)\b",
    re.IGNORECASE,
)

PROVENANCE_RE = re.compile(
    r"\b(?:Provenance|Source|Fonte|Legacy parent|Source anchor)\b", re.IGNORECASE
)


def executable_part(line: str) -> str:
    """Drop ``//`` comments before policy/dependency checks."""
    return line.split("//", 1)[0]


def is_reviewed_strategy_module(path: Path) -> bool:
    """Modules where per-function provenance is already a release requirement."""
    return path.name.startswith("CashCrusher_Flop_CBet")


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
    """Find WHENs lacking an explicit action before the next WHEN/boundary.

    OpenPPL itself supports open-ended WHEN/backpatching. CashCrusher forbids it:
    each strategic rule must repeat/combine its complete predicate explicitly.
    """
    hits: list[tuple[Path, int, str, str]] = []

    for func_name, _header, body in function_blocks(lines):
        chunks: list[tuple[int, str]] = []
        for lineno, raw in body:
            code = executable_part(raw).strip()
            if code:
                chunks.append((lineno, code))
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

            source_line = chunks[0][0]
            for off, lineno in offset_to_line:
                if off <= start:
                    source_line = lineno
                else:
                    break
            hits.append((path, source_line, func_name, span.strip()[:220]))

    return hits


def nearby_provenance(lines: list[str], header_lineno: int) -> bool:
    """Check local pre-header comments for source/provenance."""
    start = max(0, header_lineno - 10)
    neighborhood = "\n".join(lines[start : header_lineno - 1])
    return bool(PROVENANCE_RE.search(neighborhood))


def function_has_allin_owner(lines: list[str], header_lineno: int, body: list[tuple[int, str]]) -> bool:
    """Require an explicit review marker near any function that returns BetMax."""
    start = max(0, header_lineno - 14)
    comments_before = "\n".join(lines[start : header_lineno - 1])
    body_text = "\n".join(raw for _lineno, raw in body)
    return bool(ALLIN_OWNER_RE.search(comments_before + "\n" + body_text))


def main() -> int:
    files = sorted(SRC.glob("*.txt"))
    if not files:
        print("ERROR: no src/*.txt files found")
        return 1

    definitions: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    references: dict[str, list[tuple[Path, int]]] = defaultdict(list)
    legacy_game_hits: list[tuple[Path, int, str]] = []
    stackoff_hits: list[tuple[Path, int, str]] = []
    raise_committed_hits: list[tuple[Path, int, str]] = []
    unowned_betmax_hits: list[tuple[Path, int, str]] = []
    cbet_betmax_hits: list[tuple[Path, int, str]] = []
    auto_commit_callback_hits: list[tuple[Path, int, str]] = []
    open_when_hits: list[tuple[Path, int, str, str]] = []
    provenance_errors: list[tuple[Path, int, str]] = []
    provenance_warnings: list[tuple[Path, int, str]] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="strict")
        lines = text.splitlines()
        blocks = list(function_blocks(lines))
        open_when_hits.extend(open_ended_when_hits(path, lines))

        for func_name, header_lineno, body in blocks:
            executable_body = "\n".join(executable_part(raw) for _ln, raw in body)

            if BETMAX_RE.search(executable_body) and not function_has_allin_owner(lines, header_lineno, body):
                unowned_betmax_hits.append((path, header_lineno, func_name))

            if func_name == "f$allin_on_betsize_balance_ratio":
                compact = " ".join(
                    executable_part(raw).strip() for _ln, raw in body if executable_part(raw).strip()
                )
                if compact not in {"0", "0.0", "0.00", "0.000"}:
                    auto_commit_callback_hits.append((path, header_lineno, compact))

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            m = DEF_RE.fullmatch(stripped)
            if m:
                name = m.group(1)
                definitions[name].append((path, lineno))
                if not nearby_provenance(lines, lineno):
                    target = provenance_errors if is_reviewed_strategy_module(path) else provenance_warnings
                    target.append((path, lineno, name))
                continue

            code = executable_part(line)
            for ref in REF_RE.findall(code):
                references[ref].append((path, lineno))

            if LEGACY_GAME_RE.search(code):
                legacy_game_hits.append((path, lineno, code.strip()))
            if STACKOFF_RE.search(code):
                stackoff_hits.append((path, lineno, code.strip()))
            if RAISE_COMMITTED_RE.search(code):
                raise_committed_hits.append((path, lineno, code.strip()))
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

    if raise_committed_hits:
        print("\nERROR: inherited f$Raise_Committed call-to-shove promotion reintroduced:")
        for path, lineno, code in raise_committed_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {code}")

    if unowned_betmax_hits:
        print("\nERROR: BetMax function lacks ALLIN_OWNER_REVIEWED marker:")
        for path, lineno, func_name in unowned_betmax_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {func_name}")

    if cbet_betmax_hits:
        print("\nERROR: BetMax found inside current flop-CBet strategy module:")
        for path, lineno, code in cbet_betmax_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {code}")

    if auto_commit_callback_hits:
        print("\nERROR: global allin_on_betsize_balance_ratio must remain disabled:")
        for path, lineno, body in auto_commit_callback_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {body}")

    if open_when_hits:
        print("\nERROR: open-ended WHEN found (flat complete rules are mandatory):")
        for path, lineno, func_name, span in open_when_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno} [{func_name}]: {span}")

    if provenance_errors:
        print("\nERROR: reviewed strategy function lacks nearby Source/Provenance comment:")
        for path, lineno, name in provenance_errors:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {name}")

    if provenance_warnings:
        print("\nWARNING: supporting function lacks nearby Source/Provenance comment:")
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
        or raise_committed_hits
        or unowned_betmax_hits
        or cbet_betmax_hits
        or auto_commit_callback_hits
        or open_when_hits
        or provenance_errors
    )
    if hard_error:
        return 1

    print("\nPASS: dependency, flat-WHEN, explicit-allin, provenance and safety checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
