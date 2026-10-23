"""Round 4 (owner, 2026-10-22: "make HORA a bit simpler"). Three steps down from F, each drawn the same at every
size, so there is no separate small version to keep in step:
I: F made plain: no grooves, plain R bowl, solid A roof, one step (today's small logo used at every size).
J: slab tops: the cushion goes and the shafts stop tapering; a plain slab caps each column; one step.
K: bare: J without the step; the slabs alone say "column".
    ~/.cache/th-logo-venv/bin/python _simple.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '../..')))
import _build_logo as L

I = dict(L.SMALL)
J = dict(C=20, flute=0, steps=1, gap=.40, slab=True)
K = dict(J, steps=0)
SLAB = 7

def column(x, s):
    if not s.get('slab'): return _doric_column(x, s)
    C = s['C']; aw = C + 8
    return L._r(x + C / 2 - aw / 2, 0, aw, SLAB) + L._r(x, SLAB, C, L.DH - SLAB)

def A(s):
    if not s.get('slab'): return _doric_A(s)
    C = s['C']; W = 58 + (C - 17) * 1.5; peak, lean = 24, 12; y0 = peak + 6
    o = L._poly([(W / 2, 0), (W + 2, peak), (W + 2, y0), (-2, y0), (-2, peak)])
    o += L._poly([(lean, y0), (lean + C, y0), (C, L.DH), (0, L.DH)])
    o += L._poly([(W - lean - C, y0), (W - lean, y0), (W, L.DH), (W - C, L.DH)])
    return o + L._r(C + 1, 66, W - 2 * C - 2, 8 + (C - 17) * .5), W

_doric_column, _doric_A = L._column, L._A
L._column, L._A = column, A                      # hora() looks these up at call time

def write(name, w, h, body):
    with open(os.path.join(HERE, name), 'w') as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="Techne Hora">{body}</svg>\n')

for key, s in (('I', I), ('J', J), ('K', K)):
    for theme, dark in (('light', False), ('dark', True)):
        w, h, body = L.horizontal(dark, s=s)
        write(f'{key}-horizontal-{theme}.svg', w, h, body.replace('id="f', f'id="f{key}').replace('#f', f'#f{key}')
              .replace('id="b', f'id="b{key}').replace('#b', f'#b{key}'))

# the four letters alone, large, for judging the drawing
for key, s in (('F', L.FULL), ('I', I), ('J', J), ('K', K)):
    d, hh = L.hora(0, 10, 420, 100, L.N, s)
    write(f'{key}-letters.svg', 420, hh + 20, d)
print('ok')
