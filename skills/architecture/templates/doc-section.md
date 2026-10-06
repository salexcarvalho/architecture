# <Título do documento>

<!--
Cabeçalho padrão de TODO documento em `docs/architecture/`. Copiar este bloco para o topo do documento e remover os comentários.
Regras do corpo:
- Toda afirmação não trivial carrega marcador inline com ID de memória:
  [KNOWN · F-003]   fato com evidência
  [ASSUMPTION · A-002]  hipótese
  [PROPOSAL · P-002]    proposta não aprovada
  [DECISION · ADR-004]  decisão aceita
  [OPEN · Q-007]    pergunta em aberto
  [RISK · R-001]    risco
- Conteúdo sem fonte NÃO entra: se não há fato, hipótese ou proposta, é pergunta ([OPEN]).
- Não criar documento vazio: se não há conteúdo com fonte, não criar o arquivo.
- Diagramas ficam em `05-diagrams/` e são derivados; aqui apenas link.
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT <!-- DRAFT | REVIEWED | APPROVED --> |
| **Última atualização** | AAAA-MM-DD |
| **Autor (agente/skill)** | <ex.: application-architect via architecture-generate> |
| **Revisado em** | — <!-- data do REVIEW que cobriu este documento --> |
| **Aprovado por / em** | — <!-- só preencher com evidência de aprovação do usuário --> |
| **Fontes** | `.architecture/known-facts.md` (F-001, F-002), `.architecture/interview-log.md` (rodada 1), `<arquivo do repo>` |
| **Documentos relacionados** | `../03-as-is/architecture.md`, `../06-decisions/ADR-001-<titulo>.md` |

## Resumo
<!-- 3-5 linhas: o que este documento afirma e o que depende de confirmação. -->

## Conteúdo

<!-- Exemplo de corpo com marcadores: -->
- O sistema expõe uma API HTTP consumida por um frontend web. [KNOWN · F-001]
- Propõe-se separar o processamento assíncrono em um worker. [PROPOSAL · P-002]
- O volume de requisições no pico ainda não foi informado. [OPEN · Q-007]

## Pontos em aberto neste documento

| ID | Pergunta / hipótese | Impacto neste documento |
|---|---|---|
| Q-007 | Pico de requisições? | Dimensionamento da seção "Capacidade" |

## Histórico

| Data | Alteração | Motivo (commit/PR/resposta) |
|---|---|---|
| AAAA-MM-DD | Criação | Fase 4-proposal |
