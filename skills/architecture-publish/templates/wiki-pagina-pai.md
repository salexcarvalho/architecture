<!--
Modelo da página-pai das 3 páginas padrão QUANDO HÁ LEGADO: Documentação/<Sistema>/Arquitetura/Nova-Arquitetura-da-API.md
(as filhas ficam em Nova-Arquitetura-da-API/{Tecnologias-Avaliadas,Componentes,Banco-de-Dados}.md; .order da pasta = essas 3, sem extensão, sem newline final).
Sem legado: NÃO usar esta página; a landing do sistema (wiki-landing-sistema.md) é o pai. ~20 linhas. Sem H1/[[_TOC_]]/'---'/IDs. Termina com [[_TOSP_]].
Nunca criar a página "Sistema-Atual-(legado)" sem acesso à fonte do legado.
-->
**Nova Arquitetura da API do <SISTEMA> — arquitetura proposta para <a API própria que substitui <o legado>>.**

> **Situação:** proposta em validação durante <a migração (sprints X a Y)>. Descreve o destino, não o sistema em produção hoje; o que está no ar é o [Sistema Atual (legado)](/Documentação/<Sistema>/Arquitetura/Sistema-Atual-(legado)).

<Parágrafo 1: o destino em uma frase — front consome uma API versionada /v1, com worker de tarefas, banco, cache, provedor de identidade e armazenamento de arquivos.> <Parágrafo 2: o que estas páginas justificam e onde fica a execução da migração (módulos, rotas, sprints, ambientes e backup) em [Migração](/Documentação/<Sistema>/Arquitetura/Migração).>

## Páginas desta seção

| Página | Para quê |
|---|---|
| [Tecnologias Avaliadas](/Documentação/<Sistema>/Arquitetura/Nova-Arquitetura-da-API/Tecnologias-Avaliadas) | Alternativas avaliadas, critérios, decisão e motivo de cada escolha técnica |
| [Componentes](/Documentação/<Sistema>/Arquitetura/Nova-Arquitetura-da-API/Componentes) | Responsabilidade, comunicação e configuração de <API, worker, banco, cache, identidade, armazenamento, borda e pipelines> |
| [Banco de Dados](/Documentação/<Sistema>/Arquitetura/Nova-Arquitetura-da-API/Banco-de-Dados) | <Motor>, tabelas, diagrama ER, papéis, migrations e dados que migram |

## Ver também

[Sistema Atual (legado)](/Documentação/<Sistema>/Arquitetura/Sistema-Atual-(legado)) · [Migração](/Documentação/<Sistema>/Arquitetura/Migração) · [Planejamento](/Documentação/<Sistema>/Arquitetura/Planejamento)

[[_TOSP_]]
