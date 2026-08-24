# Gate 03H — River CBet sizing / stack-sensitive runtime

Status: **execution contract defined**.

## River size palette

Current canonical River CBet uses five strategic sizes:

- 25% pot;
- ~33% pot;
- 50% pot;
- 75% pot;
- 100% pot.

OpenPPL native actions own 33/50/75/100. The 25% family uses `RaiseBy 25% Force`; canonical River CBet has `AmountToCall=0`, so percentage RaiseBy contributes exactly the requested pot fraction.

## Historical `RiverMax`

DeepCrusher contains multiple RiverMax branches, but their strategic meaning is node-specific. Some are short-stack value plans, some come from human-reviewed gaps, and some naturally occur after previous large bets.

CashCrusher therefore does **not** implement one global `RiverMax` translation. Strategy modules first choose their reviewed 25/33/50/75/100 size. A future exact strategic jam can be added to a specific node if justified.

## Natural/mechanical all-in equivalence

A requested River size is locally converted to `BetMax` only when it already reaches:

- Hero's entire available stack; or
- the exact HU effective relationship; or
- in multiway, the **deepest/all-live effective relationship**.

Reaching only the shortest multiway opponent can merely create a sidepot and does not promote the entire bet to `BetMax` while a deeper opponent remains.

This is execution equivalence, not strategic commitment.

## Historical 50/60 diagnostics

The same historical ~50%-effective and ~60%-Hero-stack signals are retained as diagnostics so exact later audits can compare CashCrusher geometry to DeepCrusher behavior. They do not authorize River all-in globally.

## Defense ownership

If Villain raises after Hero's River CBet, the response is a later defensive River node. This execution gate owns only the initial checked-to River bet.
