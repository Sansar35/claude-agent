# Diger IDE / AI Assistant'lar Icin Kurulum

`claude-agent` config bundle'i Claude Code icin native uyumludur. Diger AI code asistanlari icin asagidaki adimlar.

## 🚀 Hangi Ortamlarda Calisir

| IDE / Tool | Native uyumlu mu? | Cozum |
|---|---|---|
| **Claude Code CLI** (Anthropic resmi) | ✅ TAM | `install.bat` veya `install.sh` |
| **Cursor** (cursor.sh) | ⚠️ Kismen | `claude-config/agents`, `commands` cogu surumde calisir |
| **Windsurf** (Codeium) | ⚠️ Kismen | `.windsurfrules` formatina cevirin |
| **Antigravity** (Google) | ✅ TAM | Claude Code uzantisi varsa direkt calisir |
| **VS Code Claude extension** | ✅ TAM | Claude Code icin yapilmis |
| **GitHub Copilot Chat** | ❌ | Native destek yok |
| **Cline** (VS Code extension) | ❌ | Native destek yok |
| **Aider** (CLI) | ❌ | Native destek yok |
| **Continue.dev** | ❌ | Native destek yok |

## 1️⃣ Claude Code (Anthropic resmi) — TAM UYUM

```cmd
install.bat
```

Veya manuel:

```cmd
xcopy /E /I /Y claude-config\skills %USERPROFILE%\.claude\skills
xcopy /E /I /Y claude-config\agents %USERPROFILE%\.claude\agents
xcopy /E /I /Y claude-config\commands %USERPROFILE%\.claude\commands
xcopy /E /I /Y claude-config\hooks %USERPROFILE%\.claude\hooks
xcopy /E /I /Y claude-config\hooks-templates %USERPROFILE%\.claude\hooks-templates
xcopy /E /I /Y claude-config\mcps-templates %USERPROFILE%\.claude\mcps-templates
xcopy /E /I /Y claude-config\settings-templates %USERPROFILE%\.claude\settings-templates
```

Kullanim: Claude Code'u yeniden baslat, chat'e `/` yaz, slash command'lari gor.

## 2️⃣ Cursor (cursor.sh)

Cursor `.cursor/rules/` klasoru veya `.cursorrules` dosyasi kullaniyor. Agent prompt'larini Cursor rule formatina ceviripayik kullanabilirsin:

```bash
# 1) Kendi projende .cursor/rules/ olustur
mkdir -p .cursor/rules

# 2) Istedigin agent'i kopyala (.md → .mdc)
cp claude-config/agents/code-reviewer.md .cursor/rules/code-reviewer.mdc
```

Cursor `.mdc` dosyalarini "rules" olarak okur.

Slash command icin Cursor'da native destek SINIRLI. Onun yerine: chat'e dogal dilde "code-reviewer prompt'uyla calis, su PR'i gozden gecir" yaz.

## 3️⃣ Windsurf (Codeium)

Windsurf `.windsurfrules` dosyasi kullaniyor:

```bash
# Proje root'una kopyala
cat claude-config/CLAUDE.md.example > .windsurfrules
echo "" >> .windsurfrules
cat claude-config/agents/code-reviewer.md >> .windsurfrules
```

## 4️⃣ Antigravity (Google AI IDE)

Antigravity Claude Code extension destekliyor. `install.bat` ile kurulum yap, Antigravity'yi yeniden baslat, agent'lar otomatik gozukur.

Eger Antigravity kendi Gemini agent'ini kullaniyorsa:

- Claude entegrasyonunu Antigravity Settings'tan ac
- Veya kendi prompt'unda `claude-config/CLAUDE.md.example` icerigini reference olarak ekle

## 5️⃣ Aider — `.aider.conf.yml` ile

Aider config'i model rotasini destekler:

```yaml
# .aider.conf.yml
model: claude-opus-4-7
weak-model: claude-haiku-4-5
```

Aider tek model kullanir — multi-agent orkestrasyon native yok. Ancak Claude Code prompt'larini elle Aider'a verebilirsin.

## 6️⃣ Continue.dev — `config.json` ile

Continue.dev `~/.continue/config.json` kullaniyor:

```json
{
  "models": [
    {"title": "Opus", "provider": "anthropic", "model": "claude-opus-4-7"},
    {"title": "Sonnet", "provider": "anthropic", "model": "claude-sonnet-4-6"}
  ]
}
```

`claude-config/CLAUDE.md.example` icerigini Continue'nun system prompt'una ekleyebilirsin.

## 💡 Onerilen Senaryolar

| Senaryo | Onerilen Kurulum |
|---|---|
| Claude Code kullaniyorum | `install.bat` (TAM uyum) |
| Cursor kullaniyorum | `.cursor/rules/` altina manuel kopya |
| Antigravity kullaniyorum | `install.bat` + Antigravity restart |
| VS Code + Claude extension | `install.bat` (TAM uyum) |

## ❓ Sorularin Mi Var?

[GitHub Issues](https://github.com/Sansar35/claude-agent/issues) acin.
