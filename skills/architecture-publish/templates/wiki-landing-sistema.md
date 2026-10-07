<!--
Modelo da landing do sistema: Documentação/<Sistema>.md (publicar SEM este comentário).
Pasta Documentação/<Sistema>/.order = Arquitetura, Tecnologias-Avaliadas, Componentes, Banco-de-Dados, Planejamento (sem extensão, sem newline final)
  - sem legado: Arquitetura/01..11 (Visao-Sistemica, Dominios-e-Modulos, Componentes-Tecnicos, Modelo-de-Dados, APIs-e-Integracoes, Seguranca,
    Infraestrutura-e-Deploy, Fluxos-e-Diagramas, Radar-Arquitetural, Pontos-a-Definir, Glossario) e as 3 páginas padrão ao lado de Arquitetura;
  - com legado: ver a estrutura da skill (Arquitetura/{Sistema-Atual-(legado), Nova-Arquitetura-da-API/{3 páginas}, Migração, Planejamento}).
Atualizar também Documentação/.order (inserir o sistema). Sem IDs internos; pendências do cliente em linguagem simples. Termina com [[_TOSP_]].
-->
O <SISTEMA> é um **<tipo de sistema, ainda em construção | em produção>**, para <objetivo em 1 frase>, operado por <áreas/usuários> no contexto de <programa/cliente>. <Substitui | Integra-se a> <processo/sistema atual>.

<Conceito central do domínio em 1 a 2 frases (ex.: "O trabalho é organizado por competência...").>

> **Situação:** <arquitetura aprovada (dd/mm/aaaa) | proposta em validação>, <fase atual>. <Existe ou não código/ambiente>; o que está descrito é o projeto, não um sistema em produção.

## Seções

| Seção | Conteúdo |
|---|---|
| [Arquitetura](/Documentação/<Sistema>/Arquitetura) | <visão sistêmica, domínios e módulos, componentes técnicos, modelo de dados, APIs e integrações, segurança, infraestrutura e deploy, fluxos, radar arquitetural, pontos a definir e glossário> |
| [Tecnologias Avaliadas](/Documentação/<Sistema>/Tecnologias-Avaliadas) | Alternativas avaliadas, critérios, escolha e motivo de cada camada técnica, com comparativo visual |
| [Componentes](/Documentação/<Sistema>/Componentes) | Diagrama e catálogo de componentes, fluxos, pipelines, configuração e contratos da borda |
| [Banco de Dados](/Documentação/<Sistema>/Banco-de-Dados) | <Motor>, tabelas por domínio, diagramas ER, papéis, migrations, retenção e backup |
| [Planejamento](/Documentação/<Sistema>/Planejamento) | <Roadmap, permissionamento e evoluções planejadas> |

## Contexto

| Tema | Resumo |
|---|---|
| **Objetivo** | <objetivo> |
| **Problema atual** | <problema em linguagem de negócio> |
| **Usuários** | <perfil e volume, picos> |
| **Prazo operacional** | <prazo recorrente, se houver> |
| **Fora do escopo de negócio** | <o que não entra> |
| **Roadmap** | <marcos principais com datas dd/mm/aaaa> |

## Em uma linha

| | |
|---|---|
| **Frontend** | <tecnologia, responsividade> |
| **Backend** | <linguagem, framework, estilo (monólito modular), API REST /v1> |
| **Assíncrono** | <fila e worker> |
| **Banco** | <motor, hospedagem, recuperação> |
| **Identidade** | <provedor, MFA, onde ficam perfis> |
| **Infraestrutura** | <hospedagem, ambientes, entrega> |
| **Observabilidade** | <logs, métricas, APM> |
| **Integrações** | <sistemas externos e forma de troca> |
| **Repositórios** | <planejados ou existentes> |

## Contexto institucional

- <organização responsável e quem homologa>.
- <perfis iniciais e onde está a matriz de permissões>.
- <padrão técnico de referência do cliente e adaptações>.

## Pontos a definir com <o cliente>

- <pendência em linguagem simples, com quem decide e prazo proposto quando houver>.

[[_TOSP_]]
