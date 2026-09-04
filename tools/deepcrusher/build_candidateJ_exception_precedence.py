from pathlib import Path
import re

SRC = Path('DeepCrusher_CandidateI_HUSB_TurnRaise_20260903.txt')
DST = Path('DeepCrusher_CandidateJ_ExceptionPrecedence_20260903.txt')

def get_block(text, name):
    m = re.search(r'^##'+re.escape(name)+r'##\s*$', text, re.M)
    if not m:
        raise RuntimeError(f'block not found: {name}')
    n = re.search(r'^##[^\n#]+##\s*$', text[m.end():], re.M)
    end = m.end()+n.start() if n else len(text)
    return m.start(), end, text[m.start():end]

def replace_block(text, name, new):
    s,e,_=get_block(text,name)
    return text[:s]+new+text[e:]

def cut_between(block, start_marker, end_marker):
    s=block.index(start_marker)
    e=block.index(end_marker,s)
    chunk=block[s:e]
    return block[:s]+block[e:], chunk

def insert_after_line(block, exact_substring, chunk):
    pos=block.index(exact_substring)
    line_end=block.index('\n',pos)+1
    return block[:line_end]+'\n'+chunk.rstrip()+'\n'+block[line_end:]

text=SRC.read_text(encoding='utf-8')

# FLOP RAISE: normal Facing-Bet source tree follows exceptional commitment.
s,e,b=get_block(text,'f$flop_Raise')
start='// ============================================================================\n// TRANSVERSAL 02 - source-specific flop Facing-Bet ownership BEFORE commitment.'
end='// Gate 08 top-level guard.'
b,chunk=cut_between(b,start,end)
chunk=chunk.replace('source-specific flop Facing-Bet ownership BEFORE commitment.',
                    'source-specific flop Facing-Bet ownership AFTER exceptional commitment.')
chunk=chunk.replace('// Raise branches are captured here before generic commitment/fallback logic.',
                    '// Normal-geometry raise branches are applied only after exceptional commitment did not fire.')
chunk=chunk.replace('// Dry non-lowbet is an explicit CALL. This false guard is intentionally before\n// f$Raise_Committed so a large source-mandated call is not promoted to a jam.',
                    '// Dry non-lowbet is the normal-geometry CALL branch. If stack geometry is\n// committed, f$Raise_Committed has already taken precedence and may complete all-in.')
chunk=chunk.replace('// Every remaining branch in the written TP/OP tree is CALL or FOLD, never a\n// raise. These guards prevent f$Raise_Committed from changing that ownership.',
                    '// Every remaining branch in the written TP/OP tree is CALL or FOLD in normal\n// geometry. Exceptional committed geometry is intentionally handled first.')
b=insert_after_line(b,'When f$Raise_Committed',chunk)
text=replace_block(text,'f$flop_Raise',b)

# FLOP CALL: recent normal-price rules follow the explicit microbet exception.
s,e,b=get_block(text,'f$flop_Call')
start='// SOURCE: STARTING_STRATEGY + USER_HARDCODED - pure A/K-high/air without qualifying backdoors folds here; block generic microbet calls.'
end='// Retro01 source-fidelity call/fold guards paired with the Raise guards.'
b,chunk=cut_between(b,start,end)
chunk=chunk.replace('pure A/K-high/air without qualifying backdoors folds here; block generic microbet calls.',
                    'pure A/K-high/air without qualifying backdoors folds at normal prices; the exceptional microbet helper keeps precedence.')
chunk=chunk.replace('source-specific flop Facing-Bet CALL/FOLD ownership.\n// Must run before f$Call_MicroBets and f$Odds_and_Outs.',
                    'source-specific flop Facing-Bet CALL/FOLD ownership AFTER the exceptional microbet helper.')
b=insert_after_line(b,'When f$Call_MicroBets',chunk)
text=replace_block(text,'f$flop_Call',b)

# TURN RAISE: move recent post-QTo guards after f$Raise_Committed. Older baseline
# guards are deliberately untouched in this specific re-review.
s,e,b=get_block(text,'f$turn_Raise')
m1='// TRANSVERSAL 03 - 3wBBvSB high-air/backdoor line improved to a real draw.'
m1e='// Source-explicit 3wSBvBB delayed-check response.'
b,c1=cut_between(b,m1,m1e)
c1=c1.replace('// SOURCE: USER_HARDCODED corroborates the call/fold ownership. Execute before\n// f$Raise_Committed so stack geometry cannot silently rewrite CALL into all-in.',
              '// SOURCE: USER_HARDCODED corroborates the normal-geometry call/fold ownership.\n// Exceptional committed geometry is intentionally resolved first by f$Raise_Committed.')
m2='// ============================================================================\n// TRANSVERSAL 03 - 3wBTNvBB TP+ facing a turn donk after Hero actually CBet flop.'
m2e='// ============================================================================\n// TRANSVERSAL 05 - HUSB explicit call/fold ownership before f$Raise_Committed.'
b,c2=cut_between(b,m2,m2e)
c2=c2.replace('// These guards precede f$Raise_Committed so explicit CALL/FOLD ownership cannot\n// be converted into a generic jam by stack geometry.',
              '// These are normal-geometry actions. Exceptional committed geometry is\n// intentionally resolved first by f$Raise_Committed.')
m3='// ============================================================================\n// TRANSVERSAL 05 - HUSB explicit call/fold ownership before f$Raise_Committed.'
m3e='//-----------------------------------------------------------------------------//\n// Purpose: Routes the turn to the correct raise/bet strategy family.'
b,c3=cut_between(b,m3,m3e)
c3=c3.replace('HUSB explicit call/fold ownership before f$Raise_Committed.',
              'HUSB normal-geometry call/fold ownership after exceptional commitment.')
c3=c3.replace('// These lines never alter 2P+ value raises. They only prevent one-pair/draw\n// CALL/FOLD decisions from being promoted to a generic jam.',
              '// These lines govern normal geometry only. If f$Raise_Committed fired, the\n// intentionally exceptional all-in completion has already taken precedence.')
combined=c1.rstrip()+'\n\n'+c2.rstrip()+'\n\n'+c3.rstrip()+'\n'
b=insert_after_line(b,'When f$Raise_Committed',combined)
text=replace_block(text,'f$turn_Raise',b)

# TURN CALL: recent normal-strategy trees follow the microbet exception.
s,e,b=get_block(text,'f$turn_Call')
m='// ============================================================================\n// TRANSVERSAL 03 - paired CALL/FOLD side of the 3wBTNvBB TP+ turn-donk tree.'
me='//-----------------------------------------------------------------------------//\n// Purpose: Routes the turn to the correct call strategy family.'
b,chunk=cut_between(b,m,me)
chunk=chunk.replace('// Must execute before f$Call_MicroBets and generic initiative routing.',
                    '// Applies after the exceptional microbet helper; then before generic initiative routing.')
chunk=chunk.replace('HUSB source-owned turn CALL/FOLD before generic routing.',
                    'HUSB normal-geometry turn CALL/FOLD after the exceptional microbet helper.')
b=insert_after_line(b,'When f$Call_MicroBets',chunk)
text=replace_block(text,'f$turn_Call',b)

# RIVER CALL: recent normal/exploit river plans follow microbet price protection.
s,e,b=get_block(text,'f$river_Call')
m='// SOURCE: STARTING_STRATEGY - 3wBTNvBB TP+ vs >~50% turn donk on a paired turn:'
me='// Retro11 exact HUBB check/call guards.'
b,chunk=cut_between(b,m,me)
chunk=chunk.replace('// Old HUSB MP Q8: after Hero deliberately checks the turn, the profile read\n// determines the response to BB\'s river probe. These guards must execute before\n// generic microbet/initiative routing so the explicit source plan is preserved.',
                    '// Old HUSB MP Q8: after Hero deliberately checks the turn, the profile read\n// determines the response to BB\'s river probe at normal prices. The exceptional\n// microbet helper intentionally keeps precedence.')
b=insert_after_line(b,'When f$Call_MicroBets',chunk)
text=replace_block(text,'f$river_Call',b)

DST.write_text(text,encoding='utf-8')
print(DST)
