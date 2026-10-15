# Segurança — Matriz OWASP LLM Top 10 (2025)

## Matriz de mitigação

| Risco OWASP | Mitigação no projeto | Onde está implementado |
|---|---|---|
| LLM01 Prompt Injection | Regex de borda + triagem estruturada + canonicalização unicode | `core/porteiro.py` |
| LLM05 Improper Output Handling | Execução controlada por hook com allowlist estrita e `shell=False` | `core/hook_seguranca.py` |
| LLM06 Excessive Agency | Roteador determinístico + HITL para casos sensíveis | `core/roteador.py`, `core/aprovacao.py` |
| LLM07 System Prompt Leakage | Bloqueio de padrões explícitos de exfiltração no porteiro | `core/porteiro.py` |
| LLM08 Vector/Embedding Weaknesses | RAG com índice offline e opção de reranker; base local controlada | `core/rag.py` |
| LLM10 Unbounded Consumption | Avaliação de custo por intenção e thresholds de autonomia | `core/custo.py`, `eval.py`, `core/confianca.py` |

## Princípios aplicados

1. Defesa em profundidade (camadas independentes).
2. Menor privilégio (tools estreitas e validação de caminho).
3. Controle explícito de fluxo (máquina de estados determinística).
4. Auditoria de decisões (fila HITL persistida em SQLite).
