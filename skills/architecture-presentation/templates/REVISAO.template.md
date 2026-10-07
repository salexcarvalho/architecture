# REVISAO — Apresentação de arquitetura ao cliente (<sistema>) v<N> — Fase 1 (análise)

Data: <dd/mm/aaaa>. Escopo: análise do deck atual (<N> slides, `<caminho>`) contra as fontes de verdade (`.architecture/*`, ADRs ACCEPTED, `docs/architecture/**`, inventário, requisitos do usuário de <data>). Documento INTERNO: pode citar IDs; nada daqui vai para o deck.

## 0. Método, legenda e achados principais

**Classificação interna** (não vai para o slide): FACT · DECISION (ADR ACCEPTED ou declaração registrada do usuário) · PROPOSAL · ASSUMPTION · RISK · OPEN QUESTION. Só FACT e DECISION aprovada viram afirmação definitiva; o resto vira "proposta", "hipótese", "risco" ou "pendência do cliente" (ver `checklist-classificacao.md`).

**Régua das matrizes** (igual para todas as alternativas): cada nota tem SCORE (0–10) + JUSTIFICATION + EVIDENCE. Prefixos de evidência: `P` projeto (ADR, fatos, riscos), `I` inventário de manifests, `U` declaração do usuário/cliente, `D` documentação pública do produto (a anexar; nota provisória marcada com †). Sem evidência = NOT EVALUATED: sai da média. O radar plota só critérios avaliados para TODAS as alternativas; os demais são listados como n/a. "Experiência da equipe" NÃO é pontuada: usar "Precedente na organização" com régua única (ex.: ≥10 projetos = 9; 5–9 = 7; 2–4 = 5; 1 = 4; 0 = 3) ou NOT EVALUATED. Restrição do cliente é filtro explícito, não nota baixa.

**Principais achados** (≤ 8 itens, um por linha): <...>

## 1. Slides redundantes ou consolidáveis (mapa slide atual → destino)

| Slide atual | Título atual | Problema (redundância / documento projetado / sem pergunta) | Destino na nova estrutura |
|---|---|---|---|
| <n> | <...> | <...> | <slide novo, fusão ou corte> |

## 2. Afirmações não sustentadas (ou classificadas errado)

| # | Slide | Afirmação atual | Classe correta | Evidência (ou falta dela) | Nova redação |
|---|---|---|---|---|---|
| 1 | <n> | <texto> | PROPOSAL / ASSUMPTION / ... | <fonte ou "nenhuma"> | <texto com selo Proposta/Hipótese ou remoção> |

## 3. Avaliações negativas questionáveis

Toda negativa sem evidência é removida ou vira NOT EVALUATED; limitação real vira linha de risco (Restrição atual / Impacto / Mitigação / Caminho de evolução). Nenhuma alternativa é rebaixada para justificar outra.

| Alternativa | Critério | Nota atual | Problema | Ação (manter com evidência / NOT EVALUATED / remover) |
|---|---|---|---|---|
| <...> | <...> | <n> | <...> | <...> |

## 4. Matriz tecnológica revisada

Resumo por camada (detalhe com SCORE + JUSTIFICATION + EVIDENCE em `radar-data.json`):

| Camada | Escolha | Melhor alternativa | Média | Média sem precedente | Critérios n/a | No deck? (slide) |
|---|---|---|---|---|---|---|
| <...> | <...> | <...> | <x,x> | <x,x> | <...> | <radar / tabela-resumo> |

Para cada camada com radar: tabela `alternativa × critério` com `score — justificativa — evidência`.

## 5. Banco de dados: duas decisões separadas

### 5.1 Decisão (a): motor
Alternativas, critérios, notas, justificativas, evidências, resultado. Restrições do cliente fora das notas.

### 5.2 Decisão (b): hospedagem (gerenciado × container × outro)
Idem; o que o modo escolhido exige (rede privada, papéis, ensaio de recuperação, prazo de suporte do motor).

## 6. Experiência da equipe: o que muda

Critérios que usavam "experiência do time" e como ficam (precedente na organização com régua, ou NOT EVALUATED); fatos declarados pelo usuário a registrar na memória do projeto (com data).

## 7. RBAC e segurança, separados

Seis controles distintos, cada um com dono, decisão de origem e classe (Decisão / Proposta): RBAC · autenticação · autorização · segurança da aplicação · segurança do banco · auditoria. O que está decidido × proposto × em aberto.

## 8. Caracterização da arquitetura (sem rótulo de estilo)

Sem "monólito modular" nem outro rótulo. Descrever: camadas; LB → App/API 1..N → banco; escala horizontal da aplicação × vertical/HA do banco tratada à parte (nunca afirmar escala horizontal do banco sem decisão); o que é HOJE (decisão) × EVOLUÇÃO (capacidade do desenho). Inconsistências entre documentos internos a resolver na documentação, não no deck.

## 9. Escalabilidade × Resiliência × Alta disponibilidade × Recuperação de desastres

| Capacidade | Hoje (decisão aprovada) | Evolução (sem decisão) | Meta / prova exigida | Classe |
|---|---|---|---|---|
| Escalabilidade | <...> | <...> | <...> | <...> |
| Resiliência | <...> | <...> | <...> | <...> |
| Alta disponibilidade | <...> | <...> | <...> | <...> |
| Recuperação de desastres | <...> | <...> | <...> | <...> |

## 10. NOVA ESTRUTURA — até 20 slides

Princípios: uma pergunta por slide; título = afirmação (≤ 56 caracteres, 1 linha); diagrama ou indicador por slide; no máximo 3 mensagens curtas; fontes (F-/ADR-) ficam AQUI, não no corpo do slide. Fluxogramas principais (2–3): slides <a>, <b>, <c>.

| Nº | Título-afirmação | Pergunta respondida | Conteúdo visual (tipo de slide) | Fontes internas |
|---|---|---|---|---|
| 1 | <título> | <o que esta sessão decide?> | Capa (`cover`): 3 blocos Decidido / Em prova / Precisa do cliente | <...> |
| 2 | <...> | <por que o sistema existe?> | 4 indicadores (`kpis`) | <...> |
| 3 | <...> | <como o sistema está organizado?> | Diagrama LB → App/API 1..N → banco (`diagram`) | <...> |
| 4 | <...> | <que propriedades isso dá?> | Cartões com selo Decisão/Capacidade (`cards`) | <...> |
| 5 | <...> | <como o processo principal roda?> | Fluxograma 1 (`flow`) | <...> |
| 6 | <...> | <como os dados entram?> | Fluxograma 2 (`diagram`) | <...> |
| 7 | <...> | <como o usuário entra e recebe permissões?> | Fluxograma 3 (`flow`) | <...> |
| 8 | <...> | <que tecnologias e com que evidência?> | Tabela-resumo (`stack`) | <...> |
| 9–12 | <...> | <decisões discutíveis ou críticas> | Radares (`radar`) | <...> |
| 13 | <...> | <o que protege o quê?> | Seis controles (`cards`) | <...> |
| 14 | <...> | <identidade e acesso resolvidos?> | Dois radares (`radar`) | <...> |
| 15 | <...> | <o que existe hoje e o que vem depois?> | Matriz hoje × evolução (`matrix-hoje-evolucao`) | <...> |
| 16 | <...> | <como chega à produção?> | Implantação + cadeia de promoção (`diagram`) | <...> |
| 17 | <...> | <quando recebemos cada entrega?> | Linha do tempo (`timeline`) | <...> |
| 18 | <...> | <o que pode atrasar ou limitar?> | Riscos em 4 colunas (`risks`) | <...> |
| 19 | <...> | <o que precisamos do cliente e até quando?> | Pedidos com dono e prazo (`asks`) | <...> |
| 20 | <...> | <próximas semanas?> | Encerramento (`closing`) | <...> |

### O que cortar para caber em 20
<lista do que foi consolidado/removido e para onde foi>

## Anexo A. Riscos reais mantidos (formato do slide de riscos)

| Restrição atual | Impacto | Mitigação | Caminho de evolução |
|---|---|---|---|
| <...> | <...> | <...> | <...> |

## Anexo B. Pontos para o orquestrador decidir ou registrar antes da Fase 2

1. <decisão pendente do usuário (nada inventado)>
2. <fato declarado a registrar na memória (`/architecture-context`)>
