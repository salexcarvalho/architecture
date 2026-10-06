# Arquitetura Atual (AS-IS) — <Nome do Sistema>

<!--
Local: `docs/architecture/03-as-is/` — exatamente 5 arquivos: architecture.md, applications.md, integrations.md, data.md, infrastructure.md. Este modelo reúne todas as seções; na instância cada uma vai para UM destes arquivos (não criar overview/stack/modules/cicd/observability/auth-security/gaps):
  seções 1, 2, 4 e 8 (visão geral, stack, fluxos, autenticação/segurança observável) -> architecture.md
  seção 3 (módulos, camadas, endpoints, jobs, testes) -> applications.md
  seção 5 -> data.md | seção 6 -> integrations.md
  seções 7, 9 e 10 (infraestrutura e ambientes, CI/CD, observabilidade e operação) -> infrastructure.md
  seção 11 (pontos em aberto) -> uma tabela em cada arquivo, só com os itens daquele arquivo
Lacunas NÃO têm arquivo próprio: cada lacuna é um marcador `[OPEN · Q-NNN]` no ponto do documento e uma pergunta em `.architecture/open-questions.md` (hipóteses em `.architecture/assumptions.md`).
Escrito por `architecture-discovery`. DESCREVE O QUE EXISTE. Proibido: propor melhoria, julgar qualidade, escrever TO-BE.
Cada item tem evidência (arquivo:linha). Item sem evidência não entra: vira lacuna.
Começar pelo cabeçalho padrão (templates/doc-section.md).
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |
| **Commit analisado** | `<sha>` |
| **Fontes** | repositório (arquivos citados), `git log` |

## 1. Visão geral
<!-- 3-5 linhas descritivas, sem adjetivos de valor. -->

## 2. Stack tecnológica

| Camada | Tecnologia | Versão | Evidência |
|---|---|---|---|
| Linguagem/runtime | <x> | <versão> | `package.json:5` [KNOWN · F-001] |
| Framework web | <x> | <versão> | `<arquivo:linha>` [KNOWN · F-00N] |
| Banco de dados | <x> | <versão> | `docker-compose.yml:8` [KNOWN · F-00N] |

## 3. Módulos e responsabilidades

| Módulo | Caminho | Responsabilidade observada | Dependências | Evidência |
|---|---|---|---|---|
| <módulo A> | `src/<a>/` | <o que faz> | <módulo B> | `src/<a>/index.*` |

## 4. Fluxos principais observados
<!-- Descrever o fluxo como o código o executa. Link para diagrama quando existir. -->
1. Requisição entra por `<arquivo>` → passa por `<middleware>` → chega em `<handler>` → persiste em `<repositório>`. [KNOWN · F-00N]

## 5. Dados
- Armazenamentos: <lista com evidência>
- Migrations: <pasta, ferramenta, quantidade>
- Detalhes: `data.md`

## 6. Integrações

| Integração | Direção | Protocolo | Evidência | Autenticação (apenas tipo) |
|---|---|---|---|---|
| <sistema externo> | saída | HTTPS/REST | `<arquivo:linha>` | token (nome da variável: `<VAR_NAME>`) |

## 7. Infraestrutura e ambientes
- Contêineres/serviços: <lista com evidência>
- IaC: <ferramenta ou "não encontrado">
- Ambientes identificados: <nomes> (valores de segredos NÃO lidos)

## 8. Autenticação e segurança observável
- Autenticação/autorização encontradas (mecanismo, provedor, onde é aplicada): <lista com evidência ou "não encontrado">. Apenas descrever; avaliação é do security-privacy-architect.
- Dados pessoais visíveis no modelo: somente NOMES de campos/colunas.

## 9. CI/CD
- Pipeline: <ferramenta>, etapas: <lint, test, build, deploy> — `<arquivo>`

## 10. Observabilidade e operação
- Logs / métricas / tracing encontrados: <lista ou "não encontrado">

## 11. Pontos em aberto neste documento (não encontrado no repositório)
<!-- Cada arquivo carrega só os seus. A fonte da pergunta é `.architecture/open-questions.md`; aqui ficam apenas o item e o ID. -->

| Item procurado | Onde se procurou | Pergunta gerada |
|---|---|---|
| Política de backup | scripts, IaC, docs | [OPEN · Q-00N] |
