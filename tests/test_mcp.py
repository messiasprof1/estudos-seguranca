from __future__ import annotations

import asyncio
import os
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

PROJECT_ROOT = Path(__file__).resolve().parent.parent


async def _rodar_fluxo_mcp() -> None:
    params = StdioServerParameters(
        command="python3",
        args=["-m", "mcp_server.server"],
        cwd=str(PROJECT_ROOT),
        env={**os.environ, "MCP_PREFIXO_PERMITIDO": str(PROJECT_ROOT)},
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            assert init is not None

            ferramentas = await session.list_tools()
            nomes = {tool.name for tool in ferramentas.tools}
            assert {
                "listar_diretorio",
                "ler_arquivo",
                "executar_comando_seguro",
                "triagem_porteiro",
            }.issubset(nomes)

            ok = await session.call_tool("ler_arquivo", {"caminho": "data/base_conhecimento.txt"})
            assert ok.is_error is False
            texto_ok = "\n".join(getattr(parte, "text", "") for parte in ok.content)
            assert "base_conhecimento" in texto_ok

            negado = await session.call_tool("ler_arquivo", {"caminho": "/etc/passwd"})
            assert negado.is_error is True
            texto_erro = "\n".join(getattr(parte, "text", "") for parte in negado.content)
            assert "Falha em ler_arquivo" in texto_erro


def test_mcp_handshake_list_e_call() -> None:
    asyncio.run(_rodar_fluxo_mcp())
