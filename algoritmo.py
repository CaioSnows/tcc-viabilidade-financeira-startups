import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Limiares de classificacao do runway, em meses
LIMIAR_CRITICO = 6
LIMIAR_ALERTA = 12


def calcular_indicadores(df):
    """Calcula net burn rate e runway para cada empresa."""
    df = df.copy()

    # Net burn rate: quanto de caixa a empresa consome por mes (despesa - receita).
    # Valores negativos indicam que a receita supera a despesa (ponto de equilibrio);
    # nesses casos a queima liquida e considerada zero.
    df["net_burn_rate"] = (df["despesa_mensal"] - df["receita_mensal"]).clip(lower=0)

    # Indicador explicito de ponto de equilibrio, em coluna propria,
    # para nao misturar texto com valores numericos no runway.
    df["breakeven"] = df["net_burn_rate"] == 0

    # Runway: meses de operacao que o caixa atual sustenta.
    # Empresas em equilibrio nao possuem runway finito (NaN).
    df["runway_meses"] = np.where(
        df["breakeven"], np.nan, df["caixa_atual"] / df["net_burn_rate"]
    )
    return df


def classificar(df):
    """Classifica cada empresa segundo os limiares de runway."""
    df = df.copy()
    condicoes = [
        df["breakeven"],
        df["runway_meses"] < LIMIAR_CRITICO,
        df["runway_meses"] <= LIMIAR_ALERTA,
    ]
    classes = ["Saudável", "Crítico", "Alerta"]
    df["classificacao"] = np.select(condicoes, classes, default="Saudável")
    return df


# --- Execucao -----------------------------------------------------------
dados = pd.read_csv("startups_simuladas.csv")
resultado = classificar(calcular_indicadores(dados))
resultado.to_csv("resultado_classificacao.csv", index=False)

# --- Tabela resumo ------------------------------------------------------
ordem = ["Crítico", "Alerta", "Saudável"]
resumo = (
    resultado.groupby("classificacao")
    .agg(
        empresas=("empresa_id", "count"),
        breakeven=("breakeven", "sum"),
        runway_mediano=("runway_meses", "median"),
        runway_min=("runway_meses", "min"),
        runway_max=("runway_meses", "max"),
        burn_mediano=("net_burn_rate", "median"),
    )
    .reindex(ordem)
)
print(resumo.round(1).to_string())
print()
print("Runway (empresas com queima):")
print(resultado["runway_meses"].describe().round(1).to_string())

# --- Figura no padrao do manual USP/Esalq -------------------------------
# Sem titulo, sem linhas de grade, sem borda, sem preenchimento;
# eixos principais em linha preta de 1,5 pt; Arial 11.
plt.rcParams["font.family"] = "Liberation Sans"  # metricamente identica a Arial
plt.rcParams["font.size"] = 11

fig, ax = plt.subplots(figsize=(6.3, 3.6))
contagem = resultado["classificacao"].value_counts().reindex(ordem)
ax.barh(ordem, contagem.values, color="#9e9e9e")

for i, v in enumerate(contagem.values):
    ax.text(v + 0.8, i, str(v), va="center")

ax.set_xlabel("Número de empresas")
ax.set_ylabel("Classificação")
ax.invert_yaxis()
for lado in ["top", "right"]:
    ax.spines[lado].set_visible(False)
for lado in ["left", "bottom"]:
    ax.spines[lado].set_linewidth(1.5)
    ax.spines[lado].set_color("black")
ax.grid(False)
fig.patch.set_alpha(0)

plt.tight_layout()
plt.savefig("figura_classificacao.png", dpi=300)
