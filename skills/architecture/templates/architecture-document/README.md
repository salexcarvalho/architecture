# Documento de Arquitetura de Software (ISO/IEC/IEEE 42010) em PDF

Template, estilo e gerador do PDF de arquitetura. Usado pela skill `architecture-pdf` e pelo subagente `architecture-documenter`. Reproduz o formato de um documento de referência em A4 (capa, sumário, seções 1 a 10); aqui está só a ESTRUTURA e o ESTILO, nunca conteúdo de projeto.

| Arquivo | Para quê |
|---|---|
| `document.md` | modelo Markdown com `{{placeholders}}` e guias (comentários HTML, removidos no PDF) por seção |
| `print.css` | estilo de impressão (A4, tipografia, cores, tabelas, sumário com pontilhado, cabeçalho e rodapé) |
| `render_pdf.py` | Markdown → HTML → PDF (WeasyPrint), numeração dos títulos, sumário com número de página, lint |
| `render_mermaid.mjs` | blocos Mermaid → PNG (Chromium local), paleta azul no estilo C4 |
| `setup.sh` | prepara o ambiente LOCAL (venv + npm em `~/.cache/architecture-pdf`); nada global |

## Guia de formato (o que o documento contém)

Página: A4, margens 2,54 cm. Fonte Aptos (alternativas Carlito, Calibri, Noto Sans, Liberation Sans) 10,5 a 11 pt; código em Consolas/monoespaçada. Cabeçalho em todas as páginas, alinhado à direita: `Classificação de confidencialidade: <nível>`; rodapé discreto `Página X de Y`. Títulos em azul-petróleo `#0F4761`: H1 negrito 16 pt, H2 14 pt, H3 itálico, H4 regular, H5 itálico (letras A), B)... fora da numeração, mas no sumário).

| Parte | Conteúdo obrigatório | Forma |
|---|---|---|
| Capa | Título "Arquitetura de Software — <Sistema> (<escopo>)" e subtítulo itálico "(Conforme ISO/IEC/IEEE 42010)" | sem outros elementos |
| Sumário | todos os títulos H1 a H5 com número de página; o próprio título do documento na 1ª linha | pontilhado, recuo de 11 pt por nível, sem título "Sumário" |
| 1 Identificação do Sistema | Nome do Sistema, Versão, Data da inception, Autores/Responsáveis (+ arquitetura documentada e data do documento); subtítulo "Objetivos:" com lista | tabela chave-valor sem bordas, rótulos em negrito |
| 2 Stakeholders | `Stakeholder` · `Papel / Interesse no Sistema` · `Responsabilidades` | tabela com grade preta, 1ª coluna em negrito |
| 3 Preocupações (Concerns) | `Categoria` · `Descrição da Preocupação Arquitetural` (Segurança, Desempenho, Escalabilidade, Conformidade, Manutenibilidade, Auditabilidade, Usabilidade... só as que têm requisito) | tabela |
| 4 Pontos de Vista (Viewpoints) | `Ponto de Vista` · `Objetivo` · `Stakeholders Atendidos` · `Notação/Modelo Usado` (Lógico, Processos, Implantação, Informação/Dados) | tabela |
| 5 Visões (Views) | 5.1 Lógica, 5.2 Processos, 5.3 Implantação, 5.4 Informação | ver abaixo |
| 6 Decisões Arquiteturais | `Decisão` · `Justificativa` · `Impacto` (+ `Situação`: Decisão, Proposta, Em aberto) | tabela |
| 7 Raciocínio e Justificativas | parágrafo de contexto; 7.1 Decisões Arquiteturais Principais; 7.2 Justificativas Técnicas | listas com rótulo em negrito |
| 8 Correspondências | matriz Preocupação × Visões × Decisões | tabela (a referência salta de 7 para 9; o template preenche 8) |
| 9 Conformidade e Padrões | `Norma / Framework` · `Aplicação` | tabela |
| 10 Referências | lista | bullets |

Visões:

- **5.1 Visão Lógica**: 5.1.1 Camadas e limites (5.1.1.1 Apresentação, 5.1.1.2 Aplicação/APIs, 5.1.1.3 Serviços de Aplicação com blocos `A) Nome` — "Responsável por", "Principais operações", "Orientação de uso" — e tabela `Serviço · Depende de · Produz / Envia para`, 5.1.1.4 Infraestrutura); 5.1.2 Domínio e relacionamentos; 5.1.3 Módulos Funcionais; 5.1.4 Integrações & Eventos; 5.1.5 Fluxos Lógicos Essenciais. Diagramas de container e componente.
- **5.2 Visão de Processos**: frase de abertura e um subtítulo por processo, cada um com "Fluxo geral" (passos), "Serviços envolvidos" e, quando há, diagrama de sequência.
- **5.3 Visão de Implantação**: Plataforma/Ambiente de Execução; Componentes em Execução; Serviços Gerenciados; Mensageria & Filas; Observabilidade; Topologia/Exposição; Segurança & SSL; Deploy/CI-CD; Configuração por Ambiente. Diagrama de implantação.
- **5.4 Visão de Informação**: Camada de Persistência (texto), tabela `Entidade · Descrição · Relacionamentos`, ERD.

Tabelas: grade preta 0,9 pt, contorno e linha do cabeçalho 1,4 pt, texto 9,8 pt. Diagramas: PNG centralizado com legenda em negrito acima ("Figura N — título"), caixas azuis `#438DD5`, atores azul-escuro `#08427B`.

## Sintaxe do Markdown (além do comum)

- Front-matter: `titulo`, `subtitulo`, `classificacao`, `autor`.
- Títulos sem número; o renderizador numera H1 a H4 (`1`, `1.1`, `1.1.1`, `1.1.1.1`). `{.nonum}` no fim do título suprime o número.
- Bloco ` ```kv ` com linhas `Rótulo: valor` para a tabela de identificação.
- Bloco ` ```mermaid ` com `%% titulo: <legenda>` na 1ª linha. Prefira `flowchart TD` (LR largo vira ilegível), até 12 nós por diagrama, rótulos sem acento ou entre aspas. `sequenceDiagram` e `erDiagram` também funcionam.
- Listas aninhadas com 4 espaços; continuação de item na mesma linha (`- **Título:** texto`).

## Uso

```bash
bash setup.sh            # uma vez: venv (weasyprint, markdown) + npm (mermaid, playwright-core) em ~/.cache/architecture-pdf
~/.cache/architecture-pdf/venv/bin/python render_pdf.py documento.md saida.pdf --strict
```

- `--lint-only` valida sem gerar; `--strict` falha com termos de IA, IDs internos de memória, marcadores `[KNOWN ·...]`, caminhos locais, valores que parecem segredo e `{{placeholders}}` restantes; `--deny REGEX` acrescenta termos proibidos (nomes de pessoas, custos, siglas internas).
- `--keep-work DIR` guarda o HTML e os PNG dos diagramas; `--no-mermaid` não renderiza diagramas.
- Variáveis: `ARCH_PDF_HOME` (padrão `~/.cache/architecture-pdf`), `CHROMIUM_PATH` (navegador). O `setup.sh` reaproveita um Chromium já baixado (Playwright em `~/.cache/ms-playwright`, Chrome ou Chromium do sistema); se não houver nenhum, imprime o comando e sai com código 3 sem baixar nada.

## Dependências

| Item | Para quê | Onde fica |
|---|---|---|
| Python 3 + `weasyprint` + `markdown` | HTML/CSS → PDF (sumário com `target-counter`, cabeçalho e rodapé) | venv em `$ARCH_PDF_HOME/venv` |
| Node + `mermaid` + `playwright-core` | diagramas Mermaid → PNG | `$ARCH_PDF_HOME/node` |
| Chromium | renderizar o Mermaid | já instalado; não é baixado pelo script |
| `pdfinfo`, `pdftoppm` (poppler) | contagem de páginas e conferência visual | sistema |

Biblioteca de sistema exigida pelo WeasyPrint: Pango (`libpango-1.0`).
