---
name: architecture-discover
description: (Re)descobre a arquitetura AS-IS lendo o repositório, com evidência por item e sem julgamento. Use quando o usuário disser "descobrir a arquitetura atual", "mapear o AS-IS", "reanalisar o repositório", "o que existe hoje no sistema", "rediscover", "discover current architecture", "map as-is".
---

# architecture-discover — descoberta (ou redescoberta) do AS-IS

## Quando usar
- Fase `1-discovery` incompleta, ou AS-IS desatualizado (mudanças grandes no código/infra).
- Complemento direcionado: "descubra só a parte de dados/integrações/CI".
- Para atualização incremental guiada por diff, preferir `architecture-update`.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Ler `known-facts.md` (para não duplicar fatos) e `docs/architecture/03-as-is/*` existentes.
3. Definir o ESCOPO da descoberta: completo, ou lista de áreas (stack, módulos, dados, integrações, infra, CI/CD, observabilidade, testes).

## Passos
1. Determinar escopo e commit de referência (`git rev-parse --short HEAD`).
2. Delegar a `architecture-discovery` (prompt abaixo). Para repositórios muito grandes (monorepo), dividir por áreas e disparar VÁRIAS delegações em paralelo (numa mesma mensagem), cada uma com escopo disjunto de arquivos de saída.
3. Consolidar o retorno:
   - Fatos: já gravados pelo subagente na seção discovery de `known-facts.md` (F-NNN finais; fatos existentes confirmados mantêm ID; fatos que deixaram de valer → `SUPERSEDED por F-NNN`). Conferir IDs únicos (em execuções paralelas, cada uma recebe uma faixa disjunta, ex.: F-101..F-150).
   - Lacunas e divergências → `open-questions.md` (Q-NNN, priorizadas, após REGRA DE BUSCA ANTES DE PERGUNTAR); lacuna não vira arquivo em `03-as-is/`.
   - Hipóteses → `assumptions.md` (A-NNN, Source `inferred`).
   - Renumerar os `Q-novo-n`/`A-novo-n` dos documentos de `03-as-is/` pela regra de IDs provisórios (skill `architecture`) e conferir `grep -rn 'novo-' docs/architecture` = 0.
4. Verificar que `03-as-is/*` não contém julgamento de valor nem proposta de melhoria. Se contiver, remover o trecho.
5. Atualizar `docs/architecture/README.md` (índice) com os documentos AS-IS que existem.

## Delegação
Subagente: `architecture-discovery`. Prompt-base:

```
Fase: 1-discovery (modo: <completo | redescoberta | área: X>). Somente leitura sobre o código; escreva APENAS os arquivos de saída.
Raiz: <caminho absoluto>. Commit de referência: <sha>.
Memória a respeitar: known-facts.md (IDs existentes: <faixa F-001..F-NNN>) — não duplicar; sinalizar fatos que mudaram.
Escopo: <áreas>.
Procure em: docker-compose*, Dockerfile*, .env.example (SÓ nomes de variáveis, NUNCA valores/segredos), manifests de pacote, migrations, ORM, código, docs/, README, CI/CD, IaC, scripts. Use git log para áreas quentes.
Cada item: evidência arquivo:linha. Sem evidência = lacuna. Proibido: TO-BE, julgamento, recomendação, invenção.
Escreva: .architecture/known-facts.md (seção discovery); docs/architecture/03-as-is/{architecture,applications,integrations,data,infrastructure}.md — SÓ os que tiverem conteúdo (modelo: ~/.claude/skills/architecture/templates/as-is.md); stack/autenticação em architecture.md, módulos em applications.md, CI/CD e observabilidade como seções de infrastructure.md; NÃO criar outros arquivos. Lacunas/hipóteses: relatório + marcadores `[OPEN · Q-novo-N]`/`[ASSUMPTION · A-novo-N]`.
Retorne ≤ 40 linhas: ## Escrito / ## Memória (itens com Status+Source+evidência; IDs `A-novo-N`/`R-novo-N`; mudanças vs fatos existentes) / ## Perguntas sugeridas (≤ 7 por impacto, citando achado) / ## ADRs propostos / ## Riscos observados.
```

## Gate de pergunta
Toda pergunta nascida do discovery cita o achado e o motivo de importar. Perguntas respondíveis pelo repo são descartadas.

## Saída
- `known-facts.md` e `03-as-is/{architecture,applications,integrations,data,infrastructure}.md` atualizados; lacunas em `open-questions.md`.
- Resumo ao usuário: o que mudou desde a última descoberta, lacunas de alto impacto.

## Critério de conclusão
Inventário de stack, módulos, dados, integrações, infra e CI/CD com evidência (arquivo) por item; lacunas listadas; nenhum julgamento de valor; nenhum documento vazio.

## Atualização de state.md
Registrar execução (data, `architecture-discover`, escopo, HEAD). `1-discovery` → DONE. Se foi redescoberta em fase avançada, manter a fase atual e anotar em "Próximos passos" quais documentos TO-BE podem ter sido afetados (sugerir `architecture-update`).
