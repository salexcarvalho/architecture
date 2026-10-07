---
name: architecture-publish
description: Publica a arquitetura decidida como wiki LIMPA para o cliente (3 páginas padrão com gráficos radar) mais a delegação do deck de apresentação à skill `architecture-presentation`, mantendo decisões, riscos e perguntas só no repositório do sistema. Use quando o usuário disser "publicar arquitetura na wiki", "documentação para o cliente", "tecnologias avaliadas", "componentes", "banco de dados no padrão", "padrão das 3 páginas", "gráficos radar", "6-documentation", "publish architecture", "client-facing architecture docs". Deck/apresentação de arquitetura: use a skill architecture-presentation.
---

# architecture-publish — wiki limpa para o cliente (deck: architecture-presentation)

Padrão reutilizável: qualquer projeto gera o mesmo conjunto sem o usuário repetir os detalhes. Coordenação e validação rodam na SESSÃO PRINCIPAL; a escrita das páginas, gráficos e deck é delegada a subagentes (`sonnet`).

## Quando usar
- Fase `6-documentation` (ver skill `architecture`) com a arquitetura aprovada, ou pedido direto de publicar/atualizar a documentação do cliente.
- Pedido de "tecnologias avaliadas/componentes/banco de dados no padrão" ou de gráficos radar. Pedido de deck/"versão resumida"/apresentação: delegar à skill `architecture-presentation` (abaixo).
- Não usar para gerar o TO-BE (`architecture-generate`) nem para decidir tecnologia (`architecture-tech-evaluation`, `architecture-adr`).

## Pré-condições
1. `.architecture/state.md` lido; fase mínima `5-validation` DONE: ADRs relevantes `ACCEPTED` com Evidence. Se houver ADR `PROPOSED` que afeta uma das páginas, NÃO publicar como decidido: perguntar ao usuário ou marcar "a definir com <cliente>".
2. Fontes: `docs/architecture/**`, `.architecture/**`, `07-technology/evaluations/*`, código quando existir. Nada inventado: número sem fonte vira "a medir/definir".
3. Acesso ao repositório da wiki (Azure DevOps wiki = repo git). Se o sistema TEM legado: só documentar o legado com acesso à fonte dele.
4. Dados do cliente que o usuário não deu (nome do cliente/sistema, datas, siglas) → perguntar uma vez, em bloco.

## REGRA DE SEPARAÇÃO (obrigatória)

| Fica no repositório do sistema (interno) | Vai para a wiki (versão limpa, para o cliente) |
|---|---|
| `docs/architecture/**` e `.architecture/**`: ADRs, decisões (ADR-/DEC-/P-), riscos (R-), perguntas (Q-), hipóteses (A-), fatos (F-), requisitos com ID (RF/RNF/RES), pauta de refinamento, revisões | Arquitetura, tecnologias avaliadas, componentes, banco de dados, planejamento |
| Marcadores `[KNOWN ·]`, `[PROPOSAL ·]`, `[DECISION ·]`, selos PROPOSED/ACCEPTED | Nenhum ID (F/A/Q/R/P/RF/RNF/RES/TD/G/RV-NNN, ADR-, DEC-), nenhum PROPOSAL/DECISION/selo colorido |
| Páginas de decisões, mapa de riscos, perguntas abertas | NÃO existem na wiki. Pendências do cliente: seção "Pontos a definir com <cliente>" em linguagem simples (o quê, quem decide, prazo proposto) |
| Nomes de pessoas, custos, caminhos locais | Nunca na wiki nem no deck; responsáveis por PAPEL ou área |

Traduza: ADR aceito vira "Decisão de arquitetura"; restrição do cliente vira "Definida no projeto"; pergunta aberta vira "A definir com <cliente>"; adiado vira "Adiado até medir". Se a wiki ainda tem páginas internas de decisão/risco, mover o conteúdo para o repositório (`docs/architecture/06-decisions`, `.architecture/risks.md`, `open-questions.md`; pauta em `.architecture/`), sem apagar histórico, e remover os links da wiki.

## Estrutura da wiki (Azure DevOps: página `X.md` + pasta `X/` + `X/.order`)

`.order` = nomes das páginas da pasta, sem extensão, um por linha, SEM newline final. Pasta sem página-pai `.md` não aparece. Inserir o sistema em `Documentação/.order`.

**Sem legado** (sistema novo):
```
Documentação/<Sistema>.md                      (landing: wiki-landing-sistema.md)
Documentação/<Sistema>/.order                  Arquitetura, Tecnologias-Avaliadas, Componentes, Banco-de-Dados, Planejamento
Documentação/<Sistema>/Arquitetura.md          (índice + Páginas desta seção + Ver também)
Documentação/<Sistema>/Arquitetura/01..11-*.md Visao-Sistemica, Dominios-e-Modulos, Componentes-Tecnicos, Modelo-de-Dados, APIs-e-Integracoes,
                                               Seguranca, Infraestrutura-e-Deploy, Fluxos-e-Diagramas, Radar-Arquitetural,
                                               Pontos-a-Definir (no lugar de Riscos), Glossario
Documentação/<Sistema>/{Tecnologias-Avaliadas,Componentes,Banco-de-Dados,Planejamento}.md
```
**Com legado** (reescrita/migração; modelo com legado):
```
Documentação/<Sistema>/Arquitetura/{Sistema-Atual-(legado), Nova-Arquitetura-da-API, Migração, Planejamento}.md  (+ pastas)
Documentação/<Sistema>/Arquitetura/Nova-Arquitetura-da-API.md   (página-pai: wiki-pagina-pai.md)
Documentação/<Sistema>/Arquitetura/Nova-Arquitetura-da-API/{Tecnologias-Avaliadas,Componentes,Banco-de-Dados}.md   .order = esses 3
```
NUNCA criar a página "Sistema-Atual-(legado)" (nem a de Migração) sem acesso à fonte/código do legado: registrar a pendência no repositório e seguir com a nova arquitetura.

Convenções de todas as páginas: sem H1, sem `[[_TOC_]]`, sem `---`; 1ª linha em negrito com ponto final; links absolutos sem `.md` (`/Documentação/<Sistema>/...`); mermaid só `::: mermaid` … `:::` (rótulos de nós sem acento); datas dd/mm/aaaa; tom tabular, denso, afirmativo; marcar "planejado", "a confirmar", "ainda não"; sem emoji (exceto ✅ na linha escolhida das notas); só nomes de variáveis, nunca valores; páginas-pai e landing terminam com `[[_TOSP_]]`.

## As 3 páginas padrão (exatamente o espec em `templates/padrao-3-paginas.md`)
Modelos: `templates/wiki-tecnologias-avaliadas.md`, `wiki-componentes.md`, `wiki-banco-de-dados.md`, `wiki-pagina-pai.md` (só com legado), `wiki-landing-sistema.md`. Cada modelo traz um comentário-guia inicial (remover ao publicar; `radar_charts.py --fill` remove sozinho).
- **Tecnologias-Avaliadas:** Contexto que condiciona as escolhas → Resumo das escolhas (`# | Camada | Escolha | Registro | Comparativo | Alternativas principais`) → Como ler os comparativos (faixas 9-10/7-8/5-6/3-4/0-2) → uma seção `## N. <Camada>` por camada (tabela de alternativas, Critérios/Motivo/Risco/Referência, `### Comparativo visual` com radar + tabela de notas + 2 linhas fixas) → Escolhas complementares → Como a comparação foi conduzida e o que ficou aberto.
- **Componentes:** diagrama `graph LR` → fluxo `sequenceDiagram` → catálogo → pipelines → configuração (só nomes) → contratos e limites da borda → estado de implementação → lacunas.
- **Banco-de-Dados:** números do baseline → schemas e o que não migra → papéis → tabelas por domínio → ER (`erDiagram`) por domínio → migrations → o que sai do banco → dados que migram → retenção/dados pessoais → backup → lacunas.
Dados vêm de `04-to-be/*`, `07-technology/*`, `08-security/*`, `09-operations/*` e dos ADRs ACCEPTED, traduzidos pela regra de separação.

## Gráficos radar (1 PNG por camada com comparativo)
1. Montar `radar-data.json` (modelo `templates/radar-data.example.json`): por camada `slug`, `titulo`, 3 a 5 `criterios`, 2 a 4 `alternativas` com `notas` 0–10 (mesma ordem dos critérios), exatamente 1 `escolhida`, `situacao`, `marcas` (índices de notas com † = avaliação da equipe, sem comparativo formal).
2. Escala 0–10: 10 = melhor para o sistema (em custo, esforço e nº de componentes, 10 = menor). As notas traduzem o comparativo/ADR registrado; não são medição. Tecnologia imposta pelo cliente é restrição: a média pode ficar abaixo da de uma descartada, e o texto explica.
3. Gerar: `radar_charts.py radar-data.json <wiki>/.attachments --prefix <sistema> --manifest manifest.json --sistema <SISTEMA> --fill tec.tpl.md --out <wiki>/Documentação/<Sistema>/Tecnologias-Avaliadas.md`. Arquivo `<sistema>-<slug>-<uuid4>.png` em `.attachments/`, referenciado `/.attachments/<arquivo>`; o manifest reaproveita os uuids em reexecuções (evita PNGs novos a cada rodada). Marcador `@@CMP:<slug>@@` no rascunho marca onde entra cada comparativo.
4. Estilo fixo (já no script): título "Comparação — <Camada>", anéis tracejados 2/4/6/8/10, legenda fora com "(escolhida)", escolhida azul traço 4, demais vermelho/verde/roxo.

## Apresentação (deck) — delegada à skill `architecture-presentation`
O deck ao cliente NÃO é mais montado aqui: usar `~/.claude/skills/architecture-presentation` (2 fases: REVISÃO com `REVISAO.md` + `radar-data.json`, depois PRODUÇÃO em HTML 1920x1080 -> PDF -> PPTX; até 20 slides; classificação FACT/DECISION/PROPOSAL/ASSUMPTION/RISK/OPEN QUESTION; verificação com `verify_deck.py`). O `radar-data.json` da skill nova é um superconjunto do desta (exige `justificativas` e `evidencias` por nota; `null` = NOT EVALUATED, que o `radar_charts.py` da wiki não aceita: para a wiki, usar só camadas totalmente avaliadas). Saída: `docs/apresentacoes/<cliente-vN>/`. Wiki e deck devem repetir os mesmos números e nomes. (`scripts/build_deck.py` e `templates/deck-conteudo.example.json` desta skill ficam como legado de um deck simples de ~13 slides, sem a fase de revisão.)

## Verificação obrigatória (antes de qualquer commit)
`verify_wiki.py <worktree-da-wiki> Documentação/<Sistema> --prefix <sistema> --deny <nomes de pessoas, custos, siglas internas>` deve sair com 0 problemas. Ele cobre: links e imagens existentes, `.order` exato, mermaid `::: mermaid` balanceado, tabelas com colunas consistentes, formato das páginas padrão, IDs internos = 0, sem caminhos locais, sem "Claude"/"Anthropic", sem links para decisões/riscos. Complementar:
- `grep -rniE 'claude|anthropic|/home/|/tmp/' <páginas>` = 0; deck: `architecture-presentation/scripts/verify_deck.py` = 0 problemas.
- Páginas novas renderizadas na wiki quando houver acesso (mermaid, imagens); avisos de PNG órfão tratados.
- Memória interna atualizada: o que saiu da wiki existe no repositório (`docs/architecture`, `.architecture`).

## Publicação git (wiki)
1. `git fetch` e criar WORKTREE limpa a partir de `origin/<branch da wiki>` (`git worktree add <dir> origin/<branch>`); NUNCA mexer no checkout local do usuário nem descartar alterações locais dele (`reset --hard`, `checkout .`, `clean`, stash sem tag proibidos).
2. Gerar/atualizar páginas, `.attachments/`, `.order`; rodar a verificação.
3. Commit em pt-BR, imperativo, sem atribuição ("Claude", Co-Authored-By, "Generated with") em mensagem ou corpo. Revisar `git diff --stat` antes.
4. `git push` SOMENTE quando o usuário pedir. Sem pedido: parar no commit local e informar branch/hash.
5. Publicação por API do Azure DevOps só com pedido explícito; preferir git.

## Delegação (modelo `sonnet`; contexto mínimo: caminhos, não conteúdo)
Subagentes não herdam contexto e NÃO decidem: dúvida de arquitetura → `ESCALATION_REQUIRED`. Ondas:
1. **Paralelo (arquivos disjuntos):** (a) Tecnologias-Avaliadas + `radar-data.json` + PNGs; (b) Componentes; (c) Banco-de-Dados; (d) páginas de Arquitetura/landing/Planejamento; (e) deck: skill `architecture-presentation` (fases 1 e 2, em série entre si). 2. **Série:** `verify_wiki.py`, correção. 3. Commit na worktree.

Prompt-base (preencher `<...>`):
```
Tarefa: <página/arquivo a produzir>. Skill de referência: ~/.claude/skills/architecture-publish (leia SKILL.md, o modelo em templates/<arquivo> e templates/padrao-3-paginas.md).
Fontes (somente leitura): <caminhos em docs/architecture, .architecture, ADRs ACCEPTED>. Saída (únicos arquivos que pode escrever): <caminhos>.
Regras: versão LIMPA para o cliente: zero IDs (F/A/Q/R/P/RF/RNF/RES/TD/ADR/DEC), zero PROPOSAL/DECISION, zero link para decisões/riscos/perguntas, zero nomes de pessoas/custos/caminhos locais/"Claude". Pendências = "A definir com <cliente>". Sem H1/[[_TOC_]]/'---'. Links absolutos sem .md; mermaid só '::: mermaid'. Nada inventado: sem fonte = "a definir/medir".
Ferramentas: <venv com matplotlib/python-pptx>; scripts em ~/.claude/skills/architecture-publish/scripts.
Retorne ≤ 15 linhas: arquivos escritos, lacunas encontradas (sem fonte), ESCALATION_REQUIRED se houver decisão pendente.
```

## Saída
- Wiki limpa (worktree/commit local), deck (saída da skill `architecture-presentation`), `radar-data.json` (guardar no repositório do sistema, `docs/architecture/07-technology/`, para regerar), relatório da verificação.
- Mensagem ao usuário (≤ 10 linhas): páginas e imagens geradas, resultado da verificação, hash do commit, o que falta (pushes, pendências do cliente).

## Critério de conclusão
`verify_wiki.py` = 0 problemas; deck conforme `architecture-presentation` (verify_deck = 0); nenhuma decisão/risco/pergunta na wiki e todas preservadas no repositório; nada publicado (push) sem pedido; `state.md` atualizado (fase `6-documentation`, data, hash do commit da wiki).
