"""12.11.2026 — Annuitet vs differensial (ovozli, Narakeet shavkat). python3 scenes_20261112.py OUT stills|render TIMING.json"""
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



import math
S, RATE, N = 100.0, 0.229, 60
r = RATE / 12
ANN = S * r / (1 - (1 + r) ** -N)
DIFF = [S / N + (S - S / N * k) * r for k in range(N)]


def card(img, y, h, col, a):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((90, y, W - 90, y + h), 32, fill=(24, 24, 24, int(255 * a)),
                                          outline=col + (int(230 * a),), width=5)
    img.alpha_composite(lay)


def bars(img, x, y, w, h, vals, vmax, col, a, p):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    n = len(vals)
    bw = w / n
    for i, v in enumerate(vals):
        if i / n > p:
            break
        bh = h * v / vmax
        ld.rectangle((x + i * bw + 2, y + h - bh, x + (i + 1) * bw - 3, y + h), fill=col + (int(235 * a),))
    img.alpha_composite(lay)


def sA(t, tg, D):  # hook: raqam 0-soniyada
    img, d = base(tg)
    a0 = min(1, t / 0.1)
    text_c(d, 400, "100 mln so'm kredit", font(FX, 96), WHITE, a0, img)
    text_c(d, 560, "bitta tanlov tejaydi:", font(FB, 64), GREY, a0, img)
    a = back(t / 0.5)
    sz = max(10, int(210 * (0.6 + 0.4 * a)))
    glow_text(img, 680 - (sz - 210) / 2, "10,6 mln", font(FX, sz), LIME, a0)
    badge(img, 1000 + 30 * (1 - fi(t, REL["A"][1] - 0.2)), "Annuitet yoki differensial?", WHITE if False else LIME,
          fi(t, REL["A"][1] - 0.2), size=58)
    src(img, "Kredit 22,9% · 5 yil · bir xil bank, bir xil foiz", a0, y=1330)
    src(img, "Stavka: Markaziy bank, 19.10.2026", a0)
    return img


def sB(t, tg, D):
    img, d = base(tg)
    r1 = REL["B"][1]
    text_c(d, 300, "Oylik to'lov grafigi", font(FB, 60), GREY, fi(t, 0), img)
    vmax = max(DIFF)
    # Annuitet
    a1 = fi(t, 0.1)
    if a1 > 0:
        card(img, 420, 470, (90, 90, 90), a1)
        dd = ImageDraw.Draw(img)
        text_c(dd, 450, "ANNUITET", font(FX, 66), WHITE, a1, img)
        text_c(ImageDraw.Draw(img), 535, "har oy bir xil: 2,81 mln", font(FB, 50), GREY, a1, img)
        bars(img, 150, 620, W - 300, 230, [ANN] * N, vmax, RED, a1, ease((t - 0.3) / 1.2))
    a2 = fi(t, r1 - 0.2)
    if a2 > 0:
        card(img, 940, 470, LIME, a2)
        text_c(ImageDraw.Draw(img), 970, "DIFFERENSIAL", font(FX, 66), LIME, a2, img)
        text_c(ImageDraw.Draw(img), 1055, "foiz qolgan qarzga: 3,58 → 1,70", font(FB, 50), GREY, a2, img)
        bars(img, 150, 1140, W - 300, 230, DIFF, vmax, LIME, a2, ease((t - r1) / 1.2))
    src(img, "100 mln · 22,9% · 60 oy (mln so'm)", fi(t, 0.3), y=1470)
    return img


def sC(t, tg, D):
    img, d = base(tg)
    r1 = REL["C"][1]
    text_c(d, 330, "5 yilda ustama foiz", font(FB, 64), GREY, fi(t, 0), img)
    data = [("Annuitet", 68.8, RED, 0.2), ("Differensial", 58.2, LIME, r1 - 0.3)]
    x0, wmax = 120, W - 240
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, v, col, t0) in enumerate(data):
        aa = fi(t, t0)
        if aa <= 0:
            continue
        y = 480 + i * 290
        p = ease((t - t0) / 0.7)
        ld.text((x0, y), lab, font=font(FB, 58), fill=WHITE + (int(255 * aa),))
        ld.rounded_rectangle((x0, y + 90, x0 + max(2, wmax * v / 68.8 * p), y + 200), 22, fill=col + (int(235 * aa),))
        s = f"+{v:.1f}".replace(".", ",") + " mln"
        ld.text((x0 + 28, y + 108), s, font=font(FX, 66), fill=(11, 11, 11, int(255 * aa)))
    img.alpha_composite(lay)
    badge(img, 1080 + 30 * (1 - fi(t, r1 + 0.9)), "Farq: 10,6 mln so'm", GREEN, fi(t, r1 + 0.9), size=76)
    a3 = fi(t, r1 + 1.6)
    text_c(ImageDraw.Draw(img), 1290, "Differensial ustama:", font(FB, 48), GREY, a3, img)
    text_c(ImageDraw.Draw(img), 1360, "S × F × (oy + 1) ÷ 24", font(FX, 66), WHITE, a3, img)
    text_c(ImageDraw.Draw(img), 1450, "100 × 22,9% × 61 ÷ 24 = 58,2", font(FM, 44), GREY, a3, img)
    src(img, "Manba: Markaziy bank, 19.10.2026", fi(t, 0.3), y=1580)
    src(img, "jismoniy shaxslar krediti o'rtacha 22,9%", fi(t, 0.3), y=1630)
    return img


def sD(t, tg, D):
    img, d = base(tg)
    r1 = REL["D"][1]
    text_c(d, 360, "Lekin 1-oy to'lovi", font(FB, 64), GREY, fi(t, 0), img)
    for i, (lab, val, col) in enumerate([("Differensial", "3,58 mln", LIME), ("Annuitet", "2,81 mln", WHITE)]):
        aa = fi(t, 0.2 + i * 0.4)
        if aa <= 0:
            continue
        y = 480 + i * 180
        card(img, y, 150, (70, 70, 70), aa)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.text((140, y + 45), lab, font=font(FB, 56), fill=GREY + (int(255 * aa),))
        fw = ld.textbbox((0, 0), val, font=font(FX, 70))[2]
        ld.text((W - 140 - fw, y + 38), val, font=font(FX, 70), fill=col + (int(255 * aa),))
        img.alpha_composite(lay)
    text_c(ImageDraw.Draw(img), 870, "+0,76 mln boshida", font(FB, 56), RED, fi(t, 1.1), img)
    glow_text(img, 1000, "Daromad yetsa —", font(FX, 80), WHITE, fi(t, r1 - 0.1))
    badge(img, 1110 + 30 * (1 - fi(t, r1 + 0.2)), "differensial", LIME, fi(t, r1 + 0.2), size=80)
    return img


def sE(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Kredit olishdan oldin:", font(FB, 58), GREY, fi(t, 0), img)
    glow_text(img, 510, "to'lov turini so'rang", font(FX, 84), WHITE, fi(t, 0.1))
    badge(img, 700 + 30 * (1 - fi(t, 0.3)), "Saqlab qo'ying", LIME, fi(t, 0.3), size=64)
    text_c(ImageDraw.Draw(img), 920, "Kredit olmoqchi do'stingizga yuboring", font(FB, 50), WHITE, fi(t, 0.8), img)
    a4 = fi(t, 1.3)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    text_c(ImageDraw.Draw(img), 1600, "Hisob: stavka o'zgarmas, komissiya/sug'urtasiz · bu maslahat emas", font(FM, 29), GREY, fi(t, 1.5), img)
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
