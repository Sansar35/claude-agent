#!/usr/bin/env bash
# ============================================================
#  Claude Agent — macOS / Linux Kurulum
#  claude-config/ icerigini ~/.claude/ altina kopyalar
# ============================================================

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC="$SCRIPT_DIR/claude-config"
DST="$HOME/.claude"

echo
echo "============================================================"
echo "  CLAUDE AGENT KURULUM"
echo "============================================================"
echo
echo "  Kaynak : $SRC"
echo "  Hedef  : $DST"
echo

# Hedef klasor olustur
if [ ! -d "$DST" ]; then
    echo "  [INFO] $DST yok, olusturuluyor..."
    mkdir -p "$DST"
fi

# Kopyalama
for D in skills agents commands awesome-claude-skills hooks-templates mcps-templates settings-templates hooks; do
    if [ -d "$SRC/$D" ]; then
        echo "  [COPY] $D ..."
        mkdir -p "$DST/$D"
        cp -R "$SRC/$D/." "$DST/$D/"
        echo "  [OK]   $D"
    fi
done

# Ornek dosyalar
if [ -f "$SRC/CLAUDE.md.example" ]; then
    cp "$SRC/CLAUDE.md.example" "$DST/CLAUDE.md.example"
    echo "  [OK]   CLAUDE.md.example"
fi
if [ -f "$SRC/settings.example.json" ]; then
    cp "$SRC/settings.example.json" "$DST/settings.example.json"
    echo "  [OK]   settings.example.json"
fi

echo
echo "============================================================"
echo "  KURULUM TAMAMLANDI"
echo "============================================================"
echo
echo "  Dosyalar $DST altina yerlestirildi."
echo
echo "  Sonraki adimlar:"
echo "  1) cd team && pip install -r requirements.txt"
echo "  2) cp .env.example .env && nano .env  (key'leri yaz)"
echo "  3) python team.py 'Test projesi yaz'"
echo
echo "  Detay: README.md"
echo
