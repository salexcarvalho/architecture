#!/usr/bin/env python3
"""Matriz tecnológica -> radares (PNG) para o deck de arquitetura.

Uso:
    radar_charts.py DADOS.json SAIDA_DIR [--deck conteudo-deck.json] [--prefix radar] [--check]

  --check   só valida o JSON (sem matplotlib) e imprime as médias.
  --deck    desenha só as camadas usadas nos slides "radar" do deck; 1 radar por slide = perfil grande (g),
            2 por slide = perfil par (p). Sem --deck, desenha todas as camadas no perfil g.

DADOS.json: lista de camadas (ver templates/radar-data.example.json):
  [{"slug": "...", "titulo": "...", "criterios": ["...", ...],            # 3 a 6
    "regua_precedente": {...},                                            # obrigatório se há critério "Precedente na organização"
    "alternativas": [{"nome": "...", "escolhida": true, "situacao": "...",
                      "notas": [0..10 | null],                            # null = NOT EVALUATED (sem evidência)
                      "justificativas": ["...", ...],                     # 1 por critério (alias: justification)
                      "evidencias": ["P: ...", ...],                      # 1 por critério (alias: evidence)
                      "marcas": [idx]}]}]                                  # opcional: nota provisória (†)

Regras de qualidade (erro se violadas):
  - toda nota tem JUSTIFICATIVA e EVIDÊNCIA; null exige o motivo na justificativa (NOT EVALUATED);
  - o radar plota só critérios avaliados para TODAS as alternativas; os demais viram "n/a" (fora da média);
  - nada de critério "Experiência da equipe/time": use "Precedente na organização" (régua única) ou NOT EVALUATED;
  - exatamente 1 alternativa escolhida; 2 a 4 alternativas.
Requer matplotlib só para desenhar (use um venv; nunca instalação global).
"""
import argparse
import json
import math
import os
import re
import sys
import textwrap

CORES = ["#0000FF", "#FF0000", "#008000", "#800080"]  # escolhida azul, demais na ordem
PRECEDENTE = re.compile(r"preced[eê]n(?:cia|te)", re.I)
EXPERIENCIA = re.compile(r"experi[eê]ncia\s+(d[aoe]s?\s+)?(equipe|time|pessoal|squad)", re.I)
NOT_EVAL = "NOT EVALUATED"


def _pick(d, *keys, default=None):
    for k in keys:
        if k in d:
            return d[k]
    return default


def carregar(path):
    return json.load(open(path, encoding="utf-8"))


def analisar(camadas):
    """Valida e devolve {slug: camada enriquecida} (plotados, medias, n/a). Levanta ValueError listando todos os erros."""
    erros, out = [], {}
    for c in camadas:
        slug = c.get("slug", "?")
        crit = c.get("criterios", [])
        alts = c.get("alternativas", [])
        n = len(crit)
        if slug in out:
            erros.append(f"{slug}: slug duplicado")
        if not 3 <= n <= 6:
            erros.append(f"{slug}: use de 3 a 6 critérios (tem {n})")
        if not 2 <= len(alts) <= 4:
            erros.append(f"{slug}: use de 2 a 4 alternativas (tem {len(alts)})")
        if sum(1 for a in alts if a.get("escolhida")) != 1:
            erros.append(f"{slug}: exatamente 1 alternativa com escolhida=true")
        for ci in crit:
            if EXPERIENCIA.search(ci):
                erros.append(f"{slug}: critério '{ci}' proibido; use 'Precedente na organização' (régua única) ou NOT EVALUATED")
        if any(PRECEDENTE.search(ci) for ci in crit) and not c.get("regua_precedente"):
            erros.append(f"{slug}: critério de precedente exige 'regua_precedente' (mesma régua para todas as alternativas)")
        for a in alts:
            nome = a.get("nome", "?")
            notas = a.get("notas", [])
            just = _pick(a, "justificativas", "justification", default=[])
            evid = _pick(a, "evidencias", "evidence", default=[])
            if len(notas) != n or len(just) != n or len(evid) != n:
                erros.append(f"{slug}/{nome}: notas({len(notas)}), justificativas({len(just)}) e evidencias({len(evid)}) devem ter {n} itens")
                continue
            for i, v in enumerate(notas):
                lab = f"{slug}/{nome}/{crit[i]}"
                if not str(just[i]).strip():
                    erros.append(f"{lab}: sem justificativa")
                if v is None or v == NOT_EVAL:
                    continue
                if not isinstance(v, (int, float)) or not 0 <= v <= 10:
                    erros.append(f"{lab}: nota fora de 0-10")
                if not str(evid[i]).strip():
                    erros.append(f"{lab}: nota sem evidência (use null = NOT EVALUATED)")
        # derivados
        if len(alts) >= 2 and not erros:
            ok = [i for i in range(n) if all(_nota(a, i) is not None for a in alts)]
            nao = [i for i in range(n) if i not in ok]
            if len(ok) < 3:
                erros.append(f"{slug}: só {len(ok)} critério(s) avaliado(s) para todas as alternativas (mínimo 3 para o radar)")
            else:
                medias, sem_prec = {}, {}
                idx_prec = [i for i in ok if PRECEDENTE.search(crit[i])]
                for a in alts:
                    vs = [_nota(a, i) for i in ok]
                    medias[a["nome"]] = sum(vs) / len(vs)
                    vp = [_nota(a, i) for i in ok if i not in idx_prec]
                    sem_prec[a["nome"]] = sum(vp) / len(vp) if vp and idx_prec else None
                na = []
                for i in nao:
                    motivo = next((str(_pick(a, "justificativas", "justification")[i]) for a in alts if _nota(a, i) is None), "")
                    na.append({"criterio": crit[i], "motivo": motivo})
                out[slug] = dict(c, _plot=ok, _medias=medias, _sem_prec=sem_prec, _na=na)
    if erros:
        raise ValueError("\n".join(erros))
    return out


def _nota(a, i):
    v = a["notas"][i]
    return None if v is None or v == NOT_EVAL else float(v)


def quebrar(rotulo, largura=20):
    linhas = textwrap.wrap(rotulo, width=largura, break_long_words=False)
    if len(linhas) > 2:
        linhas = [linhas[0], " ".join(linhas[1:])]
    return "\n".join(linhas)


PERFIL = {"g": dict(fig=(5.0, 4.1), fs=14, w=22, pad=15), "p": dict(fig=(4.0, 3.2), fs=13, w=28, pad=10)}


def desenhar(camada, destino, perfil="g"):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    p = PERFIL[perfil]
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    ok = camada["_plot"]
    rot = [quebrar(camada["criterios"][i], p["w"]) for i in ok]
    n = len(rot)
    ang = [i * 2 * math.pi / n for i in range(n)]
    fig = plt.figure(figsize=p["fig"])
    ax = fig.add_subplot(111, projection="polar")
    ax.set_ylim(0, 10)
    ax.set_xticks(ang)
    labels = ax.set_xticklabels(rot, fontsize=p["fs"])
    for i, lab in enumerate(labels):  # rótulos laterais não invadem o gráfico
        c = math.cos(ang[i])
        lab.set_ha("left" if c > 0.4 else "right" if c < -0.4 else "center")
    ax.tick_params(axis="x", pad=p["pad"])
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["", "4", "6", "8", "10"], fontsize=9, color="gray")
    ax.set_rlabel_position(22)
    ax.yaxis.grid(True, linestyle="--", color="silver", linewidth=0.9, alpha=0.8)
    ax.xaxis.grid(True, linestyle="--", color="silver", linewidth=0.9, alpha=0.8)
    ax.spines["polar"].set_color("black")
    for k, a in enumerate(ordenadas(camada)):
        vs = [_nota(a, i) for i in ok]
        cor = CORES[k % len(CORES)]
        esc = bool(a.get("escolhida"))
        ax.plot(ang + ang[:1], vs + vs[:1], color=cor, linewidth=4 if esc else 2)
        ax.fill(ang + ang[:1], vs + vs[:1], color=cor, alpha=0.2 if esc else 0.1)
    fig.savefig(destino, dpi=220, bbox_inches="tight")
    plt.close(fig)


def ordenadas(camada):
    return sorted(camada["alternativas"], key=lambda a: 0 if a.get("escolhida") else 1)


def perfis_do_deck(deck_path):
    """slug -> 'g' | 'p' conforme os slides do tipo radar."""
    deck = json.load(open(deck_path, encoding="utf-8"))
    uso = {}
    for s in deck.get("slides", []):
        if s.get("type") == "radar":
            slugs = s.get("slugs") or [s.get("slug")]
            for sl in slugs:
                uso[sl] = "p" if len(slugs) > 1 else "g"
    return uso


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dados")
    ap.add_argument("saida", nargs="?")
    ap.add_argument("--deck")
    ap.add_argument("--prefix", default="radar")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    try:
        info = analisar(carregar(a.dados))
    except ValueError as e:
        print("radar-data inválido:\n" + str(e), file=sys.stderr)
        sys.exit(2)
    for slug, c in info.items():
        m = ", ".join(f"{k}={v:.2f}" for k, v in c["_medias"].items())
        na = f" | n/a: {', '.join(x['criterio'] for x in c['_na'])}" if c["_na"] else ""
        print(f"{slug}: {m}{na}")
    if a.check:
        return
    if not a.saida:
        ap.error("informe SAIDA_DIR")
    uso = perfis_do_deck(a.deck) if a.deck else {s: "g" for s in info}
    faltam = [s for s in uso if s not in info]
    if faltam:
        print(f"slide radar usa slug inexistente no radar-data: {faltam}", file=sys.stderr)
        sys.exit(2)
    os.makedirs(a.saida, exist_ok=True)
    for slug, perfil in uso.items():
        dest = os.path.join(a.saida, f"{a.prefix}-{slug}.png")
        desenhar(info[slug], dest, perfil)
        print("ok", dest)


if __name__ == "__main__":
    main()
