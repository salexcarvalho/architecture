# Checklist de classificação e de qualidade (use na Fase 1 e antes de entregar a Fase 2)

## 1. Classificar TODA afirmação (interno; o rótulo não aparece no slide)

| Classe | Critério | Como aparece no slide |
|---|---|---|
| FACT | Verificável no repositório, documento do cliente, inventário ou declaração registrada com data | Afirmação direta, sem selo |
| DECISION | ADR ACCEPTED ou aprovação registrada (resposta do usuário com data) | Afirmação direta + selo "Decisão" quando houver contraste com proposta |
| PROPOSAL | Desenho sugerido, ainda sem aprovação | Selo "Proposta"; verbo condicional ("propõe-se") |
| ASSUMPTION | Hipótese sem evidência | Selo "Hipótese" ou remover; nunca como fato |
| RISK | Limitação ou incerteza real | Linha na tabela de riscos: Restrição atual / Impacto / Mitigação / Caminho de evolução. Risco real nunca é omitido |
| OPEN QUESTION | Falta decisão ou dado | "A definir com o cliente" + dono (papel) + prazo proposto, no slide de pedidos |

Regra: só FACT e DECISION aprovada são definitivas. PROPOSAL, ASSUMPTION e OPEN QUESTION nunca ganham tom de definitivo. Afirmação sem classe = remover.

Hoje × evolução: o que existe/foi decidido é "hoje" (selo Decisão); o que o desenho permite sem decisão é "capacidade/evolução" (selo Capacidade, tracejado). Nunca misturar.

## 2. Negativas e matrizes

- [ ] Toda avaliação negativa (nota baixa, "não atende", "limitado") tem EVIDENCE; sem evidência = NOT EVALUATED ou removida.
- [ ] Limitação real = linha de risco (Restrição atual / Impacto / Mitigação / Caminho de evolução), não adjetivo.
- [ ] Nenhuma alternativa rebaixada para justificar outra (mesma régua, mesmos critérios, mesma fonte para todas).
- [ ] Todo SCORE tem JUSTIFICATION + EVIDENCE no `radar-data.json`.
- [ ] "Experiência da equipe/time" NÃO é nota: usar "Precedente na organização" (régua única, igual para todas as alternativas) ou NOT EVALUATED quando faltar evidência. Capacidade interna declarada pelo usuário = evidência `U`, só para o que foi declarado.
- [ ] Restrição do cliente (tecnologia imposta) é filtro explícito, não nota baixa da alternativa.
- [ ] Critério avaliado só para algumas alternativas fica fora do radar e é listado como n/a.
- [ ] Padrões já adotados pela organização/cliente são valorizados (coluna Precedente, linha no "por que esta").

## 3. Separações obrigatórias

- [ ] Banco: motor (decisão a) e hospedagem (decisão b) em slides/decisões separados.
- [ ] Segurança em seis controles distintos: RBAC, autenticação, autorização, segurança da aplicação, segurança do banco, auditoria.
- [ ] Escalabilidade, resiliência, alta disponibilidade e recuperação de desastres tratadas como capacidades diferentes (cada uma com hoje × evolução, meta e prova).
- [ ] Arquitetura sem rótulo de estilo: camadas; LB → App/API 1..N → banco; escala horizontal da aplicação × vertical/HA do banco tratada à parte (não afirmar escala horizontal do banco sem decisão).

## 4. Forma

- [ ] ≤ 20 slides; uma pergunta por slide; título = afirmação (≥ 4 palavras, ≤ 56 caracteres, sem "Nome: explicação").
- [ ] Diagrama, fluxograma ou indicador em cada slide (nunca documento projetado); 2–3 fluxogramas principais.
- [ ] Sem IDs internos (F-/A-/Q-/R-/P-/RF-/RNF-/RES-/TD-/G-/RV-NNN, ADR-, DEC-), sem custos, sem nomes de pessoas (papéis/áreas), sem caminhos locais, sem menção à ferramenta de IA.
- [ ] Tom de domínio técnico e governança: nada de termos de `termos-banidos.txt`.
- [ ] Pedidos ao cliente com dono (papel) e prazo proposto; datas dd/mm/aaaa.
- [ ] Números do deck = números da wiki e da documentação (mesmos nomes e valores).

## 5. Entrega

- [ ] `REVISAO.md` (10 seções) e `radar-data.json` gerados na Fase 1 e conferidos pelo usuário (Anexo B resolvido).
- [ ] `build.sh` sem aviso de transbordo; `verify_deck.py` = 0 problemas.
- [ ] TODOS os slides lidos como imagem (Read), um a um ou em folhas de contato + os densos individualmente.
- [ ] PDF e PPTX com a mesma contagem do HTML; notas do PPTX presentes.
