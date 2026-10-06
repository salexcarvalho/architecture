# Decisions

<!--
Local: `.architecture/decisions.md`.
Índice: espelho resumido dos ADRs em `docs/architecture/06-decisions/` + propostas que ainda não viraram ADR.
Fonte de verdade do conteúdo é o arquivo ADR; este índice só aponta.
Regras:
- Status do ADR: PROPOSED | ACCEPTED | SUPERSEDED | REJECTED | DEPRECATED.
- ACCEPTED exige Evidence (resposta do usuário registrada com data, PR ou ata). Sem Evidence, o ADR permanece PROPOSED.
- Proposta P-NNN = ideia de decisão ainda sem ADR. Promover a ADR quando for relevante (afeta estrutura, custo, segurança, dados, operação ou é difícil de reverter).
- Atualizar este índice sempre que um ADR mudar de status.
-->

**Última atualização:** AAAA-MM-DD

## ADRs

| ID | Título | Status | Data | Evidence | Substitui / Substituído por |
|---|---|---|---|---|---|
| ADR-001 | Adotar banco relacional como armazenamento principal | ACCEPTED | AAAA-MM-DD | resposta do usuário em AAAA-MM-DD (rodada 2) | — |
| ADR-002 | Adotar fila de mensagens para integrações assíncronas | PROPOSED | AAAA-MM-DD | — | — |

## Propostas sem ADR

| ID | Proposta | Origem | Relevância | Próximo passo |
|---|---|---|---|---|
| P-001 | Centralizar logs em stack de observabilidade única | platform-architect | média | Aguardar requisito de retenção (Q-009) |
| P-002 | Introduzir cache de leitura no catálogo | application-architect | baixa | Avaliar após medir carga (R-003) |

## Decisões rejeitadas

| ID | Título | Motivo | Data |
|---|---|---|---|
| — | — | — | — |
