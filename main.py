import streamlit as st

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

df_raw                   = load_data()
df, df_normalized, corr  = preprocess(df_raw)
rapport_df               = build_rapport(df)

PAGES = {
    "Vue générale":              "vue",
    "Sommeil & Productivité":    "sommeil",
    "Sport & Énergie":           "sport",
    "Définition & Productivité": "definition",
    "Analyse multivariée":       "pairplot",
    "Corrélations":              "corr",
    "Rapport statistique":       "rapport",
    "Conclusions":               "conclusions",
}

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/activity-monitor.png", width=60)
    st.title("Santé & Productivité")
    st.caption("Analyse — Février 2026")
    st.divider()
    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption("Données mises à jour toutes les 5 min")
    st.caption(f"👥 n = {len(df)} répondants")

section = PAGES[page]

if section == "vue":
    section_header(
        "Santé & Productivité",
        "Analyse des habitudes de vie et leur impact sur la productivité — Février 2026",
    )
    kpi_row(df)
    st.divider()
    st.subheader("Distributions des variables clés")
    st.pyplot(plot_distributions(df))

elif section == "sommeil":
    section_header(
        "💤 Sommeil & Productivité",
        "Exploration du lien entre les heures de sommeil et la productivité ressentie",
    )
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_scatter_sommeil_productivite(df))
    with col2:
        st.pyplot(plot_sommeil_efficacite_kde(df))

elif section == "sport":
    section_header(
        "🏃 Sport & Énergie",
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
        "Moyennes des indicateurs clés de l'échantillon",
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        rapport_table(rapport_df)
    with col2:
        st.bar_chart(rapport_df)

elif section == "conclusions":
    section_header("Conclusions")

    st.markdown("### Points clés")
    col1, col2 = st.columns(2)

    with col1:
        st.success("**Sommeil** — Tendance positive avec la productivité. Dormir davantage semble associé à une meilleure performance.")
        st.success("**Sport** — Les personnes actives affichent une meilleure énergie et productivité, notamment au-delà de 3×/semaine.")

    with col2:
        st.error("**Stress** — Corrélation négative avec l'efficacité ressentie. Un stress élevé nuit à la productivité.")
        st.warning("**Hydratation & Caféine** — Signal peu clair avec n=27. Échantillon insuffisant pour conclure.")

    st.divider()
    st.markdown("### Limites")
    st.markdown("""
    - Échantillon faible **(n=27)** → résultats à interpréter avec précaution
    - Données **auto-reportées** → biais de perception possible
    - **Corrélation ≠ causalité** — aucune relation de cause à effet établie
    - Population majoritairement **étudiante (18-25 ans)** → peu généralisable
    """)

    st.divider()
    st.markdown("### Recommandations")
    st.markdown("""
    - Augmenter l'échantillon **(n ≥ 100)** pour confirmer les tendances
    - Ajouter un **suivi longitudinal** sur plusieurs semaines
    - Inclure des variables supplémentaires : qualité de l'alimentation, temps d'écran, etc.
    """)
