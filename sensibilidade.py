import numpy as np
import pandas as pd

# Analise de sensibilidade: repete a classificacao com limiares alternativos
# e conta quantas empresas mudam de classe em relacao aos limiares de referencia.

dados = pd.read_csv("startups_simuladas.csv")

queima = (dados["despesa_mensal"] - dados["receita_mensal"]).clip(lower=0)
breakeven = queima == 0
runway = np.where(breakeven, np.inf, dados["caixa_atual"] / queima.replace(0, np.nan))


def classificar(limiar_critico, limiar_alerta):
    """Classifica as empresas para um par de limiares (em meses)."""
    condicoes = [breakeven, runway < limiar_critico, runway <= limiar_alerta]
    return np.select(condicoes, ["Saudável", "Crítico", "Alerta"], default="Saudável")


referencia = classificar(6, 12)
cenarios = [(3, 9), (6, 12), (9, 18)]

resultado = []
for critico, alerta in cenarios:
    classes = classificar(critico, alerta)
    contagem = pd.Series(classes).value_counts()
    resultado.append({
        "limiares": f"{critico} e {alerta}",
        "critico": contagem.get("Crítico", 0),
        "alerta": contagem.get("Alerta", 0),
        "saudavel": contagem.get("Saudável", 0),
        "reclassificadas": int((classes != referencia).sum()),
    })

print(pd.DataFrame(resultado).to_string(index=False))
