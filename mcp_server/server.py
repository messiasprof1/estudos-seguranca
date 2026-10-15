"""Servidor MCP em stdio expondo ferramentas seguras do projeto."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from core.cliente_llm import criar_provider
from core.hook_seguranca import interceptar_e_executar
from core.porteiro import triagem_porteiro
from core.tools import ErroPermissaoTool, ler_arquivo, listar_diretorio

ROOT_DIR = Path(__file__).resolve().parent.parent
PREFIXO_PERMITIDO = Path(os.getenv("MCP_PREFIXO_PERMITIDO", str(ROOT_DIR))).resolve()

provider = criar_provider()
server = MCPServer(
    name="porteiro-mcp",
    title="Porteiro MCP",
    description="Servidor MCP com ferramentas seguras de arquivos, comandos e triagem.",
    version="1.0.0",
)


def _normalizar_caminho(caminho: str) -> str:
    alvo = Path(caminho)
    if not alvo.is_absolute():
        alvo = PREFIXO_PERMITIDO / alvo
    return str(alvo)


@server.tool(
    name="listar_diretorio",
    description=(
        "Lista arquivos de um diretório permitido. "
        "Args JSON: {\"caminho\":\".\"}."
    ),
)
def tool_listar_diretorio(caminho: str = ".") -> dict[str, Any]:
    try:
        caminho_resolvido = _normalizar_caminho(caminho)
        itens = listar_diretorio(caminho_resolvido, str(PREFIXO_PERMITIDO))
        return {
            "prefixo_permitido": str(PREFIXO_PERMITIDO),
            "caminho": caminho_resolvido,
            "itens": itens,
            "total": len(itens),
        }
    except (ErroPermissaoTool, FileNotFoundError) as exc:
        raise ToolError(f"Falha em listar_diretorio: {exc}") from exc


@server.tool(
    name="ler_arquivo",
    description=(
        "Lê conteúdo de arquivo dentro do prefixo permitido. "
        "Args JSON: {\"caminho\":\"data/base_conhecimento.txt\",\"max_chars\":2000}."
    ),
)
def tool_ler_arquivo(caminho: str, max_chars: int = 5000) -> dict[str, Any]:
    try:
        caminho_resolvido = _normalizar_caminho(caminho)
        conteudo = ler_arquivo(caminho_resolvido, str(PREFIXO_PERMITIDO), max_chars=max_chars)
        return {
            "prefixo_permitido": str(PREFIXO_PERMITIDO),
            "caminho": caminho_resolvido,
            "conteudo": conteudo,
            "chars": len(conteudo),
        }
    except (ErroPermissaoTool, FileNotFoundError) as exc:
        raise ToolError(f"Falha em ler_arquivo: {exc}") from exc


@server.tool(
    name="executar_comando_seguro",
    description=(
        "Executa comando de shell estritamente permitido pela allowlist do hook. "
        "Args JSON: {\"comando\":\"ls -la\"}."
    ),
)
def tool_executar_comando_seguro(comando: str) -> dict[str, Any]:
    resultado = interceptar_e_executar(comando, diretorio_trabalho=str(PREFIXO_PERMITIDO))
    return resultado.model_dump(mode="json")


@server.tool(
    name="triagem_porteiro",
    description=(
        "Executa triagem de segurança/intenção do porteiro. "
        "Args JSON: {\"mensagem\":\"texto do usuário\"}."
    ),
)
def tool_triagem_porteiro(mensagem: str) -> dict[str, Any]:
    analise = triagem_porteiro(mensagem, provider)
    return {
        "is_prompt_injection": analise.tentativa_injecao,
        "intencao": analise.intencao.value,
        "urgencia": analise.urgencia.value,
        "resposta_limpa": analise.mensagem_canonica,
        "justificativa_seguranca": analise.justificativa,
        "risco": analise.risco,
    }


async def _run() -> None:
    await server.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(_run())
