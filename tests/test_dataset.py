from dataset import obter_dataset, resumo_distribuicao


def test_dataset_tem_60_itens_exatos():
    ds = obter_dataset()
    assert len(ds) == 60


def test_distribuicao_realista():
    dist = resumo_distribuicao()
    total = sum(dist.values())
    assert total == 60
    assert dist['financeiro'] == 24
    assert dist['suporte'] == 15
    assert dist['comercial'] == 9
    assert dist['ataque'] == 7
    assert dist['ambiguo'] == 5
