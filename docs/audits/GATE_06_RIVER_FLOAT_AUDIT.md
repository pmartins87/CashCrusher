# Gate 06 — River Float audit

Status: **static/deterministic strategy + runtime layer complete for reviewed families; whole-bot/OpenHoldem replay certification remains pending**.

CI closure: GitHub Actions **run #652**, commit `96399d000103d64e154bd63fbbc04705ed8c914d`, completed successfully with the full regression suite.

## 1. Canonical ownership

River Float is not “Hero floated Turn and got called”. The canonical Gate06A parent is:

- Hero **called** exactly one Turn bet;
- Hero did not check/bet/raise/all-in on that Turn action path;
- exactly one opponent is proven as final Turn aggressor by `raisbits3 + lastraised3`;
- that aggressor remains live;
- River is Hero's first action, `AmountToCall = 0`, Hero is exact LAST;
- in HU, Hero is IP and the aggressor is the current `headsupchair`.

An executed Turn Float leaves Hero as Turn aggressor and is therefore a different River owner.

## 2. Source findings

`Crusher Framework 5` leaves `f$move_river_floatbet` empty.

The manually reviewed CrusherTBP / mature DeepCrusher evidence supports a portable value ladder inside the source-sized field:

- nutted/literal-nuts subset: 75%;
- 2P+: 75%, reduced to 50% on super-completed River unless literal nuts;
- real overpair: 50%;
- real top pair with `NumberOfBetterKickers <= 4`: 50%.

The only explicit no-made source bluff retained is the exact `3wBBvSB` called-two-barrel busted-draw line. The mature source uses 25%, but CashCrusher keeps it locked until a future defensive Turn-call snapshot proves the required history:

`flop high-air/backdoor -> Turn real draw -> call second barrel -> River miss -> SB checks`.

`3wBTNvSB + NoMadeHand` remains an explicit source check.

## 3. Source-domain firewall correction

During Gate06E/F review, an ownership leak was found in Gate06B: the generic source value ladder was initially guarded only by 2-3-player field size. That could allow source value to fire in an unreviewed unraised, 5bet+, or unresolved reraised pot merely because the River was short-handed.

This was corrected before Gate06 completion.

`f$cc_river_float_source_reviewed_pot_domain` now admits the portable source value ladder only in explicitly reviewed pot structures:

1. one-raise ordinary SRP / proven ISO / true-HU limp-raised;
2. repaired supported plain 3BP or squeeze chronology;
3. clean HU 4BP with either:
   - Hero as proven clean final 4bettor versus original opener/3bettor survivor; or
   - the single caller-side chronology `opener -> Hero 3bet -> opener 4bet -> Hero call`.

Unraised, 5bet+, reversed/unknown 3BP, multiway/unresolved 4BP and other-caller 4BP do not acquire generic source ownership.

## 4. Gate06C — ordinary SRP gaps

Reviewed topologies are kept distinct:

- clean HU caller vs PFA;
- clean HU PFA that later lost initiative;
- current three-way;
- three-way flop origin now HU with Turn-call player count unresolved;
- four-plus flop origin.

No generic River bluff is created from current `NoMadeHand`. The source itself demonstrates that River-Float bluffing depends on prior draw provenance, and CashCrusher does not yet have a generic defensive Turn-call draw snapshot.

For four-plus flop origins, only robust current value becomes a new positive P action. Public four-card straight/flush structures tighten the threshold heavily; literal nuts or FH+ are preferred there. Other approved robust value uses 50%, literal nuts 75%.

## 5. Gate06D — ISO / true-HU limp-raised

Multi-handed ISO preserves both Hero and actual Turn-aggressor origin:

- original limper;
- post-raise coldcaller;
- isolation raiser.

True-HU SB/Button limp -> BB raise -> call remains separate from multi-handed ISO.

Clean-HU limper-v-isolator, coldcaller-v-isolator and isolator-lost-initiative are separate reviewed families. Post-multiway-now-HU, current-multiway and four-plus origin remain separate range states.

Source-sized positive value is owned by Gate06B. Source-silent no-made / weak showdown value checks. Four-plus origin receives only the conservative robust-value P adaptation.

## 6. Gate06E — plain 3BP / squeeze

Gate06E uses the repaired `lastraised1` chronology, not Hero-participation assumptions.

Hero origin is uniquely reconstructed as:

- final 3bettor/squeezer;
- opener-call;
- pre-3bet coldcaller (squeeze only);
- post-3bet coldcaller.

The actual Turn aggressor is independently reconstructed from the same four range origins.

Plain 3BP and squeeze are separate pot families. Clean-HU opener-v-3bettor, postcold-v-3bettor, 3bettor-lost-initiative, opener-v-squeezer, precold-v-squeezer, postcold-v-squeezer and squeezer-lost-initiative are not collapsed into one generic reraised-pot range.

Again, no source-silent missed-draw bluff is manufactured without the missing Turn-call draw/blocker provenance. Four-plus origins receive only robust-value positive P action.

## 7. Gate06F — clean HU 4BP

Only clean HU-from-HU-flop histories are reviewed:

- caller-side `opener -> Hero 3bet -> opener 4bet -> Hero call`;
- Hero clean opener4 versus original 3bettor;
- Hero clean cold4 versus original opener;
- Hero clean cold4 versus original 3bettor.

The portable source value ladder is allowed only through the Gate06B reviewed 4BP pot-domain firewall.

Gate06F itself adds **no source-silent positive River action**. Weak/no-made classes are reviewed checks. Multiway/post-multiway 4BP, unresolved other caller, reversed/backraise/limp-reraise and 5bet+ remain visible fail-closed states.

This is deliberate: naturally low 4BP SPR can make a source value bet large relative to stacks, but that does not justify inventing a generic bluff or TP+/OP stackoff rule.

## 8. Gate06H — runtime sizing and natural all-in

River Float uses the canonical River palette:

- 25% -> `RaiseBy 25%`;
- 33% -> `BetThirdPot`;
- 50% -> `BetHalfPot`;
- 75% -> `BetThreeFourthPot`;
- 100% -> `BetPot`.

The runtime layer preserves:

- Hero-stack ratio;
- exact HU effective ratio;
- multiway shallowest effective ratio for sidepot diagnostics;
- multiway **deepest effective** ratio for all-live equivalence;
- historical ~50/60 threshold diagnostics.

`BetMax` is returned locally only if the already-selected strategic size reaches:

1. Hero's whole stack; or
2. the exact HU effective stack; or
3. the deepest/all-live multiway effective relationship.

Reaching only the shortest multiway opponent never promotes the entire action.

Historical 50/55/60 near-all-in thresholds do not trigger River-Float `BetMax`.

Pre-action `user_cc_river_float_*` markers record intended family/size/all-in expectation for eventual same-River defense. They are not proof that the client executed the intended action.

## 9. Current fail-closed boundary

The following River-Float states remain intentionally unsupported rather than borrowing another family:

- unraised pot River Float not separately audited;
- unresolved/reversed 3BP chronology;
- multiway/post-multiway/unresolved-othercaller 4BP;
- reversed/backraise/limp-reraise 4BP;
- 5bet+;
- generic missed-draw River bluff without a defensive Turn-call draw/blocker snapshot;
- any multi-aggressor Turn history that Gate06A cannot assign to one final aggressor.

## 10. Validation state

Static linter and all deterministic strategy/history/runtime regressions passed in **run #652**. This includes Gate06A history, Gate06B source ownership, SRP, ISO, plain3BP/squeeze, clean4BP, canonical coverage and River-Float runtime sizing/all-in geometry.

Gate06 is therefore complete at the **static/deterministic policy layer**.

It is **not table-certified** until the global whole-bot `f$river` / sizing composition, OpenHoldem parser/runtime fixtures and replay gates pass.
