# Avaliação de Tecnologia — <TECHNOLOGY>

<!--
Local: `docs/architecture/07-technology/evaluations/<tecnologia>.md`. Usado por `architecture-tech-evaluation`.
Regras:
- Cada critério: nota 1–5 (5 = melhor para ESTE contexto), justificativa objetiva e fonte (doc oficial, repositório, benchmark reproduzível, fato F-NNN, resposta do usuário).
- Critério sem fonte: nota "?" e [OPEN] — não inventar nota.
- JUSTIFICATIVAS PROIBIDAS: "é moderno", "todo mundo usa", "é tendência", "é mais rápido" sem medição, "a comunidade gosta". Reescrever com fato verificável ou remover.
- Incluir SEMPRE a alternativa atual e, quando cabível, "não adotar nada".
- Resultado: classificação ADOPT | TRIAL | ASSESS | HOLD | REJECT. Se a escolha é relevante, gerar ADR PROPOSED (ver adr.md).
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Data** | AAAA-MM-DD |
| **Avaliador** | <skill/agente> |

## TECHNOLOGY
<nome e versão avaliada>

## PURPOSE
<para que seria usada neste sistema, em 1–2 frases>

## PROBLEM IT SOLVES
<problema concreto, ligado a requisito (RNF-NNN) ou fato (F-NNN)>

## CURRENT ALTERNATIVE
<o que se usa hoje para esse problema e por que é insuficiente — com evidência; ou "nada">

## ALTERNATIVES ANALYZED
| # | Alternativa | Observação |
|---|---|---|
| 1 | <tecnologia proposta> | |
| 2 | <alternativa B> | |
| 3 | Manter a solução atual / não adotar nada | |

## Critérios

| Critério | Nota (1–5) A: <proposta> | Nota B: <alt. B> | Nota C: <atual/nenhuma> | Justificativa | Fonte |
|---|---|---|---|---|---|
| Maturity | 4 | 3 | 5 | A tem 8 anos de releases estáveis | changelog oficial |
| Community | | | | | |
| Maintenance | | | | Frequência de releases/issues fechadas nos últimos 12 meses | repositório |
| Licensing | | | | Licença compatível com o uso comercial? | arquivo LICENSE |
| Security | | | | Histórico de CVEs e prazo de correção | avisos de segurança |
| Performance | | | | Medição reproduzível no nosso cenário | benchmark (link) |
| Scalability | | | | | |
| Operational complexity | | | | Componentes a operar, upgrades, monitoramento | docs oficiais |
| Learning curve | | | | | |
| Ecosystem | | | | | |
| Observability | | | | Métricas/logs/tracing nativos | docs oficiais |
| Vendor lock-in | | | | Custo de saída | |
| Cost | | | | Licença + infra + operação | |
| Team knowledge | | | | Experiência da equipe | [OPEN · Q-0NN] |
| Integration effort | | | | Esforço para integrar com a stack atual | `<arquivo>` |

**Total ponderado (opcional, com pesos explícitos):** A = <n>, B = <n>, C = <n>. Pesos: <critério: peso> — origem dos pesos: <usuário/requisito>.

## Riscos da adoção
| Risco | Mitigação |
|---|---|
| <risco> | <mitigação> |

## Classificação
**<ADOPT | TRIAL | ASSESS | HOLD | REJECT>** — <motivo técnico em 2–3 linhas, citando critérios e fontes>

## Plano (se TRIAL ou ADOPT)
- Escopo do piloto: <limitado a quê>
- Critério de sucesso: <métrica>
- Critério de saída/rollback: <condição>

## Decisão associada
- ADR: `../../06-decisions/ADR-NNN-<titulo>.md` (PROPOSED) — ou "não relevante o bastante para ADR"
