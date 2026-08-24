# Gate 03G — Clean HU 4-bet-pot River CBet

Status: **P-heavy clean-HU policy boundary frozen**.

CashCrusher only reaches Gate02 family 12 from already-supported clean HU 4BP Turn-CBet families. Multiway 4BP, other-caller unresolved call stage, reversed/backraise/limp-reraise and 5bet+ never obtain this parent and remain fail-closed.

## Natural low SPR matters

A hand that starts 100bb can legitimately reach River 4BP with SPR well below 1 after open/3bet/4bet/call and two postflop bets. CashCrusher therefore does not treat all aggressive short-stack behavior as invalid merely because the hand started deep.

At the same time, the historical Spin idea that almost any TP+ can simply play stacks is not imported. Current River hand, runout, exact 4BP range family and actual SPR determine value.

## Clean range families

- true-HU opener4 versus original 3bettor;
- reduced-HU opener4 versus original 3bettor;
- reduced-HU cold4 versus original opener;
- reduced-HU cold4 versus original 3bettor.

Cold4 continuation ranges are treated as more selected/condensed than ordinary opener4-v-3bettor.

## Professional baseline

- 2P+/straight+ are robust value except extreme public-board counterfeiting/completion concerns;
- OP/strong TP remain legitimate River value more often than in SRP when SPR is naturally low and runout is clean;
- medium TP only enters very low-SPR/value-specific cases and is not universal;
- pure-air River bluffing is omitted in the first deterministic 4BP pass because exact blocker/nut-range selection deserves its own treatment rather than fabricated precision;
- requested 75/100 sizing can become a natural mechanical all-in later if it reaches the remaining stack/effective stack.

No generic historical 50/55/60% promotion is reintroduced by this strategy gate.
