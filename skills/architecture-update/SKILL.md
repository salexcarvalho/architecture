---
name: architecture-update
description: Mantém a documentação de arquitetura viva. Detecta impacto de mudanças de código (git diff/log desde o último commit revisado), atualiza documentos, propõe ADR, atualiza diagramas e chama a revisão. Use quando o usuário disser "atualizar a arquitetura", "o código mudou, atualize os docs", "documentação desatualizada", "mudança de arquitetura", "sync architecture docs", "update architecture", "docs drift".
---

# architecture-update — documentação viva (fase 8-evolution)

Fluxo: **CODE CHANGE → IMPACTO? → UPDATE DOC → ADR? → UPDATE DIAGRAM → REVIEW**.

## Quando usar
- Mudanças relevantes no código/infra/pipeline desde a última revisão de arquitetura.
- Antes de um release, após uma feature grande, ou quando o `architecture-reviewer` apontou docs obsoletos.
- O usuário descreve uma mudança de arquitetura que ainda não está documentada.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Obter o **último commit revisado** em `state.md` ("Último commit revisado"). Se vazio/inexistente no histórico: avisar e usar o commit da última linha de "Execuções" ou pedir ao usuário um ponto de partida (não inventar).
3. Verificar que o repositório é git: `git rev-parse --is-inside-work-tree`; `git cat-file -e <sha>^{commit}`.
4. Ler `docs/architecture/README.md` (mapa de documentos) e `decisions.md`.

## Passos

### 1. CODE CHANGE — coletar a mudança
```
git log --oneline <sha>..HEAD
git diff --stat <sha>..HEAD
git diff --name-status <sha>..HEAD
```
Para arquivos de interesse, ler apenas o diff relevante (`git diff <sha>..HEAD -- <caminho>`), nunca a árvore inteira. Se houver mudança não commitada relevante, incluir `git status --short` e avisar.

### 2. IMPACTO? — classificar os arquivos alterados

| Mudança detectada | Documentos potencialmente afetados |
|---|---|
| manifests de pacote, framework, módulos novos/removidos | `03-as-is/{architecture,applications}.md`, `04-to-be/{architecture,applications}.md`, `05-diagrams/{container,component}.md` |
| rotas/contratos de API, eventos, clientes de integração | `03-as-is/{applications,integrations}.md`, `04-to-be/integrations.md`, `05-diagrams/flows/*` |
| migrations, schema, ORM | `03-as-is/data.md`, `04-to-be/data.md` |
| Dockerfile, compose, IaC, variáveis de ambiente (nomes) | `03-as-is/infrastructure.md`, `04-to-be/{infrastructure,deployment}.md`, `05-diagrams/deployment.md`, `09-operations/environments.md` |
| pipeline CI/CD, scripts de deploy | `03-as-is/infrastructure.md` (seção CI/CD), `04-to-be/deployment.md`, `09-operations/runbooks.md` |
| autenticação, autorização, criptografia, dados pessoais | `03-as-is/architecture.md` (seção autenticação e segurança observável), `04-to-be/security.md`, `08-security/{threat-model,privacy-lgpd,security-baseline}.md` |
| logs, métricas, tracing | `03-as-is/infrastructure.md` (seção observabilidade), `04-to-be/observability.md`, `09-operations/observability.md` |
| só testes, formatação, comentários, refactor sem mudança estrutural | sem impacto (registrar "sem impacto") |

Se NÃO há impacto: registrar em `state.md` (último commit revisado = HEAD) e encerrar; sem alterar documentos.

### 3. UPDATE DOC — atualizar documentos impactados
- Marcar cada documento: ATUALIZAR / SEM IMPACTO / OBSOLETO (conteúdo contradiz o código).
- Delegar ao especialista do domínio (ver Delegação). Fatos novos → `known-facts.md` (Source `repository`, `arquivo:linha`); fatos que mudaram → antigo `SUPERSEDED por F-NNN`. Renumerar os IDs provisórios `<TIPO>-novo-<n>` do retorno e dos documentos pela regra da skill `architecture` (`grep -rn 'novo-' docs/architecture .architecture` = 0).
- Decisões aceitas (ADR ACCEPTED) que o código contradiz: NÃO editar o ADR; sinalizar ao usuário e abrir ADR substituto (passo 4).
- Atualizar "Última atualização" e a tabela "Histórico" dos documentos, com o commit/PR de origem.
- Documentos que passam a não ter conteúdo: não manter vazios; marcar OBSOLETO e perguntar ao usuário se remove.

### 4. ADR? — a mudança é relevante?
Relevante = afeta estrutura, custo, segurança, dados, operação ou é difícil de reverter. Se sim: propor ADR via `architecture-adr` (PROPOSED; se a mudança já está no código e o usuário a confirma, registrar a confirmação como Evidence antes de ACCEPTED; se contradiz um ADR ACCEPTED, criar ADR que o substitui).

### 5. UPDATE DIAGRAM
Atualizar os diagramas dos documentos alterados (derivados; nota "Derivado de: <doc>"). Nunca desenhar o que o texto não afirma. Diagrama cuja fonte ficou obsoleta: marcar "fora de sincronia" no mapa de derivação.

### 6. REVIEW
Chamar `architecture-review` com escopo = documentos alterados + os que referenciam ADRs afetados. Após revisão sem CRÍTICO aberto: registrar o novo "Último commit revisado".

## Delegação
Especialista por domínio (disparar em paralelo apenas os de arquivos disjuntos; reviewer por último e via `architecture-review`):
`application-architect` (aplicação/integrações/diagramas de contêiner e componente), `data-architect` (dados), `platform-architect` (infra, deploy, observabilidade, operações), `security-privacy-architect` (segurança/privacidade), `architecture-discovery` (atualização do AS-IS). Prompt-base:

```
Fase: 8-evolution (atualização incremental). Raiz: <caminho absoluto>. Intervalo de commits: <sha>..<HEAD>.
Mudanças relevantes (resumo do diff, sem colar arquivos): <lista de arquivos/áreas e o que mudou>.
Documentos a atualizar (ÚNICOS que pode escrever; só arquivos da árvore de `docs/architecture/`): <lista>. Memória: <caminho>/.architecture/ (leia known-facts.md, decisions.md). IDs novos como `<TIPO>-novo-<n>` (a skill renumera).
Tarefa: atualizar SOMENTE o que o diff afeta; manter marcadores inline e IDs; fatos novos com evidência arquivo:linha; não reescrever o que não mudou. Atualizar diagramas derivados dos documentos alterados. Se a mudança contradiz uma decisão ACCEPTED, NÃO edite o ADR: reporte.
Proibido: decidir, criar ADR, marcar ACCEPTED, ler valores de segredos, criar documento sem conteúdo.
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source+evidência) / ## Perguntas sugeridas (≤ 7) / ## ADRs propostos / ## Riscos.
```

## Gate de pergunta
Mudança de comportamento cuja intenção não está clara no diff (por que mudou? é permanente?): perguntar ao usuário antes de documentar como decisão; documentar o fato (KNOWN) e a intenção como `[OPEN]`.

## Saída
- Lista de documentos atualizados, obsoletos e sem impacto; diagramas atualizados; ADRs propostos; relatório de revisão.
- Mensagem ao usuário: resumo do impacto (≤ 15 linhas) e decisões necessárias.

## Critério de conclusão
- `state.md` com o último commit revisado = HEAD revisado; `architecture-update` aponta todos os docs obsoletos; documentos sem contradição com o código; diagramas em sincronia; zero ACCEPTED sem Evidence; nenhum documento vazio.

## Atualização de state.md
Fase `8-evolution`. Atualizar "Último commit revisado" (somente após revisão sem CRÍTICO aberto), "Execuções" (data, `architecture-update`, intervalo `<sha>..<HEAD>`, documentos alterados), "Próximos passos" (docs obsoletos que dependem do usuário) e "Pontos de validação pendentes" (ADRs PROPOSED).
