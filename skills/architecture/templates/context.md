# Contexto do Sistema

<!--
Local: `.architecture/context.md`. Resumo de UMA página (máx. ~60 linhas).
Cada afirmação carrega marcador inline e referência de memória: [KNOWN · F-001], [ASSUMPTION · A-001], [OPEN · Q-001].
Não duplicar tabelas de known-facts: resumir e referenciar IDs.
Não preencher o que não se sabe: manter o marcador [OPEN · Q-NNN] com a pergunta correspondente.
-->

**Última atualização:** AAAA-MM-DD

## Propósito
<!-- 2-3 frases: o que o sistema faz e para quem. -->
Sistema de <domínio genérico, ex.: gestão de pedidos> usado por <perfil de usuário>. [KNOWN · F-001]

## Stakeholders e usuários
| Grupo | Papel | Volume estimado | Marcador |
|---|---|---|---|
| Operadores internos | Cadastro e acompanhamento | ~50 usuários | [KNOWN · F-004] |
| Clientes externos | Consulta via portal | [OPEN · Q-002] | [OPEN · Q-002] |

## Stack e componentes principais
| Camada | Tecnologia | Evidência | Marcador |
|---|---|---|---|
| Frontend | <framework> | `package.json` | [KNOWN · F-002] |
| Backend | <runtime/framework> | `<arquivo>` | [KNOWN · F-003] |
| Banco de dados | <SGBD> | `docker-compose.yml` | [KNOWN · F-005] |

## Integrações
- <sistema externo A> via <protocolo> [KNOWN · F-006]
- <sistema externo B> [OPEN · Q-005]

## Restrições conhecidas
- <restrição dura: regulatória, infraestrutura obrigatória, prazo, orçamento, equipe> [KNOWN · F-0NN]

## Situação da arquitetura
- Fase atual: ver `.architecture/state.md`
- ADRs aceitos: <n> | Propostas pendentes: <n> | Perguntas abertas de alta prioridade: <n>

## Fora de escopo (por enquanto)
- <item> [DECISION · ADR-NNN] ou [ASSUMPTION · A-0NN]
