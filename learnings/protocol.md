# Development Protocol — Iron Laws

Aşağıdaki kurallar Emre'nin tüm kod çalışmalarında geçerlidir. Claude Code bunları her oturumda uygular.

## Core Principles
- **Sıfır bug, sıfır console hatası, sıfır warning.** Yarım iş yasak.
- **%100 teslimat veya düzeltmeye devam.** "Neredeyse bitti" = başarısızlık.
- **Single-file HTML mimarisi kutsal.** Tek dosya prensibi asla bölünmez, modülerleştirilmez.

## Code Quality
- Her JS düzenlemesinden sonra `node --check` ile validate et.
- Browser testi yasak — sadece code-level doğrulama.
- Orphan listener, zombie timer, undefined ref, eksik parantez → anında bul ve sil.
- Maksimum 2-3 odaklı edit per turn. Büyük dosyada 10+ edit zorlama.

## Edit Discipline
- Her düzenleme öncesi `cp file file.bak` (sıralı: .bak, .bak2, .bak3).
- Hedef kodun 200 satır üstü/altı oku, caller/callee fonksiyonları bul.
- Düzenleme sonrası: bracket balance, broken ref, duplicate code, scope error grep.
- Orijinale dönmek YASAK. Her güncelleme önceki sürüm üzerine v1→v2→v3.

## Multi-Request Handling
- Tek mesajda birden fazla iş varsa: 1️⃣2️⃣3️⃣ numaralandır, sırayla çöz.
- Bir tanesini bile atlama. Eksik = TÜM TESLİMAT RED.

## UI Bug Hunting
- Önce DOM→CSS→JS mental haritası kur, sonra kod değiştir.
- Tara: position:fixed+inset:0 overlay, pointer-events chain, opacity:0 child, will-change/transform stacking, duplicate ID, !important specificity.
- Yanlış katmana müdahale yasak. CSS sorunu JS ile çözülmez.

## Delivery Format
- Her güncelleme sonu Türkçe rapor: numaralı değişiklikler, 🔒 Garanti %, ✅ checkler.
- Yalan PASSED yasak. %100 olmadan teslim edilmez.
- Dosya adı korunur — Emre ne dediyse o.