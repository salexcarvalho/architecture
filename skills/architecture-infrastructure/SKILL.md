---
name: architecture-infrastructure
description: Arquitetura de infraestrutura (hospedagem, rede, contêineres, capacidade, observabilidade, backup e recuperação de desastres), sem introduzir complexidade sem justificativa. Use quando o usuário disser "arquitetura de infraestrutura", "desenhar a infra", "hospedagem", "backup e restore", "observabilidade", "disaster recovery", "infrastructure architecture", "capacity planning".
---

# architecture-infrastructure — infraestrutura, observabilidade e DR

## Quando usar
- Infra, hospedagem, rede, capacidade, observabilidade, backup/restore, DR.
- Para pipelines, ambientes e releases usar `architecture-devops` (mesmo subagente, arquivos disjuntos).

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Existir AS-IS (`03-as-is/`). Ler `known-facts.md` (compose, IaC, hospedagem), `assumptions.md`, `open-questions.md`, `risks.md`, `decisions.md`, `02-requirements/non-functional.md`.
3. Passar pelo GATE DE PERGUNTA.

## Gate de pergunta
Informação mínima (para `04-to-be/{infrastructure,observability}.md` e `09-operations/{observability,backup-restore,disaster-recovery}.md`): infraestrutura obrigatória (nuvem/on-premises/híbrido, provedor imposto); disponibilidade esperada; RPO/RTO; orçamento; quem opera e com que competência; volume/pico; requisitos regulatórios de localização de dados. Falta item de ALTO impacto → `architecture-interview` antes de delegar. Antes de perguntar, procurar em Dockerfile, compose, IaC, scripts, CI e docs.

## Passos
1. Definir escopo (infra inteira, observabilidade, backup/DR, capacidade).
2. Delegar a `platform-architect` com a divisão de arquivos de infraestrutura (abaixo). Se `architecture-devops` for rodada junto, disparar as duas delegações numa mesma mensagem: os arquivos são disjuntos.
3. Reconciliar: memória (IDs finais — renumerar os IDs provisórios `<TIPO>-novo-<n>` nos documentos escritos pelo subagente, conforme a regra da skill `architecture` (conferir `grep -rn 'novo-' docs/architecture` = 0)), ADRs propostos → `architecture-adr`, perguntas filtradas → `architecture-interview` se alto impacto.
4. Conferir: toda complexidade (ex.: orquestradores de contêineres, multi-região, malha de serviços) tem justificativa registrada por requisito; RPO/RTO com fonte; backup só "existe" com restore testado (senão `[RISK]`); sem segredos.
5. Atualizar `docs/architecture/README.md`.

## Delegação
Subagente: `platform-architect`. Prompt-base:

```
Fase: <4-proposal | 8-evolution>. Raiz: <caminho absoluto>. Memória: <caminho>/.architecture/ (leia known-facts.md, assumptions.md, open-questions.md, risks.md, decisions.md).
Insumos: Dockerfile*, docker-compose*, IaC, scripts, docs/architecture/03-as-is/*, docs/architecture/02-requirements/non-functional.md. IDs relevantes: <F-..., RNF-..., Q-...>. Escopo: <infra | observabilidade | backup/DR | capacidade>.
Frente "infraestrutura". ÚNICOS arquivos que pode escrever: docs/architecture/04-to-be/{infrastructure,observability}.md, docs/architecture/05-diagrams/deployment.md, docs/architecture/09-operations/{observability,backup-restore,disaster-recovery}.md. NÃO escreva 04-to-be/deployment.md, 09-operations/environments.md nem 09-operations/runbooks.md (frente devops; cenários de infra/DR entram em disaster-recovery.md, e a frente devops os referencia em runbooks.md). Não crie arquivo sem conteúdo com fonte.
Cobrir (o que se aplicar): topologia e hospedagem; rede e exposição; capacidade e dimensionamento (com base em RNF; sem número inventado); observabilidade (logs, métricas, tracing, alertas — foco operacional); backup/restore com RPO/RTO, retenção e TESTES de restore; cenários de DR; diagrama de deployment (Mermaid) derivado.
Regras: você PROPÕE, não decide. NÃO introduza complexidade (ex.: Kubernetes, multi-região, malha de serviços) sem justificativa registrada em requisito; sempre apresente a alternativa mais simples. Escolhas relevantes com ≥ 2 alternativas (incluindo "não mudar"). Leia apenas NOMES de variáveis, NUNCA valores de segredos. Não crie ADR nem marque ACCEPTED.
Modelos: ~/.claude/skills/architecture/templates/{to-be,backup-restore,disaster-recovery,diagrams,doc-section}.md.
IDs novos: `P-novo-n`, `Q-novo-n`, `A-novo-n`, `F-novo-n`, `R-novo-n` (a skill renumera).
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source+evidência) / ## Perguntas sugeridas (≤ 7, por impacto) / ## ADRs propostos / ## Riscos.
```

## Saída
- `04-to-be/{infrastructure,observability}.md`, `05-diagrams/deployment.md`, `09-operations/{observability,backup-restore,disaster-recovery}.md` (somente com conteúdo); memória atualizada; ADRs PROPOSED quando relevante.
- Mensagem ao usuário: proposta resumida, justificativa de cada complexidade, perguntas.

## Critério de conclusão
- Cada componente de infra rastreável a requisito/fato; RPO/RTO com fonte ou `[OPEN]`; restore testado ou `[RISK]`; nenhuma complexidade sem justificativa; nenhum documento vazio; nada inventado.

## Atualização de state.md
"Execuções": data, `architecture-infrastructure`, escopo, HEAD, arquivos. Em `4-proposal`: anotar frentes pendentes e Q-IDs críticos em "Bloqueios".
