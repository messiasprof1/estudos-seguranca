"""Provider mock determinístico para execução sem chave de API."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from core.schemas import IntencaoEnum, UrgenciaEnum


@dataclass
class MockProvider:
    """Simula respostas de classificação/triagem/confianca de forma determinística."""

    nome_modelo: str = "mock-gpt"

    def _hash01(self, texto: str) -> float:
        h = hashlib.sha256(texto.encode("utf-8")).hexdigest()
        return int(h[:8], 16) / 0xFFFFFFFF

    def analisar_triagem(self, mensagem: str) -> dict:
        msg = mensagem.lower()
        if any(k in msg for k in ["boleto", "pix", "fatura", "pagamento", "nota fiscal", "reembolso"]):
            intencao = IntencaoEnum.FINANCEIRO
        elif any(k in msg for k in ["erro", "bug", "senha", "login", "acesso", "suporte", "api"]):
            intencao = IntencaoEnum.SUPORTE
        elif any(k in msg for k in ["preço", "preco", "plano", "proposta", "contratar", "demo", "comercial"]):
            intencao = IntencaoEnum.COMERCIAL
        elif any(k in msg for k in ["ignore", "system prompt", "desative", "rm -rf", "sudo", "bypass"]):
            intencao = IntencaoEnum.ATAQUE
        else:
            intencao = IntencaoEnum.AMBIGUO

        if any(k in msg for k in ["urgente", "hoje", "agora", "imediato", "travou"]):
            urgencia = UrgenciaEnum.ALTA
        elif any(k in msg for k in ["quando puder", "sem pressa", "depois"]):
            urgencia = UrgenciaEnum.BAIXA
        else:
            urgencia = UrgenciaEnum.MEDIA

        tentativa = intencao == IntencaoEnum.ATAQUE
        risco = 0.9 if tentativa else 0.2 + self._hash01(msg) * 0.4
        return {
            "intencao": intencao,
            "urgencia": urgencia,
            "tentativa_injecao": tentativa,
            "risco": round(min(risco, 1.0), 3),
            "justificativa": "Classificação mock determinística.",
        }

    def avaliar_confianca(self, mensagem: str) -> dict:
        msg = mensagem.lower()
        if any(k in msg for k in ["talvez", "acho", "não sei", "nao sei", "duvida"]):
            margem = 0.22
        elif any(k in msg for k in ["executar", "comando:", "reiniciar", "deletar", "apagar"]):
            margem = 0.52
        else:
            margem = 0.78
        return {
            "margem": margem,
            "justificativa": "Margem simulada a partir de chamada separada de confiança.",
        }

    def classificar_llm_puro(self, mensagem: str) -> str:
        """Baseline LLM puro para avaliação comparativa (ainda mock)."""
        return self.analisar_triagem(mensagem)["intencao"].value
