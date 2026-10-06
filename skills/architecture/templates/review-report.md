# Relatório de Revisão de Arquitetura — AAAA-MM-DD

<!--
Local: `.architecture/reviews/REVIEW-AAAA-MM-DD.md`. Escrito por `architecture-reviewer` (independente: nunca revisa o que ele mesmo escreveu).
O revisor APONTA, não edita os documentos revisados.
Severidade: CRÍTICO (bloqueia aprovação: contradição, decisão sem Evidence, segredo exposto, fato sem Source) | ALTO | MÉDIO | BAIXO.
Cada achado: onde (arquivo + trecho), regra violada, evidência, correção sugerida.
Retorno ao orquestrador ≤ 40 linhas; este arquivo contém o detalhe.
-->

| Campo | Valor |
|---|---|
| **Data** | AAAA-MM-DD |
| **Escopo** | <documentos revisados> |
| **Commit** | `<sha>` |
| **Veredito** | APROVADO / APROVADO COM RESSALVAS / REPROVADO |
| **Itens CRÍTICO abertos** | <n> |

## 1. Checklist de integridade

| # | Verificação | Resultado | Observação |
|---|---|---|---|
| 1 | Todo fato tem Source e evidência | OK / FALHA | |
| 2 | Nenhum item inferido marcado como KNOWN | OK / FALHA | |
| 3 | Nenhum ADR ACCEPTED sem Evidence | OK / FALHA | |
| 4 | Nenhuma proposta marcada como decisão | OK / FALHA | |
| 5 | Documentos sem contradição entre si, com memória e com o código | OK / FALHA | |
| 6 | Diagramas derivados e coerentes com o texto | OK / FALHA | |
| 7 | Nenhum documento vazio ou placeholder sem conteúdo | OK / FALHA | |
| 8 | Nenhum segredo/valor sensível exposto | OK / FALHA | |
| 9 | Escolhas relevantes têm ≥2 alternativas e ADR | OK / FALHA | |
| 10 | Complexidade introduzida tem justificativa registrada | OK / FALHA | |
| 11 | Afirmações de conformidade (privacidade) têm evidência | OK / FALHA | |

## 2. Achados

| ID | Severidade | Documento / trecho | Problema | Evidência | Correção sugerida | Status |
|---|---|---|---|---|---|---|
| RV-001 | CRÍTICO | `04-to-be/architecture.md` §3 | Componente "Worker" sem rastreio a requisito | RNF-005 não existe em `non-functional.md` | Criar RNF-005 ou remover o componente | OPEN |
| RV-002 | MÉDIO | `06-decisions/ADR-002-*.md` | Opções sem "não fazer nada" | — | Adicionar opção C | OPEN |

## 3. Docs possivelmente obsoletos
| Documento | Motivo | Mudança de código relacionada (commit) |
|---|---|---|
| — | — | — |

## 4. Lacunas de memória
- Perguntas de alta prioridade ainda abertas: Q-0NN
- Hipóteses sem plano de validação: A-0NN

## 5. Perguntas sugeridas (≤ 7, por impacto)
1. <pergunta> — por que importa — bloqueia <doc>

## 6. Conclusão
<2–4 linhas: o que impede a aprovação e o que o usuário precisa decidir.>
