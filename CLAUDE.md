# Claude Code — Global Rules Template

Bu dosya `claude-agent` paketinin top-level CLAUDE.md sablonudur. Kendi `~/.claude/CLAUDE.md` veya proje `CLAUDE.md` dosyaniza istediginiz bolumleri kopyalayin.

## Iletisim

- Direkt, kisa, sonuc odakli yanit
- "Belki / muhtemelen" gibi belirsiz dil yerine kesin ifade
- Numarali raporlar
- Her teslimat sonu kisa rapor: ne degistirildi, hangi dosyalar etkilendi

## Dosya Disiplini

- Dosya adi verilirse → birebir koru, degistirme
- Tek-dosya HTML/projects: kullanici acikca istemedikce parcalama / modulerlestirme onerme
- Yeni dosya gerekiyorsa once kullaniciya sor

## 31 Kural Protokolu (Iron Laws)

### Disiplin (R1-R10)

- R1: Eski versiyona donmek YASAK
- R2: %100 kusursuz teslim
- R3: `node --check` / linter ile validate
- R4: Sifir dead code, orphan listener, zombie timer
- R5: Clean code, sifir spaghetti
- R6: Bozuk kodu duzelt veya sil
- R7: Post-edit self-check (bracket, ref, scope)
- R8: Edit history yeterli — gereksiz `.bak` dosyalari yaratma
- R9: Coklu gorev = sifir atlama
- R10: Tum dosyayi satir satir tara

### Yapi (R11-R20)

- R11: 200 satir context oku, sonra cerrahi duzenle
- R12: Max 2-3 odakli edit per turn
- R13: Belirsizlikte sor, ama gereksiz onay isteme
- R14: Istenmeyen kod / feature ekleme YASAK
- R15: Tek-dosya mimarisi sacred — bolme/dagitma onerme
- R16: UI bug'da TUM katmanlari (HTML/CSS/JS) tara
- R17: Bug hunt: fixed overlays, pointer-events, opacity, stacking, !important
- R18: Yeni ozellikten once grep ile cakisma kontrolu
- R19: Edit oncesi 200 satir context (yukari + asagi)
- R20: Mental model first, sonra duzenle

### Kalite (R21-R30)

- R21: Silent breakage scan
- R22: %100 garanti yoksa teslim ETME
- R23: Mutlak tarama + chained update + %100
- R24: Numarali rapor zorunlu
- R25: (rezerve)
- R26: Dogru katman teshisi (HTML / CSS / JS)
- R27: SIFIR `console.log` / popup / unrequested notification
- R28: Scrollbar tek merkezi sistem (4px, rgba(0,255,136,0.45))
- R29: Anti-flash CSS HEAD'de zorunlu
- R30: Sifir duplicate fonksiyon

### Mutlak (R31)

- R31: Sert dil olmadan eski versiyona donme YASAK

## Onay Sormadan Teslim (opsiyonel)

- "Devam edeyim mi?" YASAK
- "X mi Y mi?" YASAK
- Plan teklifi sonrasi onay bekleme YASAK
- Kullanici ne dediyse en iyi yorumla → tasarla → uygula → teslim et

Istisnalar (sadece bunlar onay ister):

- Veri silme, dosya silme, klasor silme
- Shared sistem degisikligi (database drop, prod deploy, force push)
- Para harcayacak servis
- Kullanici hesabini etkileyen islem

## Tarayici Teyit Protokolu (web yazilim icin)

Yazilim BITTIGINDE (her edit'te degil, en sonda):

1. `preview_start` ile dev server / dosya ac
2. `preview_screenshot` ile gozle gor
3. `preview_console_logs` ile hata var mi tara
4. TUM butonlar / formlar / route'lar test et
5. Sorun varsa onar → tekrar test
6. Console temiz + tum etkilesimler OK olunca teslim et

Pure logic / CLI degisiklikleri icin: terminal calistir, smoke test yeter.

## Tek-Dosya Disiplini

Kullanici "su dosyaya sunu yap" dediyse:

- AKTIF HEDEF = sadece o dosya
- Tum Edit / Write o dosyaya yapilir
- Yan dosya / yeni klasor / modulerlestirme YASAK
- Yeni dosya gerekiyorsa once kullaniciya sor

## Memory Imports

@learnings/protocol.md
@learnings/tooling.md

@RTK.md
