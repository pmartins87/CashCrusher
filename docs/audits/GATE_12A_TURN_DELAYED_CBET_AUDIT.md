# Gate 12A — Turn Delayed CBet Audit

## Status

**CLOSED at the static/deterministic strategy + runtime layer.**

Final validated checkpoint before this audit document:

- branch: `gate-00-context-engine`
- commit: `53f23cc99bf39874a8c3014bdaae1fc720f31bc2`
- GitHub Actions push run: **#1259**
- run id: `32926478303`
- result: **SUCCESS**

Table/OpenHoldem replay certification remains a later global integration concern; this closure does not claim table certification.

## Canonical ownership

Gate12A owns a Turn first-action bet only when Hero owned supported preflop initiative, Hero did **not** bet the flop, the complete flop checked through cleanly, and Hero reaches Turn with `AmountToCall = 0`. A strategy child never manufactures ownership.

This separates Delayed CBet from Turn Probe, Turn Float and Gate12B Delayed Float. The central historical invariant is the executed flop X/X...X line, not a pre-action plan marker.

## Source hierarchy

The implementation follows the project precedence rule:

1. **T** — direct source mechanics/rules where the original Crusher/DeepCrusher source defines the state;
2. **A** — high-ancestry translation of source concepts where literal scenario copying is unsafe in six-max cash;
3. **P** — deterministic professional cash adaptation only where source coverage is silent;
4. unknown or unprovable state — **fail closed**.

No generic `HandPower`, `random`, `BetMax`, commitment shortcut or TP+ stackoff fallback was introduced.

## Reviewed strategy families

The canonical router contains 17 mutually exclusive child IDs:

| ID | Family | Provenance level |
|---:|---|---|
| 1 | HUSB | T/A direct-source descendant |
| 2 | HUBB | T/A direct-source descendant |
| 3 | 3wBTNvBB | T/A direct-source descendant |
| 4 | 3wBTNvSB | T/A direct-source descendant |
| 5 | 3wBBvSB | T/A direct-source descendant |
| 6 | 3wSBvBB | T/A direct-source descendant |
| 7 | 3wBTNv2p | A/TBP reviewed gap fill + explicit checks |
| 8 | 3wBlinds-v-BTN | T reviewed source check |
| 9 | 4–6h ordinary SRP reduced-HU | P-heavy, source-ancestry constrained |
| 10 | 4–6h ordinary SRP current-multiway | P-heavy, source-ancestry constrained |
| 11 | proven ISO reduced-HU | P-heavy, range-origin aware |
| 12 | proven ISO current-multiway | P-heavy, range-origin aware |
| 13 | 4–6h plain 3BP reduced-HU | P-heavy, survivor-origin aware |
| 14 | 4–6h plain 3BP current-multiway | P-heavy, survivor-origin aware |
| 15 | 4–6h squeeze reduced-HU | P-heavy, opener/pre3bet/post3bet aware |
| 16 | 4–6h squeeze current-multiway | P-heavy, composition aware |
| 17 | clean 4–6h HU 4BP | P-heavy, exact subtype/survivor aware |

Owner-count consistency requires exactly one child whenever strategy is marked covered.

## Six-max adaptation boundaries

### Ordinary SRP

4–6 handed SRP is adapted separately for reduced-HU and current-multiway states. Pure-air delayed barrels are not created without audited skipped-flop bluff provenance. Current hand strength, position, draw quality and dangerous Turn runouts drive the P-heavy branches.

### ISO

Original pre-raise limpers and post-raise coldcallers remain different range origins. HU and multiway fields are separate. Contradictory or incomplete survivor masks fail closed.

### Plain 3BP and squeeze

Plain 3BP and squeeze never share one generic child. The implementation preserves original opener, pre-3bet coldcaller and post-3bet coldcaller provenance. Squeeze multiway policy is intentionally tighter than plain-3BP multiway policy.

### 4BP

Only mechanically clean 4–6h HU 4BP families are covered: supported opener4/cold4 chronology with an exact original opener or original 3bettor survivor. Multiway 4BP, `othercaller` survivor, reversed/backraise/limp-reraise chronology and 5bet+ remain explicit unresolved/fail-closed states pending stronger evidence.

## Sizing and runtime

The strategic size palette is:

- source MIN (`BetMin`, modeled as 1bb for stack geometry);
- A/P 33% (`BetThirdPot`);
- 50% (`BetHalfPot`);
- exact 62.5% (`RaiseBy 62.5%`);
- 75% (`BetThreeFourthPot`);
- 100% (`BetPot`);
- exact 150% (`RaiseBy 150%`).

The runtime adapter preserves exact source sizes rather than rounding 62.5% or 150%. Unknown size IDs execute nothing.

The stack-geometry layer measures Hero-stack, HU-effective, multiway-shallowest and multiway-deepest reach. Shortest-only multiway reach is labeled as a possible sidepot divergence and cannot promote the whole action.

**Gate12A deliberately has no runtime all-in promotion.** A requested bet may naturally touch a stack boundary, but that fact is diagnostic and does not import historical 50/55/60 commitment thresholds or create `BetMax`.

## Validation

CI #1259 validates the complete pre-existing attack regression plus Gate12A:

- source/native delayed-CBet descendants;
- 3w reviewed gaps;
- 4–6h ordinary SRP;
- ISO;
- plain 3BP;
- squeeze;
- clean HU 4BP;
- 17-family coverage/exclusivity and fail-closed boundaries;
- exact runtime sizing;
- stack geometry and no-all-in-promotion invariant;
- global custom-dependency/provenance lint.

The immediately preceding failed run was caused only by a brittle `.endswith()` assertion in the new coverage test. The strategy/runtime implementation itself passed; the assertion was corrected to inspect executable content, after which #1259 completed successfully.

## Known exclusions carried forward

Gate12A closure intentionally does **not** resolve:

- multiway 4BP Delayed CBet;
- 4BP `othercaller` survivor;
- reversed/backraise/limp-reraise 4BP;
- 5bet+ postflop families;
- whole-bot `f$turn` / `f$BestBetsize` composition;
- OpenHoldem parser/replay certification.

These exclusions are evidence boundaries, not silent fallbacks.

## Next attack node

**Gate12B — Turn Delayed Float / no-initiative delayed bet** is next. It must be kept separate from Gate12A because Hero did not own flop initiative. The Framework/TBP routing explicitly distinguishes the two histories, and source-first reconstruction begins from that ownership split.
