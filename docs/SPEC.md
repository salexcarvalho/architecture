# SPEC — Framework global de Arquitetura (Claude Code)

Fonte: pedido do usuário (arquiteto). Este SPEC é a decisão de desenho do orquestrador; os arquivos gerados devem segui-lo à risca.
Idioma dos arquivos: português (rótulos de status em inglês: KNOWN, UNKNOWN, ASSUMPTION, PROPOSAL, DECISION, RISK, OPEN QUESTION; DRAFT/OPEN; PROPOSED/ACCEPTED/SUPERSEDED/REJECTED/DEPRECATED; ADOPT/TRIAL/ASSESS/HOLD/REJECT).
NENHUMA menção a projeto, cliente ou sistema específico nos arquivos globais. Exemplos genéricos apenas.

## 1. Restrições da plataforma que moldam o desenho
- Subagentes (tool Agent) NÃO conversam com o usuário: rodam, retornam um relatório e encerram. Não podem fazer entrevista interativa.
- Subagentes não devem disparar outros subagentes (aninhamento não é confiável/permitido).
- Portanto: coordenação e entrevista rodam na SESSÃO PRINCIPAL via skills; especialistas são subagentes que analisam e PROPÕEM (incluindo perguntas sugeridas), nunca decidem.

## 2. Análise crítica do desenho original (11 agentes → 6 subagentes + skills)
| Original | Destino | Motivo |
|---|---|---|
| architecture-orchestrator | skill `architecture` (+ `architecture-start`) na sessão principal | só a sessão principal fala com o usuário e delega; subagente orquestrador não conseguiria delegar nem entrevistar |
| requirements-interviewer | skill `architecture-interview` na sessão principal | entrevista exige diálogo; especialistas só sugerem perguntas |
| architecture-decision-manager | skill `architecture-adr` | trabalho de template + regra de estado; não precisa de contexto isolado |
| solution-architect + integration-api-architect | subagente `application-architect` | APIs/contratos/eventos são parte da arquitetura de aplicação; separados geravam sobreposição (filas, resiliência, comunicação) |
| infrastructure-architect + devops-architect | subagente `platform-architect` | ambientes, deploy, pipelines, backup e observabilidade operacional se sobrepunham |
| architecture-discovery | subagente `architecture-discovery` (mantido) | leitura em massa do repo, isolada, somente leitura |
| data-architect | subagente `data-architect` (mantido) | domínio próprio, CURRENT vs PROPOSED |
| security-privacy-architect | subagente `security-privacy-architect` (mantido) | revisão transversal com threat model/LGPD |
| architecture-reviewer | subagente `architecture-reviewer` (mantido) | independência: nunca revisa o que ele mesmo escreveu |
Resultado: 6 subagentes, 16 skills (1 de entrada + 15 especializadas).

## 3. Responsabilidades (sem sobreposição) e escrita
| Subagente | Escreve em | Lê | Nunca |
|---|---|---|---|
| architecture-discovery | `.architecture/known-facts.md` (seção discovery), `docs/architecture/03-as-is/{architecture,applications,integrations,data,infrastructure}.md` (stack, módulos, CI/CD, observabilidade e autenticação entram como seções destes 5; lacunas vão ao relatório → `.architecture/open-questions.md`/`assumptions.md` pela skill) | repo inteiro, git log | propor TO-BE; julgar se está certo |
| application-architect | `04-to-be/{architecture,applications,integrations}.md`, `05-diagrams/{context,container,component}.md`, `05-diagrams/flows/*` | memória, AS-IS, requisitos | decidir; tocar dados/infra/segurança além de interfaces |
| data-architect | `03-as-is/data.md` (complemento), `04-to-be/data.md` (CURRENT DATA MODEL vs PROPOSED DATA MODEL) | migrations, schema, ORM, memória | fechar modelo sem evidência; marcar não confirmado como decisão (usar DRAFT/PROPOSAL/OPEN) |
| platform-architect | `04-to-be/{infrastructure,observability,deployment}.md`, `05-diagrams/deployment.md`, `09-operations/{environments,observability,backup-restore,disaster-recovery,runbooks}.md` | Docker, CI/CD, IaC, envs (só nomes de variáveis) | introduzir complexidade (ex.: Kubernetes) sem justificativa registrada; ler valores de segredos |
| security-privacy-architect | `04-to-be/security.md`, `08-security/{threat-model,privacy-lgpd,security-baseline}.md` (riscos → `.architecture/risks.md` via relatório) | tudo | expor segredos; afirmar conformidade LGPD sem evidência |
| architecture-reviewer | `.architecture/reviews/REVIEW-<AAAA-MM-DD>.md` | tudo | editar documentos revisados (só aponta) |
Todos os especialistas: ao final retornam (a) o que escreveram, (b) itens novos para memória com Status+Source, (c) até 7 perguntas sugeridas priorizadas por impacto, (d) propostas de ADR. Nenhum escreve em `06-decisions/` (só a skill `architecture-adr`) nem marca ACCEPTED. IDs novos nos retornos e documentos são provisórios (`P-novo-1`, `Q-novo-1`, ...) e renumerados pela skill que delegou (ver §6). Exceção de escrita: no modo avaliação de tecnologia (acionado por `architecture-tech-evaluation`) o especialista pode escrever `07-technology/evaluations/<tecnologia>.md`.
Quem delega: só a sessão principal (skills). Subagentes não delegam.

### 3.1 Árvore de `docs/architecture/` (definida pelo usuário; prevalece sobre qualquer outra menção)
```
docs/architecture/
README.md
01-context/{project-context.md, stakeholders.md, glossary.md, assumptions.md}
02-requirements/{functional.md, non-functional.md, constraints.md, open-questions.md}
03-as-is/{architecture.md, applications.md, integrations.md, data.md, infrastructure.md}
04-to-be/{architecture.md, applications.md, integrations.md, data.md, infrastructure.md, security.md, observability.md, deployment.md}
05-diagrams/{context.md, container.md, component.md, deployment.md, flows/}
06-decisions/ADR-NNN-*.md
07-technology/{technology-radar.md, evaluations/}
08-security/{threat-model.md, privacy-lgpd.md, security-baseline.md}
09-operations/{environments.md, observability.md, backup-restore.md, disaster-recovery.md, runbooks.md}
10-roadmap/{architecture-roadmap.md, technical-debt.md}
```
Regras da árvore: nenhum arquivo ou pasta fora dela (nomes próprios dos autores originais foram mapeados para estes arquivos); só nascem arquivos com conteúdo verificado; `.architecture/` (memória) fica fora de `docs/` e prevalece sobre as projeções `01-context/assumptions.md` e `02-requirements/open-questions.md`. Dono de cada arquivo: tabela do §3 (e `architecture-context` para 01 e 02; `architecture-adr` para 06; `architecture-tech-evaluation` para 07; `architecture-gap-analysis` para 10).


## 4. Skills e dono
| Skill | Executa | Delega para |
|---|---|---|
| `architecture` | ponto de entrada: lê `.architecture/state.md`, decide a fase e chama a skill certa | — |
| `architecture-start` | inicializa `.architecture/` (se não existir), roda discovery, monta primeiro bloco de perguntas | architecture-discovery |
| `architecture-context` | atualiza memória (context, known-facts, assumptions, open-questions, risks) com respostas/fatos do usuário; na fase 3 escreve `01-context/{project-context,stakeholders,glossary,assumptions}.md` e `02-requirements/{functional,non-functional,constraints,open-questions}.md` (os dois `assumptions`/`open-questions` são projeções da memória) | — |
| `architecture-discover` | (re)descobre AS-IS | architecture-discovery |
| `architecture-interview` | entrevista question-first (blocos 3–7), registra respostas | — (usa sugestões dos especialistas) |
| `architecture-generate` | produz/atualiza TO-BE completo, em ordem | application, data, platform, security (paralelo quando independente) + reviewer |
| `architecture-api` | APIs e integrações | application-architect |
| `architecture-data` | dados | data-architect |
| `architecture-infrastructure` | infra | platform-architect |
| `architecture-devops` | CI/CD, ambientes, releases | platform-architect |
| `architecture-security` | segurança e LGPD | security-privacy-architect |
| `architecture-adr` | cria/atualiza ADR, controla status | — |
| `architecture-tech-evaluation` | avaliação de tecnologia (template seção 7) | especialista do domínio, opcional |
| `architecture-review` | revisão independente | architecture-reviewer |
| `architecture-gap-analysis` | AS-IS × TO-BE → `10-roadmap/{architecture-roadmap,technical-debt}.md` | — (lê docs) |
| `architecture-update` | doc viva: detecta impacto de mudança (git diff/log desde a última revisão registrada em state.md), atualiza docs, propõe ADR, atualiza diagramas, chama review | especialista do domínio + reviewer |

## 5. Fluxo
DESCOBRIR → LER → CONHECIDO → LACUNAS → PERGUNTAR → REGISTRAR → ALTERNATIVAS → PROPOR → VALIDAR COM USUÁRIO → DOCUMENTAR → REVISAR → EVOLUIR.
Fases em `.architecture/state.md`: `0-init`, `1-discovery`, `2-interview`, `3-requirements`, `4-proposal`, `5-validation`, `6-documentation`, `7-review`, `8-evolution`.
Gate de pergunta (antes de qualquer documento relevante): checklist de informações mínimas por documento; se faltar item de alto impacto → entrevista primeiro.
Regra de busca antes de perguntar (OBRIGATÓRIA): procurar em docker-compose, .env.example, manifests de pacote, migrations, código, docs, CI. Se achar, não perguntar existência; perguntar algo de maior valor citando o achado ("Identifiquei X em <arquivo>. ...?").

## 6. Memória do projeto: `.architecture/` (versionada no repo do projeto; sem segredos)
- `state.md` — fase atual, última execução por skill, último commit revisado, próximos passos.
- `context.md` — resumo do sistema (1 página).
- `known-facts.md` — tabela: ID (F-001), fato, Status (KNOWN), Source (repository|documentation|user|runtime), evidência (arquivo:linha / data da resposta).
- `assumptions.md` — A-001: hipótese, Source (inferred|architectural analysis), motivo, como validar, status (OPEN|CONFIRMED→vira fato|REJECTED).
- `open-questions.md` — Q-001: pergunta, por que importa (impacto), bloqueia o quê, prioridade (alta/média/baixa), rodada, status (OPEN|ANSWERED|DEFERRED), resposta + data.
- `decisions.md` — índice de ADRs (id, título, status, data) + propostas ainda sem ADR (P-001).
- `risks.md` — R-001: risco, probabilidade, impacto, mitigação, dono, status.
- `interview-log.md` — rodadas: data, perguntas, respostas literais resumidas, itens de memória gerados.
- `reviews/` — relatórios do reviewer.
IDs provisórios: subagentes escrevem item novo como `<TIPO>-novo-<n>` (`F-novo-1`, `A-novo-1`, `Q-novo-1`, `P-novo-1`, `R-novo-1`) e não escrevem em `decisions/open-questions/assumptions/risks`; a skill que delegou atribui os IDs finais, registra o item na memória e substitui, arquivo por arquivo, todas as ocorrências nos documentos (verificação: `grep -rn 'novo-' docs/architecture .architecture` = 0). Exceção: `architecture-discovery` escreve a seção discovery de `known-facts.md` com `F-NNN` finais (faixas disjuntas em execuções paralelas). IDs locais a documento (RNF/RF/RES, G/TD, RV) são numerados pelo autor.
Regras: inferido nunca vira KNOWN; PROPOSAL só vira DECISION com evidência de aprovação (resposta do usuário registrada com data, ou ADR ACCEPTED); todo item com Source.

## 7. Templates
Pasta `~/.claude/skills/architecture/templates/` (a skill `architecture` e as demais referenciam por caminho relativo à skill `architecture`; replicar onde necessário NÃO — use referência ao caminho absoluto `~/.claude/skills/architecture/templates/<arquivo>`):
- memória: state.md, context.md, known-facts.md, assumptions.md, open-questions.md, decisions.md, risks.md, interview-log.md
- docs: README.md (índice de docs/architecture, com legenda de status), doc-section.md (cabeçalho padrão: Status do documento DRAFT|REVIEWED|APPROVED, última atualização, fontes, itens KNOWN/ASSUMPTION/PROPOSAL/OPEN no corpo marcados inline com `[KNOWN · F-003]`, `[PROPOSAL · P-002]`, `[OPEN · Q-007]`), as-is.md (reúne as seções dos 5 arquivos de `03-as-is/`; cada seção indica o arquivo de destino), to-be.md, data-model.md (CURRENT vs PROPOSED, entidades com status DRAFT/PROPOSAL/OPEN), non-functional.md (RNF com métrica, alvo, fonte), constraints.md, functional.md, threat-model.md (STRIDE leve), security-baseline.md, privacy-lgpd.md (checklist LGPD com evidência), environments.md, backup-restore.md (RPO/RTO, testes), disaster-recovery.md, runbooks.md (um arquivo, uma seção por cenário), technology-radar.md, tech-evaluation.md, adr.md, review-report.md, architecture-roadmap.md, technical-debt.md, diagrams.md (Mermaid C4: C4Context, C4Container, C4Component, deployment, sequence, flowchart de dados/integração — com nota "derivado de <doc>"; cada seção vira um arquivo de `05-diagrams/`).
- ADR: Context, Problem, Options (≥2, incluindo "não fazer nada" quando cabível), Evaluation (tabela critérios×opções), Decision, Consequences (+/−), Risks, Rollback, Status (PROPOSED|ACCEPTED|SUPERSEDED|REJECTED|DEPRECATED), Date, Evidence (link para resposta do usuário/PR/ata; obrigatório para ACCEPTED), Supersedes/Superseded by. Nome: `docs/architecture/06-decisions/ADR-NNN-titulo-curto.md`. ADR só para decisão relevante (afeta estrutura, custo, segurança, dados, operação, difícil de reverter).
- Tech evaluation: TECHNOLOGY, PURPOSE, PROBLEM IT SOLVES, CURRENT ALTERNATIVE, ALTERNATIVES ANALYZED; critérios (maturity, community, maintenance, licensing, security, performance, scalability, operational complexity, learning curve, ecosystem, observability, vendor lock-in, cost, team knowledge, integration effort) com nota 1–5 + justificativa + fonte; classificação ADOPT/TRIAL/ASSESS/HOLD/REJECT; justificativas proibidas ("é moderno", "todo mundo usa", "é tendência").

## 8. Entrevista (skill architecture-interview)
- Antes: ler memória + rodar/consultar discovery; listar lacunas; descartar o que o repo responde.
- Priorizar por impacto arquitetural (restrições duras primeiro: regulatório/LGPD, infraestrutura obrigatória, integrações corporativas, disponibilidade, volume, prazo/orçamento, equipe).
- Blocos de 3–7 perguntas relacionadas e específicas; cada pergunta com: por que importa (1 linha), o que já foi encontrado no repo (se houver), opções/exemplos concretos quando ajudar, e "se não souber: qual hipótese adotamos?". Usar AskUserQuestion quando as respostas forem de múltipla escolha; texto livre caso contrário.
- Técnicas (decomposição à la Karpathy): quebrar em perguntas menores, restrições primeiro, fato × hipótese, pedir exemplo concreto, casos extremos, "o que pode dar errado", adaptar próxima rodada às respostas. Nunca despejar dezenas de perguntas.
- Depois de cada rodada: registrar em interview-log, atualizar known-facts/assumptions/open-questions/risks com Source=user e data; decidir se precisa de nova rodada (só se houver lacuna de alto impacto).
- Áreas cobertas (checklist, só o que faltar): objetivo, stakeholders, usuários, volume, disponibilidade, performance, escalabilidade, segurança, LGPD, integrações, dados, infraestrutura, restrições, orçamento, operação, deploy, observabilidade, DR, roadmap.

## 9. Critérios de conclusão
- Discovery: inventário de stack, módulos, dados, integrações, infra, CI/CD com evidência (arquivo) para cada item; lacunas listadas; nenhum julgamento de valor.
- Entrevista (rodada): todas as perguntas registradas com resposta ou DEFERRED; memória atualizada.
- Requisitos: RNFs com métrica e fonte; restrições; open questions priorizadas.
- Proposta TO-BE: cada elemento rastreável a requisito/fato; alternativas consideradas para escolhas relevantes; propostas como PROPOSAL; ADRs PROPOSED.
- Validação: usuário aprovou explicitamente (registrar data/resposta) → ADRs ACCEPTED com Evidence.
- Documentação: docs sem contradição com memória e código; diagramas derivados; nenhum documento vazio criado.
- Revisão: relatório do reviewer sem itens CRÍTICO abertos (ou aceitos pelo usuário como risco).
- Evolução: state.md com último commit revisado; `architecture-update` aponta docs obsoletos.
- Global: zero decisões inventadas; zero fato sem Source; zero ACCEPTED sem Evidence.

## 10. Formato dos arquivos Claude Code
- Subagentes: `~/.claude/agents/<nome>.md` com frontmatter YAML: `name`, `description` (quando usar, 1–3 frases, com gatilhos), `tools` (lista explícita; discovery e reviewer sem Write/Edit exceto o próprio arquivo de saída — dar Read, Grep, Glob, Bash, Write), `model: sonnet`. Corpo: Papel, Entradas esperadas no prompt, Procedimento passo a passo, Regras invioláveis, Formato de saída (arquivos + relatório de retorno ≤ 40 linhas com seções: Escrito, Memória (itens com Status/Source), Perguntas sugeridas, ADRs propostos, Riscos).
- Skills: `~/.claude/skills/<nome>/SKILL.md` com frontmatter `name`, `description` (gatilhos em PT e EN, ex.: "Vamos construir a arquitetura inicial deste projeto", "arquitetura", "architecture"). Corpo: Quando usar, Pré-condições (ler `.architecture/state.md`), Passos, Delegação (prompt-base para o subagente, com contexto mínimo: caminhos, fase, itens de memória relevantes), Gate de pergunta, Saída, Critério de conclusão, Atualização de state.md.
- A skill `architecture` deve tratar a frase "Vamos construir a arquitetura inicial deste projeto" como gatilho para iniciar o fluxo completo (start → interview → requirements → generate → validate → adr → review → gap-analysis), parando para o usuário em cada ponto de validação.
- Instalação: tudo gerado primeiro em STAGING `arch-framework/staging/{agents,skills}/` (scratchpad da sessão) espelhando `~/.claude/{agents,skills}`, mais `install.sh` (cópia idempotente, com backup do que existir com o mesmo nome) — o usuário aprova antes de instalar.

## Adendo: documento de arquitetura em PDF (42010)

- Subagente `architecture-documenter` (`agents/architecture-documenter.md`): consolida memória, `docs/architecture/`, ADRs e repositório no documento ISO/IEC/IEEE 42010 e gera o PDF. Escreve só `docs/arquitetura/<título>.{md,pdf}`. Não descobre, não propõe, não decide; sem fonte = "A definir" + pergunta provisória; ADR ACCEPTED = Decisão, PROPOSED = Proposta; AS-IS × TO-BE separados.
- Skill `architecture-pdf` (`skills/architecture-pdf/SKILL.md`): gatilhos "gerar PDF da arquitetura", "documento 42010"; gate de pergunta (identificação, stakeholders, concerns); delega e confere visualmente o PDF.
- Template e gerador em `skills/architecture/templates/architecture-document/` (`document.md`, `print.css`, `render_pdf.py`, `render_mermaid.mjs`, `setup.sh`, `README.md` com o guia de formato). Motor: WeasyPrint; diagramas Mermaid via Chromium local; ambiente local em `~/.cache/architecture-pdf`.
- Resultado: 7 subagentes, 17 skills.
