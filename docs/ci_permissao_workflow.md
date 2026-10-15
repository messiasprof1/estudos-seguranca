# CI (GitHub Actions)

O workflow `.github/workflows/ci.yml` está ativo e roda a cada push e pull request:

- **Ruff**: verifica estilo e erros comuns no código.
- **Pytest**: roda os testes (Porteiro, Hook, RAG, HITL, API, MCP) em modo mock, sem chave de API.
- **eval.py**: roda o benchmark com as 60 mensagens, para garantir que a avaliação continua funcionando.

## Por que o arquivo foi criado manualmente

O GitHub não deixa apps de terceiros criarem ou alterarem arquivos em `.github/workflows/` sem a
permissão `workflows`, que é definida pelo desenvolvedor do app (não pelo usuário). Por isso o
arquivo foi criado pelo dono do repositório, pelo site do GitHub. Alterações futuras nesse arquivo
também precisam ser feitas por esse caminho.

## Lições do processo

- O arquivo de workflow deve conter **apenas YAML** (primeira linha `name: CI`). Texto extra quebra o parse.
- Para editar pelo site, abra o arquivo na branch `main` (não num commit específico), senão o lápis não aparece.
- A tradução automática do navegador altera o texto exibido; desative-a no GitHub ao conferir código.
