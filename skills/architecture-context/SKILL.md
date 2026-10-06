---
name: architecture-context
description: Atualiza a memória do projeto (context, known-facts, assumptions, open-questions, risks) com fatos, respostas ou documentos que o usuário trouxe, e consolida requisitos. Use quando o usuário disser "registre isso na memória", "isso é um fato", "atualizar o contexto da arquitetura", "o usuário respondeu", "consolidar requisitos", "update architecture context", "record this decision input".
---

# architecture-context — manutenção da memória

Skill de memória pura: não delega. Dos documentos de `docs/architecture/`, escreve SOMENTE `01-context/{project-context,stakeholders,glossary,assumptions}.md` e `02-requirements/{functional,non-functional,constraints,open-questions}.md` (além de `.architecture/context.md`).

## Quando usar
- O usuário informa um fato/restrição/decisão fora de uma rodada formal de entrevista.
- Uma resposta da entrevista precisa ser propagada para a memória.
- Fase `3-requirements`: consolidar RNFs, restrições e perguntas abertas.
- Reconciliar memória após `architecture-discover` ou `architecture-update`.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Ler `known-facts.md`, `assumptions.md`, `open-questions.md`, `risks.md`, `context.md` (o suficiente para evitar duplicidade e IDs repetidos).

## Passos
1. **Classificar cada informação nova** (uma por linha):

| Origem | Vai para | Status | Source |
|---|---|---|---|
| Achado verificável no repo/doc | `known-facts.md` | KNOWN | repository / documentation |
| Declaração do usuário | `known-facts.md` | KNOWN | user (+ data) |
| Medição/execução | `known-facts.md` | KNOWN | runtime (+ comando, data) |
| Dedução sem confirmação | `assumptions.md` | ASSUMPTION (OPEN) | inferred / architectural analysis |
| Dúvida remanescente | `open-questions.md` | OPEN | — |
| Ameaça/incerteza com impacto | `risks.md` | RISK (OPEN) | fato/hipótese de origem |
| Ideia de decisão | `decisions.md` (Propostas) | PROPOSAL | origem |

2. **Regras de integridade**
   - Inferido NUNCA vira KNOWN. Hipótese confirmada → criar F-NNN novo (Source `user` com data) e marcar A-NNN como `CONFIRMED → F-NNN`.
   - Resposta do usuário que contradiz um fato existente: não apagar; marcar o fato antigo `SUPERSEDED por F-NNN` e registrar o novo. Avisar o usuário da contradição.
   - IDs sequenciais, nunca reutilizados. Todo item tem Source e data.
   - Nunca registrar segredo/valor sensível: redigir `[valor omitido]` e anotar só o nome da variável/serviço.
   - Resposta a Q-NNN: atualizar a pergunta (ANSWERED, resposta resumida, data) e gerar/atualizar o item de memória correspondente.
3. **Fase 3-requirements**: montar `docs/architecture/02-requirements/` (cada arquivo só se tiver conteúdo com fonte; nunca arquivo vazio):
   - `non-functional.md` (modelo: `~/.claude/skills/architecture/templates/non-functional.md`): cada RNF com métrica + alvo + fonte. RNF sem métrica ou fonte NÃO entra como requisito: vira `[OPEN · Q-NNN]` ou `[ASSUMPTION · A-NNN]`.
   - `constraints.md` (modelo: `templates/constraints.md`): restrições duras (RES-NNN) com fonte.
   - `functional.md` (modelo: `templates/functional.md`): só requisitos funcionais com impacto arquitetural (RF-NNN).
   - `open-questions.md`: PROJEÇÃO das perguntas abertas de `.architecture/open-questions.md` que bloqueiam requisitos (mesmos Q-NNN, prioridade e "bloqueia"; formato do template `open-questions.md`). A memória prevalece; não criar pergunta só aqui.
   Não criar `non-functional.md` se não houver ao menos um requisito/restrição com fonte.
   `01-context/` (cabeçalho de `templates/doc-section.md`): `project-context.md` (versão documental de `.architecture/context.md`), `stakeholders.md` (papéis, interesse, fonte), `glossary.md` (termos do domínio com a fonte do significado), `assumptions.md` (PROJEÇÃO de `.architecture/assumptions.md`, mesmos A-NNN e status; modelo `templates/assumptions.md`). Só criar quando houver conteúdo com fonte (ex.: sem stakeholders informados, não criar `stakeholders.md`; registrar a pergunta).
4. **Atualizar `context.md`** (máx. 1 página) refletindo a memória; usar marcadores inline com IDs.
5. Registrar contradições encontradas entre memória e documentos em `open-questions.md` (para `architecture-update`/`architecture-review` tratarem).

## Delegação
Nenhuma (skill sem subagente). Se o volume de informações exigir leitura em massa do repositório, chamar `architecture-discover`.

## Gate de pergunta
Se ao consolidar requisitos faltar item de ALTO impacto (disponibilidade, volume, regulatório, infraestrutura obrigatória, prazo/orçamento, equipe), NÃO assumir: encaminhar para `architecture-interview` com a lista de lacunas já priorizada.

## Saída
- Memória atualizada (`known-facts`, `assumptions`, `open-questions`, `risks`, `context`) e, na fase 3, `02-requirements/{functional,non-functional,constraints,open-questions}.md` e `01-context/*` (somente os com conteúdo); `docs/architecture/README.md` atualizado.
- Resumo ao usuário: N fatos, N hipóteses, N perguntas (abertas/respondidas), N riscos; contradições detectadas.

## Critério de conclusão
- Toda informação nova classificada com Source e data; zero fato sem Source; nenhuma hipótese promovida a fato sem confirmação.
- Fase 3: RNFs com métrica e fonte; restrições listadas; perguntas abertas priorizadas; projeções (`01-context/assumptions.md`, `02-requirements/open-questions.md`) idênticas à memória.

## Atualização de state.md
Registrar execução (data, `architecture-context`, resultado, HEAD). Em fase 3 concluída: `3-requirements` DONE e próxima fase `4-proposal`. Atualizar "Bloqueios" com Q-IDs de alta prioridade ainda abertos.
