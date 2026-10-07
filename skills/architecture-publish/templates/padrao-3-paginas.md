# Padrão "Nova Arquitetura" — 3 páginas de wiki (Tecnologias Avaliadas, Componentes, Banco de Dados)

Espec de referência da skill `architecture-publish`. As 3 páginas são sempre geradas no mesmo formato. Com legado: ficam sob `<Sistema>/Arquitetura/Nova-Arquitetura-da-API/` (+ página-pai `Nova-Arquitetura-da-API.md`); sem legado: ficam direto em `<Sistema>/` (a página-pai é a landing `<Sistema>.md`, ver `wiki-landing-sistema.md`). Origem do formato visual: página "Tecnologias avaliadas" de um produto anterior da mesma wiki.

AJUSTE DA REGRA DE SEPARAÇÃO (prevalece sobre o texto abaixo): a wiki é a versão LIMPA para o cliente. Nenhum ID interno (F/A/Q/R/P/RF/RNF/RES/ADR/DEC), nenhum selo PROPOSAL/DECISION, nenhuma página de decisões, riscos ou perguntas. Onde o espec abaixo fala em "DEC-NN"/"registro de decisão", a coluna `Registro` usa texto em linguagem simples: `Definida no projeto` | `Decisão de arquitetura` | `A definir com <cliente>` | `Adiado até medir`. Rastreabilidade por ID fica só no repositório do sistema.

## Estrutura
- Pai `<Sistema>/Arquitetura/Nova-Arquitetura[-da-API].md` (~20 linhas): linha 1 em negrito com ponto final; callout `> **Situação:** proposta em validação ... Descreve o destino, não o sistema em produção.`; 2 parágrafos de contexto (destino: front → API /v1 + worker, banco, cache, IdP, storage); `## Páginas desta seção` tabela `| Página | Para quê |` (3 linhas); `## Ver também` links separados por ` · `; termina com `[[_TOSP_]]`.
- `.order` = `Tecnologias-Avaliadas`, `Componentes`, `Banco-de-Dados` (sem extensão, sem newline final).
- Sem H1, sem `[[_TOC_]]`, sem `---`, sem selos/emoji (exceto ✅ na linha escolhida das notas). Links absolutos sem .md. Mermaid só `::: mermaid` … `:::`. Datas dd/mm/aaaa. Rastreio em linguagem simples (sem IDs); marcar "planejado", "a confirmar", "ainda não".
- Cabeçalho comum das filhas: `**<Tema> da nova API do <SISTEMA>.**`; callout `> **Resumo:** …` + `>` + `> **Como ler:**` (Tecnologias) / `> **Contexto:**` (Componentes) / `> **Estado:**` (Banco); linha `Páginas relacionadas: [A](..), [B](..) e [C](..).` Corpo em H2, H3 só dentro de seção. Tom tabular, denso, afirmativo; texto corrido curto.

## Tecnologias-Avaliadas
1. `## Contexto que condiciona todas as escolhas` — `| Fato | Efeito nas escolhas |`.
2. `## Resumo das escolhas` — `| # | Camada | Escolha | Registro | Comparativo | Alternativas principais |` (Comparativo = Sim/Parcial/Só registro) + `Resultado: **N …**`.
3. `## Como ler os comparativos visuais` — `| Faixa | Leitura |` (9 a 10 / 7 a 8 / 5 a 6 / 3 a 4 / 0 a 2) + parágrafo "As notas **não são medição**…" e definição de †.
4. `## N. <Camada>` (uma por camada): `**Pergunta:**` opcional; tabela `| Alternativa | Vantagens | Desvantagens | Resultado |` (escolhida em negrito, `**Escolhida**`; demais `Descartada`) — ou `| Alternativa | Avaliação | Resultado |` sem comparativo formal; linhas `**Critérios:**`, `**Motivo:**`/`**Decisão:**`, `**Lacuna:**`, `**Referência:**`; `### Comparativo visual`: imagem `![<sistema>-<slug>.png](/.attachments/<sistema>-<slug>-<uuid>.png)` + tabela `| Alternativa | <crit1> | … | <critN> | Média | Situação |` (escolhida: `✅ **Nome**`, notas/média/situação em negrito) + 2 linhas fixas:
   - "Escala de 0 a 10 (10 = melhor para o <SISTEMA>; em custo, esforço e quantidade de componentes, 10 = menor). Notas sem marca traduzem o que o comparativo registrado mostra; a média é simples e serve só de apoio à leitura, a decisão segue o registro acima."
   - "† Avaliação da equipe de arquitetura, sem comparativo formal registrado."
5. `## Escolhas complementares` — `| Tema | Escolha | Alternativas | Registro |`.
6. `## Como a comparação foi conduzida e o que ficou aberto` — 3 bullets.

## Imagens (gráfico radar/polar matplotlib)
- 1 PNG por camada; título à esquerda "Comparação — <Camada>" ~14 pt; 3–5 eixos = critérios (rótulos 2 linhas ~10 pt); anéis tracejados cinza 2/4/6/8/10; círculo externo preto; legenda fora, canto sup. direito, 1ª entrada com "(escolhida)".
- Série 1 = escolhida, azul, traço ~4 pt, preenchimento azul translúcido; demais traço ~2 pt: vermelho, verde, roxo, alfa ~0.1. DejaVu Sans. Figura ~9x7 pol, bbox tight (~1100x870 px). Escala 0–10, mesmas notas da tabela; 2–4 alternativas.
- Nome `<sistema>-<slug>.png` no texto alternativo; o arquivo em git é `.attachments/<sistema>-<slug>-<uuid4>.png`. Gerador: `scripts/radar_charts.py`.

## Componentes
`## Diagrama de componentes` (mermaid `graph LR`, subgraphs Navegador / Serviços compartilhados do cliente / Hospedagem (VM, contêineres); setas contínuas síncrono, tracejadas externo/telemetria; rótulos sem acento) · `## Fluxo de uma requisição autenticada` (`sequenceDiagram`) · `## Catálogo de componentes` `| Componente | Responsabilidade | Comunicação | Estado no repositório |` · `## Pipelines` `| Pipeline | Gatilho | O que faz |` · `## Configuração por componente` ("Apenas nomes. Valores ficam no Coolify…") `| Componente | Variáveis | Observação |` · `## Contratos e limites da borda` `| Controle | Valor | Dono | Registro |` · `## Estado de implementação (dd/mm/aaaa)` `| Já na develop | Planejado (sprint) |` · `## Lacunas`.

## Banco-de-Dados
`## Números do baseline` `| Item | Valor |` · `## Schemas e o que não migra` · `## Papéis do banco` `| Papel | Uso | Privilégios |` + "Regras:" · `## Tabelas` (parágrafo "Convenção:" + H3 por domínio, `| Tabela | Finalidade | Principais colunas | FK |`) · `## Diagrama ER: <domínio>` (`erDiagram`) · `## Estratégia de migrations` `| Tema | Regra |` + `| Migration | O que faz |` · `## O que sai do banco e vai para a API` · `## Dados que migram` · `## Retenção, dados pessoais e mascaramento` · `## Backup e recuperação` · `## Lacunas e pontos em aberto`.
