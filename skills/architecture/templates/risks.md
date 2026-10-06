# Risks

<!--
Local: `.architecture/risks.md`.
Registro de riscos arquiteturais. Marcador inline nos docs: [RISK · R-001].
Escala: probabilidade e impacto = baixa | média | alta. Severidade = combinação (alta+alta = CRÍTICO).
Status: OPEN | MITIGATING | ACCEPTED | CLOSED. ACCEPTED (status de RISCO, distinto de ADR ACCEPTED) exige evidência de aceite pelo usuário (data + resposta); nenhum subagente o define.
Todo risco CRÍTICO precisa de dono e mitigação.
Nunca registrar risco sem fonte: indique de onde veio (fato F-NNN, hipótese A-NNN ou análise).
-->

**Última atualização:** AAAA-MM-DD

| ID | Risco | Origem | Probabilidade | Impacto | Mitigação | Dono | Status |
|---|---|---|---|---|---|---|---|
| R-001 | Ponto único de falha no banco de dados (sem réplica) | F-002 | média | alta | Avaliar réplica de leitura + backup testado (ver `09-operations/backup-restore.md`) | <papel/pessoa> | OPEN |
| R-002 | Dependência de integração externa sem contrato formal | F-006 | alta | média | Definir contrato e testes de contrato; ADR-003 proposto | <papel/pessoa> | MITIGATING |
| R-003 | Hipótese de carga baixa pode estar errada | A-001 | média | média | Medir carga real antes de dimensionar | <papel/pessoa> | OPEN |
