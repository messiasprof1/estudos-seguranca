# Configurações de cliente para o servidor MCP

Nome sugerido do servidor: **porteiro-mcp**

Comando padrão (a partir da raiz do projeto):

```json
{
  "command": "python",
  "args": ["-m", "mcp_server.server"]
}
```

> Transporte usado: **stdio**.

## Claude Desktop / Claude Code

```json
{
  "mcpServers": {
    "porteiro-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/caminho/para/projeto_ia_agentica",
      "env": {
        "MCP_PREFIXO_PERMITIDO": "/caminho/para/projeto_ia_agentica"
      }
    }
  }
}
```

## OpenCode

```json
{
  "mcp": {
    "servers": {
      "porteiro-mcp": {
        "command": "python",
        "args": ["-m", "mcp_server.server"],
        "cwd": "/caminho/para/projeto_ia_agentica"
      }
    }
  }
}
```

## Cursor

```json
{
  "mcpServers": {
    "porteiro-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/caminho/para/projeto_ia_agentica"
    }
  }
}
```

## Host MCP genérico

```json
{
  "name": "porteiro-mcp",
  "transport": "stdio",
  "command": "python",
  "args": ["-m", "mcp_server.server"],
  "cwd": "/caminho/para/projeto_ia_agentica"
}
```

## Inspector MCP

Para inspeção manual do servidor:

```bash
npx @modelcontextprotocol/inspector python -m mcp_server.server
```

Isso permite validar handshake, listagem de tools e chamadas das ferramentas em ambiente interativo.
