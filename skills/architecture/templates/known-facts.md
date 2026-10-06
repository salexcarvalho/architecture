# Known Facts

<!--
Local: `.architecture/known-facts.md`.
SOMENTE o que tem evidência verificável. Inferência NUNCA entra aqui (vai para assumptions.md).
Colunas:
- ID: F-NNN sequencial, nunca reutilizado.
- Status: sempre KNOWN. Se o fato deixou de valer, mudar para SUPERSEDED e citar o fato que o substitui (não apagar).
- Source: repository | documentation | user | runtime
- Evidência: `caminho/arquivo:linha` (repository/documentation), "resposta do usuário em AAAA-MM-DD, rodada N" (user), comando+data (runtime).
Nunca registrar valores de segredos, tokens ou senhas — apenas nomes de variáveis.
Cada ID pode ser referenciado inline nos documentos: [KNOWN · F-001].
-->

**Última atualização:** AAAA-MM-DD

| ID | Fato | Status | Source | Evidência | Data |
|---|---|---|---|---|---|
| F-001 | A aplicação backend usa <runtime> versão <x> | KNOWN | repository | `package.json:12` | AAAA-MM-DD |
| F-002 | O banco de dados é <SGBD> | KNOWN | repository | `docker-compose.yml:8` | AAAA-MM-DD |
| F-003 | O pipeline de CI executa lint e testes a cada PR | KNOWN | repository | `.github/workflows/ci.yml:1-30` | AAAA-MM-DD |
| F-004 | A disponibilidade esperada é 99,5% em horário comercial | KNOWN | user | resposta do usuário em AAAA-MM-DD, rodada 1 | AAAA-MM-DD |

## Seção discovery — AAAA-MM-DD

<!--
Preenchida pelo subagente `architecture-discovery` (única exceção em que um subagente escreve na memória): uma seção por execução, com a MESMA tabela acima (ID final F-NNN, continuando do maior existente; Status KNOWN; Source repository|documentation|runtime; Evidência arquivo:linha). Inventário factual, sem julgamento de valor.
Agrupar as linhas por área nesta ordem: Stack, Aplicações/módulos, Dados, Integrações, Infraestrutura, CI/CD, Observabilidade, Autenticação/segurança observável.
Lacunas (não encontrado no repositório) NÃO ficam aqui: viram perguntas em `open-questions.md` (Q-NNN) e hipóteses em `assumptions.md` (A-NNN), registradas pela skill a partir do relatório do subagente.
-->

| ID | Fato | Status | Source | Evidência | Data |
|---|---|---|---|---|---|
| F-005 | <item da área Stack> | KNOWN | repository | `arquivo:linha` | AAAA-MM-DD |
