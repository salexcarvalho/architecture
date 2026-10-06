# Dívida Técnica Arquitetural — <Nome do Sistema>

<!--
Local: `docs/architecture/10-roadmap/technical-debt.md`. Gerado por `architecture-gap-analysis`.
Dívida = desvio ENTRE o estado atual e o que o sistema/requisitos exigem, com custo de manter (juros). Não é lista de gostos.
Cada item: evidência no AS-IS, impacto (o que piora se nada for feito), custo estimado de pagar (P/M/G), gatilho de urgência.
Item sem evidência não entra (vira [OPEN] ou hipótese).
Tipos: intencional (decisão registrada), acidental, ambiental (dependência envelhecendo).
-->

**Última atualização:** AAAA-MM-DD

| ID | Dívida | Tipo | Evidência | Impacto se mantida ("juros") | Custo p/ pagar | Prioridade | Gatilho de urgência | Relacionado |
|---|---|---|---|---|---|---|---|---|
| TD-001 | Dependência `<lib>` sem manutenção | ambiental | `package.json:20` [KNOWN · F-0NN] | Vulnerabilidades sem correção | M | alta | Nova CVE sem patch | ADR-0NN |
| TD-002 | Regras de negócio duplicadas em dois módulos | acidental | `src/a/x.*`, `src/b/y.*` [KNOWN · F-0NN] | Divergência de comportamento | M | média | Mudança de regra | G-0NN |
| TD-003 | Ausência de testes automatizados de contrato | acidental | lacuna (não encontrado) [KNOWN · F-0NN] | Regressões em integrações | G | média | Mudança de contrato externo | R-0NN |

## Resumo por prioridade
| Prioridade | Quantidade | IDs |
|---|---|---|
| alta | 1 | TD-001 |
| média | 2 | TD-002, TD-003 |
| baixa | 0 | — |

## Dívidas aceitas conscientemente
| ID | Dívida | Aceita por / em | Evidência de aceite | Reavaliar em |
|---|---|---|---|---|
| — | — | — | — | — |

## Fora desta lista
- Itens sem evidência: ver `.architecture/open-questions.md` (Q-0NN).
