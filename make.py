import subprocess, os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BG = (11, 11, 11)
LIME = (200, 240, 49)
WHITE = (245, 245, 245)
GREY = (150, 150, 150)
RED = (235, 77, 61)
FB = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
FX = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
FM = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
_fc = {}


def font(path, size):
    k = (path, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def back(t):
    t = max(0.0, min(1.0, t))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def fmt(n):
    return f"{int(round(n)):,}".replace(",", " ")


def text_c(d, y, s, f, fill, alpha=1.0, img=None):
    """centered text with alpha via separate layer"""
    if alpha <= 0:
        return
    bbox = d.textbbox((0, 0), s, font=f)
    w = bbox[2] - bbox[0]
    x = (W - w) / 2 - bbox[0]
    if alpha >= 1:
        d.text((x, y), s, font=f, fill=fill)
    else:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((x, y), s, font=f, fill=fill + (int(255 * alpha),))
        img.alpha_composite(layer)


def base(t_global, total):
    img = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(img)
    # subtle grid dots
    for gx in range(60, W, 120):
        for gy in range(60, H, 120):
            d.ellipse((gx - 2, gy - 2, gx + 2, gy + 2), fill=(32, 32, 32))
    # brand
    text_c(d, 120, "anlyz.uz", font(FB, 44), LIME)
    # progress bar
    p = t_global / total
    d.rounded_rectangle((90, 70, W - 90, 78), 4, fill=(40, 40, 40))
    d.rounded_rectangle((90, 70, 90 + (W - 180) * p, 78), 4, fill=LIME)
    return img, d


def glow_text(img, y, s, f, color, alpha=1.0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    bbox = ld.textbbox((0, 0), s, font=f)
    x = (W - (bbox[2] - bbox[0])) / 2 - bbox[0]
    ld.text((x, y), s, font=f, fill=color + (int(140 * alpha),))
    layer = layer.filter(ImageFilter.GaussianBlur(28))
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    text_c(d, y, s, f, color, alpha, img)


TOTAL = 16.0


def scene1(t, tg):  # 0-3s hook
    img, d = base(tg, TOTAL)
    a = ease(t / 0.4)
    text_c(d, 640 - 40 * (1 - a), "Kuniga bitta kofe", font(FB, 78), WHITE, a, img)
    s = back((t - 0.4) / 0.5)
    if t > 0.4:
        size = max(10, int(145 * (0.6 + 0.4 * s)))
        glow_text(img, 870 - (size - 145) / 2, "20 000 so'm", font(FX, size), LIME, min(1, (t - 0.4) / 0.2))
    a2 = ease((t - 1.3) / 0.4)
    if a2 > 0:
        # badge
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        bw, bh = 420, 120
        bx, by = (W - bw) / 2, 1160 + 30 * (1 - a2)
        ld.rounded_rectangle((bx, by, bx + bw, by + bh), 28, fill=RED + (int(255 * a2),))
        img.alpha_composite(lay)
        text_c(ImageDraw.Draw(img), by + 22, "Arzonmi?", font(FX, 66), WHITE, a2, img)
    return img


def counter_scene(label, target, sub, accent):
    def sc(t, tg):
        img, d = base(tg, TOTAL)
        a = ease(t / 0.35)
        text_c(d, 600 - 40 * (1 - a), label, font(FB, 90), WHITE, a, img)
        v = target * ease((t - 0.2) / 1.4)
        if t > 0.2:
            glow_text(img, 800, fmt(v), font(FX, 190 if target < 1e6 else 150), accent, 1)
            text_c(ImageDraw.Draw(img), 1040, "so'm", font(FB, 80), GREY, 1, img)
        a2 = ease((t - 1.8) / 0.4)
        if a2 > 0:
            text_c(ImageDraw.Draw(img), 1230 + 30 * (1 - a2), sub, font(FM, 58), GREY, a2, img)
        return img
    return sc


def scene4(t, tg):
    img, d = base(tg, TOTAL)
    a = ease(t / 0.4)
    text_c(d, 700 - 40 * (1 - a), "Kichik xarajat", font(FX, 110), WHITE, a, img)
    a2 = ease((t - 0.5) / 0.4)
    if a2 > 0:
        glow_text(img, 850 + 40 * (1 - a2), "katta pulga", font(FX, 120), LIME, a2)
        glow_text(img, 1000 + 40 * (1 - a2), "aylanadi.", font(FX, 120), LIME, a2)
    a3 = ease((t - 1.4) / 0.4)
    if a3 > 0:
        dd = ImageDraw.Draw(img)
        text_c(dd, 1250, "Sizda qaysi xarajat", font(FM, 60), GREY, a3, img)
        text_c(dd, 1330, "shunday? Kommentda yozing", font(FM, 60), GREY, a3, img)
    return img


def scene5(t, tg):
    img, d = base(tg, TOTAL)
    a = back(t / 0.5)
    size = max(10, int(110 * (0.7 + 0.3 * a)))
    glow_text(img, 760 - (size - 110) / 2, "Saqlab qo'ying", font(FX, size), LIME, min(1, t / 0.2))
    a2 = ease((t - 0.6) / 0.4)
    if a2 > 0:
        dd = ImageDraw.Draw(img)
        text_c(dd, 960, "@anlyz.uz", font(FX, 90), WHITE, a2, img)
        text_c(dd, 1080, "analitika oddiy tilda", font(FM, 60), GREY, a2, img)
    return img


SCENES = [
    ("s1", 3.0, scene1),
    ("s2", 3.5, counter_scene("Oyiga", 600000, "30 kun × 20 000", WHITE)),
    ("s3", 4.0, counter_scene("Yiliga", 7300000, "365 kun × 20 000", LIME)),
    ("s4", 3.0, scene4),
    ("s5", 2.5, scene5),
]


def render(name, dur, fn, start):
    tmp = os.path.join(OUT, f"{name}.part.mp4")
    final = os.path.join(OUT, f"{name}.mp4")
    n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "18", "-pix_fmt", "yuv420p", "-f", "mp4", tmp], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        p.stdin.write(fn(t, start + t).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, final)
    return final


if __name__ == "__main__":
    mode = sys.argv[2] if len(sys.argv) > 2 else "render"
    if mode == "stills":
        start = 0
        for name, dur, fn in SCENES:
            fn(dur * 0.9, start + dur * 0.9).convert("RGB").save(os.path.join(OUT, f"{name}_still.jpg"), quality=90)
            start += dur
    else:
        files, start = [], 0
        for name, dur, fn in SCENES:
            files.append(render(name, dur, fn, start))
            start += dur
        with open(os.path.join(OUT, "list.txt"), "w") as f:
            for fl in files:
                f.write(f"file '{os.path.abspath(fl)}'\n")
