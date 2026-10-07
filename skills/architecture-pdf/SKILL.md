---
name: architecture-pdf
description: Gera o Documento de Arquitetura de Software em PDF no formato ISO/IEC/IEEE 42010 (capa, sumário, identificação, stakeholders, concerns, viewpoints, visões lógica/processos/implantação/informação, decisões, justificativas, conformidade, referências) a partir da memória .architecture/ e de docs/architecture/, para a arquitetura atual, a proposta ou ambas. Use quando o usuário disser "gerar PDF da arquitetura", "documento de arquitetura de software", "documento 42010", "PDF de arquitetura no padrão", "documentar a arquitetura em PDF", "architecture document pdf", "generate architecture PDF", "ISO 42010 document".
---

# architecture-pdf — Documento de Arquitetura de Software (42010) em PDF

Coordenação, gate de pergunta e conferência rodam na SESSÃO PRINCIPAL (esta skill). A montagem do documento e a geração do PDF são delegadas ao subagente `architecture-documenter` (`sonnet`). O formato (estrutura, tabelas, estilo) está em `~/.claude/skills/architecture/templates/architecture-document/` (`README.md` traz o guia de formato).

## Quando usar
- Fase `6-documentation` (ver skill `architecture`), com a arquitetura validada, ou pedido direto do documento formal em PDF.
- Atualizar o PDF depois de `architecture-update` ou de mudança de ADRs.
- Não usar: para gerar o TO-BE (`architecture-generate`), para decidir (`architecture-adr`, `architecture-tech-evaluation`) ou para a wiki/apresentação do cliente (skill `architecture-publish`, mantida à parte e fora deste repositório: documento interno 42010 e wiki limpa têm regras de separação diferentes).

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar. Ler `context.md`, `decisions.md`, `open-questions.md` e `docs/architecture/README.md`.
2. Definir o ESCOPO com o usuário (uma pergunta, se não foi dito): `atual` (AS-IS), `proposta` (TO-BE) ou `ambas`.
   - `atual` exige `03-as-is/` (fase `1-discovery` DONE).
   - `proposta`/`ambas` exigem `04-to-be/` e fase mínima `4-proposal`. ADR `PROPOSED` aparece como "Proposta", nunca como decisão; sem ADR `ACCEPTED`, a seção 6 sai só com propostas (avisar o usuário).
3. Ambiente de geração: `bash ~/.claude/skills/architecture/templates/architecture-document/setup.sh --check`. Se faltar algo, rodar `setup.sh` sem `--check` (cria venv e `node_modules` LOCAIS em `~/.cache/architecture-pdf`; nada global). Código de saída 3 = sem Chromium: pedir autorização antes de baixar (`npx playwright-core install chromium`) ou usar `CHROMIUM_PATH`; sem navegador, o PDF sai sem diagramas (`--no-mermaid`) e isso deve ser dito ao usuário.

## Gate de pergunta
Antes de delegar, checar a informação mínima. Faltando item de ALTO impacto, chamar `architecture-interview` (uma rodada, 3 a 7 perguntas) ANTES de gerar:

| Seção do documento | Informação mínima |
|---|---|
| 1 Identificação | nome do sistema, versão/marco, autores/responsáveis (nome e papel), data de início, classificação de confidencialidade |
| 2 Stakeholders | pelo menos os grupos de usuários e a equipe responsável, com o que cada um faz no/com o sistema |
| 3 Concerns | requisitos não funcionais com alvo e fonte (`02-requirements/non-functional.md`) |
| 5 a 7 | os documentos de arquitetura do escopo (`03-as-is/` e/ou `04-to-be/`), ADRs e, se houver, `05-diagrams/` |
Dado de identificação que não existe em nenhuma fonte (autor, data de início, classificação) NÃO se inventa: perguntar uma vez, em bloco; sem resposta, vira "A definir".

## Passos
1. Ler as pré-condições e o gate; coletar do usuário: escopo, título (padrão: "Arquitetura de Software — <Sistema> (<escopo>)"), autores, classificação, pasta de saída (padrão `docs/arquitetura/`, FORA da árvore `docs/architecture/`, que não recebe novos arquivos), termos proibidos (`--deny`: nomes de pessoas, custos, siglas internas).
2. Delegar a `architecture-documenter` (prompt abaixo). Subagente único; não paralelizar (escreve um só documento).
3. Conferir o retorno e o PDF: ler `pdfinfo` e renderizar 4 páginas (`pdftoppm -r 60 -png`: capa, sumário, uma com tabela, uma com diagrama) e LER as imagens. Defeito visível (texto cortado, diagrama ilegível, sumário sem página) → devolver ao subagente com a correção pedida.
4. Reconciliar memória: itens `Q-novo-n` do retorno → `open-questions.md` (IDs finais pela regra de IDs provisórios da skill `architecture`; `grep -rn 'novo-' .architecture` = 0). Cada "A definir" do documento deve ter a pergunta correspondente registrada.
5. Entregar ao usuário: caminho do PDF, nº de páginas, seções com "A definir" e perguntas abertas. Oferecer `architecture-review` se o documento for ser base de decisão.

## Delegação
Subagente: `architecture-documenter`. Prompt-base (preencher `<...>`; contexto mínimo: caminhos, não colar arquivos):

```
Fase: 6-documentation. Raiz: <caminho absoluto>. Memória: <raiz>/.architecture/. Documentos: <raiz>/docs/architecture/.
Escopo: <atual | proposta | ambas>. Título: "<título>". Sistema: <nome>. Versão/marco: <...>. Autores: <nome (papel)>. Data do documento: <dd/mm/aaaa>. Início: <mês/ano ou "não informado">. Classificação: <Restrito|Interno|Público>.
Saída: <raiz>/docs/arquitetura/ (Markdown-fonte + PDF). Termos proibidos adicionais (--deny): <lista ou "nenhum">. Fontes extras: <caminhos ou "nenhuma">.
Template e formato: ~/.claude/skills/architecture/templates/architecture-document/ (README.md = guia de formato; document.md = modelo; render_pdf.py; setup.sh).
Regras: nada inventado (sem fonte = "A definir" + pergunta provisória Q-novo-n); ADR ACCEPTED = Decisão, PROPOSED/PROPOSAL = Proposta; AS-IS e TO-BE nunca misturados; sem segredos, sem IDs internos, sem caminhos locais, sem termos de IA; não escrever fora da pasta de saída.
Gere o PDF com render_pdf.py --strict, confira as páginas visualmente e corrija até o lint sair limpo.
Retorne ≤ 40 linhas: ## Escrito / ## Memória / ## Seções com "A definir" / ## Decisões no documento / ## Perguntas sugeridas (≤ 7) / ## ADRs propostos / ## Riscos.
```

## Saída
- `docs/arquitetura/<título>.pdf` e o fonte `docs/arquitetura/<título>.md` (para regenerar com `render_pdf.py`).
- Resposta curta: caminho, páginas, escopo, "A definir" e próxima pergunta.

## Critério de conclusão
- PDF gerado com todas as seções do formato (1 a 10), lint limpo, diagramas legíveis, páginas conferidas.
- Zero decisão fora do status real; zero segredo; zero termo de IA; AS-IS e TO-BE separados.
- Cada "A definir" tem pergunta em `open-questions.md`.

## Dependências (resumo; detalhes no `README.md` do template)
Python 3 com `weasyprint` e `markdown` (venv local), Node com `mermaid` e `playwright-core` (local), um Chromium já instalado, `pdfinfo`/`pdftoppm` (poppler) e a biblioteca Pango do sistema. `setup.sh` prepara tudo em `~/.cache/architecture-pdf`.

## Atualização de state.md
"Execuções": data, `architecture-pdf`, escopo, caminho do PDF, nº de "A definir", HEAD. A fase `6-documentation` só fica DONE com o PDF gerado e revisado (`architecture-review`) quando o usuário exigir documento formal; não regride a fase atual por gerar o PDF.
