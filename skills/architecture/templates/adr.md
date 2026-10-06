# ADR-NNN: <Título curto da decisão>

<!--
Local: `docs/architecture/06-decisions/ADR-NNN-titulo-curto.md` (NNN sequencial, 3 dígitos, nunca reutilizado).
Criar ADR só para decisão RELEVANTE: afeta estrutura, custo, segurança, dados, operação, ou é difícil de reverter.
Estados: PROPOSED | ACCEPTED | SUPERSEDED | REJECTED | DEPRECATED.
REGRA CRÍTICA: ACCEPTED só com Evidence de aprovação do usuário (resposta registrada com data em `.architecture/interview-log.md`, PR aprovado ou ata). Sem Evidence o status é PROPOSED.
Subagentes NÃO criam ADR nem marcam ACCEPTED: apenas propõem. A skill `architecture-adr` cria o arquivo.
Para mudar uma decisão: criar ADR novo que "Supersedes" o antigo; o antigo vira SUPERSEDED (não apagar, não reescrever).
-->

| Campo | Valor |
|---|---|
| **Status** | PROPOSED <!-- PROPOSED | ACCEPTED | SUPERSEDED | REJECTED | DEPRECATED --> |
| **Date** | AAAA-MM-DD |
| **Evidence** | — <!-- obrigatório para ACCEPTED: "resposta do usuário em AAAA-MM-DD (interview-log rodada N)" | link do PR | ata --> |
| **Supersedes** | — <!-- ADR-NNN --> |
| **Superseded by** | — |
| **Decisores** | <papéis> |
| **Origem** | <P-NNN / Q-NNN / skill que propôs> |

## Context
<!-- Situação e forças em jogo. Fatos com marcadores: [KNOWN · F-NNN]. Restrições: RES-NNN. Sem opinião. -->
O sistema precisa <necessidade>. Hoje <situação atual>. [KNOWN · F-002] Restrição: <restrição>. [KNOWN · F-008]

## Problem
<!-- Uma frase: qual decisão precisa ser tomada e por quê agora. -->
Como <objetivo> dado <restrição>?

## Options
<!-- Mínimo 2 opções. Incluir "Não fazer nada" quando cabível. -->
1. **Opção A — <nome>**: <descrição breve>
2. **Opção B — <nome>**: <descrição breve>
3. **Opção C — Não fazer nada**: manter <situação atual>

## Evaluation

| Critério | Peso | Opção A | Opção B | Opção C (nada) | Fonte |
|---|---|---|---|---|---|
| Atende RNF-003 (RTO ≤ 4 h) | alto | sim | parcial | não | `non-functional.md` |
| Complexidade operacional | alto | média | baixa | nenhuma | tech-evaluation |
| Custo (implantação + operação) | médio | <valor/qualitativo> | | | |
| Esforço de migração | médio | | | | |
| Risco de segurança/privacidade | alto | | | | `threat-model.md` |
| Reversibilidade | médio | | | | |

## Decision
<!-- Só preencher o texto final se Status = ACCEPTED. Em PROPOSED: "Proposta: ..." -->
Proposta: adotar a **Opção A** porque <razões ligadas à tabela de avaliação>.

## Consequences

**Positivas (+)**
- <consequência>

**Negativas (−)**
- <consequência / custo / dívida assumida>

## Risks
| ID | Risco | Mitigação |
|---|---|---|
| R-0NN | <risco da decisão> | <mitigação> |

## Rollback
<!-- Como desfazer: passos, custo, ponto de não retorno. "Irreversível" deve ser explícito e justificado. -->
1. <passo>
- Ponto de não retorno: <quando>

## Links
- Documentos afetados: `../04-to-be/<doc>.md`
- Perguntas/hipóteses: Q-NNN, A-NNN
- Tech evaluation: `../07-technology/evaluations/<x>.md`
