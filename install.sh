#!/usr/bin/env bash
# Instalador do framework global de arquitetura para Claude Code.
# Copia  agents/*.md  -> ~/.claude/agents/
#        skills/*     -> ~/.claude/skills/
# Idempotente: itens idênticos são ignorados; itens diferentes são salvos em
# ~/.claude/arch-framework-backup-<timestamp>/ antes de serem substituídos.
#
# Uso:
#   ./install.sh             instala
#   ./install.sh --dry-run   mostra o que seria feito, sem alterar nada
#   ./install.sh --help
#
# Variável opcional: CLAUDE_HOME (padrão: ~/.claude)

set -euo pipefail

DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run|-n) DRY_RUN=1 ;;
    --help|-h)
      sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Argumento desconhecido: $arg (use --dry-run ou --help)" >&2
      exit 2
      ;;
  esac
done

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
AGENTS_SRC="$SRC_DIR/agents"
SKILLS_SRC="$SRC_DIR/skills"
AGENTS_DST="$CLAUDE_HOME/agents"
SKILLS_DST="$CLAUDE_HOME/skills"
TS="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$CLAUDE_HOME/arch-framework-backup-$TS"

INSTALLED=()
UPDATED=()
UNCHANGED=()
BACKED_UP=()

log() { printf '%s\n' "$*"; }
run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    log "  [dry-run] $*"
  else
    "$@"
  fi
}

if [ ! -d "$AGENTS_SRC" ] && [ ! -d "$SKILLS_SRC" ]; then
  echo "Nada para instalar: não encontrei $AGENTS_SRC nem $SKILLS_SRC" >&2
  exit 1
fi

[ "$DRY_RUN" -eq 1 ] && log "== MODO DRY-RUN: nenhuma alteração será feita ==" || log "== Instalando em $CLAUDE_HOME =="
log "Origem: $SRC_DIR"
log "Backup (se necessário): $BACKUP_DIR"
log ""

# backup_item <caminho-existente> <categoria>  (agents|skills)
backup_item() {
  local path="$1" cat="$2"
  local dest="$BACKUP_DIR/$cat"
  run mkdir -p "$dest"
  run cp -a "$path" "$dest/"
  BACKED_UP+=("$cat/$(basename "$path")")
}

# install_file <origem> <destino>  — arquivo único (agentes)
install_file() {
  local src="$1" dst="$2" name
  name="$(basename "$dst")"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if [ -f "$dst" ] && cmp -s "$src" "$dst"; then
      UNCHANGED+=("agents/$name")
      return 0
    fi
    backup_item "$dst" agents
    run cp -f "$src" "$dst"
    UPDATED+=("agents/$name")
  else
    run cp "$src" "$dst"
    INSTALLED+=("agents/$name")
  fi
}

# install_dir <origem> <destino>  — pasta (skills)
install_dir() {
  local src="$1" dst="$2" name
  name="$(basename "$dst")"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if [ -d "$dst" ] && diff -rq "$src" "$dst" >/dev/null 2>&1; then
      UNCHANGED+=("skills/$name")
      return 0
    fi
    backup_item "$dst" skills
    run rm -rf "$dst"
    run cp -a "$src" "$dst"
    UPDATED+=("skills/$name")
  else
    run cp -a "$src" "$dst"
    INSTALLED+=("skills/$name")
  fi
}

# --- agentes ---
if [ -d "$AGENTS_SRC" ]; then
  run mkdir -p "$AGENTS_DST"
  shopt -s nullglob
  for f in "$AGENTS_SRC"/*.md; do
    install_file "$f" "$AGENTS_DST/$(basename "$f")"
  done
  shopt -u nullglob
else
  log "Aviso: pasta de agentes não encontrada em $AGENTS_SRC (ignorada)"
fi

# --- skills ---
if [ -d "$SKILLS_SRC" ]; then
  run mkdir -p "$SKILLS_DST"
  for d in "$SKILLS_SRC"/*/; do
    [ -d "$d" ] || continue
    install_dir "${d%/}" "$SKILLS_DST/$(basename "$d")"
  done
else
  log "Aviso: pasta de skills não encontrada em $SKILLS_SRC (ignorada)"
fi

# --- resumo ---
print_list() {
  local title="$1"; shift
  local n=$#
  log "$title ($n)"
  local item
  for item in "$@"; do log "  - $item"; done
}

log ""
if [ "$DRY_RUN" -eq 1 ]; then
  log "== Resumo (DRY-RUN — nada foi alterado) =="
else
  log "== Resumo =="
fi
print_list "Novos" ${INSTALLED[@]+"${INSTALLED[@]}"}
print_list "Atualizados (versão anterior salva em backup)" ${UPDATED[@]+"${UPDATED[@]}"}
print_list "Já idênticos (ignorados)" ${UNCHANGED[@]+"${UNCHANGED[@]}"}
if [ "${#BACKED_UP[@]}" -gt 0 ]; then
  log "Backup em: $BACKUP_DIR"
fi
log ""
if [ "$DRY_RUN" -eq 1 ]; then
  log "Para instalar de fato, rode novamente sem --dry-run."
else
  log "Instalação concluída. Reinicie a sessão do Claude Code para carregar agentes e skills."
  log "Para desfazer: restaure os itens do backup acima e remova os 'Novos' listados."
fi
