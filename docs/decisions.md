# ADRs — Decisões de Arquitetura

## ADR-001 — Separar chamada de confiança da chamada estruturada

- **Contexto:** logprobs não são retornados de forma consistente com `response_format` estruturado.
- **Decisão:** usar chamada separada para confiança (margem de logprobs) e manter triagem estruturada dedicada.
- **Consequência:** duas chamadas em fluxos sensíveis, mas comportamento tecnicamente correto.

## ADR-002 — Allowlist de tupla completa em vez de blacklist

- **Contexto:** blacklist é contornável e `shell=True` abre injeção de comando.
- **Decisão:** parse com `shlex`, validação da tupla completa e execução com `shell=False` + env restrito.
- **Consequência:** reduz superfície de ataque; limita comandos permitidos por design.

## ADR-003 — Índice de embeddings offline

- **Contexto:** recalcular embeddings da base por pergunta custa caro e aumenta latência.
- **Decisão:** indexar offline com `np.savez`; na consulta, vetoriza-se apenas a pergunta.
- **Consequência:** latência previsível e custo controlado.

## ADR-004 — Dataset com exatamente 60 mensagens e métricas honestas

- **Contexto:** promessas sem medição reduzem credibilidade do portfólio.
- **Decisão:** manter `dataset.py` com 60 mensagens e geração automática de `resultados.md`/`resultados.csv`.
- **Consequência:** benchmark reproduzível por comando único (`python eval.py`).

## ADR-005 — Camada REST com FastAPI e CORS aberto para demo local

- **Contexto:** era necessário expor o ecossistema para integração externa e validação via HTTP sem quebrar a filosofia de baixo acoplamento.
- **Decisão:** adotar FastAPI + uvicorn com endpoints mínimos (`/health`, `/triagem`, `/executar`, `/consultar`, `/fila`, `/fila/{id}/aprovar`) e CORS liberado para demonstrações locais.
- **Consequência:** integração simples para clientes web/CLI e testes com `TestClient`, mantendo segurança no core (hook allowlist e tools validadas).

## ADR-006 — Servidor MCP via SDK oficial `mcp` (stdio)

- **Contexto:** o projeto precisava expor ferramentas seguras no padrão MCP reutilizando as proteções existentes.
- **Decisão:** usar o SDK oficial Python `mcp` (v2) com `MCPServer` em transporte stdio e tools: `listar_diretorio`, `ler_arquivo`, `executar_comando_seguro` e `triagem_porteiro`.
- **Consequência:** interoperabilidade com hosts MCP modernos e sem dependência de frameworks agênticos pesados; erros de autorização retornam `is_error=true` no protocolo.
