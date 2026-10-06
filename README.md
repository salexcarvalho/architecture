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
| `agents/` | 6 subagentes: `architecture-discovery`, `application-architect`, `data-architect`, `platform-architect`, `security-privacy-architect`, `architecture-reviewer` |
| `skills/` | 16 skills: `architecture` (entrada) e `architecture-{start,context,discover,interview,generate,api,data,infrastructure,devops,security,adr,tech-evaluation,review,gap-analysis,update}` |
| `skills/architecture/templates/` | 30 templates (memória, documentos, ADR, avaliação de tecnologia, diagramas C4 em Mermaid) |
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

## Saída no projeto

- `.architecture/` — memória: `state.md`, `context.md`, `known-facts.md`, `assumptions.md`, `open-questions.md`, `decisions.md`, `risks.md`, `interview-log.md`, `reviews/`.
- `docs/architecture/` — documentação (`01-context` a `10-roadmap`), criada só quando há conteúdo real.

## Evolução do framework

Edite os arquivos aqui, rode `bash install.sh` de novo e versione a mudança. Nada específico de projeto entra neste repositório.
