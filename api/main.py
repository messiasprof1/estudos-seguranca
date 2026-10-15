"""API FastAPI para expor o ecossistema de IA agêntica com segurança defensiva."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.aprovacao import FilaAprovacao
from core.cliente_llm import ClienteLLM, criar_provider
from core.hook_seguranca import interceptar_e_executar
from core.porteiro import triagem_porteiro
from core.rag import consultar, garantir_indice_padrao
from core.roteador import roteador_fluxo

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "hitl.db"
INDICE_PATH = DATA_DIR / "indice_rag.npz"
BASE_PATH = DATA_DIR / "base_conhecimento.txt"

provider = criar_provider()
fila = FilaAprovacao(str(DB_PATH))

app = FastAPI(
    title="Porteiro API",
    description="Camada REST com triagem, execução segura, consulta RAG e HITL.",
    version="1.0.0",
)

# CORS liberado para demos locais.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MensagemRequest(BaseModel):
    mensagem: str = Field(min_length=0)


class ComandoRequest(BaseModel):
    comando: str


class ConsultaRequest(BaseModel):
    pergunta: str


class AtualizarFilaRequest(BaseModel):
    acao: str = Field(description="Valores aceitos: aprovado ou rejeitado")
    aprovado_por: str


@app.get("/health")
def health() -> dict:
    modo = "mock" if ClienteLLM().usa_mock else "real"
    return {"status": "ok", "modo": modo}


@app.post("/triagem")
def triagem(payload: MensagemRequest) -> dict:
    analise = triagem_porteiro(payload.mensagem, provider)
    decisao = roteador_fluxo(analise)
    return {
        "analise": analise.model_dump(mode="json"),
        "decisao": decisao.model_dump(mode="json"),
        "status_roteador": decisao.acao,
    }


@app.post("/executar")
def executar(payload: ComandoRequest) -> dict:
    resultado = interceptar_e_executar(payload.comando, diretorio_trabalho=str(ROOT_DIR))
    return resultado.model_dump(mode="json")


@app.post("/consultar")
def consultar_rag(payload: ConsultaRequest) -> dict:
    if not BASE_PATH.exists():
        raise HTTPException(
            status_code=400,
            detail="Base de conhecimento não encontrada em data/base_conhecimento.txt.",
        )

    garantir_indice_padrao(str(INDICE_PATH), str(BASE_PATH))
    contexto = consultar(payload.pergunta, str(INDICE_PATH), top_k=5, usar_reranker=False, top_n_rerank=3)

    resposta = "Resposta orientada por contexto local (modo mock)."
    return {
        "pergunta": payload.pergunta,
        "resposta": resposta,
        "contexto": contexto,
    }


@app.get("/fila")
def listar_fila() -> dict:
    itens = fila.listar(status="pendente")
    return {"total": len(itens), "itens": itens}


@app.post("/fila/{item_id}/aprovar")
def aprovar_rejeitar_item(item_id: int, payload: AtualizarFilaRequest) -> dict:
    acao = payload.acao.lower().strip()
    if acao not in {"aprovado", "rejeitado"}:
        raise HTTPException(status_code=400, detail="Ação inválida. Use 'aprovado' ou 'rejeitado'.")

    atualizado = fila.atualizar_status(item_id, acao, aprovado_por=payload.aprovado_por)
    if not atualizado:
        raise HTTPException(status_code=404, detail=f"Item {item_id} não encontrado na fila HITL.")

    return {
        "ok": True,
        "id": item_id,
        "status": acao,
        "aprovado_por": payload.aprovado_por,
    }
