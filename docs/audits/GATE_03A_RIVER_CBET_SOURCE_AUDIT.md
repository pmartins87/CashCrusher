# Gate 03A — Canonical River CBet source audit

Status: **source boundary frozen for the first River-CBet implementation pass**.

## 1. Ownership: River CBet is an executed-history node

CashCrusher defines canonical River CBet narrowly:

- Hero actually executed the reviewed flop CBet;
- Hero actually executed one normal reviewed Turn CBet;
- Hero did not check, call or re-aggress later on Turn;
- Hero did not finish Turn all-in;
- Hero remained the final Turn aggressor;
- the Gate02N Turn snapshot/plan/runtime history is internally consistent;
- River action reaches Hero with nothing to call.

Therefore River CBet consumes `f$cc_hist_river_standard_cbet_parent_valid`, not a stale initiative flag and not `user_*` plan markers alone.

Turn check-through belongs to delayed/no-action ownership. Turn CBet -> raise -> Hero call belongs to Villain-initiative continuation. Turn CBet -> Hero re-aggression belongs to a raised-Turn continuation node.

## 2. DeepCrusher normal-CBet source boundary

The audited `f$move_river_cbet` contains a dedicated **SOURCE-FIDELITY RETRO03 — RIVER CBET** layer. Its own hierarchy is:

1. clear Crusher Starting Strategy;
2. human-reviewed CrusherTBP gap fill;
3. `user_hardcoded.cpp` cross-check;
4. theory residue.

Most importantly, after the reviewed normal-CBet branches it has a quarantine:

`When user_did_cbet_OTF && user_did_cbet_OTT Return false Force`

That means a genuine flop+turn CBet history not matched by an audited river contract **checks** instead of falling into broad generic tails. CashCrusher retains this fail-closed philosophy.

## 3. Source-anchored standard-CBet descendants

### 3.1 True-HU HUSB — Hero SB/Button PFA IP vs BB

Source contracts:

- standard TP+ plan: approximately 75 / 75 across Turn/River;
- flop TP demoted by Turn overcard: 50 Turn / 50 River family;
- Turn TP barrel 75: current 2P+ remains value; completed River plus meaningful OC pressure from Turn or River checks; otherwise 75;
- Turn MP barrel: current 2P+ -> 75, current TP/OP -> 50, otherwise check;
- Turn draw barrel: current 2P+ -> 75, current TP/OP -> 50, missed draw -> check by default;
- Turn air barrel: current 2P+ -> 75, current TP/OP -> 50, otherwise check;
- old optional/narrow missed-draw 3-barrel prose is not converted into an unconditional bluff.

This is strong A ancestry for CashCrusher true HU. Full-HU ranges are still wider than ordinary 6-max heads-up pots.

### 3.2 True-HU HUBB ordinary CBet — Hero BB PFA OOP vs SB/Button limp-call

The Starting Strategy does not contain a complete ordinary-CBet river table; the human-reviewed CrusherTBP interpretation is binding in the audited DeepCrusher layer.

Source contracts include:

- completed River straight+ -> 75;
- completed River TP+ -> small 33 block/thin-value family;
- non-completed 2P+ -> historical `RiverMax`;
- TP/OP -> 33;
- draw-origin line can continue current value and some no-made states with 50/100 source sizes.

The **action direction** is useful A evidence, but historical `RiverMax` and no-made continuation require cash-depth review. They are not automatic T-level all-ins at 100bb-starting-stack cash.

### 3.3 Reduced-HU BTN PFA IP vs SB

Source contracts:

- strong-value Turn plan -> historical `RiverMax`;
- weak-kicker TP two-street plan checks River unless current hand improved to 2P+, then 75.

Cash adaptation must preserve the two-street-vs-three-street distinction while separately reviewing whether `Max` should be 75/pot/jam at the actual River SPR.

### 3.4 Reduced-HU BTN PFA IP vs BB

The normal-CBet source table is comparatively explicit:

- exact 2P+ that blocks the top-pair board rank -> 50;
- other 2P+ -> 75;
- overpair -> 75;
- just TP below TPGK source threshold -> check;
- just TP on completed River -> check;
- TPGK+ on non-completed River -> 50;
- explicit no-made Turn plans can either give up or barrel, but those plans require exact source-plan provenance. CashCrusher does not reconstruct them from size alone.

The source TPGK threshold is `NumberOfBetterKickers <= 3`.

### 3.5 Reduced-HU SB PFA OOP vs BB

The source is highly history-dependent:

- low-TP paired two-barrel lines check River;
- a specific straight-completing Turn 100% line historically uses `RiverMax` for stronger TP+/OP/2P+, weaker TP 50;
- draw-origin Turn50 gives up when missed and value-bets river improvements with size depending on made-hand contribution/SPR.

Because the exact historical Turn-plan markers were not copied into CashCrusher, this family may only transplant branches whose provenance can be proved from the CashCrusher Turn snapshot/size/runout. Ambiguous residue fails closed.

## 4. `3wBBvSB` source is not automatically ordinary SRP River CBet

Legacy `3wBBvSB` can arise from histories where Hero BB obtained initiative through a limp-raise/isolation or another non-ordinary path. Current absolute matchup alone is insufficient. CashCrusher will route it through the exact preflop/Turn family (ISO/other) rather than treating the label as an ordinary-SRP ancestor.

## 5. Current River strength supersedes stale history

Stored Turn hand class answers **how Hero arrived here**. Current River hand strength answers **what Hero has now**.

Examples:

- Turn draw that rivers 2P+/straight/flush is reclassified as current value;
- Turn TP that is counterfeited or becomes fragile on a completed River is evaluated from current River strength/runout;
- a Turn air barrel that pairs River may become showdown/value state instead of remaining "air".

This mirrors the mature DeepCrusher source-fidelity repair.

## 6. River texture facts to preserve mechanically

Portable T/A descriptors are required for:

- `river_Completed` = straight possible OR flush possible;
- `river_SuperCompleted` = both straight and flush possible;
- River newly creates straight possibility;
- River newly creates flush possibility;
- River meaningful overcard / strict overcard;
- River under-flop / under-board;
- River pairs a previous board rank;
- one-card/four-card straight or flush completion pressure;
- whether the **Turn** was a meaningful overcard, reconstructed from persistent Turn/Flop cards rather than from an `IsTurn`-only helper.

These descriptors never choose an action by themselves.

## 7. Multiway history must remain selected on River

Gate02N snapshots the exact player count and live-opponent mask at the Turn CBet decision.

If Turn was multiway and River becomes HU, the surviving Villain called a **multiway Turn barrel**. That selected range must not inherit an ordinary HU three-barrel tree merely because `headsupchair` now reports one opponent.

Likewise a River that remains multiway requires its own value-heavy policy. These are P-heavy families except where an exact legacy source descendant can be proven.

## 8. Other pot families

ISO, plain 3BP, squeeze and clean HU 4BP retain their Gate02 family IDs into River. The Spin source does not provide clean deep-stack River-CBet trees for these six-max range families. Their River policy is therefore P-heavy and must be implemented separately after the source-anchored SRP gate.

## 9. Stack-depth migration rule on River

Historical `RiverMax` is **not deleted merely because CashCrusher starts 100bb**, and it is **not transplanted merely because DeepCrusher used it**.

Each Max/shove line is reviewed against:

- exact range family;
- current River hand class;
- board/runout and blockers;
- actual effective stack and River SPR;
- prior bet sizes and range selection.

A normal River value bet with TP/OP is not automatic stack-off authority. Conversely, naturally low-SPR 3BP/4BP/squeeze or source-exact polar nodes may legitimately end in all-in once their exact geometry supports it.

## 10. First implementation order

1. portable River texture/current-strength/common context;
2. source-anchored SRP descendants: HUSB, HUBB, BTN-v-BB, BTN-v-SB, SB-v-BB where provenance is provable;
3. post-multiway-HU and still-multiway SRP;
4. six-max SRP P-heavy gaps;
5. ISO;
6. plain 3BP;
7. squeeze;
8. clean HU 4BP;
9. River sizing/runtime/natural-all-in layer;
10. closed River action history only when needed by subsequent ownership nodes.

Unknown or ambiguous standard-CBet histories check rather than borrow a neighboring source tree.
