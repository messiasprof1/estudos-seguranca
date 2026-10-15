"""Módulo de confiança via margem de logprobs em chamada separada."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from core.schemas import DecisaoConfianca

load_dotenv()

THRESHOLD_AUTONOMO = float(os.getenv("THRESHOLD_AUTONOMO", "0.60"))
THRESHOLD_CONFIRMACAO = float(os.getenv("THRESHOLD_CONFIRMACAO", "0.30"))


def classificar_faixa(margem: float) -> str:
    if margem >= THRESHOLD_AUTONOMO:
        return "autonomo"
    if margem >= THRESHOLD_CONFIRMACAO:
        return "confirmacao"
    return "escalar"


def avaliar_confianca_separada(mensagem: str, provider) -> DecisaoConfianca:
    """Usa uma chamada separada (sem structured output) para obter sinal de confiança."""
    resultado = provider.avaliar_confianca(mensagem)
    margem = float(resultado["margem"])
    return DecisaoConfianca(
        margem=margem,
        faixa=classificar_faixa(margem),
        justificativa=resultado["justificativa"],
    )
