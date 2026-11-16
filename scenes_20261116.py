"""16.11.2026 — Oylikdan soliq: yozilgan vs qo'lga tegadigan (ovozli, Narakeet shavkat). python3 scenes_20261114.py OUT stills|render TIMING.json"""
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




def card(img, y, h, col, a):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((90, y, W - 90, y + h), 32, fill=(24, 24, 24, int(255 * a)),
                                          outline=col + (int(230 * a),), width=5)
    img.alpha_composite(lay)



import random


def shake(t, t0, amp=14, d=0.35):
    k = (t - t0) / d
    if k < 0 or k > 1:
        return 0
    random.seed(int(t * 60))
    return int(amp * (1 - k) * random.uniform(-1, 1))


def sA(t, tg, D):
    img, d = base(tg)
    a0 = min(1, t / 0.12)
    badge(img, 300, "KUTILGAN", GREY, a0, size=60)
    text_c(ImageDraw.Draw(img), 520, "\u201cOyligim 5 mln \u2014", font(FX, 84), WHITE, a0, img)
    text_c(ImageDraw.Draw(img), 640, "qo'limga 5 mln\u201d", font(FX, 84), WHITE, a0, img)
    a = back(t / 0.5)
    sz = max(10, int(175 * (0.6 + 0.4 * a)))
    glow_text(img, 850 - (sz - 175) / 2, "5 000 000", font(FX, sz), WHITE, a0)
    text_c(ImageDraw.Draw(img), 1110, "so'm \u2014 shartnomada", font(FB, 62), GREY, a0, img)
    a2 = fi(t, 1.2)
    text_c(ImageDraw.Draw(img), 1300 + 30 * (1 - a2), "Qo'lingizga qancha tegadi?", font(FB, 60), LIME, a2, img)
    src(img, "Soliq stavkalari 2026: Senat, 18.12.2025 (kun.uz)", a0)
    return img


def sB(t, tg, D):
    img, d = base(tg)
    badge(img, 300, "HAQIQAT", RED, fi(t, 0, 0.15), size=60)
    a = back(t / 0.45)
    sz = max(10, int(215 * (0.5 + 0.5 * a)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_text(lay, 580 - (sz - 215) / 2, "4,4 mln", font(FX, sz), RED, min(1, t / 0.15))
    img.alpha_composite(lay, (shake(t, 0.05), shake(t, 0.05, 10)))
    text_c(ImageDraw.Draw(img), 880, "so'm qo'lga tegadi", font(FB, 70), WHITE, fi(t, 0.2), img)
    a2 = fi(t, 0.9)
    card(img, 1060, 200, RED, a2)
    text_c(ImageDraw.Draw(img), 1090, "\u2212600 ming so'm", font(FX, 70), RED, a2, img)
    text_c(ImageDraw.Draw(img), 1180, "daromad solig'i (JShDS) 12%", font(FB, 44), GREY, a2, img)
    src(img, "5 000 000 \u00d7 0,88 = 4 400 000 so'm", fi(t, 0.9), y=1420)
    src(img, "Manba: Senat qonuni, 18.12.2025 (kun.uz, uza.uz)", fi(t, 0.3))
    return img


def sC(t, tg, D):
    img, d = base(tg)
    r1, r2 = REL["C"][1], REL["C"][2]
    text_c(d, 280, "Ish beruvchi siz uchun", font(FB, 60), GREY, fi(t, 0), img)
    text_c(ImageDraw.Draw(img), 360, "qancha to'laydi?", font(FX, 76), WHITE, fi(t, 0.1), img)
    parts = [("Qo'lingizga", 4.4, LIME, 0.0), ("Daromad solig'i 12%", 0.6, RED, 0.3),
             ("Ijtimoiy soliq 12%", 0.6, (245, 150, 60), r1 - 0.2)]
    x0, x1, y0, hb = 120, W - 120, 560, 150
    scale = (x1 - x0) / 5.6
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    x = x0
    for i, (lab, v, col, t0) in enumerate(parts):
        aa = fi(t, t0)
        if aa > 0:
            p = ease((t - t0) / 0.6)
            ld.rectangle((x, y0, x + v * scale * p, y0 + hb), fill=col + (int(235 * aa),))
            yy = 790 + i * 120
            ld.rounded_rectangle((x0, yy + 12, x0 + 44, yy + 56), 10, fill=col + (int(255 * aa),))
            ld.text((x0 + 70, yy), lab, font=font(FB, 52), fill=WHITE + (int(255 * aa),))
            vs = f"{v:.1f}".replace(".", ",") + " mln"
            bb = ld.textbbox((0, 0), vs, font=font(FX, 56))
            ld.text((x1 - (bb[2] - bb[0]), yy), vs, font=font(FX, 56), fill=col + (int(255 * aa),))
        x += v * scale
    img.alpha_composite(lay)
    a3 = fi(t, r2 - 0.2)
    if a3 > 0:
        card(img, 1200, 230, WHITE, a3)
        text_c(ImageDraw.Draw(img), 1225, "Jami xarajat", font(FB, 52), GREY, a3, img)
        text_c(ImageDraw.Draw(img), 1300, "5,6 mln so'm", font(FX, 84), WHITE, a3, img)
    src(img, "Davlatga: 1,2 mln = jami xarajatning 21%", fi(t, r2), y=1490)
    src(img, "Stavkalar: JShDS 12%, ijtimoiy soliq 12% (Senat, 18.12.2025)", fi(t, 0.3), y=1600)
    return img


def sD(t, tg, D):
    img, d = base(tg)
    r1 = REL["D"][1]
    text_c(d, 320, "Qoida:", font(FB, 64), GREY, fi(t, 0), img)
    a1 = fi(t, 0.15)
    card(img, 440, 260, LIME, a1)
    text_c(ImageDraw.Draw(img), 470, "Qo'lga tegadigan =", font(FB, 58), WHITE, a1, img)
    text_c(ImageDraw.Draw(img), 560, "oylik \u00d7 0,88", font(FX, 92), LIME, a1, img)
    a2 = fi(t, r1 - 0.2)
    text_c(ImageDraw.Draw(img), 820, "Ish suhbatida:", font(FB, 58), GREY, a2, img)
    text_c(ImageDraw.Draw(img), 910, "qo'lga 5 mln kerakmi?", font(FB, 64), WHITE, a2, img)
    a3 = fi(t, r1 + 0.6)
    badge(img, 1050 + 30 * (1 - a3), "5,7 mln so'rang", GREEN, a3, size=84)
    text_c(ImageDraw.Draw(img), 1270, "kerakli summa \u00f7 0,88", font(FM, 54), GREY, a3, img)
    src(img, "5 000 000 \u00f7 0,88 = 5 681 818 so'm", fi(t, r1 + 0.6))
    return img


def sE(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Oylik so'rashdan oldin:", font(FB, 58), GREY, fi(t, 0), img)
    glow_text(img, 510, "\u00d7 0,88 ni eslang", font(FX, 92), WHITE, fi(t, 0.05))
    badge(img, 700 + 30 * (1 - fi(t, 0.2)), "Saqlab qo'ying", LIME, fi(t, 0.2), size=64)
    text_c(ImageDraw.Draw(img), 920, "Ish qidirayotgan do'stingizga yuboring", font(FB, 48), WHITE, fi(t, 0.5), img)
    a4 = fi(t, 0.8)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    text_c(ImageDraw.Draw(img), 1600, "Rezident xodim, asosiy ish joyi · imtiyozlar hisobga olinmagan", font(FM, 30), GREY, fi(t, 1.0), img)
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
