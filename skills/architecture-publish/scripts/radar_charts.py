#!/usr/bin/env python3
"""Gera os gráficos radar (polares) das páginas de Tecnologias Avaliadas e,
opcionalmente, injeta o bloco "Comparativo visual" (imagem + tabela de notas)
no rascunho da página.

Uso:
    radar_charts.py DADOS.json SAIDA_DIR --prefix <sistema> [--manifest manifest.json]
                    [--sistema "NOME"] [--fill TEMPLATE.md --out PAGINA.md]

Dependência: matplotlib (use um venv; nunca instalação global).

DADOS.json: lista de camadas (ver templates/radar-data.example.json)
    [{"slug": "framework-da-api", "titulo": "Linguagem e framework da API",
      "criterios": ["Critério 1", ...],             # 3 a 5; "\\n" opcional para quebrar linha
      "alternativas": [{"nome": "...", "notas": [0..10, ...],   # 0-10, mesmo nº de critérios
                        "escolhida": true,                       # exatamente 1 por camada
                        "sufixo": "(escolhida)",                 # opcional (legenda)
                        "marcas": [idx, ...],                    # opcional: índices de notas com † (só tabela)
                        "situacao": "Escolhida"}, ...]}]         # opcional (só tabela)

Saída: SAIDA_DIR/<prefix>-<slug>-<uuid4>.png (1 por camada). O uuid é reaproveitado se
--manifest apontar para um JSON existente (slug -> nome do arquivo), para não gerar
arquivos novos a cada execução; sem manifest, gera sempre um uuid novo.
O PNG vai para `.attachments/` da wiki; a página referencia `/.attachments/<arquivo>`.

--fill/--out: remove o comentário-guia inicial `<!-- ... -->` do TEMPLATE.md, substitui cada marcador `@@CMP:<slug>@@` pelo bloco
"### Comparativo visual" (imagem + tabela + 2 linhas fixas) e grava PAGINA.md.

Estilo: título à esquerda "Comparação — <Camada>", anéis tracejados 2/4/6/8/10, círculo
externo preto, legenda fora (canto superior direito) com "(escolhida)" na primeira entrada,
série escolhida azul traço 4 + preenchimento, demais vermelho/verde/roxo traço 2 com alfa 0.1,
DejaVu Sans, figsize 9x7, bbox tight.
"""
import argparse
import json
import math
import os
import re
import sys
import textwrap
import uuid

CORES = ["blue", "red", "green", "purple"]


def quebrar(rotulo, largura=20):
    if "\n" in rotulo:
        return rotulo
    linhas = textwrap.wrap(rotulo, width=largura, break_long_words=False)
    if len(linhas) > 2:  # no máximo 2 linhas: junta o excedente na segunda
        linhas = [linhas[0], " ".join(linhas[1:])]
    return "\n".join(linhas)


def validar(camadas):
    for c in camadas:
        n = len(c["criterios"])
        if not 3 <= n <= 5:
            raise ValueError(f"{c['slug']}: use de 3 a 5 critérios (tem {n})")
        alts = c["alternativas"]
        if not 2 <= len(alts) <= 4:
            raise ValueError(f"{c['slug']}: use de 2 a 4 alternativas (tem {len(alts)})")
        if sum(1 for a in alts if a.get("escolhida")) != 1:
            raise ValueError(f"{c['slug']}: exatamente 1 alternativa deve ter escolhida=true")
        for a in alts:
            if len(a["notas"]) != n:
                raise ValueError(f"{c['slug']}: '{a['nome']}' tem {len(a['notas'])} notas para {n} critérios")
            if any(not 0 <= v <= 10 for v in a["notas"]):
                raise ValueError(f"{c['slug']}: '{a['nome']}' tem nota fora de 0-10")


def desenhar(camada, destino):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams["font.family"] = "DejaVu Sans"

    criterios = [quebrar(c) for c in camada["criterios"]]
    n = len(criterios)
    angulos = [i * 2 * math.pi / n for i in range(n)]
    angulos_fechados = angulos + angulos[:1]

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="polar")
    ax.set_ylim(0, 10)
    ax.set_xticks(angulos)
    ax.set_xticklabels(criterios, fontsize=10)
    ax.tick_params(axis="x", pad=18)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["", "4", "6", "8", "10"], fontsize=8, color="gray")
    ax.set_rlabel_position(22)
    ax.yaxis.grid(True, linestyle="--", color="silver", linewidth=0.9, alpha=0.8)
    ax.xaxis.grid(True, linestyle="--", color="silver", linewidth=0.9, alpha=0.8)
    ax.spines["polar"].set_color("black")
    ax.spines["polar"].set_linewidth(1.0)

    # a escolhida sempre vem primeiro (azul)
    ordenadas = sorted(camada["alternativas"], key=lambda a: 0 if a.get("escolhida") else 1)
    for idx, alt in enumerate(ordenadas):
        notas = list(alt["notas"])
        valores = notas + notas[:1]
        cor = CORES[idx % len(CORES)]
        escolhida = bool(alt.get("escolhida"))
        rotulo = alt["nome"] + (f" {alt.get('sufixo', '(escolhida)')}" if escolhida else "")
        ax.plot(angulos_fechados, valores, color=cor, linewidth=4 if escolhida else 2, label=rotulo)
        ax.fill(angulos_fechados, valores, color=cor, alpha=0.2 if escolhida else 0.1)

    fig.suptitle(f"Comparação — {camada['titulo']}", x=0.14, y=0.99, ha="left", fontsize=14)
    ax.legend(loc="upper left", bbox_to_anchor=(1.12, 1.12), fontsize=9, frameon=True)
    fig.savefig(destino, dpi=125, bbox_inches="tight")
    plt.close(fig)


def bloco_comparativo(camada, arquivo, sistema, prefix):
    """Markdown do '### Comparativo visual' (padrão das 3 páginas)."""
    crit = [x.replace("\n", " ") for x in camada["criterios"]]
    slug = camada["slug"]
    out = ["### Comparativo visual", "", f"![{prefix}-{slug}.png](/.attachments/{arquivo})", "",
           "| Alternativa | " + " | ".join(crit) + " | Média | Situação |",
           "|---|" + "---|" * (len(crit) + 2)]
    for a in camada["alternativas"]:
        notas = a["notas"]
        media = sum(notas) / len(notas)
        esc = bool(a.get("escolhida"))
        marcas = set(a.get("marcas", []))
        cels = []
        for i, v in enumerate(notas):
            t = f"{v}" + ("†" if i in marcas else "")
            cels.append(f"**{t}**" if esc else t)
        nome = f"✅ **{a['nome']}**" if esc else a["nome"]
        sit = a.get("situacao", "Escolhida" if esc else "Descartada")
        sit = f"**{sit}**" if esc else sit
        med = f"{media:.1f}"
        med = f"**{med}**" if esc else med
        out.append(f"| {nome} | " + " | ".join(cels) + f" | {med} | {sit} |")
    out += ["",
            f"Escala de 0 a 10 (10 = melhor para o {sistema}; em custo, esforço e quantidade de componentes, "
            "10 = menor). Notas sem marca traduzem o que o comparativo registrado mostra; a média é simples e "
            "serve só de apoio à leitura, a decisão segue o registro acima.",
            "", "† Avaliação da equipe de arquitetura, sem comparativo formal registrado."]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        description="Gera gráficos radar (PNG) e blocos de comparativo visual para a wiki.",
        epilog="Dependência: matplotlib (venv). Exemplo: radar_charts.py radar-data.json .attachments "
               "--prefix meusistema --manifest manifest.json --sistema MEUSISTEMA "
               "--fill tec.tpl.md --out Tecnologias-Avaliadas.md")
    ap.add_argument("dados", help="JSON com a lista de camadas (ver radar-data.example.json)")
    ap.add_argument("saida", help="diretório de saída dos PNG (normalmente .attachments/ da wiki)")
    ap.add_argument("--prefix", default="sistema", help="prefixo do arquivo: <prefix>-<slug>-<uuid4>.png (use o slug do sistema)")
    ap.add_argument("--manifest", default=None, help="JSON slug->arquivo, reaproveita os uuids entre execuções")
    ap.add_argument("--sistema", default=None, help="nome do sistema no texto da escala (padrão: prefixo em maiúsculas)")
    ap.add_argument("--fill", default=None, help="rascunho .md com marcadores @@CMP:<slug>@@")
    ap.add_argument("--out", default=None, help="página .md gerada a partir de --fill")
    args = ap.parse_args()

    if bool(args.fill) != bool(args.out):
        ap.error("--fill e --out devem ser usados juntos")

    with open(args.dados, encoding="utf-8") as f:
        camadas = json.load(f)
    validar(camadas)
    os.makedirs(args.saida, exist_ok=True)

    manifest = {}
    if args.manifest and os.path.exists(args.manifest):
        with open(args.manifest, encoding="utf-8") as f:
            manifest = json.load(f)

    por_slug = {}
    for camada in camadas:
        slug = camada["slug"]
        nome = manifest.get(slug) or f"{args.prefix}-{slug}-{uuid.uuid4()}.png"
        manifest[slug] = nome
        desenhar(camada, os.path.join(args.saida, nome))
        por_slug[slug] = camada
        print(nome)

    if args.manifest:
        with open(args.manifest, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    if args.fill:
        sistema = args.sistema or args.prefix.upper()
        with open(args.fill, encoding="utf-8") as f:
            texto = f.read()

        def troca(m):
            slug = m.group(1)
            if slug not in por_slug:
                raise SystemExit(f"marcador @@CMP:{slug}@@ sem camada correspondente no JSON")
            return bloco_comparativo(por_slug[slug], manifest[slug], sistema, args.prefix)

        texto = re.sub(r"\A\s*<!--.*?-->\s*", "", texto, count=1, flags=re.S)  # remove o comentário-guia do modelo
        texto = re.sub(r"@@CMP:([\w-]+)@@", troca, texto)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(texto.rstrip("\n") + "\n")
        print(f"página gerada: {args.out}")


if __name__ == "__main__":
    sys.exit(main())
