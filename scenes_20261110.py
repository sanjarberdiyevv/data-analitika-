"""10.11.2026 — Avtokredit: haqiqiy narx (ovozli, Narakeet shavkat). python3 scenes_20261110.py OUT stills|render TIMING.json"""
import os, sys, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make as M
from make import W, H, LIME, WHITE, GREY, RED, FB, FX, FM, font, ease, back, fmt, text_c, glow_text

GREEN = (90, 210, 120)
TM = json.load(open(sys.argv[3] if len(sys.argv) > 3 else "timing.json"))
G = TM["groups"]
TOTAL = TM["total"]
ORDER = list("ABCDE")
STARTS = [0.0] + [g[0] for g in G[1:]]
DUR = {k: (STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL) - STARTS[i] for i, k in enumerate(ORDER)}
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


def src(img, s, a, y=1600):
    text_c(ImageDraw.Draw(img), y, s, font(FM, 38), GREY, a, img)


def sA(t, tg, D):  # hook: raqam 0-soniyada
    img, d = base(tg)
    a0 = min(1, t / 0.1)
    text_c(d, 380, "Mashina narxi", font(FB, 64), GREY, a0, img)
    text_c(d, 470, "200 mln so'm", font(FX, 110), WHITE, a0, img)
    if a0 > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p = ease((t - 0.5) / 0.4)
        if p > 0:
            ImageDraw.Draw(lay).line((200, 545, 200 + 680 * p, 545), fill=RED + (255,), width=10)
        img.alpha_composite(lay)
    text_c(ImageDraw.Draw(img), 700, "kreditda aslida", font(FB, 64), GREY, fi(t, 0.6, 0.25), img)
    a = back((t - 0.8) / 0.5)
    if t > 0.8:
        sz = max(10, int(165 * (0.6 + 0.4 * a)))
        glow_text(img, 810 - (sz - 165) / 2, "289,6 mln", font(FX, sz), RED, min(1, (t - 0.8) / 0.2))
    badge(img, 1100 + 30 * (1 - fi(t, 1.8)), "+89,6 mln ustama", RED, fi(t, 1.8), size=70)
    src(img, "Avtokredit 21,5% · 30% boshlang'ich · 5 yil", a0, y=1330)
    src(img, "Stavka: Markaziy bank, 28.09.2026", a0)
    return img


def sB(t, tg, D):
    img, d = base(tg)
    r1 = REL["B"][1]
    text_c(d, 340, "Avtokredit, o'rtacha stavka", font(FB, 60), GREY, fi(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(200 * (0.6 + 0.4 * a)))
    glow_text(img, 430 - (sz - 200) / 2, "21,5%", font(FX, sz), LIME, min(1, t / 0.2))
    text_c(ImageDraw.Draw(img), 680, "eng past 18,6% · eng yuqori 25,2%", font(FM, 48), GREY, fi(t, 0.8), img)
    rows = [("Kredit (70%)", "140 mln", WHITE, 0), ("Oylik to'lov", "3,83 mln", WHITE, 0.5),
            ("60 oyda jami", "229,6 mln", WHITE, 1.4), ("Ustama foiz", "+89,6 mln", RED, 2.3)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, val, col, dt) in enumerate(rows):
        aa = fi(t, r1 - 0.3 + dt)
        if aa <= 0:
            continue
        y = 820 + i * 170
        ld.rounded_rectangle((90, y, W - 90, y + 145), 28, fill=(24, 24, 24, int(255 * aa)),
                             outline=((RED if col == RED else (70, 70, 70))) + (int(220 * aa),), width=4)
        ld.text((130, y + 42), lab, font=font(FB, 50), fill=GREY + (int(255 * aa),))
        fw = ld.textbbox((0, 0), val, font=font(FX, 64))[2]
        ld.text((W - 130 - fw, y + 36), val, font=font(FX, 64), fill=col + (int(255 * aa),))
    img.alpha_composite(lay)
    src(img, "Manba: Markaziy bank, 28.09.2026 holati (anhor.uz)", fi(t, 0.3))
    src(img, "Hisob: annuitet, 21,5% yillik", fi(t, r1), y=1650)
    return img


def sC(t, tg, D):
    img, d = base(tg)
    r = REL["C"]
    glow_text(img, 340, "Tez qoida", font(FX, 120), LIME, fi(t, 0))
    text_c(d, 500, "21,5% da kredit summasiga qo'shing:", font(FB, 52), GREY, fi(t, 0.3), img)
    for i, (lab, val, t0) in enumerate([("5 yil", "+64%", r[1]), ("3 yil", "+37%", r[2])]):
        aa = fi(t, t0 - 0.1)
        if aa <= 0:
            continue
        y = 620 + i * 300
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((90, y, W - 90, y + 250), 36, outline=LIME + (int(255 * aa),), width=6,
                                              fill=(22, 22, 22, int(255 * aa)))
        img.alpha_composite(lay)
        dd = ImageDraw.Draw(img)
        lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        l2 = ImageDraw.Draw(lay2)
        l2.text((150, y + 70), lab, font=font(FB, 84), fill=WHITE + (int(255 * aa),))
        fw = l2.textbbox((0, 0), val, font=font(FX, 130))[2]
        l2.text((W - 150 - fw, y + 45), val, font=font(FX, 130), fill=(RED if i == 0 else LIME) + (int(255 * aa),))
        img.alpha_composite(lay2)
    if t > r[2] + 0.8:
        text_c(ImageDraw.Draw(img), 1260, "140 mln × 1,64 = 229,6 mln", font(FX, 64), WHITE, fi(t, r[2] + 0.8), img)
        text_c(ImageDraw.Draw(img), 1350, "har qanday summa uchun ishlaydi", font(FM, 46), GREY, fi(t, r[2] + 1.0), img)
    return img


def sD(t, tg, D):
    img, d = base(tg)
    r1 = REL["D"][1]
    text_c(d, 360, "Mashina jami qanchaga tushadi", font(FB, 60), GREY, fi(t, 0), img)
    data = [("30% naqd · 5 yil", 289.6, RED, 0.2), ("50% naqd · 3 yil", 236.6, LIME, 0.9)]
    x0, wmax = 120, W - 240
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, v, col, t0) in enumerate(data):
        aa = fi(t, t0)
        if aa <= 0:
            continue
        y = 520 + i * 300
        p = ease((t - t0) / 0.7)
        ld.text((x0, y), lab, font=font(FB, 56), fill=WHITE + (int(255 * aa),))
        ld.rounded_rectangle((x0, y + 90, x0 + max(2, wmax * v / 289.6 * p), y + 200), 22, fill=col + (int(235 * aa),))
        s = f"{v:.1f}".replace(".", ",") + " mln"
        ld.text((x0 + 28, y + 108), s, font=font(FX, 66), fill=(11, 11, 11, int(255 * aa)))
    img.alpha_composite(lay)
    text_c(ImageDraw.Draw(img), 1150, "oylik: 3,83 mln → 3,79 mln", font(FM, 48), GREY, fi(t, 1.6), img)
    badge(img, 1260 + 30 * (1 - fi(t, r1 - 0.2)), "Tejash: 53 mln so'm", GREEN, fi(t, r1 - 0.2), size=76)
    src(img, "Mashina 200 mln · 21,5% · annuitet", fi(t, 0.3))
    return img


def sE(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Kredit olishdan oldin:", font(FB, 58), GREY, fi(t, 0), img)
    glow_text(img, 510, "5 yil: kredit × 1,64", font(FX, 84), WHITE, fi(t, 0.1))
    badge(img, 700 + 30 * (1 - fi(t, 0.3)), "Saqlab qo'ying", LIME, fi(t, 0.3), size=64)
    text_c(ImageDraw.Draw(img), 900, "Mashina olmoqchi do'stingizga", font(FB, 60), WHITE, fi(t, REL["E"][1] - 0.1), img)
    text_c(ImageDraw.Draw(img), 985, "yuboring", font(FB, 60), WHITE, fi(t, REL["E"][1] - 0.1), img)
    a4 = fi(t, 1.4)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    text_c(ImageDraw.Draw(img), 1600, "Hisob: stavka o'zgarmas, komissiya/sug'urtasiz · bu maslahat emas", font(FM, 29), GREY, fi(t, 1.6), img)
    return img


FN = {"A": sA, "B": sB, "C": sC, "D": sD, "E": sE}


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
    print("total", TOTAL, DUR)
