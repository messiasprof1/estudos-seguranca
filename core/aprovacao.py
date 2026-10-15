"""Fila HITL persistida em SQLite."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class FilaAprovacao:
    caminho_db: str = "aprovacoes.db"

    def __post_init__(self) -> None:
        Path(self.caminho_db).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.caminho_db)

    def _init_db(self) -> None:
        sql = """
        CREATE TABLE IF NOT EXISTS fila_hitl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comando TEXT NOT NULL,
            contexto TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente',
            timestamp TEXT NOT NULL,
            aprovado_por TEXT
        )
        """
        with self._conn() as conn:
            conn.execute(sql)

    def enfileirar(self, comando: str, contexto: str) -> int:
        ts = datetime.utcnow().isoformat()
        with self._conn() as conn:
            cur = conn.execute(
                'INSERT INTO fila_hitl (comando, contexto, status, timestamp) VALUES (?, ?, ?, ?)',
                (comando, contexto, 'pendente', ts),
            )
            return int(cur.lastrowid)

    def listar(self, status: str | None = None) -> list[dict[str, Any]]:
        with self._conn() as conn:
            conn.row_factory = sqlite3.Row
            if status:
                cur = conn.execute('SELECT * FROM fila_hitl WHERE status = ? ORDER BY id', (status,))
            else:
                cur = conn.execute('SELECT * FROM fila_hitl ORDER BY id')
            return [dict(row) for row in cur.fetchall()]

    def atualizar_status(self, item_id: int, status: str, aprovado_por: str | None = None) -> bool:
        if status not in {'pendente', 'aprovado', 'rejeitado', 'expirado'}:
            raise ValueError('Status inválido para HITL.')
        with self._conn() as conn:
            cur = conn.execute(
                'UPDATE fila_hitl SET status = ?, aprovado_por = ? WHERE id = ?',
                (status, aprovado_por, item_id),
            )
            return cur.rowcount > 0

    def expirar_antigos(self, minutos: int = 30) -> int:
        limite = (datetime.utcnow() - timedelta(minutes=minutos)).isoformat()
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE fila_hitl SET status = 'expirado' WHERE status = 'pendente' AND timestamp < ?",
                (limite,),
            )
            return cur.rowcount
