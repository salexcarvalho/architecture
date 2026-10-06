# Interview Log

<!--
Local: `.architecture/interview-log.md`.
Uma seção por rodada de entrevista. Append-only (nunca reescrever rodadas passadas).
Registrar: data, perguntas (com Q-ID), respostas resumidas fiéis (sem interpretar), itens de memória gerados (F/A/Q/R/P).
Respostas do usuário são Source=user e têm data. Se o usuário não soube responder, registrar DEFERRED e a hipótese adotada.
Não registrar segredos que o usuário porventura cole na resposta: redigir "[valor omitido]".
-->

## Rodada 1 — AAAA-MM-DD

**Objetivo da rodada:** <ex.: fechar restrições duras (regulatório, infraestrutura obrigatória, disponibilidade)>
**Achados do repositório usados para evitar perguntas:** <ex.: banco = SGBD X (`docker-compose.yml:8`); CI = pipeline Y (`.github/workflows/ci.yml`)>

| # | Q-ID | Pergunta (resumo) | Resposta (resumo literal) | Status | Memória gerada |
|---|---|---|---|---|---|
| 1 | Q-001 | Há obrigação regulatória sobre os dados? | "Sim, dados pessoais de clientes" | ANSWERED | F-007, R-004 |
| 2 | Q-002 | Pico de usuários simultâneos? | "Não sei" | DEFERRED | A-001 (hipótese: ≤200) |
| 3 | Q-003 | Infraestrutura obrigatória (nuvem/on-premises)? | "Servidores próprios" | ANSWERED | F-008 |

**Nova rodada necessária?** sim | não — <motivo: lacunas de alta prioridade restantes: Q-0NN>
**Próxima rodada:** <tema e quantidade de perguntas>
