"""Cliente HTTP puro para Chat Completions com retry e streaming (TTFT)."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Generator, Optional

from dotenv import load_dotenv

from core.mock_provider import MockProvider

load_dotenv()


@dataclass
class ConfigLLM:
    base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    modelo: str = os.getenv("MODELO_RAPIDO", "gpt-4o-mini")
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    modo_mock: str = os.getenv("MODO_MOCK", "auto").lower()


class ClienteLLM:
    def __init__(self, config: Optional[ConfigLLM] = None) -> None:
        self.config = config or ConfigLLM()

    @property
    def usa_mock(self) -> bool:
        if self.config.modo_mock == "true":
            return True
        if self.config.modo_mock == "false":
            return False
        return not bool(self.config.api_key)

    def _endpoint(self) -> str:
        return f"{self.config.base_url.rstrip('/')}/chat/completions"

    def _request_json(self, payload: dict[str, Any], timeout: int = 30, tentativas: int = 3) -> dict[str, Any]:
        if self.usa_mock:
            raise RuntimeError("Cliente HTTP não deve ser chamado em modo mock.")

        ultimo_erro: Exception | None = None
        for tentativa in range(tentativas):
            try:
                req = urllib.request.Request(
                    self._endpoint(),
                    data=json.dumps(payload).encode("utf-8"),
                    method="POST",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.config.api_key}",
                    },
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    body = resp.read().decode("utf-8")
                return json.loads(body)
            except urllib.error.HTTPError as exc:
                ultimo_erro = exc
                if exc.code < 500 and exc.code != 429:
                    raise
            except (urllib.error.URLError, TimeoutError) as exc:
                ultimo_erro = exc
            time.sleep(2 ** tentativa)

        raise RuntimeError(f"Falha após retries: {ultimo_erro}")

    def criar_completion(self, messages: list[dict[str, str]], max_tokens: int = 200) -> dict[str, Any]:
        payload = {
            "model": self.config.modelo,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0,
        }
        return self._request_json(payload)

    def stream_completion(self, messages: list[dict[str, str]], max_tokens: int = 200) -> Generator[str, None, None]:
        payload = {
            "model": self.config.modelo,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0,
            "stream": True,
        }
        req = urllib.request.Request(
            self._endpoint(),
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            for linha in resp:
                raw = linha.decode("utf-8").strip()
                if not raw.startswith("data:"):
                    continue
                chunk = raw[5:].strip()
                if chunk == "[DONE]":
                    break
                yield chunk

    def medir_ttft(self, messages: list[dict[str, str]], max_tokens: int = 200) -> tuple[float, float]:
        """Retorna (ttft, latencia_total)."""
        inicio = time.perf_counter()
        primeiro_token = None
        if self.usa_mock:
            return 0.01, 0.02

        for _chunk in self.stream_completion(messages, max_tokens=max_tokens):
            if primeiro_token is None:
                primeiro_token = time.perf_counter()
                break
        fim = time.perf_counter()
        if primeiro_token is None:
            return fim - inicio, fim - inicio
        return primeiro_token - inicio, fim - inicio


def criar_provider(config: Optional[ConfigLLM] = None) -> MockProvider:
    """Provider atual: mock determinístico para modo sem chave."""
    cfg = config or ConfigLLM()
    cliente = ClienteLLM(cfg)
    if cliente.usa_mock:
        return MockProvider()
    # Para simplificar o projeto sem frameworks extras: fallback para mock mesmo com chave,
    # mantendo pipeline reproduzível no portfólio.
    return MockProvider(nome_modelo=cfg.modelo)
