# CashCrusher OpenPPL coding contract

Status: **binding project rule**.

This contract carries forward the OpenPPL safety rules established during the DeepCrusher audit and makes them explicit for CashCrusher. It is stricter than what the parser technically permits, because the project prioritizes auditable semantics over compact syntax.

## 1. Flat complete `WHEN` rules — mandatory

OpenPPL does **not** create logical scope from indentation. The parser supports open-ended `WHEN` conditions and back-patches their branches by token order. Therefore code that *looks* nested can execute differently from what visual alignment suggests.

CashCrusher consequently forbids open-ended `WHEN` syntax in `src/*.txt`.

Bad / forbidden:

```text
When A
    When B Return true Force
    When C Return false Force
When Others Return false Force
```

The apparent visual block is not a reliable scope contract.

Required CashCrusher form:

```text
When A && B Return true Force
When A && C Return false Force
When Others Return false Force
```

A condition may wrap physically over multiple lines for readability, but **before the next `WHEN` token there must be an explicit OpenPPL action** (`Return`, `Set`, etc.). Indentation is documentation only.

`tools/lint_custom_dependencies.py` enforces this rule as a CI error.

## 2. Evaluation order is strategy

`WHEN` rules are evaluated from top to bottom. More specific exceptions must appear before broader parents. A later broad rule must never make an earlier source-specific exception unreachable.

For every strategic function:

1. mechanical/context guard;
2. source-specific exception(s);
3. reviewed baseline rules from strongest to weakest/specific to broad;
4. explicit fallback.

Do not reorder conditions merely for visual tidiness without re-auditing semantics.

## 3. `Return ... Force` versus `Set`

- `Return ... Force` is terminal for the current function.
- `Set user_*` / memory writes create state and evaluation continues.
- A state write must occur **before** every terminal return that later streets/readers depend on.
- Never write a provenance/history flag after the action that is supposed to create it.

For helper functions that return booleans, IDs or sizes, prefer explicit `Return ... Force` branches and an explicit `When Others Return ... Force` fallback.

## 4. Unknown strategic states fail closed

A mechanically valid context is not automatically a strategically covered context.

Rules:

- missing strategy -> check / false / zero-size;
- unknown chronology -> unknown subtype, not approximation;
- unsupported pot family -> no leakage from a neighboring family;
- never use `When Others Return true Force` as a generic strategic tail unless the audited source explicitly proves that the entire remaining domain takes that action.

This is particularly important for 3BP/squeeze/ISO/multiway boundaries.

## 5. No invented OpenPPL semantics

Before using a native symbol or reserved callback:

1. verify the symbol/callback exists in the OpenHoldem/OpenPPL implementation/manual available to the project;
2. verify units and persistence (chips vs BB, current street vs saved history, current player set vs dealt set);
3. do not infer chronological information from aggregate bitmasks when the runtime does not preserve it;
4. when evidence is insufficient, expose an `unknown` state and fail closed.

Examples already frozen by Gate 00:

- `NumberOfRaisesBeforeFlop` is used as the persisted preflop raise count;
- `raisbits1` / `callbits1` are historical bitmasks, not full action-order logs;
- current-player count is different from deal size and different from flop-entry count;
- true HU deal is different from a multi-handed deal reduced to two players.

## 6. Source/provenance comment contract

Every CashCrusher function must explain **what it means and where it came from**. Strategic functions require more detail than trivial mechanical aliases.

### Mechanical/context helper

At minimum:

```text
// Purpose: what mechanical fact this function exposes.
// Source/Provenance: OpenHoldem/OpenPPL runtime symbol and/or DeepCrusher helper; T/A.
```

### Strategic policy function

Use a local contract such as:

```text
// Purpose: exact decision family owned by this function.
// Context: pot family, Hero role, position, opponent/range family, street.
// Source: exact DeepCrusher/Crusher ancestor if one exists.
// Provenance: T / A / P / X, including which parts are professional-theory fills.
// Decision logic: ordered explanation of value/draw/bluff/check regions.
// Safety/Limits: unsupported contexts, shallow-stack rules rejected, future dependencies.
```

A professional-theory fill must be labelled **P** at the point where it enters the policy. It must never be presented as if it came from Crusher.

## 7. T/A/P/X provenance remains binding

- **T — Transplant:** source rule is mechanically and strategically safe in the new context.
- **A — Adapt:** source principle survives but range, stack, sizing or scope changes.
- **P — Professional theory fill:** source does not cover the six-max gap adequately; use robust professional NLHE principles and state that provenance explicitly.
- **X — Reject:** inherited rule is too Spin/shallow/context-specific to survive literally.

One function may contain multiple provenances. Comments should identify which branch is which.

## 8. Postflop node ownership must remain explicit

Do not collapse distinct nodes because they happen to bet on the same street.

Examples:

- CBet != Donk Bet;
- Float Bet != Probe Bet;
- Delayed CBet != generic no-action bet;
- CBet response to raise != ordinary defense versus a bet;
- HU after a multiway flop != HU range topology.

Cross-street flags must record the exact node that produced the state so later streets do not infer history from the current board alone.

## 9. Sizing and all-in safety

For the current CashCrusher baseline:

- canonical postflop size families: ~33%, 50%, 75%, 100%, and explicit all-in only when a reviewed node owns it;
- global inherited auto-jam conversion remains disabled;
- no strategy function may use `BetMax` merely because a planned bet consumes a large part of the stack;
- raw SPR is an input, not an automatic commitment instruction.

## 10. Review rule

Before any Gate can be called implemented:

1. source audit completed;
2. exact context ownership documented;
3. OpenPPL code uses flat complete `WHEN`s;
4. function provenance/comments present;
5. custom dependency/strategy lint passes;
6. parser/runtime validation still required before release to table testing.

Static CI success is necessary but **not** equivalent to OpenHoldem parser/runtime PASS.
