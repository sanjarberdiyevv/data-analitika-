# anlyz.uz — kunlik Reels avtomati

Kanal: Instagram @anlyz.uz ("Analitika | Pul va raqamlar"). Har kuni 1 ta o'rgatuvchi moliya Reels.
Egasi: Sanjar. U bilan faqat **o'zbek kirill** yozuvida gaplashiladi. Videodagi matn — o'zbek lotin.

## Kunlik tartib (scheduled run)
1. **Mavzu.** `topics.md` ni o'qing — oldingi mavzularni takrorlamang. Yangi mavzu: kredit, omonat, inflyatsiya,
   valyuta kursi, ipoteka, avtokredit, kartalar, soliq, maosh, narxlar... Shu hafta yangiligi bo'lsa — o'shani oling.
   Mavzu "o'rgatadigan" bo'lsin: aniq hisob + tez formula/qoida. Oddiy fakt (kofe narxi, 50%+50%) — rad etilgan.
2. **Ma'lumot.** WebSearch bilan rasmiy manba (Markaziy bank cbu.uz, Statistika qo'mitasi stat.uz, banklar).
   Har bir raqamni tekshiring, hisob-kitobni python bilan qiling. Ekranga manba + sana yozing.
3. **Ssenariy — FORMAT «KUTILGAN vs HAQIQAT» (Sanjar tanlovi, 14.11.2026; 15.11 dan majburiy).**
   Sabab (Metricool, 07–13.11): har video ~110 qamrovda to'xtaydi, 3 s ichida 46–70% o'tkazib yuboradi,
   o'rtacha tomosha 5–10 s, saqlash 0. Eng uzoq tomosha qilinganlar — savol/jumboqli videolar (17–20 s).
   Ohang: JIDDIY, tushuntiruvchi; yengil kinoya mumkin, so'kinish/haqorat YO'Q. Uzunligi **18–25 s**, 5 abzats:
   - **A Kutilgan (0–2,5 s):** keng tarqalgan ishonch, odamning o'z gapi bilan. Kichik, shaxsiy summa
     (oylik 5 mln, telefon 10 mln, kredit 20–50 mln — 100+ mln emas). Ekranda «KUTILGAN» yorlig'i (kulrang/oq).
     Masalan: "Kutilgan: nasiya — oyiga atigi 1,2 mln, arzimas narsa."
   - **B Haqiqat (2,5–6 s):** «HAQIQAT» yorlig'i (qizil), katta raqam — keskin o'tish (zoom/silkinish).
     "Haqiqat: 12 oyda 4 mln ortiqcha to'laysiz."
   - **C Nega (6–14 s):** 1–2 qisqa gap bilan sababini tushuntiring + oddiy vizual (ustun, chiziq, taqqoslash).
   - **D Qoida (14–20 s):** bitta eslab qolinadigan qoida/formula ("ustama × 1,7", "muddatni qisqartiring").
   - **E CTA (oxirgi 2–3 s):** "Shunday do'stingizni belgilang" yoki "Saqlab qo'ying". Izohda savol.
   Bitta video = bitta fikr. Sonlarni ssenariyda so'z bilan yozing. Vergul kamroq.
   Caption 1-qatori ham shu format: "Kutilgan: … / Haqiqat: …".
   Mavzu g'oyalari: nasiya/Uzum nasiya, kredit karta, erta to'lash, omonat foizi va inflyatsiya, maoshdan soliq,
   ijara vs ipoteka, to'y xarajati (rasmiy ma'lumot bo'lsa), valyuta ayirboshlash spredi, "0% muddatli to'lov".
   Avvalgi mavzularni yangi formatda qayta ishlash MUMKIN (topics.md da "qayta: <sana>" deb yozing).
4. **IKKI REJIM.**
   - **A) Ovozli (kompyuter ulangan run, 18:08):** pastdagi Narakeet yo'li. Bu ASOSIY rejim.
   - **B) Ovozsiz zaxira (bulutli run, 19:30):** avval `topics.md` ni tekshiring — bugungi sana bilan qator bo'lsa
     (ovozli run ishlagan), HECH NARSA QILMANG, faqat to'xtang. Bo'lmasa — ovozsiz video: matn animatsiyasi +
     musiqa + SFX, har sahna ~2,5 s + 0,08 s/belgi (2,5–5 s), jami 25–40 s, hook ≤2,5 s; comp.py kerak emas.
     Joylash vaqti: hozirdan ≥15 daqiqa keyin (20:00 o'tib ketgan bo'lsa — darhol +15 daq).
   - Ovozli run'da Narakeet limiti tugasa yoki brauser ishlamasa → shu run'da ovozsiz variantni qiling.
   **Ovoz — Narakeet (captchasiz)**, built-in browser:
   `https://www.narakeet.com/languages/uzbek-text-to-speech/` → `#trynow` ichida select[name=voice]=`shavkat`,
   select[name=format]=`mp3`, textarea[name=unparsedScript]=ssenariy, input[name=generateaudio].click().
   Sahifa `/app/text-to-audio/?projectId=...` ga o'tadi; ~15 s kuting; "DOWNLOAD" havolasini JS bilan
   `fetch` qilib blob qiling va `<a download="anlyz_voice_YYYYMMDD.mp3">` orqali yuklab oling.
   Fayl `C:\Users\SanjarBerdiyevv\Downloads\` ga tushadi (brauser «Saqlash» oynasini ochadi, lekin fayl to'liq `*.tmp` nomi bilan tushadi — eng yangi mtime'li .tmp ni o'lchami bo'yicha tekshirib stage qiling; Sanjardan hech narsa so'ramang),
   `device_stage_files` bilan workspace'ga oling.
   **Bepul limit ~12 ta.** Agar Narakeet "limit/paid plan" desa → OVOZSIZ variant: matn+animatsiya+musiqa,
   sahnalar uzunligini o'qish tezligiga qarab qo'ying (~2,5–4 s/sahna). Sanjarga xabar bering.
5. **Vaqtlar.** Abzatslar orasida pauza bo'lishi uchun ssenariyda abzatslarni bo'sh qator bilan ajrating.
   `python3 comp.py voice.mp3 N_ABZATS` (TTSMaker) yoki `python3 comp.py voice.mp3 2,3,3,2,2,5,3` (Narakeet: har abzatsdagi gaplar soni — Narakeet har gapdan keyin ~1 s pauza qiladi) → voice_c.wav + timing.json (guruhlar = abzatslar, ichida gap boshlanishlari).
   Narakeet pauzalari TTSMaker'dan farq qiladi — chiqqan guruhlar ssenariyga mos kelishini TEKSHIRING,
   kerak bo'lsa silencedetect natijasiga qarab qo'lda belgilang.
6. **Sahnalar.** `scenes_20261114.py` (yoki `example_scenes_inflyatsiya.py`) andozasi bo'yicha yangi `scenes_YYYYMMDD.py` yozing; sahnalar A–E yuqoridagi Kutilgan/Haqiqat tartibida, A da «KUTILGAN», B da qizil «HAQIQAT» badge
   (`make.py` dan: W,H,LIME,WHITE,GREY,RED, font, glow_text, text_c, base, render). Har abzats = 1 sahna.
   Avval `stills` rejimida kadrlarni ko'ring (matn chetga chiqmasin!), keyin render.
   Shriftlar: /usr/share/fonts/opentype/inter/ (Inter).
7. **Musiqa va yig'ish — HAQIQIY MUSIQA (Sanjar talabi: sintez "tng-tng" emas!).**
   `music/` papkasidagi Pixabay treklaridan mavzuga mosini tanlang (Pixabay Content License: Instagram'da
   bepul, mualliflik da'vosi yo'q, atributsiya shart emas):
   motiv_1/motiv_3 — energik (omonat, daromad, "qanday qilish"); tension_1/tension_2 — xavf, yo'qotish,
   qarz, firibgarlik, minusli hook; chill_1/chill_3 — byudjet, odatlar; inspire_1/inspire_2 — uzoq muddat,
   investitsiya, murakkab foiz; news_1/news_2 — kurs/stavka/qonun yangiliklari.
   Ketma-ket ikki kun bir xil trekni ishlatmang (topics.md ga trek nomini yozing).
   `python3 mix.py video.mp4 voice_c.wav music/<trek>.mp3 out.mp4` (ovozsizda `none`). Musiqa ovoz ostida
   avtomatik pasayadi (ducking). Ixtiyoriy: `music2.py` dan faqat whoosh SFX (5-argument), juda past.
   Mashhur qo'shiqlarni (Spotify/YouTube hitlari) HECH QACHON qo'ymang — Instagram ovozni o'chiradi yoki
   videoni bloklaydi. Yangi trek kerak bo'lsa — faqat pixabay.com/music (kompyuter ulangan run'da brauser orqali).
   1080x1920, 30fps, libx264 crf18 veryfast, aac 192k.
8. **Yuklash.** Video → shu repo `anlyz-reels` branch, `reels/anlyz_YYYYMMDD.mp4`, push.
   Raw URL: `https://raw.githubusercontent.com/sanjarberdiyevv/data-analitika-/anlyz-reels/reels/anlyz_YYYYMMDD.mp4`
9. **Instagram — 1-yo'l: Metricool (to'liq avtomat).** `getBrandSettings` → Instagram ulangan bo'lsa
   `createScheduledPost`: blogId, date = bugun 20:00 Asia/Tashkent, info: providers [{network:"instagram"}],
   instagramData {type:"REEL", showReelOnFeed:true}, media [raw URL], videoCoverMilliseconds = hook kadri (~3000),
   text = caption, autoPublish true. Natijadagi plannerUrl ni hisobotga qo'shing.
   **Bulutli run'da Metricool ulanmagan bo'lsa:** videoni push qiling va Sanjarga raw havolani yuborib,
   "Metricool'ga Instagram'ni ulang (app.metricool.com/brands/connections?blogId=7556886), shunda o'zi joylanadi"
   deb yozing. Kompyuter talab qilmang.
   **2-yo'l (faqat kompyuter ulangan sessiyada, Metricool'da Instagram ulanmagan bo'lsa):** Instagram CSP raw.githubusercontent'dan fetch'ni
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
