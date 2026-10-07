<!--
Modelo da página "Banco de Dados" (publicar SEM este comentário). Sem H1/[[_TOC_]]/'---'/IDs internos. Links absolutos sem .md.
Mermaid SOMENTE com '::: mermaid' ... ':::'. Diagrama ER por domínio (erDiagram). Datas dd/mm/aaaa. Sem dados pessoais reais; só nomes de colunas.
-->
**Banco de dados do <SISTEMA>: <motor e versão, ferramenta de migrations, nº de schemas>.**

> **Resumo:** <1 parágrafo: motor, hospedagem, acesso, ORM, migrations, papéis, modelo temporal/versionamento, auditoria>. Fontes: documentos de arquitetura de dados, infraestrutura e deploy do projeto (<dd/mm/aaaa>).
>
> **Estado:** <planejado | em implementação>. <o que já existe e o que é desenho de partida>. Para a visão por capítulo, veja a seção Arquitetura (<link para o capítulo de modelo de dados, quando existir>).

Páginas relacionadas: [Arquitetura](/Documentação/<Sistema>/Arquitetura), [Tecnologias Avaliadas](/Documentação/<Sistema>/Tecnologias-Avaliadas) e [Componentes](/Documentação/<Sistema>/Componentes).

## Números do baseline

| Item | Valor |
|---|---|
| Motor | <motor, versão, hospedagem> |
| Ambientes | <N e nomes; um banco por ambiente?> |
| Rede | <acesso privado, TLS> |
| Schemas | <N (um por contexto)> |
| Tabelas | <N e origem (migrations, dicionário do legado)> |
| ORM e migrations | <ferramentas> |
| Disponibilidade | <RPO e RTO> |
| Retenção | <regra> |
| Volume | <valor ou "desconhecido; medição pedida a <área>"> |

## Schemas e o que não migra

<Lista dos schemas por contexto e o que fica de fora (ou "não há legado a migrar").>

## Papéis do banco

| Papel | Uso | Privilégios |
|---|---|---|
| `<app>_migrator` | <migrations pelo pipeline> | <DDL no schema> |
| `<app>_app` | <API> | <DML mínimo> |

Regras:

- <papéis separados por função; nenhuma credencial de superusuário na aplicação>.

## Tabelas

Convenção: <nomes, chaves, colunas de auditoria, tipo de timestamp>.

### <Domínio 1>

| Tabela | Finalidade | Principais colunas | FK |
|---|---|---|---|
| `<schema>.<tabela>` | <finalidade> | `<col1>`, `<col2>` | `<tabela>.<col>` |

## Diagrama ER: <Domínio 1>

::: mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : faz
    PEDIDO ||--|{ ITEM_PEDIDO : contem
    CLIENTE {
        int id PK
        string nome
    }
    PEDIDO {
        int id PK
        int cliente_id FK
    }
:::

## Estratégia de migrations

| Tema | Regra |
|---|---|
| <Ferramenta> | <regra> |
| <Compatibilidade> | <expandir e depois contrair; rollback> |

| Migration | O que faz |
|---|---|
| `<0001_baseline>` | <cria schemas, papéis e tabelas fixas> |

## O que sai do banco e vai para a API

<Regras, funções e gatilhos que migram para a camada de aplicação (ou "não se aplica").>

## Dados que migram

<Carga inicial a partir do legado, ordem, validação (ou "nenhum dado a migrar: sistema novo").>

## Retenção, dados pessoais e mascaramento

<Quais dados pessoais existem, base legal quando definida, retenção, mascaramento em ambientes não produtivos.>

## Backup e recuperação

<Backup gerenciado, recuperação para ponto no tempo, cópia por evento, ensaio de restauração, RPO e RTO.>

## Lacunas e pontos em aberto

- <o que falta definir, em linguagem simples>.
