---
name: zernio-operations
description: Use when operating Zernio safely with evidence.
version: 1.0.0
author: José Carlos Amorim
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [zernio, social-media, api, publishing, analytics, webhooks]
    related_skills: [social-post-publishing, xurl, linkedin-operations]
---

# Zernio Operations

Use esta skill quando o pedido envolver Zernio, suas contas sociais, posts, analytics, inbox, webhooks, automações ou API. O padrão é descoberta em leitura, aprovação explícita antes de escrita e evidência após alteração.

## Pré-requisitos

- `ZERNIO_API_KEY` existe apenas no ambiente protegido do perfil atual.
- A chave não pode aparecer em shell history, logs, chat, repositório, URL, payload de frontend ou artefato público.
- Base API oficial: `https://zernio.com/api/v1`.
- Leia `references/capability-map.md` e `policies/action-classification.yaml` do repositório antes de operar.

## Procedimento

1. **Classificar o pedido.**
   - Consulta, listagem e analytics são leitura.
   - Publicar, agendar, editar, responder, enviar DM, criar webhook, conectar conta, criar automação, criar ou mudar anúncios e marcar conversas como lidas são escritas externas.
   - Apagar, desconectar, cancelar, despublicar, enviar broadcast e publicar fluxo de WhatsApp são destrutivas ou de alto impacto.

2. **Inventariar primeiro.**
   Rode `scripts/inventory_zernio.py` com `ZERNIO_API_KEY` no ambiente. Ele usa somente `GET` e produz um JSON sanitizado de perfis, contas, posts e webhooks. Não afirme que uma conta está conectada até a resposta da API confirmar.

3. **Resolver escopo antes de qualquer ação.**
   Para um pedido de conteúdo, use o inventário para encontrar perfil, plataforma e conta. Se houver mais de uma opção ou não houver alvo explícito, peça somente a decisão que muda o destino. Não invente `accountId`, `profileId`, handle ou timezone.

4. **Fazer prévia antes de escrita.**
   Para post ou agendamento, mostre conteúdo literal, plataformas e contas alvo, mídia, `publishNow` ou horário com timezone. Para DM, comentário, broadcast ou automação, mostre também destinatário, gatilho e alcance. Exija aprovação explícita do payload final.

5. **Executar com proteção contra duplicação.**
   Para criar post, gere um UUID novo como `x-request-id` para aquela chamada lógica. Em timeout, erro de conexão ou 5xx, retente somente com o mesmo UUID. Em resposta 200 com `existingPost`, trate como replay confirmado. Em 409 de hash de conteúdo, consulte o post existente, não altere nem republique por inferência.

6. **Verificar a mudança.**
   Leia de volta o post, webhook, automação, conta ou recurso alterado. Só declare publicação, agendamento ou alteração com status e ID retornados pela leitura final. Uma resposta de criação isolada não encerra a operação.

7. **Webhooks e inbound.**
   Antes de criar, confirme endpoint, eventos, armazenamento, assinatura, segredo e deduplicação. O receptor deve validar assinatura, limitar payload, registrar o mínimo e responder rápido. Não coloque a chave Zernio no receptor de browser nem conceda a ele capacidade de envio, pagamento ou deleção sem necessidade.

8. **Documentação e ferramentas.**
   - SDK Python: padrão para rotinas determinísticas do Hermes.
   - CLI: diagnóstico local e exploração humana, não base de automação sem guardas.
   - MCP: descoberta assistida e tarefas pontuais, sempre com a política desta skill acima do catálogo de ferramentas.
   - SDK Node.js: receptor HTTP, worker e aplicações serverless.
   - OpenAPI: referência contratual para endpoints e schemas.

## Falhas e limites

- `401`/`403`: informe acesso insuficiente e pare.
- `429`: respeite `Retry-After`; não tente contornar limitação com paralelismo.
- OAuth pendente: aguarde a autorização e releia o estado.
- Mídia: use o fluxo oficial de upload e valide a URL ou estado antes de criar o post.
- APIs com alto impacto, como WhatsApp, telefonia, ads e automações, nunca têm aprovação implícita por uma instrução genérica de “operar Zernio”.
- Nunca exponha `ZERNIO_API_KEY`, segredo de assinatura, estado OAuth, URL privada de webhook ou listas de destinatários.

## Verificação

O resultado precisa registrar sistema, recurso, status e identificador, sem expor segredo. Exemplo: `Zernio, post <id>, SCHEDULED, relido em GET /posts/<id>`.
