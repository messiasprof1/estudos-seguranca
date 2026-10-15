import json
from unittest.mock import patch

from core.cliente_llm import ClienteLLM, ConfigLLM


class _Resp:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps({'ok': True, 'choices': []}).encode('utf-8')


def test_cliente_http_retry_sem_erro():
    cfg = ConfigLLM(api_key='x', modo_mock='false', base_url='https://api.openai.com/v1')
    c = ClienteLLM(cfg)
    with patch('urllib.request.urlopen', return_value=_Resp()):
        out = c._request_json({'model': 'x'})
    assert out['ok'] is True


def test_ttft_mock():
    cfg = ConfigLLM(api_key='', modo_mock='auto')
    c = ClienteLLM(cfg)
    ttft, total = c.medir_ttft([{'role': 'user', 'content': 'oi'}])
    assert ttft <= total
