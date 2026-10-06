---
name: architecture-interview
description: Entrevista question-first com o usuário, em rodadas de 3 a 7 perguntas, procurando no repositório antes de perguntar e registrando as respostas na memória. Use quando o usuário disser "me entreviste", "faça perguntas sobre o sistema", "levantar requisitos de arquitetura", "rodada de perguntas", "preciso responder dúvidas da arquitetura", "interview me", "architecture interview", "requirements questions".
---

# architecture-interview — entrevista de arquitetura (sessão principal)

Subagentes não conversam com o usuário: a entrevista acontece AQUI. Especialistas apenas sugerem perguntas nos relatórios; esta skill as filtra, prioriza e consolida.

## Quando usar
- Fase `2-interview` (rodada 1 em diante) ou sempre que o Gate de pergunta de outra skill detectar lacuna de ALTO impacto.
- Consolidação das perguntas sugeridas por especialistas após `architecture-generate` (uma única rodada).

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Ler `known-facts.md`, `assumptions.md`, `open-questions.md`, `interview-log.md`, `risks.md`, `context.md`.
3. Ler perguntas sugeridas pendentes (relatórios recentes de subagentes: `.architecture/reviews/`, retornos de discovery).

## Passos

### 1. Preparar (antes de perguntar uma única coisa)
1. Listar as LACUNAS: áreas do checklist sem fato nem hipótese confirmada.
   Checklist (só o que faltar): objetivo, stakeholders, usuários, volume, disponibilidade, performance, escalabilidade, segurança, privacidade/regulatório, integrações, dados, infraestrutura, restrições, orçamento, operação, deploy, observabilidade, recuperação de desastres, roadmap.
2. **BUSCA OBRIGATÓRIA ANTES DE PERGUNTAR.** Para cada lacuna, procurar a resposta no repositório (Grep/Glob direto, ou `architecture-discover` com escopo pequeno se a busca for grande): `docker-compose*`, `.env.example` (só nomes), manifests de pacote, migrations, código, `docs/`, README, CI/CD, IaC.
   - Achou → registrar como KNOWN (Source `repository`, `arquivo:linha`) via `architecture-context`; NÃO perguntar a existência. Se houver pergunta de maior valor relacionada, fazê-la citando o achado.
   - Não achou → a pergunta entra na fila.
3. Descartar perguntas já ANSWERED ou DEFERRED recentes, duplicadas ou cuja resposta é irrelevante para alguma decisão pendente.

### 2. Priorizar por impacto arquitetural
Ordem: (1) restrições duras: regulatório/privacidade, infraestrutura obrigatória, integrações corporativas obrigatórias; (2) disponibilidade/continuidade, volume e crescimento; (3) prazo, orçamento, equipe/competências; (4) segurança e dados; (5) operação, deploy, observabilidade; (6) roadmap/preferências. Perguntas que destravam várias decisões vêm antes.

### 3. Montar o bloco (3 a 7 perguntas — nunca dezenas)
Perguntas relacionadas ao mesmo tema, específicas e respondíveis. Cada pergunta traz:
- **Pergunta** (uma só coisa por vez);
- **Por que importa** (1 linha: decisão/documento que destrava);
- **Achado no repositório** (se houver): "Identifiquei X em `<arquivo>`. ...?";
- **Opções/exemplos concretos** quando ajudar;
- **Se não souber:** "qual hipótese adotamos?" (propor uma hipótese padrão marcada como ASSUMPTION).

Técnicas: quebrar em perguntas menores; restrições antes de preferências; separar fato de hipótese; pedir exemplo concreto; casos extremos ("qual o pior dia de carga?"); "o que pode dar errado?"; adaptar a próxima rodada às respostas. Se o usuário responde de forma vaga, reformular com exemplo, não insistir mais de uma vez.

### 4. Perguntar
- Respostas de **múltipla escolha** (opções finitas e claras) → usar `AskUserQuestion` (até 4 perguntas por chamada, opções curtas, "Outro/Não sei" sempre disponível).
- Respostas **abertas** ou que exijam contexto → texto livre, numerado, formato de bloco acima.
- Combinar: perguntas fechadas via `AskUserQuestion` e abertas em texto, na mesma rodada, sem ultrapassar 7 no total.
- Registrar o número da rodada (`state.md` → "Rodada de entrevista atual").

### 5. Registrar (logo após as respostas)
1. `interview-log.md`: nova seção "Rodada N — AAAA-MM-DD" (modelo: `~/.claude/skills/architecture/templates/interview-log.md`): objetivo, achados do repo usados, tabela pergunta/resposta resumida literal/status/memória gerada. Append-only.
2. `open-questions.md`: cada Q-NNN → `ANSWERED` (resposta + data) ou `DEFERRED` (motivo + hipótese adotada).
3. Gerar itens com **Source = `user` e data**: respostas viram `known-facts.md` (KNOWN); respostas "não sei" viram `assumptions.md` (A-NNN, Source `inferred`/`architectural analysis`, OPEN); ameaças e incertezas relevantes → `risks.md`; ideias de solução → `decisions.md` (Propostas P-NNN), nunca DECISION.
4. Nunca registrar segredos colados na resposta: `[valor omitido]`.
5. Contradição com fato existente: marcar o antigo `SUPERSEDED por F-NNN` e avisar o usuário.

### 6. Decidir sobre nova rodada
- Nova rodada SOMENTE se restar lacuna de ALTO impacto que bloqueie documento relevante ou decisão. Máximo recomendado: 3 rodadas antes da proposta; lacunas de média/baixa prioridade viram hipóteses ou DEFERRED.
- Nova rodada: tema e contagem definidos na rodada anterior; adaptar às respostas (aprofundar o que o usuário revelou).
- Sem lacuna de alto impacto: encerrar a entrevista e sugerir `architecture-context` (requisitos) → `architecture-generate`.

## Delegação
Nenhum subagente é chamado por esta skill. Para entender melhor o repositório durante a preparação, pode ser usada `architecture-discover` (escopo restrito), cujo prompt-base está nessa skill. Perguntas sugeridas por subagentes chegam em seus retornos e devem ser filtradas pelos passos 1–2.

## Gate de pergunta
O Gate desta skill é a própria preparação: nenhuma pergunta sai sem (a) busca prévia feita, (b) justificativa de impacto, (c) prioridade definida. Se o usuário disser "decida você", NÃO decidir: registrar `[PROPOSAL]` com a recomendação e a justificativa e pedir aprovação explícita depois.

## Saída
- Rodada concluída e registrada (`interview-log.md`, `open-questions.md`, `known-facts.md`, `assumptions.md`, `risks.md`, `decisions.md` conforme o caso).
- Mensagem ao usuário: o que foi registrado (N fatos, N hipóteses, N DEFERRED), lacunas de alto impacto restantes e se haverá nova rodada.

## Critério de conclusão
- Todas as perguntas da rodada com resposta ou DEFERRED (com hipótese); memória atualizada com Source=user e data.
- Nenhuma pergunta feita cuja resposta estava no repositório.
- Entrevista encerrada quando não há lacuna de alto impacto que bloqueie requisitos.

## Atualização de state.md
Rodada atual = N; "Execuções": data, `architecture-interview` (rodada N), resultado, HEAD, arquivos de memória alterados. "Bloqueios": Q-IDs de alta prioridade ainda abertos. Fase: `2-interview` IN PROGRESS → DONE quando não houver lacuna de alto impacto; próxima fase `3-requirements`.
