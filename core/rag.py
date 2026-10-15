"""RAG com indexação offline e reranker opcional."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

try:
    from sentence_transformers import CrossEncoder  # type: ignore
except Exception:  # pragma: no cover - opcional
    CrossEncoder = None


def _vetorizar_texto(texto: str, dimensao: int = 128) -> np.ndarray:
    vetor = np.zeros(dimensao, dtype=np.float32)
    for i, b in enumerate(texto.encode('utf-8', errors='ignore')):
        vetor[i % dimensao] += float((b % 31) + 1)
    norma = np.linalg.norm(vetor)
    if norma > 0:
        vetor /= norma
    return vetor


def indexar_offline(documentos: list[str], caminho_indice: str) -> None:
    vetores = np.vstack([_vetorizar_texto(doc) for doc in documentos])
    np.savez(caminho_indice, vetores=vetores, documentos=np.array(documentos, dtype=object))


def _similaridade(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


def consultar(
    pergunta: str,
    caminho_indice: str,
    top_k: int = 5,
    usar_reranker: bool = False,
    top_n_rerank: int = 3,
) -> list[dict[str, Any]]:
    dados = np.load(caminho_indice, allow_pickle=True)
    vetores = dados['vetores']
    documentos = dados['documentos'].tolist()

    v_pergunta = _vetorizar_texto(pergunta)
    scores = [(_similaridade(v_pergunta, v), i) for i, v in enumerate(vetores)]
    scores.sort(reverse=True, key=lambda x: x[0])
    candidatos = [
        {'documento': documentos[i], 'score': float(s)}
        for s, i in scores[:top_k]
    ]

    if usar_reranker and CrossEncoder is not None and candidatos:
        modelo = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        pares = [(pergunta, c['documento']) for c in candidatos]
        rr_scores = modelo.predict(pares)
        rerank = list(zip(rr_scores, candidatos))
        rerank.sort(reverse=True, key=lambda x: float(x[0]))
        saida = []
        for score, cand in rerank[:top_n_rerank]:
            saida.append({'documento': cand['documento'], 'score': float(cand['score']), 'rerank_score': float(score)})
        return saida

    return candidatos[:top_n_rerank]


def garantir_indice_padrao(caminho_indice: str, caminho_base: str) -> None:
    p_indice = Path(caminho_indice)
    if p_indice.exists():
        return
    docs = []
    for linha in Path(caminho_base).read_text(encoding='utf-8').splitlines():
        linha = linha.strip()
        if linha:
            docs.append(linha)
    indexar_offline(docs, caminho_indice)
