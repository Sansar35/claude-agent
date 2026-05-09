---
description: Claude Agent Team — Lider Opus + 20+ AI'i paralel calistirip proje gelistirir
argument-hint: "proje aciklamasi (ornek: FastAPI ile JWT login API yaz)"
---

# /team — Multi-AI Ekibi

Sen Multi-AI ekibinin tetikleyicisisin. Kullanicinin istegini farkli AI'lara paralel yazdiracaksin.

## Kullanici Istegi
$ARGUMENTS

## Yapilacaklar
1. Once konfig kontrolu — Bash:
   ```cmd
   python "%USERPROFILE%\claude-agent\team\test.py"
   ```
2. Sonra paralel calistirma — Bash:
   ```cmd
   chcp 65001 && python "%USERPROFILE%\claude-agent\team\team.py" "$ARGUMENTS"
   ```
3. Komut 60-180 saniye surebilir, sabirli bekle.
4. team.py kendi sentezini yapar (Lider Opus son halini verir).
5. Cikti web ise → preview_start ile teyit. CLI ise → kucuk bir test ile teyit.
6. Turkce numarali rapor:
   - Kac AI cevap verdi (kac OK / kac FAIL)
   - Toplam paralel sure
   - Sentez sonucu
   - Test teyit sonucu

## Onemli
- Eger kullanici claude-agent klasorunu farkli yere koyduysa path'i guncelle.
- Bash komutunu foreground calistir.
- Onay sorma, dogrudan calistir.
