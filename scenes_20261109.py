"""09.11.2026 — Omonat kapitalizatsiyasi (ovozsiz). python3 scenes_20261109.py OUT stills|render"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make as M
from make import W, H, LIME, WHITE, GREY, RED, FB, FX, FM, font, ease, back, fmt, text_c, glow_text

GREEN = (90, 210, 120)
ORDER = list("ABCDEF")
DUR = {"A": 2.5, "B": 4.0, "C": 5.5, "D": 5.5, "E": 5.0, "F": 4.0}
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
    text_c(d, 380, "10 mln · 18,8% · 3 yil", font(FB, 68), GREY, min(1, t / 0.1), img)
    bar_row(img, 500, "Foizni har oy yechsangiz", 5.64, 7.50, (110, 110, 110), min(1, t / 0.1), ease(t / 0.6), "+5,64 mln", WHITE)
    bar_row(img, 720, "Kapitalizatsiya bilan", 7.50, 7.50, LIME, fi(t, 0.3, 0.2), ease((t - 0.3) / 0.6), "+7,50 mln")
    badge(img, 1000 + 30 * (1 - fi(t, 0.9, 0.3)), "Farq: +1,86 mln so'm", GREEN, fi(t, 0.9, 0.3), size=74)
    if t > 1.5:
        glow_text(img, 1230, "Bir xil omonat. Bir xil foiz.", font(FX, 60), WHITE, fi(t, 1.5, 0.3))
    src(img, "Stavka: Markaziy bank, sentyabr 2026", min(1, t / 0.1))
    return img


def sB(t, tg, D):
    img, d = base(tg)
    text_c(d, 400, "Aholining uzoq muddatli", font(FB, 60), GREY, fi(t, 0), img)
    text_c(d, 475, "so'm omonatlari, o'rtacha", font(FB, 60), GREY, fi(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(220 * (0.6 + 0.4 * a)))
    glow_text(img, 580 - (sz - 220) / 2, "18,8%", font(FX, sz), LIME, min(1, t / 0.2))
    if t > 1.3:
        text_c(ImageDraw.Draw(img), 900, "qisqa muddatli: 15,6%", font(FB, 58), WHITE, fi(t, 1.3), img)
        text_c(ImageDraw.Draw(img), 985, "real daromadlilik: 8,9%", font(FB, 58), WHITE, fi(t, 1.7), img)
    src(img, "Manba: Markaziy bank, sentyabr 2026 yakuni", fi(t, 0.5))
    src(img, "(spot.uz, 09.11.2026)", fi(t, 0.5), y=1650)
    return img


def sC(t, tg, D):
    img, d = base(tg)
    glow_text(img, 340, "Kapitalizatsiya nima?", font(FX, 84), LIME, fi(t, 0))
    text_c(d, 470, "Foiz har oy omonatga qo'shiladi", font(FB, 54), WHITE, fi(t, 0.3), img)
    text_c(d, 540, "→ keyingi oy foizga ham foiz", font(FB, 54), WHITE, fi(t, 0.6), img)
    rows = [("1-oy", "10 000 000", "+156 667", 1.2), ("2-oy", "10 156 667", "+159 121", 1.9), ("3-oy", "10 315 788", "+161 614", 2.6)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (m, b, inc, t0) in enumerate(rows):
        aa = fi(t, t0)
        if aa <= 0:
            continue
        y = 680 + i * 200
        ld.rounded_rectangle((90, y, W - 90, y + 170), 28, fill=(24, 24, 24, int(255 * aa)), outline=(GREEN if i else (110, 110, 110)) + (int(200 * aa),), width=4)
        ld.text((130, y + 22), m, font=font(FB, 46), fill=GREY + (int(255 * aa),))
        ld.text((130, y + 80), b, font=font(FX, 62), fill=WHITE + (int(255 * aa),))
        fw = ld.textbbox((0, 0), inc, font=font(FX, 62))[2]
        ld.text((W - 130 - fw, y + 80), inc, font=font(FX, 62), fill=GREEN + (int(255 * aa),))
    img.alpha_composite(lay)
    if t > 3.4:
        text_c(ImageDraw.Draw(img), 1320, "Har oy foiz biroz kattaroq", font(FB, 56), LIME, fi(t, 3.4), img)
    src(img, "Hisob: 18,8% ÷ 12 = 1,567% oyiga", fi(t, 1.2))
    return img


def sD(t, tg, D):
    img, d = base(tg)
    text_c(d, 360, "10 mln dan foyda", font(FB, 64), GREY, fi(t, 0), img)
    data = [("1 yil", 1.88, 2.05), ("2 yil", 3.76, 4.52), ("3 yil", 5.64, 7.50)]
    mx = 7.50
    x0, wmax = 260, W - 400
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, s, c) in enumerate(data):
        t0 = 0.3 + i * 0.9
        aa = fi(t, t0)
        if aa <= 0:
            continue
        y = 500 + i * 280
        p = ease((t - t0) / 0.7)
        ld.text((90, y + 50), lab, font=font(FB, 52), fill=WHITE + (int(255 * aa),))
        ld.rounded_rectangle((x0, y, x0 + max(2, wmax * s / mx * p), y + 90), 18, fill=(110, 110, 110, int(235 * aa)))
        ld.rounded_rectangle((x0, y + 110, x0 + max(2, wmax * c / mx * p), y + 200), 18, fill=LIME + (int(235 * aa),))
        f = font(FX, 48)
        ld.text((x0 + max(2, wmax * s / mx * p) + 16, y + 18), f"{s:.2f}".replace(".", ","), font=f, fill=WHITE + (int(255 * aa),))
        ld.text((x0 + max(2, wmax * c / mx * p) + 16, y + 128), f"{c:.2f}".replace(".", ","), font=f, fill=LIME + (int(255 * aa),))
    img.alpha_composite(lay)
    a2 = fi(t, 0.2)
    lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    l2 = ImageDraw.Draw(lay2)
    l2.rounded_rectangle((90, 1370, 130, 1410), 8, fill=(110, 110, 110, int(255 * a2)))
    l2.text((150, 1362), "yechib olsangiz", font=font(FM, 44), fill=GREY + (int(255 * a2),))
    l2.rounded_rectangle((560, 1370, 600, 1410), 8, fill=LIME + (int(255 * a2),))
    l2.text((620, 1362), "kapitalizatsiya", font=font(FM, 44), fill=GREY + (int(255 * a2),))
    img.alpha_composite(lay2)
    text_c(ImageDraw.Draw(img), 1460, "mln so'm", font(FM, 44), GREY, a2, img)
    if t > 3.4:
        badge(img, 1540, "Muddat uzaygan sari farq o'sadi", GREEN, fi(t, 3.4), size=52)
    return img


def sE(t, tg, D):
    img, d = base(tg)
    glow_text(img, 360, "Tez qoida", font(FX, 110), LIME, fi(t, 0))
    a = fi(t, 0.4)
    if a > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((70, 540, W - 70, 860), 36, outline=LIME + (int(255 * a),), width=6, fill=(22, 22, 22, int(255 * a)))
        img.alpha_composite(lay)
        dd = ImageDraw.Draw(img)
        text_c(dd, 580, "Haqiqiy yillik foiz =", font(FB, 56), GREY, a, img)
        text_c(dd, 680, "(1 + F ÷ 12)¹² − 1", font(FX, 84), WHITE, fi(t, 0.7), img)
    if t > 1.6:
        text_c(ImageDraw.Draw(img), 960, "18,8% oylik kapitalizatsiya", font(FB, 58), GREY, fi(t, 1.6), img)
        glow_text(img, 1050, "≈ 20,5% yiliga", font(FX, 120), GREEN, fi(t, 1.9))
    if t > 3.0:
        text_c(ImageDraw.Draw(img), 1260, "Yechib olsangiz — 18,8% qoladi", font(FB, 54), WHITE, fi(t, 3.0), img)
    return img


def sF(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Omonat ochishdan oldin so'rang:", font(FB, 58), GREY, fi(t, 0), img)
    glow_text(img, 510, "Kapitalizatsiya bormi?", font(FX, 84), WHITE, fi(t, 0.1))
    badge(img, 700 + 30 * (1 - fi(t, 0.4)), "Saqlab qo'ying", LIME, fi(t, 0.4), size=64)
    text_c(ImageDraw.Draw(img), 900, "Omonatingiz necha foiz?", font(FB, 60), WHITE, fi(t, 0.9), img)
    text_c(ImageDraw.Draw(img), 985, "Izohda yozing", font(FB, 58), GREY, fi(t, 1.1), img)
    a4 = fi(t, 1.4)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    text_c(ImageDraw.Draw(img), 1600, "Hisob: stavka o'zgarmas, soliqsiz · bu maslahat emas", font(FM, 34), GREY, fi(t, 1.6), img)
    return img


FN = {"A": sA, "B": sB, "C": sC, "D": sD, "E": sE, "F": sF}


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
