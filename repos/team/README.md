# MULTI-AI TEAM

> Lider **Claude Opus 4.7** + **20+ farkli AI** ayni projeyi PARALEL gelistirir.

## Mimari

```
                  ┌──────────────────────────┐
                  │  CLAUDE OPUS 4.7  ★ LIDER │
                  │  (Claude Max abonelik —   │
                  │   key gerekmez)           │
                  └────────────┬──────────────┘
                               │ plan / dagit / sentez
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
   ┌─────────┐         ┌──────────────┐       ┌────────────────┐
   │ Sonnet  │         │  OPENROUTER  │       │ DIREKT KEY'LER │
   │ + Haiku │         │   (1 key →   │       │ Groq/Cerebras/ │
   │ (subs)  │         │  7 model)    │       │  Mistral/xAI/  │
   └─────────┘         │ GPT-5/Gemini │       │  DeepSeek/     │
                       │ DeepSeek/    │       │  Cohere/Pplx/  │
                       │ Llama/Qwen/  │       │  Together/     │
                       │ Mistral/Grok │       │  Fireworks ... │
                       └──────────────┘       └────────────────┘
```

## Kurulum (TEK SEFERLIK)

```cmd
copy C:\Users\emre\.claude\repos\team\.env.example C:\Users\emre\.claude\repos\team\.env
notepad C:\Users\emre\.claude\repos\team\.env
```

Notepad'de **istedigin kadar key** doldur (hangi key'i girersen o ajan ekibe katilir, gerisi pas gecer). Anthropic key'e GEREK YOK — Claude Max aboneligi yetiyor.

## Test (key durumu gor)

```cmd
cd C:\Users\emre\.claude\repos\team
python test.py
```

Cikti: aktif worker listesi + hangi key girilmis.

## Kullanim

```cmd
cd C:\Users\emre\.claude\repos\team
python team.py "FastAPI ile JWT login API yaz, sqlite + bcrypt"
```

Akis:
1. **Lider (Opus)** projeyi `n` alt-goreve bolup ekibe dagitir
2. **Tum worker'lar PARALEL** calisir (asyncio.gather)
3. **Lider** sonuclari sentezleyip son ciktiyi verir

## Yeni AI ekleme

`team.py` icindeki `DIRECTS` listesine bir satir ekle:
```python
("YENI_API_KEY", "litellm-model-id", "agent-name", "Rol Aciklamasi"),
```
`.env`'e `YENI_API_KEY=...` ekle. Tamam.

## Onerilen Key'ler (oncelik sirasi)

1. **OPENROUTER_API_KEY** ★ — tek key ile 7 farkli en gucly model
2. **GROQ_API_KEY** — bedava katmani var, cok hizli
3. **GOOGLE_API_KEY** — Gemini bedava katmani genis
4. **DEEPSEEK_API_KEY** — cok ucuz, kod kalitesi yuksek
5. **CEREBRAS_API_KEY** — saniyede 2000+ token

## Kritik Notlar

- **Anthropic API key girme** — Claude Max aboneligi varsa key gereksiz, claude-agent-sdk Claude Code CLI auth'unu kullanir
- **Hiç key girilmezse** sadece Claude (Opus + Sonnet + Haiku) calisir, bu bile guclu bir ekip
- **Key'ler kullaniciyaa ozel** — `.env` dosyasi git'e commit edilmez (zaten `.gitignore`'a girmesi tavsiye edilir)
- **Maliyet** — her worker bir API cagrisi = potansiyel para. Once `test.py` ile aktif sayiyi kontrol et

---

## 🔗 Key Alma Baglantilari (Tikla → Sayfaya Git)

> `.env` dosyasinin en altinda da ayni liste yorum olarak duruyor — VS Code / Notepad++ icinde Ctrl+Click ile acilir.

### Ana Tavsiye (1 key = 7 model)
| # | Provider | Bedava Katman | Key URL |
|---|---|---|---|
| ★ | **OpenRouter** (GPT-5, Gemini, DeepSeek, Llama, Qwen, Mistral, Grok hepsi) | Var | https://openrouter.ai/keys |

### Bedava Katmani Olanlar (oncelik bunlar)
| Provider | Bedava Limit | Key URL |
|---|---|---|
| **Groq** (Llama 3.3 saniyede 800+ token) | Genis | https://console.groq.com/keys |
| **Google** (Gemini 2.5 Pro) | 1500 req/gun | https://aistudio.google.com/apikey |
| **Cerebras** (Llama 3.3 saniyede 2000+ token) | Var | https://cloud.cerebras.ai/platform |
| **Mistral AI** | La Plateforme dene | https://console.mistral.ai/api-keys |
| **HuggingFace** | Inference API | https://huggingface.co/settings/tokens |
| **NVIDIA NIM** | 1000 cagri/ay bedava | https://build.nvidia.com/explore/discover |
| **Together AI** | $1 kredi | https://api.together.ai/settings/api-keys |

### Ucuz / Kaliteli (kucuk kredi yetiyor)
| Provider | Ozellik | Key URL |
|---|---|---|
| **DeepSeek** | Cok ucuz, kod kalitesi yuksek | https://platform.deepseek.com/api_keys |
| **Fireworks AI** | Production inference | https://fireworks.ai/api-keys |
| **DeepInfra** | Acik kaynak modeller | https://deepinfra.com/dash/api_keys |
| **Cohere** | RAG / Command R+ | https://dashboard.cohere.com/api-keys |
| **Perplexity** | Web bilgili Sonar | https://www.perplexity.ai/account/api/keys |
| **Hyperbolic** | Llama / FLUX | https://app.hyperbolic.xyz/settings |
| **SambaNova** | Hizli Llama | https://cloud.sambanova.ai/apis |

### Premium
| Provider | Ozellik | Key URL |
|---|---|---|
| **OpenAI** (GPT-5) | Direkt OpenAI | https://platform.openai.com/api-keys |
| **xAI** (Grok 3) | X.com entegre | https://console.x.ai |

### NOT
- **Anthropic key girme** — Claude Max aboneligin var, key gereksiz, sistem `claude-agent-sdk` ile abonelik kullanir.
- Bedava katman kullanim limitlerini provider sitesinden teyit et — degisiyor.
