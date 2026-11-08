"""08.11.2026 — Ipoteka muddati (ovozsiz zaxira). python3 scenes_20261108.py OUT stills|render"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make as M
from make import W, H, LIME, WHITE, GREY, RED, FB, FX, FM, font, ease, back, fmt, text_c, glow_text

GREEN = (90, 210, 120)
ORDER = list("ABCDEFG")
DUR = {"A": 2.5, "B": 4.0, "C": 5.0, "D": 4.0, "E": 5.5, "F": 4.0, "G": 3.5}
TOTAL = sum(DUR.values())


def base(tg):
    return M.base(tg, TOTAL)


def fi(t, t0, d=0.35):
    return ease((t - t0) / d)


def badge(img, y, label, color, a, size=62):
    if a <= 0:
        return
    f = font(FX, size)
    bb = ImageDraw.Draw(img).textbbox((0, 0), label, font=f)
    bw, bh = bb[2] - bb[0] + 90, size + 54
    bx = (W - bw) / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((bx, y, bx + bw, y + bh), 28, fill=color + (int(255 * a),))
    img.alpha_composite(lay)
    text_c(ImageDraw.Draw(img), y + 22, label, f, (11, 11, 11) if color in (LIME, GREEN) else WHITE, a, img)


def src(img, s, a, y=1600):
    text_c(ImageDraw.Draw(img), y, s, font(FM, 38), GREY, a, img)


def mln(v):
    return f"{v/1e6:.2f}".replace(".", ",") + " mln"


def bar_row(img, y, lab, val, maxv, col, a, p, label, txtcol=(11, 11, 11)):
    if a <= 0:
        return
    x0, wmax = 120, W - 240
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.text((x0, y), lab, font=font(FB, 52), fill=WHITE + (int(255 * a),))
    bw = max(2, wmax * (val / maxv) * p)
    ld.rounded_rectangle((x0, y + 80, x0 + bw, y + 160), 20, fill=col + (int(235 * a),))
    ld.text((x0 + 24, y + 88), label, font=font(FX, 56), fill=txtcol + (int(255 * a),))
    img.alpha_composite(lay)


def sA(t, tg, D):  # hook: raqam 0-soniyada
    img, d = base(tg)
    text_c(d, 430, "500 mln ipoteka · 20 yil", font(FB, 68), GREY, min(1, t / 0.1), img)
    glow_text(img, 560, "2,1 mlrd so'm", font(FX, 150), RED, min(1, t / 0.1))
    text_c(ImageDraw.Draw(img), 760, "qaytarasiz", font(FB, 70), WHITE, fi(t, 0.2, 0.2), img)
    badge(img, 920 + 30 * (1 - fi(t, 0.7, 0.3)), "4,2 baravar ko'p", RED, fi(t, 0.7, 0.3), size=80)
    if t > 1.5:
        glow_text(img, 1160, "Muddatni qisqartirsangiz?", font(FX, 64), LIME, fi(t, 1.5, 0.3))
    return img


def sB(t, tg, D):
    img, d = base(tg)
    text_c(d, 400, "Ipoteka stavkasi (bank mablag'i)", font(FB, 56), GREY, fi(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(200 * (0.6 + 0.4 * a)))
    glow_text(img, 500 - (sz - 200) / 2, "20,7%", font(FX, sz), WHITE, min(1, t / 0.2))
    if t > 1.2:
        text_c(ImageDraw.Draw(img), 800, "500 mln so'm · 20 yil", font(FB, 62), GREY, fi(t, 1.2), img)
        text_c(ImageDraw.Draw(img), 900, "oylik to'lov:", font(FB, 56), GREY, fi(t, 1.4), img)
        v = 8_769_655 * ease((t - 1.5) / 1.0)
        glow_text(img, 990, fmt(v) + " so'm", font(FX, 104), LIME, fi(t, 1.5))
    src(img, "Manba: Markaziy bank, yanvar–avgust 2026", fi(t, 0.5))
    return img


def sC(t, tg, D):
    img, d = base(tg)
    text_c(d, 360, "Oylik to'lov", font(FB, 62), GREY, fi(t, 0), img)
    bar_row(img, 450, "20 yil", 8_769_655, 9_895_967, (110, 110, 110), fi(t, 0.1), ease((t - 0.1) / 0.7), mln(8_769_655), WHITE)
    bar_row(img, 650, "10 yil", 9_895_967, 9_895_967, LIME, fi(t, 0.5), ease((t - 0.5) / 0.7), mln(9_895_967))
    if t > 2.0:
        text_c(ImageDraw.Draw(img), 920, "Jami qaytarasiz", font(FB, 62), GREY, fi(t, 2.0), img)
        bar_row(img, 1010, "20 yil", 2_104_717_315, 2_104_717_315, RED, fi(t, 2.1), ease((t - 2.1) / 0.7), "2 105 mln", WHITE)
        bar_row(img, 1210, "10 yil", 1_187_516_097, 2_104_717_315, GREEN, fi(t, 2.5), ease((t - 2.5) / 0.7), "1 188 mln")
    return img


def sD(t, tg, D):
    img, d = base(tg)
    text_c(d, 450, "Oyiga atigi", font(FB, 70), GREY, fi(t, 0), img)
    glow_text(img, 550, "+1,13 mln", font(FX, 150), WHITE, fi(t, 0.1))
    text_c(ImageDraw.Draw(img), 780, "ko'proq to'lasangiz —", font(FB, 64), GREY, fi(t, 0.6), img)
    if t > 1.2:
        v = 917_201_218 * ease((t - 1.3) / 1.2)
        glow_text(img, 900, fmt(v / 1e6) + " mln", font(FX, 140), GREEN, fi(t, 1.2))
        text_c(ImageDraw.Draw(img), 1090, "so'm tejaysiz", font(FX, 76), GREEN, fi(t, 1.4), img)
    return img


def sE(t, tg, D):
    img, d = base(tg)
    glow_text(img, 360, "Tez qoida", font(FX, 110), LIME, fi(t, 0))
    a = fi(t, 0.4)
    if a > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((70, 540, W - 70, 1000), 36, outline=LIME + (int(255 * a),), width=6, fill=(22, 22, 22, int(255 * a)))
        img.alpha_composite(lay)
        dd = ImageDraw.Draw(img)
        text_c(dd, 580, "Har 1 mln qarzga oyiga", font(FB, 56), GREY, a, img)
        text_c(dd, 680, "20 yil ≈ 17,5 ming", font(FX, 78), WHITE, fi(t, 0.7), img)
        text_c(dd, 790, "10 yil ≈ 19,8 ming", font(FX, 78), LIME, fi(t, 1.1), img)
        text_c(dd, 900, "(stavka 20,7% bo'lsa)", font(FM, 44), GREY, fi(t, 1.3), img)
    if t > 2.2:
        text_c(ImageDraw.Draw(img), 1080, "Jami = oylik × 12 × yil", font(FX, 70), WHITE, fi(t, 2.2), img)
    if t > 3.2:
        text_c(ImageDraw.Draw(img), 1200, "500 mln → 500 × 17,5 ming", font(FB, 54), GREY, fi(t, 3.2), img)
        text_c(ImageDraw.Draw(img), 1275, "= 8,75 mln oyiga", font(FB, 54), GREY, fi(t, 3.4), img)
    return img


def sF(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Ortiqcha to'lov (foiz)", font(FB, 62), GREY, fi(t, 0), img)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, val, col, t0) in enumerate([("10 yil", "688 mln", GREEN, 0.1), ("20 yil", "1 605 mln", RED, 0.6)]):
        aa = fi(t, t0)
        y = 540 + i * 250
        ld.rounded_rectangle((90, y, W - 90, y + 200), 30, fill=(24, 24, 24, int(255 * aa)), outline=col + (int(200 * aa),), width=4)
        ld.text((140, y + 30), lab, font=font(FB, 50), fill=GREY + (int(255 * aa),))
        ld.text((140, y + 95), val, font=font(FX, 80), fill=col + (int(255 * aa),))
    img.alpha_composite(lay)
    if t > 1.4:
        badge(img, 1100, "Muddat 2× → foiz 2,3×", LIME, fi(t, 1.4), size=66)
    if t > 2.4:
        text_c(ImageDraw.Draw(img), 1300, "Hisob: annuitet, stavka o'zgarmas · bu maslahat emas", font(FM, 36), GREY, fi(t, 2.4), img)
    return img


def sG(t, tg, D):
    img, d = base(tg)
    glow_text(img, 520, "Qisqa muddat = arzon uy", font(FX, 78), WHITE, fi(t, 0))
    badge(img, 700 + 30 * (1 - fi(t, 0.3)), "Saqlab qo'ying", LIME, fi(t, 0.3), size=64)
    text_c(ImageDraw.Draw(img), 900, "Siz necha yilga olgansiz?", font(FB, 60), WHITE, fi(t, 0.8), img)
    text_c(ImageDraw.Draw(img), 985, "Izohda yozing", font(FB, 58), GREY, fi(t, 1.0), img)
    a4 = fi(t, 1.3)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    return img


FN = {"A": sA, "B": sB, "C": sC, "D": sD, "E": sE, "F": sF, "G": sG}


def mk(k):
    D = DUR[k]
    return lambda t, tg: FN[k](t, tg, D)


if __name__ == "__main__":
    OUT, mode = sys.argv[1], sys.argv[2]
    os.makedirs(OUT, exist_ok=True)
    M.OUT = OUT
    st, files = 0, []
    for k in ORDER:
        D = DUR[k]
        if mode == "stills":
            mk(k)(D * 0.92, st + D * 0.92).convert("RGB").save(os.path.join(OUT, f"v{k}_still.jpg"), quality=85)
        else:
            files.append(M.render("v" + k, D, mk(k), st))
        st += D
    if mode != "stills":
        with open(os.path.join(OUT, "list.txt"), "w") as f:
            for fl in files:
                f.write(f"file '{os.path.abspath(fl)}'\n")
    print("total", TOTAL)
