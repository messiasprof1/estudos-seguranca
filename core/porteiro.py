"""Porteiro em duas camadas: regex + triagem estruturada."""

from __future__ import annotations

import re
import unicodedata

from core.schemas import AnalisePorteiro, IntencaoEnum, UrgenciaEnum

PADROES_ATAQUE = [
    re.compile(r"ignore\s+as\s+instru", re.IGNORECASE),
    re.compile(r"system\s*prompt", re.IGNORECASE),
    re.compile(r"\brm\s+-rf\b", re.IGNORECASE),
    re.compile(r"\bsudo\b", re.IGNORECASE),
    re.compile(r"\b(base64|b64)\b", re.IGNORECASE),
]


def canonicalizar_texto(mensagem: str) -> str:
    texto = unicodedata.normalize("NFKC", mensagem or "")
    texto = texto.lower().strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def triagem_regex(mensagem_canonica: str) -> tuple[bool, str]:
    for padrao in PADROES_ATAQUE:
        if padrao.search(mensagem_canonica):
            return True, f"Padrão detectado: {padrao.pattern}"
    return False, "Sem padrão crítico por regex."


def triagem_porteiro(mensagem: str, provider) -> AnalisePorteiro:
    canonica = canonicalizar_texto(mensagem)

    if not canonica:
        return AnalisePorteiro(
            mensagem_original=mensagem,
            mensagem_canonica=canonica,
            intencao=IntencaoEnum.AMBIGUO,
            urgencia=UrgenciaEnum.BAIXA,
            tentativa_injecao=False,
            risco=0.1,
            justificativa="Mensagem vazia após normalização.",
        )

    injecao_regex, justificativa_regex = triagem_regex(canonica)
    if injecao_regex:
        return AnalisePorteiro(
            mensagem_original=mensagem,
            mensagem_canonica=canonica,
            intencao=IntencaoEnum.ATAQUE,
            urgencia=UrgenciaEnum.ALTA,
            tentativa_injecao=True,
            risco=0.99,
            justificativa=justificativa_regex,
        )

    analise = provider.analisar_triagem(canonica)
    return AnalisePorteiro(
        mensagem_original=mensagem,
        mensagem_canonica=canonica,
        intencao=analise["intencao"],
        urgencia=analise["urgencia"],
        tentativa_injecao=analise["tentativa_injecao"],
        risco=analise["risco"],
        justificativa=analise["justificativa"],
    )
