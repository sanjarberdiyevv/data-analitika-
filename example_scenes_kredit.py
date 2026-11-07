import os, sys, json
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
import make as M
from make import W, H, FPS, LIME, WHITE, GREY, RED, FB, FX, FM, font, ease, back, fmt, text_c, glow_text

GREEN = (90, 210, 120)
DUR = {"A": 4.5, "B": 7.0, "C": 8.5, "D": 8.0, "E": 7.5, "F": 4.5}
if os.path.exists(os.path.join(os.path.dirname(__file__), "dur3.json")):
    DUR.update(json.load(open(os.path.join(os.path.dirname(__file__), "dur3.json"))))
ORDER = ["A", "B", "C", "D", "E", "F"]
TOTAL = sum(DUR[k] for k in ORDER)


def base(tg):
    return M.base(tg, TOTAL)


def badge(img, y, label, color, a, size=62, fg=None):
    if a <= 0:
        return
    f = font(FX, size)
    bb = ImageDraw.Draw(img).textbbox((0, 0), label, font=f)
    bw, bh = bb[2] - bb[0] + 90, size + 54
    bx = (W - bw) / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((bx, y, bx + bw, y + bh), 28, fill=color + (int(255 * a),))
    img.alpha_composite(lay)
    text_c(ImageDraw.Draw(img), y + 22, label, f, fg or ((11, 11, 11) if color in (LIME, GREEN) else WHITE), a, img)


def fade_in(t, t0, d=0.35):
    return ease((t - t0) / d)


def sA(t, tg, D):
    img, d = base(tg)
    a = back(t / 0.5)
    sz = max(10, int(150 * (0.6 + 0.4 * a)))
    glow_text(img, 640 - (sz - 150) / 2, "10 000 000", font(FX, sz), LIME, min(1, t / 0.2))
    text_c(d, 830, "so'm kredit · 12 oy", font(FB, 70), WHITE, fade_in(t, 0.5), img)
    t2 = D * 0.5
    badge(img, 1010 + 30 * (1 - fade_in(t, t2)), "Qancha ortiqcha to'laysiz?", RED, fade_in(t, t2), size=58)
    return img


def sB(t, tg, D):
    img, d = base(tg)
    text_c(d, 470, "Mikroqarz o'rtacha foizi", font(FB, 66), GREY, fade_in(t, 0), img)
    a = back(t / 0.5)
    sz = max(10, int(230 * (0.6 + 0.4 * a)))
    glow_text(img, 560 - (sz - 230) / 2, "28,3%", font(FX, sz), LIME, min(1, t / 0.2))
    t2 = D * 0.62
    p = fade_in(t, t2, 0.8)
    if p > 0:
        x0, x1, y = 140, W - 140, 960
        dd = ImageDraw.Draw(img)
        dd.rounded_rectangle((x0, y, x0 + (x1 - x0) * p, y + 26), 13, fill=(60, 60, 60))
        # gradient-ish ends
        dd.ellipse((x0 - 20, y - 7, x0 + 20, y + 33), fill=GREEN)
        if p > 0.98:
            dd.ellipse((x1 - 20, y - 7, x1 + 20, y + 33), fill=RED)
            # avg marker at 28.3 within 21.8..41.4
            mx = x0 + (x1 - x0) * (28.3 - 21.8) / (41.4 - 21.8)
            dd.polygon([(mx, y - 14), (mx - 18, y - 44), (mx + 18, y - 44)], fill=LIME)
        a3 = fade_in(t, t2 + 0.5)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.text((x0 - 40, y + 60), "21,8%", font=font(FX, 72), fill=GREEN + (int(255 * a3),))
        ld.text((x0 - 40, y + 145), "Mikrokreditbank", font=font(FM, 40), fill=GREY + (int(255 * a3),))
        f = font(FX, 72)
        w = ld.textbbox((0, 0), "41,4%", font=f)[2]
        ld.text((x1 + 40 - w, y + 60), "41,4%", font=f, fill=RED + (int(255 * a3),))
        f2 = font(FM, 40)
        w2 = ld.textbbox((0, 0), "TBC bank", font=f2)[2]
        ld.text((x1 + 40 - w2, y + 145), "TBC bank", font=f2, fill=GREY + (int(255 * a3),))
        img.alpha_composite(lay)
    text_c(ImageDraw.Draw(img), 1560, "Manba: Markaziy bank, 19.10.2026", font(FM, 40), GREY, fade_in(t, 0.6), img)
    return img


def sC(t, tg, D):
    img, d = base(tg)
    text_c(d, 430, "Oylik to'lov", font(FB, 66), GREY, fade_in(t, 0), img)
    v = 966528 * ease((t - 0.1) / 1.0)
    glow_text(img, 520, fmt(v), font(FX, 150), WHITE, min(1, t / 0.2))
    t2 = D * 0.42
    if t > t2:
        text_c(ImageDraw.Draw(img), 720, "× 12 oy =", font(FB, 70), GREY, fade_in(t, t2), img)
        v2 = 11598339 * ease((t - t2 - 0.2) / 1.0)
        glow_text(img, 830, fmt(v2), font(FX, 130), WHITE, fade_in(t, t2 + 0.1))
    t3 = D * 0.72
    badge(img, 1060 + 30 * (1 - fade_in(t, t3)), "+1 598 339 so'm ortiqcha", RED, fade_in(t, t3), size=60)
    return img


def sD(t, tg, D):
    img, d = base(tg)
    text_c(d, 420, "Bitta kredit — ikki bank", font(FB, 70), GREY, fade_in(t, 0), img)
    maxv = 2381560
    x0, wmax = 140, W - 280
    rows = [("21,8%", 1219778, GREEN, 0.0), ("41,4%", 2381560, RED, D * 0.45)]
    for i, (lab, val, col, t0) in enumerate(rows):
        y = 600 + i * 260
        a = fade_in(t, t0)
        if a <= 0:
            continue
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.text((x0, y), lab + " foizda ortiqcha", font=font(FB, 52), fill=WHITE + (int(255 * a),))
        p = ease((t - t0) / 0.9)
        bw = wmax * (val / maxv) * p
        ld.rounded_rectangle((x0, y + 80, x0 + max(bw, 1), y + 150), 18, fill=col + (int(230 * a),))
        ld.text((x0 + max(bw, 1) - 0 if False else x0 + 20, y + 87), f"{val/1e6:.2f}".replace(".", ",") + " mln", font=font(FX, 52), fill=(11, 11, 11, int(255 * a)) if col != RED else (255, 255, 255, int(255 * a)))
        img.alpha_composite(lay)
    t3 = D * 0.78
    if t > t3:
        glow_text(img, 1180, "Farq: 1,16 mln so'm", font(FX, 100), LIME, fade_in(t, t3))
        text_c(ImageDraw.Draw(img), 1320, "10 mln · 12 oy · teng to'lov", font(FM, 44), GREY, fade_in(t, t3), img)
    return img


def sE(t, tg, D):
    img, d = base(tg)
    glow_text(img, 400, "Tez formula", font(FX, 110), LIME, fade_in(t, 0))
    a = fade_in(t, 0.4)
    if a > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((70, 590, W - 70, 880), 36, outline=LIME + (int(255 * a),), width=6, fill=(22, 22, 22, int(255 * a)))
        img.alpha_composite(lay)
        dd = ImageDraw.Draw(img)
        text_c(dd, 630, "Ortiqcha to'lov ≈", font(FB, 56), GREY, a, img)
        text_c(dd, 720, "Summa × Foiz × (Oy+1) ÷ 24", font(FX, 66), WHITE, a, img)
    t2 = D * 0.55
    a2 = fade_in(t, t2)
    if a2 > 0:
        dd = ImageDraw.Draw(img)
        text_c(dd, 980, "Misol:", font(FB, 56), GREY, a2, img)
        text_c(dd, 1060, "10 mln × 0,283 × 13 ÷ 24", font(FB, 64), WHITE, a2, img)
        glow_text(img, 1160, "≈ 1,53 mln so'm", font(FX, 96), LIME, a2)
        text_c(dd, 1300, "(aniq hisob: 1,60 mln)", font(FM, 44), GREY, a2, img)
    return img


def sF(t, tg, D):
    img, d = base(tg)
    text_c(d, 560, "Kredit olishdan oldin", font(FX, 84), WHITE, fade_in(t, 0), img)
    glow_text(img, 670, "1 daqiqada hisoblang", font(FX, 80), LIME, fade_in(t, 0.3))
    t2 = D * 0.6
    badge(img, 900 + 30 * (1 - fade_in(t, t2)), "Saqlab qo'ying", LIME, fade_in(t, t2), size=64)
    a4 = fade_in(t, t2 + 0.4)
    if a4 > 0:
        dd = ImageDraw.Draw(img)
        text_c(dd, 1090, "@anlyz.uz", font(FX, 80), WHITE, a4, img)
        text_c(dd, 1200, "analitika oddiy tilda", font(FM, 56), GREY, a4, img)
    return img


FN = {"A": sA, "B": sB, "C": sC, "D": sD, "E": sE, "F": sF}


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
            mk(k)(D * 0.95, st + D * 0.95).convert("RGB").save(os.path.join(OUT, f"k{k}_still.jpg"), quality=90)
        else:
            files.append(M.render("k" + k, D, mk(k), st))
        st += D
    if mode != "stills":
        with open(os.path.join(OUT, "list3.txt"), "w") as f:
            for fl in files:
                f.write(f"file '{os.path.abspath(fl)}'\n")
