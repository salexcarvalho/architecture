# Runbooks — <Sistema>

<!--
Local: `docs/architecture/09-operations/runbooks.md` (UM arquivo; cada cenário é uma seção `## Runbook: <cenário>` que repete a estrutura abaixo).
Escrito por `platform-architect`. Só criar runbook para cenário real (incidente plausível, procedimento recorrente). Nunca criar runbook vazio.
Passos executáveis por quem não conhece o sistema. Sem segredos: referenciar ONDE o segredo é obtido, nunca o valor.
Comandos: apenas os confirmados no repositório/infra (KNOWN) ou marcados PROPOSAL.
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |
| **Cenário** | <ex.: API retornando 5xx em massa> |
| **Severidade típica** | SEV1 / SEV2 / SEV3 |
| **Responsável** | <papel> |
| **Último teste do procedimento** | AAAA-MM-DD ou "não testado" |

## 1. Sintomas e detecção
| Sinal | Fonte (alerta/log/dashboard) | Limite |
|---|---|---|
| Taxa de erro 5xx acima do normal | <monitoramento> | > 5% por 5 min |

## 2. Impacto
- Usuários afetados: <quem>
- Funções afetadas: <quais>
- Dependências afetadas: <quais>

## 3. Pré-requisitos
- Acessos necessários: <papéis, não credenciais>
- Ferramentas: <lista>

## 4. Diagnóstico (em ordem)
1. Verificar saúde do serviço: `<comando confirmado>` — esperado: `<resultado>`.
2. Verificar mudanças recentes (deploy/migration): `<como>`.
3. Verificar dependências (banco, integrações externas): `<como>`.

## 5. Mitigação / correção
| Causa provável | Ação | Reversível? | Quem aprova |
|---|---|---|---|
| Deploy recente com defeito | Rollback para a versão anterior (ver `environments.md`) | sim | <papel> |
| Banco sem conexões livres | Reiniciar pool / escalar conexões | sim | <papel> |

## 6. Verificação de recuperação
- Critérios: <métrica volta ao normal; smoke test passa>

## 7. Escalonamento
| Condição | Escalar para | Canal |
|---|---|---|
| Sem melhora em 30 min | <papel> | <canal> |

## 8. Pós-incidente
- Registrar linha do tempo, causa raiz, ação corretiva.
- Se a causa expõe lacuna arquitetural: abrir `[RISK · R-NNN]` e avaliar ADR.
