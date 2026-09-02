# Mapa de capacidade Zernio

Fonte primária: [documentação Zernio](https://docs.zernio.com/), [OpenAPI](https://zernio.com/openapi.yaml), consultados em 2026-09-02.

## Descoberta

| Recurso | Operação segura inicial | Resolve |
|---|---|---|
| Perfis | `GET /v1/profiles` | contêineres de marcas/projetos |
| Contas | `GET /v1/accounts` | plataforma, perfil e conta conectada |
| Posts | `GET /v1/posts` | publicação, agendamento e estado já existente |
| Webhooks | `GET /v1/webhooks` | integrações outbound existentes |
| Analytics | endpoints `GET /v1/analytics/*` | métricas de conta e post |
| Inbox | endpoints `GET /v1/inbox/*` | conversas e status, sem marcar como lido |

Antes de pedir um ID ao usuário, liste o recurso complementar apropriado. Exemplo: para publicar em uma conta social, consulte contas e perfis ativos antes de pedir o `accountId`.

## Escrita que exige aprovação por payload

| Área | Exemplos |
|---|---|
| Conteúdo | criar, agendar, editar, cancelar ou apagar post; upload de mídia |
| Inbox | enviar DM, responder comentário/review, editar/deletar comentário, marcar conversa como lida |
| Automação | criar sequência, broadcast, workflow ou comment-to-DM |
| Integração | conectar/desconectar conta, criar ou alterar webhook |
| Ads | criar/pausar campanha, anúncios, públicos, conversões, orçamento |
| Comunicação | WhatsApp, SMS, chamadas, Telegram, Discord ou Slack |

## Postagem confiável

O endpoint de criação aceita `x-request-id`. Gere uma UUID por post lógico e reutilize apenas se repetir exatamente a requisição após falha transitória. A documentação declara duas barreiras: a mesma `x-request-id` retorna o post original por aproximadamente 5 minutos, e o mesmo conteúdo/plataforma/conta é rejeitado por hash durante 24 horas com `409`.

## Escolha de interface

| Necessidade | Interface preferida | Por quê |
|---|---|---|
| Rotina reprodutível Hermes | Python SDK `zernio-sdk` | cliente sync/async, env `ZERNIO_API_KEY` |
| Endpoint serverless ou worker | Node SDK `@zernio/node` | tipagem e integração web |
| Diagnóstico e uso humano | CLI `@zernio/cli` | JSON por padrão, 371 comandos documentados |
| Exploração assistida | MCP hospedado `https://mcp.zernio.com/mcp` | descoberta sob demanda de ferramentas |
| Contrato e lacunas de SDK | OpenAPI | schema oficial versionado |

O MCP oferece grande superfície de escrita. A disponibilidade de uma ferramenta não substitui aprovação e verificação desta skill.

## Plataformas e risco

Zernio documenta publicação e comunicação em X, LinkedIn, Instagram, Facebook, Threads, TikTok, YouTube, Bluesky, Pinterest, Reddit, Telegram, Discord, Slack, WhatsApp, Google Business e Snapchat, além de ads. Cada plataforma tem regras de mídia e permissões próprias. Consulte a página oficial específica antes de montar payload de plataforma.
