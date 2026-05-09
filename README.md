<div align="center">

# 🤖 Claude Agent Config

### Comprehensive Claude Code configuration bundle

**11.000+ community skills · 591 specialized subagents · 417 slash commands · 14-provider multi-AI orchestrator**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Multi-IDE](https://img.shields.io/badge/IDE-Claude_Code_·_Cursor_·_Antigravity_·_VS_Code-purple.svg)](INSTALL-OTHER-IDES.md)
[![Skills](https://img.shields.io/badge/Community_Skills-11k+-blueviolet.svg)](#-community-content)
[![Multi-AI](https://img.shields.io/badge/Multi--AI-63_models_·_14_providers-ff69b4.svg)](#-multi-ai-orchestration)
[![Modes](https://img.shields.io/badge/Modes-SOLO_·_LIGHT_·_HEAVY-orange.svg)](#-multi-ai-orchestration)

---

**One-shot Claude Code config installer.** Copies a curated bundle of skills, subagents, slash commands, hooks, MCP templates, and settings templates into your `~/.claude/` directory so Claude Code starts fully equipped.

</div>

---

## 🎬 What You Get

After running the installer your `~/.claude/` directory contains:

- **8.619 community skills** — domain expertise, frameworks, workflows
- **591 specialized subagents** — `code-reviewer`, `security-auditor`, `debugger`, `test-automator`, ...
- **417 slash commands** — `/commit`, `/review`, `/deploy`, `/pr`, ...
- **1.141 awesome-claude-skills** references
- **230+ templates** for hooks, MCP servers, and settings
- **CLAUDE.md.example** — starter rules template
- **settings.example.json** — starter settings template

---

## 🧠 Multi-AI Orchestration

Claude Agent ships with a **line-threshold orchestrator**: every task is routed to the smallest team that can deliver it, scaling from 1 AI for trivial edits up to 63 AI for whole-system rewrites.

<table align="center">
<tr>
  <th align="center">Mode</th>
  <th align="center">Trigger</th>
  <th align="center">AI Count</th>
  <th align="center">Composition</th>
</tr>
<tr>
  <td align="center">🟢 <b>SOLO</b></td>
  <td align="center">≤ 2 000 lines</td>
  <td align="center"><code>1</code></td>
  <td>Claude Opus (lead only)</td>
</tr>
<tr>
  <td align="center">🟡 <b>LIGHT</b></td>
  <td align="center">2 001 – 5 000 lines</td>
  <td align="center"><code>3</code></td>
  <td>Opus + Sonnet + Haiku<br><sub>Anthropic-only, subscription-friendly</sub></td>
</tr>
<tr>
  <td align="center">🔴 <b>HEAVY</b></td>
  <td align="center">&gt; 5 000 lines</td>
  <td align="center"><code>63</code></td>
  <td>Opus lead + 62 parallel workers across 14 providers</td>
</tr>
</table>

> **Auto-routing.** The orchestrator estimates the diff size before writing code and picks the cheapest mode that still ships zero-bug output.

<details>
<summary><b>📊 HEAVY mode — full provider line-up (63 AI)</b></summary>

<br>

<table>
<tr>
  <td>

**Anthropic (3)**
- ★ Claude Opus 4.7 *(lead)*
- Claude Sonnet 4.6
- Claude Haiku 4.5

**OpenAI (8)**
- GPT-5 · GPT-5 Mini
- GPT-4o · GPT-4o Mini
- o1 · o1 Mini
- o3 · o3 Mini

**Google Gemini (5)**
- Gemini 2.5 Pro · 2.5 Flash
- Gemini 2.0 Flash
- Gemini 1.5 Pro · 1.5 Flash

**DeepSeek (2)**
- DeepSeek V3 Chat
- DeepSeek R1

**Mistral (6)**
- Large · Medium · Small
- Codestral · Ministral · Pixtral

**Groq (8)**
- Llama 3.3 · 3.1 · Vision
- Qwen · R1 Distill
- Gemma 2 · Saba · Llama 3 70B

  </td>
  <td>

**Cerebras (4)**
- Qwen 235B
- Llama 3.3 · Llama 4 · Llama 3.1

**Together (6)**
- Llama 3.3 · 405B
- Qwen · Mixtral
- DeepSeek V3 · QwQ

**Fireworks (5)**
- Llama 3.3 · 405B
- Qwen · DeepSeek V3 · Mixtral

**xAI (3)**
- Grok 3 · Grok 3 Mini
- Grok 2 Vision

**Cohere (4)**
- Command A · R+ · R · R7B

**Hyperbolic (5)**
- Llama 405B · 70B · 3.3
- Qwen · DeepSeek V3

**SambaNova (4)**
- Llama 3.3 · 405B
- Qwen · DeepSeek V3

  </td>
</tr>
</table>

</details>

<details>
<summary><b>💤 Optional providers (drop in extra credentials to unlock +200 models)</b></summary>

<br>

| Provider | Adds |
|---|---|
| **OpenRouter** | 200+ aggregated models |
| **Google AI Studio** | extra Gemini variants |
| **Perplexity** | Sonar, Sonar Pro, Sonar Reasoning |
| **DeepInfra** | Llama 3 · Mixtral · Qwen tier |
| **NVIDIA NIM** | Llama-Nemotron, retrieval-tuned models |
| **Hugging Face Inference** | open-weights router |

</details>

<details>
<summary><b>⚙️ How auto-routing decides</b></summary>

<br>

```text
incoming task
   │
   ├─ knowledge / one-line / typo / pure read   → SOLO
   ├─ existing-file surgical fix (≤ 2k lines)   → SOLO
   ├─ multi-file refactor (2k – 5k lines)       → LIGHT
   └─ greenfield / cross-cutting (> 5k lines)   → HEAVY
```

The router prefers **the smallest viable mode** to keep latency low and runs cost predictable.

</details>

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

1. ✅ Copies `claude-config/` → `~/.claude/` (skills, agents, slash commands, hooks, templates)
2. ✅ Drops example templates (`CLAUDE.md.example`, `settings.example.json`) for you to customise
3. ✅ Provides `install.bat` / `install.sh` to re-run anytime

Then start Claude Code, type `/` in chat, watch the new commands light up.

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
├── 🪟 install.bat                ← Windows auto-installer
├── 🐧 install.sh                 ← macOS / Linux auto-installer
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

**Total: 11.016 files**

---

## 🌍 IDE Compatibility

| IDE / Tool | Native | Slash commands | Subagents |
|---|:-:|:-:|:-:|
| **Claude Code** (Anthropic CLI) | ✅ | ✅ | ✅ |
| **Antigravity** (Google AI IDE) | ✅ | ✅ | ✅ |
| **VS Code** + Claude extension | ✅ | ✅ | ✅ |
| **Cursor** | ⚠️ rules | ❌ | ⚠️ |
| **Windsurf** (Codeium) | ⚠️ rules | ❌ | ⚠️ |
| **Cline** / **Aider** / **Continue** | ❌ | ❌ | ❌ |

> Detailed IDE-specific guidance: [INSTALL-OTHER-IDES.md](INSTALL-OTHER-IDES.md).

---

## 📦 Community Content (auto-installed via `install.bat`)

After running the installer, your `~/.claude/` directory will contain:

- **8.619 skills** — from `claude-api` to `frontend-design` to `deep-research`
- **591 subagents** — `code-reviewer`, `security-auditor`, `debugger`, `test-automator`, ...
- **417 slash commands** — `/commit`, `/review`, `/deploy`, `/pr`, ...
- **1.141 awesome-claude-skills** references
- **230+ templates** for hooks, MCPs, and settings

Restart Claude Code, type `/` in chat, see them all light up.

---

## ⚙️ Configuration

### `~/.claude/CLAUDE.md` (auto-trigger rules)

After running the installer, see `claude-config/CLAUDE.md.example` for ready-made auto-trigger rules. Copy what you want into your own `~/.claude/CLAUDE.md`.

### `~/.claude/settings.json`

See `claude-config/settings.example.json` for a tested baseline. Customise hooks, permission policy, and MCP configuration to taste.

---

## 🤝 Contributing

PRs welcome! Areas of interest:

- New skill / subagent / slash command contributions
- IDE adapters (Cursor `.mdc`, Windsurf `.windsurfrules`, etc.)
- Hook templates and MCP integrations

Open an issue first for major changes.

---

## 📜 License

[MIT](LICENSE) — use commercially, fork, modify, redistribute. Just keep the copyright notice.

---

<div align="center">

**Built for Claude Code users who want a powerful starting point.**

⭐ Star this repo if it helped you ship faster.

[Report issue](https://github.com/Sansar35/claude-agent/issues) · [Discussions](https://github.com/Sansar35/claude-agent/discussions)

</div>
