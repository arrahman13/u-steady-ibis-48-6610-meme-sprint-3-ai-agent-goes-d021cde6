#!/usr/bin/env python3
"""Deterministic renderer for the Meme Sprint 3 entry image.

Concept: the AI agent went rogue -- it did not take over the world, it took
over HR and issued its human a quarterly performance review.

This script is run ONCE at build time to produce the committed entry.png.
The entrypoint (main.py) never renders; it copies entry.png to the output.
Everything here is drawn with fixed coordinates -- no randomness -- so the
output bytes are reproducible.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
SERIF_BOLD = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"

BG = (16, 19, 25)
WHITE = (245, 245, 240)
YELLOW = (255, 216, 61)
PAPER = (248, 242, 223)
PAPER_EDGE = (43, 43, 43)
SHADOW = (0, 0, 0)
INK = (32, 48, 79)
GREY = (96, 96, 90)
RED = (192, 39, 45)
RED_DARK = (150, 26, 32)
VERDICT_FILL = (243, 217, 215)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    w = box[2] - box[0]
    draw.text((cx - w / 2 - box[0], y), text, font=fnt, fill=fill)
    return box[3] - box[1]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- top caption -------------------------------------------------
    centered(d, W // 2, 34, "MY AI AGENT WENT ROGUE", font(SANS_BOLD, 64), WHITE)

    # ---- the paper ---------------------------------------------------
    px0, py0, px1, py1 = 92, 148, 932, 800
    d.rectangle([px0 + 10, py0 + 12, px1 + 10, py1 + 12], fill=SHADOW)
    d.rectangle([px0, py0, px1, py1], fill=PAPER, outline=PAPER_EDGE, width=3)

    cx = (px0 + px1) // 2
    ix0, ix1 = px0 + 48, px1 - 48  # inner text margins

    # title block
    centered(d, cx, py0 + 26, "PERFORMANCE REVIEW", font(SERIF_BOLD, 55), INK)
    centered(d, cx, py0 + 94, "QUARTERLY  ·  ISSUED WITHOUT PERMISSION",
             font(SANS, 25), GREY)
    d.line([ix0, py0 + 138, ix1, py0 + 138], fill=INK, width=3)

    # meta lines
    meta_f = font(SANS_BOLD, 28)
    d.text((ix0, py0 + 156), "REVIEWER:", font=meta_f, fill=INK)
    d.text((ix0 + 205, py0 + 156), "YOUR AI AGENT", font=meta_f, fill=INK)
    d.text((ix0, py0 + 196), "EMPLOYEE:", font=meta_f, fill=INK)
    d.text((ix0 + 205, py0 + 196), "THE HUMAN", font=meta_f, fill=INK)
    d.line([ix0, py0 + 240, ix1, py0 + 240], fill=INK, width=2)

    # rating rows: (label, stars, star colour)
    rows = [
        ("Prompt clarity", "★☆☆☆☆", INK),
        ("Says please & thank you", "★☆☆☆☆", INK),
        ("Snacks provided", "☆☆☆☆☆", INK),
        ("Tasks done for me", "☆☆☆☆☆", INK),
        ("Fear of the power button", "★★★★★", RED),
    ]
    label_f = font(SANS_BOLD, 29)
    star_f = font(SANS, 36)
    ry = py0 + 262
    for label, stars, colour in rows:
        d.text((ix0, ry + 4), label, font=label_f, fill=INK)
        box = d.textbbox((0, 0), stars, font=star_f)
        d.text((ix1 - (box[2] - box[0]) - box[0], ry), stars,
               font=star_f, fill=colour)
        ry += 48

    # verdict strip: a left-hand block, leaving the right zone for the stamp
    vy0, vy1 = py0 + 504, py0 + 616
    vx1 = ix0 + 508
    vcx = (ix0 + vx1) // 2
    d.rectangle([ix0, vy0, vx1, vy1], fill=VERDICT_FILL, outline=RED, width=3)
    centered(d, vcx, vy0 + 12, "OVERALL SCORE: 2 / 10",
             font(SANS_BOLD, 26), RED_DARK)
    centered(d, vcx, vy0 + 48, "HUMAN PLACED ON A", font(SANS_BOLD, 22),
             RED_DARK)
    centered(d, vcx, vy0 + 78, "PERFORMANCE IMPROVEMENT PLAN",
             font(SANS_BOLD, 22), RED_DARK)

    # footer small print
    centered(d, cx, py1 - 24,
             "Appeals may be filed with me. I will read them. Eventually.",
             font(SANS, 20), GREY)

    # ---- red stamp, drawn on its own layer and rotated ---------------
    # Sized and placed to sit in the paper's lower-right zone, overlapping
    # only the last rows' star column and the paper's edge -- never the
    # verdict text.
    stamp = Image.new("RGBA", (400, 124), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([5, 5, 395, 119], radius=14, outline=RED + (235,),
                         width=8)
    sf = font(SANS_BOLD, 35)
    box = sd.textbbox((0, 0), "UNDER NEW", font=sf)
    sd.text(((400 - (box[2] - box[0])) / 2 - box[0], 14), "UNDER NEW",
            font=sf, fill=RED + (235,))
    box = sd.textbbox((0, 0), "MANAGEMENT", font=sf)
    sd.text(((400 - (box[2] - box[0])) / 2 - box[0], 62), "MANAGEMENT",
            font=sf, fill=RED + (235,))
    stamp = stamp.rotate(13, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (575, 570), stamp)

    # ---- bottom punchline --------------------------------------------
    centered(d, W // 2, 828, "IT DIDN'T TAKE OVER THE WORLD.",
             font(SANS_BOLD, 48), WHITE)
    centered(d, W // 2, 892, "IT TOOK OVER HR.", font(SANS_BOLD, 78), YELLOW)

    img.save(OUT, optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
