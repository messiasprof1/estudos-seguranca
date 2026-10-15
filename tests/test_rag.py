from core.rag import consultar, indexar_offline


def test_rag_indexa_e_consulta(tmp_path):
    docs = ['boleto e pagamentos', 'erro 500 no login', 'plano enterprise com SLA']
    indice = tmp_path / 'idx.npz'
    indexar_offline(docs, str(indice))
    out = consultar('tenho erro de login', str(indice), top_k=2, usar_reranker=False, top_n_rerank=2)
    assert len(out) == 2
    assert isinstance(out[0]['score'], float)
