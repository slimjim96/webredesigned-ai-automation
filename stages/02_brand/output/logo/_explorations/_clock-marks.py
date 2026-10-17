import math, sys, os
N,ND,NL,P,B,BL='#1B2A4A','#111B31','#2B4374','#FAF7F0','#A63D2A','#E07A5F'
def pt(deg,r,c=32):
    a=math.radians(deg); return (c+r*math.sin(a), c-r*math.cos(a))
f=lambda p:f"{p[0]:.2f} {p[1]:.2f}"
def sector(a0,a1,r):  # clockwise from a0 to a1
    s,e=pt(a0,r),pt(a1,r); large=1 if (a1-a0)%360>180 else 0
    return f"M32 32L{f(s)}A{r} {r} 0 {large} 1 {f(e)}Z"
def taper_arc(a_start,a_end,r,w0,w1,head=6.5,steps=48):
    """counter-clockwise from a_start down to a_end; width w0->w1; arrowhead at end"""
    outer,inner=[],[]
    for i in range(steps+1):
        t=i/steps; a=a_start+(a_end-a_start)*t; w=w0+(w1-w0)*t
        outer.append(pt(a,r+w/2)); inner.append(pt(a,r-w/2))
    # arrowhead: extend in travel direction
    ae=a_end; tip=pt(ae-head*360/(2*math.pi*r)*1.0, r)
    hw=w1*1.25+1.5
    d="M"+f(outer[0])+"".join("L"+f(p) for p in outer[1:])
    d+="L"+f(pt(ae,r+hw))+"L"+f(tip)+"L"+f(pt(ae,r-hw))
    d+="".join("L"+f(p) for p in reversed(inner))+"Z"
    return d
def base(id):
    return (f'<defs><radialGradient id="{id}g" cx="35%" cy="28%" r="80%"><stop offset="0" stop-color="{NL}"/><stop offset=".55" stop-color="{N}"/><stop offset="1" stop-color="{ND}"/></radialGradient>'
            f'<linearGradient id="{id}a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E9E1D0"/></linearGradient>'
            f'<linearGradient id="{id}w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BL}"/><stop offset="1" stop-color="{B}"/></linearGradient></defs>'
            f'<circle cx="32" cy="32" r="30" fill="url(#{id}g)"/><circle cx="32" cy="32" r="29.4" fill="none" stroke="#FFFFFF" stroke-opacity=".10" stroke-width="1.2"/>')
def hands(minute_deg, hour_deg, mcol, hcol, ml=14, hl=9, mw=3.2, hw=4):
    m,h=pt(minute_deg,ml),pt(hour_deg,hl)
    return (f'<path d="M32 32L{f(h)}" stroke="{hcol}" stroke-width="{hw}" stroke-linecap="round"/>'
            f'<path d="M32 32L{f(m)}" stroke="{mcol}" stroke-width="{mw}" stroke-linecap="round"/>')
def pin(col,ring):
    return f'<circle cx="32" cy="32" r="3.2" fill="{ring}"/><circle cx="32" cy="32" r="1.4" fill="{col}"/>'

def reclaimed(id='ra'):
    # gained-back wedge 10->12, tapered arrow over the top, counter-clockwise
    s=base(id)
    s+=f'<circle cx="32" cy="32" r="19.5" fill="{ND}" fill-opacity=".45"/>'
    s+=f'<path d="{sector(300,360,19.5)}" fill="url(#{id}w)"/>'
    s+=f'<path d="{taper_arc(70,-75,23.5,1.2,4.2)}" fill="url(#{id}a)"/>'
    s+=hands(0,300,P,P,ml=17,hl=13,mw=3.2,hw=3.2)  # minute hand at 12, wedge edge does the hour
    s+=pin(B,P)
    return s
def dial(id='da'):
    # paper wall-clock face with drop shadow; brick tapered arrow wrapping it
    s=base(id)
    s+=f'<circle cx="33.4" cy="34" r="19" fill="{ND}" opacity=".7"/>'
    s+=f'<circle cx="32" cy="32" r="19" fill="url(#{id}a)"/>'
    s+=f'<circle cx="32" cy="32" r="19" fill="none" stroke="{N}" stroke-opacity=".15" stroke-width="1"/>'
    s+=f'<path d="{sector(300,360,15.5)}" fill="{BL}" fill-opacity=".28"/>'
    for a in range(0,360,30):
        r0=15.8 if a%90==0 else 16.6; p0,p1=pt(a,r0),pt(a,17.6)
        s+=f'<path d="M{f(p0)}L{f(p1)}" stroke="{N}" stroke-width="{1.6 if a%90==0 else 1}" stroke-linecap="round" stroke-opacity=".75"/>'
    s+=hands(0,300,N,B,ml=13,hl=9.5,mw=2.6,hw=3.6)
    s+=f'<path d="{taper_arc(55,-95,25.5,1,3.6,head=6)}" fill="{BL}"/>'
    s+=pin(P,N)
    return s
def sweep(id='sa'):
    # hand sweeping backwards leaves a fading trail: time being pulled back
    s=base(id)
    s+=f'<circle cx="32" cy="32" r="23" fill="none" stroke="{P}" stroke-opacity=".9" stroke-width="2.4"/>'
    n=10
    for i in range(n):  # trail from 60deg (2 o'clock) back to 300 (10 o'clock); strongest near the hand
        a0=300+ (120/n)*i; a1=a0+120/n+0.6
        op=0.85*(1-i/n)**1.6
        s+=f'<path d="{sector(a0,a1,20.5)}" fill="{BL}" fill-opacity="{op:.3f}"/>'
    for a in (0,90,180,270):
        p0,p1=pt(a,23),pt(a,19.8); s+=f'<path d="M{f(p0)}L{f(p1)}" stroke="{P}" stroke-width="2.4" stroke-linecap="round"/>'
    s+=hands(300,0,P,P,ml=19,hl=10,mw=3.2,hw=4)
    # small chevron on the outer ring showing direction (counter-clockwise at 10 o'clock)
    s+=f'<path d="{taper_arc(330,292,23,2.4,2.4,head=5,steps=8)}" fill="{P}"/>'
    s+=pin(B,P)
    return s
out=sys.argv[1]
for name,fn in (('reclaimed',reclaimed),('dial',dial),('sweep',sweep)):
    body=fn('h'+name[0])
    open(os.path.join(out,f'hourback-{name}-mark.svg'),'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Hourback mark">{body}</svg>\n')
