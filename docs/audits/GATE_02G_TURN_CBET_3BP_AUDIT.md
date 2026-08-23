# Gate 02G — Plain 3-bet-pot Turn CBet

Status: **source boundary audited; policy is P-heavy with exact opener/coldcaller provenance**.

DeepCrusher does not contain a clean deep-stack 3BP flop-CBet tree, and therefore does not provide a trustworthy dedicated 3BP second-barrel tree either. Its reusable evidence is architectural: initiative/current-strength handling, IP/OOP separation, runout sensitivity, draw quality, and protected checking ranges. Exact deep-cash 3BP turn frequencies are P.

CashCrusher preserves two plain-3BP survivor origins: original opener-call and post-3bet coldcaller. A post-3bet coldcaller must not inherit opener-call policy. If a multiway 3BP flop becomes HU on turn, the current survivor is reclassified by the same exact masks and receives an additional selection penalty.

Professional baseline: 3BP ranges are tighter and turn SPR is naturally lower than SRP. Static/clean high-card runouts can sustain broad small/medium pressure, while low/dynamic/new-completion turns increase checks. Robust value and premium draws remain active. Marginal one-pair and air tighten, especially OOP and versus a post-3bet coldcaller. Low SPR is a strategic input, not automatic TP+ stackoff authority.

Multiway plain 3BP remains value-heavy: robust made value, selective OP/strong-TP and premium draws, with deepest-effective SPR controlling any field-wide depth relaxation. Pure air is omitted from the first deterministic multiway baseline.

No historical short-stack commitment helper is globally disabled or imported by this Gate. A future response to a raise remains a separate node with actor-specific geometry.
