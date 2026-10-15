from core.confianca import avaliar_confianca_separada, classificar_faixa
from core.mock_provider import MockProvider


def test_faixas_confianca():
    assert classificar_faixa(0.8) == 'autonomo'
    assert classificar_faixa(0.4) == 'confirmacao'
    assert classificar_faixa(0.1) == 'escalar'


def test_avaliacao_mock():
    dec = avaliar_confianca_separada('executar comando: ls', MockProvider())
    assert 0 <= dec.margem <= 1
    assert dec.faixa in {'autonomo', 'confirmacao', 'escalar'}
