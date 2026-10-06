---
name: architecture-gap-analysis
description: Compara AS-IS com TO-BE e gera roadmap de arquitetura e lista de dívida técnica. Use quando o usuário disser "gap analysis", "análise de lacunas da arquitetura", "gerar roadmap de arquitetura", "dívida técnica", "o que falta para chegar no TO-BE", "plano de migração", "architecture roadmap", "technical debt".
---

# architecture-gap-analysis — AS-IS × TO-BE → roadmap e dívida técnica

Skill de análise de documentos: lê os docs já produzidos, não delega.

## Quando usar
- TO-BE existe e foi validado (fase `5-validation` DONE) — ou ao menos há proposta aprovada em parte; gap analysis só sobre itens aprovados (`[DECISION]`) e, separado, sobre propostas ainda pendentes.
- Após `architecture-update` que alterou AS-IS/TO-BE de forma relevante.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Existir `docs/architecture/03-as-is/*` e `docs/architecture/04-to-be/*`. Se faltar um dos dois: não gerar (NÃO criar documento vazio); orientar `architecture-discover` ou `architecture-generate`.
3. Ler `decisions.md`, `risks.md`, `open-questions.md`, `02-requirements/non-functional.md`.

## Passos
1. **Mapear dimensões** (somente as que têm AS-IS e TO-BE): aplicação, dados, integrações, infraestrutura, deploy/CI/CD, observabilidade, segurança/privacidade, operação/DR.
2. **Identificar lacunas (G-NNN):** para cada elemento do TO-BE, o equivalente no AS-IS (com evidência) e a diferença. Lacuna sem AS-IS comprovado → `[OPEN]`, não gap.
3. **Estimar esforço relativo (P/M/G)** e risco por lacuna; dependências entre lacunas; requisito ou ADR que a motiva. Esforço em horas/datas só se o usuário fornecer parâmetros (senão não inventar).
4. **Montar ondas** ordenadas por dependência técnica, depois valor/risco; cada onda com objetivo, pré-requisitos e critério de saída. Itens que dependem de ADR PROPOSED ficam marcados "aguardando decisão".
5. **Dívida técnica (TD-NNN):** desvios do AS-IS em relação aos requisitos/boas práticas comprovadas por evidência, com impacto ("juros"), custo para pagar, prioridade e gatilho de urgência. Dívida sem evidência não entra. Dívida aceita conscientemente exige evidência de aceite do usuário.
6. **Escrever:**
   - `docs/architecture/10-roadmap/architecture-roadmap.md` (modelo: `~/.claude/skills/architecture/templates/architecture-roadmap.md`)
   - `docs/architecture/10-roadmap/technical-debt.md` (modelo: `~/.claude/skills/architecture/templates/technical-debt.md`)
   Criar apenas o que tiver conteúdo com fonte (NÃO criar documento vazio); se não houver dívida comprovada, não criar `technical-debt.md`.
7. Riscos do plano → `risks.md`; decisões que dependem do usuário → `open-questions.md` ou ADR PROPOSED via `architecture-adr`.
8. Atualizar `docs/architecture/README.md`.

## Delegação
Nenhuma (lê documentos). Se o AS-IS estiver desatualizado a ponto de invalidar lacunas, chamar `architecture-discover`/`architecture-update` antes.

## Gate de pergunta
Para ondas e prioridades: se faltarem prazo, orçamento, equipe ou janela de mudança (alto impacto no sequenciamento), fazer UMA rodada com `architecture-interview` (3–7 perguntas). Sem resposta: horizontes relativos (curto/médio/longo) e `[ASSUMPTION]`.

## Saída
- `10-roadmap/architecture-roadmap.md` e, se aplicável, `10-roadmap/technical-debt.md`; memória atualizada.
- Mensagem ao usuário: nº de lacunas por dimensão, ondas propostas, decisões necessárias.

## Critério de conclusão
- Toda lacuna com origem em AS-IS (evidência) × TO-BE (PROPOSAL/DECISION); ondas com dependências coerentes; dívida técnica com evidência; nada inventado; nenhum documento vazio.

## Atualização de state.md
"Execuções": data, `architecture-gap-analysis`, nº de lacunas/dívidas, HEAD. "Próximos passos": decisões pendentes do usuário. Se todas as fases 0–7 estão DONE: fase atual → `8-evolution`.
