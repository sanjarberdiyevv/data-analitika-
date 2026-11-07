import subprocess, json
gaps=[(4.11,5.10),(5.64,6.58),(7.55,8.32),(11.85,12.80),(17.74,18.50),(21.68,22.67),(25.70,26.45),(33.31,34.28),(38.26,39.03),(40.50,41.49),(43.98,44.97),(47.32,48.10),(48.83,49.78),(53.08,54.05),(56.32,57.05),(57.55,58.51),(60.35,61.37),(62.37,63.34),(66.04,66.79),(67.54,68.51),(70.14,71.12)]
para={7.55,17.74,25.70,38.26,47.32,56.32,66.04}
END=72.0; TEMPO=1.12
segs=[];s=0.0
for a,b in gaps: segs.append((s,a+0.08)); s=b-0.08
segs.append((s,END))
parts=[];t=0.0;onsets=[];pbreak=[]
for i,(a,b) in enumerate(segs):
    onsets.append(t); t+=b-a
    if i<len(gaps):
        g=0.42 if gaps[i][0] in para else 0.22
        if gaps[i][0] in para: pbreak.append(len(onsets))
        parts.append((a,b,g)); t+=g
    else: parts.append((a,b,0.5)); t+=0.5
fc=[];lab=[]
for i,(a,b,g) in enumerate(parts):
    fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,apad=pad_dur={g}[p{i}]");lab.append(f"[p{i}]")
fc.append("".join(lab)+f"concat=n={len(parts)}:v=0:a=1,atempo={TEMPO}[o]")
subprocess.run(["ffmpeg","-y","-v","error","-i","voice.mp3","-filter_complex",";".join(fc),"-map","[o]","-ar","44100","voice_c.wav"],check=True)
on=[x/TEMPO for x in onsets]; tot=t/TEMPO
# group by paragraph
groups=[];cur=[];
for i,o in enumerate(on):
    if i in pbreak: groups.append(cur);cur=[]
    cur.append(round(o,2))
groups.append(cur)
json.dump({"total":round(tot,2),"groups":groups},open("timing.json","w"))
print(round(tot,2));[print(g) for g in groups]
