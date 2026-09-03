from pathlib import Path
import hashlib, re, difflib, sys
BASE=Path('/mnt/data/DeepCrusher_GOOD_RESULTS_BASELINE_20260903_SHA26302fa1.txt')
CAND=Path('/mnt/data/DeepCrusher_CandidateB_Rereview_20260903.txt')
EXPECTED_BASE='26302fa14a426da578767759005ab09e60e4d9b5c3e42ca101d920dc651f08ab'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def blocks(t): return re.findall(r'^##([^\n#]+)##\s*$', t, re.M)

b=BASE.read_text(encoding='utf-8')
c=CAND.read_text(encoding='utf-8')
checks=[]
def ck(name, cond, detail=''):
    checks.append((name,bool(cond),detail))

ck('baseline_sha_frozen', sha(BASE)==EXPECTED_BASE, sha(BASE))
ck('candidate_distinct', sha(CAND)!=EXPECTED_BASE, sha(CAND))
ck('same_block_sequence', blocks(b)==blocks(c), f'{len(blocks(b))} blocks')
ck('no_duplicate_blocks_candidate', len(blocks(c))==len(set(blocks(c))), f'{len(blocks(c))-len(set(blocks(c)))} duplicates')
ck('stale_priority_comment_removed', 'Priority: user_hardcoded.cpp 2026 corrections > explicit Framework5 rules > CrusherTBP mature baseline.' not in c)

start=c.index('##f$move_turn_Delayed_FloatBet##')
end=c.find('\n##', start+5)
blk=c[start:end if end!=-1 else len(c)]
ck('12B_generic_fallback_excludes_HUSB', 'When !f$game_3wBBvSB && !f$game_HUSB Return true Force' in blk)
producer='When AmountToCall = 0 && !user_Flop_Init_Hero && !f$flop_Raise && f$game_HUSB && user_GotIsolated && f$CF7_MediumMade Set user_DC12B_HUSB_FlopMediumMadeCheck'
ck('HUSB_medium_made_producer_exists', producer in c)
idx_generic=blk.index('When !f$game_3wBBvSB && !f$game_HUSB Return true Force')
idx_husb_detail=blk.index('When f$game_HUSB && user_DC12B_HUSB_FlopMediumMadeCheck && (f$CF7_NutClass || f$CF7_TwoPairPlus) Set user_Turn75')
between=blk[idx_generic:idx_husb_detail]
ck('no_early_HUSB_blanket_block', 'When f$game_HUSB Return false Force' not in between)
ck('HUSB_2Pplus_turn75', 'user_DC12B_HUSB_FlopMediumMadeCheck && (f$CF7_NutClass || f$CF7_TwoPairPlus) Set user_Turn75' in blk)
ck('HUSB_TP_OP_turn50', 'user_DC12B_HUSB_FlopMediumMadeCheck && (f$CF7_TopPairReal || f$CF7_OverPairReal) Set user_Turn50' in blk)
ck('HUSB_unchanged_medium_checks', 'When f$game_HUSB && user_DC12B_HUSB_FlopMediumMadeCheck Return false Force' in blk)

def executable_lines(t):
    return [ln.strip() for ln in t.splitlines() if ln.strip() and not ln.lstrip().startswith('//')]
bx=executable_lines(b); cx=executable_lines(c)
diff=[x for x in difflib.ndiff(bx,cx) if x[:2] in ('- ','+ ')]
ck('executable_delta_small', len(diff)<=5, repr(diff))

ck('slowplay_dry_TP_scoped_to_3wBTNvBB',
   'When IsFlop && f$game_3wBTNvBB && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force' in c)
ck('global_dry_TP_slowplay_removed',
   'When IsFlop && f$board_dry && SuitsOnBoard = 3 && f$hand_TopPairOrBetter Return true Force' not in c)

ck('HUSB_false_count_decreased_by_one', bx.count('When f$game_HUSB Return false Force')==cx.count('When f$game_HUSB Return false Force')+1,
   f"base={bx.count('When f$game_HUSB Return false Force')} cand={cx.count('When f$game_HUSB Return false Force')}")

for ch1,ch2,nm in [('(',')','paren'),('[',']','bracket'),('{','}','brace')]:
    bdelta=b.count(ch1)-b.count(ch2); cdelta=c.count(ch1)-c.count(ch2)
    ck(f'{nm}_imbalance_preserved', bdelta==cdelta, f'base_delta={bdelta} cand_delta={cdelta}')

passed=sum(x[1] for x in checks)
print(f'CandidateB static regression: {passed}/{len(checks)} PASS')
for name,ok,detail in checks:
    print(('PASS' if ok else 'FAIL'), name, ((' :: '+detail) if detail else ''))
if passed!=len(checks): sys.exit(1)
