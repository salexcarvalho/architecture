---
name: architecture-tech-evaluation
description: Avalia uma tecnologia com critérios objetivos, nota 1-5 com fonte e classificação ADOPT/TRIAL/ASSESS/HOLD/REJECT; proíbe justificativas como "é moderno". Use quando o usuário disser "avaliar tecnologia", "comparar X com Y", "devemos adotar X?", "technology radar", "tech evaluation", "evaluate technology", "compare alternatives".
---

# architecture-tech-evaluation — avaliação de tecnologia

## Quando usar
- Escolha tecnológica relevante (banco, fila, framework, ferramenta de observabilidade, IaC, etc.) ligada a um requisito ou problema real.
- Atualização do technology radar.
- Insumo para um ADR.
- NÃO usar para "curiosidade": sem problema concreto (requisito/fato) a avaliação não começa; perguntar o problema.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Ler `known-facts.md` (tecnologia atual e restrições), `02-requirements/non-functional.md`, `docs/architecture/07-technology/technology-radar.md` (se existir) e avaliações anteriores.
3. Ter claros: TECHNOLOGY, PURPOSE, PROBLEM IT SOLVES, CURRENT ALTERNATIVE (se algum faltar, perguntar — Gate de pergunta).

## Passos
1. Preencher o cabeçalho do template `~/.claude/skills/architecture/templates/tech-evaluation.md`: TECHNOLOGY, PURPOSE, PROBLEM IT SOLVES (ligado a RNF/fato), CURRENT ALTERNATIVE (com evidência) e ALTERNATIVES ANALYZED (≥ 2, incluindo a atual/"não adotar nada").
2. Pesquisar fontes para cada critério: documentação oficial, repositório (releases, issues, licença), avisos de segurança, benchmarks reproduzíveis, fatos do projeto (`known-facts.md`). Usar WebSearch/WebFetch ou docs de biblioteca quando necessário; citar a fonte de cada nota.
3. Pontuar os 15 critérios — maturity, community, maintenance, licensing, security, performance, scalability, operational complexity, learning curve, ecosystem, observability, vendor lock-in, cost, team knowledge, integration effort — com **nota 1–5, justificativa objetiva e fonte**. Critério sem fonte: nota `?` e `[OPEN · Q-NNN]` (ex.: conhecimento da equipe → perguntar). Pesos só se o usuário/requisito os definir (registrar a origem dos pesos).
4. **Justificativas PROIBIDAS** (reescrever com fato verificável ou remover): "é moderno", "todo mundo usa", "é tendência", "é mais rápido" sem medição, "a comunidade gosta", "é o padrão de mercado" sem fonte. O revisor trata como achado.
5. Classificar: **ADOPT** (padrão recomendado), **TRIAL** (piloto limitado, com critério de sucesso e saída), **ASSESS** (investigar, sem compromisso), **HOLD** (não iniciar novos usos), **REJECT** (descartada, com motivo). A classificação decorre das notas e do requisito, não do gosto.
6. Salvar em `docs/architecture/07-technology/evaluations/<tecnologia>.md`. Não criar o arquivo se não houver ao menos o problema, as alternativas e notas com fonte (NÃO criar documento vazio).
7. Atualizar `07-technology/technology-radar.md` (modelo: `~/.claude/skills/architecture/templates/technology-radar.md`), apenas com entradas que têm avaliação ou fato por trás.
8. Se a escolha é relevante: acionar `architecture-adr` para ADR PROPOSED referenciando a avaliação. Registrar riscos novos em `risks.md`. Se a avaliação veio de um especialista, renumerar os IDs provisórios `<TIPO>-novo-<n>` (regra da skill `architecture`).

## Delegação
Opcional: especialista do domínio para a pesquisa técnica pesada. Escolher UM: `application-architect` (framework, integração, mensageria), `data-architect` (bancos, ORM, migração), `platform-architect` (infra, CI/CD, observabilidade), `security-privacy-architect` (identidade, segredos, criptografia). Prompt-base:

```
Fase: <fase atual>. Tarefa: apoio a avaliação de tecnologia (somente pesquisa e proposta; não decide).
TECHNOLOGY: <x>. PROBLEM: <problema + RNF/F relacionados>. CURRENT ALTERNATIVE: <atual, com evidência>. ALTERNATIVES: <lista>.
Contexto mínimo: <caminhos> .architecture/known-facts.md (F-<ids>), docs/architecture/02-requirements/non-functional.md (RNF-<ids>).
Preencha os critérios (nota 1–5 + justificativa + fonte) em: docs/architecture/07-technology/evaluations/<x>.md (modelo: ~/.claude/skills/architecture/templates/tech-evaluation.md). Critério sem fonte: nota "?" e pergunta sugerida.
Proibido justificar com "é moderno", "todo mundo usa", "é tendência". ÚNICO arquivo que você pode escrever neste modo (exceção autorizada à lista de saída do seu agente): o acima; NÃO escreva `technology-radar.md` (a skill o atualiza). Não crie ADR nem marque ACCEPTED. Não crie arquivos fora do indicado. IDs novos como `<TIPO>-novo-<n>` (a skill renumera).
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source) / ## Perguntas sugeridas (≤ 7) / ## ADRs propostos / ## Riscos.
```

## Gate de pergunta
Sem problema concreto, sem alternativa atual ou sem requisito relacionado → perguntar antes de avaliar (`architecture-interview`). Critérios dependentes do usuário (equipe, orçamento, licenças permitidas) → perguntar, não supor.

## Saída
- `07-technology/evaluations/<tecnologia>.md`, `technology-radar.md` atualizado e, quando relevante, ADR PROPOSED.
- Mensagem ao usuário: classificação, 3 razões principais com fonte e perguntas abertas.

## Critério de conclusão
- Problema ligado a requisito/fato; ≥ 2 alternativas (incluindo atual/nenhuma); 15 critérios com nota+justificativa+fonte (ou `?` com pergunta); nenhuma justificativa proibida; classificação coerente com as notas.

## Atualização de state.md
"Execuções": data, `architecture-tech-evaluation`, tecnologia, classificação, HEAD. Se gerou ADR PROPOSED: acrescentar em "Pontos de validação pendentes". A fase atual não muda.
