# Baseline de Segurança — <Nome do Sistema>

<!--
Local: `docs/architecture/08-security/security-baseline.md`. Escrito por `security-privacy-architect`.
Controles-base atuais (KNOWN, com evidência) e propostos (PROPOSAL): autenticação, autorização, segredos (só NOMES), criptografia, logs/auditoria, dependências. Ameaças por fluxo: `threat-model.md`.
Proibido: expor segredos; afirmar conformidade com LGPD (ou lei equivalente) sem evidência. Sem evidência = "não verificado" + [OPEN].
Controles existentes só com evidência (KNOWN). Controles propostos = PROPOSAL.
Começar pelo cabeçalho padrão (templates/doc-section.md).
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |
| **Base** | `../04-to-be/security.md`, `../03-as-is/*` |

## 1. Autenticação, autorização e segredos
| Tema | Situação atual | Proposta | Marcador |
|---|---|---|---|
| Autenticação | <mecanismo encontrado> | <proposta> | [KNOWN · F-0NN] / [PROPOSAL · P-0NN] |
| Autorização | <modelo: RBAC etc.> | <proposta> | |
| Gestão de segredos | só nomes de variáveis lidos | <proposta> | |
