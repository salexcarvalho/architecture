---
name: architecture-generate
description: Produz ou atualiza a arquitetura TO-BE completa orquestrando os especialistas em ordem e em paralelo (application, data, platform, depois security, e reviewer por último). Use quando o usuário disser "gerar a arquitetura proposta", "gerar o TO-BE", "montar a documentação de arquitetura", "gerar docs de arquitetura", "generate target architecture", "produce to-be docs".
---

# architecture-generate — geração do TO-BE (orquestração de especialistas)

## Quando usar
- Fase `4-proposal` (primeira geração) ou `6-documentation` (consolidação após validação).
- Regeneração ampla após mudança grande de requisitos. Para mudança pontual de código, usar `architecture-update`.
- Para um domínio isolado, usar `architecture-api`, `architecture-data`, `architecture-infrastructure`, `architecture-devops` ou `architecture-security`.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Fase mínima: `3-requirements` DONE (existe `02-requirements/non-functional.md` (e `constraints.md`) com RNFs com métrica e fonte, e AS-IS em `03-as-is/`).
3. Ler a memória: `known-facts.md`, `assumptions.md`, `open-questions.md`, `risks.md`, `decisions.md`, `context.md`.
4. Aplicar o GATE DE PERGUNTA (abaixo) antes de delegar.

## Gate de pergunta
Para cada documento a gerar, checar a informação mínima (tabela na skill `architecture`). Falta item de ALTO impacto → NÃO delegar o documento correspondente; chamar `architecture-interview` primeiro (uma rodada, 3–7 perguntas). Itens de média/baixa prioridade não bloqueiam: entram como `[ASSUMPTION]`/`[OPEN]` nos documentos.

## Passos

### Ordem de execução e paralelismo
```
requisitos prontos (non-functional.md) ──┬─► application-architect ─┐
                              ├─► data-architect        ─┼─► security-privacy-architect ─► architecture-reviewer
                              └─► platform-architect    ─┘        (lê os 3 resultados)        (por último)
```
1. **Onda 1 (paralelo):** `application-architect`, `data-architect`, `platform-architect` — disparados numa ÚNICA mensagem, pois escrevem arquivos disjuntos (ver Delegação). Omitir um especialista se o seu domínio não tem conteúdo com fonte nem pedido do usuário.
2. **Consolidar perguntas:** reunir "Perguntas sugeridas" dos retornos; remover as respondíveis pelo repo/memória; deduplicar; priorizar por impacto. Se houver pergunta de ALTO impacto: UMA rodada de `architecture-interview` (3–7 perguntas, consolidadas de todos os especialistas) e, depois das respostas, re-delegar apenas os especialistas afetados.
3. **Onda 2 (série):** `security-privacy-architect`, lendo os resultados das três frentes (não paralelizar com a onda 1: depende deles).
4. **Reconciliar memória:** promover os itens de "Memória" dos retornos para `known-facts.md`/`assumptions.md`/`open-questions.md`/`risks.md`/`decisions.md` (Propostas P-NNN); IDs finais atribuídos aqui (os IDs `<TIPO>-novo-<n>` dos subagentes são provisórios): aplicar a regra de renumeração da skill `architecture` (substituir arquivo por arquivo nos documentos de cada subagente e conferir `grep -rn 'novo-' docs/architecture .architecture` = 0). Atualizar também as projeções `01-context/assumptions.md` e `02-requirements/open-questions.md` se existirem.
5. **ADRs:** para cada "ADR proposto" relevante (afeta estrutura, custo, segurança, dados, operação ou é difícil de reverter), acionar `architecture-adr` para criar ADR PROPOSED. Subagentes NUNCA criam ADR nem marcam ACCEPTED.
6. **Onda 3:** `architecture-reviewer` por último (independência: revisa o que outros escreveram) — via `architecture-review`.
7. Atualizar `docs/architecture/README.md` (somente documentos existentes; pendentes na seção própria).
8. **PARAR para validação do usuário:** apresentar a proposta (componentes, alternativas, ADRs PROPOSED, riscos, perguntas abertas) e pedir aprovação explícita por item. Não marcar nada como aprovado sem resposta registrada.

### Regras de escrita
- Tudo que é proposta: `[PROPOSAL · P-NNN]`; fato: `[KNOWN · F-NNN]`; pendente: `[OPEN · Q-NNN]`.
- Cada elemento do TO-BE rastreável a requisito, fato ou restrição; escolhas relevantes com ≥ 2 alternativas.
- Complexidade (ex.: orquestradores de contêineres, microsserviços, filas) só com justificativa registrada.
- NÃO CRIAR DOCUMENTO VAZIO: arquivo sem conteúdo com fonte não é criado; vira linha em "Pendentes" do README e pergunta em `open-questions.md`.
- Diagramas derivados dos documentos (nota "Derivado de").

## Delegação
Prompt-base comum (preencher `<...>`; contexto mínimo: não colar arquivos inteiros, passar caminhos e IDs):

```
Fase: 4-proposal. Raiz: <caminho absoluto>. Memória: <caminho>/.architecture/ (leia: context.md, known-facts.md, assumptions.md, open-questions.md, decisions.md, risks.md).
Insumos: docs/architecture/03-as-is/*, docs/architecture/02-requirements/{non-functional,constraints,functional}.md e docs/architecture/01-context/* (os que existirem). IDs relevantes: <F-..., A-..., Q-..., RNF-...>.
Seu escopo e ÚNICOS arquivos que pode escrever: <lista conforme especialista>.
Regras: você PROPÕE, não decide. Marque propostas como [PROPOSAL · P-NNN] (IDs provisórios `P-novo-1`, `P-novo-2`...; o mesmo para `F-novo-n`, `A-novo-n`, `Q-novo-n`, `R-novo-n`), fatos como [KNOWN · F-NNN], pendências como [OPEN · Q-NNN]. Cada elemento rastreável a requisito/fato. Escolhas relevantes: ≥ 2 alternativas (incluindo "não mudar" quando cabível). Não crie documento sem conteúdo com fonte. Não escreva em 06-decisions/ nem marque ACCEPTED. Nunca leia/registre valores de segredos. Modelos: ~/.claude/skills/architecture/templates/ (<templates específicos>).
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source+evidência) / ## Perguntas sugeridas (≤ 7, por impacto, citando achado) / ## ADRs propostos / ## Riscos.
```

Especialização por especialista:

| Subagente | Arquivos que pode escrever | Templates |
|---|---|---|
| `application-architect` | `04-to-be/{architecture,applications,integrations}.md`, `05-diagrams/{context,container,component}.md`, `05-diagrams/flows/<fluxo>.md` | `to-be.md`, `diagrams.md` |
| `data-architect` | `03-as-is/data.md` (complemento), `04-to-be/data.md` | `data-model.md` |
| `platform-architect` | `04-to-be/{infrastructure,observability,deployment}.md`, `05-diagrams/deployment.md`, `09-operations/{environments,observability,backup-restore,disaster-recovery,runbooks}.md` | `to-be.md`, `environments.md`, `backup-restore.md`, `disaster-recovery.md`, `runbooks.md`, `diagrams.md` |
| `security-privacy-architect` (onda 2; adicionar: "leia também os resultados dos três especialistas anteriores") | `04-to-be/security.md`, `08-security/{threat-model,privacy-lgpd,security-baseline}.md` | `to-be.md`, `threat-model.md`, `security-baseline.md`, `privacy-lgpd.md` |

## Saída
- Documentos TO-BE (somente os com conteúdo), diagramas derivados, memória atualizada, ADRs PROPOSED, README atualizado, relatório de revisão (`.architecture/reviews/REVIEW-AAAA-MM-DD.md`).
- Mensagem ao usuário: proposta resumida (≤ 20 linhas), pedido de aprovação explícita por item, perguntas abertas de alto impacto.

## Critério de conclusão
- Cada elemento TO-BE rastreável a requisito/fato; alternativas consideradas para escolhas relevantes; propostas marcadas PROPOSAL; ADRs PROPOSED; nenhum documento vazio; nenhuma decisão inventada.
- Documentos sem contradição com a memória e com o código; diagramas derivados.

## Atualização de state.md
Fase → `4-proposal` DONE e `5-validation` OPEN (aguardando o usuário). "Execuções": data, `architecture-generate`, especialistas acionados, HEAD. "Pontos de validação pendentes": "Aprovar proposta TO-BE (itens P-..., ADR-...)". "Bloqueios": Q-IDs de alto impacto.
