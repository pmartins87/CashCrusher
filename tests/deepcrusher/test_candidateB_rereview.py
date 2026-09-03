from pathlib import Path
import hashlib
import re
import difflib
import sys

BASE = Path("DeepCrusher_GOOD_RESULTS_BASELINE_20260903_SHA26302fa1.txt")
CAND = Path("DeepCrusher_CandidateB_Rereview_20260903.txt")
EXPECTED_BASE = "26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blocks(text: str) -> list[str]:
    return re.findall(r"^##([^\n#]+)##\s*$", text, re.M)


def executable_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    ]


def main() -> None:
    b = BASE.read_text(encoding="utf-8")
    c = CAND.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    def ck(name: str, condition: bool, detail: str = "") -> None:
        checks.append((name, bool(condition), detail))

    ck("baseline_sha_frozen", sha(BASE) == EXPECTED_BASE, sha(BASE))
    ck("candidate_distinct", sha(CAND) != EXPECTED_BASE, sha(CAND))
    ck("same_block_sequence", blocks(b) == blocks(c), f"{len(blocks(b))} blocks")
    ck("no_duplicate_blocks_candidate", len(blocks(c)) == len(set(blocks(c))))
    ck(
        "stale_priority_comment_removed",
        "Priority: user_hardcoded.cpp 2026 corrections > explicit Framework5 rules > CrusherTBP mature baseline."
        not in c,
    )

    start = c.index("##f$move_turn_Delayed_FloatBet##")
    end = c.find("\n##", start + 5)
    block = c[start : end if end != -1 else len(c)]

    ck(
        "12B_generic_fallback_excludes_HUSB",
        "When !f$game_3wBBvSB && !f$game_HUSB Return true Force" in block,
    )
    producer = (
        "When AmountToCall = 0 && !user_Flop_Init_Hero && !f$flop_Raise && "
        "f$game_HUSB && user_GotIsolated && f$CF7_MediumMade "
        "Set user_DC12B_HUSB_FlopMediumMadeCheck"
    )
    ck("HUSB_medium_made_producer_exists", producer in c)

    generic = block.index("When !f$game_3wBBvSB && !f$game_HUSB Return true Force")
    detail = block.index(
        "When f$game_HUSB && user_DC12B_HUSB_FlopMediumMadeCheck && "
        "(f$CF7_NutClass || f$CF7_TwoPairPlus) Set user_Turn75"
    )
    ck(
        "no_early_HUSB_blanket_block",
        "When f$game_HUSB Return false Force" not in block[generic:detail],
    )
    ck(
        "HUSB_2Pplus_turn75",
        "user_DC12B_HUSB_FlopMediumMadeCheck && "
        "(f$CF7_NutClass || f$CF7_TwoPairPlus) Set user_Turn75" in block,
    )
    ck(
        "HUSB_TP_OP_turn50",
        "user_DC12B_HUSB_FlopMediumMadeCheck && "
        "(f$CF7_TopPairReal || f$CF7_OverPairReal) Set user_Turn50" in block,
    )
    ck(
        "HUSB_unchanged_medium_checks",
        "When f$game_HUSB && user_DC12B_HUSB_FlopMediumMadeCheck Return false Force"
        in block,
    )

    bx, cx = executable_lines(b), executable_lines(c)
    delta = [x for x in difflib.ndiff(bx, cx) if x[:2] in ("- ", "+ ")]
    ck("executable_delta_small", len(delta) <= 3, repr(delta))
    ck(
        "HUSB_false_count_decreased_by_one",
        bx.count("When f$game_HUSB Return false Force")
        == cx.count("When f$game_HUSB Return false Force") + 1,
    )

    for left, right, name in [("(", ")", "paren"), ("[", "]", "bracket"), ("{", "}", "brace")]:
        base_delta = b.count(left) - b.count(right)
        cand_delta = c.count(left) - c.count(right)
        ck(f"{name}_imbalance_preserved", base_delta == cand_delta)

    passed = sum(ok for _, ok, _ in checks)
    print(f"CandidateB static regression: {passed}/{len(checks)} PASS")
    for name, ok, detail in checks:
        print("PASS" if ok else "FAIL", name, detail)
    if passed != len(checks):
        sys.exit(1)


if __name__ == "__main__":
    main()
