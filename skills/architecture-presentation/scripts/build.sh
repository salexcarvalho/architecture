#!/usr/bin/env bash
# Gera radares, deck.html, PDF (Chrome headless), PNG por slide e PPTX a partir de WORKDIR.
# Uso: build.sh WORKDIR
#   WORKDIR contém conteudo-deck.json e radar-data.json (docs/apresentacoes/<cliente-vN>/).
# Env: ARCH_DECK_VENV (venv com python-pptx e matplotlib; criado se não existir; nunca instala global),
#      CHROME (padrão google-chrome). Saída: <arquivo_base>.pdf e .pptx em WORKDIR (meta.arquivo_base).
set -euo pipefail
SK="$(cd "$(dirname "$0")" && pwd)"
WD="$(cd "${1:?uso: build.sh WORKDIR}" && pwd)"
cd "$WD"
[ -f conteudo-deck.json ] || { echo "faltou $WD/conteudo-deck.json" >&2; exit 2; }

VENV="${ARCH_DECK_VENV:-$WD/.venv}"
if [ ! -x "$VENV/bin/python" ] || ! "$VENV/bin/python" -c "import pptx, matplotlib" 2>/dev/null; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q python-pptx matplotlib
fi
PY="$VENV/bin/python"
BASE="$("$PY" -c "import json;print(json.load(open('conteudo-deck.json',encoding='utf-8'))['meta'].get('arquivo_base','apresentacao-arquitetura'))")"
PREFIX="$("$PY" -c "import json;print(json.load(open('conteudo-deck.json',encoding='utf-8'))['meta'].get('radar_prefix','radar'))")"
PDF="$WD/$BASE.pdf"; PPTX="$WD/$BASE.pptx"

# 1) radares (só as camadas usadas nos slides "radar")
rm -rf assets/radares && mkdir -p assets/radares
if [ -f radar-data.json ]; then
  "$PY" "$SK/radar_charts.py" radar-data.json assets/radares --deck conteudo-deck.json --prefix "$PREFIX" >/dev/null
fi

# 2) HTML
python3 "$SK/build_deck.py" "$WD"

# 3) PDF + checagem de transbordo (data-overflow gravado pelo script do deck)
CHROME="${CHROME:-google-chrome}"
"$CHROME" --headless=new --no-sandbox --disable-gpu --hide-scrollbars \
  --print-to-pdf="$PDF" --no-pdf-header-footer --virtual-time-budget=15000 \
  "file://$WD/deck.html" >/dev/null 2>&1
OV="$("$CHROME" --headless=new --no-sandbox --disable-gpu --virtual-time-budget=15000 --dump-dom "file://$WD/deck.html" 2>/dev/null | grep -o 'data-overflow="[^"]*"' | head -1 || true)"
if [ -n "$OV" ] && [ "$OV" != 'data-overflow=""' ]; then
  echo "ATENCAO transbordo/texto cortado: $OV" | sed 's/|/\n   /g' >&2
  echo "$OV" > "$WD/.overflow.txt"
else
  rm -f "$WD/.overflow.txt"
fi

# 4) PNG por slide e PPTX
rm -rf assets/slides && mkdir -p assets/slides
pdftoppm -r 96 -png "$PDF" assets/slides/slide
"$PY" "$SK/build_pptx.py" "$WD" "$PPTX"
echo "ok: $PDF"
