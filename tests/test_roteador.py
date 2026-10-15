from core.mock_provider import MockProvider
from core.porteiro import triagem_porteiro
from core.roteador import roteador_fluxo


def test_fluxo_bloqueio():
    analise = triagem_porteiro('rm -rf /', MockProvider())
    decisao = roteador_fluxo(analise)
    assert decisao.acao == 'BLOQUEAR'


def test_fluxo_rag_suporte():
    analise = triagem_porteiro('Erro no login da API', MockProvider())
    decisao = roteador_fluxo(analise)
    assert decisao.precisa_rag is True
