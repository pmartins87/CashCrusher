# Gate 02I — Clean HU 4-bet-pot Turn CBet

Status: **source boundary audited; clean HU policy is P-heavy, with natural low-SPR geometry explicitly retained**.

DeepCrusher does not contain a dedicated deep-stack 4BP flop or turn CBet tree. Its reusable contribution is A-level architecture: current hand strength, IP/OOP, board/runout sensitivity, draw quality and protected checking. Exact 100bb cash 4BP continuation frequencies are P.

CashCrusher currently has flop CBet coverage only for clean HU 4BP families: true-HU standard opener4 and reduced-HU opener4/cold4 versus proven opener/3bettor survivors. Multiway 4BP flop CBet remains fail-closed because aggregate call history cannot reliably identify every non-raiser caller's call stage. Consequently Gate02I also limits strategic coverage to clean flop-HU 4BP histories that can actually have a certified standard flop CBet parent.

## Natural low SPR

A 100bb hand can reach turn with very low SPR after open/3bet/4bet/call and a flop CBet. This is exactly where the project rule matters: old short-stack aggression is neither automatically discarded nor automatically transplanted.

The Turn node therefore uses actual current HU SPR as a strategic input. Robust overpairs/top pairs may continue more often at low SPR than in SRP; strong draws can remain active; but TP/OP are still not unconditional stackoff classes.

A requested 50/75/pot turn sizing that reaches the remaining stack can later become a natural/mechanical all-in through the turn execution layer. Gate02I does not invent a blanket strategic `BetMax` threshold.

## Range families

1. **opener4 vs original 3bettor-call** — the broadest clean 4BP family currently supported;
2. **cold4 vs original opener-call** — very strong/condensed continuing range, tightest one-pair/air policy;
3. **cold4 vs original 3bettor-call** — also strong and selected, with slightly different nut/range distribution;
4. **true-HU opener4** — same topology as opener4-v-3bettor but true-HU range ancestry remains separate.

## Professional baseline

- trips+/strong two pair remain primary value;
- overpair/strong TP continue frequently on clean turns, especially at SPR <2–3;
- completion/four-card turns reduce one-pair barrels when still deep enough for meaningful future decisions;
- medium/weak TP check more, particularly against cold4 continuation ranges;
- premium draws remain active; good draws are more IP/clean-turn dependent;
- pure air is narrow for opener4-v-3bettor IP and absent against cold4-v-opener in the first deterministic baseline;
- OOP checks more while preserving low-SPR value continuation.

## Fail-closed boundary

No Turn 4BP strategy runs if clean subtype/survivor proof, actual standard flop CBet history, HU origin or SPR geometry is inconsistent. Multiway 4BP, other-caller survivor, reversed/limp-reraise/backraise and 5bet+ remain unsupported.
