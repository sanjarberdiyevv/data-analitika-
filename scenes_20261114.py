"""14.11.2026 — Kreditni muddatidan oldin to'lash: muddat vs oylik (ovozli, Narakeet shavkat). python3 scenes_20261114.py OUT stills|render TIMING.json"""
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


def sA(t, tg, D):  # hook
    img, d = base(tg)
    a0 = min(1, t / 0.1)
    text_c(d, 380, "Kreditni erta yopyapsizmi?", font(FX, 68), WHITE, a0, img)
    text_c(ImageDraw.Draw(img), 500, "Bitta tanlov farqi:", font(FB, 64), GREY, a0, img)
    a = back(t / 0.5)
    sz = max(10, int(240 * (0.6 + 0.4 * a)))
    glow_text(img, 610 - (sz - 240) / 2, "11 mln", font(FX, sz), LIME, a0)
    text_c(ImageDraw.Draw(img), 900, "so'm", font(FB, 70), WHITE, a0, img)
    badge(img, 1060 + 30 * (1 - fi(t, REL["A"][1] - 0.2)), "Muddat yoki oylik?", RED, fi(t, REL["A"][1] - 0.2), size=60)
    src(img, "100 mln kredit · 5 yil · 21,3% · +20 mln erta to'lov", a0, y=1330)
    src(img, "Stavka: Markaziy bank, avgust 2026 (gazeta.uz, 04.11.2026)", a0)
    return img


def sB(t, tg, D):
    img, d = base(tg)
    r1 = REL["B"][1]
    text_c(d, 300, "Kredit: 100 mln so'm · 5 yil", font(FB, 60), GREY, fi(t, 0), img)
    glow_text(img, 400, "21,3%", font(FX, 170), WHITE, fi(t, 0.05))
    text_c(ImageDraw.Draw(img), 620, "jismoniy shaxslar o'rtacha stavkasi", font(FB, 46), GREY, fi(t, 0.3), img)
    a1 = fi(t, 0.6)
    card(img, 740, 230, GREY, a1)
    text_c(ImageDraw.Draw(img), 770, "Oylik to'lov (annuitet)", font(FB, 50), GREY, a1, img)
    text_c(ImageDraw.Draw(img), 850, "2,72 mln so'm", font(FX, 76), WHITE, a1, img)
    a2 = fi(t, r1 - 0.2)
    if a2 > 0:
        card(img, 1030, 260, LIME, a2)
        text_c(ImageDraw.Draw(img), 1060, "1 yildan keyin", font(FB, 54), WHITE, a2, img)
        text_c(ImageDraw.Draw(img), 1140, "+20 mln qo'shimcha to'lov", font(FX, 56), LIME, a2, img)
    src(img, "Qolgan qarz 12-oydan keyin: 87,5 mln", fi(t, 0.6), y=1400)
    src(img, "Manba: Markaziy bank, avgust 2026", fi(t, 0.3), y=1600)
    return img


def sC(t, tg, D):
    img, d = base(tg)
    r1, r2 = REL["C"][1], REL["C"][2]
    text_c(d, 300, "Bank so'raydi:", font(FB, 64), GREY, fi(t, 0), img)
    text_c(ImageDraw.Draw(img), 390, "nimani kamaytiramiz?", font(FX, 76), WHITE, fi(t, 0.1), img)
    data = [("Oylikni kamaytirish", 9.88, "2,10 mln/oy · 48 oy", RED, r1 - 0.2),
            ("Muddatni qisqartirish", 21.0, "2,72 mln/oy · 33 oy", LIME, r2 - 0.2)]
    x0, wmax = 120, W - 240
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, v, sub, col, t0) in enumerate(data):
        aa = fi(t, t0)
        if aa <= 0:
            continue
        y = 560 + i * 380
        p = ease((t - t0) / 0.7)
        ld.text((x0, y), lab, font=font(FB, 56), fill=WHITE + (int(255 * aa),))
        bwid = wmax * v / 21.0
        ld.rounded_rectangle((x0, y + 90, x0 + max(2, bwid * p), y + 200), 22, fill=col + (int(235 * aa),))
        s = f"−{v:.1f}".replace(".", ",") + " mln"
        if bwid > 520:
            ld.text((x0 + 28, y + 108), s, font=font(FX, 66), fill=(11, 11, 11, int(255 * aa)))
        else:
            ld.text((x0 + bwid + 30, y + 108), s, font=font(FX, 66), fill=col + (int(255 * aa * min(1, p * 1.5)),))
        ld.text((x0, y + 225), sub, font=font(FM, 42), fill=GREY + (int(255 * aa),))
    img.alpha_composite(lay)
    src(img, "ustama tejalishi · 5 yillik jadvalga nisbatan", fi(t, 0.3), y=1400)
    src(img, "Hisob: annuitet, 21,3%, komissiyasiz", fi(t, 0.3), y=1600)
    return img


def sD(t, tg, D):
    img, d = base(tg)
    r1, r2 = REL["D"][1], REL["D"][2]
    text_c(d, 330, "Qoida:", font(FB, 64), GREY, fi(t, 0), img)
    a1 = fi(t, r1 - 0.2)
    card(img, 450, 300, LIME, a1)
    text_c(ImageDraw.Draw(img), 480, "Oylikni ko'tara olsangiz —", font(FB, 56), WHITE, a1, img)
    text_c(ImageDraw.Draw(img), 580, "MUDDATNI qisqartiring", font(FX, 64), LIME, a1, img)
    text_c(ImageDraw.Draw(img), 820, "≈ 2 barobar ko'p tejash", font(FB, 60), WHITE, fi(t, r1 + 0.5), img)
    a3 = fi(t, r2 - 0.2)
    badge(img, 1000 + 30 * (1 - a3), "60 oy → 45 oy", GREEN, a3, size=80)
    text_c(ImageDraw.Draw(img), 1220, "kredit 15 oy oldin yopiladi", font(FB, 56), WHITE, a3, img)
    src(img, "21,0 mln vs 9,9 mln tejash", fi(t, 0.3), y=1600)
    return img


def sE(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Erta to'lovda:", font(FB, 58), GREY, fi(t, 0), img)
    glow_text(img, 510, "muddatni tanlang", font(FX, 92), WHITE, fi(t, 0.05))
    badge(img, 700 + 30 * (1 - fi(t, 0.2)), "Saqlab qo'ying", LIME, fi(t, 0.2), size=64)
    text_c(ImageDraw.Draw(img), 920, "Kredit to'layotgan do'stingizga yuboring", font(FB, 48), WHITE, fi(t, 0.5), img)
    a4 = fi(t, 0.8)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    text_c(ImageDraw.Draw(img), 1600, "Shartnomangizni tekshiring · bu maslahat emas", font(FM, 32), GREY, fi(t, 1.0), img)
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
