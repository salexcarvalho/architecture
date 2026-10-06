# Arquitetura Proposta (TO-BE) — <Nome do Sistema>

<!--
Local: `docs/architecture/04-to-be/architecture.md`. Escrito por `application-architect` (visão de aplicação) e consolidado por `architecture-generate`. Serve também de estrutura-base para os demais documentos de `04-to-be/` (applications, integrations, data, infrastructure, security, observability, deployment), cada um com o seu escopo.
Tudo aqui é PROPOSTA até o usuário aprovar. Marcar [PROPOSAL · P-NNN]; só vira [DECISION · ADR-NNN] com ADR ACCEPTED + Evidence.
Rastreabilidade obrigatória: cada elemento aponta para um requisito (RNF-NNN / RF-NNN), fato (F-NNN) ou restrição.
Para escolhas relevantes: ≥2 alternativas consideradas (incluir "não mudar" quando cabível) e ADR PROPOSED.
Proibido: complexidade sem justificativa registrada (ex.: orquestrador de contêineres, microsserviços, filas) — justificar com requisito ou rejeitar.
Começar pelo cabeçalho padrão (templates/doc-section.md).
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |
| **Base AS-IS** | `../03-as-is/architecture.md` |
| **Requisitos** | `../02-requirements/non-functional.md` |

## 1. Objetivos e princípios
| # | Objetivo / princípio | Origem (requisito/fato) |
|---|---|---|
| 1 | Reduzir tempo de recuperação após falha | RNF-003, [KNOWN · F-004] |
| 2 | Manter a stack atual onde não há requisito de mudança | [DECISION · ADR-001] |

## 2. Visão geral da solução
<!-- Estilo arquitetural proposto (ex.: monólito modular), por quê, e o que NÃO muda. -->
[PROPOSAL · P-001] Evoluir o monólito atual para monólito modular, mantendo um único artefato de deploy.

Diagramas derivados: `../05-diagrams/context.md`, `../05-diagrams/container.md`.

## 3. Componentes

| Componente | Responsabilidade | Tecnologia | Status vs AS-IS | Rastreia para |
|---|---|---|---|---|
| API | Regras de negócio e contratos HTTP | <tecnologia atual> | mantido | F-001 |
| Worker | Processamento assíncrono | <tecnologia> | novo [PROPOSAL · P-002] | RNF-005 |

## 4. Integrações e contratos
| Integração | Estilo (síncrono/assíncrono) | Contrato | Resiliência (retry/timeout/idempotência) | Status |
|---|---|---|---|---|
| <sistema externo> | síncrono REST | `<openapi>` | timeout + retry com backoff | [PROPOSAL · P-003] |

## 5. Alternativas consideradas (escolhas relevantes)

| Escolha | Alternativa A (proposta) | Alternativa B | "Não fazer nada" | ADR |
|---|---|---|---|---|
| Processamento assíncrono | Fila gerenciada | Tabela de jobs no banco | Manter síncrono | ADR-002 (PROPOSED) |

## 6. Mapa de rastreabilidade

| Elemento TO-BE | Requisito / fato / restrição |
|---|---|
| Worker | RNF-005 (processar em até 5 min) |

## 7. Riscos e pontos em aberto
- [RISK · R-002] <risco da proposta>
- [OPEN · Q-00N] <pergunta que bloqueia refinamento>

## 8. Fora de escopo
- <item e motivo>
