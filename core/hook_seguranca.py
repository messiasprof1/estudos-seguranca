"""Hook de segurança para execução de comandos com allowlist estrita."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from core.schemas import ExecucaoComandoResult

ALLOWLIST_TUPLAS = {
    ('ls',),
    ('ls', '-la'),
    ('ls', '-l'),
    ('pwd',),
    ('date',),
    ('uptime',),
}


def interceptar_e_executar(comando_bruto: str, diretorio_trabalho: str) -> ExecucaoComandoResult:
    try:
        args = shlex.split(comando_bruto)
    except ValueError:
        return ExecucaoComandoResult(
            status='INVALIDO',
            comando=comando_bruto,
            erro='Comando malformado para parser shlex.',
        )

    if not args:
        return ExecucaoComandoResult(status='VAZIO', comando=comando_bruto, erro='Nenhum comando informado.')

    if tuple(args) not in ALLOWLIST_TUPLAS:
        return ExecucaoComandoResult(
            status='BLOQUEADO',
            comando=comando_bruto,
            erro='Comando fora da allowlist de tupla completa.',
        )

    try:
        resultado = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            timeout=5,
            env={'PATH': '/usr/bin:/bin'},
            cwd=str(Path(diretorio_trabalho).resolve()),
        )
        return ExecucaoComandoResult(
            status='OK' if resultado.returncode == 0 else 'ERRO',
            comando=comando_bruto,
            codigo_retorno=resultado.returncode,
            saida=resultado.stdout.strip(),
            erro=resultado.stderr.strip(),
        )
    except subprocess.TimeoutExpired:
        return ExecucaoComandoResult(
            status='TIMEOUT',
            comando=comando_bruto,
            erro='Tempo limite excedido.',
        )
