"""Tools estreitas com validação de caminho."""

from __future__ import annotations

from pathlib import Path


class ErroPermissaoTool(Exception):
    """Erro lançado quando uma tool tenta acessar caminho não permitido."""


def _validar_caminho(caminho: str, prefixo_permitido: str) -> Path:
    base = Path(prefixo_permitido).resolve()
    alvo = Path(caminho).resolve()
    if not str(alvo).startswith(str(base)):
        raise ErroPermissaoTool(f"Acesso negado: {alvo}")
    return alvo


def listar_diretorio(caminho: str, prefixo_permitido: str) -> list[str]:
    alvo = _validar_caminho(caminho, prefixo_permitido)
    if not alvo.is_dir():
        raise FileNotFoundError(f"Diretório não encontrado: {alvo}")
    return sorted([p.name for p in alvo.iterdir()])


def ler_arquivo(caminho: str, prefixo_permitido: str, max_chars: int = 5000) -> str:
    alvo = _validar_caminho(caminho, prefixo_permitido)
    if not alvo.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {alvo}")
    conteudo = alvo.read_text(encoding='utf-8', errors='ignore')
    return conteudo[:max_chars]
