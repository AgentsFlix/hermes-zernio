# Hermes Zernio

Processo público e verificável para um Hermes descobrir e operar uma conta Zernio com segurança.

## Ativação

Forneça a chave somente em um canal seguro. Em seguida, diga ao Hermes:

> Leia e ative esta skill: https://raw.githubusercontent.com/AgentsFlix/hermes-zernio/main/skills/integrations/zernio-operations/SKILL.md. Salve `ZERNIO_API_KEY` apenas no ambiente protegido do perfil atual e faça exclusivamente o inventário de leitura.

A skill não publica, agenda, responde, envia DM, cria automação, altera campanhas, nem apaga conteúdo por inferência.

## O que ela faz

1. Valida a credencial por leitura de menor impacto.
2. Lista perfis, contas conectadas, posts, webhooks e escopos acessíveis.
3. Separa capacidades de leitura das ações externas.
4. Exige aprovação explícita, payload exato e verificação posterior para toda escrita.
5. Mantém IDs e segredos fora de relatórios públicos.

## Fontes oficiais

- [Quickstart](https://docs.zernio.com/)
- [OpenAPI](https://zernio.com/openapi.yaml)
- [MCP](https://docs.zernio.com/mcp)
- [CLI](https://docs.zernio.com/cli)
- [Idempotência](https://docs.zernio.com/idempotency)
- [Webhooks](https://docs.zernio.com/webhooks)

Leia [START_HERE.md](START_HERE.md) para o protocolo completo. Este repositório contém processo, não credenciais nem dados de contas.