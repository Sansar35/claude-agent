# 📦 Kurulum Rehberi

## 1. Sistem Gereksinimleri

- **Claude Code CLI** (Anthropic resmi)
- **Git** (klonlama için)
- Windows / macOS / Linux — hepsi destekli

## 2. Adım Adım

### 2.1 Repo'yu klonla

```bash
git clone https://github.com/Sansar35/claude-agent.git
cd claude-agent
```

### 2.2 Otomatik kurulum

**Windows:**

```cmd
install.bat
```

**macOS / Linux:**

```bash
chmod +x install.sh
./install.sh
```

Kurulum scripti `claude-config/` klasörünün içeriğini `~/.claude/` (Windows: `%USERPROFILE%\.claude\`) altına kopyalar:

- `skills/` → 8.619 community skill
- `agents/` → 591 specialized subagent
- `commands/` → 417 slash command
- `awesome-claude-skills/` → 1.141 awesome reference
- `hooks/` → 21 hook
- `hooks-templates/` → 57 hook template
- `mcps-templates/` → 85 MCP template
- `settings-templates/` → 67 settings template
- `CLAUDE.md.example` → starter rules
- `settings.example.json` → starter settings

### 2.3 Claude Code CLI kurulumu (eğer yoksa)

Anthropic resmi:

- https://docs.claude.com/en/docs/claude-code/quickstart
- Veya: `npm install -g @anthropic-ai/claude-code`
- Sonra: `claude login`

### 2.4 İlk yapılandırma

`~/.claude/CLAUDE.md.example` dosyasını incele ve istediğin kuralları kendi `~/.claude/CLAUDE.md` dosyana kopyala.

`~/.claude/settings.example.json` dosyasındaki tested baseline'ı `~/.claude/settings.json` olarak adapte et.

### 2.5 Test

Claude Code'u başlat ve `/` yazınca yeni slash command'lar görmeli, agent'lar listelenmeli.

```bash
claude
```

## 3. IDE-spesifik kurulum

Claude Code dışındaki IDE'ler için: [INSTALL-OTHER-IDES.md](INSTALL-OTHER-IDES.md)

## 4. Sorun Giderme

| Hata | Çözüm |
|---|---|
| `~/.claude/` klasörü görünmüyor | İlk Claude Code başlatıldığında otomatik oluşur — `claude` komutunu bir kere çalıştır |
| Slash command'lar görünmüyor | Claude Code'u yeniden başlat, `/` yaz |
| Skill listede yok | `~/.claude/skills/` altına dosyaların kopyalandığından emin ol |
| Windows'ta Türkçe karakter bozuk | CMD'de `chcp 65001` çalıştır |

## 5. Geri yükleme / yeniden çalıştırma

İstediğin zaman tekrar `install.bat` veya `install.sh` çalıştırabilirsin — mevcut dosyaların üzerine yazar (idempotent).
