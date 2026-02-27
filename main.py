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
    page_title="PyFusion — Santé & Productivité",
    layout="wide",
)

st.markdown("""
    <style>
        /* Global */
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; background: #ffffff; }
        body { background-color: #ffffff; }

        /* Métriques */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            border-top: 4px solid #A41E37;
            box-shadow: 0 2px 8px rgba(164,30,55,0.10);
        }
        [data-testid="stMetricValue"] {
            font-size: 1.6rem;
            font-weight: 800;
            color: #A41E37;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.82rem;
            color: #333;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 3px solid #A41E37;
        }
        section[data-testid="stSidebar"] .stRadio label {
            font-size: 0.9rem;
            color: #222;
            padding: 0.25rem 0;
        }
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: #333;
        }

        /* Header band */
        .header-band {
            background: linear-gradient(135deg, #A41E37 0%, #7a1228 100%);
            padding: 2rem 2.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }
        .header-band h1 {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 0.3rem 0;
        }
        .header-band p {
            color: rgba(255,255,255,0.85);
            margin: 0;
            font-size: 0.95rem;
        }

        /* Badges */
        .badge {
            display: inline-block;
            background: #ffffff;
            color: #A41E37;
            border-radius: 20px;
            padding: 0.2rem 0.9rem;
            font-size: 0.75rem;
            font-weight: 700;
            margin-right: 0.5rem;
            margin-top: 0.6rem;
        }
        .badge-outline {
            display: inline-block;
            border: 1.5px solid rgba(255,255,255,0.7);
            color: #ffffff;
            border-radius: 20px;
            padding: 0.2rem 0.9rem;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
            margin-top: 0.6rem;
        }

        /* Cards */
        .card {
            background: #ffffff;
            border-radius: 10px;
            padding: 1.4rem 1.6rem;
            border-left: 4px solid #A41E37;
            box-shadow: 0 2px 10px rgba(0,0,0,0.07);
            margin-bottom: 1rem;
            height: 100%;
        }
        .card h4 {
            color: #A41E37;
            margin: 0 0 0.6rem 0;
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .card p {
            color: #333;
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.7;
        }

        /* Section title */
        .section-title {
            color: #A41E37;
            font-size: 1.6rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .section-sub {
            color: #555;
            font-size: 0.92rem;
            margin-top: 0;
            margin-bottom: 0.5rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #999;
            font-size: 0.8rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }
        .footer span { color: #A41E37; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

LOGO_URL = "https://images.squarespace-cdn.com/content/v1/604f4f7bdad32a12b24382e6/8350aaa8-4e63-4176-90f1-c6ce04a63f56/Cover_ESIH-29.jpg?format=1500w"

df_raw                  = load_data()
df, df_normalized, corr = preprocess(df_raw)
rapport_df              = build_rapport(df)

n                    = len(df)
age_predominant      = df["Age"].mode()[0]
situation_top        = df["Situation"].mode()[0]
situation_pct        = round(df["Situation"].value_counts(normalize=True).iloc[0] * 100)
sommeil_moy          = round(df["Sommeil_moyen"].mean(), 1)
stress_moy           = round(df["Stress"].mean(), 2)
prod_moy             = round(df["Productivite_7j"].mean(), 2)

sport_labels_map     = {0: "Jamais", 1: "1-2x/sem", 2: "3-4x/sem", 3: "5+x/sem", 4: "Quotidien"}
sport_prod           = df.groupby("Frequence_sport")["Productivite_7j"].mean()
meilleur_sport_label = sport_labels_map.get(int(sport_prod.idxmax()), "N/A")

r_sommeil_prod, p_sommeil_prod = scipy_stats.pearsonr(df["Sommeil_moyen"], df["Productivite_7j"])
r_stress_eff,   p_stress_eff   = scipy_stats.pearsonr(df["Stress"], df["Efficacite_aujourdhui"])
r_eau_energie,  p_eau_energie  = scipy_stats.pearsonr(df["Eau_litres"], df["Energie"])

PAGES = {
    "Introduction":              "intro",
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
    st.image(LOGO_URL, use_container_width=True)
    st.markdown("<hr style='border-color:#A41E37;margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center;margin-bottom:0.8rem;'>"
        "<span style='color:#A41E37;font-size:1.1rem;font-weight:800;'>PyFusion</span><br>"
        "<span style='color:#555;font-size:0.78rem;'>Python orientée Data · ESIH</span>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color:#A41E37;margin:0.8rem 0;'>", unsafe_allow_html=True)
    page = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.markdown("<hr style='border-color:#eee;margin:0.8rem 0;'>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:0.78rem;color:#777;text-align:center;'>"
        f"Données en temps réel · n={n} répondants"
        f"</div>",
        unsafe_allow_html=True,
    )

section = PAGES[page]

def footer():
    st.markdown(
        f"<div class='footer'>PyFusion · <span>Python orientée Data</span> · ESIH · n={n} répondants</div>",
        unsafe_allow_html=True,
    )

if section == "intro":
    st.markdown(
        f"""
        <div class="header-band">
            <h1>Santé, Habitudes de vie & Productivité</h1>
            <p>Projet final · Python orientée Data · ESIH · Groupe PyFusion</p>
            <div style="margin-top:0.6rem;">
                <span class="badge">PyFusion</span>
                <span class="badge-outline">ESIH</span>
                <span class="badge-outline">n={n} répondants</span>
                <span class="badge-outline">{age_predominant}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h4>Contexte & Problématique</h4>
                <p>
                    La productivité est souvent traitée comme un enjeu purement organisationnel,
                    mais elle est profondément liée aux habitudes de vie des individus.
                    Sommeil insuffisant, sédentarité, stress chronique — ces facteurs influencent
                    directement la capacité à travailler efficacement.<br><br>
                    <strong>Question centrale :</strong> Existe-t-il un lien mesurable entre
                    les habitudes de vie (sommeil, sport, hydratation) et le sentiment de
                    productivité ou de stress ?
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="card">
                <h4>Objectifs de l'analyse</h4>
                <p>
                    1. Identifier les corrélations entre variables de santé et productivité<br>
                    2. Comparer les profils selon la fréquence de sport et le sommeil<br>
                    3. Quantifier l'impact du stress sur l'efficacité ressentie<br>
                    4. Produire des recommandations basées sur les données
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h4>Méthodologie & Outils</h4>
                <p>
                    <strong>Collecte</strong> — Questionnaire Google Forms, février 2026<br>
                    <strong>Nettoyage</strong> — Normalisation des réponses textuelles,
                    traitement des outliers, imputation par mode<br>
                    <strong>Analyse</strong> — Corrélation de Pearson, visualisation
                    multivariée, test de significativité (p &lt; 0.05)<br><br>
                    <strong>Stack technique :</strong><br>
                    Python · Pandas · NumPy · Seaborn · Matplotlib · SciPy · Streamlit
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="card">
                <h4>Description de l'échantillon</h4>
                <p>
                    <strong>Taille :</strong> {n} répondants<br>
                    <strong>Tranche d'âge dominante :</strong> {age_predominant}<br>
                    <strong>Situation principale :</strong> {situation_top} ({situation_pct}%)<br>
                    <strong>Période :</strong> Février 2026<br>
                    <strong>Mode de collecte :</strong> Questionnaire en ligne anonyme
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    footer()

elif section == "vue":
    section_header(
        "Vue générale",
        f"Analyse de {n} répondants — majorité {age_predominant} ({situation_top} : {situation_pct}%)",
    )
    kpi_row(df)
    st.divider()
    st.subheader("Distributions des variables clés")
    st.pyplot(plot_distributions(df))
    footer()

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
    footer()

elif section == "sport":
    section_header(
        "Sport & Energie",
        "Impact de la fréquence d'activité physique sur la productivité et l'énergie",
    )
    st.pyplot(plot_sport_productivite_energie(df))
    footer()

elif section == "definition":
    section_header(
        "Définition & Productivité",
        "La vision de la productivité influence-t-elle les résultats réels ?",
    )
    st.pyplot(plot_definition_productivite(df))
    footer()

elif section == "pairplot":
    section_header(
        "Analyse multivariée",
        "Vue globale des relations entre sommeil, stress, énergie et productivité",
    )
    st.info("Chaque point représente un répondant. La couleur indique l'efficacité ressentie.")
    st.pyplot(plot_pairplot(df))
    footer()

elif section == "corr":
    section_header(
        "Matrice de Corrélation",
        "Corrélations de Pearson entre toutes les variables — seuil de significativité p < 0.05",
    )
    st.pyplot(plot_correlation(corr, df_normalized))
    footer()

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
    footer()

elif section == "conclusions":
    section_header(
        "Conclusions & Recommandations",
        f"Analyse automatisée basée sur n={n} répondants",
    )

    # --- LOGIQUE D'INTERPRÉTATION DYNAMIQUE ---
    # Sommeil
    if p_sommeil_prod < 0.05:
        sommeil_status = "Significatif"
        sommeil_color = "success"
        sommeil_desc = f"Le sommeil influence directement la productivité (r={r_sommeil_prod:.2f})."
    else:
        sommeil_status = "Non significatif"
        sommeil_color = "warning"
        sommeil_desc = "Le groupe maintient sa productivité malgré la fatigue (effort de volonté)."

    # Stress
    if p_stress_eff < 0.05:
        stress_status = "Impact Critique"
        stress_color = "error"
        stress_desc = f"Le stress dégrade l'efficacité (r={r_stress_eff:.2f})."
    else:
        stress_status = "Sous contrôle"
        stress_color = "success"
        stress_desc = "Le stress actuel n'impacte pas encore l'efficacité de manière majeure."

    # --- AFFICHAGE ---
    st.markdown("### 1. Diagnostic de l'échantillon")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Potentiel de Récupération", f"{8 - sommeil_moy:.1f}h", "Dette de sommeil")
    with col2:
        st.metric("Efficacité moyenne", f"{prod_moy}/5")
    with col3:
        st.metric("Meilleur levier", meilleur_sport_label)

    st.divider()

    st.markdown("### 2. Synthèse des corrélations")
    c1, c2 = st.columns(2)
    
    with c1:
        if sommeil_color == "success":
            st.success(f"**Sommeil ({sommeil_status})** : {sommeil_desc}")
        else:
            st.warning(f"**Sommeil ({sommeil_status})** : {sommeil_desc}")
            
        st.info(f"**Sport** : La fréquence '{meilleur_sport_label}' génère le pic d'énergie maximal.")

    with c2:
        if stress_color == "error":
            st.error(f"**Stress ({stress_status})** : {stress_desc}")
        else:
            st.success(f"**Stress ({stress_status})** : {stress_desc}")
        
        # Hydratation (Logique dynamique simplifiée)
        hydro_msg = "Lien eau/énergie confirmé." if p_eau_energie < 0.05 else "Pas de lien eau/énergie clair."
        st.write(f"**Hydratation** : {hydro_msg} (r={r_eau_energie:.2f})")

    st.divider()

    # --- RECOMMANDATIONS SUR MESURE ---
    st.markdown("### 3. Recommandations basées sur les données")
    
    recos = []
    if sommeil_moy < 6.5:
        recos.append(f"**Priorité Sommeil** : La moyenne de {sommeil_moy}h est trop basse. Augmenter de 30min/nuit pour stabiliser l'énergie.")
    if r_stress_eff < -0.20:
        recos.append("**Gestion du Stress** : L'impact sur l'efficacité est visible. Introduire des micro-pauses actives.")
    if n < 100:
        recos.append(f"**Fiabilité** : Collecter {100 - n} réponses supplémentaires pour valider les tendances (actuellement n={n}).")

    for r in recos:
        st.markdown(r)

    footer()