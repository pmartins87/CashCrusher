from pathlib import Path
import hashlib,re,sys

BASE=Path('DeepCrusher_GOOD_RESULTS_BASELINE_20260903_SHA26302fa1.txt')
PARENT=Path('DeepCrusher_CandidateI_HUSB_TurnRaise_20260903.txt')
CAND=Path('DeepCrusher_CandidateJ_ExceptionPrecedence_20260903.txt')
EXPECTED_BASE='26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def blocks(t): return re.findall(r'^##([^\n#]+)##\s*$',t,re.M)
def get(t,name):
    m=re.search(r'^##'+re.escape(name)+r'##\s*$',t,re.M); assert m
    n=re.search(r'^##[^\n#]+##\s*$',t[m.end():],re.M); e=m.end()+n.start() if n else len(t)
    return t[m.start():e]
def exe_block_diffs(a,b):
    names=blocks(a); out=[]
    for n in names:
        aa='\n'.join(x.strip() for x in get(a,n).splitlines() if x.strip() and not x.lstrip().startswith('//'))
        bb='\n'.join(x.strip() for x in get(b,n).splitlines() if x.strip() and not x.lstrip().startswith('//'))
        if aa!=bb: out.append(n)
    return out

a=BASE.read_text(errors='replace'); p=PARENT.read_text(errors='replace'); c=CAND.read_text(errors='replace')
checks=[]
def ck(n,v,d=''): checks.append((n,bool(v),d))
ck('baseline_sha',sha(BASE)==EXPECTED_BASE,sha(BASE))
ck('candidate_distinct_parent',sha(CAND)!=sha(PARENT),sha(CAND))
ck('same_block_sequence_parent',blocks(p)==blocks(c),str(len(blocks(c))))
ck('same_block_sequence_baseline',blocks(a)==blocks(c),str(len(blocks(c))))
ck('no_duplicate_blocks',len(blocks(c))==len(set(blocks(c))))
ck('lowbet_margin_preserved','##f$act_6_vs_lowbet##' in c)
ck('normal_high_margin_preserved','##f$act_1_vs_normalbet##' in c and '##f$act_2_vs_highbet##' in c)
fr=get(c,'f$flop_Raise')
ck('flop_commit_before_recent_FB',fr.index('When f$Raise_Committed') < fr.index('TRANSVERSAL 02 - source-specific flop Facing-Bet ownership AFTER exceptional commitment'))
fc=get(c,'f$flop_Call')
ck('flop_microbet_before_recent_FB',fc.index('When f$Call_MicroBets') < fc.index('TRANSVERSAL 02 - source-specific flop Facing-Bet CALL/FOLD ownership AFTER'))
ck('flop_microbet_before_recent_air_fold',fc.index('When f$Call_MicroBets') < fc.index('pure A/K-high/air without qualifying backdoors folds at normal prices'))
tr=get(c,'f$turn_Raise')
ck('turn_commit_before_BBvSB_draw',tr.index('When f$Raise_Committed') < tr.index('TRANSVERSAL 03 - 3wBBvSB high-air/backdoor'))
ck('turn_commit_before_BTNvBB_donk',tr.index('When f$Raise_Committed') < tr.index('TRANSVERSAL 03 - 3wBTNvBB TP+ facing a turn donk'))
ck('turn_commit_before_HUSB',tr.index('When f$Raise_Committed') < tr.index('TRANSVERSAL 05 - HUSB normal-geometry'))
tc=get(c,'f$turn_Call')
ck('turn_microbet_before_recent_trees',tc.index('When f$Call_MicroBets') < tc.index('TRANSVERSAL 03 - paired CALL/FOLD'))
rc=get(c,'f$river_Call')
ck('river_microbet_before_recent_BTNvBB_plan',rc.index('When f$Call_MicroBets') < rc.index('SOURCE: STARTING_STRATEGY - 3wBTNvBB TP+ vs >~50% turn donk'))
ck('river_microbet_before_recent_HUSB_plan',rc.index('When f$Call_MicroBets') < rc.index('Old HUSB MP Q8'))
ck('QTo_class_call_exists','f$game_3wBBvSB' in fc and 'f$CF7_StrongMade && f$board_dry && !f$act_6_vs_lowbet Return true Force' in fc)
ck('QTo_raise_false_exists_after_commit','f$CF7_StrongMade && f$board_dry && !f$act_6_vs_lowbet Return false Force' in fr)
ck('slowplay_scope_fix','When IsFlop && f$game_3wBTNvBB && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force' in c)
ck('delayed_float_fix','When !f$game_3wBBvSB && !f$game_HUSB Return true Force' in c)
ck('stale_air_river_removed','When user_3wBTN_Had_Air_OTF Return true Force' not in c)
ck('current_strength_river_fix','user_RaisedFlopTP_3wBBvBTN' in c and 'f$CF7_TopPairReal' in c)
changed=exe_block_diffs(p,c)
ck('I_to_J_changed_blocks_expected',set(changed)=={'f$flop_Raise','f$flop_Call','f$turn_Raise','f$turn_Call','f$river_Call'},repr(changed))
for L,R,n in [('(',')','paren'),('[',']','bracket'),('{','}','brace')]:
    ck(n+'_imbalance_preserved',p.count(L)-p.count(R)==c.count(L)-c.count(R))
print(f'CandidateJ regression: {sum(x[1] for x in checks)}/{len(checks)} PASS')
for n,v,d in checks: print('PASS' if v else 'FAIL',n,d)
if not all(v for _,v,_ in checks): sys.exit(1)
