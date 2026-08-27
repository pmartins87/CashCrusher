# CashCrusher

CashCrusher is the six-max cash postflop adaptation of the audited DeepCrusher/Crusher strategy framework.

Current development principles:

- dynamic 2-6 handed context;
- true-HU deal distinguished from fold-reduced HU;
- exact pot/range provenance before strategy;
- T/A/P/X source classification;
- flat complete OpenPPL `WHEN` rules;
- source/provenance comments on reviewed strategy functions;
- stack-sensitive DeepCrusher rules are reviewed in their exact cash context rather than copied blindly or globally disabled.

Development is currently on `gate-00-context-engine`. `main` remains intentionally conservative until parser/runtime and replay gates pass.
