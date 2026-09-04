# DeepCrusher Strategic Source Policy

Status: **BINDING** for every DeepCrusher strategic review or modification.

Last updated: 2026-09-03.

## 1. Core rule

No strategic source is to be followed blindly. Every material rule must be checked in context against the available sources and against the actual executable OpenPPL flow.

The intended evidence process is:

1. **Crusher Starting Strategy** — the written/original strategic source establishes the intended poker plan, terminology and scenario logic.
2. **CrusherTBP** — the repeatedly human-reviewed implementation is the primary implementation/interpretation of the written strategy and the preferred source for resolving coding/generalization details, but it must still be checked against the written source and actual runtime scope.
3. **user_hardcoded.cpp** — AI-assisted C++ implementation used as secondary evidence, cross-check and detail source; it does not automatically override the written strategy or CrusherTBP.
4. **Professional poker theory** — used to fill genuine gaps, evaluate whether a generalization is strategically reasonable, or help reconcile inconsistent material. Theory-derived rules must be explicitly identified as such.

When the sources agree, implement the strongest faithful generalization rather than a one-hand patch. When they materially conflict and reconciliation is not sufficiently reliable, record the conflict for user decision instead of silently choosing one source.

## 2. Executable semantics over labels

Function names, labels and comments are evidence, not the definition of runtime scope. Before changing a rule, trace the executable path that can reach it.

Required trace where relevant:

`pot classifier -> preflop/history state -> initiative -> scenario -> position -> sizing bucket -> exceptional geometry/price helpers -> raise/call router -> strategic node -> sizing helper -> final action`

Example already confirmed in the legacy runtime: a pot created by `SB limp -> Hero BB raise -> SB call` can execute through the **SingleRaised/SRP** family because Hero raised and no opponent raised, even though `user_did_ISO` also records the isolation history. Therefore `SRP`, `ISO`, `limped` and similar names must never be treated as mutually exclusive merely from their labels.

## 3. Provenance required in code

Every new or materially modified strategic rule must document its provenance and real scope. Use one or more of:

- `SOURCE: STARTING_STRATEGY`
- `SOURCE: CRUSHERTBP`
- `SOURCE: USER_HARDCODED`
- `SOURCE: PRO_THEORY`
- `SOURCE: RECONCILED`

A `RECONCILED` comment must briefly state which sources were combined or why one literal implementation was narrowed/rejected.

Comments must describe the **actual executable scope**, not only the historical name of the source node.

## 4. Comments are part of the audit

A code review includes review of comments. Stale comments about source priority, scope, sizing, history or precedence must be corrected in the same change that corrects the logic.

No comment may claim a source priority that contradicts this policy.

## 5. Baseline safety

The frozen 2026-09-03 DeepCrusher good-results baseline must never be overwritten. Improvements are developed in separate candidates and compared against the frozen baseline.

A known-good-results baseline is not a claim of strategic perfection. A new candidate is not promoted merely because it appears theoretically cleaner; it must preserve intended source behavior and pass regression/runtime validation.

## 6. Material errors versus deliberate margins

Small numerical differences are **not errors by themselves**. Thresholds such as written `50%` implemented near `52%`, or `75%` represented near `76%`, may deliberately provide operational tolerance, bucket separation, scraper robustness or a practical margin.

Do not spend review effort literalizing a threshold merely because two sources differ by a few percentage points. Preserve an existing small margin unless there is concrete evidence that it creates a material strategic problem.

Escalate or change sizing thresholds only when the difference causes a meaningful and unsupported change of strategy — for example a broad class changing from CALL/RAISE to FOLD solely because routing crosses a generic bucket boundary — or when the sources clearly show that the numerical distinction itself is strategically intentional.

The audit target is material poker behavior: grossly wrong actions, lost scenario rules, scope leaks, precedence faults, unreachable code, excessive generic restrictions, or unsupported action cliffs.

## 7. Exceptional geometry and price have legitimate precedence

The written Crusher strategy generally describes the ordinary strategic tree unless it explicitly states an exceptional stack/price state. It does not enumerate every short-stack, effectively committed, all-in-adjacent, or abnormally tiny-bet geometry at every node.

Therefore do **not** apply a normal source action literally when runtime has entered an explicit exceptional helper state merely because the source says CALL/FOLD in the ordinary node.

### `f$Raise_Committed`

`f$Raise_Committed` is an intentional exceptional stack-geometry helper. Its purpose is to complete all-in when the ordinary strategy already wants to continue and the remaining effective stack is economically trivial. A normal source CALL does not automatically prohibit this conversion.

Default precedence for new/reconciled rules is:

`f$Raise_Committed -> scenario-specific normal strategy -> generic scenario fallback`

Only override or bypass commitment when there is **specific evidence about the committed geometry itself** showing that the helper action is materially wrong. A normal-stack line from Starting Strategy is not sufficient evidence by itself.

### `f$Call_MicroBets`

`f$Call_MicroBets` is an intentional extreme-price exception. A normal-price source fold/call should not automatically suppress it. Preserve microbet precedence unless the source explicitly covers that tiny sizing or the helper itself is shown to make a materially bad call.

### General rule

Before overriding any global helper, ask whether the helper represents a real exceptional game state that the written source did not intend to enumerate. Judge that state with poker logic, stack/pot geometry, source material and runtime semantics together.

Exceptional helpers are not immune from review. They simply are not defects merely because they differ from an ordinary source action.

## 8. Prohibited review shortcuts

Do not:

- infer strategy from a function name without tracing its callers and state conditions;
- invent kicker/SPR/board/sizing restrictions merely to make a generic fallback appear safer;
- allow a generic High/Over fallback to erase a more specific scenario rule without explicit justification;
- disable `f$Raise_Committed` merely because the ordinary source tree says CALL; first prove the committed all-in is wrong in that exceptional geometry;
- disable `f$Call_MicroBets` merely because the ordinary source tree says FOLD; first analyze the exceptional price;
- copy a broad CrusherTBP condition when its comment/source shows it was meant for a narrower scenario;
- treat `user_hardcoded.cpp` as higher authority merely because it is newer or more explicit;
- make hand+board-specific patches where a source-supported strategic class can be represented correctly;
- classify a 1–3 percentage-point threshold mismatch as a strategic defect without showing material consequence.

## 9. Change checklist

Before modifying executable strategy:

1. identify the real runtime route and all helpers with precedence over the target node;
2. classify the state as ordinary strategy or exceptional geometry/price/all-in-adjacent state;
3. read the relevant Starting Strategy passage and determine whether it actually covers that exceptional state;
4. inspect CrusherTBP implementation and development comments;
5. inspect relevant `user_hardcoded.cpp` behavior;
6. check professional poker coherence, including stack/pot commitment and pot-odds logic;
7. reconcile the sources and document provenance;
8. preserve legitimate exceptional-helper precedence unless its exceptional action is itself shown wrong;
9. update stale comments together with code;
10. add class-level regressions targeted at the actual defect; use boundary cases only when the boundary itself is strategically material;
11. run static/parser/runtime checks available for the project;
12. compare against the frozen good-results baseline and keep rollback possible.

This policy is a development constraint, not optional documentation.