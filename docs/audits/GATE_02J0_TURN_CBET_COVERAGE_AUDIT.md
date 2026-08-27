# Gate 02J.0 — Turn-CBet strategic coverage audit

Status: **static coverage boundary frozen; runtime OpenHoldem replay certification remains pending**.

## 1. What this audit certifies

This Gate does not claim that every conceivable poker history is strategically solved. It certifies that every Turn-CBet state currently admitted by CashCrusher belongs to one explicit pot/range/history owner and that unsupported histories do not silently inherit a neighboring child.

The canonical parent remains:

`actual standard flop CBet -> turn -> no bet facing Hero -> same aggressive line eligible to second barrel`.

Flop check-through, flop check-call/check-raise, CBet-then-raise histories and runtime-plan mismatches are excluded before pot-family routing.

## 2. Implemented ordinary-SRP Turn coverage

### Flop began heads-up / preflop reduced to heads-up

The normal six-max one-open/one-call matrix is covered by:

- true-HU HUSB PFA-IP source descendant;
- reduced-HU BTN-v-BB and BTN-v-SB source descendants;
- true-HU BB-PFA-OOP after SB limp -> BB raise -> call;
- reduced-HU SB-PFA-OOP vs BB source-safe descendant;
- UTG/HJ/CO PFA-IP vs SB/BB P-heavy family;
- UTG/HJ/CO PFA-OOP vs later nonblind cold caller P-heavy family.

The residual `SRP IP/OOP uncovered` flags remain intentionally outside strategy coverage. They are diagnostics for malformed/unsupported histories, not generic fallback nodes.

### Flop began multiway

Two separate owners exist:

- flop multiway -> turn HU, with exact surviving-opponent provenance;
- turn still multiway, preserving original flop entrant count, current live composition and FIRST/MIDDLE/LAST.

Current handedness therefore never rewrites a multiway-origin range into a normal flop-HU range.

## 3. Implemented other pot families

### ISO

HU and current-multiway ISO are covered only when opponent provenance is exactly reconstructable as:

- original limper; or
- post-raise cold caller.

### Plain 3BP

HU and current-multiway plain 3BP are covered only under supported first-orbit chronology and exact opener/post-3bet-coldcaller provenance.

### Squeeze

HU and current-multiway squeeze are covered separately from plain 3BP and retain opener / pre-3bet-coldcaller / post-3bet-coldcaller range origin.

### Clean HU 4BP

Supported clean HU families are:

- true-HU opener4 vs original 3bettor-call;
- reduced-HU opener4 vs original 3bettor-call;
- reduced-HU cold4 vs original opener-call;
- reduced-HU cold4 vs original 3bettor-call.

## 4. Explicitly unsupported Turn-CBet histories

The following remain fail-closed:

- multiway 4BP, because flop 4BP policy itself remains unsupported;
- a 4BP flop that was multiway and only became HU after the flop;
- 4BP survivor of type `other caller` whose exact call stage cannot be reconstructed;
- reversed / limp-reraise / backraise 4BP chronology not proven by aggregate action masks;
- 5bet+ postflop families;
- unsupported/reversed 3bet chronology;
- any pot/range state whose exact current survivor cannot be mapped to the persisted preflop masks;
- any actual-action history that is not a certified standard flop CBet parent.

These states receive `false` action and size ID `0`; they do not borrow ordinary SRP, ISO, 3BP or 4BP logic.

## 5. Pot-family exclusivity

The top-level Turn router now separates:

- ordinary SRP: pot family 2 + one-raise ordinary-SRP proof;
- ISO: pot family 2 + ISO proof;
- plain 3BP: pot family 3 + plain-3bet proof + explicit `!squeeze`;
- squeeze: pot family 3 + squeeze proof + explicit `!plain3bet`;
- 4BP: pot family 4 + Hero final-4bettor role.

This prevents plain3BP/squeeze overlap and prevents one-raise ordinary SRP from swallowing an ISO history.

## 6. Current Turn size-domain contract

Every implemented Turn-CBet action returns one of seven strategic size IDs only:

1. 25%
2. 33%
3. 40%
4. 50%
5. 62.5%
6. 75%
7. 100%

ID `0` means check/uncovered/invalid. Runtime conversion is owned by Gate02J.1/02J.2 and is intentionally separate from strategic action ownership.

## 7. What is not certified yet

This is a static source/routing audit. It does not replace:

- native OpenPPL parser validation;
- OpenHoldem replay fixtures;
- whole-bot `f$turn` / `f$BestBetsize` composition;
- final global `f$allin_on_betsize_balance_ratio` audit;
- response to a turn raise after Hero barrels.

Those remain later runtime/defense gates.
