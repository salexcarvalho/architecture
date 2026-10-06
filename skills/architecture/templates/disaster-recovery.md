# Recuperação de Desastres — <Nome do Sistema>

<!--
Local: `docs/architecture/09-operations/disaster-recovery.md`. Escrito por `platform-architect`.
Só cenários plausíveis para o sistema real. RPO/RTO vêm de `backup-restore.md` (mesma fonte); sem fonte = [OPEN] e hipótese marcada ASSUMPTION.
Plano que nunca foi ensaiado = "não ensaiado" + [RISK]. Nunca registrar credenciais ou endpoints com segredo.
Começar pelo cabeçalho padrão (templates/doc-section.md).
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |
| **Último ensaio de DR** | AAAA-MM-DD ou "não ensaiado" |

## 1. Cenários de desastre cobertos

| Cenário | Coberto? | Estratégia | Observação |
|---|---|---|---|
| Corrupção lógica de dados | sim | restore point-in-time | |
| Perda do host/servidor | parcial | reprovisionar via IaC + restore | [OPEN · Q-0NN] |
| Perda do site inteiro | não | — | exige decisão de custo [OPEN · Q-0NN] |

## 2. Estratégia de recuperação e failover
| Cenário | Procedimento (referência a `runbooks.md`) | RTO esperado | Dependências | Marcador |
|---|---|---|---|---|
| Perda do host/servidor | <resumo; passos em `runbooks.md`> | <valor com fonte> | backup válido, IaC | [PROPOSAL · P-0NN] |

## 3. Critérios de acionamento e de retorno (failback)
- Quem declara o desastre e com quais critérios: <papel; critério objetivo>
- Critério de retorno à operação normal: <métrica/verificação>

## 4. Ensaios
| Data | Cenário simulado | Resultado | Lacunas encontradas |
|---|---|---|---|
| AAAA-MM-DD | <cenário> | sucesso / falha | <lista> |

## 5. Riscos
- [RISK · R-0NN] <ex.: DR nunca ensaiado>
