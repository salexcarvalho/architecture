# Ambientes — <Nome do Sistema>

<!--
Local: `docs/architecture/09-operations/environments.md`. Escrito por `platform-architect`.
Listar apenas ambientes confirmados (evidência) ou propostos (PROPOSAL). Variáveis: SOMENTE nomes, nunca valores.
Não criar ambiente "por completude": cada ambiente precisa de propósito claro.
-->

| Campo | Valor |
|---|---|
| **Status do documento** | DRAFT |
| **Última atualização** | AAAA-MM-DD |

## 1. Inventário de ambientes

| Ambiente | Propósito | Hospedagem | Dados | Acesso | Promoção a partir de | Marcador |
|---|---|---|---|---|---|---|
| local | desenvolvimento | máquina do desenvolvedor / contêineres | sintéticos | desenvolvedores | — | [KNOWN · F-0NN] |
| homologação | validação pré-produção | <hospedagem> | anonimizados | time + validadores | main | [KNOWN · F-0NN] |
| produção | uso real | <hospedagem> | reais | restrito | homologação | [KNOWN · F-0NN] |

## 2. Paridade entre ambientes

| Aspecto | local | homologação | produção | Diferença aceitável? |
|---|---|---|---|---|
| Versão do banco | <x> | <x> | <x> | sim/não |
| Proxy/TLS | não | sim | sim | sim |

## 3. Configuração (somente nomes)

| Variável | Finalidade | Obrigatória | Onde é definida | Tem segredo? |
|---|---|---|---|---|
| `DATABASE_URL` | conexão com o banco | sim | gerenciador de segredos / `.env` local | sim (valor não lido) |
| `LOG_LEVEL` | nível de log | não | variável do ambiente | não |

## 4. Promoção e controle de mudanças
- Fluxo: <ex.: merge → build → deploy em homologação → aprovação → produção> [KNOWN · F-0NN] ou [PROPOSAL · P-0NN]
- Aprovações necessárias: <quem>
- Rollback: <como reverter>; ver `runbooks.md`

## 5. Dados em ambientes não produtivos
| Ambiente | Origem dos dados | Anonimização | Marcador |
|---|---|---|---|
| homologação | cópia da produção? | [OPEN · Q-0NN] | |

## 6. Pontos em aberto
- [OPEN · Q-0NN] <pergunta>
