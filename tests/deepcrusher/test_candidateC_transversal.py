from pathlib import Path
import hashlib, re, difflib, sys

BASE=Path('/mnt/data/DeepCrusher_GOOD_RESULTS_BASELINE_20260903_SHA26302fa1.txt')
CAND=Path('/mnt/data/DeepCrusher_CandidateC_Transversal_20260903.txt')
EXPECTED='26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def block_names(s): return re.findall(r'^##([^#\n]+)##\s*$', s, re.M)
def get_block(s,name):
    m=re.search(r'^##'+re.escape(name)+r'##\s*$',s,re.M); assert m,name
    e=re.search(r'^##[^#\n]+##\s*$',s[m.end():],re.M)
    return s[m.start():m.end()+(e.start() if e else len(s)-m.end())]
def exec_lines(s):
    return [x.strip() for x in s.splitlines() if x.strip() and not x.lstrip().startswith('//')]
def frefs(s): return set(re.findall(r'\bf\$[A-Za-z0-9_]+',s))

a=BASE.read_text(encoding='utf-8'); b=CAND.read_text(encoding='utf-8')
checks=[]
def ck(n,c,d=''): checks.append((n,bool(c),d))
ck('baseline_sha_frozen',sha(BASE)==EXPECTED,sha(BASE))
ck('candidate_distinct',sha(CAND)!=EXPECTED,sha(CAND))
ck('same_block_sequence',block_names(a)==block_names(b),f'{len(block_names(a))}/{len(block_names(b))}')
ck('1283_blocks',len(block_names(b))==1283,str(len(block_names(b))))
ck('no_duplicate_blocks',len(block_names(b))==len(set(block_names(b))))
ck('no_literal_template_braces','{fb}' not in b and '{onepair}' not in b)
new_exec_refs=frefs('\n'.join(exec_lines(b)))-frefs('\n'.join(exec_lines(a)))
ck('no_new_f_refs',new_exec_refs==set(),repr(sorted(new_exec_refs)))
ck('stale_priority_removed','Priority: user_hardcoded.cpp 2026 corrections > explicit Framework5 rules > CrusherTBP mature baseline.' not in b)
ck('slowplay_scope_fixed','When IsFlop && f$game_3wBTNvBB && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force' in b)
ck('global_dry_tp_slowplay_removed','When IsFlop && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force' not in b)

fr=get_block(b,'f$flop_Raise'); fc=get_block(b,'f$flop_Call')
ck('bbvsb_dry_large_call_guard_before_commit', fr.index('f$game_3wBBvSB') < fr.index('When f$Raise_Committed'), '')
line='When IsFlop && f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && (f$act_1_vs_normalbet || f$act_2_vs_highbet || f$act_3_vs_overbet) && (f$CF7_TopPairReal || f$CF7_OverPairReal) && f$board_dry && !f$act_6_vs_lowbet Return false Force'
ck('bbvsb_explicit_call_blocks_commit',line in fr and fr.index(line)<fr.index('When f$Raise_Committed'))
ck('btnvbb_all_nonraise_branches_block_commit', all(x in fr and fr.index(x)<fr.index('When f$Raise_Committed') for x in [
'When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_1_vs_normalbet && (f$CF7_TopPairReal || f$CF7_OverPairReal) && f$board_dry Return false Force',
'When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && !f$act_1_vs_normalbet && f$act_7_vs_bet_1_to_150 && (f$CF7_TopPairReal || f$CF7_OverPairReal) && !f$flop_Completed Return false Force',
'When IsFlop && f$game_3wBTNvBB && f$pot_SingleRaised && f$act_9_vs_bet_150up && (f$CF7_TopPairReal || f$CF7_OverPairReal) Return false Force']))

micro=fc.find('When f$Call_MicroBets')
ck('callmicro_exists',micro>=0)
for label, needle in [
('bbvsb_dry_large_call_before_micro','f$game_3wBBvSB && (f$pot_SingleRaised || f$pot_Limped) && (f$act_1_vs_normalbet || f$act_2_vs_highbet || f$act_3_vs_overbet) && (f$CF7_TopPairReal || f$CF7_OverPairReal) && f$board_dry && !f$act_6_vs_lowbet Return true Force'),
('btnvbb_150plus_cpl_noeq_fold_before_micro','f$act_9_vs_bet_150up && (f$CF7_TopPairReal || f$CF7_OverPairReal) && f$flop_Completed && !(f$hand_Gutshot_or_BetterFDSD || HaveBackdoorFlushDraw) Return false Force'),
('bbvsb_pure_air_fold_before_micro','f$pot_SingleRaised && !f$board_dry && f$hand_Air && !f$hand_Gutshot_or_BetterFDSD && !(f$GoodBackDoors || f$MediumBackDoors) Return false Force')]:
    pos=fc.find(needle); ck(label,pos>=0 and pos<micro,f'{pos}<{micro}')

for nm in ['f$BetsizeFlopHeadsup','f$BetsizeFlopMultiway']:
    z=get_block(b,nm)
    ck(nm+'_bbvsb_dedicated50','user_DCR_3wBBvSB_TP_FB_Raise50 RaiseBy 50% Force' in z)
    ck(nm+'_btn_target33','user_DCR_3wBTNvBB_TP_FB_Raised RaiseTo (0.33*f$EffectiveStack_BKP) Force' in z)
    ck(nm+'_sizing_scoped_first_bet',z.count('(f$act_1_vs_normalbet || f$act_2_vs_highbet || f$act_3_vs_overbet) && user_DCR_')>=3)

tr=get_block(b,'f$turn_Raise')
commit=tr.find('When f$Raise_Committed')
for label,needle2 in [
('turn_oesd_fd_call_blocks_commit','user_DC6R_3wBBvSB_HighAirBackdoor_FlopCalled && (f$CF7_RealOESD || f$CF7_RealFD) && f$CF8_BetAtMost75 Return false Force'),
('turn_gs_call_blocks_commit','user_DC6R_3wBBvSB_HighAirBackdoor_FlopCalled && f$hand_Gutshot && f$CF8_BetAtMost50 Return false Force')]:
    pos=tr.find(needle2); ck(label,pos>=0 and pos<commit,f'{pos}<{commit}')

tc=get_block(b,'f$move_turn_cbet'); tf=get_block(b,'f$move_turn_floatbet'); rc=get_block(b,'f$move_river_cbet')
ck('btn_turn_gt13_75','user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio > 1.3 Set user_Turn75' in tc)
ck('btn_turn_le13_draw_40','user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio <= 1.3 && f$hand_SD_or_FD Set user_Turn40' in tc)
ck('btn_turn_le13_no_draw_jam','user_DCR_3wBTNvBB_TP_FB_Raised && f$StackPotRatio <= 1.3 Set user_TurnMax' in tc)
for nm,z in [('turn_cbet',tc),('turn_float',tf)]:
    ck(nm+'_bbvsb_cpl75','user_DCR_3wBBvSB_TP_FB_Line && f$turn_Completed Set user_Turn75' in z)
    ck(nm+'_bbvsb_noncpl50','user_DCR_3wBBvSB_TP_FB_Line && !f$turn_Completed Set user_Turn50' in z)
ck('bbvsb_river_onepair25','user_DCR_3wBBvSB_TP_FB_TurnBarreled && (f$CF7_TopPairReal || f$CF7_OverPairReal) Set user_River25' in rc)

df=get_block(b,'f$move_turn_Delayed_FloatBet')
ck('delayed_generic_excludes_husb','When !f$game_3wBBvSB && !f$game_HUSB Return true Force' in df)
detail=df.find('user_DC12B_HUSB_FlopMediumMadeCheck && (f$CF7_NutClass || f$CF7_TwoPairPlus)')
ck('delayed_husb_detail_reachable',detail>=0 and 'When f$game_HUSB Return false Force' not in df[:detail])

ck('provenance_tags_present', all(x in b for x in ['SOURCE: STARTING_STRATEGY','SOURCE: USER_HARDCODED','SOURCE: RECONCILED']))

for L,R,n in [('(',')','paren'),('[',']','bracket'),('{','}','brace')]:
    ck(n+'_imbalance_preserved', a.count(L)-a.count(R)==b.count(L)-b.count(R),f'{a.count(L)-a.count(R)}/{b.count(L)-b.count(R)}')

changed=[]
for name in block_names(a):
    ea=exec_lines(get_block(a,name)); eb=exec_lines(get_block(b,name))
    if ea!=eb: changed.append(name)
expected={'f$flop_Raise','f$flop_Call','f$turn_Raise','f$move_turn_cbet','f$move_turn_floatbet','f$move_river_cbet','f$move_turn_Delayed_FloatBet','f$hand_slowplay','f$BetsizeFlopHeadsup','f$BetsizeFlopMultiway'}
ck('executable_changes_limited_to_10_blocks',set(changed)==expected,repr(changed))

passed=sum(ok for _,ok,_ in checks)
print(f'Candidate C transversal static regression: {passed}/{len(checks)} PASS')
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n,d)
print('candidate_sha',sha(CAND))
print('changed_blocks',changed)
if passed!=len(checks): sys.exit(1)
