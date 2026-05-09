<div align="center">

# 🤖 Claude Agent

### Multi-LLM AI agent team with **Claude Opus** as the leader

**18 providers · 75 models · 11.000+ community skills · Single command install**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Multi-IDE](https://img.shields.io/badge/IDE-Claude_Code_·_Cursor_·_Antigravity_·_VS_Code-purple.svg)](INSTALL-OTHER-IDES.md)
[![Providers](https://img.shields.io/badge/Providers-18-orange.svg)](#-supported-providers)
[![Models](https://img.shields.io/badge/Models-75-red.svg)](#-supported-providers)
[![Skills](https://img.shields.io/badge/Community_Skills-11k+-blueviolet.svg)](#-community-content)

---

**One leader, many minds.** Claude Opus orchestrates a team of frontier LLMs that work **in parallel** on the same project, then synthesizes the best output. Pay only for the keys you set — every API key activates a new worker.

</div>

---

## 🎬 What You Get

```
You: "Build me a FastAPI JWT login endpoint with sqlite + bcrypt"

  ┌─ Claude Opus 4.7 (Leader)  ──► breaks task into 8 sub-tasks
  │
  ├─ Claude Sonnet 4.6   ──► writes the architecture
  ├─ Claude Haiku 4.5    ──► writes utility helpers
  ├─ Google Gemini 2.5   ──► reviews for bugs
  ├─ Mistral Large       ──► writes documentation
  ├─ Groq Llama 3.3      ──► writes pytest tests
  ├─ Cerebras Qwen 235B  ──► optimizes performance
  ├─ Together Llama      ──► writes deployment config
  │
  └─ Claude Opus (Leader) ──► synthesizes all outputs into final code
```

**Result:** production-ready code in ~30 seconds (vs. ~4 minutes if run sequentially).

---

## 🏗️ Architecture

```
                  ┌────────────────────────────────────┐
                  │   ⭐  CLAUDE OPUS 4.7  (LEADER)     │
                  │   Plan · Delegate · Synthesize     │
                  │   (Claude Max subscription)        │
                  └────────────────┬───────────────────┘
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       ▼                           ▼                           ▼
 ┌───────────┐         ┌────────────────────┐       ┌──────────────────────┐
 │  Anthropic │         │   OpenRouter      │       │   Direct Providers    │
 │  Sonnet    │         │   1 key →         │       │   Groq · Cerebras     │
 │  Haiku     │         │   7 models        │       │   Mistral · DeepSeek  │
 │  (subs)    │         │   GPT-5/Gemini/   │       │   xAI · Cohere        │
 │            │         │   DeepSeek/Llama/ │       │   Perplexity ·        │
 │            │         │   Qwen/Mistral/   │       │   Together · Fireworks│
 │            │         │   Grok            │       │   NVIDIA · HF · ...   │
 └───────────┘         └────────────────────┘       └──────────────────────┘

  asyncio.gather(*workers)  ──►  parallel HTTP / subprocess execution
```

---

## ⚡ Quick Start

### 🪟 Windows (one-liner)
```cmd
git clone https://github.com/Sansar35/claude-agent.git %USERPROFILE%\claude-agent && cd /d %USERPROFILE%\claude-agent && install.bat
```

### 🍎 macOS / 🐧 Linux (one-liner)
```bash
git clone https://github.com/Sansar35/claude-agent.git ~/claude-agent && cd ~/claude-agent && chmod +x install.sh && ./install.sh
```

The installer:
1. ✅ Copies `claude-config/` → `~/.claude/` (skills, agents, slash commands)
2. ✅ Sets up the orchestrator in `team/`
3. ✅ Provides `install.bat` / `install.sh` to re-run anytime

Then add API keys (whichever providers you want):
```bash
cd team
cp .env.example .env
# Edit .env — only the keys you set will be activated
```

Test it:
```bash
python team/test.py     # See active workers
python team/verify.py   # Prove every endpoint actually receives requests
python team/demo.py     # Watch parallelism live (ASCII timeline)
python team/team.py "Write a FastAPI JWT login API"
```

---

## ✨ Features

### Core
- 🧠 **Hierarchical orchestration** — Opus plans, workers execute, Opus synthesizes
- ⚡ **True parallelism** — `asyncio.gather` runs all workers concurrently
- 🔌 **Plug-and-play providers** — drop a key in `.env`, that worker auto-joins
- 💰 **No Anthropic key needed** — works with Claude Max subscription via `claude-agent-sdk`
- 🎚️ **Two modes** — `light` (3 Claude only, fast/cheap) or `heavy` (all providers, max coverage)
- 📊 **Verification tools** — prove HTTP requests are real (latency + token counts)

### Bundle Extras
- 📚 **8.619 community skills** — from `claude-api` to `frontend-design` to `mcp-builder`
- 🤖 **591 specialized subagents** — `code-reviewer`, `security-auditor`, `debugger`, ...
- ⚡ **417 slash commands** — `/commit`, `/review`, `/deploy`, ...
- 📦 **1.141 awesome-claude-skills** references
- 🔧 **Templates** — hooks, MCPs, settings

---

## 🌐 Supported Providers

| # | Provider | Env Variable | Free Tier? | Get Key |
|---|---|---|:-:|---|
| 1 | **OpenRouter** ⭐ | `OPENROUTER_API_KEY` | Trial | [openrouter.ai/keys](https://openrouter.ai/keys) |
| 2 | OpenAI (GPT-5/o1/o3/4o) | `OPENAI_API_KEY` | ❌ | [platform.openai.com](https://platform.openai.com/api-keys) |
| 3 | Google Gemini (2.5/2.0/1.5) | `GEMINI_API_KEY` | ✅ 1500/day | [aistudio.google.com](https://aistudio.google.com/apikey) |
| 4 | Google Direct | `GOOGLE_API_KEY` | ✅ | [aistudio.google.com](https://aistudio.google.com/apikey) |
| 5 | DeepSeek (chat + reasoner) | `DEEPSEEK_API_KEY` | 💰 cheap | [platform.deepseek.com](https://platform.deepseek.com/api_keys) |
| 6 | Mistral (large + medium) | `MISTRAL_API_KEY` | Trial | [console.mistral.ai](https://console.mistral.ai/api-keys) |
| 7 | Groq (Llama 3.3 — 800+ tok/s) | `GROQ_API_KEY` | ✅ generous | [console.groq.com](https://console.groq.com/keys) |
| 8 | Cerebras (Qwen / Llama — 2000+ tok/s) | `CEREBRAS_API_KEY` | Trial | [cloud.cerebras.ai](https://cloud.cerebras.ai/platform) |
| 9 | Together AI | `TOGETHER_API_KEY` | $1 credit | [api.together.ai](https://api.together.ai/settings/api-keys) |
| 10 | Fireworks AI | `FIREWORKS_API_KEY` | Trial | [fireworks.ai](https://fireworks.ai/api-keys) |
| 11 | xAI (Grok 3) | `XAI_API_KEY` | ❌ | [console.x.ai](https://console.x.ai) |
| 12 | Cohere (Command R+) | `COHERE_API_KEY` | Trial | [dashboard.cohere.com](https://dashboard.cohere.com/api-keys) |
| 13 | Perplexity (Sonar Pro) | `PERPLEXITY_API_KEY` | 💰 cheap | [perplexity.ai/account/api](https://www.perplexity.ai/account/api/keys) |
| 14 | DeepInfra | `DEEPINFRA_API_KEY` | 💰 cheap | [deepinfra.com](https://deepinfra.com/dash/api_keys) |
| 15 | Hyperbolic | `HYPERBOLIC_API_KEY` | Trial | [hyperbolic.xyz](https://app.hyperbolic.xyz/settings) |
| 16 | SambaNova | `SAMBANOVA_API_KEY` | Trial | [cloud.sambanova.ai](https://cloud.sambanova.ai/apis) |
| 17 | NVIDIA NIM | `NVIDIA_API_KEY` | ✅ 1000/mo | [build.nvidia.com](https://build.nvidia.com/explore/discover) |
| 18 | HuggingFace | `HUGGINGFACE_API_KEY` | ✅ | [huggingface.co/settings](https://huggingface.co/settings/tokens) |

> 💡 **Tip:** Open `key.html` in your browser — every provider has a clickable card with a "Get Key" button.

---

## 📂 Project Structure

```
claude-agent/
│
├── 📄 README.md                  ← you are here
├── 📄 INSTALL.md                 ← detailed install guide
├── 📄 INSTALL-OTHER-IDES.md      ← Cursor / Windsurf / Aider / Cline
├── 📄 LICENSE                    ← MIT
├── 📄 .gitignore
├── 🌐 key.html                   ← in-browser key cheat sheet
├── 🪟 install.bat                ← Windows auto-installer
├── 🐧 install.sh                 ← macOS / Linux auto-installer
│
├── 🤖 team/                      ← THE ORCHESTRATOR
│   ├── team.py                   ← leader + worker dispatcher (481 lines)
│   ├── demo.py                   ← parallelism test (ASCII timeline)
│   ├── verify.py                 ← prove every endpoint receives HTTP
│   ├── test.py                   ← config snapshot
│   ├── README.md
│   ├── requirements.txt          ← claude-agent-sdk · litellm · python-dotenv
│   ├── .env.example              ← key template
│   └── .gitignore
│
└── 📦 claude-config/             ← Claude Code .claude/ extras
    ├── skills/                   ← 8.619 community skills
    ├── agents/                   ← 591 specialized subagents
    ├── commands/                 ← 417 slash commands
    ├── awesome-claude-skills/    ← 1.141 awesome refs
    ├── hooks/                    ← 21 hooks
    ├── hooks-templates/          ← 57 templates
    ├── mcps-templates/           ← 85 MCP templates
    ├── settings-templates/       ← 67 setting templates
    ├── CLAUDE.md.example         ← starter rules template
    └── settings.example.json     ← starter settings template
```

**Total: 11.016 files / 105 MB**

---

## 🌍 IDE Compatibility

| IDE / Tool | Native | Slash `/team` | Subagent | Python `team.py` |
|---|:-:|:-:|:-:|:-:|
| **Claude Code** (Anthropic CLI) | ✅ | ✅ | ✅ | ✅ |
| **Antigravity** (Google AI IDE) | ✅ | ✅ | ✅ | ✅ |
| **VS Code** + Claude extension | ✅ | ✅ | ✅ | ✅ |
| **Cursor** | ⚠️ rules | ❌ | ⚠️ | ✅ |
| **Windsurf** (Codeium) | ⚠️ rules | ❌ | ⚠️ | ✅ |
| **Cline** / **Aider** / **Continue** | ❌ | ❌ | ❌ | ✅ |
| **Plain Python** (any terminal) | — | — | — | ✅ |

> The `team/` Python scripts work **everywhere** — IDE-agnostic. Detailed guidance: [INSTALL-OTHER-IDES.md](INSTALL-OTHER-IDES.md).

---

## 🧪 Verification

`python team/verify.py` proves every active worker actually fires HTTP requests:

```
[ANTHROPIC LAYER - claude-agent-sdk subprocess]
  ✓  Claude Opus 4.7    | claude.exe subprocess          | 24.49s | resp: pong
  ✓  Claude Sonnet 4.6  | claude.exe subprocess          | 26.62s | resp: pong
  ✓  Claude Haiku 4.5   | claude.exe subprocess          | 25.15s | resp: pong

[EXTERNAL PROVIDERS - LiteLLM HTTP]
  ✓  Mistral            | api.mistral.ai                 |  1.21s | resp: Pong  | 13 tokens
  ✓  Groq               | api.groq.com                   |  1.01s | resp: pong  | 43 tokens
  ✓  Together           | api.together.xyz               |  3.70s | resp: pong  | 43 tokens
  ✓  Cerebras           | api.cerebras.ai                |  0.45s | resp: pong  |  7 tokens
  ✓  Gemini             | generativelanguage.googleapis.com | 0.62s | resp: pong | 8 tokens

PROOF: 8 agents actually sent HTTP requests (latency > 0, response received)
```

Token counts + latency = real LLM execution + network round-trip. **Not simulated.**

---

## 🎮 Usage Examples

### Light mode (3 Claude only — fast, cheap)
```python
from team.team import develop
import asyncio

result = asyncio.run(develop("Refactor this function for clarity", mode="light"))
print(result)
```

### Heavy mode (all active providers — best coverage, default)
```python
result = asyncio.run(develop("Build a multi-tenant SaaS billing module"))
```

### CLI (terminal-friendly)
```bash
python team/team.py "Build a multi-tenant SaaS billing module"
```

### Slash command (Claude Code / Antigravity)
```
/team Build a multi-tenant SaaS billing module
```

### Demo (parallelism proof)
```bash
python team/demo.py "Write a Python fizzbuzz function"
```
Output:
```
+ 0.00s  >> Claude Sonnet 4.6     STARTED
+ 0.01s  >> Claude Haiku 4.5      STARTED
+ 0.02s  >> Google Gemini         STARTED
+ 0.02s  >> Mistral Direct        STARTED
+ 0.03s  >> Groq Llama 3.3        STARTED
+ 0.03s  >> Cerebras Llama 3.3    STARTED
+ 0.04s  >> Together Llama 3.3    STARTED

ZAMAN CIZGISI (each agent's runtime)
  Claude Opus 4.7    |####################                    | 20.73s
  Claude Sonnet 4.6  |##########################              | 25.03s
  Claude Haiku 4.5   |#######################################  | 34.37s
  Google Gemini      |#                                       |  0.59s
  Mistral Direct     |##                                      |  1.63s
  Groq Llama 3.3     |#                                       |  0.72s
  Cerebras Llama     |#                                       |  0.77s
  Together AI        |#####                                   |  3.87s

PARALEL ANALYSIS
  Active AIs       : 8
  Parallel time    : 34.38s
  Sequential time  : 87.73s
  GAIN             : 53.35s (61% faster)
  RESULT           : >>> ALL AGENTS RAN IN PARALLEL <<<
```

---

## 📦 Community Content (auto-installed via `install.bat`)

After running `install.bat`, your `~/.claude/` directory will contain:

- **8.619 skills** — from `claude-api` to `frontend-design` to `deep-research`
- **591 subagents** — `code-reviewer`, `security-auditor`, `debugger`, `test-automator`, ...
- **417 slash commands** — `/commit`, `/review`, `/deploy`, `/pr`, ...
- **1.141 awesome-claude-skills** references
- **230+ templates** for hooks, MCPs, and settings

Restart Claude Code, type `/` in chat, see them all light up.

---

## ⚙️ Configuration

### `team/.env`
```env
# === RECOMMENDED: 1 key = 7 models ===
OPENROUTER_API_KEY=sk-or-v1-...

# === FREE TIER FRIENDLY ===
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
CEREBRAS_API_KEY=csk-...

# === CHEAP / HIGH QUALITY ===
DEEPSEEK_API_KEY=sk-...
MISTRAL_API_KEY=...

# === PREMIUM ===
OPENAI_API_KEY=sk-proj-...
XAI_API_KEY=xai-...

# Leader model override (default: claude-opus-4-7)
LEAD_MODEL=claude-opus-4-7
```

### `~/.claude/CLAUDE.md` (auto-trigger rules)
After `install.bat`, see `claude-config/CLAUDE.md.example` for ready-made auto-trigger rules. Copy what you want into your own `~/.claude/CLAUDE.md`.

---

## ❓ FAQ

<details>
<summary><b>Do I need an Anthropic API key?</b></summary>

**No** — if you have a Claude Max subscription, the `claude-agent-sdk` uses your CLI auth. If you don't have a subscription, set `ANTHROPIC_API_KEY` in `.env` and the system falls back to API.
</details>

<details>
<summary><b>What if I only set 2-3 keys?</b></summary>

The system gracefully skips missing providers. Even with **zero external keys**, you still get a 3-Claude team (Opus + Sonnet + Haiku) via subscription.
</details>

<details>
<summary><b>How does it stay parallel?</b></summary>

`asyncio.gather()` fires all workers concurrently. HTTP-based providers (LiteLLM) connect to different domains; the Anthropic layer uses subprocess. Network round-trips overlap.
</details>

<details>
<summary><b>Can I add my own provider?</b></summary>

Yes — 5-minute job. Add a tuple to the `DIRECTS` list in `team/team.py`:
```python
("YOUR_API_KEY", "litellm-model-id", "agent-name", "Role description"),
```
Set `YOUR_API_KEY` in `.env`. Done — auto-active on next run.
</details>

<details>
<summary><b>How do I prove it's working?</b></summary>

Run `python team/verify.py`. It pings every active provider with a real HTTP request and reports endpoint, latency, and token counts. If you see "OK" with token counts > 0, the LLM actually executed.
</details>

<details>
<summary><b>Cost concerns?</b></summary>

You control which providers are active via `.env`. Use `mode="light"` for cheap iterations (3 Claude only). Most providers have free tiers — Groq, Gemini, NVIDIA NIM, Hugging Face. Cerebras and OpenRouter offer trial credits.
</details>

---

## 🛠️ Tech Stack

- **Python 3.10+** — async/await, dataclasses
- **[claude-agent-sdk](https://github.com/anthropics/claude-agent-sdk-python)** — Anthropic Claude (subscription or API key)
- **[LiteLLM](https://github.com/BerriAI/litellm)** — unified API for 100+ providers
- **python-dotenv** — env var loading

---

## 🤝 Contributing

PRs welcome! Areas of interest:
- New provider integrations
- Improved synthesis logic
- More slash commands and subagents
- IDE adapters (Cursor `.mdc`, Windsurf `.windsurfrules`, etc.)

Open an issue first for major changes.

---

## 📜 License

[MIT](LICENSE) — use commercially, fork, modify, redistribute. Just keep the copyright notice.

---

## 🙏 Credits

- **[Anthropic](https://anthropic.com)** — Claude Opus / Sonnet / Haiku, claude-agent-sdk
- **[BerriAI](https://github.com/BerriAI)** — LiteLLM (the abstraction that makes 18 providers possible)
- **All providers** above for their APIs and free tiers

---

<div align="center">

**Built with 🧠 by humans + 🤖 by AIs working in parallel.**

⭐ Star this repo if it helped you ship faster.

[Report issue](https://github.com/Sansar35/claude-agent/issues) · [Discussions](https://github.com/Sansar35/claude-agent/discussions)

</div>
