---
name: architecture-review
description: Revisão independente da documentação de arquitetura (coerência, evidência, ADRs, diagramas, segurança) por um revisor que nunca revisa o que ele mesmo escreveu. Use quando o usuário disser "revisar a arquitetura", "revisão independente", "validar os documentos de arquitetura", "o que está inconsistente", "review architecture", "architecture review", "audit architecture docs".
---

# architecture-review — revisão independente

## Quando usar
- Fase `7-review` (após documentação), depois de `architecture-generate`, `architecture-update` ou mudança grande de ADRs.
- Sob demanda: "a documentação está consistente?".

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Existir ao menos um documento em `docs/architecture/` (04-to-be, 06-decisions ou 03-as-is). Se não houver nada a revisar: informar e parar (não gerar relatório vazio).
3. Ler `decisions.md` e a lista de documentos do `docs/architecture/README.md` para definir o ESCOPO. Ler o último `reviews/REVIEW-*.md` para acompanhar achados abertos.

## Passos
1. Definir o escopo (todos os documentos, ou lista) e o commit de referência (`git rev-parse --short HEAD`).
2. Delegar a `architecture-reviewer` (prompt abaixo). O revisor é independente: NÃO usar o mesmo subagente que escreveu os documentos e NÃO editar os documentos na mesma execução.
3. Ler o relatório em `.architecture/reviews/REVIEW-AAAA-MM-DD.md` e o retorno do subagente. Registrar na memória os itens novos do retorno (`R-novo-n` → `risks.md`, perguntas → `open-questions.md`), com IDs finais pela regra de IDs provisórios da skill `architecture`; os achados `RV-NNN` ficam só no relatório.
4. Triar os achados com o usuário:
   - CRÍTICO: bloqueia aprovação. Corrigir (via skill do domínio / `architecture-update`) OU o usuário aceita explicitamente como risco → registrar em `risks.md` (status ACCEPTED, data e resposta).
   - ALTO/MÉDIO/BAIXO: lista priorizada; correção na próxima atualização.
5. Perguntas sugeridas pelo revisor: filtrar pela regra de busca antes de perguntar; levar as relevantes para uma rodada de `architecture-interview`.
6. Após correções, solicitar nova revisão apenas do escopo corrigido (re-review).
7. Atualizar o status dos documentos revisados (DRAFT → REVIEWED) somente se não houver CRÍTICO aberto naquele documento; `APPROVED` apenas com aprovação explícita do usuário (registrada).

## Delegação
Subagente: `architecture-reviewer`. Prompt-base:

```
Fase: 7-review. Você é revisor independente: NÃO edite nenhum documento revisado; escreva APENAS o relatório de saída.
Raiz: <caminho absoluto>. Commit: <sha>.
Escopo: <lista de documentos em docs/architecture/> + memória .architecture/ (known-facts, assumptions, open-questions, decisions, risks, interview-log).
Último relatório (para acompanhar achados abertos): <caminho ou "nenhum">.
Verifique (checklist do modelo ~/.claude/skills/architecture/templates/review-report.md):
 1) todo fato com Source e evidência; 2) nada inferido marcado KNOWN; 3) nenhum ADR ACCEPTED sem Evidence; 4) nenhuma proposta marcada como decisão; 5) sem contradição entre documentos, memória e código (verifique por amostragem no repositório); 6) diagramas derivados e coerentes com o texto; 7) nenhum documento vazio/placeholder; 8) nenhum segredo exposto; 9) escolhas relevantes com ≥ 2 alternativas e ADR; 10) complexidade com justificativa registrada; 11) afirmações de conformidade de privacidade com evidência; 12) justificativas proibidas ("é moderno", "todo mundo usa"); 13) `docs/architecture/` contém somente arquivos da árvore definida (ver README do índice), ADRs só em `06-decisions/`, nenhum ID provisório `-novo-` restante e projeções (`01-context/assumptions.md`, `02-requirements/open-questions.md`) coerentes com a memória.
Severidade: CRÍTICO | ALTO | MÉDIO | BAIXO. Cada achado: documento/trecho, regra violada, evidência, correção sugerida.
Escreva: .architecture/reviews/REVIEW-<AAAA-MM-DD>.md (modelo: ~/.claude/skills/architecture/templates/review-report.md). Liste também docs possivelmente obsoletos (código mudou).
Retorne ≤ 40 linhas: ## Escrito / ## Memória (itens com Status/Source que faltam ou conflitam) / ## Perguntas sugeridas (≤ 7) / ## ADRs propostos / ## Riscos (achados CRÍTICO resumidos).
```

## Gate de pergunta
Antes de revisar: o escopo e o commit estão definidos? Há decisões aguardando aprovação que impeçam a revisão de ADRs? (Revisão pode prosseguir; ADRs PROPOSED são apenas listados.)

## Saída
- `.architecture/reviews/REVIEW-AAAA-MM-DD.md` e resumo ao usuário: veredito, nº de achados por severidade, os CRÍTICO/ALTO em 1 linha cada e decisões pedidas.

## Critério de conclusão
- Relatório sem itens CRÍTICO abertos, ou CRÍTICO explicitamente aceitos pelo usuário como risco (registrados em `risks.md` com data).
- Docs sem contradição com memória e código; nenhum documento vazio.

## Atualização de state.md
"Execuções": data, `architecture-review`, veredito, nº CRÍTICO abertos, HEAD. Fase `7-review` DONE quando o critério for cumprido; próxima fase: `8-evolution` (e `architecture-gap-analysis` se ainda não rodou). Registrar "Último commit revisado" = HEAD revisado.
