# Backup e Restore — <Nome do Sistema>

<!--
Local: `docs/architecture/09-operations/backup-restore.md`. Escrito por `platform-architect`. Cenários de desastre e failover: `disaster-recovery.md`.
Um backup só existe se o restore foi TESTADO. Registrar data do último teste; sem teste = "não testado" + [RISK].
RPO/RTO: valores só com fonte (usuário/contrato). Sem fonte: [OPEN] e hipótese marcada como ASSUMPTION.
Nunca registrar credenciais ou endpoints com segredo.
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |

## 1. Objetivos de recuperação

| Serviço / dado | RPO (perda máx. de dados) | RTO (tempo máx. de recuperação) | Fonte | Marcador |
|---|---|---|---|---|
| Banco principal | 1 h | 4 h | usuário, AAAA-MM-DD | [KNOWN · F-012] |
| Arquivos enviados | 24 h | 8 h | hipótese | [ASSUMPTION · A-0NN] |
| Configuração/IaC | 0 (versionado em git) | 1 h | repositório | [KNOWN · F-0NN] |

## 2. Estratégia de backup

| Item | Tipo (completo/incremental/WAL/snapshot) | Frequência | Retenção | Destino | Criptografado | Marcador |
|---|---|---|---|---|---|---|
| Banco principal | completo + log contínuo | diário + contínuo | 30 dias | <destino> | <sim/não> | [PROPOSAL · P-0NN] |
| Arquivos enviados | incremental | diário | 30 dias | <destino> | <sim/não> | [OPEN · Q-0NN] |

## 3. Procedimento de restore
1. Declarar incidente e identificar o ponto no tempo alvo.
2. Provisionar ambiente de restore isolado.
3. Restaurar <item> a partir de <origem>; validar integridade (contagem de registros, checksum).
4. Validar a aplicação contra o restore (smoke test).
5. Promover/reapontar tráfego; registrar horário e duração (medir RTO real).

## 4. Testes de restore

| Data | Escopo | Resultado | RPO/RTO medidos | Responsável |
|---|---|---|---|---|
| AAAA-MM-DD | banco principal em ambiente isolado | sucesso / falha | RPO 40 min / RTO 3 h | <papel> |

<!-- Frequência recomendada: definir com o usuário. Se nunca testado: "não testado" + [RISK · R-0NN]. -->

## 5. Responsabilidades e contatos
| Papel | Responsável | Contato (canal, não dados pessoais) |
|---|---|---|
| Executor do restore | <papel> | <canal> |

## 6. Riscos
- [RISK · R-0NN] <ex.: restore nunca testado>
