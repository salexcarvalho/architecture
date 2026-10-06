---
name: architecture-adr
description: Cria e atualiza ADRs (Architecture Decision Records) e controla o status PROPOSED/ACCEPTED/SUPERSEDED/REJECTED/DEPRECATED; ACCEPTED só com Evidence de aprovação do usuário. Use quando o usuário disser "criar ADR", "registrar decisão", "aprovar decisão", "aceitar o ADR", "substituir decisão", "decision record", "record architecture decision", "supersede ADR".
---

# architecture-adr — decisões de arquitetura

Trabalho de template + regra de estado; roda na sessão principal e não delega.

## Quando usar
- Um especialista propôs um ADR (retorno "ADRs propostos") ou há uma proposta P-NNN relevante.
- O usuário tomou/aprovou uma decisão e é preciso registrá-la (PROPOSED → ACCEPTED).
- Uma decisão aceita mudou (novo ADR que substitui o antigo) ou foi descartada (REJECTED/DEPRECATED).
- Tecnologia avaliada em `architecture-tech-evaluation` com escolha relevante.

## Pré-condições
1. Ler `.architecture/state.md`. Se não existir: orientar `architecture-start` e parar.
2. Ler `.architecture/decisions.md` (índice, próximo número NNN), `open-questions.md`, `interview-log.md`, e o ADR existente se for atualização.
3. Verificar se a decisão é RELEVANTE: afeta estrutura, custo, segurança, dados, operação, ou é difícil de reverter. Se não for, não criar ADR: manter como P-NNN em `decisions.md` ou apenas registrar no documento.

## Estados e transições

| Estado | Significado | Quem/quando | Exigência |
|---|---|---|---|
| PROPOSED | proposta registrada, sem aprovação | criação por esta skill a partir de proposta de especialista ou do usuário | contexto factual, ≥ 2 opções, avaliação |
| ACCEPTED | aprovada pelo usuário | somente após aprovação explícita | **Evidence obrigatória** |
| REJECTED | usuário recusou | resposta do usuário registrada | motivo + data |
| SUPERSEDED | substituída por ADR mais novo | criação do ADR substituto | campos Supersedes / Superseded by preenchidos nos dois |
| DEPRECATED | deixou de se aplicar sem substituto | decisão do usuário | motivo + data |

**REGRA CRÍTICA: ACCEPTED só com Evidence de aprovação do usuário.** Evidence válida = (a) resposta do usuário registrada com data em `interview-log.md` ou no `state.md` (citar rodada/linha), (b) PR aprovado (link), (c) ata/documento do usuário (caminho/link). "Parece razoável", silêncio ou aprovação implícita NÃO são evidência. Sem Evidence o ADR permanece PROPOSED. Nunca editar a Decision de um ADR ACCEPTED: criar ADR substituto.

## Passos
1. **Criar ADR (PROPOSED):**
   - Arquivo: `docs/architecture/06-decisions/ADR-NNN-titulo-curto.md` (NNN = próximo número de 3 dígitos; título em minúsculas com hífens). Modelo: `~/.claude/skills/architecture/templates/adr.md`.
   - Preencher TODAS as seções: Context (fatos com `[KNOWN · F-NNN]`), Problem, Options (≥ 2; incluir "não fazer nada" quando cabível), Evaluation (tabela critérios × opções, com fonte), Decision (como "Proposta: ..."), Consequences (+/−), Risks, Rollback, Status, Date, Evidence (`—`), Supersedes/Superseded by.
   - Opções e avaliação vêm de evidências (tech-evaluation, requisitos não funcionais, fatos); proibido justificativa vaga ("é moderno", "é padrão de mercado").
   - Seção sem conteúdo com fonte: não inventar; registrar `[OPEN · Q-NNN]` e manter PROPOSED.
2. **Aprovar (PROPOSED → ACCEPTED):**
   - Confirmar com o usuário (texto: "Aprova o ADR-NNN, opção X? sim/não/ajustar") — pode usar `AskUserQuestion`.
   - Registrar a resposta em `interview-log.md` (data + resposta resumida) e preencher `Evidence` com a referência exata. Só então Status = ACCEPTED, Date = data da aprovação.
   - Atualizar documentos afetados: `[PROPOSAL · P-NNN]` → `[DECISION · ADR-NNN]`.
3. **Recusar:** Status REJECTED + motivo + data; manter arquivo (histórico); remover a proposta do TO-BE ou marcá-la `[OPEN]`.
4. **Substituir:** criar ADR novo (PROPOSED → ACCEPTED pelo mesmo processo) com `Supersedes: ADR-NNN`; no antigo, Status SUPERSEDED e `Superseded by: ADR-MMM`. Não reescrever o texto do antigo.
5. **Atualizar `.architecture/decisions.md`**: índice (id, título, status, data, evidence, substitui/substituído) e remover de "Propostas sem ADR" as que viraram ADR.
6. Registrar riscos novos da decisão em `risks.md` e fechar perguntas respondidas em `open-questions.md`.
7. Atualizar a linha do ADR no `docs/architecture/README.md`.

## Delegação
Nenhuma. Para levantar opções/avaliação técnica com leitura pesada, chamar antes `architecture-tech-evaluation` ou a skill do domínio (`architecture-api`, `architecture-data`, `architecture-infrastructure`, `architecture-devops`, `architecture-security`).

## Gate de pergunta
Antes de criar o ADR: contexto factual suficiente? ≥ 2 opções reais? critérios de avaliação definidos pelo requisito? Falta item de alto impacto → `architecture-interview`. Antes de ACCEPTED: aprovação explícita registrada.

## Saída
- ADR(s) em `docs/architecture/06-decisions/`, `decisions.md` atualizado, documentos afetados com marcadores corretos.
- Mensagem ao usuário: ADRs criados/alterados e o que falta para aprovação (se for o caso).

## Critério de conclusão
- Todo ADR com todas as seções e ≥ 2 opções; todo ACCEPTED com Evidence (zero ACCEPTED sem Evidence); índice consistente com os arquivos; nenhuma decisão inventada.

## Atualização de state.md
"Execuções": data, `architecture-adr`, ADRs afetados (ex.: ADR-003 PROPOSED→ACCEPTED), HEAD. "Pontos de validação pendentes": ADRs PROPOSED aguardando aprovação. Quando todos os ADRs da proposta estiverem decididos (ACCEPTED/REJECTED): `5-validation` DONE e próxima fase `6-documentation`.
