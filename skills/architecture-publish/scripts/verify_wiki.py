#!/usr/bin/env python3
"""Verificação obrigatória da wiki limpa de um sistema (Azure DevOps wiki em git).

Uso:
    verify_wiki.py WIKI_ROOT SISTEMA_DIR [--prefix <sistema>] [--deny TERMO ...]
                   [--allow-id REGEX] [--no-pattern-check]

    WIKI_ROOT    raiz da worktree da wiki (contém .attachments/ e a pasta Documentação/)
    SISTEMA_DIR  pasta do sistema relativa a WIKI_ROOT, ex.: Documentação/MEUSISTEMA
                 (a página de landing é SISTEMA_DIR + ".md")

Verifica (exit 1 se houver qualquer problema):
  1. links absolutos `](/...)` resolvem para página (.md), pasta ou arquivo; imagens em /.attachments/ existem;
  2. `.order` de cada pasta: lista exatamente as páginas da pasta (sem extensão, sem newline final);
     pasta sem página-pai .md é erro;
  3. blocos mermaid `::: mermaid` ... `:::` balanceados (nunca ```mermaid);
  4. IDs internos = 0 (F/A/Q/R/P/RF/RNF/RES/TD/G/RV-NNN, ADR-, DEC-, PROPOSAL, PROPOSED, ACCEPTED, marcadores [KNOWN ...]);
  5. sem caminhos locais (/home/, /tmp/, C:\\), sem "Claude"/"Anthropic", sem selos coloridos (🟢🟡🔴),
     sem links para páginas internas (decisões, riscos, perguntas) e sem termos de --deny;
  6. tabelas com número de colunas consistente em cada bloco;
  7. páginas padrão (Tecnologias-Avaliadas, Componentes, Banco-de-Dados e a página-pai delas, ex. Nova-Arquitetura-da-API; a landing do sistema fica fora desta regra):
     sem H1, sem [[_TOC_]], sem separador `---`, 1ª linha em negrito com ponto final;
     Tecnologias-Avaliadas: toda imagem referenciada existe e há "Escala de 0 a 10" e "†" por comparativo;
  8. PNGs de .attachments com o --prefix do sistema que não são referenciados por nenhuma página (órfãos: aviso).

Só usa a biblioteca padrão do Python.
"""
import argparse
import glob
import os
import re
import sys
from urllib.parse import unquote

ID_PADRAO = (r"\b(F|A|Q|R|P|RF|RNF|RES|TD|G|RV)-\d{3}\b|\bADR-\d|\bDEC-\d|PROPOSAL|PROPOSED|ACCEPTED|"
             r"\[(KNOWN|ASSUMPTION|OPEN|DECISION|RISK)\b|-novo-\d")
PROIBIDOS = ["/home/", "/tmp/", "C:\\", "Claude", "Anthropic", "🟢", "🟡", "🔴",
             "Questões-e-Decisões", "Mapa-de-Riscos", "Decisões-de-Arquitetura", "Registro-de-Decisões"]
PADRAO3 = {"Tecnologias-Avaliadas", "Componentes", "Banco-de-Dados"}


def main():
    ap = argparse.ArgumentParser(description="Verifica a wiki limpa de um sistema (links, .order, mermaid, imagens, IDs internos).",
                                 epilog="Exemplo: verify_wiki.py ./wiki-wt Documentação/MEUSISTEMA --prefix meusistema --deny 'Fulano'")
    ap.add_argument("wiki_root")
    ap.add_argument("sistema_dir", help="ex.: Documentação/MEUSISTEMA")
    ap.add_argument("--prefix", default=None, help="prefixo dos PNG de radar em .attachments (padrão: nome da pasta em minúsculas)")
    ap.add_argument("--deny", nargs="*", default=[], help="termos extras proibidos (nomes de pessoas, custos, siglas internas)")
    ap.add_argument("--allow-id", default=None, help="regex de ocorrências que NÃO devem contar como ID interno (ex.: um código de produto real)")
    ap.add_argument("--no-pattern-check", action="store_true", help="pula a checagem de formato das páginas padrão (use em wikis sem as 3 páginas)")
    args = ap.parse_args()

    root = os.path.abspath(args.wiki_root)
    os.chdir(root)
    sdir = args.sistema_dir.rstrip("/")
    if not os.path.isdir(sdir):
        sys.exit(f"pasta do sistema não encontrada: {sdir}")
    prefix = (args.prefix or os.path.basename(sdir).lower()) + "-"
    files = glob.glob(sdir + "/**/*.md", recursive=True)
    if os.path.exists(sdir + ".md"):
        files.append(sdir + ".md")
    files.sort()
    bad = 0

    def err(*a):
        nonlocal bad
        bad += 1
        print("ERRO", *a)

    def existe(link):
        p = unquote(link.split("#")[0]).lstrip("/")
        return os.path.exists(p + ".md") or os.path.isdir(p) or os.path.exists(p)

    id_re = re.compile(ID_PADRAO)
    allow = re.compile(args.allow_id) if args.allow_id else None
    deny = PROIBIDOS + list(args.deny)
    referenciadas = set()

    for f in files:
        t = open(f, encoding="utf-8").read()
        nome = os.path.splitext(os.path.basename(f))[0]
        # 1. links e imagens
        for m in re.finditer(r"\]\((/[^)\s]+)\)", t):
            l = m.group(1)
            if l.startswith("/.attachments/"):
                referenciadas.add(os.path.basename(unquote(l)))
                if not os.path.exists(unquote(l)[1:]):
                    err(f, "IMAGEM inexistente", l)
            elif not existe(l):
                err(f, "LINK quebrado", l)
            elif l.endswith(".md"):
                err(f, "LINK com .md (use sem extensão)", l)
        # 3. mermaid
        if "```mermaid" in t:
            err(f, "mermaid com cerca de código; use '::: mermaid'")
        if len(re.findall(r"^:::", t, re.M)) % 2:
            err(f, "blocos '::: mermaid' desbalanceados")
        # 4/5. IDs e proibidos
        for i, line in enumerate(t.split("\n"), 1):
            m = id_re.search(line)
            if m and not (allow and allow.search(m.group(0))):
                err(f, i, "ID/selo interno:", line[:90])
        for w in deny:
            if w and w in t:
                err(f, "contém termo proibido:", w)
        # 6. tabelas
        bloco = []
        for i, line in enumerate(t.split("\n") + [""], 1):
            if line.startswith("|"):
                bloco.append((i, len(re.findall(r"(?<!\\)\|", line))))
            else:
                if bloco and len({c for _, c in bloco}) > 1:
                    err(f, "tabela com colunas inconsistentes a partir da linha", bloco[0][0])
                bloco = []
        # 7. páginas padrão
        pai_padrao = f != sdir + ".md" and os.path.isdir(os.path.splitext(f)[0]) and any(
            os.path.exists(os.path.join(os.path.splitext(f)[0], p + ".md")) for p in PADRAO3)
        if not args.no_pattern_check and (nome in PADRAO3 or pai_padrao):
            if re.search(r"^# ", t, re.M):
                err(f, "H1 não permitido nas páginas padrão")
            if "[[_TOC_]]" in t:
                err(f, "[[_TOC_]] não permitido nas páginas padrão")
            if re.search(r"^(---|\* \* \*)\s*$", t, re.M):
                err(f, "separador '---' não permitido nas páginas padrão")
            if not re.match(r"\*\*[^\n]*\.\*\*", t):
                err(f, "1ª linha deve ser negrito terminando em ponto: **Texto.**")
            if pai_padrao and not t.rstrip().endswith("[[_TOSP_]]"):
                err(f, "página-pai deve terminar com [[_TOSP_]]")
            if nome == "Tecnologias-Avaliadas":
                n_img = len(re.findall(r"!\[[^\]]*\]\(/\.attachments/", t))
                if n_img and (t.count("Escala de 0 a 10") < n_img or t.count("† Avaliação") < n_img):
                    err(f, "cada comparativo visual precisa das 2 linhas fixas (Escala de 0 a 10 / †)")
            if nome == "Componentes" and "::: mermaid" not in t:
                err(f, "Componentes sem diagrama '::: mermaid'")
            if nome == "Banco-de-Dados" and "erDiagram" not in t:
                err(f, "Banco-de-Dados sem diagrama erDiagram")

    # 2. .order
    pastas = {os.path.dirname(f) for f in files if os.path.dirname(f) != os.path.dirname(sdir)}
    pastas.add(sdir)
    for d in sorted(pastas):
        ordem = os.path.join(d, ".order")
        paginas = {os.path.splitext(x)[0] for x in os.listdir(d) if x.endswith(".md")}
        if not os.path.exists(ordem):
            if paginas:
                err(d, ".order ausente")
            continue
        raw = open(ordem, encoding="utf-8").read()
        if raw.endswith("\n"):
            print("AVISO", ordem, "termina com newline (padrão: sem newline final)")
        ent = [e for e in raw.split("\n") if e]
        for e in ent:
            if e not in paginas:
                err(ordem, "entrada sem página:", e)
        for p in sorted(paginas - set(ent)):
            err(ordem, "página fora do .order:", p)
        if len(ent) != len(set(ent)):
            err(ordem, "entradas duplicadas")
        for x in os.listdir(d):
            if os.path.isdir(os.path.join(d, x)) and x not in paginas:
                err(d, "pasta sem página-pai .md:", x)

    # 8. órfãos
    anex = [x for x in os.listdir(".attachments") if x.startswith(prefix)] if os.path.isdir(".attachments") else []
    for x in anex:
        if x not in referenciadas:
            print("AVISO PNG órfão em .attachments:", x)
    print(f"arquivos verificados: {len(files)} | PNGs '{prefix}*': {len(anex)} | problemas: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
