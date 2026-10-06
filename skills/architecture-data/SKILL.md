---
name: architecture-data
description: Arquitetura de dados, separando CURRENT DATA MODEL de PROPOSED DATA MODEL, com retenção, migração e dados pessoais. Use quando o usuário disser "arquitetura de dados", "modelo de dados", "ERD", "estratégia de migração de banco", "retenção de dados", "data architecture", "data model", "database design review".
---

# architecture-data — arquitetura e modelo de dados

## Quando usar
- Descrever o modelo de dados atual e propor evolução, isoladamente.
- Fase `4-proposal` (parcial) ou `8-evolution` quando migrations/schema mudaram.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Existir AS-IS (`03-as-is/`). Ler `known-facts.md` (SGBD, ORM, migrations), `assumptions.md`, `open-questions.md`, `risks.md`, `decisions.md`, `02-requirements/non-functional.md`.
3. Passar pelo GATE DE PERGUNTA.

## Gate de pergunta
Informação mínima (para `04-to-be/data.md`): entidades atuais (migrations/schema); volume e crescimento; requisitos de consistência/transação; retenção e descarte; existência de dados pessoais/sensíveis; necessidades analíticas/relatórios; integrações que leem/escrevem dados. Falta item de ALTO impacto (volume, dados pessoais, retenção) → `architecture-interview` antes de delegar. Antes de perguntar, procurar em migrations, ORM, `docker-compose`, scripts e docs.

## Passos
1. Definir escopo (todo o modelo, um domínio, uma migração).
2. Delegar a `data-architect` (prompt abaixo).
3. Reconciliar: memória (IDs finais — renumerar os IDs provisórios `<TIPO>-novo-<n>` nos documentos escritos pelo subagente, conforme a regra da skill `architecture` (conferir `grep -rn 'novo-' docs/architecture` = 0)), ADRs propostos → `architecture-adr` (PROPOSED), perguntas filtradas → `architecture-interview` se alto impacto.
4. Conferir: CURRENT só com KNOWN e evidência; PROPOSED com status DRAFT/PROPOSAL/OPEN por entidade; nada não confirmado marcado como decisão; dados pessoais classificados; migração com rollback.
5. Atualizar `docs/architecture/README.md`.

## Delegação
Subagente: `data-architect`. Prompt-base:

```
Fase: <4-proposal | 8-evolution>. Raiz: <caminho absoluto>. Memória: <caminho>/.architecture/ (leia known-facts.md, assumptions.md, open-questions.md, risks.md, decisions.md).
Insumos: migrations (<pasta>), schema/ORM (<pasta>), docs/architecture/03-as-is/*, docs/architecture/02-requirements/non-functional.md. IDs relevantes: <F-..., RNF-..., Q-...>. Escopo: <modelo inteiro | domínio X | migração Y>.
ÚNICOS arquivos que pode escrever: docs/architecture/03-as-is/data.md (complemento) e docs/architecture/04-to-be/data.md. Não crie arquivo sem conteúdo com fonte.
Estruture 04-to-be/data.md em CURRENT DATA MODEL (só KNOWN, com evidência de migration/schema/ORM) e PROPOSED DATA MODEL (cada entidade/campo novo com status DRAFT | PROPOSAL | OPEN, motivo e impacto de migração). Inclua: classificação de dados pessoais, retenção/descarte, estratégia de migração com rollback, índices/particionamento só com evidência de necessidade, diagramas erDiagram (Mermaid) derivados.
Regras: você PROPÕE, não decide. Não feche o modelo sem evidência; não marque como decisão o que não foi confirmado (usar DRAFT/PROPOSAL/OPEN). Escolhas relevantes com ≥ 2 alternativas. Não registre dados reais nem valores de segredos. Não crie ADR nem marque ACCEPTED.
Modelos: ~/.claude/skills/architecture/templates/{data-model,doc-section}.md.
IDs novos: `P-novo-n`, `Q-novo-n`, `A-novo-n`, `F-novo-n`, `R-novo-n` (a skill renumera).
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source+evidência) / ## Perguntas sugeridas (≤ 7, por impacto) / ## ADRs propostos / ## Riscos.
```

## Saída
- `03-as-is/data.md` (complemento) e `04-to-be/data.md` (somente com conteúdo); memória atualizada; ADRs PROPOSED quando relevante.
- Mensagem ao usuário: diferenças CURRENT × PROPOSED, riscos e perguntas.

## Critério de conclusão
- CURRENT sem item sem evidência; PROPOSED com status por entidade; dados pessoais classificados (ou `[OPEN]`); migração com rollback; nenhum documento vazio; nenhuma decisão inventada.

## Atualização de state.md
"Execuções": data, `architecture-data`, escopo, HEAD, arquivos. Em `4-proposal`: anotar frentes pendentes e Q-IDs de alta prioridade em "Bloqueios".
