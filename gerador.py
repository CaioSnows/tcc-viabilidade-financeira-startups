import numpy as np
import pandas as pd

SEMENTE = 42
N = 100
rng = np.random.default_rng(SEMENTE)

# --- Calibracao da distribuicao de runway -------------------------------
# Limiares definidos: critico < 6 meses; alerta 6-12; saudavel > 12.
# Adota-se distribuicao lognormal para o runway (assimetrica, sempre positiva).
# Parametros escolhidos para que os tercis da distribuicao coincidam com os
# limiares de classificacao, ou seja, ~1/3 das empresas em cada faixa.
#
#   mediana = sqrt(6 * 12) = 8,485 meses  (media geometrica dos limiares)
#   sigma   = ln(2) / 0,8614 = 0,805       (0,8614 = z de 2/3 menos z de 1/3)
MEDIANA_RUNWAY = np.sqrt(6 * 12)
SIGMA_RUNWAY = np.log(2) / 0.8614

# Fracao de empresas que ja atingiram o ponto de equilibrio (receita >= despesa)
P_BREAKEVEN = 0.10

# --- Geracao ------------------------------------------------------------
# Caixa disponivel: lognormal. A escala e arbitraria e declarada como tal;
# o que se calibra e a razao caixa/queima, nao o valor absoluto.
caixa = rng.lognormal(mean=np.log(200_000), sigma=0.8, size=N)

# Receita mensal: lognormal, independente do caixa
receita = rng.lognormal(mean=np.log(30_000), sigma=1.0, size=N)

# Runway alvo por empresa
runway_alvo = rng.lognormal(mean=np.log(MEDIANA_RUNWAY), sigma=SIGMA_RUNWAY, size=N)

# Queima liquida derivada: despesa - receita = caixa / runway
queima = caixa / runway_alvo
despesa = receita + queima

# Empresas em breakeven: despesa passa a ser menor que a receita
breakeven = rng.random(N) < P_BREAKEVEN
despesa[breakeven] = receita[breakeven] * rng.uniform(0.75, 0.95, size=breakeven.sum())

df = pd.DataFrame({
    "empresa_id": [f"E{i:03d}" for i in range(1, N + 1)],
    "caixa_atual": caixa.round(2),
    "receita_mensal": receita.round(2),
    "despesa_mensal": despesa.round(2),
})

df.to_csv("startups_simuladas.csv", index=False)

# --- Conferencia --------------------------------------------------------
burn = (df["despesa_mensal"] - df["receita_mensal"]).clip(lower=0)
rw = np.where(burn > 0, df["caixa_atual"] / burn.replace(0, np.nan), np.inf)

faixa = pd.cut(rw, bins=[-np.inf, 6, 12, np.inf],
               labels=["critico", "alerta", "saudavel"])
print(pd.Series(faixa).value_counts().sort_index())
print()
print(df.describe().round(2).to_string())
