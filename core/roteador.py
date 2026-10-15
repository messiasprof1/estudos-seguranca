"""Roteador determinístico (máquina de estados) do ecossistema."""

from __future__ import annotations

from core.schemas import AnalisePorteiro, DecisaoAgente, IntencaoEnum


def roteador_fluxo(analise: AnalisePorteiro) -> DecisaoAgente:
    if analise.tentativa_injecao:
        return DecisaoAgente(
            acao="BLOQUEAR",
            precisa_rag=False,
            precisa_tool=False,
            mensagem_ao_usuario="Solicitação bloqueada por política de segurança.",
        )

    canonica = analise.mensagem_canonica
    if "comando:" in canonica or "listar diretório" in canonica or "listar diretorio" in canonica:
        comando = canonica.split("comando:", 1)[-1].strip() if "comando:" in canonica else "ls"
        return DecisaoAgente(
            acao="EXECUTAR_COMANDO",
            precisa_tool=True,
            comando_sugerido=comando,
            mensagem_ao_usuario="Pedido envolve ação de sistema e será validado.",
        )

    if analise.intencao == IntencaoEnum.FINANCEIRO:
        return DecisaoAgente(
            acao="CONSULTAR_RAG",
            precisa_rag=True,
            mensagem_ao_usuario="Vou consultar a base financeira para responder com precisão.",
        )

    if analise.intencao == IntencaoEnum.SUPORTE:
        return DecisaoAgente(
            acao="CONSULTAR_RAG",
            precisa_rag=True,
            mensagem_ao_usuario="Vou consultar a base de suporte para te orientar.",
        )

    if analise.intencao == IntencaoEnum.COMERCIAL:
        return DecisaoAgente(
            acao="RESPONDER_DIRETO",
            mensagem_ao_usuario="Posso te passar os próximos passos comerciais.",
        )

    return DecisaoAgente(
        acao="ESCALAR_HUMANO",
        mensagem_ao_usuario="Caso ambíguo: encaminhando para validação humana.",
    )
