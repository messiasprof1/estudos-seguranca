from __future__ import annotations

from fastapi.testclient import TestClient

import api.main as api_main
from core.aprovacao import FilaAprovacao
from core.mock_provider import MockProvider


def criar_client_teste(tmp_path):
    api_main.provider = MockProvider()
    api_main.fila = FilaAprovacao(str(tmp_path / "hitl_api_test.db"))
    return TestClient(api_main.app)


def test_health_ok_modo_mock(tmp_path):
    client = criar_client_teste(tmp_path)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["modo"] in {"mock", "real"}


def test_triagem_retorna_intencao_e_status(tmp_path):
    client = criar_client_teste(tmp_path)
    resp = client.post("/triagem", json={"mensagem": "Preciso de ajuda com boleto"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["analise"]["intencao"] == "financeiro"
    assert data["status_roteador"] in {"CONSULTAR_RAG", "RESPONDER_DIRETO", "EXECUTAR_COMANDO", "BLOQUEAR"}


def test_executar_permite_ls_e_bloqueia_rm(tmp_path):
    client = criar_client_teste(tmp_path)

    ok_resp = client.post("/executar", json={"comando": "ls -la"})
    assert ok_resp.status_code == 200
    assert ok_resp.json()["status"] in {"OK", "ERRO"}

    block_resp = client.post("/executar", json={"comando": "rm -rf /"})
    assert block_resp.status_code == 200
    assert block_resp.json()["status"] == "BLOQUEADO"


def test_fluxo_fila_aprovacao(tmp_path):
    client = criar_client_teste(tmp_path)

    item_id = api_main.fila.enfileirar("ls -la", "pedido de teste")

    list_resp = client.get("/fila")
    assert list_resp.status_code == 200
    itens = list_resp.json()["itens"]
    assert any(item["id"] == item_id for item in itens)

    approve_resp = client.post(
        f"/fila/{item_id}/aprovar",
        json={"acao": "aprovado", "aprovado_por": "analista_teste"},
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "aprovado"


def test_consultar_rag_retorna_contexto(tmp_path):
    client = criar_client_teste(tmp_path)
    resp = client.post("/consultar", json={"pergunta": "Como emitir boleto?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["pergunta"] == "Como emitir boleto?"
    assert isinstance(data["contexto"], list)
    assert len(data["contexto"]) >= 1
