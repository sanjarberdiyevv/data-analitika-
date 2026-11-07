import os, sys, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import make as M
from make import W, H, LIME, WHITE, GREY, RED, FB, FX, FM, font, ease, back, fmt, text_c, glow_text

GREEN = (90, 210, 120)
TM = json.load(open("/home/claude/val_out/timing.json"))
G = TM["groups"]
TOTAL = TM["total"]
ORDER = list("ABCDEFG")
STARTS = [0.0] + [g[0] for g in G[1:]]
DUR = {k: (STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL) - STARTS[i] for i, k in enumerate(ORDER)}
# sentence onsets relative to each scene start
REL = {k: [round(x - STARTS[i], 2) for x in G[i]] for i, k in enumerate(ORDER)}


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


def src(img, s, a):
    text_c(ImageDraw.Draw(img), 1600, s, font(FM, 38), GREY, a, img)


def bar_row(img, y, lab, val, maxv, col, a, p, txtcol=(11, 11, 11)):
    if a <= 0:
        return
    x0, wmax = 120, W - 240
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.text((x0, y), lab, font=font(FB, 52), fill=WHITE + (int(255 * a),))
    bw = max(2, wmax * (val / maxv) * p)
    ld.rounded_rectangle((x0, y + 80, x0 + bw, y + 160), 20, fill=col + (int(235 * a),))
    ld.text((x0 + 24, y + 88), f"{val/1e6:.2f}".replace(".", ",") + " mln", font=font(FX, 56), fill=txtcol + (int(255 * a),))
    img.alpha_composite(lay)


def sA(t, tg, D):  # hook
    img, d = base(tg)
    r = REL["A"]
    text_c(d, 430, "1 yil oldin dollarga aylantirdi:", font(FB, 58), GREY, fi(t, 0, 0.2), img)
    glow_text(img, 525, "10 000 000 so'm", font(FX, 106), WHITE, min(1, t / 0.15))
    text_c(ImageDraw.Draw(img), 690, "→ $ omonat", font(FB, 64), GREY, fi(t, 0.3), img)
    badge(img, 840 + 30 * (1 - fi(t, 0.9)), "−1 330 000 so'm", RED, fi(t, 0.9), size=86)
    text_c(ImageDraw.Draw(img), 1040, "so'mda saqlaganga nisbatan", font(FB, 50), GREY, fi(t, 1.3), img)
    if len(r) > 1 and t > r[1] - 0.1:
        glow_text(img, 1200, "Nega?", font(FX, 130), LIME, fi(t, r[1] - 0.1))
    return img


def sB(t, tg, D):
    img, d = base(tg)
    r = REL["B"]
    text_c(d, 400, "Dollar kursi", font(FB, 66), GREY, fi(t, 0), img)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, val, t0) in enumerate([("1 yil oldin", "12 025 so'm", 0.1), ("Bugun", "11 987 so'm", r[1] - 0.1)]):
        aa = fi(t, t0)
        y = 540 + i * 250
        ld.rounded_rectangle((90, y, W - 90, y + 200), 30, fill=(24, 24, 24, int(255 * aa)), outline=WHITE + (int(120 * aa),), width=3)
        ld.text((140, y + 30), lab, font=font(FB, 50), fill=GREY + (int(255 * aa),))
        ld.text((140, y + 95), val, font=font(FX, 80), fill=WHITE + (int(255 * aa),))
    img.alpha_composite(lay)
    t3 = r[2] - 0.1 if len(r) > 2 else D * 0.7
    if t > t3:
        badge(img, 1090, "−0,3% — deyarli o'zgarmadi", LIME, fi(t, t3), size=58)
    src(img, "Manba: Markaziy bank kursi, 31.10.2025 va 07.11.2026", fi(t, 0.6))
    return img


def sC(t, tg, D):
    img, d = base(tg)
    r = REL["C"]
    text_c(d, 400, "Dollar omonati", font(FB, 66), GREY, fi(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(190 * (0.6 + 0.4 * a)))
    glow_text(img, 480 - (sz - 190) / 2, "5,4%", font(FX, sz), WHITE, min(1, t / 0.2))
    t1 = r[1] - 0.1
    if t > t1:
        text_c(ImageDraw.Draw(img), 760, "$831,6  →  $876,5", font(FX, 90), WHITE, fi(t, t1), img)
    t2 = r[2] - 0.1
    if t > t2:
        text_c(ImageDraw.Draw(img), 920, "× 11 987 so'm =", font(FB, 60), GREY, fi(t, t2), img)
        v = 10_000_000 + 506_641 * ease((t - t2 - 0.2) / 1.0)
        glow_text(img, 1010, fmt(v) + " so'm", font(FX, 100), WHITE, fi(t, t2))
    src(img, "Manba: Markaziy bank, avgust 2026 (jismoniy shaxslar)", fi(t, 0.6))
    return img


def sD(t, tg, D):
    img, d = base(tg)
    r = REL["D"]
    text_c(d, 400, "So'mdagi omonat", font(FB, 66), GREY, fi(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(200 * (0.6 + 0.4 * a)))
    glow_text(img, 480 - (sz - 200) / 2, "18,4%", font(FX, sz), GREEN, min(1, t / 0.2))
    t1 = r[1] - 0.1
    if t > t1:
        text_c(ImageDraw.Draw(img), 780, "10 000 000 so'm  →", font(FB, 64), GREY, fi(t, t1), img)
        v = 10_000_000 + 1_840_000 * ease((t - t1 - 0.2) / 1.0)
        glow_text(img, 880, fmt(v) + " so'm", font(FX, 104), GREEN, fi(t, t1))
    src(img, "Manba: Markaziy bank, avgust 2026", fi(t, 0.6))
    return img


def sE(t, tg, D):
    img, d = base(tg)
    r = REL["E"]
    text_c(d, 380, "1 yildan keyin, 10 mln so'mdan", font(FB, 58), GREY, fi(t, 0), img)
    bar_row(img, 520, "Dollarda saqlagan", 10_506_641, 11_840_000, (110, 110, 110), fi(t, 0.1), ease((t - 0.1) / 0.8), WHITE)
    bar_row(img, 780, "So'mda saqlagan", 11_840_000, 11_840_000, GREEN, fi(t, 0.6), ease((t - 0.6) / 0.8))
    glow_text(img, 1060, "Farq: 1,33 mln so'm", font(FX, 92), LIME, fi(t, 1.2))
    t2 = r[1] - 0.1
    if t > t2:
        badge(img, 1220 + 30 * (1 - fi(t, t2)), "Bu safar so'm yutdi", GREEN, fi(t, t2), size=64)
    return img


def sF(t, tg, D):
    img, d = base(tg)
    r = REL["F"]
    glow_text(img, 380, "Tez qoida", font(FX, 110), LIME, fi(t, 0))
    t1 = r[1] - 0.1
    a = fi(t, t1)
    if a > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((70, 560, W - 70, 840), 36, outline=LIME + (int(255 * a),), width=6, fill=(22, 22, 22, int(255 * a)))
        img.alpha_composite(lay)
        text_c(ImageDraw.Draw(img), 600, "Chegara ≈", font(FB, 56), GREY, a, img)
        text_c(ImageDraw.Draw(img), 690, "So'm % − Dollar %", font(FX, 76), WHITE, a, img)
    t2 = r[2] - 0.1
    if t > t2:
        glow_text(img, 900, "18,4 − 5,4 ≈ 13%", font(FX, 96), WHITE, fi(t, t2))
    t3 = r[3] - 0.1
    if t > t3:
        text_c(ImageDraw.Draw(img), 1060, "Dollar yiliga 13% dan kam oshsa —", font(FB, 52), WHITE, fi(t, t3), img)
        text_c(ImageDraw.Draw(img), 1130, "so'mdagi omonat foydaliroq", font(FX, 58), GREEN, fi(t, t3 + 0.2), img)
    t4 = r[4] - 0.1
    if t > t4:
        text_c(ImageDraw.Draw(img), 1280, "Kurs oldindan ma'lum emas · bu maslahat emas", font(FM, 40), GREY, fi(t, t4), img)
    return img


def sG(t, tg, D):
    img, d = base(tg)
    r = REL["G"]
    glow_text(img, 520, "Dollar yoki so'm?", font(FX, 96), WHITE, fi(t, 0))
    badge(img, 700 + 30 * (1 - fi(t, 0.3)), "Saqlab qo'ying", LIME, fi(t, 0.3), size=64)
    t2 = r[1] - 0.1
    if t > t2:
        text_c(ImageDraw.Draw(img), 900, "Siz qayerda saqlaysiz?", font(FB, 60), WHITE, fi(t, t2), img)
        text_c(ImageDraw.Draw(img), 985, "Izohda yozing", font(FB, 58), GREY, fi(t, t2 + 0.3), img)
    a4 = fi(t, 0.9)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    return img


FN = {"A": sA, "B": sB, "C": sC, "D": sD, "E": sE, "F": sF, "G": sG}


def mk(k):
    D = DUR[k]
    return lambda t, tg: FN[k](t, tg, D)


if __name__ == "__main__":
    OUT, mode = sys.argv[1], sys.argv[2]
    M.OUT = OUT
    st = 0
    files = []
    for k in ORDER:
        D = DUR[k]
        if mode == "stills":
            mk(k)(D * 0.92, st + D * 0.92).convert("RGB").save(os.path.join(OUT, f"v{k}_still.jpg"), quality=85)
        else:
            files.append(M.render("v" + k, D, mk(k), st))
        st += D
    if mode != "stills":
        with open(os.path.join(OUT, "list5.txt"), "w") as f:
            for fl in files:
                f.write(f"file '{os.path.abspath(fl)}'\n")
    print(DUR, REL)
