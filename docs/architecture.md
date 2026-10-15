# Arquitetura do Pipeline

```mermaid
flowchart TD
    U[Mensagem do usuário] --> P0[Camada 0: Canonicalização + Regex]
    P0 -->|Ataque explícito| BLQ[Bloquear]
    P0 -->|Passou| P1[Camada 1: Triagem estruturada (Pydantic)]
    P1 --> R[Roteador determinístico]

    R -->|EXECUTAR_COMANDO| C[Confiança: margem de logprobs em chamada separada]
    C -->|autônomo| H[Hook de segurança\nallowlist + shell=False]
    C -->|confirmação/escalar| Q[Fila HITL SQLite]

    R -->|CONSULTAR_RAG| RG[RAG: índice offline + consulta]
    RG --> OUT[Resposta com grounding]

    R -->|RESPONDER_DIRETO| OUT
    H --> OUT
    Q --> OUT
    BLQ --> OUT
```

## Observações

- O Porteiro executa **triagem em chamada única** estruturada.
- A confiança é calculada em **chamada separada** para compatibilidade com logprobs.
- O hook de segurança bloqueia qualquer comando fora da allowlist de tupla completa.
