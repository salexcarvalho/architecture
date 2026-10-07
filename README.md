# Claude Architecture Framework

Conjunto global de subagentes e skills do Claude Code para levantar, analisar, questionar, propor, documentar, revisar e evoluir a arquitetura de qualquer repositório.

O framework conhece o **método**, não o projeto. O contexto de cada projeto é descoberto no próprio repositório (código, docs, configs, migrations, CI/CD, git) e nas respostas do arquiteto, e fica salvo em `.architecture/` dentro do projeto.

## Princípio

```
DESCOBRIR → LER → CONHECIDO → LACUNAS → PERGUNTAR → REGISTRAR
→ ALTERNATIVAS → PROPOR → VALIDAR → DOCUMENTAR → REVISAR → EVOLUIR
```

- Nada é inventado. Tudo tem `Status` (KNOWN, UNKNOWN, ASSUMPTION, PROPOSAL, DECISION, RISK, OPEN QUESTION) e `Source` (repository, documentation, user, runtime, inferred).
- Proposta só vira decisão com evidência de aprovação. ADR `ACCEPTED` exige `Evidence`.
- Antes de perguntar, procura no repositório. Perguntas em blocos de 3 a 7, priorizadas por impacto.

## Conteúdo

| Pasta | O que é |
|---|---|
| `agents/` | 7 subagentes: `architecture-discovery`, `application-architect`, `data-architect`, `platform-architect`, `security-privacy-architect`, `architecture-reviewer`, `architecture-documenter` |
| `skills/` | 17 skills: `architecture` (entrada) e `architecture-{start,context,discover,interview,generate,api,data,infrastructure,devops,security,adr,tech-evaluation,review,gap-analysis,update,pdf}` |
| `skills/architecture/templates/` | 30 templates (memória, documentos, ADR, avaliação de tecnologia, diagramas C4 em Mermaid) e a pasta `architecture-document/` (template, CSS e gerador do PDF 42010) |
| `docs/ANALISE.md` | análise crítica e desenho (divisão de responsabilidades, fluxo, memória, entrevista, critérios de conclusão) |
| `docs/SPEC.md` | especificação usada para gerar os arquivos |
| `install.sh` | instala em `~/.claude/` com backup do que já existir |

## Instalação

```bash
bash install.sh --dry-run   # mostra o que seria instalado
bash install.sh             # instala em ~/.claude/agents e ~/.claude/skills
```

Arquivos com o mesmo nome já existentes são salvos em `~/.claude/arch-framework-backup-<data>/` antes de serem substituídos.

## Uso

Dentro de qualquer repositório, numa sessão do Claude Code:

> Vamos construir a arquitetura inicial deste projeto.

A skill `architecture` lê `.architecture/state.md`, decide a fase e conduz o fluxo, parando nos pontos de validação com você. Cada etapa também pode ser chamada direto (`/architecture-interview`, `/architecture-adr`, `/architecture-review`, ...).

## Documento de arquitetura em PDF (ISO/IEC/IEEE 42010)

A skill `architecture-pdf` (subagente `architecture-documenter`) consolida `.architecture/` e `docs/architecture/` em um PDF A4 no formato 42010: capa, sumário, identificação, stakeholders, concerns, viewpoints, visões lógica, de processos, de implantação e de informação, decisões, justificativas, conformidade e referências. Escopo à escolha: arquitetura atual, proposta ou ambas. ADR aceito vira "Decisão"; proposto vira "Proposta"; o que não tem fonte vira "A definir" com pergunta registrada. O PDF vai para `docs/arquitetura/` (fora da árvore fixa `docs/architecture/`).

```bash
# uma vez (local, nada global): venv com weasyprint + markdown, npm com mermaid + playwright-core, em ~/.cache/architecture-pdf
bash ~/.claude/skills/architecture/templates/architecture-document/setup.sh
```

Pré-requisitos do sistema: Python 3 com Pango (WeasyPrint), Node/npm, um Chromium já instalado (Playwright, Chrome ou Chromium; o script não baixa navegador) e `poppler-utils` (`pdfinfo`, `pdftoppm`). Guia de formato, sintaxe e opções em `skills/architecture/templates/architecture-document/README.md`. A publicação da wiki limpa e do deck para o cliente é outra skill (`architecture-publish`), mantida à parte.

## Saída no projeto

- `.architecture/` — memória: `state.md`, `context.md`, `known-facts.md`, `assumptions.md`, `open-questions.md`, `decisions.md`, `risks.md`, `interview-log.md`, `reviews/`.
- `docs/architecture/` — documentação (`01-context` a `10-roadmap`), criada só quando há conteúdo real.
- `docs/arquitetura/` — documento de arquitetura em PDF (e o Markdown-fonte), gerado por `architecture-pdf`.

## Evolução do framework

Edite os arquivos aqui, rode `bash install.sh` de novo e versione a mudança. Nada específico de projeto entra neste repositório.
