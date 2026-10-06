---
name: architecture-security
description: Arquitetura de segurança e privacidade/LGPD com threat model (STRIDE leve), controles, autenticação/autorização e gestão de segredos. Use quando o usuário disser "arquitetura de segurança", "threat model", "modelagem de ameaças", "LGPD", "privacidade", "autenticação e autorização", "security architecture", "privacy review".
---

# architecture-security — segurança e privacidade

## Quando usar
- Threat model, controles, autenticação/autorização, segredos e checklist de privacidade (LGPD ou lei equivalente).
- Em `architecture-generate` roda na ONDA 2 (depois de application/data/platform). Isoladamente, pode rodar a qualquer momento, desde que haja AS-IS ou TO-BE para analisar.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Existir AS-IS e, preferencialmente, TO-BE (`04-to-be/{architecture,data,infrastructure}.md`). Ler `known-facts.md`, `assumptions.md`, `open-questions.md`, `risks.md`, `decisions.md`, `02-requirements/non-functional.md`.
3. Passar pelo GATE DE PERGUNTA.

## Gate de pergunta
Informação mínima (para `04-to-be/security.md` e `08-security/{threat-model,privacy-lgpd,security-baseline}.md`): existência e tipo de dados pessoais/sensíveis; base regulatória aplicável; mecanismo de autenticação atual e provedor de identidade imposto; integrações externas e o que trafega; ativos críticos; requisitos de auditoria; papel de encarregado/responsável por privacidade. Falta item de ALTO impacto (dados pessoais, regulatório, identidade) → `architecture-interview` antes de delegar. Antes de perguntar, procurar em código de autenticação, configuração de CORS/headers, migrations (colunas pessoais), docs e CI (análise de dependências).

## Passos
1. Definir escopo (sistema inteiro, uma fronteira, um fluxo).
2. Delegar a `security-privacy-architect` (prompt abaixo), informando os caminhos dos documentos produzidos pelos demais especialistas.
3. Reconciliar: memória (IDs finais — renumerar os IDs provisórios `<TIPO>-novo-<n>` nos documentos escritos pelo subagente, conforme a regra da skill `architecture` (conferir `grep -rn 'novo-' docs/architecture` = 0)), riscos → `risks.md`, ADRs propostos → `architecture-adr`, perguntas filtradas → `architecture-interview` se alto impacto.
4. Conferir: nenhuma afirmação de conformidade sem evidência (padrão = "não verificado" + `[OPEN]`); nenhum segredo exposto; controles existentes só com evidência; controles novos marcados PROPOSAL.
5. Atualizar `docs/architecture/README.md`.

## Delegação
Subagente: `security-privacy-architect`. Prompt-base:

```
Fase: <4-proposal | 8-evolution>. Raiz: <caminho absoluto>. Memória: <caminho>/.architecture/ (leia known-facts.md, assumptions.md, open-questions.md, risks.md, decisions.md).
Insumos: docs/architecture/03-as-is/*, docs/architecture/04-to-be/{architecture,applications,integrations,data,infrastructure,deployment}.md (os que existirem), docs/architecture/02-requirements/non-functional.md. IDs relevantes: <F-..., RNF-..., Q-..., R-...>. Escopo: <sistema | fronteira X | fluxo Y>.
ÚNICOS arquivos que pode escrever: docs/architecture/04-to-be/security.md e docs/architecture/08-security/{threat-model,privacy-lgpd,security-baseline}.md (somente estes 3 na pasta; cada um só se houver conteúdo com fonte). Riscos NÃO têm arquivo: devolva-os como `R-novo-n` no retorno (a skill registra em `.architecture/risks.md`).
Cobrir (o que se aplicar): ativos e classificação; fronteiras de confiança (diagrama Mermaid); STRIDE leve por componente/fluxo (só ameaças plausíveis); autenticação/autorização (modelo atual e proposto); gestão de segredos (por NOMES, nunca valores); criptografia em trânsito/repouso; auditoria/log de segurança; dependências e supply chain; checklist de privacidade (inventário de dados pessoais, base legal, retenção, direitos do titular, incidentes, operadores/terceiros).
Regras: você PROPÕE, não decide. NUNCA exponha segredos. NUNCA afirme conformidade com LGPD (ou lei equivalente) sem evidência citada: o padrão é "não verificado" + [OPEN · Q-NNN]. Controles existentes só com evidência [KNOWN]; novos como [PROPOSAL]. Escolhas relevantes com ≥ 2 alternativas. Não crie ADR nem marque ACCEPTED.
Modelos: ~/.claude/skills/architecture/templates/{to-be,threat-model,security-baseline,privacy-lgpd,doc-section}.md.
IDs novos: `P-novo-n`, `Q-novo-n`, `A-novo-n`, `F-novo-n`, `R-novo-n` (a skill renumera).
Retorne ≤ 40 linhas: ## Escrito / ## Memória (Status+Source+evidência) / ## Perguntas sugeridas (≤ 7, por impacto) / ## ADRs propostos / ## Riscos.
```

## Saída
- `04-to-be/security.md` e `08-security/{threat-model,privacy-lgpd,security-baseline}.md` (somente com conteúdo); riscos em `.architecture/risks.md`; ADRs PROPOSED quando relevante.
- Mensagem ao usuário: principais riscos, lacunas de privacidade "não verificado", perguntas.

## Critério de conclusão
- Ameaças priorizadas com mitigação proposta; privacidade com evidência ou `[OPEN]`; nenhum segredo exposto; nenhuma conformidade afirmada sem evidência; nenhum documento vazio.

## Atualização de state.md
"Execuções": data, `architecture-security`, escopo, HEAD, arquivos. Em `4-proposal`: com a onda 2 concluída, sinalizar que o reviewer pode rodar (`architecture-review`); registrar Q-IDs críticos em "Bloqueios".
