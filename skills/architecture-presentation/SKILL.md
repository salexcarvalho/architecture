---
name: architecture-presentation
description: Gera e revisa APRESENTAÇÕES DE ARQUITETURA ao cliente (deck executivo/técnico de até 20 slides, HTML 1920x1080 para PDF e PPTX) em duas fases obrigatórias, REVISÃO (REVISAO.md + radar-data.json) e PRODUÇÃO, com classificação de cada afirmação, matrizes com score/justificativa/evidência e verificação mecânica e visual. Reutilizável em qualquer projeto. Use quando o usuário disser "apresentação de arquitetura", "deck para o cliente", "revisar apresentação", "slides da arquitetura", "versão executiva", "versão técnica da apresentação", "apresentação ao cliente", "deck de arquitetura", "client architecture deck", "review architecture presentation".
---

# architecture-presentation — apresentação de arquitetura ao cliente (2 fases)

Substitui e aprimora a parte de deck da skill `architecture-publish` (que cobre a wiki limpa e delega o deck para cá). Coordenação, decisões e conferência rodam na SESSÃO PRINCIPAL; leitura de fontes, análise, redação do JSON e renders são delegados a subagentes (`sonnet`).

## Quando usar
- Criar ou refazer o deck de arquitetura para o cliente, versão executiva ou técnica; revisar um deck existente.
- Não usar para gerar o TO-BE (`architecture-generate`), decidir tecnologia (`architecture-tech-evaluation`, `architecture-adr`) nem para a wiki (`architecture-publish`).

## Pré-condições
1. `.architecture/state.md` lido; ADRs relevantes `ACCEPTED` com Evidence (fase mínima `5-validation`). ADR `PROPOSED` NÃO vira afirmação definitiva: entra como "Proposta" ou "A definir com o cliente".
2. Fontes: `.architecture/**`, `docs/architecture/**` (to-be, diagramas, `07-technology/evaluations`, riscos, perguntas), inventário de projetos/manifests quando existir, wiki publicada, deck anterior. Número sem fonte = "a medir/definir"; nada inventado.
3. Dados do cliente que o usuário não deu (nome do cliente/sistema, mês/ano, papéis dos donos dos pedidos) → perguntar uma vez, em bloco.
4. Ferramentas: `google-chrome`, `pdftoppm`/`pdfinfo` (poppler) e um venv com `python-pptx` e `matplotlib` NO SCRATCHPAD (nunca instalar global): `python3 -m venv <scratchpad>/venv && <venv>/bin/pip install python-pptx matplotlib`. Exportar `ARCH_DECK_VENV=<venv>`.

## REGRAS (valem para as duas fases)

**Forma**
1. Máx. 20 slides. Executiva e técnica ao mesmo tempo: o título e o visual dizem a mensagem; o detalhe técnico vai em diagrama/tabela e nas notas do apresentador.
2. Uma pergunta por slide; título-AFIRMAÇÃO (≥ 4 palavras, ≤ 56 caracteres, 1 linha, sem "Nome: explicação"); no máx. 3 mensagens curtas.
3. Diagramas, fluxogramas e indicadores; nunca "documento projetado" (parágrafo corrido, tabela de 15 linhas de prosa). Incluir os 2–3 fluxogramas principais do sistema.
4. Sem IDs internos (F/A/Q/R/P/RF/RNF/RES/TD/G/RV-NNN, ADR-, DEC-), sem custos, sem nomes de pessoas (papéis/áreas), sem caminhos locais, sem menção a ferramenta de IA. Fontes internas ficam no REVISAO.md.
5. Tom de domínio técnico e governança; expressões de `templates/termos-banidos.txt` são proibidas (monólito modular, "robusto", "de ponta", promessas absolutas, "equipe sem experiência", etc.).

**Conteúdo**
6. Classificar CADA afirmação: FACT · DECISION · PROPOSAL · ASSUMPTION · RISK · OPEN QUESTION (`templates/checklist-classificacao.md`). Só FACT e decisão aprovada são definitivas; o resto leva selo/linguagem de proposta, hipótese, risco ou pendência.
7. Não ocultar riscos reais. Limitação real = Restrição atual / Impacto / Mitigação / Caminho de evolução. Negativa sem evidência é removida (ou NOT EVALUATED).
8. Nunca pontuar baixo "experiência da equipe" sem evidência: usar "Precedente na organização" com régua única (mesma para todas as alternativas); sem evidência = NOT EVALUATED, fora da média e listado como n/a. Capacidade interna declarada pelo usuário = evidência `U`, só no que foi declarado.
9. Matrizes com SCORE + JUSTIFICATION + EVIDENCE por critério e alternativa. Nenhuma alternativa é rebaixada para justificar outra. Restrição do cliente é filtro explícito, não nota baixa.
10. Banco: separar MOTOR (decisão a) de HOSPEDAGEM (decisão b).
11. Segurança: separar RBAC, autenticação, autorização, segurança da aplicação, segurança do banco e auditoria (seis controles).
12. Não rotular a arquitetura ("monólito modular", "microsserviços"): mostrar camadas, LB → App/API 1..N → banco; escala horizontal da aplicação × vertical/HA do banco tratada à parte; diferenciar HOJE (decisão) × EVOLUÇÃO (capacidade, sem decisão).
13. Diferenciar escalabilidade, resiliência, alta disponibilidade e recuperação de desastres (cada uma com meta e prova exigida).
14. Valorizar padrões já adotados pela organização/cliente (coluna Precedente; "por que esta").

## FASE 1 — REVISÃO (obrigatória, antes de produzir qualquer slide)
Entradas: deck atual (se houver), fontes da pré-condição 2, pedidos do usuário. Saídas em `docs/apresentacoes/<cliente-vN>/`:
- `REVISAO.md` (modelo `templates/REVISAO.template.md`) com as 10 seções: 1 redundâncias · 2 afirmações não sustentadas · 3 negativas questionáveis · 4 matriz revisada · 5 banco (motor × hospedagem) · 6 experiência da equipe · 7 RBAC/segurança · 8 caracterização da arquitetura · 9 escalabilidade × resiliência × HA × DR · 10 nova estrutura ≤ 20 slides (tabela: nº, título-afirmação, pergunta, visual, fontes) + Anexo A (riscos) + Anexo B (pontos para o orquestrador decidir).
- `radar-data.json` (modelo `templates/radar-data.example.json`): por camada, critérios, alternativas, `notas` (null = NOT EVALUATED), `justificativas` e `evidencias` por critério, `regua_precedente`. Validar: `<venv>/bin/python ~/.claude/skills/architecture-presentation/scripts/radar_charts.py radar-data.json --check`.
Gate: apresentar ao usuário os pontos do Anexo B e as decisões que mudam o conteúdo (≤ 7 linhas); fato novo declarado vai para a memória via `architecture-context`. Só avançar com a estrutura aceita. Não inventar decisão: dúvida de arquitetura = `ESCALATION_REQUIRED`.

## FASE 2 — PRODUÇÃO
1. Escrever `conteudo-deck.json` a partir da seção 10 (modelo `templates/conteudo-deck.example.json`, 20 slides; tipos abaixo). `meta`: `sistema`, `cliente`, `rodape`, `rodape_capa`, `titulo_html`, `autor`, `arquivo_base`, `radar_prefix`. Campo `notas` do slide = notas do apresentador (senão sai o texto do slide); campos desconhecidos (ex. `fontes_internas`) são ignorados.
2. `ARCH_DECK_VENV=<venv> ~/.claude/skills/architecture-presentation/scripts/build.sh docs/apresentacoes/<cliente-vN>`: radares (PNG) → `deck.html` (1920x1080) → PDF (Chrome headless) → PNG por slide (`assets/slides/`) → PPTX (imagens + notas). O build avisa transbordo/texto cortado e título largo (`.overflow.txt`).
3. Verificação visual de TODOS os slides com Read (folhas de contato 2x3 para varredura + leitura individual dos densos: diagramas, tabelas, radares). Procurar: texto cortado, setas fora de lugar, sobreposição, tabela batendo no rodapé. Corrigir o JSON e repetir.
4. `python3 ~/.claude/skills/architecture-presentation/scripts/verify_deck.py <dir> --deny "<nomes de pessoas>" --deny "<siglas internas>"`: contagem ≤ 20 (HTML = PDF = PPTX), termos banidos, IDs internos, custos, caminhos locais, marcadores não preenchidos, títulos, `radar-data.json`, transbordo. Deve sair com 0 problemas.

Tipos de slide (`type`): `cover` (kicker, title, subtitle, blocks[label,text], footer) · `kpis` (side{mini,title,text}, items[value,title,sub] x4) · `diagram` (boxes[x,y,w,h,title,sub,kind plain|app|shared|evo|dark,num], arrows[pts,dashed,label,lx,ly,both], groups, minis, strips, notes, deps, cards, bands, pills, legend) · `flow` (lanes[label,steps[title,sub,kind,num,tag,tag_tone op|wk],brackets[from,to,text,dashed]], foot_cards[text,dark], band, note; geometria automática) · `radar` (slug ou slugs[2], why, strip{label,items,hi,chips,extra_dash}, head/heads) · `stack` (rows[slug?,camada,escolha,precedente]; média e melhor alternativa vêm do radar-data) · `table` (headers, rows, widths, cls) · `cards` (items[title,text,seal dec|capac|prop|hip|pend|risk,num] até 6, strip, band, note, h) · `matrix-hoje-evolucao` (kpis, columns[title,hoje,evolucao] x4, notes) · `timeline` (items[date,title,text,dep], callout) · `risks` (rows de 4 colunas) · `asks` (rows: ponto, pedido, quem decide, prazo) · `closing` (dates[date,text]). Texto aceita `**negrito**` e `\n`.

Estrutura-modelo (20): capa · contexto (indicadores) · arquitetura em camadas (LB → App/API 1..N → banco) · características (hoje × capacidade) · fluxograma 1 · fluxograma 2 · fluxograma 3 · stack avaliada · radares das decisões críticas (motor, hospedagem, jobs...) · modelo de dados · segurança em 6 controles · identidade e acesso · escalar × resistir × manter no ar × recuperar · ambientes e entrega · marcos · riscos · pedidos ao cliente · encerramento.

## Delegação (modelo `sonnet`; contexto mínimo: caminhos, não conteúdo; subagentes não herdam nada e NÃO decidem)
Fase 1 em paralelo (saídas disjuntas, sem editar fontes): (a) auditoria do deck atual → seções 1–3; (b) matriz → `radar-data.json` + seções 4–6; (c) segurança/arquitetura/capacidades → seções 7–9; a seção 10 e o Anexo B são montados pela sessão principal. Fase 2 em série: (d) `conteudo-deck.json` + build + leitura visual + verify; correções até limpo.

Prompt-base Fase 1 (preencher `<...>`):
```
Tarefa: <seções do REVISAO / radar-data.json>. Skill de referência: ~/.claude/skills/architecture-presentation (leia SKILL.md, templates/REVISAO.template.md e templates/checklist-classificacao.md).
Fontes (somente leitura): <deck atual, .architecture, docs/architecture, inventário>. Saída (únicos arquivos que pode escrever): <caminhos em docs/apresentacoes/<cliente-vN>/>.
Regras: classifique cada afirmação (FACT/DECISION/PROPOSAL/ASSUMPTION/RISK/OPEN QUESTION); sem evidência = NOT EVALUATED; nunca pontuar "experiência da equipe" (use precedente na organização com régua única); nenhuma alternativa rebaixada para justificar outra; cite a fonte de cada nota; nada inventado. Dúvida de arquitetura = ESCALATION_REQUIRED (Problema/Contexto/Arquivos/Alternativas/Impactos/Recomendação/Decisão necessária).
Retorne ≤ 12 linhas: arquivos, achados principais, lacunas, ESCALATION_REQUIRED se houver.
```
Prompt-base Fase 2:
```
Tarefa: produzir o deck de <sistema> a partir de <REVISAO.md seção 10> e <radar-data.json>. Skill: ~/.claude/skills/architecture-presentation (SKILL.md, templates/conteudo-deck.example.json).
Escreva só <dir>/conteudo-deck.json. Rode: ARCH_DECK_VENV=<venv> scripts/build.sh <dir>; leia TODOS os PNG de <dir>/assets/slides com Read; corrija e repita; rode scripts/verify_deck.py <dir> --deny <...> até 0 problemas.
Regras: ≤ 20 slides; título-afirmação ≤ 56 caracteres; diagrama/indicador por slide; zero IDs internos, custos, nomes de pessoas, caminhos locais; PROPOSAL/ASSUMPTION com selo; riscos como Restrição/Impacto/Mitigação/Evolução; hoje × evolução separados.
Retorne ≤ 10 linhas: arquivos, resultado do build e do verify, slides com ajuste visual pendente.
```

## Saída
`docs/apresentacoes/<cliente-vN>/` (N incrementa a cada rodada): `REVISAO.md`, `radar-data.json`, `conteudo-deck.json`, `<arquivo_base>.pdf`, `<arquivo_base>.pptx`, `deck.html`, `assets/` (regerável; `.venv` e `assets/` podem ir ao `.gitignore`). Salvar `REVISAO.md`, JSONs, PDF e PPTX; não versionar venv. Wiki e deck devem ter os mesmos números e nomes (`architecture-publish`).

## Checklist final
- [ ] Fase 1 feita: `REVISAO.md` com 10 seções e Anexo B resolvido; `radar-data.json` válido (`--check`).
- [ ] ≤ 20 slides (HTML = PDF = PPTX); `verify_deck.py` = 0 problemas; build sem aviso de transbordo.
- [ ] TODOS os slides lidos como imagem; nenhum texto cortado, seta fora de lugar ou tabela no rodapé.
- [ ] Cada afirmação classificada; só FACT e decisão aprovada como definitivas; riscos reais presentes; negativas com evidência.
- [ ] Matrizes com score + justificativa + evidência; precedente com régua única; NOT EVALUATED fora da média.
- [ ] Motor × hospedagem, seis controles de segurança, hoje × evolução e as quatro capacidades (escala, resiliência, HA, DR) separados.
- [ ] Sem IDs, custos, nomes de pessoas, caminhos locais, menção a ferramenta de IA; pedidos com papel e prazo.
- [ ] Nada publicado/enviado sem pedido do usuário; mensagem final ≤ 10 linhas (arquivos, contagem, verificação, pendências do cliente).
