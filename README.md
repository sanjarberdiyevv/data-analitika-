# anlyz.uz — kunlik Reels avtomati

Kanal: Instagram @anlyz.uz ("Analitika | Pul va raqamlar"). Har kuni 1 ta o'rgatuvchi moliya Reels.
Egasi: Sanjar. U bilan faqat **o'zbek kirill** yozuvida gaplashiladi. Videodagi matn — o'zbek lotin.

## Kunlik tartib (scheduled run)
1. **Mavzu.** `topics.md` ni o'qing — oldingi mavzularni takrorlamang. Yangi mavzu: kredit, omonat, inflyatsiya,
   valyuta kursi, ipoteka, avtokredit, kartalar, soliq, maosh, narxlar... Shu hafta yangiligi bo'lsa — o'shani oling.
   Mavzu "o'rgatadigan" bo'lsin: aniq hisob + tez formula/qoida. Oddiy fakt (kofe narxi, 50%+50%) — rad etilgan.
2. **Ma'lumot.** WebSearch bilan rasmiy manba (Markaziy bank cbu.uz, Statistika qo'mitasi stat.uz, banklar).
   Har bir raqamni tekshiring, hisob-kitobni python bilan qiling. Ekranga manba + sana yozing.
3. **Ssenariy** (o'zbek lotin, 6–8 abzats, 35–50 s): 1-abzats — kuchli hook (shaxsiy pulga tegadigan aniq raqam,
   1–2 soniyada). Oxirgi abzats — CTA ("Saqlab qo'ying / do'stingizga yuboring / izohda yozing").
   Sonlarni so'z bilan yozing ("o'n sakkiz foiz"). Vergul kamroq — har vergul pauza beradi.
4. **Ovoz — Narakeet (captchasiz)**, built-in browser:
   `https://www.narakeet.com/languages/uzbek-text-to-speech/` → `#trynow` ichida select[name=voice]=`shavkat`,
   select[name=format]=`mp3`, textarea[name=unparsedScript]=ssenariy, input[name=generateaudio].click().
   Sahifa `/app/text-to-audio/?projectId=...` ga o'tadi; ~15 s kuting; "DOWNLOAD" havolasini JS bilan
   `fetch` qilib blob qiling va `<a download="anlyz_voice_YYYYMMDD.mp3">` orqali yuklab oling.
   Fayl `C:\Users\SanjarBerdiyevv\Downloads\` ga tushadi (ba'zan `*.tmp` nomi bilan — eng yangi mtime faylini oling),
   `device_stage_files` bilan workspace'ga oling.
   **Bepul limit ~12 ta.** Agar Narakeet "limit/paid plan" desa → OVOZSIZ variant: matn+animatsiya+musiqa,
   sahnalar uzunligini o'qish tezligiga qarab qo'ying (~2,5–4 s/sahna). Sanjarga xabar bering.
5. **Vaqtlar.** Abzatslar orasida pauza bo'lishi uchun ssenariyda abzatslarni bo'sh qator bilan ajrating.
   `python3 comp.py voice.mp3 N_ABZATS` → voice_c.wav + timing.json (guruhlar = abzatslar, ichida gap boshlanishlari).
   Narakeet pauzalari TTSMaker'dan farq qiladi — chiqqan guruhlar ssenariyga mos kelishini TEKSHIRING,
   kerak bo'lsa silencedetect natijasiga qarab qo'lda belgilang.
6. **Sahnalar.** `example_scenes_inflyatsiya.py` andozasi bo'yicha yangi `scenes_YYYYMMDD.py` yozing
   (`make.py` dan: W,H,LIME,WHITE,GREY,RED, font, glow_text, text_c, base, render). Har abzats = 1 sahna.
   Avval `stills` rejimida kadrlarni ko'ring (matn chetga chiqmasin!), keyin render.
   Shriftlar: /usr/share/fonts/opentype/inter/ (Inter).
7. **Musiqa va yig'ish.** `python3 music2.py music.wav TOTAL whoosh_vaqtlari pop_vaqtlari`;
   ffmpeg: video + voice_c.wav (volume 1.6) + music (volume 0.22), amix normalize=0, alimiter.
   1080x1920, 30fps, libx264 crf18 veryfast, aac 192k.
8. **Yuklash.** Video → shu repo `anlyz-reels` branch, `reels/anlyz_YYYYMMDD.mp4`, push.
   Raw URL: `https://raw.githubusercontent.com/sanjarberdiyevv/data-analitika-/anlyz-reels/reels/anlyz_YYYYMMDD.mp4`
9. **Instagram — 1-yo'l: Metricool (to'liq avtomat).** `getBrandSettings` → Instagram ulangan bo'lsa
   `createScheduledPost`: blogId, date = bugun 20:00 Asia/Tashkent, info: providers [{network:"instagram"}],
   instagramData {type:"REEL", showReelOnFeed:true}, media [raw URL], videoCoverMilliseconds = hook kadri (~3000),
   text = caption, autoPublish true. Natijadagi plannerUrl ni hisobotga qo'shing.
   **2-yo'l (Metricool'da Instagram ulanmagan bo'lsa):** Instagram CSP raw.githubusercontent'dan fetch'ni
   bloklaydi, shuning uchun JS bilan faylni bera olmaysiz. Videoni `device_commit_files` bilan
   `Downloads\anlyz_YYYYMMDD.mp4` ga yozing, instagram.com → "+" → "Выбрать на компьютере" bosing va
   Sanjardan faylni tanlashni so'rang (Ctrl+Shift+B). Keyin: "Оригинал" nisbat → Далее → muqova hook kadri →
   Далее → caption → "Поделиться" → "Видео Reels опубликовано" ni tekshiring.
10. **Caption:** hook qatori, 3–4 qator asosiy raqamlar, 🧮 formula, 📌 CTA, 💬 savol, Manba, 5 ta heshteg
    (#moliyaviysavodxonlik #analitika #anlyzuz + 2 ta mavzuga oid).
11. **Log.** `topics.md` ga sana | mavzu | hook | asosiy raqamlar | manba qatorini qo'shing, push.
12. Sanjarga kirill o'zbekchada qisqa hisobot (SendUserMessage + PushNotification): nima joylandi.

## Muammo bo'lsa
- Kompyuter/ilova o'chiq, browser javob bermasa → videoni tayyorlab, repo'ga push qiling va Sanjarga
  "kompyuter yoqilganda joylash kerak" deb yozing.
- Instagram login so'rasa — parol kiritmang, Sanjarga ayting.
- Captcha chiqsa — aylanib o'tmang.
