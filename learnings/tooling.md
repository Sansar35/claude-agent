# Tooling & Environment

## Workspace
- OS: Windows 11 Pro
- Editor: VS Code (27 extensions, 13 MCP servers, 10 Claude plugins)
- GitHub: Sansar35
- Ana üs: `C:\Users\emre` — TÜM dinamik dosyalar buradan yönetilir.
- Claude Code config: `C:\Users\emre\.claude` (RTK global hook + tüm araçlar dinamik)

## UI Component Reference (her görsel iş için)
**Görsel/copy-paste:**
- aura.build
- magicui.design
- ui.aceternity.com
- uiverse.io
- hyperui.dev
- cult-ui.com
- tailwindui.com

**MCP ile VS Code'a bağlanabilir:**
- 21st.dev Magic — github.com/21st-dev/magic-mcp
- shadcn/ui — ui.shadcn.com/docs/mcp
- shadcn.io Pro — shadcn.io/mcp
- v0.dev — vercel.com/docs/mcp
- Vercel MCP — mcp.vercel.com
- Figma MCP

## Scrollbar Standardı (RULE 28)
Tüm scrollbar'lar bar.png stili: 4px, rgba(0,255,136,0.45), border-radius:99px, transparent track, hover 6px/0.65, active 0.8.

## Anti-Flash CSS (RULE 29)
HEAD'de: `html:not(.app-ready) *{transition:none!important;animation:none!important}`
Load sonrası `.app-ready` eklenir.