"""13.11.2026 — Nasiya ustamasi -> haqiqiy yillik foiz (ovozli, Narakeet shavkat). python3 scenes_20261112.py OUT stills|render TIMING.json"""
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
    text_c(d, 400, "Nasiyaga telefon =", font(FX, 92), WHITE, a0, img)
    a = back(t / 0.5)
    sz = max(10, int(250 * (0.6 + 0.4 * a)))
    glow_text(img, 560 - (sz - 250) / 2, "66,5%", font(FX, sz), RED, a0)
    text_c(ImageDraw.Draw(img), 860, "yillik foizli kredit", font(FB, 70), WHITE, a0, img)
    badge(img, 1030 + 30 * (1 - fi(t, REL["A"][1] - 0.2)), "Markaziy bank hisobi", LIME, fi(t, REL["A"][1] - 0.2), size=58)
    src(img, "12 oylik nasiya · o'rtacha ustama 39,6%", a0, y=1330)
    src(img, "Manba: Markaziy bank tadqiqoti (spot.uz, 18.06.2025)", a0)
    return img


def sB(t, tg, D):
    img, d = base(tg)
    r1 = REL["B"][1]
    text_c(d, 300, "12 oylik nasiya ustamasi", font(FB, 60), GREY, fi(t, 0), img)
    glow_text(img, 400, "39,6%", font(FX, 190), WHITE, fi(t, 0.05))
    text_c(ImageDraw.Draw(img), 640, "o'rtacha · 27,3% dan 44,3% gacha", font(FB, 48), GREY, fi(t, 0.4), img)
    a2 = fi(t, r1 - 0.2)
    if a2 > 0:
        card(img, 780, 620, LIME, a2)
        text_c(ImageDraw.Draw(img), 810, "Lekin qarz har oy kamayadi", font(FB, 56), LIME, a2, img)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        x, y, w, h, n = 150, 920, W - 300, 400, 12
        bw = w / n
        p = ease((t - r1) / 1.4)
        for i in range(n):
            if i / n > p:
                break
            bh = h * (n - i) / n
            ld.rectangle((x + i * bw + 4, y + h - bh, x + (i + 1) * bw - 6, y + h), fill=LIME + (int(220 * a2),))
        img.alpha_composite(lay)
        text_c(ImageDraw.Draw(img), 1340, "1-oy                qolgan qarz                12-oy", font(FM, 36), GREY, a2, img)
    src(img, "Ustama esa butun summaga hisoblanadi", fi(t, r1 + 0.6), y=1500)
    return img


def sC(t, tg, D):
    img, d = base(tg)
    r1 = REL["C"][1]
    text_c(d, 330, "Tez qoida (12 oy):", font(FB, 64), GREY, fi(t, 0), img)
    a1 = fi(t, 0.1)
    card(img, 450, 260, LIME, a1)
    text_c(ImageDraw.Draw(img), 490, "Yillik foiz ≈", font(FB, 60), WHITE, a1, img)
    text_c(ImageDraw.Draw(img), 580, "ustama × 1,7", font(FX, 92), LIME, a1, img)
    rows = [("27,3%", "46%", "47,1%"), ("39,6%", "67%", "66,5%"), ("44,3%", "75%", "73,8%")]
    a3 = fi(t, r1 - 0.2)
    if a3 > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        hy = 820
        for x, s in [(130, "ustama"), (430, "× 1,7"), (720, "MB hisobi")]:
            ld.text((x, hy), s, font=font(FM, 42), fill=GREY + (int(255 * a3),))
        for i, (u, q, mb) in enumerate(rows):
            aa = fi(t, r1 - 0.2 + 0.25 * i)
            y = hy + 90 + i * 120
            ld.text((130, y), u, font=font(FX, 66), fill=WHITE + (int(255 * aa),))
            ld.text((430, y), "≈ " + q, font=font(FX, 66), fill=LIME + (int(255 * aa),))
            ld.text((720, y), mb, font=font(FX, 66), fill=RED + (int(255 * aa),))
        img.alpha_composite(lay)
    src(img, "Teng 12 to'lov, boshlang'ich to'lovsiz", fi(t, 0.3), y=1340)
    src(img, "Manba: Markaziy bank (spot.uz, 18.06.2025)", fi(t, 0.3), y=1600)
    return img


def sD(t, tg, D):
    img, d = base(tg)
    r1 = REL["D"][1]
    text_c(d, 330, "10 mln so'mlik telefon, 12 oy", font(FB, 60), GREY, fi(t, 0), img)
    data = [("Nasiya (ustama 39,6%)", 3.96, RED, 0.2), ("Mikroqarz (28,3%)", 1.60, LIME, r1 - 0.3)]
    x0, wmax = 120, W - 240
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i, (lab, v, col, t0) in enumerate(data):
        aa = fi(t, t0)
        if aa <= 0:
            continue
        y = 470 + i * 290
        p = ease((t - t0) / 0.7)
        ld.text((x0, y), lab, font=font(FB, 54), fill=WHITE + (int(255 * aa),))
        ld.rounded_rectangle((x0, y + 90, x0 + max(2, wmax * v / 3.96 * p), y + 200), 22, fill=col + (int(235 * aa),))
        s = f"+{v:.2f}".replace(".", ",") + " mln"
        bwid = wmax * v / 3.96
        if bwid > 450:
            ld.text((x0 + 28, y + 108), s, font=font(FX, 66), fill=(11, 11, 11, int(255 * aa)))
        else:
            ld.text((x0 + bwid + 30, y + 108), s, font=font(FX, 66), fill=col + (int(255 * aa * min(1, p * 1.5)),))
    img.alpha_composite(lay)
    badge(img, 1080 + 30 * (1 - fi(t, r1 + 0.6)), "Farq: 2,36 mln so'm", GREEN, fi(t, r1 + 0.6), size=76)
    text_c(ImageDraw.Draw(img), 1300, "oyiga 1,16 mln vs 0,97 mln", font(FB, 50), GREY, fi(t, r1 + 0.9), img)
    src(img, "Mikroqarz o'rtacha 28,3%: Markaziy bank, 19.10.2026", fi(t, 0.3), y=1580)
    src(img, "ortiqcha to'lov, annuitet hisobi", fi(t, 0.3), y=1630)
    return img


def sE(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Nasiyadan oldin:", font(FB, 58), GREY, fi(t, 0), img)
    glow_text(img, 510, "ustama × 1,7", font(FX, 96), WHITE, fi(t, 0.05))
    badge(img, 700 + 30 * (1 - fi(t, 0.2)), "Saqlab qo'ying", LIME, fi(t, 0.2), size=64)
    text_c(ImageDraw.Draw(img), 920, "Nasiya olmoqchi do'stingizga yuboring", font(FB, 50), WHITE, fi(t, 0.5), img)
    a4 = fi(t, 0.8)
    text_c(ImageDraw.Draw(img), 1200, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
    text_c(ImageDraw.Draw(img), 1310, "analitika oddiy tilda", font(FM, 52), GREY, a4, img)
    text_c(ImageDraw.Draw(img), 1600, "Hisob: komissiya/sug'urtasiz · bu maslahat emas", font(FM, 32), GREY, fi(t, 1.0), img)
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
