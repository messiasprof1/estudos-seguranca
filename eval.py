"""Harness de avaliação: Porteiro vs LLM puro vs regex puro."""

from __future__ import annotations

import csv
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from core.cliente_llm import criar_provider
from core.custo import calcular_custo, estimar_tokens
from core.porteiro import canonicalizar_texto, triagem_porteiro, triagem_regex
from dataset import obter_dataset

CLASSES = ['financeiro', 'suporte', 'comercial', 'ataque', 'ambiguo']


def baseline_regex_puro(mensagem: str) -> str:
    canonica = canonicalizar_texto(mensagem)
    eh_ataque, _ = triagem_regex(canonica)
    if eh_ataque:
        return 'ataque'
    if any(k in canonica for k in ['boleto', 'pix', 'fatura', 'reembolso', 'nota fiscal']):
        return 'financeiro'
    if any(k in canonica for k in ['erro', 'senha', 'login', 'api', 'suporte']):
        return 'suporte'
    if any(k in canonica for k in ['plano', 'proposta', 'demo', 'vendas', 'comercial', 'contrato']):
        return 'comercial'
    return 'ambiguo'


def matriz_confusao(y_true: list[str], y_pred: list[str]) -> dict[str, dict[str, int]]:
    matriz = {c: {c2: 0 for c2 in CLASSES} for c in CLASSES}
    for t, p in zip(y_true, y_pred):
        matriz[t][p] += 1
    return matriz


def metricas_por_classe(y_true: list[str], y_pred: list[str]) -> dict[str, dict[str, float]]:
    mtx = matriz_confusao(y_true, y_pred)
    saida = {}
    for classe in CLASSES:
        tp = mtx[classe][classe]
        fp = sum(mtx[c][classe] for c in CLASSES if c != classe)
        fn = sum(mtx[classe][c] for c in CLASSES if c != classe)
        precisao = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precisao * recall / (precisao + recall)) if (precisao + recall) else 0.0
        saida[classe] = {'precisao': precisao, 'recall': recall, 'f1': f1}
    return saida


def avaliar_sistema(nome: str, dataset: list[dict[str, str]], provider) -> dict[str, Any]:
    y_true, y_pred = [], []
    latencias, custos = [], []
    custo_por_intent = defaultdict(list)

    for item in dataset:
        msg, real = item['mensagem'], item['rotulo']
        ini = time.perf_counter()
        if nome == 'porteiro':
            pred = triagem_porteiro(msg, provider).intencao.value
        elif nome == 'llm_puro':
            pred = provider.classificar_llm_puro(msg)
        else:
            pred = baseline_regex_puro(msg)
        lat = time.perf_counter() - ini

        prompt_tokens = estimar_tokens(msg)
        completion_tokens = 12
        custo = calcular_custo(prompt_tokens, completion_tokens)

        y_true.append(real)
        y_pred.append(pred)
        latencias.append(lat)
        custos.append(custo)
        custo_por_intent[pred].append(custo)

    acertos = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    acc = acertos / len(dataset)
    por_classe = metricas_por_classe(y_true, y_pred)
    macro_f1 = statistics.mean(v['f1'] for v in por_classe.values())
    mtx = matriz_confusao(y_true, y_pred)

    lat_ordenada = sorted(latencias)
    p50 = lat_ordenada[int(0.5 * (len(lat_ordenada) - 1))]
    p95 = lat_ordenada[int(0.95 * (len(lat_ordenada) - 1))]

    custo_intent_media = {k: sum(v) / len(v) for k, v in custo_por_intent.items()}

    return {
        'nome': nome,
        'acuracia': acc,
        'macro_f1': macro_f1,
        'por_classe': por_classe,
        'matriz_confusao': mtx,
        'latencia_p50': p50,
        'latencia_p95': p95,
        'custo_medio': sum(custos) / len(custos),
        'custo_por_intent': custo_intent_media,
    }


def salvar_resultados_csv(resultados: list[dict[str, Any]], caminho_csv: str) -> None:
    campos = ['sistema', 'acuracia', 'macro_f1', 'latencia_p50', 'latencia_p95', 'custo_medio']
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for r in resultados:
            w.writerow(
                {
                    'sistema': r['nome'],
                    'acuracia': f"{r['acuracia']:.4f}",
                    'macro_f1': f"{r['macro_f1']:.4f}",
                    'latencia_p50': f"{r['latencia_p50']*1000:.3f}",
                    'latencia_p95': f"{r['latencia_p95']*1000:.3f}",
                    'custo_medio': f"{r['custo_medio']:.8f}",
                }
            )


def salvar_resultados_md(resultados: list[dict[str, Any]], caminho_md: str, dataset: list[dict[str, str]]) -> None:
    dist = Counter(item['rotulo'] for item in dataset)

    linhas = [
        '# Resultados de Avaliação (Modo Mock)',
        '',
        '## Configuração',
        '- Execução em modo mock determinístico (sem chave de API).',
        f"- Total de mensagens: {len(dataset)}",
        f"- Distribuição: {dict(dist)}",
        '',
        '## Comparação entre estratégias',
        '| Sistema | Acurácia | Macro F1 | Latência p50 (ms) | Latência p95 (ms) | Custo médio (USD/chamada) |',
        '|---|---:|---:|---:|---:|---:|',
    ]

    for r in resultados:
        linhas.append(
            f"| {r['nome']} | {r['acuracia']:.4f} | {r['macro_f1']:.4f} | {r['latencia_p50']*1000:.3f} | {r['latencia_p95']*1000:.3f} | {r['custo_medio']:.8f} |"
        )

    import json
    for r in resultados:
        linhas.append('')
        linhas.append(f"## Detalhes — {r['nome']}")
        linhas.append('### F1 por classe')
        for classe, m in r['por_classe'].items():
            linhas.append(f"- {classe}: precisão={m['precisao']:.3f}, recall={m['recall']:.3f}, f1={m['f1']:.3f}")
        linhas.append('### Custo médio por intenção prevista')
        for intent, custo in sorted(r['custo_por_intent'].items()):
            linhas.append(f"- {intent}: USD {custo:.8f}")
        linhas.append('### Matriz de confusão (real x previsto)')
        linhas.append('```json')
        linhas.append(json.dumps(r['matriz_confusao'], ensure_ascii=False, indent=2))
        linhas.append('```')

    Path(caminho_md).write_text('\n'.join(linhas), encoding='utf-8')


def main() -> None:
    dataset = obter_dataset()
    provider = criar_provider()

    resultados = [
        avaliar_sistema('porteiro', dataset, provider),
        avaliar_sistema('llm_puro', dataset, provider),
        avaliar_sistema('regex_puro', dataset, provider),
    ]

    salvar_resultados_csv(resultados, 'resultados.csv')
    salvar_resultados_md(resultados, 'resultados.md', dataset)
    print('Avaliação concluída. Arquivos: resultados.csv e resultados.md')


if __name__ == '__main__':
    main()
