"""Concept C refined: three variations of the clock with HORA signed quietly, plus one soft touch (a recessed face).

Reuses the outline helpers in ../plex/_concepts.py. Needs fontTools + brotli and the Plex woff2 files:
    python _refined.py
Writes C1-/C2-/C3- SVGs (horizontal light/dark, stacked light/dark, icon, icon-flat) next to this file.
"""
import importlib.util, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('plex', os.path.join(HERE, '../plex/_concepts.py'))
plex = importlib.util.module_from_spec(spec); spec.loader.exec_module(plex)
text, cap, pt, f2, line, taper_arc, sector, svg = plex.text, plex.cap, plex.pt, plex.f2, plex.line, plex.taper_arc, plex.sector, plex.svg
SERIF, MONO = plex.SERIF, plex.MONO
N, NL, P, B, E, BL = plex.N, plex.NL, plex.P, plex.B, plex.E, plex.BL
G, GD = '#5C6170', '#B8BFCC'  # graphite on light, its pair on dark


def dial(cx, cy, R, uid, dark=False, arrow=False, signature=False, soft=True):
    """Bezel + face, four ticks, hands at 10:00 with the last two hours tinted.
    arrow: an ember rewind arc running along the bezel. signature: HORA in small mono on the lower face.
    soft: the one soft touch, a faint shadow inside the top of the face so it sits below the bezel."""
    face = R * .72
    o = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R:.2f}" fill="{NL if dark else N}"/>',
         f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face:.2f}" fill="{P}"/>']
    if soft:
        o.append(f'<defs><clipPath id="f{uid}"><circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face:.2f}"/></clipPath>'
                 f'<filter id="b{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{face * .05:.2f}"/></filter></defs>'
                 f'<g clip-path="url(#f{uid})"><circle cx="{cx:.2f}" cy="{cy + face * .06:.2f}" r="{face * 1.04:.2f}" fill="none" '
                 f'stroke="{N}" stroke-opacity=".22" stroke-width="{face * .12:.2f}" filter="url(#b{uid})"/></g>')
    o.append(f'<path d="{sector(cx, cy, 300, 360, face * .82)}" fill="{BL}"/>')
    for a in (0, 90, 180, 270):
        o.append(line(pt(cx, cy, a, face * .78), pt(cx, cy, a, face * .92), N, face * .08))
    if signature:
        s = face * .17
        _, w = text(MONO, 'HORA', s, 0, 0, track=.22)
        t, _ = text(MONO, 'HORA', s, cx - w / 2, cy + face * .55, track=.22, fill=G)
        o.append(t)
    o.append(line((cx, cy), pt(cx, cy, 300, face * .50), B, face * .13))
    o.append(line((cx, cy), pt(cx, cy, 0, face * .70), N, face * .09))
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{face * .11:.2f}" fill="{N}"/>')
    if arrow:
        o.append(f'<path d="{taper_arc(cx, cy, 62, -48, R * .86, R * .025, R * .075, R * .14)}" fill="{E}"/>')
    return ''.join(o)


VARIANTS = {
    'C1': dict(arrow=True, signature=True, label=False),   # signed, with the rewind arc
    'C2': dict(arrow=False, signature=True, label=False),  # signed, still: the tinted hours are the only cue
    'C3': dict(arrow=False, signature=False, label=True),  # HORA moves under Techne as a dial label
}
SIZE, PAD = 100, 10


def hora_label(x, base, width, size, fill):
    """H · O · R · A in mono, spread to `width`, with small round ticks between letters like hour marks."""
    advs = [text(MONO, ch, size, 0, 0)[1] for ch in 'HORA']
    step = (width - advs[-1]) / 3
    out = ''.join(text(MONO, ch, size, x + i * step, base, fill=fill)[0] for i, ch in enumerate('HORA'))
    capS = cap(MONO, size)
    for i in range(3):
        mx = x + i * step + advs[i] + (step - advs[i]) / 2
        out += f'<circle cx="{mx:.2f}" cy="{base - capS / 2:.2f}" r="{size * .07:.2f}" fill="{fill}"/>'
    return out


def horizontal(v, dark=False):
    o = VARIANTS[v]; ink = P if dark else N; mute = GD if dark else G
    capH = cap(SERIF, SIZE)
    if o['label']:
        small = SIZE * .34; capS = cap(MONO, small); lead = capH * .42
        block = capH + lead + capS; R = block * .62
        cy = PAD + R; cx = PAD + R; x = cx + R + SIZE * .28
        base1 = cy - block / 2 + capH
        t, w = text(SERIF, 'Techne', SIZE, x, base1, track=.01, fill=ink)
        t += hora_label(x + 2, base1 + lead + capS, w - 4, small, mute)
    else:
        R = capH * 1.05; cy = PAD + R; cx = PAD + R; x = cx + R + SIZE * .28
        t, w = text(SERIF, 'Techne', SIZE, x, cy + capH / 2, track=.01, fill=ink)
    body = dial(cx, cy, R, f'{v}h{int(dark)}', dark, o['arrow'], o['signature']) + t
    return svg(x + w + PAD, 2 * R + 2 * PAD, body, 'Techne Hora')


def stacked(v, dark=False):
    o = VARIANTS[v]; ink = P if dark else N; mute = GD if dark else G
    size = 64; R = 70; W = 300; capH = cap(SERIF, size)
    _, w = text(SERIF, 'Techne', size, 0, 0, track=.01)
    base = 2 * R + 34 + capH
    t, _ = text(SERIF, 'Techne', size, (W - w) / 2, base, track=.01, fill=ink)
    h = base + 14
    if o['label']:
        small = size * .34; capS = cap(MONO, small)
        t += hora_label((W - w) / 2 + 2, base + capH * .42 + capS, w - 4, small, mute); h += capH * .42 + capS
    return svg(W, h, dial(W / 2, R + 6, R, f'{v}s{int(dark)}', dark, o['arrow'], o['signature']) + t, 'Techne Hora')


def icon(v, flat=False):
    o = VARIANTS[v]
    # the signature is too small to read below about 48px, so the icon drops it
    return svg(64, 64, dial(32, 32, 30, f'{v}i{int(flat)}', arrow=o['arrow'], soft=not flat), 'Techne Hora icon')


if __name__ == '__main__':
    for v in VARIANTS:
        files = {f'{v}-horizontal-light.svg': horizontal(v), f'{v}-horizontal-dark.svg': horizontal(v, True),
                 f'{v}-stacked-light.svg': stacked(v), f'{v}-stacked-dark.svg': stacked(v, True),
                 f'{v}-icon.svg': icon(v), f'{v}-icon-flat.svg': icon(v, True)}
        for name, s in files.items():
            with open(os.path.join(HERE, name), 'w') as fh:
                fh.write(s)
