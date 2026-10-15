# Porteiro & Ecossistema de IA Agêntica (Zero-Framework)

[![CI](https://github.com/messiasprof1/estudos-seguranca/actions/workflows/ci.yml/badge.svg)](https://github.com/messiasprof1/estudos-seguranca/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)

Repositório técnico em **Python puro** com integração real dos módulos: Porteiro, Roteador, Confiança por margem, HITL persistente, RAG offline, hook seguro e avaliação comparativa.

## Objetivo

Demonstrar arquitetura de IA agêntica com foco em segurança, previsibilidade e avaliação reprodutível.

## Stack

- `openai` (cliente opcional)
- `pydantic`
- `numpy`
- `python-dotenv`
- `fastapi` + `uvicorn`
- `mcp` (SDK oficial para servidor MCP em stdio)
- `pytest`
- `sentence-transformers` (**opcional**, apenas para reranker cross-encoder)

## Estrutura

```text
api/
  main.py
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
mcp_server/
  server.py
  config_exemplos.md
docs/
  architecture.md
  security.md
  decisions.md
  api_usage.md
  mcp.md
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

## 🛰️ API FastAPI (deploy via Docker)

### Subir local com Python

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Acesse:
- Health: `GET http://localhost:8000/health`
- Docs Swagger: `http://localhost:8000/docs`

### Subir com Docker Compose

```bash
docker compose up --build
```

- Porta exposta: `8000`
- Persistência da fila HITL: volume `./data:/app/data`

### Curls rápidos

```bash
curl -s http://localhost:8000/health | jq
```

```bash
curl -s -X POST http://localhost:8000/triagem \
  -H "Content-Type: application/json" \
  -d '{"mensagem":"Preciso de ajuda com boleto"}' | jq
```

```bash
curl -s -X POST http://localhost:8000/executar \
  -H "Content-Type: application/json" \
  -d '{"comando":"ls -la"}' | jq
```

```bash
curl -s -X POST http://localhost:8000/consultar \
  -H "Content-Type: application/json" \
  -d '{"pergunta":"Como emitir boleto?"}' | jq
```

```bash
curl -s http://localhost:8000/fila | jq
```

Documentação detalhada: `docs/api_usage.md`.

## 🔌 Servidor MCP (ferramentas seguras)

Servidor MCP em **stdio** com ferramentas:
- `listar_diretorio`
- `ler_arquivo`
- `executar_comando_seguro`
- `triagem_porteiro`

### Quickstart

```bash
python -m mcp_server.server
```

### Exemplo de registro em host MCP

```json
{
  "mcpServers": {
    "porteiro-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/caminho/para/projeto_ia_agentica"
    }
  }
}
```

Configurações completas: `mcp_server/config_exemplos.md`.

Guia conceitual: `docs/mcp.md`.

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
