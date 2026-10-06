# Requisitos Não Funcionais — <Nome do Sistema>

<!--
Local: `docs/architecture/02-requirements/non-functional.md`. Restrições ficam em `constraints.md`; requisitos funcionais com impacto arquitetural em `functional.md`; perguntas abertas em `open-questions.md` (projeção de `.architecture/open-questions.md`). Escrito por `architecture-context` (fase 3-requirements).
Cada RNF tem: métrica mensurável, alvo, fonte (de onde vem o número). RNF sem métrica e sem fonte NÃO entra como requisito: vira `[OPEN · Q-NNN]` em `.architecture/open-questions.md` (e na projeção `02-requirements/open-questions.md`).
Fonte válida: resposta do usuário (data), documento citado, contrato/regulação, medição em runtime. "Boa prática" não é fonte.
Se o alvo foi assumido: marcar [ASSUMPTION · A-NNN] e registrar como validar.
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |

## 1. Requisitos não funcionais

| ID | Categoria | Requisito | Métrica | Alvo | Fonte | Marcador |
|---|---|---|---|---|---|---|
| RNF-001 | Disponibilidade | O sistema deve estar disponível em horário comercial | % uptime mensal (seg–sex 08–18h) | ≥ 99,5% | usuário, AAAA-MM-DD, rodada 1 | [KNOWN · F-004] |
| RNF-002 | Desempenho | Resposta das consultas principais | p95 de latência da API | ≤ 800 ms | hipótese de projeto | [ASSUMPTION · A-005] |
| RNF-003 | Recuperação | Restaurar o serviço após falha do banco | RTO / RPO | RTO ≤ 4 h / RPO ≤ 1 h | usuário, AAAA-MM-DD | [KNOWN · F-012] |
| RNF-004 | Escalabilidade | Suportar crescimento da base de usuários | usuários simultâneos no pico | 200 | — | [OPEN · Q-002] |
| RNF-005 | Segurança | Dados pessoais protegidos em repouso e trânsito | criptografia habilitada (sim/não) | sim | regulação aplicável (ver `08-security/`) | [KNOWN · F-007] |

Categorias a cobrir (só as que faltarem): disponibilidade, desempenho, escalabilidade, segurança, privacidade/LGPD, observabilidade, recuperação de desastres, manutenibilidade, portabilidade, custo, conformidade.

## 2. Rastreabilidade
| Requisito | Atendido por (documento/ADR) |
|---|---|
| RNF-003 | `09-operations/backup-restore.md`, ADR-0NN |
