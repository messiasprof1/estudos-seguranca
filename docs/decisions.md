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
