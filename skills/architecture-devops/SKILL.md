---
name: architecture-devops
description: Arquitetura de CI/CD, ambientes, estratégia de deploy, releases, rollback e runbooks operacionais. Use quando o usuário disser "arquitetura de CI/CD", "pipeline", "estratégia de deploy", "ambientes", "release e rollback", "runbook", "devops architecture", "deployment strategy", "environments".
---

# architecture-devops — CI/CD, ambientes e releases

## Quando usar
- Pipelines, ambientes, promoção entre ambientes, estratégia de deploy, rollback, runbooks.
- Para infraestrutura, observabilidade e DR usar `architecture-infrastructure` (mesmo subagente, arquivos disjuntos).

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Existir AS-IS (`03-as-is/`, em especial a seção CI/CD de `infrastructure.md`). Ler `known-facts.md` (CI, scripts, ambientes), `assumptions.md`, `open-questions.md`, `risks.md`, `decisions.md`, `02-requirements/non-functional.md`.
3. Passar pelo GATE DE PERGUNTA.

## Gate de pergunta
Informação mínima (para `04-to-be/deployment.md`, `09-operations/environments.md`, `09-operations/runbooks.md`): ambientes existentes/desejados; quem aprova releases; janelas de manutenção e tolerância a indisponibilidade; frequência de releases; política de rollback; plataforma de CI/CD imposta; separação de dados entre ambientes. Falta item de ALTO impacto → `architecture-interview` antes de delegar. Antes de perguntar, procurar em `.github`/pipelines, scripts de deploy, compose e docs.

## Passos
1. Definir escopo (pipeline, ambientes, deploy, runbooks).
2. Delegar a `platform-architect` com a divisão de arquivos de devops (abaixo). Se `architecture-infrastructure` rodar junto, disparar as duas numa mesma mensagem (arquivos disjuntos).
3. Reconciliar: memória (IDs finais — renumerar os IDs provisórios `<TIPO>-novo-<n>` nos documentos escritos pelo subagente, conforme a regra da skill `architecture` (conferir `grep -rn 'novo-' docs/architecture` = 0)), ADRs propostos → `architecture-adr`, perguntas filtradas → `architecture-interview` se alto impacto.
4. Conferir: ambientes com propósito claro e paridade documentada; promoção e rollback descritos; runbooks só para cenários reais; apenas nomes de variáveis (nunca valores); complexidade justificada.
5. Atualizar `docs/architecture/README.md`.

## Delegação
Subagente: `platform-architect`. Prompt-base:

```
Fase: <4-proposal | 8-evolution>. Raiz: <caminho absoluto>. Memória: <caminho>/.architecture/ (leia known-facts.md, assumptions.md, open-questions.md, risks.md, decisions.md).
Insumos: pipelines de CI/CD (<caminhos>), scripts de deploy, Dockerfile*, docker-compose*, .env.example (SÓ nomes), docs/architecture/03-as-is/*, docs/architecture/02-requirements/non-functional.md. IDs relevantes: <F-..., RNF-..., Q-...>. Escopo: <pipeline | ambientes | deploy | runbooks>.
Frente "devops". ÚNICOS arquivos que pode escrever: docs/architecture/04-to-be/deployment.md, docs/architecture/09-operations/environments.md, docs/architecture/09-operations/runbooks.md (UM arquivo, uma seção por procedimento). NÃO escreva 04-to-be/infrastructure.md, 04-to-be/observability.md, 09-operations/observability.md, backup-restore.md nem disaster-recovery.md (frente infraestrutura). Não crie arquivo sem conteúdo com fonte.
Cobrir (o que se aplicar): etapas do pipeline (build, testes, análise, empacotamento, deploy) e portões de qualidade; ambientes, propósito, paridade e promoção; estratégia de deploy (ex.: rolling, blue/green, canary — só se justificado) e rollback; gestão de configuração por NOMES de variáveis; migrações de banco no fluxo de release; runbooks de cenários reais.
Regras: você PROPÕE, não decide. NÃO introduza complexidade sem justificativa em requisito; sempre apresente a alternativa mais simples. Escolhas relevantes com ≥ 2 alternativas (incluindo "não mudar"). NUNCA leia/registre valores de segredos. Não crie ADR nem marque ACCEPTED.
Modelos: ~/.claude/skills/architecture/templates/{to-be,environments,runbooks,doc-section}.md.
IDs novos: `P-novo-n`, `Q-novo-n`, `A-novo-n`, `F-novo-n`, `R-novo-n` (a skill renumera).
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source+evidência) / ## Perguntas sugeridas (≤ 7, por impacto) / ## ADRs propostos / ## Riscos.
```

## Saída
- `04-to-be/deployment.md`, `09-operations/environments.md`, `09-operations/runbooks.md` (somente com conteúdo); memória atualizada; ADRs PROPOSED quando relevante.
- Mensagem ao usuário: fluxo de promoção/rollback proposto, riscos e perguntas.

## Critério de conclusão
- Pipeline, ambientes e deploy rastreáveis a fato/requisito; rollback definido; runbooks só para cenários reais; sem segredos; nenhuma complexidade sem justificativa; nenhum documento vazio.

## Atualização de state.md
"Execuções": data, `architecture-devops`, escopo, HEAD, arquivos. Em `4-proposal`: anotar frentes pendentes e Q-IDs críticos em "Bloqueios".
