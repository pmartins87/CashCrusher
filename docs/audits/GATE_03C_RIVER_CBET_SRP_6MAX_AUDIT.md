# Gate 03C — Six-max ordinary-SRP River CBet gaps

Status: **P-heavy policy boundary frozen for Turn families 2/4/7/8**.

## 1. Why these are new River ranges

The Spin source does not contain literal six-max equivalents for:

- UTG/HJ/CO PFA IP versus SB/BB after two barrels;
- UTG/HJ/CO PFA OOP versus a later nonblind cold caller after two barrels;
- a pot that began flop multiway, became HU on Turn, then called a second barrel;
- a Turn that was still multiway and becomes HU only on River;
- a Turn that remains multiway through River.

The legacy positional shells can donate IP/OOP/FIRST/MIDDLE/LAST architecture, but not the actual River range interaction or frequency. These nodes are therefore P-heavy.

## 2. General River principle

A River caller has survived **two prior streets of betting**. Thin value and bluffs must be evaluated against the selected continuing range, not against the preflop calling range.

Selection becomes stronger when:

- the prior street was multiway;
- more players were still live when Hero barrelled;
- prior bet sizes were large;
- Villain is a selected SB/nonblind cold caller rather than a wide BB defender;
- River completes obvious straight/flush/four-card structures.

## 3. EP/MP/CO PFA IP versus BB

BB begins widest, so clean Rivers retain the broadest thin-value region among these P-heavy gaps. Robust 2P+ remains active; OP/strong TP can value-bet clean Rivers; medium TP may thin-value only under favorable selection/SPR conditions. Weak TP checks.

Bluffs are deliberately narrow. A missed Turn draw can bluff selected clean high-pressure Rivers only with a useful high-card/blocker feature. This is a deterministic professional-theory fill, not a solver frequency.

## 4. EP/MP/CO PFA IP versus SB

SB cold-call and two-street continue ranges are more condensed/selected than BB. Medium/weak TP checks more. Missed draws/air have a smaller bluff region. Robust value remains active.

## 5. PFA OOP versus later nonblind cold caller

This is the most selected ordinary flop-HU six-max caller family. OOP River value should be more polarized; medium one-pair checks frequently; pure-air triple barrels require specific blocker/range reasons not yet represented robustly enough, so the first deterministic baseline omits them.

## 6. Flop multiway -> Turn HU -> River HU

Gate02 family 7 already encoded that the Turn caller came from a multiway flop. That selected history persists on River. It must not inherit ordinary flop-HU triple-barrel frequencies.

The initial policy is value-heavy: 2P+ robust; OP/strong TP only on cleaner runouts and suitable SPR; no generic missed-draw bluff.

## 7. Turn multiway -> River HU

This range is even more selected: the surviving Villain called a **multiway Turn second barrel**. Current HU is only a geometric fact. Strategy remains multiway-origin/value-heavy.

## 8. River remains multiway

With two or more opponents still live after two barrels, the first deterministic baseline is strongly value-first:

- straight+/strong 2P+ are primary value;
- weaker 2P can check on completed/four-card structures when deep;
- OP/TP require unusually favorable clean, low deepest-effective SPR conditions;
- no pure-air triple-barrel baseline is authorized.

Any field-wide low-SPR relaxation uses **deepest-effective River SPR**, never the shortest sidepot opponent.

## 9. Stack-depth rule

The same migration rule applies: short-stack source behavior is a review flag, not a global ban or transplant. A 75/100 River bet may naturally exhaust a stack at low SPR; that is handled later by River execution/all-in equivalence. This strategy gate does not grant TP+ automatic stack-off status.
