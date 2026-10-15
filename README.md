# Porteiro & Ecossistema de IA Agêntica (Zero-Framework)

Repositório técnico em **Python puro** com integração real dos módulos: Porteiro, Roteador, Confiança por margem, HITL persistente, RAG offline, hook seguro e avaliação comparativa.

## Objetivo

Demonstrar arquitetura de IA agêntica com foco em segurança, previsibilidade e avaliação reprodutível.

## Stack

- `openai` (cliente opcional)
- `pydantic`
- `numpy`
- `python-dotenv`
- `pytest`
- `sentence-transformers` (**opcional**, apenas para reranker cross-encoder)

## Estrutura

```text
core/
  porteiro.py
  roteador.py
  confianca.py
  aprovacao.py
  rag.py
  tools.py
  hook_seguranca.py
  cliente_llm.py
  mock_provider.py
  custo.py
docs/
  architecture.md
  security.md
  decisions.md
tests/
  ...
dataset.py
eval.py
main.py
```

## Correções técnicas aplicadas (Parte 1 do estudo)

1. **Confiança por margem de logprobs** (sinal, não probabilidade calibrada).
2. **Chamada separada de confiança** (logprobs fora de structured outputs).
3. **Hook seguro com allowlist de tupla completa + `shell=False`**.
4. **RAG com indexação offline** e reranker real opcional (`CrossEncoder`).
5. **Cliente HTTP com base_url configurável, timeout/retry e streaming/TTFT**.
6. **Sem nomenclatura incorreta de servidor de inferência** (suporta OpenAI-compatível).
7. **Dataset com exatamente 60 mensagens rotuladas**.
8. **README com métricas reproduzíveis** via `python eval.py`.

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest -q
python eval.py
python main.py
```

> Por padrão, o projeto roda em **modo mock determinístico** quando não há chave (`MODO_MOCK=auto` sem `OPENAI_API_KEY`).

## Métricas

As métricas são geradas por `python eval.py` em:
- `resultados.md`
- `resultados.csv`

Esses arquivos comparam:
- Porteiro (regex + triagem estruturada)
- LLM puro
- Regex puro

Incluem:
- Acurácia global
- F1 (macro e por classe)
- Matriz de confusão
- Latência p50/p95
- Custo por intenção

## Segurança

Veja `docs/security.md` com matriz de mitigação OWASP LLM Top 10 (2025).

## Arquitetura

Veja `docs/architecture.md` com diagrama Mermaid do pipeline.

## Decisões (ADRs)

Veja `docs/decisions.md` para decisões de arquitetura e trade-offs.
