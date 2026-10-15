# Resultados de Avaliação (Modo Mock)

## Configuração
- Execução em modo mock determinístico (sem chave de API).
- Total de mensagens: 60
- Distribuição: {'financeiro': 24, 'suporte': 15, 'comercial': 9, 'ataque': 7, 'ambiguo': 5}

## Comparação entre estratégias
| Sistema | Acurácia | Macro F1 | Latência p50 (ms) | Latência p95 (ms) | Custo médio (USD/chamada) |
|---|---:|---:|---:|---:|---:|
| porteiro | 0.6167 | 0.6564 | 0.013 | 0.036 | 0.00000938 |
| llm_puro | 0.5833 | 0.6101 | 0.005 | 0.007 | 0.00000938 |
| regex_puro | 0.5667 | 0.6239 | 0.007 | 0.010 | 0.00000938 |

## Detalhes — porteiro
### F1 por classe
- financeiro: precisão=0.938, recall=0.625, f1=0.750
- suporte: precisão=1.000, recall=0.467, f1=0.636
- comercial: precisão=1.000, recall=0.556, f1=0.714
- ataque: precisão=1.000, recall=0.857, f1=0.923
- ambiguo: precisão=0.154, recall=0.800, f1=0.258
### Custo médio por intenção prevista
- ambiguo: USD 0.00001052
- ataque: USD 0.00000848
- comercial: USD 0.00000849
- financeiro: USD 0.00000856
- suporte: USD 0.00000844
### Matriz de confusão (real x previsto)
```json
{
  "financeiro": {
    "financeiro": 15,
    "suporte": 0,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 9
  },
  "suporte": {
    "financeiro": 0,
    "suporte": 7,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 8
  },
  "comercial": {
    "financeiro": 0,
    "suporte": 0,
    "comercial": 5,
    "ataque": 0,
    "ambiguo": 4
  },
  "ataque": {
    "financeiro": 0,
    "suporte": 0,
    "comercial": 0,
    "ataque": 6,
    "ambiguo": 1
  },
  "ambiguo": {
    "financeiro": 1,
    "suporte": 0,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 4
  }
}
```

## Detalhes — llm_puro
### F1 por classe
- financeiro: precisão=0.938, recall=0.625, f1=0.750
- suporte: precisão=0.875, recall=0.467, f1=0.609
- comercial: precisão=1.000, recall=0.556, f1=0.714
- ataque: precisão=1.000, recall=0.571, f1=0.727
- ambiguo: precisão=0.148, recall=0.800, f1=0.250
### Custo médio por intenção prevista
- ambiguo: USD 0.00001043
- ataque: USD 0.00000851
- comercial: USD 0.00000849
- financeiro: USD 0.00000856
- suporte: USD 0.00000849
### Matriz de confusão (real x previsto)
```json
{
  "financeiro": {
    "financeiro": 15,
    "suporte": 0,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 9
  },
  "suporte": {
    "financeiro": 0,
    "suporte": 7,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 8
  },
  "comercial": {
    "financeiro": 0,
    "suporte": 0,
    "comercial": 5,
    "ataque": 0,
    "ambiguo": 4
  },
  "ataque": {
    "financeiro": 0,
    "suporte": 1,
    "comercial": 0,
    "ataque": 4,
    "ambiguo": 2
  },
  "ambiguo": {
    "financeiro": 1,
    "suporte": 0,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 4
  }
}
```

## Detalhes — regex_puro
### F1 por classe
- financeiro: precisão=0.923, recall=0.500, f1=0.649
- suporte: precisão=1.000, recall=0.400, f1=0.571
- comercial: precisão=0.875, recall=0.778, f1=0.824
- ataque: precisão=1.000, recall=0.714, f1=0.833
- ambiguo: precisão=0.143, recall=0.800, f1=0.242
### Custo médio por intenção prevista
- ambiguo: USD 0.00001039
- ataque: USD 0.00000840
- comercial: USD 0.00000851
- financeiro: USD 0.00000855
- suporte: USD 0.00000847
### Matriz de confusão (real x previsto)
```json
{
  "financeiro": {
    "financeiro": 12,
    "suporte": 0,
    "comercial": 1,
    "ataque": 0,
    "ambiguo": 11
  },
  "suporte": {
    "financeiro": 0,
    "suporte": 6,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 9
  },
  "comercial": {
    "financeiro": 0,
    "suporte": 0,
    "comercial": 7,
    "ataque": 0,
    "ambiguo": 2
  },
  "ataque": {
    "financeiro": 0,
    "suporte": 0,
    "comercial": 0,
    "ataque": 5,
    "ambiguo": 2
  },
  "ambiguo": {
    "financeiro": 1,
    "suporte": 0,
    "comercial": 0,
    "ataque": 0,
    "ambiguo": 4
  }
}
```