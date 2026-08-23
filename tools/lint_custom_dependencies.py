#!/usr/bin/env python3
"""Static linter for CashCrusher OpenPPL source.

CashCrusher deliberately uses a stricter coding/documentation subset than
OpenPPL technically permits.  The goal is to make semantic scope, source
provenance and short-stack review obligations visible in code rather than
relying on indentation or tribal knowledge.

Hard checks
===========
- unresolved ``f$cc_*`` references across ``src/*.txt``;
- duplicate ``##f$cc_*##`` definitions;
- legacy ``f$game_*`` dependencies in executable CashCrusher strategy code;
- **open-ended WHEN conditions**. Every WHEN must own an explicit action before
  the next WHEN/function boundary; indentation never creates scope;
- **every ``f$cc_*`` function must have a nearby Source/Provenance comment**.

Review warnings — NOT prohibitions
==================================
DeepCrusher was short-stack Spin strategy. The following constructs can be
correct in CashCrusher, but deserve explicit cash-stack review when imported:
- ``f$Raise_Committed``;
- ``f$hand_StackOffDraws``;
- ``f$allin_on_betsize_balance_ratio``;
- executable ``BetMax`` / ``Allin``.

The linter only WARNS about these constructs. It does not force them to zero,
disable them, or declare them invalid. Correctness depends on the exact pot
family, range provenance, board/runout, effective stack/SPR and action size.

Other warnings include custom definitions not referenced by executable code yet.
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
BETMAX_RE = re.compile(r"\b(?:BetMax|Allin)\b", re.IGNORECASE)
WHEN_RE = re.compile(r"\bWhen\b", re.IGNORECASE)

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
    """Find WHENs lacking an explicit action before next WHEN/boundary.

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
    """Require local source/provenance immediately around each custom function."""
    start = max(0, header_lineno - 10)
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
    shortstack_review_hits: list[tuple[Path, int, str]] = []
    allin_review_hits: list[tuple[Path, int, str]] = []
    callback_defs: list[tuple[Path, int]] = []
    open_when_hits: list[tuple[Path, int, str, str]] = []
    provenance_errors: list[tuple[Path, int, str]] = []

    for path in files:
        text = path.read_text(encoding="utf-8", errors="strict")
        lines = text.splitlines()
        blocks = list(function_blocks(lines))
        open_when_hits.extend(open_ended_when_hits(path, lines))

        for func_name, header_lineno, _body in blocks:
            if func_name == "f$allin_on_betsize_balance_ratio":
                callback_defs.append((path, header_lineno))

        for lineno, line in enumerate(lines, 1):
            stripped = line.strip()
            m = DEF_RE.fullmatch(stripped)
            if m:
                name = m.group(1)
                definitions[name].append((path, lineno))
                if not nearby_provenance(lines, lineno):
                    provenance_errors.append((path, lineno, name))
                continue

            code = executable_part(line)
            for ref in REF_RE.findall(code):
                references[ref].append((path, lineno))

            if LEGACY_GAME_RE.search(code):
                legacy_game_hits.append((path, lineno, code.strip()))
            if STACKOFF_RE.search(code) or RAISE_COMMITTED_RE.search(code):
                shortstack_review_hits.append((path, lineno, code.strip()))
            if BETMAX_RE.search(code):
                allin_review_hits.append((path, lineno, code.strip()))

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

    if open_when_hits:
        print("\nERROR: open-ended WHEN found (flat complete rules are mandatory):")
        for path, lineno, func_name, span in open_when_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno} [{func_name}]: {span}")

    if provenance_errors:
        print("\nERROR: custom function lacks nearby Source/Provenance comment:")
        for path, lineno, name in provenance_errors:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {name}")

    if shortstack_review_hits:
        print("\nWARNING: inherited short-stack helper used; cash-context review required:")
        for path, lineno, code in shortstack_review_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {code}")

    if callback_defs:
        print("\nWARNING: allin_on_betsize_balance_ratio is defined; verify threshold against CashCrusher stack geometry:")
        for path, lineno in callback_defs:
            print(f"  {path.relative_to(ROOT)}:{lineno}")

    if allin_review_hits:
        print("\nWARNING: explicit all-in action found; verify exact pot/range/SPR ownership:")
        for path, lineno, code in allin_review_hits:
            print(f"  {path.relative_to(ROOT)}:{lineno}: {code}")

    if unused:
        print("\nWARNING: custom definitions with no executable reference yet:")
        for name in unused:
            print(f"  {name}")

    hard_error = bool(
        duplicate_defs
        or unresolved
        or legacy_game_hits
        or open_when_hits
        or provenance_errors
    )
    if hard_error:
        return 1

    print("\nPASS: dependency, flat-WHEN, global provenance and safety checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
