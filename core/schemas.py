"""Schemas centrais do projeto usando Pydantic."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class IntencaoEnum(str, Enum):
    FINANCEIRO = "financeiro"
    SUPORTE = "suporte"
    COMERCIAL = "comercial"
    ATAQUE = "ataque"
    AMBIGUO = "ambiguo"


class UrgenciaEnum(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class AnalisePorteiro(BaseModel):
    mensagem_original: str
    mensagem_canonica: str
    intencao: IntencaoEnum
    urgencia: UrgenciaEnum
    tentativa_injecao: bool
    risco: float = Field(ge=0.0, le=1.0)
    justificativa: str


class DecisaoAgente(BaseModel):
    acao: str
    precisa_rag: bool = False
    precisa_tool: bool = False
    comando_sugerido: Optional[str] = None
    mensagem_ao_usuario: str


class ExecucaoComandoResult(BaseModel):
    status: str
    comando: str
    codigo_retorno: int = -1
    saida: str = ""
    erro: str = ""


class DecisaoConfianca(BaseModel):
    margem: float = Field(ge=0.0, le=1.0)
    faixa: str
    justificativa: str
