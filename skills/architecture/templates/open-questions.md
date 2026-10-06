# Open Questions

<!--
Local: `.architecture/open-questions.md`.
Regra de ouro: NÃO registrar como pergunta o que o repositório já responde (ver "busca antes de perguntar").
Colunas:
- ID: Q-NNN.
- Pergunta: específica e respondível. Cite o achado do repositório quando houver.
- Por que importa: impacto arquitetural em 1 linha.
- Bloqueia: documento/decisão/fase que depende da resposta.
- Prioridade: alta | média | baixa (por impacto; restrições duras = alta).
- Rodada: número da rodada de entrevista em que foi (ou será) feita.
- Status: OPEN | ANSWERED | DEFERRED.
- Resposta + data: texto resumido; ao responder, gerar/atualizar F-NNN, A-NNN ou R-NNN correspondente.
DEFERRED exige motivo e hipótese adotada (A-NNN) enquanto não houver resposta.
-->

**Última atualização:** AAAA-MM-DD

| ID | Pergunta | Por que importa | Bloqueia | Prioridade | Rodada | Status | Resposta | Data |
|---|---|---|---|---|---|---|---|---|
| Q-001 | Existe obrigação regulatória (ex.: proteção de dados pessoais) sobre os dados armazenados? | Define criptografia, retenção e hospedagem | `08-security/*`, `04-to-be/infrastructure.md` | alta | 1 | ANSWERED | Sim, há dados pessoais sensíveis | AAAA-MM-DD |
| Q-002 | Identifiquei no `docker-compose.yml` um serviço de cache. Qual o pico de usuários simultâneos esperado? | Dimensiona cache e banco | `02-requirements/non-functional.md` | alta | 1 | OPEN | — | — |
| Q-003 | Há janela de manutenção aceitável? | Define estratégia de deploy | `04-to-be/deployment.md` | média | 2 | DEFERRED | Sem resposta; hipótese A-004 | AAAA-MM-DD |
