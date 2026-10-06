# Architecture State

<!--
Arquivo de controle do framework. Local: `.architecture/state.md`.
Lido por TODA skill `architecture-*` antes de qualquer ação. Atualizado por TODA skill ao terminar.
Regras:
- Sem segredos. Sem valores de variáveis de ambiente.
- Só uma fase ativa por vez. Mudar de fase só quando o critério de conclusão da fase foi cumprido.
- Não apagar histórico: acrescentar linhas à tabela "Execuções".
-->

- **Projeto:** <nome genérico do sistema>
- **Fase atual:** `0-init`  <!-- 0-init | 1-discovery | 2-interview | 3-requirements | 4-proposal | 5-validation | 6-documentation | 7-review | 8-evolution -->
- **Última atualização:** AAAA-MM-DD
- **Último commit revisado:** `<sha>` <!-- usado por architecture-update para calcular `git diff <sha>..HEAD`; vazio até a primeira revisão -->
- **Rodada de entrevista atual:** 0

## Fases

| Fase | Nome | Status | Concluída em | Observação |
|---|---|---|---|---|
| 0-init | Inicialização da memória | OPEN | — | |
| 1-discovery | Descoberta AS-IS | OPEN | — | |
| 2-interview | Entrevista | OPEN | — | |
| 3-requirements | Requisitos e restrições | OPEN | — | |
| 4-proposal | Proposta TO-BE | OPEN | — | |
| 5-validation | Validação com o usuário | OPEN | — | |
| 6-documentation | Documentação final | OPEN | — | |
| 7-review | Revisão independente | OPEN | — | |
| 8-evolution | Evolução (doc viva) | OPEN | — | |

<!-- Status de fase: OPEN | IN PROGRESS | DONE | BLOCKED -->

## Execuções

| Data | Skill | Resultado | Commit (HEAD) | Arquivos afetados |
|---|---|---|---|---|
| AAAA-MM-DD | architecture-start | DONE | `<sha>` | `.architecture/*` |

## Próximos passos

1. <ação objetiva e a skill responsável, ex.: "rodar `architecture-interview` — rodada 1 (6 perguntas, bloco restrições)">
2. <...>

## Bloqueios

<!-- Liste IDs de perguntas abertas que bloqueiam a próxima fase. Ex.: Q-003 bloqueia 3-requirements. -->
- (nenhum)

## Pontos de validação com o usuário pendentes

<!-- Ex.: "Aprovar proposta TO-BE (4-proposal → 5-validation)". Registrar data e resposta quando houver. -->
- (nenhum)
