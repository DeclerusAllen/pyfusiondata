import streamlit as st
from scipy import stats as scipy_stats

from src.data_loader import load_data
from src.preprocessing import preprocess, build_rapport
from src.visualizations import (
    plot_scatter_sommeil_productivite,
    plot_distributions,
    plot_sommeil_efficacite_kde,
    plot_sport_productivite_energie,
    plot_definition_productivite,
    plot_pairplot,
    plot_correlation,
)
from src.components import kpi_row, section_header, rapport_table

st.set_page_config(
    page_title="Santé & Productivité",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; }
        [data-testid="stMetricValue"] { font-size: 1.4rem; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

df_raw                  = load_data()
df, df_normalized, corr = preprocess(df_raw)
rapport_df              = build_rapport(df)

n                    = len(df)
age_predominant      = df["Age"].mode()[0]
situation_top        = df["Situation"].mode()[0]
situation_pct        = round(df["Situation"].value_counts(normalize=True).iloc[0] * 100)
sommeil_moy          = round(df["Sommeil_moyen"].mean(), 1)
stress_moy           = round(df["Stress"].mean(), 2)
energie_moy          = round(df["Energie"].mean(), 2)
prod_moy             = round(df["Productivite_7j"].mean(), 2)

sport_labels_map     = {0: "Jamais", 1: "1-2x/sem", 2: "3-4x/sem", 3: "5+x/sem", 4: "Quotidien"}
sport_prod           = df.groupby("Frequence_sport")["Productivite_7j"].mean()
meilleur_sport_label = sport_labels_map.get(int(sport_prod.idxmax()), "N/A")

r_sommeil_prod, p_sommeil_prod = scipy_stats.pearsonr(df["Sommeil_moyen"], df["Productivite_7j"])
r_stress_eff,   p_stress_eff   = scipy_stats.pearsonr(df["Stress"], df["Efficacite_aujourdhui"])
r_eau_energie,  p_eau_energie  = scipy_stats.pearsonr(df["Eau_litres"], df["Energie"])

PAGES = {
    "Vue générale":              "vue",
    "Sommeil & Productivité":    "sommeil",
    "Sport & Energie":           "sport",
    "Définition & Productivité": "definition",
    "Analyse multivariée":       "pairplot",
    "Corrélations":              "corr",
    "Rapport statistique":       "rapport",
    "Conclusions":               "conclusions",
}

with st.sidebar:
    st.title("Santé & Productivité")
    st.caption(f"n={n} répondants — {age_predominant}")
    st.divider()
    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("Données mises à jour toutes les 5 min")
    st.caption(f"{n} répondants")
    st.caption(f"Majorité : {age_predominant}")

section = PAGES[page]

if section == "vue":
    section_header(
        "Santé & Productivité",
        f"Analyse de {n} répondants — majorité {age_predominant} ({situation_top} : {situation_pct}%)",
    )
    kpi_row(df)
    st.divider()
    st.subheader("Distributions des variables clés")
    st.pyplot(plot_distributions(df))

elif section == "sommeil":
    section_header(
        "Sommeil & Productivité",
        "Exploration du lien entre les heures de sommeil et la productivité ressentie",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_scatter_sommeil_productivite(df))
    with col2:
        st.pyplot(plot_sommeil_efficacite_kde(df))

elif section == "sport":
    section_header(
        "Sport & Energie",
        "Impact de la fréquence d'activité physique sur la productivité et l'énergie",
    )
    st.pyplot(plot_sport_productivite_energie(df))

elif section == "definition":
    section_header(
        "Définition & Productivité",
        "La vision de la productivité influence-t-elle les résultats réels ?",
    )
    st.pyplot(plot_definition_productivite(df))

elif section == "pairplot":
    section_header(
        "Analyse multivariée",
        "Vue globale des relations entre sommeil, stress, énergie et productivité",
    )
    st.info("Chaque point représente un répondant. La couleur indique l'efficacité ressentie.")
    st.pyplot(plot_pairplot(df))

elif section == "corr":
    section_header(
        "Matrice de Corrélation",
        "Corrélations de Pearson entre toutes les variables — seuil de significativité p < 0.05",
    )
    st.pyplot(plot_correlation(corr, df_normalized))

elif section == "rapport":
    section_header(
        "Rapport statistique",
        f"Moyennes des indicateurs clés — échantillon de {n} répondants",
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        rapport_table(rapport_df)
    with col2:
        st.bar_chart(rapport_df)

elif section == "conclusions":
    section_header(
        "Conclusions",
        f"Synthèse de l'analyse — n={n} répondants",
    )

    st.markdown("### Points clés")
    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"**Sommeil** — Moyenne de {sommeil_moy}h/nuit. "
            f"Corrélation avec la productivité : r={r_sommeil_prod:.2f} (p={p_sommeil_prod:.3f}). "
            f"{'Lien significatif.' if p_sommeil_prod < 0.05 else 'Lien non significatif sur cet échantillon.'}"
        )
        st.success(
            f"**Sport** — La fréquence '{meilleur_sport_label}' est associée à la meilleure "
            f"productivité moyenne ({sport_prod.max():.2f}/5)."
        )

    with col2:
        st.error(
            f"**Stress** — Moyenne de {stress_moy}/5. "
            f"Corrélation avec l'efficacité : r={r_stress_eff:.2f} (p={p_stress_eff:.3f}). "
            f"{'Lien significatif.' if p_stress_eff < 0.05 else 'Tendance négative observée.'}"
        )
        st.warning(
            f"**Hydratation & Caféine** — Corrélation eau/énergie : r={r_eau_energie:.2f} "
            f"(p={p_eau_energie:.3f}). Signal {'significatif' if p_eau_energie < 0.05 else 'peu clair'} "
            f"avec n={n}."
        )

    st.divider()
    st.markdown("### Limites")
    st.markdown(f"""
    - Échantillon faible **(n={n})** — résultats à interpréter avec précaution
    - Données **auto-reportées** — biais de perception possible
    - **Corrélation ≠ causalité** — aucune relation de cause à effet établie
    - Population majoritairement **{age_predominant}** ({situation_top} : {situation_pct}%) — peu généralisable
    """)

    st.divider()
    st.markdown("### Recommandations")
    st.markdown(f"""
    - Augmenter l'échantillon au-delà de **{n * 4}** répondants pour confirmer les tendances
    - Ajouter un **suivi longitudinal** sur plusieurs semaines
    - Diversifier la population au-delà des **{age_predominant}**
    - Inclure des variables supplémentaires : qualité de l'alimentation, temps d'écran, etc.
    """)