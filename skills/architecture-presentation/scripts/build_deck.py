#!/usr/bin/env python3
"""Gera deck.html (1920x1080, 1 <section> por slide) e assets/notes.json a partir de um JSON de conteúdo.

Uso: build_deck.py WORKDIR [--content conteudo-deck.json] [--radar radar-data.json]
Só biblioteca padrão. Lê WORKDIR/conteudo-deck.json e WORKDIR/radar-data.json; copia assets (CSS e fontes)
da skill para WORKDIR/assets. Os radares (PNG) vêm de radar_charts.py (build.sh chama antes).

Tipos de slide (campo "type"): cover, kpis, diagram, flow, radar, stack, table, cards,
matrix-hoje-evolucao, timeline, risks, asks, closing. Veja templates/conteudo-deck.example.json.
Texto aceita **negrito** e \\n (quebra de linha); todo o resto é escapado.
"""
import argparse
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import radar_charts as rc  # noqa: E402

SW = rc.CORES
CAP_DEFAULT = "Notas de 0 a 10 com justificativa e evidência documentadas; critérios sem evidência não entram na média."
SEALS = {"dec": "Decisão", "capac": "Capacidade", "prop": "Proposta", "hip": "Hipótese", "pend": "Pendência", "risk": "Risco"}
BOX_KIND = {"plain": "bx", "app": "bx app", "shared": "bx shared", "dark": "bx dk", "evo": "bx evo"}
SLIDES = []
NOTES_OVERRIDE = []
META = {}
RADAR = {}


# ---------------------------------------------------------------- utilidades
def esc(t):
    return html.escape(str(t), quote=False)


def rich(t):
    s = esc(t)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s.replace("\\n", "<br>").replace("\n", "<br>")


def fmt(v):
    if v is None:
        return "n/a"
    return f"{v:.2f}".rstrip("0").rstrip(".").replace(".", ",") if abs(v * 10 - round(v * 10)) > 1e-6 else f"{v:.1f}".replace(".", ",")


def slide(body, bg="light", kicker=None, title=None, page=True, cls="", notas=None):
    n = len(SLIDES) + 1
    head = ""
    if kicker:
        head += f'<div class="kicker">{esc(kicker)}</div>'
    if title:
        head += f'<h1 class="title">{esc(title)}</h1>'
    foot = f'<div class="foot"><span>{esc(META["rodape"])}</span><span>{n:02d}</span></div>' if page else ""
    SLIDES.append(f'<section class="slide {bg} {cls}" id="s{n:02d}" data-n="{n}">{head}{body}{foot}</section>')
    NOTES_OVERRIDE.append(notas)


def card(inner, cls="", style=""):
    return f'<div class="card {cls}" style="{style}">{inner}</div>'


def seal(kind, text=None):
    return f'<span class="seal {kind}">{esc(text or SEALS[kind])}</span>'


def mini(text, x, y, teal=True):
    return f'<div class="mini {"teal" if teal else ""}" style="left:{x}px;top:{y}px">{esc(text)}</div>'


def box(x, y, w, h, title, sub="", kind="plain", num=None, extra=""):
    badge = f'<i class="nb">{esc(num)}</i>' if num else ""
    s = f"<span>{rich(sub)}</span>" if sub else ""
    return f'<div class="{BOX_KIND[kind]} {extra}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{badge}<b>{rich(title)}</b>{s}</div>'


def arrow(pts, dashed=False, label=None, lx=0, ly=0, both=False):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    cls = "ar dsh" if dashed else "ar"
    mk = "ahd" if dashed else "ah"
    start = f' marker-start="url(#{mk})"' if both else ""
    out = f'<path class="{cls}" d="{d}" marker-end="url(#{mk})"{start}/>'
    lab = f'<div class="al" style="left:{lx}px;top:{ly}px">{esc(label)}</div>' if label else ""
    return out, lab


def diagram_svg(boxes, arrows):
    paths, labels = "", ""
    for a in arrows:
        p, l = arrow(**{k: v for k, v in a.items() if k in ("pts", "dashed", "label", "lx", "ly", "both")})
        paths += p
        labels += l
    return f'<svg class="ov" width="1920" height="1080" viewBox="0 0 1920 1080">{paths}</svg>' + "".join(boxes) + labels


def table(headers, rows, widths=None, hl=None, cls=""):
    colg = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in widths) + "</colgroup>" if widths else ""
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    trs = ""
    for i, r in enumerate(rows):
        c = ' class="hl"' if hl is not None and i in (hl if isinstance(hl, (list, tuple, set)) else [hl]) else ""
        trs += f"<tr{c}>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>"
    return f'<table class="tbl {cls}">{colg}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


def strip_html(s):
    """Faixa de etapas (cadeia com setas) ou de chips. s: label, items, x, y, hi, dash, lw, chips."""
    lab = f'<div class="lbl" style="width:{s.get("lw", 230)}px">{esc(s["label"])}</div>' if s.get("label") else ""
    out = f'<div class="strip" style="left:{s.get("x", 128)}px;top:{s.get("y", 866)}px">{lab}'
    items = s["items"]
    for i, t in enumerate(items):
        cls = "ch" + (" hi" if t == s.get("hi") else "") + (" dash" if t == s.get("dash") else "")
        out += f'<div class="{cls}">{esc(t)}</div>'
        if not s.get("chips") and i < len(items) - 1:
            out += '<i class="ar2"></i>'
    if s.get("extra_dash"):
        out += f'<div class="ch dash">{esc(s["extra_dash"])}</div>'
    return out + "</div>"


def legend_html(lg):
    items = lg.get("items") if isinstance(lg, dict) else None
    items = items or [("l1", "Hoje, decisão aprovada"), ("l2", "Capacidade do desenho"), ("l3", "Serviços externos")]
    x, y = (lg.get("x", 128), lg.get("y", 740)) if isinstance(lg, dict) else (128, 740)
    if items and isinstance(items[0], dict):
        items = [(i["cls"], i["text"]) for i in items]
    inner = "".join(f'<div><i class="{c}"></i>{esc(t)}</div>' for c, t in items)
    return f'<div class="legend" style="left:{x}px;top:{y}px">{inner}</div>'


def free_elements(s):
    """Elementos posicionados livremente (diagram/flow): groups, minis, strips, notes, deps, cards, bands, pills, legend."""
    out = ""
    for g in s.get("groups", []):
        cls = "vm" if g.get("kind", "vm") == "vm" else "lane"
        out += f'<div class="{cls}" style="left:{g["x"]}px;top:{g["y"]}px;width:{g["w"]}px;height:{g["h"]}px"></div>'
        if g.get("label"):
            out += mini(g["label"], g["x"] + 22, g["y"] + 18)
    for m in s.get("minis", []):
        out += mini(m["text"], m["x"], m["y"], m.get("teal", True))
    for st in s.get("strips", []):
        out += strip_html(st)
    for n in s.get("notes", []):
        out += f'<div class="note" style="left:{n["x"]}px;top:{n["y"]}px;width:{n.get("w", 1664)}px">{rich(n["text"])}</div>'
    for d in s.get("deps", []):
        out += f'<div class="dep" style="left:{d["x"]}px;top:{d["y"]}px;width:{d["w"]}px">{rich(d["text"])}</div>'
    for c in s.get("cards", []):
        dark = " dark" if c.get("dark") else ""
        inner = (f'<h3>{rich(c["title"])}</h3>' if c.get("title") else "") + (f'<p>{rich(c["text"])}</p>' if c.get("text") else "")
        out += f'<div class="card g7{dark}" style="left:{c["x"]}px;top:{c["y"]}px;width:{c["w"]}px;height:{c["h"]}px">{inner}</div>'
    for b in s.get("bands", []):
        out += f'<div class="card dark band" style="left:{b["x"]}px;top:{b["y"]}px;width:{b.get("w", 1664)}px;height:{b.get("h", 100)}px"><p>{rich(b["text"])}</p></div>'
    for p in s.get("pills", []):
        out += f'<div class="pill {p.get("tone", "op")}" style="left:{p["x"]}px;top:{p["y"]}px;width:{p.get("w", 116)}px;padding:0">{esc(p["text"])}</div>'
    if s.get("legend"):
        out += legend_html(s["legend"] if s["legend"] is not True else {})
    return out


# ---------------------------------------------------------------- radares
def ordered(slug):
    return rc.ordenadas(RADAR[slug])


def radar_rows(slug):
    c = RADAR[slug]
    rows = []
    for i, a in enumerate(ordered(slug)):
        sit = str(a.get("situacao", "Escolhida" if a.get("escolhida") else "Alternativa avaliada")).split(" (")[0]
        rows.append([f'<i class="sw" style="background:{SW[i % 4]}"></i>{esc(a["nome"])}', fmt(c["_medias"][a["nome"]]), esc(sit)])
    return rows


def img(slug):
    return f'<img src="assets/radares/{META["radar_prefix"]}-{slug}.png" alt="Radar: {esc(RADAR[slug]["titulo"])}">'


def na_text(slug):
    nomes = [x["criterio"] for x in RADAR[slug]["_na"]]
    return f"<b>n/a</b> (sem evidência: não plotado e fora da média): {esc(', '.join(nomes))}." if nomes else ""


def why(items, head="Por que esta", cls=""):
    lis = "".join(f"<li>{rich(x)}</li>" for x in items)
    return f'<div class="card dark why {cls}"><h3>{esc(head)}</h3><ul>{lis}</ul></div>'


def render_radar(s):
    slugs = s.get("slugs") or [s["slug"]]
    for sl in slugs:
        if sl not in RADAR:
            sys.exit(f"slide radar: slug '{sl}' não existe em radar-data.json")
    cap = META.get("legenda_radar", CAP_DEFAULT)
    if len(slugs) == 1:
        sl = slugs[0]
        t = table([s.get("head", "Alternativa"), "Média", "Situação"], radar_rows(sl), ["52%", "12%", "36%"], 0, "rt")
        body = (
            f'<div class="rcard" style="left:128px;top:275px;width:800px;height:490px">{img(sl)}</div>'
            f'<div class="na" style="left:128px;top:775px;width:800px">{na_text(sl)}</div>'
            f'<div class="rcol" style="left:960px;top:275px;width:832px">{t}{why(s.get("why", []), s.get("why_head", "Por que esta"))}</div>'
            + (strip_html(s["strip"]) if s.get("strip") else "")
            + f'<div class="foot2">{esc(cap)}</div>'
        )
    else:
        body, extra = "", []
        heads = s.get("heads", ["Alternativa", "Alternativa"])
        whys = s.get("why", [[], []])
        for k, sl in enumerate(slugs[:2]):
            x = 128 + k * 856
            t = table([heads[k], "Média", "Situação"], radar_rows(sl), ["57%", "13%", "30%"], 0, "rt rc")
            lis = "".join(f"<li>{rich(i)}</li>" for i in whys[k])
            body += (
                f'<div class="rcard" style="left:{x}px;top:268px;width:808px;height:376px">{img(sl)}</div>'
                f'<div style="position:absolute;left:{x}px;top:656px;width:808px">{t}</div>'
                f'<div class="card dark why cmpct" style="position:absolute;left:{x}px;top:810px;width:808px;height:114px">'
                f'<div class="mini">POR QUE ESTA</div><ul>{lis}</ul></div>'
            )
            if RADAR[sl]["_na"]:
                extra.append(f'{esc(", ".join(x["criterio"] for x in RADAR[sl]["_na"]))}, em {esc(RADAR[sl]["titulo"].lower())}')
        na = f" <b>n/a</b> (não plotado): {'; '.join(extra)}." if extra else ""
        body += f'<div class="foot2" style="top:940px;font-size:20px">{esc(cap)}{na}</div>'
    slide(body, s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


# ---------------------------------------------------------------- tipos de slide
def render_cover(s):
    blocos = "".join(f'<div class="dc"><b>{esc(b["label"])}</b><p>{rich(b["text"])}</p></div>' for b in s.get("blocks", []))
    slide(
        '<div class="rings"><i class="r1"></i><i class="r2"></i><i class="r3"></i></div>'
        f'<div class="kicker mint" style="top:130px">{esc(s.get("kicker", ""))}</div>'
        f'<h1 class="ctitle">{esc(s["title"])}</h1>'
        f'<p class="csub">{rich(s.get("subtitle", ""))}</p>'
        f'<div class="dcs">{blocos}</div>'
        f'<div class="cfoot">{esc(s.get("footer", META.get("rodape_capa", "")))}</div>',
        bg="cover", page=False, notas=s.get("notas"),
    )


def render_kpis(s):
    sd = s.get("side", {})
    grid = "".join(
        card(f'<div class="big">{esc(i["value"])}</div><div class="ct">{esc(i["title"])}</div><div class="cs">{esc(i.get("sub", ""))}</div>')
        for i in s["items"][:4]
    )
    side = (
        '<div class="card dark side" style="left:128px;top:281px;width:736px;height:640px">'
        f'<div class="mini">{esc(sd.get("mini", ""))}</div><h2>{rich(sd.get("title", ""))}</h2><p>{rich(sd.get("text", ""))}</p></div>'
        if sd else ""
    )
    left = 896 if sd else 128
    width = 896 if sd else 1664
    slide(side + f'<div class="g22" style="left:{left}px;top:281px;width:{width}px;height:640px">{grid}</div>',
          s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_diagram(s):
    boxes = [box(b["x"], b["y"], b["w"], b["h"], b["title"], b.get("sub", ""), b.get("kind", "plain"), b.get("num"), b.get("extra", "")) for b in s.get("boxes", [])]
    body = free_elements({"groups": s.get("groups", [])}) + diagram_svg(boxes, s.get("arrows", []))
    rest = {k: v for k, v in s.items() if k != "groups"}
    body += free_elements(rest)
    slide(body, s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_flow(s):
    lanes = s["lanes"]
    y = 275
    boxes, arrows, extras = [], [], ""
    for ln in lanes:
        steps = ln["steps"]
        n = len(steps)
        has_num = any(st.get("num") for st in steps)
        bh = ln.get("box_h", 180 if has_num else 110)
        tags = any(st.get("tag") for st in steps)
        brks = ln.get("brackets", [])
        lh = 62 + bh + (56 if tags else 0) + (66 if brks else 0) + 14
        lh = ln.get("h", lh)
        extras += f'<div class="lane" style="left:128px;top:{y}px;width:1664px;height:{lh}px"></div>' + mini(ln.get("label", ""), 150, y + 18)
        w = min(340, int((1620 - 44 * (n - 1)) / n))
        gap = (1620 - n * w) / (n - 1) if n > 1 else 0
        top = y + 62
        for i, st in enumerate(steps):
            x = int(150 + i * (w + gap))
            boxes.append(box(x, top, w, bh, st["title"], st.get("sub", ""), st.get("kind", "plain"), st.get("num"), "sm" if not has_num else ""))
            if i < n - 1:
                arrows.append(dict(pts=[(x + w, top + bh // 2), (int(x + w + gap), top + bh // 2)]))
            if st.get("tag"):
                tone = st.get("tag_tone", "wk" if st.get("tag_kind") == "sistema" else "op")
                extras += f'<div class="pill {tone}" style="left:{x + w // 2 - 70}px;top:{top + bh + 10}px;width:140px;padding:0">{esc(st["tag"])}</div>'
        for b in brks:
            x0 = int(150 + b["from"] * (w + gap))
            x1 = int(150 + b["to"] * (w + gap) + w)
            by = top + bh + (56 if tags else 12)
            dsh = " dsh" if b.get("dashed") else ""
            extras += (
                f'<div class="brk{dsh}" style="left:{x0}px;top:{by}px;width:{x1 - x0}px;height:14px;border-top:0;border-bottom:3px solid #1D5C63"></div>'
                f'<div class="brk-t" style="left:{x0}px;top:{by + 20}px;width:{x1 - x0}px">{esc(b["text"])}</div>'
            )
        y += lh + 26
    foot = ""
    cards = s.get("foot_cards", [])
    if cards:
        cw = (1664 - 24 * (len(cards) - 1)) // len(cards)
        for i, c in enumerate(cards):
            dark = " dark" if c.get("dark") else ""
            col = "color:#E6F0F0;" if c.get("dark") else ""
            foot += (
                f'<div class="card{dark}" style="left:{128 + i * (cw + 24)}px;top:{y}px;width:{cw}px;height:102px;padding:20px 30px;display:flex;align-items:center">'
                f'<p class="pp" style="{col}font-size:26px">{rich(c["text"])}</p></div>'
            )
    if s.get("band"):
        foot += f'<div class="card dark band" style="left:128px;top:{y}px;width:1664px;height:104px"><p>{rich(s["band"])}</p></div>'
    if s.get("note"):
        foot += f'<div class="note" style="left:128px;top:{y + 120}px;width:1664px">{rich(s["note"])}</div>'
    slide(extras + diagram_svg(boxes, arrows) + foot, s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_table(s, cls="mid", widths=None):
    t = table(s["headers"], [[rich(c) for c in r] for r in s["rows"]], s.get("widths", widths), s.get("hl"), s.get("cls", cls))
    foot = f'<div class="foot2" style="top:{s.get("foot_y", 928)}px">{rich(s["foot"])}</div>' if s.get("foot") else ""
    slide(f'<div style="position:absolute;left:128px;top:{s.get("top", 281)}px;width:1664px">{t}</div>{foot}',
          s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_risks(s):
    s = dict(s)
    s.setdefault("headers", ["Restrição atual", "Impacto", "Mitigação", "Caminho de evolução"])
    s.setdefault("widths", ["26%", "19%", "30%", "25%"])
    s.setdefault("bg", "alt")
    s.setdefault("top", 268)
    render_table(s, "risk rk")


def render_asks(s):
    s = dict(s)
    s.setdefault("headers", ["Ponto", "O que pedimos ao cliente", "Quem decide", "Prazo proposto"])
    s.setdefault("widths", ["22%", "44%", "12%", "22%"])
    s.setdefault("top", 281)
    render_table(s, "risk rk")


def render_stack(s):
    rows = []
    for r in s["rows"]:
        if r.get("slug"):
            c = RADAR[r["slug"]]
            ch = next(a for a in c["alternativas"] if a.get("escolhida"))
            outros = [a for a in c["alternativas"] if not a.get("escolhida")]
            best = max(outros, key=lambda a: c["_medias"][a["nome"]])
            alt = f'{esc(r.get("melhor", best["nome"]))} {fmt(c["_medias"][best["nome"]])}'
            media = fmt(c["_medias"][ch["nome"]])
            sp = fmt(c["_sem_prec"][ch["nome"]])
        else:
            alt, media, sp = esc(r.get("melhor", "n/a")), esc(r.get("media", "n/a")), esc(r.get("sem_precedente", "n/a"))
        rows.append((esc(r["camada"]), esc(r["escolha"]), alt, media, sp, esc(r.get("precedente", ""))))
    trs = "".join(
        f'<tr><td><b>{c}</b></td><td>{e}</td><td class="alt">{a}</td><td class="n">{m}</td><td class="n">{sp}</td><td>{p}</td></tr>'
        for c, e, a, m, sp, p in rows
    )
    t = (
        '<table class="tbl stk"><colgroup><col style="width:17%"><col style="width:24%"><col style="width:22%"><col style="width:8%"><col style="width:14%"><col style="width:15%"></colgroup>'
        '<thead><tr><th>Camada</th><th>Escolha</th><th>Melhor alternativa avaliada</th><th class="n">Média</th><th class="n">Sem precedente</th><th>Precedente</th></tr></thead>'
        f"<tbody>{trs}</tbody></table>"
    )
    foot = rich(s.get("foot", "n/a: critérios sem evidência ficam fora da média. Precedente: peça menos frequente em stacks compostas."))
    slide(f'<div style="position:absolute;left:128px;top:268px;width:1664px">{t}</div><div class="foot2" style="top:940px">{foot}</div>',
          s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_cards(s):
    items = s["items"]
    n = len(items)
    if n > 6:
        sys.exit("slide cards: no máximo 6 cartões")
    cls = "g6" if n == 6 else "g5"
    cols = f"grid-template-columns:repeat({3 if n == 6 else n},1fr);"
    h = s.get("h", {2: 300, 3: 320, 4: 340, 5: 390, 6: 560}[n] if n >= 2 else 320)
    inner = ""
    for it in items:
        sl = seal(it["seal"]) if it.get("seal") else ""
        num = f'<div class="num">{esc(it["num"])}</div>' if it.get("num") else ""
        if n == 6:
            inner += card(f'{num}<h3>{rich(it["title"])}</h3><p>{rich(it["text"])}</p>' + (f'<div style="margin-top:auto;padding-top:14px">{sl}</div>' if sl else ""))
        else:
            inner += card(f'{num}{sl}<h3>{rich(it["title"])}</h3><p>{rich(it["text"])}</p>')
    body = f'<div class="{cls}" style="left:128px;top:281px;width:1664px;height:{h}px;{cols}">{inner}</div>'
    y = 281 + h + 34
    if s.get("strip_label"):  # texto curto acima da faixa
        body += mini(s["strip_label"], 128, y)
        y += 36
    if s.get("strip"):
        st = dict(s["strip"], x=128, y=y)
        body += strip_html(st)
        y += 90
    if s.get("band"):
        body += f'<div class="card dark band" style="left:128px;top:{y}px;width:1664px;height:112px"><p>{rich(s["band"])}</p></div>'
        y += 140
    if s.get("note"):
        body += f'<div class="note" style="left:128px;top:{y}px;width:1664px">{rich(s["note"])}</div>'
    slide(body, s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_matrix(s):
    cols = s["columns"][:4]
    n = len(cols)
    gap = 24
    w = int((1664 - gap * (n - 1)) / n)
    body = ""
    for i, k in enumerate(s.get("kpis", [])):
        body += f'<div class="kpi" style="left:{128 + i * 432}px;top:290px"><b>{esc(k["value"])}</b><span>{rich(k["label"])}</span></div>'
    for i, c in enumerate(cols):
        x = 128 + i * (w + gap)
        body += (
            f'<div class="hc" style="left:{x}px;top:390px;width:{w}px"><div class="hd">{esc(c["title"])}</div>'
            f'<div class="hoje"><div class="tg">Hoje</div><p>{rich(c["hoje"])}</p></div>'
            f'<div class="evo"><div class="tg">Evolução</div><p>{rich(c["evolucao"])}</p></div></div>'
        )
    for j, nt in enumerate(s.get("notes", [])):
        body += f'<div class="note" style="left:128px;top:{876 + 38 * j}px;width:1664px">{rich(nt)}</div>'
    slide(body, s.get("bg", "light"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_timeline(s):
    tl = ""
    items = s["items"]
    for i, m in enumerate(items):
        last = i % 4 == 3 or i == len(items) - 1
        line = "" if last else '<i class="ln"></i>'
        tag = f'<div class="tagd">{esc(m.get("tag", "Dependência externa"))}</div>' if m.get("dep") else ""
        tl += f'<div class="mile"><div class="dr"><i class="dt"></i>{line}</div><div class="md">{esc(m["date"])}</div><h3>{rich(m["title"])}</h3><p>{rich(m.get("text", ""))}</p>{tag}</div>'
    body = f'<div class="tl" style="left:128px;top:285px;width:1664px">{tl}</div>'
    if s.get("callout"):
        body += f'<div class="callout solo" style="left:128px;top:{s.get("callout_y", 860)}px;width:1664px">{rich(s["callout"])}</div>'
    slide(body, s.get("bg", "dark"), s.get("kicker"), s["title"], notas=s.get("notas"))


def render_closing(s):
    d = "".join(f'<div class="dc"><b>{esc(x["date"])}</b><p>{rich(x["text"])}</p></div>' for x in s.get("dates", []))
    slide(
        '<div class="ring29"></div>'
        f'<div class="kicker mint" style="top:130px">{esc(s.get("kicker", "ENCERRAMENTO"))}</div>'
        f'<h1 class="etitle">{esc(s["title"])}</h1>'
        f'<div class="dcs">{d}</div>'
        f'<div class="foot"><span>{esc(META.get("rodape_capa", META["rodape"]))}</span><span>{len(SLIDES) + 1:02d}</span></div>',
        bg="cover end", page=False, notas=s.get("notas"),
    )


RENDER = {
    "cover": render_cover, "kpis": render_kpis, "diagram": render_diagram, "flow": render_flow, "radar": render_radar,
    "stack": render_stack, "table": render_table, "cards": render_cards, "matrix-hoje-evolucao": render_matrix,
    "timeline": render_timeline, "risks": render_risks, "asks": render_asks, "closing": render_closing,
}


# ---------------------------------------------------------------- saída
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("--content", default="conteudo-deck.json")
    ap.add_argument("--radar", default="radar-data.json")
    a = ap.parse_args()
    wd = os.path.abspath(a.workdir)
    deck = json.load(open(os.path.join(wd, a.content), encoding="utf-8"))
    META.update(deck["meta"])
    META.setdefault("radar_prefix", "radar")
    META.setdefault("rodape", META.get("sistema", "") + " · Arquitetura")
    rp = os.path.join(wd, a.radar)
    if os.path.exists(rp):
        try:
            RADAR.update(rc.analisar(rc.carregar(rp)))
        except ValueError as e:
            sys.exit("radar-data inválido:\n" + str(e))
    for i, s in enumerate(deck["slides"], 1):
        t = s.get("type")
        if t not in RENDER:
            sys.exit(f"slide {i}: tipo '{t}' desconhecido ({', '.join(RENDER)})")
        try:
            RENDER[t](s)
        except KeyError as e:
            sys.exit(f"slide {i} ({t}): campo obrigatório ausente: {e}")

    css = open(os.path.join(SKILL, "assets", "deck.css"), encoding="utf-8").read()
    fonts = open(os.path.join(SKILL, "assets", "fonts.css"), encoding="utf-8").read().replace("url(fonts/", "url(assets/fonts/")
    os.makedirs(os.path.join(wd, "assets"), exist_ok=True)
    dst = os.path.join(wd, "assets", "fonts")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(SKILL, "assets", "fonts"), dst)
    defs = (
        '<svg width="0" height="0" style="position:absolute"><defs>'
        '<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#12404A"/></marker>'
        '<marker id="ahd" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#5E7A80"/></marker>'
        "</defs></svg>"
    )
    check = (
        "<script>document.fonts.ready.then(function(){var bad=[];document.querySelectorAll('section.slide').forEach(function(s){"
        "var sr=s.getBoundingClientRect(),n=s.dataset.n;"
        "s.querySelectorAll('*').forEach(function(e){if(e.closest('svg'))return;var r=e.getBoundingClientRect();if(r.width===0&&r.height===0)return;"
        "if(r.right>sr.right+2||r.bottom>sr.bottom+2||r.left<sr.left-2)bad.push(n+':fora-do-slide:'+(e.className||e.tagName));"
        "else if(e.matches('table.tbl,.card,.bx,.band,.note,.foot2,.strip,.rcard,.na,.legend,.hc,.tl,.callout,.lane')&&!e.closest('.foot')&&(r.bottom-sr.top)>982)bad.push(n+':invade-rodape:'+(e.className||e.tagName));});"
        "var t=s.querySelector('h1.title');if(t&&t.scrollWidth>t.clientWidth+2)bad.push(n+':titulo-largo');"
        "s.querySelectorAll('.bx,.card,.hc div,.pill,.ch').forEach(function(e){if(e.scrollHeight>e.clientHeight+3||e.scrollWidth>e.clientWidth+3)bad.push(n+':transborda:'+e.className);});});"
        "document.body.setAttribute('data-overflow',bad.join('|'));});</script>"
    )
    doc = (
        f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=1920">'
        f'<title>{esc(META.get("titulo_html", META.get("sistema", "Arquitetura")))}</title>'
        f"<style>{fonts}\n{css}</style></head><body>{defs}" + "\n".join(SLIDES) + check + "</body></html>"
    )
    open(os.path.join(wd, "deck.html"), "w", encoding="utf-8").write(doc)

    notes = []
    for s, ov in zip(SLIDES, NOTES_OVERRIDE):
        if ov:
            notes.append(ov)
            continue
        t = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S)
        t = re.sub(r"<(br|/p|/h\d|/div|/tr|/li)[^>]*>", "\n", t)
        t = re.sub(r"</t[dh]>", " | ", t)
        t = re.sub(r"<[^>]+>", " ", t)
        t = html.unescape(t)
        lines = [re.sub(r"[ \t]+", " ", l).strip() for l in t.split("\n")]
        notes.append("\n".join(l for l in lines if l))
    json.dump(notes, open(os.path.join(wd, "assets", "notes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(SLIDES)} slides")


if __name__ == "__main__":
    main()
