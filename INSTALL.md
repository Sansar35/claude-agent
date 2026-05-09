# 📦 Kurulum Rehberi

## 1. Sistem Gereksinimleri

- **Python 3.10+** (3.13 önerilir)
- **Claude Code CLI** (Lider Claude için — abonelik gerekir, key opsiyonel)
- **Git** (klonlama için)
- Windows / macOS / Linux — hepsi destekli

## 2. Adım Adım

### 2.1 Repo'yu klonla
```bash
git clone https://github.com/<your-username>/claude-agent.git
cd claude-agent
```

### 2.2 Python ortamı (opsiyonel ama önerilir)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2.3 Bağımlılıkları kur
```bash
pip install -r team/requirements.txt
```

Bu komut şunları kurar:
- `claude-agent-sdk` — Claude Max abonelik üzerinden Claude çağrısı
- `litellm` — 100+ LLM provider'a tek API
- `python-dotenv` — .env dosyası yükleme

### 2.4 Claude Code CLI (Lider için ZORUNLU)

Claude Opus / Sonnet / Haiku abonelik üzerinden çalışır, `claude.exe` CLI gerekir.

**Kurulum** (Anthropic resmi):
- https://docs.claude.com/en/docs/claude-code/quickstart
- Veya: `npm install -g @anthropic-ai/claude-code`
- Sonra: `claude login` ile abonelik authentikasyonu

**Eğer Claude Max aboneliğin YOKSA** → API key kullan:
```bash
# .env dosyasına ekle:
ANTHROPIC_API_KEY=sk-ant-...
```
Sistem otomatik algılar, abonelik yerine API key kullanır.

### 2.5 Diğer Provider Key'leri (opsiyonel, hangini istersen)

```bash
cp team/.env.example team/.env
```

`team/.env`'i metin editöründe aç. Hangi provider'ı kullanmak istiyorsan o satıra key yapıştır:

```env
OPENROUTER_API_KEY=sk-or-v1-...    # tek key = 7 model birden
GROQ_API_KEY=gsk_...               # bedava katman var
GOOGLE_API_KEY=AIza...             # Gemini bedava katman
CEREBRAS_API_KEY=csk-...
MISTRAL_API_KEY=...
TOGETHER_API_KEY=tgp_v1_...
# ... vs
```

**Hangi key'i nereden alacağını bilmiyorsan**: `key.html` dosyasını tarayıcında aç (çift tıkla). Her provider için kart + "Key Al" butonu var.

### 2.6 Test

```bash
# Hangi ajanlar aktif gör
python team/test.py

# Her ajan gerçek HTTP istek atıyor mu (token sayısı + latency ile kanıt)
python team/verify.py

# Paralellik demo'su (ASCII grafik)
python team/demo.py "Python'da fizzbuzz yaz"
```

### 2.7 Asıl Kullanım

```bash
python team/team.py "FastAPI ile JWT login API yaz"
```

Akış:
1. Lider (Claude Opus) projeyi alt-görevlere böler
2. Tüm worker'lar paralel iş yapar
3. Lider sentezleyip son halini verir

## 3. Claude Code / Cursor / Antigravity Entegrasyonu

`claude-code-config/` klasöründeki dosyaları Claude Code config dizinine kopyalayın → `/team` slash command ve subagent dispatch otomatik aktif olur.

Detay: [`claude-code-config/README.md`](claude-code-config/README.md)

## 4. Sorun Giderme

| Hata | Çözüm |
|---|---|
| `ModuleNotFoundError: claude_agent_sdk` | `pip install -r team/requirements.txt` |
| `Claude CLI not found` | https://docs.claude.com/claude-code adresinden Claude Code CLI kur |
| `RateLimitError` (Gemini) | Bedava katman dakika limiti — 1-2 dk bekle |
| `Payment required` (Cerebras) | Cerebras hesabında billing aktif değil — 5$ kredi yükle veya başka provider kullan |
| `Model not found` | Provider hesabında o model erişimi yok — `python verify.py` ile mevcut modelleri gör |
| Windows'ta Türkçe karakter bozuk | CMD'de `chcp 65001` çalıştır |

## 5. Geliştirme

Yeni provider ekleme — 5 dakikalık iş:
1. `team/team.py` içindeki `DIRECTS` listesine bir satır ekle:
   ```python
   ("YOUR_API_KEY", "litellm-model-id", "agent-name", "Rol Açıklaması"),
   ```
2. `team/.env.example`'a `YOUR_API_KEY=` ekle
3. Bitti — sonraki run'da otomatik aktif olur

## 6. Mimari

```
team/team.py      ← orchestrator (Lider + worker dispatch)
team/demo.py      ← paralellik testi (asyncio.gather + zaman ölçer)
team/verify.py    ← her endpoint'e ping + latency + token raporu
team/test.py      ← konfig özet
```

`team.py` iki katman:
1. **Anthropic katmanı** — `claude-agent-sdk` üzerinden subprocess (key opsiyonel)
2. **Diğer provider'lar** — `litellm` üzerinden HTTP (key zorunlu)

Lider: Claude Opus 4.7. Worker'lar: aktif key olan tüm provider'lar otomatik dahil.
