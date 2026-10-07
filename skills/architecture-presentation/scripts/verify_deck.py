#!/usr/bin/env python3
"""Verificação mecânica do deck de arquitetura (Fase 2). Sai com 1 se houver qualquer problema.

Uso: verify_deck.py WORKDIR [--max-slides 20] [--deny "Nome Pessoa" --deny "sigla interna" ...] [--termos extra.txt]

Confere, em deck.html (texto visível), assets/notes.json, PDF e PPTX (notas):
  - contagem de slides <= 20 (e PDF/PPTX com a mesma contagem do HTML);
  - termos banidos (templates/termos-banidos.txt: regex :: motivo), --deny e --termos extras;
  - IDs internos (F-/A-/Q-/R-/P-/RF-/RNF-/RES-/TD-/G-/RV-NNN, ADR-, DEC-), custos, caminhos locais, menção a ferramenta de IA;
  - marcadores de modelo não preenchidos (TODO, lorem, {{ }}, <...>);
  - títulos: afirmação (não rótulo de 1-3 palavras), sem "Nome: explicação", tamanho que cabe em 1 linha;
  - radar-data.json: justificativa+evidência por nota, NOT EVALUATED, sem "experiência da equipe";
  - transbordo/texto cortado detectado pelo build (.overflow.txt).
O que o script NÃO prova: leia TODOS os slides (PNG em assets/slides/) com Read.
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)

ID_RE = re.compile(r"\b(?:F|A|Q|R|P|RF|RNF|RES|TD|G|RV|NFR|FR|US|PBI)-\d{1,4}\b|\b(?:ADR|DEC|RFC)-\d{0,4}\b")
COST_RE = re.compile(r"R\$\s*\d|US\$|\bUSD\s*\d|€\s*\d|\b\d[\d.,]*\s*(?:mil\s+)?(?:reais|dólares|dolares)\b|\bcusto\s+(?:mensal|anual|total)\s+de\b", re.I)
PATH_RE = re.compile(r"/home/\w+|/Users/\w+|/tmp/|/mnt/[a-z]/|\b[A-Za-z]:\\\\|file://|~/\.|\.cla[u]de/|\.architecture/|docs/architecture/")
PLACEHOLDER_RE = re.compile(r"\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|[Ll]orem ipsum|\{\{|\}\}|@@|&lt;[A-Za-zÀ-ú _-]{2,30}&gt;|<[A-Za-zÀ-ú _-]{2,30}>|\[(?:[Cc]liente|[Ss]istema|[Nn]ome|[Dd]ata)\]")


def texto_visivel(doc):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", doc, flags=re.S)
    t = re.sub(r"<(br|/p|/h\d|/div|/tr|/li)[^>]*>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)


def notas_pptx(path):
    out = []
    with zipfile.ZipFile(path) as z:
        for n in sorted(z.namelist()):
            if re.match(r"ppt/(notesSlides|slides)/[^/]+\.xml$", n):
                out.append(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "ignore")))
    return "\n".join(out)


def n_slides_pptx(path):
    with zipfile.ZipFile(path) as z:
        return len([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)])


def carregar_termos(paths):
    regs = []
    for p in paths:
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            rx, _, why = ln.partition("::")
            regs.append((re.compile(rx.strip(), re.I), why.strip() or "termo banido"))
    return regs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workdir")
    ap.add_argument("--max-slides", type=int, default=20)
    ap.add_argument("--deny", action="append", default=[], help="termo literal proibido (nome de pessoa, sigla interna, custo)")
    ap.add_argument("--termos", action="append", default=[], help="arquivo extra de termos (regex :: motivo)")
    a = ap.parse_args()
    wd = os.path.abspath(a.workdir)
    erros, avisos = [], []

    def err(m):
        erros.append(m)

    deck_html = os.path.join(wd, "deck.html")
    if not os.path.exists(deck_html):
        sys.exit(f"sem {deck_html}: rode build.sh antes")
    doc = open(deck_html, encoding="utf-8").read()
    secoes = re.findall(r'<section class="slide[^"]*"[^>]*>.*?</section>', doc, flags=re.S)
    n = len(secoes)
    print(f"slides no HTML: {n}")
    if n > a.max_slides:
        err(f"{n} slides > máximo {a.max_slides}")
    if n == 0:
        err("nenhum slide encontrado")

    # contagem PDF / PPTX
    pdfs = [f for f in os.listdir(wd) if f.endswith(".pdf")]
    pptxs = [f for f in os.listdir(wd) if f.endswith(".pptx")]
    if not pdfs:
        err("PDF ausente")
    for f in pdfs:
        try:
            info = subprocess.run(["pdfinfo", os.path.join(wd, f)], capture_output=True, text=True).stdout
            pg = int(re.search(r"Pages:\s+(\d+)", info).group(1))
            print(f"{f}: {pg} páginas")
            if pg != n:
                err(f"{f}: {pg} páginas != {n} slides do HTML")
        except Exception as e:  # pdfinfo ausente
            avisos.append(f"pdfinfo indisponível ({e}); contagem do PDF não conferida")
    if not pptxs:
        err("PPTX ausente")
    for f in pptxs:
        k = n_slides_pptx(os.path.join(wd, f))
        print(f"{f}: {k} slides")
        if k != n:
            err(f"{f}: {k} slides != {n} do HTML")
    pngs = os.path.join(wd, "assets", "slides")
    if os.path.isdir(pngs) and len([x for x in os.listdir(pngs) if x.endswith(".png")]) != n:
        err("PNGs por slide != nº de slides (rode build.sh de novo)")

    # corpus de texto
    corpus = {"deck.html": texto_visivel(doc)}
    nj = os.path.join(wd, "assets", "notes.json")
    if os.path.exists(nj):
        corpus["notes.json"] = "\n".join(json.load(open(nj, encoding="utf-8")))
    for f in pptxs:
        corpus[f] = notas_pptx(os.path.join(wd, f))
    # metadados do PDF/PPTX (autor, título)
    termos = carregar_termos([os.path.join(SKILL, "templates", "termos-banidos.txt")] + a.termos)
    for nome, txt in corpus.items():
        for rx, why in termos:
            for m in rx.finditer(txt):
                ctx = txt[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                err(f"{nome}: termo banido '{m.group(0)}' ({why}) ... {ctx} ...")
        for d in a.deny:
            if d.lower() in txt.lower():
                err(f"{nome}: termo proibido (--deny) '{d}'")
        for label, rx in (("ID interno", ID_RE), ("custo", COST_RE), ("caminho local", PATH_RE), ("marcador não preenchido", PLACEHOLDER_RE)):
            for m in rx.finditer(txt):
                ctx = txt[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                err(f"{nome}: {label} '{m.group(0)}' ... {ctx} ...")

    # títulos
    for i, s in enumerate(secoes, 1):
        m = re.search(r'<h1 class="title">(.*?)</h1>', s, flags=re.S)
        if not m:
            if 'class="slide cover' not in s:
                err(f"slide {i}: sem título")
            continue
        t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        if len(t.split()) < 4:
            err(f"slide {i}: título '{t}' parece rótulo (<4 palavras); use uma afirmação")
        if ":" in t:
            err(f"slide {i}: título com ':' ('Nome: explicação'); use uma afirmação única")
        if len(t) > 56:
            avisos.append(f"slide {i}: título com {len(t)} caracteres; pode não caber em 1 linha")

    # matriz tecnológica
    rd = os.path.join(wd, "radar-data.json")
    if os.path.exists(rd):
        import radar_charts as rc
        try:
            info = rc.analisar(rc.carregar(rd))
            print(f"radar-data: {len(info)} camadas válidas")
        except ValueError as e:
            for ln in str(e).splitlines():
                err(f"radar-data: {ln}")

    ov = os.path.join(wd, ".overflow.txt")
    if os.path.exists(ov):
        err("transbordo/texto cortado detectado no build: " + open(ov).read().strip())

    for v in avisos:
        print("AVISO:", v)
    if erros:
        print(f"\n{len(erros)} problema(s):")
        for e in erros:
            print(" -", e)
        sys.exit(1)
    print("verify_deck: 0 problemas (falta a leitura visual de todos os slides)")


if __name__ == "__main__":
    main()
