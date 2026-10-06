---
name: architecture-api
description: Arquitetura de aplicação, APIs, contratos, eventos e integrações (síncronas e assíncronas), com resiliência e diagramas C4/sequência. Use quando o usuário disser "arquitetura de APIs", "desenhar integrações", "contratos de API", "eventos e filas", "arquitetura da aplicação", "diagrama de contêineres/componentes", "design the API architecture", "integration architecture".
---

# architecture-api — aplicação, APIs e integrações

## Quando usar
- Gerar ou atualizar a arquitetura de aplicação e integrações isoladamente (sem rodar o fluxo completo).
- Fase `4-proposal` (parcial) ou `8-evolution` quando contratos/integrações mudaram.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Existir AS-IS em `03-as-is/` (senão: `architecture-discover`). Ler `known-facts.md`, `assumptions.md`, `open-questions.md`, `risks.md`, `decisions.md`, `02-requirements/non-functional.md` (se existir).
3. Passar pelo GATE DE PERGUNTA.

## Gate de pergunta
Informação mínima (para `04-to-be/{architecture,applications,integrations}.md`): AS-IS descoberto; RNFs com métrica (disponibilidade, latência, volume); integrações obrigatórias e seus donos; padrões corporativos impostos (protocolos, identidade); equipe/competências. Falta item de ALTO impacto → `architecture-interview` antes de delegar. Aplicar a busca antes de perguntar (compose, `.env.example`, manifests, código, docs, CI).

## Passos
1. Definir o escopo: aplicação inteira, uma integração, ou um contrato.
2. Delegar a `application-architect` (prompt abaixo).
3. Reconciliar o retorno: itens de memória → arquivos de `.architecture/` com IDs finais — renumerar os IDs provisórios `<TIPO>-novo-<n>` nos documentos escritos pelo subagente, conforme a regra da skill `architecture` (conferir `grep -rn 'novo-' docs/architecture` = 0); ADRs propostos → `architecture-adr` (PROPOSED); perguntas sugeridas → filtrar (busca antes de perguntar) e levar a `architecture-interview` se alto impacto.
4. Conferir: cada componente/integração rastreável a requisito/fato; resiliência (timeout, retry, idempotência, fallback) nas integrações; alternativas para escolhas relevantes; diagramas derivados.
5. Atualizar `docs/architecture/README.md`.

## Delegação
Subagente: `application-architect`. Prompt-base:

```
Fase: <4-proposal | 8-evolution>. Raiz: <caminho absoluto>. Memória: <caminho>/.architecture/ (leia known-facts.md, assumptions.md, open-questions.md, risks.md, decisions.md).
Insumos: docs/architecture/03-as-is/*, docs/architecture/02-requirements/non-functional.md. IDs relevantes: <F-..., RNF-..., Q-...>. Escopo: <aplicação | integração X | contrato Y>.
ÚNICOS arquivos que pode escrever: docs/architecture/04-to-be/{architecture,applications,integrations}.md, docs/architecture/05-diagrams/{context,container,component}.md, docs/architecture/05-diagrams/flows/*. Só crie arquivo se houver conteúdo com fonte (NÃO crie documento vazio).
Cobrir (o que se aplicar): estilo arquitetural e fronteiras de módulos; APIs e contratos (versionamento, erros, paginação, idempotência); eventos/filas; integrações com resiliência (timeout, retry com backoff, circuit breaker, fallback, reprocessamento); autenticação entre serviços (apenas desenho, segurança detalhada é de outro especialista); diagramas C4 (C4Context, C4Container, C4Component) e sequência, derivados dos documentos (nota "Derivado de: <doc>").
Regras: você PROPÕE, não decide. [PROPOSAL · P-NNN] para propostas, [KNOWN · F-NNN] para fatos, [OPEN · Q-NNN] para pendências (IDs ainda inexistentes: `P-novo-n`, `Q-novo-n`, `A-novo-n`, `F-novo-n`, `R-novo-n`). Escolhas relevantes com ≥ 2 alternativas (incluindo "não mudar"). Complexidade (microsserviços, filas, orquestradores) só com justificativa registrada. Não toque dados/infra/segurança além das interfaces. Não crie ADR nem marque ACCEPTED. Nunca leia/registre valores de segredos.
Modelos: ~/.claude/skills/architecture/templates/{to-be,diagrams,doc-section}.md.
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source+evidência) / ## Perguntas sugeridas (≤ 7, por impacto) / ## ADRs propostos / ## Riscos.
```

## Saída
- `04-to-be/{architecture,applications,integrations}.md`, `05-diagrams/{context,container,component}.md`, `05-diagrams/flows/*` (somente os com conteúdo); memória atualizada; ADRs PROPOSED quando relevante.
- Mensagem ao usuário: resumo da proposta, alternativas, perguntas abertas.

## Critério de conclusão
- Componentes e integrações rastreáveis a requisito/fato; alternativas consideradas; propostas marcadas PROPOSAL; diagramas derivados e coerentes; nenhum documento vazio; nenhuma decisão inventada.

## Atualização de state.md
"Execuções": data, `architecture-api`, escopo, HEAD, arquivos. Em `4-proposal`: manter a fase até as demais frentes concluírem (ver `architecture-generate`); anotar em "Próximos passos" as frentes pendentes e perguntas abertas.
