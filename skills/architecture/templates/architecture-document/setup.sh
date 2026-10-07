#!/usr/bin/env bash
# Prepara o ambiente LOCAL (sem instalar nada global) para gerar o PDF do documento de arquitetura.
#   venv Python  : weasyprint + markdown          -> $ARCH_PDF_HOME/venv
#   Node (local) : mermaid + playwright-core      -> $ARCH_PDF_HOME/node
#   Navegador    : reaproveita um Chromium já baixado (Playwright em ~/.cache/ms-playwright,
#                  google-chrome ou chromium do sistema). Não baixa nada sozinho:
#                  se não houver, imprime o comando e sai com código 3.
# Uso: bash setup.sh [--check]        (--check só verifica, não instala)
# Variáveis: ARCH_PDF_HOME (padrão ~/.cache/architecture-pdf), CHROMIUM_PATH (opcional)
set -euo pipefail
HOME_DIR="${ARCH_PDF_HOME:-$HOME/.cache/architecture-pdf}"
CHECK=0; [ "${1:-}" = "--check" ] && CHECK=1
# nvm não é carregado em shells não interativos: procurar o node mais novo
if ! command -v node >/dev/null 2>&1; then
  for n in "$HOME"/.nvm/versions/node/*/bin; do [ -d "$n" ] && PATH="$n:$PATH"; done
fi

find_chrome() {
  [ -n "${CHROMIUM_PATH:-}" ] && [ -x "$CHROMIUM_PATH" ] && { echo "$CHROMIUM_PATH"; return; }
  local c
  for c in "$HOME"/.cache/ms-playwright/chromium-*/chrome-linux*/chrome \
           "$HOME"/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux*/chrome-headless-shell; do
    [ -x "$c" ] && { echo "$c"; return; }
  done
  for c in google-chrome google-chrome-stable chromium chromium-browser; do
    command -v "$c" >/dev/null 2>&1 && { command -v "$c"; return; }
  done
}

status=0
PY="$HOME_DIR/venv/bin/python"
if [ -x "$PY" ] && "$PY" -c "import weasyprint, markdown" 2>/dev/null; then
  echo "[ok] python: weasyprint + markdown ($PY)"
elif [ "$CHECK" -eq 1 ]; then echo "[falta] venv Python em $HOME_DIR/venv"; status=1
else
  echo "[instalando] venv Python em $HOME_DIR/venv"
  python3 -m venv "$HOME_DIR/venv"
  "$HOME_DIR/venv/bin/pip" install --quiet weasyprint markdown
  echo "[ok] python"
fi

if [ -d "$HOME_DIR/node/node_modules/mermaid" ] && [ -d "$HOME_DIR/node/node_modules/playwright-core" ]; then
  echo "[ok] node: mermaid + playwright-core ($HOME_DIR/node)"
elif [ "$CHECK" -eq 1 ]; then echo "[falta] mermaid/playwright-core em $HOME_DIR/node"; status=1
else
  command -v npm >/dev/null 2>&1 || { echo "npm não encontrado (necessário só para diagramas Mermaid)"; exit 2; }
  echo "[instalando] mermaid + playwright-core em $HOME_DIR/node"
  mkdir -p "$HOME_DIR/node"
  (cd "$HOME_DIR/node" && { [ -f package.json ] || npm init -y >/dev/null; } && npm install --silent mermaid playwright-core)
  echo "[ok] node"
fi

CH="$(find_chrome || true)"
if [ -n "$CH" ]; then echo "[ok] navegador: $CH"
else
  echo "[falta] nenhum Chromium encontrado. Opções: defina CHROMIUM_PATH, instale google-chrome/chromium,"
  echo "        ou (com autorização do usuário) rode: npx playwright-core install chromium"
  status=3
fi
echo "Pronto. Gerar: $PY $(dirname "$(readlink -f "$0")")/render_pdf.py <documento.md> <saida.pdf>"
exit $status
