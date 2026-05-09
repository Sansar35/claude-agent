<div align="center">

# 🤖 Claude Agent Config

### Comprehensive Claude Code configuration bundle

**11.000+ community skills · 591 specialized subagents · 417 slash commands · Single command install**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Multi-IDE](https://img.shields.io/badge/IDE-Claude_Code_·_Cursor_·_Antigravity_·_VS_Code-purple.svg)](INSTALL-OTHER-IDES.md)
[![Skills](https://img.shields.io/badge/Community_Skills-11k+-blueviolet.svg)](#-community-content)

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
