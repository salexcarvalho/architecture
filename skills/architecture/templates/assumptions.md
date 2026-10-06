# Assumptions

<!--
Local: `.architecture/assumptions.md`.
Hipóteses: o que foi inferido ou deduzido por análise, sem evidência direta.
Regra: inferido NUNCA vira KNOWN sozinho. Para virar fato precisa de confirmação (resposta do usuário ou evidência no repositório).
Colunas:
- ID: A-NNN.
- Source: inferred | architectural analysis
- Status: OPEN | CONFIRMED | REJECTED. Ao CONFIRMAR: criar o F-NNN correspondente em known-facts.md e citar aqui "→ F-NNN".
- Como validar: ação concreta (pergunta Q-NNN, arquivo a procurar, teste a rodar).
Todo ASSUMPTION relevante para uma decisão deve ter uma pergunta associada em open-questions.md.
-->

**Última atualização:** AAAA-MM-DD

| ID | Hipótese | Source | Motivo | Como validar | Status | Pergunta |
|---|---|---|---|---|---|---|
| A-001 | O volume de usuários simultâneos não passa de ~200 | inferred | Base de ~50 operadores e portal sem divulgação ampla | Perguntar volume de pico | OPEN | Q-002 |
| A-002 | Não há requisito de multi-região | architectural analysis | Nenhuma configuração de réplica geográfica no IaC | Confirmar com o usuário | OPEN | Q-006 |
| A-003 | Os dados pessoais estão concentrados na tabela `<tabela>` | inferred | Nome das colunas no schema | Confirmar com o responsável por dados | CONFIRMED → F-009 | Q-004 |

## Assumptions rejeitadas (histórico)

| ID | Hipótese | Motivo da rejeição | Data |
|---|---|---|---|
| — | — | — | — |
