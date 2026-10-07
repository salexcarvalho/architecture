<!--
Modelo da página "Tecnologias Avaliadas" (publicar SEM este comentário).
Marcadores: <...> = preencher; @@CMP:<slug>@@ (slug = o "slug" da camada no JSON de notas; os do exemplo são framework-da-api e banco-de-dados) = o scripts/radar_charts.py --fill substitui pelo bloco "### Comparativo visual".
Regras: sem H1, sem [[_TOC_]], sem '---', sem IDs internos (F/A/Q/R/P/RF/RNF/RES/ADR/DEC), sem selos PROPOSAL/DECISION, sem emoji (exceto ✅ nas notas).
Links absolutos, sem .md. Datas dd/mm/aaaa. Fonte dos dados: docs/architecture/07-technology + ADRs ACCEPTED (aqui só em linguagem simples).
Caminho base: sem legado -> /Documentação/<Sistema>/...; com legado -> /Documentação/<Sistema>/Arquitetura/Nova-Arquitetura-da-API/...
-->
**Tecnologias avaliadas e escolhidas para o <SISTEMA>.**

> **Resumo:** para cada camada da solução (<lista curta das camadas>) esta página mostra as alternativas avaliadas, os critérios, a escolha e o motivo. Onde não há comparativo formal, a página diz isso. Fonte: avaliação de tecnologias do projeto (<dd/mm/aaaa>).
>
> **Como ler:** "Comparativo" indica que existe uma tabela de alternativas com vantagens e desvantagens por critério. As tecnologias definidas no projeto (<exemplos>) são **restrições**: onde a avaliação aponta risco, a saída é mitigação, não troca.

Páginas relacionadas: [Arquitetura](/Documentação/<Sistema>/Arquitetura), [Componentes](/Documentação/<Sistema>/Componentes) e [Banco de Dados](/Documentação/<Sistema>/Banco-de-Dados).

## Contexto que condiciona todas as escolhas

| Fato | Efeito nas escolhas |
|---|---|
| <usuários, picos, cargas> | <o que isso pesa: operação, reaproveitamento, previsibilidade> |
| <disponibilidade, RPO, RTO, retenção> | <efeito no banco, na hospedagem> |
| <restrição regulatória, de identidade, de infraestrutura do cliente> | <efeito> |
| <experiência do time (inventário de projetos), quando houver> | <precedentes e novidades para o time> |

## Resumo das escolhas

| # | Camada | Escolha | Registro | Comparativo | Alternativas principais |
|---|---|---|---|---|---|
| 1 | <Linguagem e framework da API> | <escolha> | Definida no projeto | Sim | <alt 1>; <alt 2>; <alt 3> |
| 2 | <Camada> | <escolha> | Decisão de arquitetura | Sim | <alternativas> |
| 3 | <Camada sem comparativo formal> | <escolha> | Decisão de arquitetura | Parcial | <alternativas> |

Resultado: **<N> escolhas com comparativo registrado** (<faixa>) e **<M> com comparativo parcial** (<faixa>, <motivo>). Escolhas complementares estão na seção final.

## Como ler os comparativos visuais

Cada camada traz ao final um gráfico de radar e uma tabela de notas, com legenda e linha da alternativa escolhida em destaque (✅).

| Faixa | Leitura |
|---|---|
| 9 a 10 | Vantagem explícita na avaliação, ou atende por completo |
| 7 a 8 | Atende bem |
| 5 a 6 | Adequado, com ressalva |
| 3 a 4 | Limitado; desvantagem registrada |
| 0 a 2 | Não atende, fora do modelo do cliente ou sem experiência no time |

As notas **não são medição**: o projeto não traz benchmark nem dado de carga. Elas traduzem para números o comparativo por critério da avaliação de tecnologias (aderência, maturidade, experiência do time, alinhamento com o cliente, operação e risco). Quando a avaliação não trata a alternativa naquele critério, a nota é da equipe de arquitetura e leva a marca † ("avaliação da equipe de arquitetura, sem comparativo formal registrado"). Em tecnologias definidas no projeto, a escolha é restrição: a média das notas pode ficar abaixo da de uma alternativa descartada, e o texto de cada camada explica o motivo.

## 1. <Camada>

**Pergunta:** <qual problema esta camada resolve>.

| Alternativa | Vantagens | Desvantagens | Resultado |
|---|---|---|---|
| **<Escolhida>** | <vantagens factuais> | <desvantagens factuais> | **Escolhida** |
| <Alternativa 2> | <vantagens> | <desvantagens> | Descartada |
| <Alternativa 3> | <vantagens> | <desvantagens> | Descartada |

**Critérios:** <critérios usados>.
**Motivo:** <por que a escolhida vence, em 1 a 2 frases>.
**Risco e mitigação:** <risco da escolha e como será tratado>.
**Referência:** <decisão de arquitetura da aplicação | precedente em outro sistema do cliente>.

@@CMP:framework-da-api@@

## 2. <Camada sem comparativo formal>

| Alternativa | Avaliação | Resultado |
|---|---|---|
| <Escolhida> | <avaliação resumida> | **Escolhida** |
| <Alternativa 2> | <avaliação resumida> | Descartada |

**Critérios:** <critérios>.
**Decisão:** <o que foi decidido ou o que será decidido e quando (ex.: spike antes do incremento X)>.
**Lacuna:** <o que falta validar e com quem>.

@@CMP:banco-de-dados@@

## Escolhas complementares

| Tema | Escolha | Alternativas | Registro |
|---|---|---|---|
| <Gerenciador de dependências> | <escolha> | Sem comparativo registrado | Decisão de arquitetura |
| <Tema pendente> | <escolha provisória> | <alternativas> | A definir com <cliente> |
| <Tema adiado> | Adiado: <regra provisória> | <alternativas> | Adiado até medir |

## Como a comparação foi conduzida e o que ficou aberto

- A comparação vem da avaliação de tecnologias de <dd/mm/aaaa>: para cada camada, a tecnologia definida no projeto, as alternativas de mercado e as habilidades do time (inventário de projetos usado como indicador de experiência; não é pesquisa com pessoas). Custos monetários estão fora do escopo; "custo" é qualitativo (operação, licença, esforço).
- Afirmações que vêm de conhecimento técnico geral (<lista>) serão verificadas antes da implementação.
- Pontos que continuam a definir com <o cliente>: <lista curta, em linguagem simples>.
- Esta página não registra benchmark de desempenho: o projeto ainda não tem dado de carga.
