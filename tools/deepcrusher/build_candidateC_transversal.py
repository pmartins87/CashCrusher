from pathlib import Path
import hashlib, re

BASE=Path('/mnt/data/DeepCrusher_GOOD_RESULTS_BASELINE_20260903_SHA26302fa1.txt')
OUT=Path('/mnt/data/DeepCrusher_CandidateC_Transversal_20260903.txt')
t=BASE.read_text(encoding='utf-8')

# 1) Comments: binding source policy, no executable change.
old='// Priority: user_hardcoded.cpp 2026 corrections > explicit Framework5 rules > CrusherTBP mature baseline.'
new='// Source policy: reconcile Starting Strategy + human-reviewed CrusherTBP; user_hardcoded is secondary cross-check; professional theory fills genuine gaps.'
count=t.count(old)
assert count==25, count
t=t.replace(old,new)

# 2) Scope leak: this dry-TP slowplay line came from 3wBTNvBB specifically.
old_line='When IsFlop && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force // add 16-05 //3wBTNvBB CF Q2 TP On dry structures - CALL and let your opponent remain with his bluffs'
new_line='When IsFlop && f$game_3wBTNvBB && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force // SOURCE: RECONCILED (Starting Strategy + CrusherTBP scope comment + runtime): 3wBTNvBB dry-TP slowplay only.'
assert t.count(old_line)==1
t=t.replace(old_line,new_line)

# 3) Delayed Float precedence: keep generic residual out of HUSB so detailed HUSB reader can execute.
old_df='When !f$game_3wBBvSB Return true Force\n\n// Source-fidelity correction after Gate04R: HUSB skipped-ISO current pair/draw\n// classes bet the flop instead of being conservatively checked back. The source-\n// explicit air class also bets flop 50. Therefore no audited HUSB history remains\n// that should be manufactured into a Turn Delayed Float here.\nWhen f$game_HUSB Return false Force\n'
new_df='When !f$game_3wBBvSB && !f$game_HUSB Return true Force\n\n// SOURCE: RECONCILED (runtime reachability + existing detailed HUSB history).\n// HUSB is intentionally excluded from the residual TBP fallback above so the\n// source-aware user_DC12B_HUSB_FlopMediumMadeCheck subtree below remains reachable.\n'
assert t.count(old_df)==1
t=t.replace(old_df,new_df)

# Shared first-facing-bet expression. Existing f$act_1/2/3 exclude reraises.
fb='(f$act_1_vs_normalbet || f$act_2_vs_highbet || f$act_3_vs_overbet)'
onepair='(f$CF7_TopPairReal || f$CF7_OverPairReal)'

# 4) Insert source-specific Facing-Bet ownership BEFORE f$Raise_Committed.
marker='// Gate 08 top-level guard. f$Raise_Committed is normally evaluated before the\n'
assert t.count(marker)==1
raise_guard=f'''// ============================================================================
// TRANSVERSAL 02 — source-specific flop Facing-Bet ownership BEFORE commitment.
// These guards use executable state (scenario/pot/action buckets), not node names.
// f$act_1/2/3 prove an initial bet and exclude a raise after Hero already acted.
// ============================================================================

// 3wBBvSB TP/OP, LP/SRP.
// SOURCE: STARTING_STRATEGY — TP+ Facing Bet: wet -> raise 50%; dry -> call only
// versus roughly 50%+ sizing. The existing ~52% lowbet boundary is deliberately
// preserved as an operational margin, not literalized to 50.
// SOURCE: USER_HARDCODED — corroborates wet raise / dry large call.
// SOURCE: RECONCILED — dry small bet is raised 50% (written source excludes the
// call; CrusherTBP/C++ completion and professional value/protection logic agree).
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && !f$board_dry Set user_DCR_3wBBvSB_TP_FB_Line
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && !f$board_dry Set user_DCR_3wBBvSB_TP_FB_Raised
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && !f$board_dry Set user_DCR_3wBBvSB_TP_FB_Raise50
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && !f$board_dry Return true Force
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && f$act_6_vs_lowbet Set user_DCR_3wBBvSB_TP_FB_Line
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && f$act_6_vs_lowbet Set user_DCR_3wBBvSB_TP_FB_Raised
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && f$act_6_vs_lowbet Set user_DCR_3wBBvSB_TP_FB_Raise50
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && f$act_6_vs_lowbet Return true Force
// Dry non-lowbet is an explicit CALL. This false guard is intentionally before
// f$Raise_Committed so a large source-mandated call is not promoted to a jam.
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && !f$act_6_vs_lowbet Return false Force

// 3wBTNvBB TP/OP, SRP, facing the BB's initial flop bet.
// SOURCE: STARTING_STRATEGY — <=~75 dry+ call / wet raise; ~75-150 non-CPL call
// / CPL raise; >150 non-CPL call / CPL call only with additional equity.
// SOURCE: USER_HARDCODED — independently implements the same tree and the
// one-third-stack raise target. Small 75/76 routing margin is preserved.
// Raise branches are captured here before generic commitment/fallback logic.
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_1_vs_normalbet && {onepair} && !f$board_dry Set user_DCR_3wBTNvBB_TP_FB_Raised
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_1_vs_normalbet && {onepair} && !f$board_dry Return true Force
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && !f$act_1_vs_normalbet && f$act_7_vs_bet_1_to_150 && {onepair} && f$flop_Completed Set user_DCR_3wBTNvBB_TP_FB_Raised
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && !f$act_1_vs_normalbet && f$act_7_vs_bet_1_to_150 && {onepair} && f$flop_Completed Return true Force
// Every remaining branch in the written TP/OP tree is CALL or FOLD, never a
// raise. These guards prevent f$Raise_Committed from changing that ownership.
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_1_vs_normalbet && {onepair} && f$board_dry Return false Force
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && !f$act_1_vs_normalbet && f$act_7_vs_bet_1_to_150 && {onepair} && !f$flop_Completed Return false Force
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_9_vs_bet_150up && {onepair} Return false Force

'''
t=t.replace(marker,raise_guard+marker)

# 5) Insert call/fold ownership BEFORE Call_MicroBets / Odds-and-Outs.
call_marker='// Retro01 source-fidelity call/fold guards paired with the Raise guards.\n'
assert t.count(call_marker)==1
call_guard=f'''// ============================================================================
// TRANSVERSAL 02 — source-specific flop Facing-Bet CALL/FOLD ownership.
// Must run before f$Call_MicroBets and f$Odds_and_Outs.
// ============================================================================

// 3wBBvSB TP/OP dry, non-lowbet: explicit source CALL and history capture.
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && !f$act_6_vs_lowbet Set user_DCR_3wBBvSB_TP_FB_Line
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && !f$act_6_vs_lowbet Set user_DCR_3wBBvSB_TP_FB_Called
When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && {fb} && {onepair} && f$board_dry && !f$act_6_vs_lowbet Return true Force

// 3wBTNvBB one-pair source tree. Use the existing action buckets deliberately;
// ~76 is the project's operational representation of the written ~75 boundary.
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_1_vs_normalbet && {onepair} && f$board_dry Set user_DCR_3wBTNvBB_TP_FB_Called
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_1_vs_normalbet && {onepair} && f$board_dry Return true Force
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && !f$act_1_vs_normalbet && f$act_7_vs_bet_1_to_150 && {onepair} && !f$flop_Completed Set user_DCR_3wBTNvBB_TP_FB_Called
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && !f$act_1_vs_normalbet && f$act_7_vs_bet_1_to_150 && {onepair} && !f$flop_Completed Return true Force
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_9_vs_bet_150up && {onepair} && !f$flop_Completed Set user_DCR_3wBTNvBB_TP_FB_Called
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_9_vs_bet_150up && {onepair} && !f$flop_Completed Return true Force
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_9_vs_bet_150up && {onepair} && f$flop_Completed && (f$hand_Gutshot_or_BetterFDSD || HaveBackdoorFlushDraw) Set user_DCR_3wBTNvBB_TP_FB_Called
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_9_vs_bet_150up && {onepair} && f$flop_Completed && (f$hand_Gutshot_or_BetterFDSD || HaveBackdoorFlushDraw) Return true Force
// SOURCE: STARTING_STRATEGY + USER_HARDCODED: >150 CPL without additional equity folds.
When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_9_vs_bet_150up && {onepair} && f$flop_Completed && !(f$hand_Gutshot_or_BetterFDSD || HaveBackdoorFlushDraw) Return false Force

'''
t=t.replace(call_marker,call_guard+call_marker)

# 6) Pure-air microbet leak: exact 3wBBvSB SRP wet source requires qualifying backdoors.
existing='When f$game_3wBBvSB && f$pot_SingleRaised && !f$board_dry && f$hand_Air && !f$hand_Gutshot_or_BetterFDSD && (f$GoodBackDoors || f$MediumBackDoors) Return false Force\n'
assert t.count(existing)==1
extra=existing + '// SOURCE: STARTING_STRATEGY + USER_HARDCODED — pure A/K-high/air without qualifying backdoors folds here; block generic microbet calls.\n' + \
      'When f$game_3wBBvSB && f$pot_SingleRaised && !f$board_dry && f$hand_Air && !f$hand_Gutshot_or_BetterFDSD && !(f$GoodBackDoors || f$MediumBackDoors) Return false Force\n'
t=t.replace(existing,extra)

# 7) Exact one-third-stack flop raise sizing for 3wBTNvBB source Facing-Bet raise.
for block_name in ['##f$BetsizeFlopHeadsup##','##f$BetsizeFlopMultiway##']:
    idx=t.index(block_name)+len(block_name)
    insert=f'''\n// SOURCE: STARTING_STRATEGY + USER_HARDCODED — 3wBBvSB TP/OP raise vs flop Facing-Bet uses 50% pot.
// Keep this sizing state scoped to the initial Facing-Bet action so it cannot leak into a later flop re-raise decision.
When AmountToCall > 0 && {fb} && user_DCR_3wBBvSB_TP_FB_Raise50 RaiseBy 50% Force
// SOURCE: STARTING_STRATEGY + USER_HARDCODED — 3wBTNvBB TP/OP raise vs flop Facing-Bet targets one-third of effective stack.
// If the legal minimum raise already reaches the target, use all-in rather than an illegal under-raise.
When AmountToCall > 0 && {fb} && user_DCR_3wBTNvBB_TP_FB_Raised && (currentbet + 2*AmountToCall) >= 0.33*f$EffectiveStack_BKP BetMax Force
When AmountToCall > 0 && {fb} && user_DCR_3wBTNvBB_TP_FB_Raised RaiseTo (0.33*f$EffectiveStack_BKP) Force
'''
    t=t[:idx]+insert+t[idx:]

# 8) Turn continuation after 3wBTNvBB flop raise vs Facing Bet.
# 7b) Turn source-call ownership: prevent f$Raise_Committed from converting explicit 3wBBvSB draw calls into jams.
turn_raise='##f$turn_Raise##'
idx=t.index(turn_raise)+len(turn_raise)
turn_raise_guards='''
// TRANSVERSAL 03 — 3wBBvSB high-air/backdoor line improved to a real draw.
// SOURCE: STARTING_STRATEGY: after the flop call, versus a turn 2Bar call GS up
// to ~50% and OESD/FD up to ~75%. These are explicit CALLs, not jam prompts.
// SOURCE: USER_HARDCODED corroborates the call/fold ownership. Execute before
// f$Raise_Committed so stack geometry cannot silently rewrite CALL into all-in.
When f$game_3wBBvSB && user_DC6R_3wBBvSB_HighAirBackdoor_FlopCalled && (f$CF7_RealOESD || f$CF7_RealFD) && f$CF8_BetAtMost75 Return false Force
When f$game_3wBBvSB && user_DC6R_3wBBvSB_HighAirBackdoor_FlopCalled && f$hand_Gutshot && f$CF8_BetAtMost50 Return false Force
'''
t=t[:idx]+turn_raise_guards+t[idx:]

turn_cbet='##f$move_turn_cbet##'
idx=t.index(turn_cbet)+len(turn_cbet)
turn_btn='''\n// TRANSVERSAL 02 — 3wBTNvBB TP/OP after raising flop Facing-Bet.
// SOURCE: STARTING_STRATEGY: SPR >1.3 -> 75%; SPR <=1.3 -> all-in without
// good additional equity, 40% with OESD/FD. user_hardcoded corroborates the
// structure; DeepCrusher can represent the source 40% exactly, so it is used.
When f$game_3wBTNvBB && user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio > 1.3 Set user_Turn75
When f$game_3wBTNvBB && user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio > 1.3 Return true Force
When f$game_3wBTNvBB && user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio <= 1.3 && f$hand_SD_or_FD Set user_Turn40
When f$game_3wBTNvBB && user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio <= 1.3 && f$hand_SD_or_FD Return true Force
When f$game_3wBTNvBB && user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio <= 1.3 Set user_TurnMax
When f$game_3wBTNvBB && user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio <= 1.3 Return true Force

// TRANSVERSAL 02 — 3wBBvSB TP/OP Facing-Bet line after a flop raise.
// SOURCE: STARTING_STRATEGY + USER_HARDCODED: checked-to turn -> 50% non-CPL,
// 75% CPL. Record actual turn barrel for the source 25% one-pair river plan.
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && f$turn_Completed Set user_DCR_3wBBvSB_TP_FB_TurnBarreled
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && f$turn_Completed Set user_Turn75
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && f$turn_Completed Return true Force
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && !f$turn_Completed Set user_DCR_3wBBvSB_TP_FB_TurnBarreled
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && !f$turn_Completed Set user_Turn50
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && !f$turn_Completed Return true Force
'''
t=t[:idx]+turn_btn+t[idx:]

# Same BBvSB turn plan after flop CALL: villain checks, Hero is in Turn FloatBet node.
turn_float='##f$move_turn_floatbet##'
idx=t.index(turn_float)+len(turn_float)
turn_bb='''\n// TRANSVERSAL 02 — 3wBBvSB TP/OP Facing-Bet line after flop call, Villain checks turn.
// SOURCE: STARTING_STRATEGY + USER_HARDCODED: 50% non-CPL, 75% CPL.
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && f$turn_Completed Set user_DCR_3wBBvSB_TP_FB_TurnBarreled
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && f$turn_Completed Set user_Turn75
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && f$turn_Completed Return true Force
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && !f$turn_Completed Set user_DCR_3wBBvSB_TP_FB_TurnBarreled
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && !f$turn_Completed Set user_Turn50
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_Line && !f$turn_Completed Return true Force
'''
t=t[:idx]+turn_bb+t[idx:]

# 9) River 25 for surviving one-pair after the exact BBvSB line and actual turn barrel.
river_cbet='##f$move_river_cbet##'
idx=t.index(river_cbet)+len(river_cbet)
river='''\n// TRANSVERSAL 02 — 3wBBvSB TP/OP Facing-Bet -> turn barrel -> river check.
// SOURCE: STARTING_STRATEGY: "TP - lower the 3bar size to 25%". Apply only
// while current hand remains one pair; stronger improvements stay with existing
// value logic instead of being artificially down-sized.
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_TurnBarreled && (f$CF7_TopPairReal || f$CF7_OverPairReal) Set user_River25
When f$game_3wBBvSB && user_DCR_3wBBvSB_TP_FB_TurnBarreled && (f$CF7_TopPairReal || f$CF7_OverPairReal) Return true Force
'''
t=t[:idx]+river+t[idx:]

OUT.write_text(t,encoding='utf-8')
print('baseline',hashlib.sha256(BASE.read_bytes()).hexdigest(),len(BASE.read_bytes()))
print('candidate',hashlib.sha256(OUT.read_bytes()).hexdigest(),len(OUT.read_bytes()))
print('stale comments left',t.count(old))
print('blocks',len(re.findall(r'^##([^#\\n]+)##\\s*$',t,re.M)))
