---
name: architecture
description: Ponto de entrada do framework de arquitetura. Lê .architecture/state.md, decide a fase e chama a skill certa. Gatilho de fluxo completo "Vamos construir a arquitetura inicial deste projeto". Use quando o usuário disser "arquitetura", "architecture", "documentar a arquitetura", "construir/atualizar a arquitetura", "onde estamos na arquitetura", "próximo passo da arquitetura", "build the initial architecture for this project", "architecture status".
---

# architecture — ponto de entrada e coordenação

Coordenação e entrevista rodam na SESSÃO PRINCIPAL (esta skill). Subagentes (`architecture-discovery`, `application-architect`, `data-architect`, `platform-architect`, `security-privacy-architect`, `architecture-reviewer`) analisam e PROPÕEM; `architecture-documenter` apenas CONSOLIDA em documento o que já está verificado; nenhum fala com o usuário, nenhum decide e não disparam outros subagentes. Só a sessão principal delega.

## Quando usar
- O usuário pede para construir, continuar, revisar ou consultar o estado da arquitetura de um projeto.
- Frase-gatilho: **"Vamos construir a arquitetura inicial deste projeto"** → executar o FLUXO COMPLETO (abaixo).
- Dúvida sobre qual skill `architecture-*` usar → esta skill roteia.

## Pré-condições
1. Ler `.architecture/state.md` (se existir). Ler também `.architecture/context.md` se existir.
2. Se `.architecture/state.md` NÃO existir: orientar e executar `architecture-start` (inicializa a memória e roda discovery). Não gerar nenhum documento antes.
3. Templates: `~/.claude/skills/architecture/templates/<arquivo>` (caminho absoluto; nunca copiar templates para outro lugar além do destino do documento).

## Convenções do framework (valem para TODAS as skills `architecture-*`)

**Rótulos (em inglês):** KNOWN, UNKNOWN, ASSUMPTION, PROPOSAL, DECISION, RISK, OPEN QUESTION; documento DRAFT | REVIEWED | APPROVED; ADR PROPOSED | ACCEPTED | SUPERSEDED | REJECTED | DEPRECATED; radar ADOPT | TRIAL | ASSESS | HOLD | REJECT.

**Marcadores inline nos documentos:** `[KNOWN · F-003]`, `[ASSUMPTION · A-002]`, `[PROPOSAL · P-002]`, `[DECISION · ADR-004]`, `[OPEN · Q-007]`, `[RISK · R-001]`.

**Memória do projeto** (`.architecture/`, versionada, sem segredos): `state.md`, `context.md`, `known-facts.md` (F-NNN), `assumptions.md` (A-NNN), `open-questions.md` (Q-NNN), `decisions.md` (ADR-NNN, P-NNN), `risks.md` (R-NNN), `interview-log.md`, `reviews/`.

**Documentos** em `docs/architecture/` — ÁRVORE FIXA definida pelo usuário (nenhum outro arquivo ou pasta pode ser criado; só nascem os arquivos com conteúdo verificado):

```
docs/architecture/
README.md                                   (índice; skills que criam/alteram doc o atualizam)
01-context/      project-context.md, stakeholders.md, glossary.md, assumptions.md          <- architecture-context
02-requirements/ functional.md, non-functional.md, constraints.md, open-questions.md       <- architecture-context
03-as-is/        architecture.md, applications.md, integrations.md, data.md, infrastructure.md  <- architecture-discovery (data.md: + data-architect)
04-to-be/        architecture.md, applications.md, integrations.md                         <- application-architect
                 data.md                                                                   <- data-architect
                 infrastructure.md, observability.md, deployment.md                        <- platform-architect
                 security.md                                                               <- security-privacy-architect
05-diagrams/     context.md, container.md, component.md, flows/<fluxo>.md                  <- application-architect
                 deployment.md                                                             <- platform-architect
06-decisions/    ADR-NNN-titulo-curto.md                                                   <- SOMENTE a skill architecture-adr
07-technology/   technology-radar.md, evaluations/<tecnologia>.md                          <- architecture-tech-evaluation
08-security/     threat-model.md, privacy-lgpd.md, security-baseline.md                    <- security-privacy-architect
09-operations/   environments.md, observability.md, backup-restore.md, disaster-recovery.md, runbooks.md  <- platform-architect
10-roadmap/      architecture-roadmap.md, technical-debt.md                                <- architecture-gap-analysis
```

Projeções: `01-context/assumptions.md` e `02-requirements/open-questions.md` espelham `.architecture/assumptions.md` e `.architecture/open-questions.md` (mesmos IDs; a memória prevalece). Lacunas do discovery NÃO têm arquivo em `03-as-is/`: vão para `.architecture/open-questions.md` (Q-NNN) e `.architecture/assumptions.md` (A-NNN). Riscos (inclusive de segurança) vão para `.architecture/risks.md` (R-NNN).

**Separação wiki limpa × documentação interna (regra do usuário).** A wiki do cliente é a versão LIMPA: sem IDs (F/A/Q/R/P/RF/RNF/RES/TD/ADR/DEC), sem PROPOSAL/DECISION, sem páginas de decisões, riscos ou perguntas; pendências do cliente em linguagem simples. ADRs, decisões, riscos, perguntas e pauta de refinamento ficam SÓ no repositório do sistema (`docs/architecture` + `.architecture`). Publicação, 3 páginas padrão, radar e deck: skill `architecture-publish`.

**IDs.** Memória: `F-NNN` fatos, `A-NNN` hipóteses, `Q-NNN` perguntas, `P-NNN` propostas, `R-NNN` riscos, `ADR-NNN` decisões. Locais a um documento (numeração própria, escrita pelo autor do documento): `RNF-NNN`, `RF-NNN`, `RES-NNN` (requisitos e restrições), `G-NNN`/`TD-NNN` (lacunas e dívida técnica do roadmap), `RV-NNN` (achados do reviewer).

**IDs provisórios e renumeração (obrigatório).** Subagentes não escrevem em `decisions.md`, `open-questions.md`, `assumptions.md` nem `risks.md` e não conhecem a numeração final: item novo é escrito como `<TIPO>-novo-<n>` (`F-novo-1`, `A-novo-1`, `Q-novo-1`, `P-novo-1`, `R-novo-1`; `n` sequencial por tipo dentro da execução) nos documentos e no relatório. Exceção: `architecture-discovery` é dono da seção discovery de `known-facts.md` e atribui `F-NNN` finais (continuando do maior existente; em delegações paralelas a skill informa faixas disjuntas). A skill que delegou, ao reconciliar o retorno, DEVE: (1) ler o maior ID de cada tipo na memória; (2) atribuir IDs finais na ordem do relatório, sem reutilizar; (3) registrar o item no arquivo de memória do tipo; (4) substituir TODAS as ocorrências `X-novo-n` nos documentos que aquele subagente escreveu, arquivo por arquivo (`grep -rn 'novo-' docs/architecture`; Edit/sed), pois o mesmo `P-novo-1` pode existir em retornos de subagentes diferentes; (5) conferir que `grep -rn 'novo-' docs/architecture .architecture` retorna 0 antes de encerrar a etapa. O reviewer aponta qualquer `-novo-` restante.

**Regras invioláveis**
- Zero decisão inventada. PROPOSAL só vira DECISION com evidência de aprovação (resposta do usuário registrada com data, ou ADR ACCEPTED).
- Inferido nunca vira KNOWN. Todo item de memória tem Source (`repository | documentation | user | runtime | inferred | architectural analysis`).
- Zero ACCEPTED sem Evidence.
- Nunca ler nem registrar valores de segredos (apenas nomes de variáveis).
- NÃO CRIAR DOCUMENTO VAZIO: se não há conteúdo com fonte, não criar o arquivo; registrar a pendência em `docs/architecture/README.md` ("Pendentes") e a pergunta em `open-questions.md`.
- Busca antes de perguntar (obrigatória): procurar em docker-compose, `.env.example`, manifests de pacote, migrations, código, docs, CI. Se achou, não perguntar a existência; perguntar algo de maior valor citando o achado.

**Gate de pergunta (antes de gerar documento relevante).** Checar a informação mínima; se faltar item de ALTO impacto → `architecture-interview` primeiro.

| Documento | Informação mínima |
|---|---|
| `01-context/*`, `02-requirements/*` | objetivo, stakeholders, usuários/volume, disponibilidade, desempenho, restrições (regulatório, infra, prazo, orçamento, equipe) |
| `04-to-be/architecture.md`, `applications.md`, `integrations.md` | AS-IS descoberto, RNFs com métrica, integrações obrigatórias, equipe/competências |
| `04-to-be/data.md` | entidades atuais (migrations), volume, retenção, dados pessoais, requisitos de consistência |
| `04-to-be/infrastructure.md`, `deployment.md`, `observability.md`, `09-operations/*` | infraestrutura obrigatória, ambientes, disponibilidade, RPO/RTO, orçamento, operação (quem opera) |
| `04-to-be/security.md`, `08-security/*` | dados pessoais, base regulatória, autenticação existente, integrações externas, ativos críticos |
| ADR | contexto factual, ≥2 opções, critérios, restrições aplicáveis |

## Fluxo geral
DESCOBRIR → LER → CONHECIDO → LACUNAS → PERGUNTAR → REGISTRAR → ALTERNATIVAS → PROPOR → VALIDAR COM USUÁRIO → DOCUMENTAR → REVISAR → EVOLUIR.

## Roteamento por fase (`state.md`)

| Fase | Situação | Skill a chamar |
|---|---|---|
| `0-init` | sem memória ou recém-criada | `architecture-start` |
| `1-discovery` | AS-IS incompleto ou desatualizado | `architecture-discover` |
| `2-interview` | lacunas de alto impacto abertas | `architecture-interview` (+ `architecture-context` para registrar fatos soltos) |
| `3-requirements` | RNFs/restrições sem métrica/fonte | `architecture-context`, depois `architecture-interview` se faltar item |
| `4-proposal` | requisitos prontos, TO-BE ausente | `architecture-generate` (ou `architecture-api/data/infrastructure/devops/security` para parte) |
| `5-validation` | proposta pronta, sem aprovação | apresentar ao usuário; `architecture-adr` para registrar aprovações |
| `6-documentation` | aprovado, docs a consolidar | `architecture-generate` (consolidação), `architecture-gap-analysis`; publicação para o cliente (wiki limpa + 3 páginas padrão): `architecture-publish`; deck/apresentação ao cliente: `architecture-presentation`; documento formal em PDF (42010): `architecture-pdf` |
| `7-review` | docs prontos | `architecture-review` |
| `8-evolution` | doc viva | `architecture-update` |
| qualquer | escolha de tecnologia | `architecture-tech-evaluation` |
| qualquer | publicar na wiki, documentação para o cliente, gráficos radar | `architecture-publish` |
| qualquer | apresentação/deck de arquitetura, versão resumida, revisar apresentação | `architecture-presentation` |
| qualquer | "gerar PDF da arquitetura", "documento de arquitetura de software", "documento 42010" | `architecture-pdf` (escopo: atual, proposta ou ambas; saída em `docs/arquitetura/`, fora da árvore fixa) |

## FLUXO COMPLETO ("Vamos construir a arquitetura inicial deste projeto")

Executar em ordem, atualizando `state.md` a cada etapa. **PARAR e aguardar o usuário nos pontos marcados ⏸.**

1. **start** — `architecture-start`: cria `.architecture/` se não existir, roda discovery, monta o 1º bloco de perguntas. ⏸ *Validação 1:* apresentar o resumo do AS-IS (≤ 15 linhas) e o 1º bloco de perguntas.
2. **interview** — `architecture-interview`: rodadas de 3–7 perguntas (restrições duras primeiro). Repetir só se restar lacuna de ALTO impacto. ⏸ *Validação 2:* ao fim de cada rodada, mostrar o que foi registrado e confirmar se pode seguir.
3. **requirements** — `architecture-context`: consolidar contexto (`01-context/*`), requisitos funcionais com impacto arquitetural, RNFs (métrica+alvo+fonte), restrições e perguntas abertas priorizadas (`02-requirements/{functional,non-functional,constraints,open-questions}.md`). ⏸ *Validação 3:* usuário confirma requisitos e restrições.
4. **generate** — `architecture-generate`: TO-BE em ordem (application/data/platform em paralelo; security depois; reviewer por último). Se os especialistas sugerirem perguntas, consolidar numa única rodada de `architecture-interview`. ⏸ *Validação 4:* apresentar a proposta (componentes, alternativas, ADRs PROPOSED, riscos) e pedir aprovação EXPLÍCITA, item a item.
5. **validate + adr** — `architecture-adr`: com a aprovação registrada (data + resposta), promover ADRs a ACCEPTED com Evidence; os não aprovados ficam PROPOSED ou REJECTED. Itens PROPOSAL aprovados viram `[DECISION · ADR-NNN]`.
6. **review** — `architecture-review`: revisão independente. ⏸ *Validação 5:* mostrar achados CRÍTICO/ALTO; usuário decide corrigir ou aceitar como risco (registrar).
7. **gap-analysis** — `architecture-gap-analysis`: AS-IS × TO-BE → roadmap + dívida técnica. ⏸ *Validação final:* usuário revisa o roadmap.
8. **publish** (quando o usuário pedir documentação para o cliente / ao consolidar a fase `6-documentation`) — `architecture-publish`: wiki limpa + 3 páginas padrão com radar; deck ao cliente: `architecture-presentation` (revisão + produção); push só com pedido. Documento formal em PDF: `architecture-pdf`.
9. Fechar: `state.md` com fase `8-evolution`, último commit revisado e próximos passos; atualizar `docs/architecture/README.md`.

Se o usuário interromper, registrar o ponto exato em `state.md` ("Próximos passos") para retomada.

## Delegação
Esta skill não delega diretamente: chama as skills especializadas, que contêm os prompts-base dos subagentes. Contrato de retorno que TODO subagente deve cumprir (incluir no prompt quando delegar):

```
Retorne ≤ 40 linhas com as seções:
## Escrito        (arquivos criados/alterados, 1 linha cada)
## Memória        (itens novos: ID provisório `<TIPO>-novo-<n>`, texto, Status, Source, evidência)
## Perguntas sugeridas  (≤ 7, ordenadas por impacto; cada uma: por que importa + achado no repo)
## ADRs propostos (título, motivo, opções) — NÃO criar ADR, NÃO marcar ACCEPTED
## Riscos         (R provisórios: risco, prob., impacto, mitigação)
```

## Saída
- Resposta curta ao usuário: fase atual, o que foi feito, próximo ponto de validação.
- Nenhum documento criado fora das skills especializadas.

## Critério de conclusão (global)
- Zero decisões inventadas; zero fato sem Source; zero ACCEPTED sem Evidence; nenhum documento vazio.
- Critério por fase: ver cada skill. Projeto "concluído" para a versão inicial = fases 0–7 DONE, roadmap gerado, `state.md` com último commit revisado.

## Atualização de state.md
Ao iniciar: ler. Ao terminar qualquer etapa: atualizar fase atual, linha em "Execuções" (data, skill, resultado, HEAD), "Próximos passos", "Bloqueios" e "Pontos de validação pendentes". Modelo: `~/.claude/skills/architecture/templates/state.md`.
