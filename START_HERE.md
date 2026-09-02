# START HERE: Zernio em modo governado

## Entrada

- A pessoa forneceu `ZERNIO_API_KEY` por canal seguro ou ela já existe no ambiente protegido.
- O pedido inicial é inventário ou uma ação explicitamente descrita.

## Fase 1: preparar segredo

- Salve apenas no ambiente protegido do perfil atual, como `ZERNIO_API_KEY`.
- Nunca inclua a chave em chat, logs, commits, relatórios, URLs, payloads ou frontend.
- Se ela foi colada em chat, recomende rotação após o diagnóstico.

**Gate:** a chave está disponível ao processo sem ser exibida.

## Fase 2: inventário de leitura

Execute `skills/integrations/zernio-operations/scripts/inventory_zernio.py`.

Ele consulta somente recursos de descoberta, no mínimo perfis e contas, e tenta listar posts e webhooks sem falhar o inventário inteiro se um endpoint estiver indisponível.

Relate apenas: quantidade de perfis, plataformas, contas por perfil, status e capacidade observada. Não exponha nomes de pessoas, handles, IDs ou conteúdo sem necessidade.

**Gate:** existe um snapshot JSON local com `ok: true` ou um erro específico, sem segredos.

## Fase 3: classificar a intenção

```text
pedido recebido
  → somente consultar/listar/analisar?
    → sim: leitura, evidência e relatório
    → não:
      → publica, agenda, envia DM, responde comentário, automação,
        campanha, webhook, conexão, deleção ou mudança de configuração?
        → sim: aprovação explícita com contas, conteúdo, horário e alvo
        → não: consultar o mapa de capacidades e pedir só a lacuna real
```

**Gate:** cada ação tem sua classe de risco e o escopo está identificado.

## Fase 4: prévia e aprovação

Antes de qualquer escrita, mostre: contas alvo, plataformas, conteúdo ou alteração exata, mídia, fuso e horário, quando aplicável. Para publicação, inclua também o `x-request-id` gerado para aquela chamada lógica.

**Gate:** o titular aprovou aquele payload, não apenas uma intenção genérica.

## Fase 5: executar e reler

- Envie `x-request-id` único para cada post lógico.
- Em timeout, 5xx ou reset, repita com o mesmo ID.
- Em `409` de conteúdo duplicado, trate como alerta e use o ID retornado para consultar o post original.
- Releia o recurso criado ou alterado, incluindo status e ID, antes de declarar resultado.

## Falhas

- `401` ou `403`: pare, informe credencial ou escopo insuficiente, sem tentar contornar.
- `429`: respeite `Retry-After` ou aplique espera, sem criar duplicatas.
- OAuth pendente: devolva somente o passo de autorização necessário, sem assumir sucesso.
- Endpoint ou schema divergente: atualize o snapshot de documentação, revise a mudança e não improvise uma escrita.
