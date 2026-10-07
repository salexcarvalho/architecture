<!--
Modelo da página "Componentes" (publicar SEM este comentário). Sem H1/[[_TOC_]]/'---'/IDs internos. Links absolutos sem .md.
Mermaid SOMENTE com '::: mermaid' ... ':::'. Rótulos de nós sem acento (compatibilidade do renderizador). Datas dd/mm/aaaa.
Setas contínuas = síncrono; tracejadas (-.->) = externo/telemetria.
-->
**Componentes da arquitetura do <SISTEMA>.**

> **Resumo:** <1 parágrafo: processos da aplicação, front-end, serviços de dados, identidade, armazenamento, borda, integrações externas, telemetria e entrega>. Esta página descreve a responsabilidade de cada componente, como se comunica, quais variáveis o configuram (só nomes, nunca valores) e o que já existe (<dd/mm/aaaa>).
>
> **Contexto:** <situação do repositório: planejado | parcialmente implementado>. Para as escolhas e alternativas, veja [Tecnologias Avaliadas](/Documentação/<Sistema>/Tecnologias-Avaliadas); para o modelo de dados, [Banco de Dados](/Documentação/<Sistema>/Banco-de-Dados).

Páginas relacionadas: [Arquitetura](/Documentação/<Sistema>/Arquitetura), [Tecnologias Avaliadas](/Documentação/<Sistema>/Tecnologias-Avaliadas) e [Banco de Dados](/Documentação/<Sistema>/Banco-de-Dados).

## Diagrama de componentes

::: mermaid
graph LR
    subgraph cliente["Navegador"]
        SPA["Front-end<br/>OIDC + PKCE"]
    end
    subgraph comp["Servicos compartilhados do cliente"]
        IDP["Provedor de identidade"]
        APM["Observabilidade central"]
        CI["Pipelines de entrega"]
    end
    subgraph ext["Sistemas externos"]
        EXT["Fonte de dados externa"]
    end
    subgraph hosp["Hospedagem - rede privada"]
        PG[("Banco de dados")]
        BLOB[("Armazenamento de arquivos")]
        API["API<br/>regras e permissoes"]
        WRK["Worker<br/>tarefas em lote"]
        FILA[("Fila e cache")]
    end
    SPA -->|HTTPS| API
    SPA -->|login| IDP
    API --> PG
    API --> FILA
    API --> BLOB
    FILA --> WRK
    WRK --> PG
    WRK -->|importa| EXT
    API -.->|telemetria| APM
    CI -.->|deploy| API
:::

## Fluxo de uma requisição autenticada

::: mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Front-end
    participant I as Provedor de identidade
    participant A as API
    participant B as Banco
    U->>F: acessa o sistema
    F->>I: login (OIDC + PKCE)
    I-->>F: token de acesso
    F->>A: requisicao com token
    A->>A: valida token e permissao
    A->>B: consulta
    B-->>A: dados
    A-->>F: resposta
:::

## Catálogo de componentes

| Componente | Responsabilidade | Comunicação | Estado no repositório |
|---|---|---|---|
| <API> | <o que faz> | <com quem fala e como> | <Planejado / Na branch principal / Parcial> |
| <Worker> | <o que faz> | <comunicação> | <estado> |
| <Banco> | <o que faz> | <comunicação> | <estado> |

## Pipelines

| Pipeline | Gatilho | O que faz |
|---|---|---|
| <Pull request> | <abertura/atualização do PR> | <testes, análise estática, varredura de segredos e imagens> |
| <Deploy> | <merge na branch principal> | <build da imagem, publicação, deploy por ambiente> |

## Configuração por componente

Apenas nomes. Valores ficam no <gerenciador de segredos/hospedagem> por ambiente.

| Componente | Variáveis | Observação |
|---|---|---|
| <API> | `<NOME_DA_VARIAVEL>`, `<OUTRA>` | <observação> |

## Contratos e limites da borda

| Controle | Valor | Dono | Registro |
|---|---|---|---|
| <Tamanho máximo de requisição> | <valor> | <papel responsável> | Decisão de arquitetura |
| <Tempo limite> | <valor> | <papel> | Decisão de arquitetura |

## Estado de implementação (<dd/mm/aaaa>)

| Já na branch principal | Planejado (sprint) |
|---|---|
| <itens existentes ou "nada ainda"> | <itens com sprint/período> |

## Lacunas

- <o que ainda não está definido ou medido, em linguagem simples>.
