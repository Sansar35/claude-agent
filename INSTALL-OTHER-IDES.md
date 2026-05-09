# Diger IDE / AI Assistant'lar Icin Kurulum

`claude-agent` Claude Code icin native uyumludur. Diger AI code asistanlari icin asagidaki adimlar:

## 🚀 Hangi Ortamlarda Calisir

| IDE / Tool | Native uyumlu mu? | Cozum |
|---|---|---|
| **Claude Code CLI** (Anthropic resmi) | ✅ TAM | `install.bat` veya `install.sh` |
| **Cursor** (cursor.sh) | ⚠️ Kismen | `claude-config/agents`, `commands` cogu surumde calisir |
| **Windsurf** (Codeium) | ⚠️ Kismen | `.windsurfrules` formatina cevirin |
| **Antigravity** (Google) | ✅ TAM | Claude Code uzantisi varsa direkt calisir |
| **VS Code Claude extension** | ✅ TAM | Claude Code icin yapilmis |
| **GitHub Copilot Chat** | ❌ | Sadece `team/` Python script'leri kullanin |
| **Cline** (VS Code extension) | ❌ | Sadece `team/` Python script'leri kullanin |
| **Aider** (CLI) | ❌ | Sadece `team/` Python script'leri kullanin |
| **Continue.dev** | ❌ | Sadece `team/` Python script'leri kullanin |

## 📦 Multi-LLM Orkestrator (`team/`) — Her Yerde Calisir

`team/` icindeki Python scriptleri **AI assistant'tan bagimsiz**. Hangi IDE / terminal kullanirsaniz kullanin:

```bash
python team/team.py "FastAPI login API yaz"
python team/demo.py
python team/verify.py
```

## 1️⃣ Claude Code (Anthropic resmi) — TAM UYUM

```cmd
install.bat
```
Veya manuel:
```cmd
xcopy /E /I /Y claude-config\skills %USERPROFILE%\.claude\skills
xcopy /E /I /Y claude-config\agents %USERPROFILE%\.claude\agents
xcopy /E /I /Y claude-config\commands %USERPROFILE%\.claude\commands
```

Kullanim: Claude Code'u yeniden baslat, chat'e `/team "<istek>"` yaz.

## 2️⃣ Cursor (cursor.sh)

Cursor `.cursor/rules/` klasoru veya `.cursorrules` dosyasi kullaniyor. Manuel uyarlama:

```bash
# 1) Kendi projenizde .cursor/rules/ olusturun
mkdir -p .cursor/rules

# 2) team-runner agent'inin sistem prompt'unu kopyalayin
cp claude-config/agents/team-runner.md .cursor/rules/team-runner.mdc
```

Cursor `.mdc` dosyalari "rules" olarak okur.

Slash command icin Cursor'da native destek YOK (Mart 2026 itibariyla). Bunun yerine: chat'e dogal dilde "team-runner agent'iyla calistir, FastAPI login API yaz" yazin.

## 3️⃣ Windsurf (Codeium)

Windsurf `.windsurfrules` dosyasi kullaniyor:

```bash
# Proje root'una kopyala
cat claude-config/agents/team-runner.md > .windsurfrules
echo "" >> .windsurfrules
cat claude-config/CLAUDE.md.example >> .windsurfrules
```

## 4️⃣ Antigravity (Google AI IDE)

Antigravity Claude Code extension destekliyor. `install.bat` ile kurulum yapin, Antigravity'yi yeniden baslatin, "Open Agent Manager"'da `team-runner` gorulmeli.

Eger Antigravity kendi Gemini agent'ini kullaniyorsa:
- Claude entegrasyonunu Antigravity Settings'tan acin
- Veya `team/team.py`'i terminal'den calistirin (IDE-bagimsiz)

## 5️⃣ Generic — Sadece `team/` Python Scriptleri

Tek ihtiyac: Python 3.10+ ve `pip install -r team/requirements.txt`. IDE konusu degil.

Hangi IDE kullanirsaniz kullanin, terminal acip:
```bash
python team/team.py "proje aciklamasi"
```

Cikti dogrudan terminal'de gelir. IDE bagimsizdir.

## 6️⃣ Aider — `.aider.conf.yml` ile

Aider config'inde model rotasi destekliyor:
```yaml
# .aider.conf.yml
model: claude-opus-4-7
weak-model: claude-haiku-4-5
```

Aider tek model kullanir — multi-AI orkestrasyon icin `team/team.py`'yi script olarak calistirin, ciktiyi Aider'a verin.

## 7️⃣ Continue.dev — `config.json` ile

Continue.dev `~/.continue/config.json` kullaniyor:
```json
{
  "models": [
    {"title": "Opus", "provider": "anthropic", "model": "claude-opus-4-7"},
    {"title": "Sonnet", "provider": "anthropic", "model": "claude-sonnet-4-6"}
  ]
}
```

Multi-AI orkestrasyon native YOK — `team/` scriptlerini ayri kullan.

## 🔧 API ile Kullanim (IDE'siz)

Hicbir IDE olmadan da calisir:

```python
# Python ile direkt
from team.team import develop
import asyncio

result = asyncio.run(develop("FastAPI login API yaz"))
print(result)
```

Veya HTTP API olarak yaz (FastAPI/Flask wrapper):
```python
# api.py (kendiniz yazabilirsiniz)
from fastapi import FastAPI
from team.team import develop

app = FastAPI()

@app.post("/team")
async def team_endpoint(brief: str):
    return await develop(brief)
```

## 💡 Onerilen Senaryolar

| Senaryo | Onerilen Kurulum |
|---|---|
| Claude Code kullaniyorum | `install.bat` (TAM uyum) |
| Cursor kullaniyorum | `team/` scriptleri + `.cursor/rules/team-runner.mdc` |
| Antigravity kullaniyorum | `install.bat` + Antigravity restart |
| Hicbiri yok / sade Python | Sadece `pip install` + `python team/team.py` |
| API endpoint yapacagim | `team.develop()` fonksiyonunu FastAPI ile sarin |

## ❓ Sorularin Mi Var?

[GitHub Issues](https://github.com/<your-username>/claude-agent/issues) acin, topluluk yardim eder.
