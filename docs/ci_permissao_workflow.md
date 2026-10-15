# Como ativar o CI (GitHub Actions)

O GitHub não deixa apps de terceiros criarem arquivos em `.github/workflows/` sem uma permissão
especial (`workflows`). Quem define essa permissão é o desenvolvedor do app, não o usuário.
Por isso, quem cria o arquivo é o dono do repositório, direto pelo site do GitHub.

## Passo a passo (pelo navegador)

1. Abra o repositório no GitHub → **Add file** → **Create new file**.
2. No nome do arquivo, digite exatamente: `.github/workflows/ci.yml`
   (ao digitar `/`, o GitHub cria as pastas sozinho).
3. Cole o conteúdo abaixo.
4. Clique em **Commit changes...** → **Commit directly to the main branch** → **Commit changes**.
5. Vá na aba **Actions**: a execução "CI" aparece em alguns segundos e deve terminar com ✅.

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      MODO_MOCK: "true"
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Ruff
        run: ruff check .
      - name: Pytest
        run: pytest -q
      - name: Avaliação mock
        run: python eval.py
```

## O que este CI faz

- **Ruff**: verifica estilo e erros comuns no código.
- **Pytest**: roda os testes (Porteiro, Hook, RAG, HITL, API, MCP) em modo mock, sem chave de API.
- **eval.py**: roda o benchmark com as 60 mensagens, para garantir que a avaliação continua funcionando.

## Badge para o README (opcional)

```markdown
![CI](https://prod-assets.cosmic.aws.dev/a/3BrhofxVVRtSU7aVMEccdgkpI3I/imag.webp)
```
