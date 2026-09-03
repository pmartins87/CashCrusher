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

`pot classifier -> preflop/history state -> initiative -> scenario -> position -> sizing bucket -> raise/call router -> strategic node -> sizing/commitment helper -> final action`

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

## 6. Prohibited review shortcuts

Do not:

- infer strategy from a function name without tracing its callers and state conditions;
- invent kicker/SPR/board/sizing restrictions merely to make a generic fallback appear safer;
- allow a generic High/Over fallback to erase a more specific scenario rule without explicit justification;
- allow commitment helpers to silently transform a source-mandated CALL into a raise/jam without auditing that interaction;
- copy a broad CrusherTBP condition when its comment/source shows it was meant for a narrower scenario;
- treat `user_hardcoded.cpp` as higher authority merely because it is newer or more explicit;
- make hand+board-specific patches where a source-supported strategic class can be represented correctly.

## 7. Change checklist

Before modifying executable strategy:

1. identify the real runtime route and all helpers with precedence over the target node;
2. read the relevant Starting Strategy passage;
3. inspect CrusherTBP implementation and development comments;
4. inspect relevant `user_hardcoded.cpp` behavior;
5. check professional poker coherence, especially discontinuities at sizing/SPR boundaries;
6. reconcile the sources and document provenance;
7. update stale comments together with code;
8. add class-level regression cases, including boundary cases around sizing buckets;
9. run static/parser/runtime checks available for the project;
10. compare against the frozen good-results baseline and keep rollback possible.

This policy is a development constraint, not optional documentation.