---
name: architecture-start
description: Inicializa a memória .architecture/ de um projeto, roda o discovery do repositório e monta o primeiro bloco de perguntas. Use quando o usuário disser "iniciar arquitetura", "começar a documentar a arquitetura", "inicializar .architecture", "primeira rodada de arquitetura", "start architecture", "init architecture memory", ou quando .architecture/state.md não existir.
---

# architecture-start — inicialização + discovery + 1º bloco de perguntas

## Quando usar
- Projeto sem `.architecture/state.md` (fase `0-init`).
- Reinício explícito pedido pelo usuário (nesse caso, confirmar antes de sobrescrever qualquer arquivo existente; nunca apagar memória sem confirmação).

## Pré-condições
1. Estar na raiz do repositório do projeto (confirmar com `git rev-parse --show-toplevel`; se não for repositório git, avisar e seguir apenas com o diretório atual).
2. Ler `.architecture/state.md` se existir. Se existir e a fase for > `0-init`, NÃO reinicializar: orientar a skill `architecture` e parar.
3. Verificar `.gitignore`: `.architecture/` deve ser VERSIONADA (não ignorar). Se estiver ignorada, avisar o usuário.

## Passos
1. **Criar a memória** (só o que não existir; nunca sobrescrever):
   - `.architecture/state.md`, `context.md`, `known-facts.md`, `assumptions.md`, `open-questions.md`, `decisions.md`, `risks.md`, `interview-log.md`, `reviews/` (pasta com `.gitkeep`).
   - Origem: `~/.claude/skills/architecture/templates/<mesmo-nome>.md`. Remover comentários HTML de instrução do template ao instanciar; manter cabeçalhos e colunas; esvaziar as linhas de exemplo (substituir por linhas vazias ou "—").
   - Nome do sistema: tentar descobrir (README, manifest); se não achar, usar o nome da pasta e registrar `[OPEN]`.
   - Dados do exemplo dos templates NUNCA permanecem na memória do projeto.
2. **Rodar discovery** delegando a `architecture-discovery` (ver Delegação). Rodar uma única vez; o resultado alimenta `known-facts.md` e `docs/architecture/03-as-is/`.
3. **Consolidar o retorno**: os fatos já foram gravados pelo subagente na seção discovery de `known-facts.md` (F-NNN finais, Status KNOWN, Source `repository`/`documentation`, evidência `arquivo:linha`): conferir IDs únicos e sem duplicidade. Lacunas e divergências → `open-questions.md` (Q-NNN) já priorizadas; hipóteses → `assumptions.md` (A-NNN, Source `inferred`). Renumerar os `Q-novo-n`/`A-novo-n` dos documentos de `03-as-is/` conforme a regra de IDs provisórios da skill `architecture`.
4. **Preencher `context.md`** (1 página) apenas com o que tem fato ou marcador `[OPEN]`.
5. **Montar o 1º bloco de perguntas** (3–7), aplicando a REGRA DE BUSCA ANTES DE PERGUNTAR: descartar o que o discovery já respondeu; priorizar restrições duras (regulatório/privacidade, infraestrutura obrigatória, integrações corporativas, disponibilidade, volume, prazo/orçamento, equipe). Não fazer a entrevista aqui: apresentar o bloco e passar para `architecture-interview` (rodada 1) conforme confirmação do usuário.
6. Se `docs/architecture/` não existir, NÃO criá-la vazia. As pastas nascem quando houver documento com conteúdo (discovery cria `03-as-is/`; `01-context/` e `02-requirements/` nascem em `architecture-context`).

## Delegação
Subagente: `architecture-discovery`. Prompt-base (preencher `<...>`):

```
Fase: 1-discovery. Você é somente leitura sobre o código: escreva APENAS os arquivos de saída abaixo.
Raiz do repositório: <caminho absoluto>
Memória: <caminho>/.architecture/ (known-facts.md já inicializado e vazio; você só escreve nele. Lacunas, hipóteses e perguntas vão no relatório e como marcadores `[OPEN · Q-novo-N]`/`[ASSUMPTION · A-novo-N]`; a skill os registra)
Tarefa: inventariar stack, módulos, dados, integrações, infraestrutura, CI/CD, observabilidade, testes, com EVIDÊNCIA (arquivo:linha) para cada item. Procurar em: docker-compose*, Dockerfile*, .env.example (SÓ nomes de variáveis; NUNCA ler/registrar valores de .env ou segredos), manifests de pacote, migrations, ORM, código, docs/, README, CI (.github, .gitlab-ci, pipelines), IaC. Usar também git log (últimos 50 commits) para atividade e áreas quentes.
Proibido: propor TO-BE, julgar qualidade, recomendar tecnologia, inventar o que não achou (vira "lacuna").
Escreva:
 - .architecture/known-facts.md → seção "Seção discovery" (modelo: ~/.claude/skills/architecture/templates/known-facts.md)
 - docs/architecture/03-as-is/{architecture,applications,integrations,data,infrastructure}.md (modelo: ~/.claude/skills/architecture/templates/as-is.md) — SÓ os com conteúdo; stack, módulos, CI/CD, observabilidade e autenticação entram como seções desses 5 arquivos; NÃO criar nenhum outro arquivo.
Retorne ≤ 40 linhas: ## Escrito / ## Memória (fatos F-NNN gravados, com Source+evidência; hipóteses `A-novo-N` marcadas ASSUMPTION/inferred) / ## Perguntas sugeridas (≤ 7, por impacto, cada uma citando o achado e por que importa) / ## ADRs propostos (normalmente nenhum) / ## Riscos observados (com evidência).
```

## Gate de pergunta
Antes de formular perguntas: reler `known-facts.md` e `open-questions.md`. Pergunta cuja resposta está no repositório é descartada; reformular citando o achado ("Identifiquei X em `<arquivo>`. ...?").

## Saída
- `.architecture/*` inicializado (sem exemplos residuais), `known-facts.md` com seção discovery, `docs/architecture/03-as-is/{architecture,applications,integrations,data,infrastructure}.md` (só os com conteúdo).
- Mensagem ao usuário: resumo do AS-IS (≤ 15 linhas), lacunas principais, 1º bloco de perguntas (3–7) e pedido de confirmação para iniciar `architecture-interview`.

## Critério de conclusão
- Memória criada; `state.md` presente com fase atualizada.
- Discovery com inventário (stack, módulos, dados, integrações, infra, CI/CD) com evidência por item, lacunas listadas, nenhum julgamento de valor.
- 1º bloco de perguntas pronto, sem pergunta respondida pelo repositório.
- Nenhum documento vazio criado.

## Atualização de state.md
Fase → `1-discovery` DONE e `2-interview` OPEN (ou `2-interview` IN PROGRESS se a rodada 1 iniciar). Registrar em "Execuções": data, `architecture-start`, DONE, HEAD (`git rev-parse --short HEAD`), arquivos criados. "Próximos passos": rodada 1 de `architecture-interview`.
