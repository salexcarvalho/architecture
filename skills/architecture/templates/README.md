# Documentação de Arquitetura — <Nome do Sistema>

<!--
Local: `docs/architecture/README.md`. Índice vivo da documentação.
Regras:
- Listar SOMENTE documentos que existem. Não criar documento vazio só para preencher o índice: se o assunto não tem conteúdo ainda, omitir a linha (ou registrar em "Pendentes").
- Atualizar a coluna Status e Atualizado a cada alteração (skills fazem isso).
- Memória de trabalho (fatos, hipóteses, perguntas, riscos) fica em `.architecture/` e prevalece: `01-context/assumptions.md` e `02-requirements/open-questions.md` são projeções dela (mesmos IDs), nunca fonte independente.
-->

**Última atualização:** AAAA-MM-DD · **Fase:** <ver `.architecture/state.md`>

## Legenda

| Marcador | Significado |
|---|---|
| `[KNOWN · F-NNN]` | Fato com evidência (ver `.architecture/known-facts.md`) |
| `[ASSUMPTION · A-NNN]` | Hipótese ainda não confirmada |
| `[PROPOSAL · P-NNN]` | Proposta ainda não aprovada pelo usuário |
| `[DECISION · ADR-NNN]` | Decisão aceita, com ADR ACCEPTED e Evidence |
| `[OPEN · Q-NNN]` | Pergunta em aberto |
| `[RISK · R-NNN]` | Risco registrado |
| `DRAFT` / `REVIEWED` / `APPROVED` | Status do documento |

## Estrutura

Árvore fixa (definida pelo usuário). Só existem os arquivos com conteúdo verificado; os demais constam em "Pendentes".

| Pasta | Arquivos | Escrito por | Quando existe |
|---|---|---|---|
| `01-context/` | `project-context.md`, `stakeholders.md`, `glossary.md`, `assumptions.md` | architecture-context | após discovery + entrevista |
| `02-requirements/` | `functional.md`, `non-functional.md`, `constraints.md`, `open-questions.md` | architecture-context | fase 3 |
| `03-as-is/` | `architecture.md`, `applications.md`, `integrations.md`, `data.md`, `infrastructure.md` | architecture-discovery (data.md: + data-architect) | fase 1 |
| `04-to-be/` | `architecture.md`, `applications.md`, `integrations.md`, `data.md`, `infrastructure.md`, `security.md`, `observability.md`, `deployment.md` | application / data / platform / security-privacy | fase 4 em diante |
| `05-diagrams/` | `context.md`, `container.md`, `component.md`, `deployment.md`, `flows/` | application-architect; deployment.md: platform-architect | fase 4 em diante |
| `06-decisions/` | `ADR-NNN-*.md` | somente a skill architecture-adr | quando houver decisão relevante |
| `07-technology/` | `technology-radar.md`, `evaluations/` | architecture-tech-evaluation | quando houver escolha tecnológica |
| `08-security/` | `threat-model.md`, `privacy-lgpd.md`, `security-baseline.md` | security-privacy-architect | fase 4 em diante |
| `09-operations/` | `environments.md`, `observability.md`, `backup-restore.md`, `disaster-recovery.md`, `runbooks.md` | platform-architect | fase 4 em diante |
| `10-roadmap/` | `architecture-roadmap.md`, `technical-debt.md` | architecture-gap-analysis | após gap analysis |

## Índice de documentos

| Documento | Caminho | Status | Atualizado | Responsável |
|---|---|---|---|---|
| Arquitetura atual | `03-as-is/architecture.md` | DRAFT | AAAA-MM-DD | architecture-discovery |
| Arquitetura proposta | `04-to-be/architecture.md` | DRAFT | AAAA-MM-DD | application-architect |
| Modelo de dados | `04-to-be/data.md` | DRAFT | AAAA-MM-DD | data-architect |
| Segurança | `04-to-be/security.md` | DRAFT | AAAA-MM-DD | security-privacy-architect |
| ADR-001 | `06-decisions/ADR-001-<titulo-curto>.md` | ACCEPTED | AAAA-MM-DD | architecture-adr |

## Pendentes (documentos ainda não gerados)

- <documento> — motivo: <aguardando Q-NNN / fora de escopo / fase anterior>

## Revisões

| Data | Relatório | Itens CRÍTICO abertos |
|---|---|---|
| AAAA-MM-DD | `.architecture/reviews/REVIEW-AAAA-MM-DD.md` | 0 |
