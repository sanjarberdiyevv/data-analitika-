"""Compress TTSMaker voice + get per-paragraph sentence onsets.
Usage: python3 comp.py voice.mp3 N_PARAGRAPHS [tempo=1.12]
Writes voice_c.wav and timing.json {"total":..,"groups":[[onsets of paragraph 1],...]}.
TTSMaker (paragraph pause 600ms) leaves ~0.75s gaps between paragraphs and ~0.95s gaps
after sentences. Paragraph breaks = the (N-1) gaps whose length is closest to 0.76s.
ALWAYS check the printed groups make sense against the script.
"""
import subprocess, json, re, sys

src, NP = sys.argv[1], int(sys.argv[2])
TEMPO = float(sys.argv[3]) if len(sys.argv) > 3 else 1.12
END = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
log = subprocess.run(["ffmpeg", "-i", src, "-af", "silencedetect=noise=-38dB:d=0.5", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
gaps = [(a, b) for a, b in zip(st, en) if b < END - 0.05]
para = set(sorted(gaps, key=lambda g: abs((g[1] - g[0]) - 0.76))[: NP - 1])
segs, s = [], 0.0
for a, b in gaps:
    segs.append((s, a + 0.08)); s = b - 0.08
segs.append((s, END))
parts, t, onsets, pbreak = [], 0.0, [], []
for i, (a, b) in enumerate(segs):
    onsets.append(t); t += b - a
    if i < len(gaps):
        isp = gaps[i] in para
        g = 0.42 if isp else 0.22
        if isp: pbreak.append(i + 1)
    else:
        g = 0.5
    parts.append((a, b, g)); t += g
fc, lab = [], []
for i, (a, b, g) in enumerate(parts):
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,apad=pad_dur={g}[p{i}]"); lab.append(f"[p{i}]")
fc.append("".join(lab) + f"concat=n={len(parts)}:v=0:a=1,atempo={TEMPO}[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", ";".join(fc), "-map", "[o]", "-ar", "44100", "voice_c.wav"], check=True)
on = [x / TEMPO for x in onsets]
groups, cur = [], []
for i, o in enumerate(on):
    if i in pbreak: groups.append(cur); cur = []
    cur.append(round(o, 2))
groups.append(cur)
json.dump({"total": round(t / TEMPO, 2), "groups": groups}, open("timing.json", "w"))
print("total", round(t / TEMPO, 2))
for g in groups: print(g)
