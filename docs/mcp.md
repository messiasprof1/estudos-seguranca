# Servidor MCP (Model Context Protocol)

Este projeto fornece um servidor MCP em **stdio** com ferramentas seguras reutilizando o core.

Arquivo principal: `mcp_server/server.py`

## Conceitos essenciais

- **Tools**: ações executáveis (ex.: ler arquivo, executar comando seguro).
- **Resources**: dados passivos versionáveis (não usados nesta primeira versão).
- **Prompts**: templates orientados para LLMs (não usados nesta primeira versão).
- **Transports**:
  - `stdio` (usado aqui): ideal para integração local por subprocesso.
  - `streamable HTTP`: útil para exposição remota via rede.

## Handshake MCP

Todo cliente MCP faz, no mínimo:

1. `initialize`
2. `tools/list`
3. `tools/call`

Nos testes (`tests/test_mcp.py`), validamos exatamente esse fluxo.

## Ferramentas expostas

1. `listar_diretorio(caminho='.')`
2. `ler_arquivo(caminho, max_chars=5000)`
3. `executar_comando_seguro(comando)`
4. `triagem_porteiro(mensagem)`

## Camada de segurança aplicada

- `listar_diretorio` e `ler_arquivo` delegam para `core/tools.py`, que valida prefixo permitido.
- `executar_comando_seguro` delega para `core/hook_seguranca.py` com allowlist de tupla completa e `shell=False`.
- `triagem_porteiro` delega para `core/porteiro.py` com canonicalização + regex + classificação.

Quando há violação (ex.: tentar ler `/etc/passwd`), o servidor devolve erro MCP com `is_error=true`.

## Configuração em clientes MCP

Veja exemplos prontos em:

- `mcp_server/config_exemplos.md`

Inclui perfis para Claude Desktop/Code, OpenCode, Cursor e host genérico.

## Validação manual com MCP Inspector

```bash
npx @modelcontextprotocol/inspector python -m mcp_server.server
```

Esse fluxo permite verificar handshake, listagem e execução das tools em tempo real.
