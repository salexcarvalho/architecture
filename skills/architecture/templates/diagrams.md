# Diagramas — <Nome do Sistema>

<!--
Este modelo reúne todos os tipos só para referência. Na instância, CADA seção vira um arquivo próprio em `docs/architecture/05-diagrams/` (nunca um diagrams.md único): seção 1 → `context.md`; 2 → `container.md`; 3 → `component.md`; 4 → `deployment.md`; 5 e 6 → `flows/<fluxo>.md` (um arquivo por fluxo); a seção 7 (mapa de derivação) vira a última seção de cada arquivo, só com a sua linha.
Escritos por `application-architect` (context/container/component/flows) e `platform-architect` (deployment).
REGRAS:
- Diagrama é DERIVADO de um documento: cada bloco tem a nota "Derivado de: <doc>" e a data. Nunca desenhar o que o texto não afirma.
- Elementos propostos (TO-BE) são distinguíveis dos existentes (rótulo "(proposta)" ou classe/estilo).
- Só criar diagrama quando o documento fonte tem conteúdo. Nunca criar diagrama vazio.
- Mermaid válido: nomes de nós sem espaços/acentos nos IDs; rótulos entre aspas quando houver caracteres especiais.
- Atualizar o diagrama sempre que o documento fonte mudar (architecture-update).
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |

## 1. Contexto (C4 nível 1)

> Derivado de: `../04-to-be/architecture.md` §2 — AAAA-MM-DD

```mermaid
C4Context
    title Contexto do Sistema - <Nome>
    Person(usuario, "Usuário", "Opera o sistema")
    System(sistema, "<Nome do Sistema>", "Entrega <capacidade principal>")
    System_Ext(ext, "<Sistema Externo>", "Fornece <dado/serviço>")
    Rel(usuario, sistema, "Usa", "HTTPS")
    Rel(sistema, ext, "Consome", "REST/HTTPS")
```

## 2. Contêineres (C4 nível 2)

> Derivado de: `../04-to-be/architecture.md` §3 — AAAA-MM-DD

```mermaid
C4Container
    title Contêineres - <Nome>
    Person(usuario, "Usuário", "")
    System_Boundary(sistema, "<Nome do Sistema>") {
        Container(web, "Aplicação Web", "<tecnologia>", "Interface do usuário")
        Container(api, "API", "<tecnologia>", "Regras de negócio e contratos")
        ContainerDb(db, "Banco de Dados", "<SGBD>", "Armazena dados transacionais")
        Container(worker, "Worker (proposta)", "<tecnologia>", "Processamento assíncrono")
    }
    System_Ext(ext, "<Sistema Externo>", "")
    Rel(usuario, web, "Acessa", "HTTPS")
    Rel(web, api, "Chama", "JSON/HTTPS")
    Rel(api, db, "Lê e grava", "SQL")
    Rel(api, worker, "Enfileira jobs", "mensageria")
    Rel(api, ext, "Integra", "REST/HTTPS")
```

## 3. Componentes (C4 nível 3) — <contêiner detalhado>

> Derivado de: `../04-to-be/applications.md` — AAAA-MM-DD

```mermaid
C4Component
    title Componentes da API
    Container_Boundary(api, "API") {
        Component(ctrl, "Controladores", "<tecnologia>", "Entrada HTTP e validação")
        Component(svc, "Serviços de domínio", "<tecnologia>", "Regras de negócio")
        Component(repo, "Repositórios", "<tecnologia>", "Acesso a dados")
    }
    ContainerDb(db, "Banco de Dados", "<SGBD>", "")
    Rel(ctrl, svc, "Invoca")
    Rel(svc, repo, "Usa")
    Rel(repo, db, "SQL")
```

## 4. Implantação (deployment)

> Derivado de: `../04-to-be/infrastructure.md` e `../09-operations/environments.md` — AAAA-MM-DD

```mermaid
flowchart TB
    subgraph PROD[Ambiente: produção]
        LB[Proxy reverso / TLS]
        subgraph HOST1[Host A]
            APIC[Contêiner API]
            WRK[Contêiner Worker - proposta]
        end
        subgraph DATA[Camada de dados]
            DBP[(Banco primário)]
            BKP[(Backup)]
        end
        LB --> APIC
        APIC --> DBP
        WRK --> DBP
        DBP -.->|backup| BKP
    end
    INTERNET((Internet)) --> LB
```

## 5. Sequência — <fluxo principal>

> Derivado de: `../04-to-be/integrations.md` §<n> — AAAA-MM-DD

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant W as Aplicação Web
    participant A as API
    participant D as Banco de Dados
    participant E as Sistema Externo
    U->>W: Submete solicitação
    W->>A: POST /recurso
    A->>D: Grava solicitação
    D-->>A: OK
    A->>E: Notifica (REST)
    alt sucesso
        E-->>A: 200
        A-->>W: 201 Created
    else falha da integração
        E--xA: timeout
        A-->>W: 202 Accepted (reprocessar depois)
    end
    W-->>U: Resultado
```

## 6. Fluxo de dados / integração

> Derivado de: `../04-to-be/data.md` e `../04-to-be/integrations.md` — AAAA-MM-DD

```mermaid
flowchart LR
    FONTE[Sistema de origem] -->|extração diária| STG[(Área de staging)]
    STG -->|validação| TRF[Transformação]
    TRF -->|carga| DWH[(Armazenamento de destino)]
    TRF -.->|rejeitados| ERR[(Fila de erros)]
```

## 7. Mapa de derivação

| Diagrama | Documento fonte | Atualizado em | Em sincronia? |
|---|---|---|---|
| Contexto | `04-to-be/architecture.md` | AAAA-MM-DD | sim |
| Contêineres | `04-to-be/architecture.md` | AAAA-MM-DD | sim |
