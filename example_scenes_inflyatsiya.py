import os, sys, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import make as M
from make import W, H, LIME, WHITE, GREY, RED, FB, FX, FM, font, ease, back, fmt, text_c, glow_text

GREEN = (90, 210, 120)
TM = json.load(open("/home/claude/inf_out/timing.json"))
G = TM["groups"]
TOTAL = TM["total"]
ORDER = list("ABCDEFGH")
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


def sA(t, tg, D):  # hook: money melts
    img, d = base(tg)
    r = REL["A"]
    text_c(d, 470, "Yostiq ostidagi pul", font(FB, 64), GREY, fi(t, 0, 0.2), img)
    p = ease((t - 0.6) / 2.6)
    v = 10_000_000 - 600_000 * p
    col = tuple(int(WHITE[i] + (RED[i] - WHITE[i]) * p) for i in range(3))
    glow_text(img, 580, fmt(v), font(FX, 150), col, min(1, t / 0.15))
    text_c(ImageDraw.Draw(img), 770, "so'm · 1 yildan keyin", font(FB, 58), GREY, fi(t, 0.2), img)
    badge(img, 920 + 30 * (1 - fi(t, 1.2)), "−600 000 so'm", RED, fi(t, 1.2), size=80)
    if t > r[1] - 0.1:
        text_c(ImageDraw.Draw(img), 1160, "O'g'ri yo'q.", font(FX, 84), WHITE, fi(t, r[1] - 0.1), img)
    if len(r) > 2 and t > r[2] - 0.1:
        glow_text(img, 1270, "Bu — inflyatsiya", font(FX, 96), LIME, fi(t, r[2] - 0.1))
    return img


def sB(t, tg, D):
    img, d = base(tg)
    r = REL["B"]
    text_c(d, 420, "Rasmiy yillik inflyatsiya", font(FB, 64), GREY, fi(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(230 * (0.6 + 0.4 * a)))
    glow_text(img, 510 - (sz - 230) / 2, "6,4%", font(FX, sz), LIME, min(1, t / 0.2))
    t2 = r[1] - 0.1
    a2 = fi(t, t2)
    if a2 > 0:
        dd = ImageDraw.Draw(img)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for i, (lab, val, col, t0) in enumerate([("Bugun", 10_000_000, WHITE, t2), ("1 yildan keyin", 10_640_000, RED, t2 + 1.0)]):
            aa = fi(t, t0)
            y = 860 + i * 250
            ld.rounded_rectangle((90, y, W - 90, y + 200), 30, fill=(24, 24, 24, int(255 * aa)), outline=col + (int(200 * aa),), width=4)
            ld.text((140, y + 30), lab, font=font(FB, 50), fill=GREY + (int(255 * aa),))
            vv = 10_000_000 + (val - 10_000_000) * ease((t - t0 - 0.2) / 0.9)
            ld.text((140, y + 95), fmt(vv) + " so'm", font=font(FX, 76), fill=col + (int(255 * aa),))
        img.alpha_composite(lay)
        text_c(dd, 1380, "Xuddi shu narsa — qimmatroq", font(FB, 56), WHITE, fi(t, t2 + 1.6), img)
    src(img, "Manba: Statistika qo'mitasi, sentyabr 2026", fi(t, 0.6))
    return img


def sC(t, tg, D):
    img, d = base(tg)
    r = REL["C"]
    text_c(d, 420, "Pulni uyda saqlasangiz", font(FB, 66), GREY, fi(t, 0), img)
    x0, x1 = 120, W - 120
    # nominal bar
    a = fi(t, 0.2)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.text((x0, 560), "Qog'ozda", font=font(FB, 52), fill=WHITE + (int(255 * a),))
    ld.rounded_rectangle((x0, 640, x0 + (x1 - x0) * ease((t - 0.2) / 0.8), 730), 20, fill=(90, 90, 90, int(255 * a)))
    ld.text((x0 + 24, 655), "10 000 000", font=font(FX, 56), fill=WHITE + (int(255 * a),))
    t2 = r[1] - 0.1
    a2 = fi(t, t2)
    if a2 > 0:
        p = ease((t - t2 - 0.2) / 1.2)
        frac = 1 - 0.06 * p
        ld.text((x0, 820), "Haqiqiy kuchi", font=font(FB, 52), fill=WHITE + (int(255 * a2),))
        bw = (x1 - x0) * frac
        ld.rounded_rectangle((x0, 900, x0 + bw, 990), 20, fill=RED + (int(255 * a2),))
        ld.rounded_rectangle((x0 + bw, 900, x1, 990), 20, outline=RED + (int(160 * a2),), width=3)
        ld.text((x0 + 24, 915), fmt(10_000_000 * frac), font=font(FX, 56), fill=WHITE + (int(255 * a2),))
    img.alpha_composite(lay)
    if t > t2 + 1.4:
        glow_text(img, 1120, "≈ 9,4 mln", font(FX, 130), RED, fi(t, t2 + 1.4))
        text_c(ImageDraw.Draw(img), 1290, "10 mln = 10 mln. Lekin kuchi kamroq.", font(FB, 48), GREY, fi(t, t2 + 1.6), img)
    return img


def sD(t, tg, D):
    img, d = base(tg)
    r = REL["D"]
    text_c(d, 400, "O'rtacha omonat foizi", font(FB, 64), GREY, fi(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(200 * (0.6 + 0.4 * a)))
    glow_text(img, 480 - (sz - 200) / 2, "18,4%", font(FX, sz), GREEN, min(1, t / 0.2))
    t1 = 1.4
    if t > t1:
        text_c(ImageDraw.Draw(img), 760, "Yil oxirida", font(FB, 56), GREY, fi(t, t1), img)
        v = 10_000_000 + 1_840_000 * ease((t - t1 - 0.2) / 1.2)
        glow_text(img, 840, fmt(v) + " so'm", font(FX, 104), WHITE, fi(t, t1))
    t2 = r[1] - 0.1
    if t > t2:
        text_c(ImageDraw.Draw(img), 1040, "Inflyatsiyani ayirsak ham:", font(FB, 56), GREY, fi(t, t2), img)
        badge(img, 1130 + 30 * (1 - fi(t, t2 + 0.5)), "+1 130 000 real foyda", GREEN, fi(t, t2 + 0.5), size=66)
    src(img, "Manba: Markaziy bank, avgust 2026", fi(t, 0.6))
    return img


def sE(t, tg, D):
    img, d = base(tg)
    r = REL["E"]
    text_c(d, 360, "10 mln · 1 yil", font(FB, 66), GREY, fi(t, 0), img)
    mid = 1000
    cols = [("Uyda", -601_504, RED, r[0]), ("Bankda", 1_127_820, GREEN, r[1] - 0.1)]
    scale = 330 / 1_127_820
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.line((100, mid, W - 100, mid), fill=(90, 90, 90, 255), width=4)
    for i, (lab, val, col, t0) in enumerate(cols):
        a = fi(t, t0)
        if a <= 0:
            continue
        cx = 330 + i * 420
        h = val * scale * ease((t - t0) / 0.8)
        y0, y1 = (mid - h, mid) if h > 0 else (mid, mid - h)
        ld.rounded_rectangle((cx - 110, y0, cx + 110, max(y1, y0 + 2)), 18, fill=col + (int(240 * a),))
        f = font(FB, 52)
        w = ld.textbbox((0, 0), lab, font=f)[2]
        ly = mid + 30 if val > 0 else mid - 100
        ld.text((cx - w / 2, ly), lab, font=f, fill=WHITE + (int(255 * a),))
        s = ("+" if val > 0 else "−") + f"{abs(val)/1e6:.2f}".replace(".", ",") + " mln"
        f2 = font(FX, 60)
        w2 = ld.textbbox((0, 0), s, font=f2)[2]
        vy = (y0 - 90) if val > 0 else (y1 + 20)
        ld.text((cx - w2 / 2, vy), s, font=f2, fill=col + (int(255 * a),))
    img.alpha_composite(lay)
    t3 = r[2] - 0.1 if len(r) > 2 else D * 0.6
    if t > t3:
        glow_text(img, 1330, "Farq: 1,73 mln so'm", font(FX, 88), LIME, fi(t, t3))
    return img


def sF(t, tg, D):
    img, d = base(tg)
    r = REL["F"]
    glow_text(img, 400, "Tez formula", font(FX, 110), LIME, fi(t, 0))
    t1 = r[1] - 0.1
    a = fi(t, t1)
    if a > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((70, 590, W - 70, 880), 36, outline=LIME + (int(255 * a),), width=6, fill=(22, 22, 22, int(255 * a)))
        img.alpha_composite(lay)
        dd = ImageDraw.Draw(img)
        text_c(dd, 630, "Real foyda ≈", font(FB, 58), GREY, a, img)
        text_c(dd, 720, "Omonat % − Inflyatsiya %", font(FX, 60), WHITE, a, img)
    t2 = r[2] - 0.1
    a2 = fi(t, t2)
    if a2 > 0:
        text_c(ImageDraw.Draw(img), 1000, "18,4% − 6,4%", font(FX, 90), WHITE, a2, img)
        glow_text(img, 1130, "= 12% yiliga", font(FX, 120), GREEN, fi(t, t2 + 0.4))
    return img


def sG(t, tg, D):
    img, d = base(tg)
    r = REL["G"]
    badge(img, 380, "BONUS", LIME, fi(t, 0, 0.25), size=60)
    glow_text(img, 560, "72 qoidasi", font(FX, 120), WHITE, fi(t, 0.2))
    t1 = r[1] - 0.1
    if t > t1:
        text_c(ImageDraw.Draw(img), 780, "72 ÷ inflyatsiya", font(FB, 72), GREY, fi(t, t1), img)
        text_c(ImageDraw.Draw(img), 880, "72 ÷ 6,4 ≈ 11", font(FX, 100), WHITE, fi(t, t1 + 0.6), img)
    t2 = r[3] - 0.1 if len(r) > 3 else D * 0.6
    if t > t2:
        glow_text(img, 1080, "11 yilda", font(FX, 120), LIME, fi(t, t2))
        badge(img, 1250 + 30 * (1 - fi(t, t2 + 0.4)), "narxlar ×2", RED, fi(t, t2 + 0.4), size=78)
    return img


def sH(t, tg, D):
    img, d = base(tg)
    r = REL["H"]
    text_c(d, 520, "Pulingiz ishlasin,", font(FX, 84), WHITE, fi(t, 0), img)
    glow_text(img, 630, "yotmasin", font(FX, 110), LIME, fi(t, 0.3))
    badge(img, 870 + 30 * (1 - fi(t, 0.5)), "Saqlab qo'ying", LIME, fi(t, 0.5), size=64)
    t2 = r[1] - 0.1
    if t > t2:
        text_c(ImageDraw.Draw(img), 1070, "Pulingizni qayerda saqlaysiz?", font(FB, 58), WHITE, fi(t, t2), img)
        text_c(ImageDraw.Draw(img), 1150, "Izohda yozing 👇".replace(" 👇", ""), font(FB, 58), GREY, fi(t, t2 + 0.3), img)
    a4 = fi(t, 0.9)
    text_c(ImageDraw.Draw(img), 1350, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1460, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    return img


FN = {"A": sA, "B": sB, "C": sC, "D": sD, "E": sE, "F": sF, "G": sG, "H": sH}


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
            mk(k)(D * 0.92, st + D * 0.92).convert("RGB").save(os.path.join(OUT, f"i{k}_still.jpg"), quality=85)
        else:
            files.append(M.render("i" + k, D, mk(k), st))
        st += D
    if mode != "stills":
        with open(os.path.join(OUT, "list4.txt"), "w") as f:
            for fl in files:
                f.write(f"file '{os.path.abspath(fl)}'\n")
    print(DUR, REL)
