"""Cálculo de custo por tokens de forma configurável."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class ConfigCusto:
    preco_prompt_milhao: float = float(os.getenv('PROMPT_PRECO', '0.15'))
    preco_completion_milhao: float = float(os.getenv('COMPLETION_PRECO', '0.60'))


def estimar_tokens(texto: str) -> int:
    return max(1, int(len(texto.split()) * 1.3))


def calcular_custo(prompt_tokens: int, completion_tokens: int, cfg: ConfigCusto | None = None) -> float:
    conf = cfg or ConfigCusto()
    custo_prompt = (prompt_tokens / 1_000_000.0) * conf.preco_prompt_milhao
    custo_completion = (completion_tokens / 1_000_000.0) * conf.preco_completion_milhao
    return custo_prompt + custo_completion
