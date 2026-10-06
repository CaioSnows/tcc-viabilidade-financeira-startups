# Ferramenta digital para sistematização de indicadores de viabilidade financeira em startups em estágio inicial

Código do Trabalho de Conclusão de Curso apresentado ao MBA em Engenharia de Software (USP/Esalq), 2026.

**Autor:** Caio Cesar de Barros Neves
**Orientador:** Luiz Fernando Pereira Nunes

## O que o código faz

A ferramenta calcula, para cada empresa, dois indicadores de viabilidade financeira de curto prazo:

- **Queima líquida mensal (net burn rate):** `B = D − R` (despesa menos receita; nula quando a receita supera a despesa)
- **Runway:** `T = C / B` (meses que o caixa disponível sustenta a operação no ritmo atual)

E classifica a situação financeira de curto prazo em três faixas:

| Classe   | Critério                                   |
|----------|--------------------------------------------|
| Crítico  | runway inferior a 6 meses                  |
| Alerta   | runway entre 6 e 12 meses                  |
| Saudável | runway acima de 12 meses ou ponto de equilíbrio |

## Arquivos

| Arquivo            | Função |
|--------------------|--------|
| `gerador.py`       | Gera 100 empresas simuladas (distribuição lognormal, semente fixa 42) e salva `startups_simuladas.csv` |
| `algoritmo.py`     | Calcula os indicadores, classifica as empresas, salva `resultado_classificacao.csv` e a figura `figura_classificacao.png` |
| `sensibilidade.py` | Repete a classificação com limiares alternativos (3/9 e 9/18 meses) e conta as empresas reclassificadas |

## Como reproduzir

Requer Python 3 e as bibliotecas listadas em `requirements.txt`.

```bash
pip install -r requirements.txt
python gerador.py
python algoritmo.py
python sensibilidade.py
```

Os scripts devem ser executados nessa ordem e na mesma pasta. Com a semente fixa, os resultados reproduzem exatamente os apresentados no trabalho.

## Observação

Os dados são inteiramente simulados. Não há dados de empresas ou pessoas reais neste repositório.
