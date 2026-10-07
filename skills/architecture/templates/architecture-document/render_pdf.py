#!/usr/bin/env python3
"""Markdown -> PDF do Documento de Arquitetura de Software (formato ISO/IEC/IEEE 42010).

Uso:
  render_pdf.py <documento.md> <saida.pdf> [--css print.css] [--keep-work DIR]
                [--no-mermaid] [--lint-only] [--strict] [--deny REGEX ...]

Motor: WeasyPrint (HTML/CSS -> PDF, A4, sumario com pontilhado e numero de pagina,
cabecalho/rodape) + python-markdown. Diagramas: blocos ```mermaid sao renderizados
para PNG por render_mermaid.mjs (Chromium local) antes do PDF.
Dependencias locais (nada global): bash setup.sh

Sintaxe do .md alem do Markdown comum:
  - front-matter simples (--- chave: valor ---): titulo, subtitulo, classificacao, autor, data
  - '# Titulo' (H1) a '#### Titulo' (H4) sao numerados automaticamente (1, 1.1, 1.1.1, 1.1.1.1);
    '##### Titulo' (H5) nao e numerado e aparece no sumario; '{.nonum}' no fim do titulo
    suprime o numero em qualquer nivel.
  - ```kv  ... ```  linhas 'Rotulo: valor' -> tabela sem bordas (identificacao do sistema)
  - ```mermaid ... ``` -> figura numerada; legenda = linha '%% titulo: <texto>' dentro do bloco
  - comentarios HTML <!-- ... --> sao removidos (guias do template)
Saida: o PDF; codigo 1 se o lint encontrar problema bloqueante (placeholders, segredos,
termos proibidos) e --strict, ou se um diagrama falhar.
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import markdown
    from weasyprint import HTML
except ImportError:  # pragma: no cover
    sys.exit("Faltam weasyprint/markdown. Rode: bash setup.sh e use o python do venv "
             "($ARCH_PDF_HOME/venv/bin/python, padrao ~/.cache/architecture-pdf).")

HERE = Path(__file__).resolve().parent

# Termos que nao devem aparecer no documento final (regra do framework: sem termos de IA,
# sem segredos, sem IDs internos de memoria, sem caminhos locais).
DEFAULT_DENY = [
    (r"\b(IA|AI|LLM|GPT|Claude|Anthropic|Copilot|ChatGPT|machine learning|intelig[eê]ncia artificial)\b", "termo de IA"),
    (r"\b(F|A|Q|R|P|RV|TD|G)-(novo-\d+|\d{3})\b", "ID interno de memoria (F-/A-/Q-/R-/P-)"),
    (r"\[(KNOWN|ASSUMPTION|PROPOSAL|DECISION|OPEN|RISK)\b", "marcador interno [KNOWN/...]"),
    (r"(/home/|/tmp/|C:\\Users)", "caminho local"),
    (r"(?i)\b(password|senha|secret|token|api[_-]?key)\s*[:=]\s*\S{6,}", "possivel segredo (valor)"),
    (r"\bAKIA[0-9A-Z]{16}\b|-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{20,}\.", "possivel segredo (chave/JWT)"),
    (r"\{\{[^}]*\}\}|\bTODO\b|\bTBD\b|\bXXX\b|<<[^>]*>>", "placeholder nao preenchido"),
]


# ----------------------------------------------------------------------------- parsing
def parse_front_matter(text):
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip('"')
        text = text[m.end():]
    return meta, text


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def extract_blocks(text, workdir, no_mermaid):
    """Troca ```kv e ```mermaid por marcadores; devolve (texto, kv_blocks, mermaid_blocks)."""
    kvs, mmds = [], []

    def kv(m):
        kvs.append(m.group(1))
        return f"\n\nKVBLOCK{len(kvs) - 1}END\n\n"

    def mm(m):
        code = m.group(1).strip("\n")
        title = ""
        t = re.search(r"^\s*%%\s*titulo:\s*(.+)$", code, re.M)
        if t:
            title = t.group(1).strip()
            code = code.replace(t.group(0), "")
        mmds.append((code.strip() + "\n", title))
        return f"\n\nMMDBLOCK{len(mmds) - 1}END\n\n"

    text = re.sub(r"```kv[ \t]*\n(.*?)\n```", kv, text, flags=re.S)
    text = re.sub(r"```mermaid[ \t]*\n(.*?)\n```", mm, text, flags=re.S)
    return text, kvs, mmds


def render_mermaid(mmds, workdir, scale):
    d = Path(workdir) / "mermaid"
    d.mkdir(parents=True, exist_ok=True)
    for i, (code, _) in enumerate(mmds):
        (d / f"fig{i:02d}.mmd").write_text(code, encoding="utf-8")
    node = shutil.which("node")
    if not node:
        for p in sorted(Path.home().glob(".nvm/versions/node/*/bin/node"), reverse=True):
            node = str(p)
            break
    if not node:
        sys.exit("node nao encontrado (necessario para Mermaid). Use --no-mermaid ou instale o node.")
    r = subprocess.run([node, str(HERE / "render_mermaid.mjs"), str(d), "1600", str(scale)],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit("Falha ao renderizar diagramas Mermaid (ver erros acima). Corrija o bloco indicado.")
    return d


# ----------------------------------------------------------------------------- html
def slug(s, n):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()[:40]
    return f"s{n}-{s}"


def number_headings(body):
    """Numera H1-H4 (1 / 1.1 / 1.1.1 / 1.1.1.1), adiciona ids e devolve (html, toc_entries)."""
    counters = [0, 0, 0, 0]
    toc, n = [], 0

    def repl(m):
        nonlocal n
        lvl, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
        nonum = False
        if "{.nonum}" in inner:
            inner, nonum = inner.replace("{.nonum}", "").strip(), True
        label = inner
        if lvl <= 4 and not nonum:
            counters[lvl - 1] += 1
            for j in range(lvl, 4):
                counters[j] = 0
            num = ".".join(str(c) for c in counters[:lvl])
            label = f"{num}{'.' if lvl == 1 else ''} {inner}"
        n += 1
        hid = slug(label, n)
        toc.append((lvl, label, hid))
        cls = ' class="nonum"' if nonum else ""
        return f'<h{lvl} id="{hid}"{cls}>{label}</h{lvl}>'

    body = re.sub(r"<h([1-5])([^>]*)>(.*?)</h\1>", repl, body, flags=re.S)
    return body, toc


def build_toc(toc, title):
    rows = [f'<li class="toc1"><a href="#cover">{html.escape(title)}</a></li>']
    for lvl, label, hid in toc:
        rows.append(f'<li class="toc{lvl}"><a href="#{hid}">{label}</a></li>')
    return '<nav id="toc"><ul>' + "".join(rows) + "</ul></nav>"


def build_html(meta, md_text, workdir, css_path, no_mermaid, scale):  # scale: densidade dos PNG de diagrama
    title = meta.get("titulo", "Documento de Arquitetura de Software")
    subtitle = meta.get("subtitulo", "(Conforme ISO/IEC/IEEE 42010)")
    classif = meta.get("classificacao", "Restrito")

    text, kvs, mmds = extract_blocks(md_text, workdir, no_mermaid)
    if mmds and not no_mermaid:
        mdir = render_mermaid(mmds, workdir, scale)
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"], output_format="html")

    for i, raw in enumerate(kvs):
        rows = []
        for line in raw.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                rows.append(f"<tr><th>{html.escape(k.strip())}</th><td>{html.escape(v.strip())}</td></tr>")
        body = body.replace(f"<p>KVBLOCK{i}END</p>", f'<table class="kv">{"".join(rows)}</table>')

    fig_n = 0
    for i, (code, cap) in enumerate(mmds):
        fig_n += 1
        capt = f"<figcaption>Figura {fig_n} — {html.escape(cap)}</figcaption>" if cap else f"<figcaption>Figura {fig_n}</figcaption>"
        if no_mermaid:
            inner = f'<pre class="mmd">{html.escape(code)}</pre>'
        else:
            inner = f'<img src="{(Path(workdir) / "mermaid" / f"fig{i:02d}.png").as_uri()}" alt="{html.escape(cap)}"/>'
        body = body.replace(f"<p>MMDBLOCK{i}END</p>", f"<figure>{capt}{inner}</figure>")

    body, toc = number_headings(body)
    css = Path(css_path).read_text(encoding="utf-8")
    css = css.replace("__IMGDPI__", str(int(96 * scale))).replace("__CLASSIFICACAO__", html.escape(classif).replace('"', ""))
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"/>
<title>{html.escape(title)}</title>
<meta name="author" content="{html.escape(meta.get('autor', ''))}"/>
<meta name="description" content="{html.escape(subtitle)}"/>
<style>{css}</style></head><body>
<section id="cover" class="cover"><h1 class="doc-title">{html.escape(title)}</h1><p class="doc-subtitle"><em>{html.escape(subtitle)}</em></p></section>
<section class="toc-page">{build_toc(toc, title)}</section>
<main>{body}</main></body></html>"""
    return doc, toc


# ----------------------------------------------------------------------------- lint
def lint(md_text, deny_extra):
    text = strip_comments(md_text)
    text = re.sub(r"```mermaid.*?```", "", text, flags=re.S)  # rotulos de diagrama nao entram no lint de termos
    problems = []
    rules = DEFAULT_DENY + [(p, "termo proibido (--deny)") for p in deny_extra]
    for ln, line in enumerate(text.splitlines(), 1):
        for rx, why in rules:
            for m in re.finditer(rx, line):
                problems.append((ln, why, line.strip()[:90]))
    if re.search(r"^#{1,6}\s*$", text, re.M):
        problems.append((0, "titulo vazio", ""))
    return problems


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md")
    ap.add_argument("pdf", nargs="?")
    ap.add_argument("--css", default=str(HERE / "print.css"))
    ap.add_argument("--keep-work", metavar="DIR", help="mantem HTML e PNGs intermediarios neste diretorio")
    ap.add_argument("--no-mermaid", action="store_true", help="nao renderiza diagramas (mostra o codigo)")
    ap.add_argument("--scale", type=float, default=2.5, help="escala (DPI relativo) dos PNG dos diagramas")
    ap.add_argument("--lint-only", action="store_true")
    ap.add_argument("--strict", action="store_true", help="falha (exit 1) se o lint achar algo")
    ap.add_argument("--deny", action="append", default=[], metavar="REGEX", help="termo/regex extra proibido")
    a = ap.parse_args()

    raw = Path(a.md).read_text(encoding="utf-8")
    meta, body = parse_front_matter(raw)
    body = strip_comments(body)

    probs = lint(body, a.deny)
    for ln, why, line in probs:
        print(f"LINT linha~{ln}: {why}: {line}", file=sys.stderr)
    print(f"lint: {len(probs)} problema(s)")
    if a.lint_only:
        sys.exit(1 if probs and a.strict else 0)
    if probs and a.strict:
        sys.exit(1)
    if not a.pdf:
        ap.error("informe o PDF de saida")

    work = Path(a.keep_work) if a.keep_work else Path(tempfile.mkdtemp(prefix="archdoc-"))
    work.mkdir(parents=True, exist_ok=True)
    try:
        doc, toc = build_html(meta, body, work, a.css, a.no_mermaid, a.scale)
        (work / "documento.html").write_text(doc, encoding="utf-8")
        out = Path(a.pdf)
        out.parent.mkdir(parents=True, exist_ok=True)
        HTML(string=doc, base_url=str(work)).write_pdf(str(out))
    finally:
        if not a.keep_work:
            shutil.rmtree(work, ignore_errors=True)
    try:
        n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(out)], capture_output=True, text=True).stdout).group(1))
    except Exception:
        n = "?"
    print(f"PDF: {out}  ({n} paginas, {len(toc)} titulos)")


if __name__ == "__main__":
    main()
