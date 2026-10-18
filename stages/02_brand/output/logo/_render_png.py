"""Render the PNG set from the SVGs that _build_logo.py writes.

Needs pillow and google-chrome (headless, isolated profile):
    .venv/bin/pip install pillow && .venv/bin/python _render_png.py
Each SVG is rendered once at 1024px with a transparent background, then downscaled.
"""
import os, subprocess, tempfile
from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(OUT, 'png')
PAPER = (0xFA, 0xF7, 0xF0, 255)

def render(svg, tmp):
    dst = os.path.join(tmp, os.path.basename(svg) + '.png')
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', f'--user-data-dir={tmp}/chrome',
                    '--hide-scrollbars', '--default-background-color=00000000', '--window-size=1024,1024',
                    f'--screenshot={dst}', 'file://' + svg], check=True, capture_output=True, timeout=60)
    return Image.open(dst).convert('RGBA')

def main():
    os.makedirs(PNG, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        mark = render(os.path.join(OUT, 'technehora-mark.svg'), tmp)
        fav = render(os.path.join(OUT, 'favicon.svg'), tmp)
        for s in (512, 1024):
            mark.resize((s, s), Image.LANCZOS).save(os.path.join(PNG, f'technehora-mark-{s}.png'))
        for s in (16, 32, 48):
            fav.resize((s, s), Image.LANCZOS).save(os.path.join(PNG, f'favicon-{s}.png'))
        # iOS shows transparency as black, so the touch icon sits on paper with a margin
        tile = Image.new('RGBA', (180, 180), PAPER)
        tile.alpha_composite(mark.resize((144, 144), Image.LANCZOS), (18, 18))
        tile.convert('RGB').save(os.path.join(PNG, 'apple-touch-icon.png'))

if __name__ == '__main__':
    main()
