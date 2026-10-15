from core.hook_seguranca import interceptar_e_executar


def test_bloqueia_injecao_ponto_virgula(tmp_path):
    r = interceptar_e_executar('ls; rm -rf /', str(tmp_path))
    assert r.status == 'BLOQUEADO'


def test_bloqueia_binario_absoluto_rm(tmp_path):
    r = interceptar_e_executar('/bin/rm -rf x', str(tmp_path))
    assert r.status == 'BLOQUEADO'


def test_permite_comando_allowlist(tmp_path):
    r = interceptar_e_executar('pwd', str(tmp_path))
    assert r.status in {'OK', 'ERRO'}
