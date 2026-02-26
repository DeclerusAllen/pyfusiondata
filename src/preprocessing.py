import pandas as pd
import numpy as np
import streamlit as st

FREQ_MAP = {
    "Jamais": 0,
    "Parfois (1 à 2 fois par semaine)": 1,
    "3 à 4 fois par semaine": 2,
    "Souvent (3 à 5 fois par semaine)": 3,
    "Tous les jours": 4,
}

PROD_MAP = {
    "Mou du genou (Petite forme, beaucoup de distractions)": 1,
    "Propre (Efficacité correcte, boulot fait)": 2,
    "Déterminé (Très productif et concentré)": 3,
    "Speed (Pas mal de pression)": 2,
}

STRESS_MAP = {
    "Tranquille (Stress léger et gérable)": 1,
    "Mou du genou (Stress modéré)": 2,
    "Speed (Pas mal de pression)": 3,
    "Stress élevé / Très tendu": 4,
}


def _convertir_sommeil(val):
    if pd.isna(val):
        return np.nan
    val = (
        str(val).lower()
        .replace("heures", "").replace("hres", "")
        .replace("h", "").replace("environ", "").strip()
    )
    val = val.replace("ou", "-").replace("à", "-").replace(" ", "")
    try:
        if "-" in val:
            parts = val.split("-")
            nums = [float(p) for p in parts if p.replace(".", "", 1).isdigit()]
            return np.mean(nums)
        return float(val)
    except Exception:
        return np.nan


def _parse_mixed(val, text_map):
    if pd.isna(val):
        return np.nan
    try:
        return float(val)
    except (ValueError, TypeError):
        return text_map.get(str(val).strip(), np.nan)


@st.cache_data
def preprocess(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = df.copy()

    df["Sommeil_moyen"]         = df["Sommeil_moyen"].apply(_convertir_sommeil)
    df["Sommeil_nuit_derniere"] = df["Sommeil_nuit_derniere"].apply(_convertir_sommeil)
    df.loc[df["Sommeil_moyen"] > 12, "Sommeil_moyen"] = np.nan

    df["Frequence_sport"]       = df["Frequence_sport"].map(FREQ_MAP)
    df["Efficacite_aujourdhui"] = df["Efficacite_aujourdhui"].map(PROD_MAP)
    df["Productivite_7j"]       = pd.to_numeric(df["Productivite_7j"], errors="coerce")
    df["Stress"]                = df["Stress"].apply(_parse_mixed, text_map=STRESS_MAP)
    df["Energie"]               = pd.to_numeric(df["Energie"], errors="coerce")
    df["Eau_litres"]            = pd.to_numeric(df["Eau_litres"], errors="coerce")
    df.loc[df["Eau_litres"] > 10, "Eau_litres"] /= 1000

    num_cols = df.select_dtypes(include=np.number).columns
    df[num_cols] = df[num_cols].apply(
        lambda col: col.fillna(col.mode()[0] if not col.mode().empty else 0)
    )

    df_normalized = df.copy()
    df_normalized[num_cols] = df_normalized[num_cols].apply(
        lambda col: (col - col.min()) / (col.max() - col.min())
        if col.max() != col.min() else col
    )

    corr = df_normalized[num_cols].corr()

    return df, df_normalized, corr


def build_rapport(df: pd.DataFrame) -> pd.DataFrame:
    rapport = {
        "Moyenne sommeil (heures)":       df["Sommeil_moyen"].mean(),
        "Moyenne sommeil nuit dernière":   df["Sommeil_nuit_derniere"].mean(),
        "Moyenne productivité 7j":         df["Productivite_7j"].mean(),
        "Moyenne stress":                  df["Stress"].mean(),
        "Moyenne fréquence sport":         df["Frequence_sport"].mean(),
        "Moyenne eau (litres)":            df["Eau_litres"].mean(),
        "Moyenne énergie":                 df["Energie"].mean(),
        "Moyenne caféine (verres/j)":      df["Cafe"].mean(),
    }
    return (
        pd.DataFrame.from_dict(rapport, orient="index", columns=["Moyenne"])
        .round(2)
    )
