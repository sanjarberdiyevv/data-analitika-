"""Final audio mix with REAL royalty-free music (Pixabay Content License — free for social media, no attribution).
Usage: python3 mix.py video.mp4 voice_c.wav|none TRACK out.mp4 [sfx.wav]
TRACK: music/<mood>_<n>.mp3. Moods:
  motiv   — energetic corporate (default for savings/income/how-to topics)
  tension — suspense/documentary (debts, losses, scams, hidden fees, hooks with minus numbers)
  chill   — lofi calm (budgeting, habits, everyday money)
  inspire — piano (long-term goals, investing, compounding)
  news    — news/breaking (rate changes, new laws, Central Bank decisions)
Music is ducked under the voice (sidechain). Without voice it plays louder.
Optional sfx.wav (e.g. whooshes from music2.py with very low volume) is mixed quietly.
"""
import subprocess, sys

video, voice, track, out = sys.argv[1:5]
sfx = sys.argv[5] if len(sys.argv) > 5 else None
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video]).decode())
inp = ["-i", video, "-stream_loop", "-1", "-i", track]
fade = f"afade=t=in:st=0:d=0.4,afade=t=out:st={max(0, dur - 1.5):.2f}:d=1.5"
if voice != "none":
    inp += ["-i", voice]
    fc = (f"[1:a]aresample=44100,atrim=0:{dur:.2f},volume=0.55,{fade}[m];"
          f"[2:a]aresample=44100,volume=1.5,apad=whole_dur={dur:.2f},asplit=2[v][vk];"
          f"[m][vk]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[md];"
          f"[v][md]amix=inputs=2:duration=first:normalize=0")
    n = 3
else:
    fc = f"[1:a]aresample=44100,atrim=0:{dur:.2f},volume=0.9,{fade}"
    n = 2
if sfx:
    inp += ["-i", sfx]
    fc += f"[mx];[{n}:a]aresample=44100,volume=0.35[s];[mx][s]amix=inputs=2:duration=first:normalize=0"
fc += f",atrim=0:{dur:.2f},alimiter=limit=0.95[a]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *inp, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
print("ok", out)
