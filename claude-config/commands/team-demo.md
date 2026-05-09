---
description: Multi-AI paralellik testi — kisa soruyla ASCII grafikli kanit
argument-hint: "(opsiyonel) test sorusu"
---

# /team-demo — Paralellik Testi

Kullanici sordu: $ARGUMENTS

(Bos ise default: "Python'da fizzbuzz fonksiyonu yaz, 5 satir")

## Yapilacaklar
1. Bash:
   ```cmd
   chcp 65001 && python "%USERPROFILE%\claude-agent\team\demo.py" "$ARGUMENTS"
   ```
2. Output'u oldugu gibi yazdir (ASCII grafik onemli).
3. Cikti analizi:
   - Kac AI BASLADI (delta < 1s ise paralel)
   - Kac AI BITTI (basari orani)
   - Toplam vs sirayla sure (kazanc yuzdesi)
4. Turkce ozet.

## Onemli
- demo.py kisa soruyla calisir, team.py uzun proje icin.
- Foreground (output canli gelsin).
