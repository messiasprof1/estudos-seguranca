from core.aprovacao import FilaAprovacao


def test_fila_hitl_basica(tmp_path):
    db = tmp_path / 'hitl.db'
    fila = FilaAprovacao(str(db))
    item = fila.enfileirar('ls -la', 'teste')
    pendentes = fila.listar('pendente')
    assert len(pendentes) == 1
    assert pendentes[0]['id'] == item

    ok = fila.atualizar_status(item, 'aprovado', aprovado_por='analista')
    assert ok
    todos = fila.listar()
    assert todos[0]['status'] == 'aprovado'
