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
    "Que dalle (Rien fait du tout)": 0,
}

STRESS_MAP = {
    "Tranquille (Stress léger et gérable)": 1,
    "Mou du genou (Stress modéré)": 2,
    "Speed (Pas mal de pression)": 3,
    "Stress élevé / Très tendu": 4,
}

MOTS_CHIFFRES = {
    "zero": 0, "un": 1, "deux": 2, "trois": 3, "quatre": 4,
    "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9,
    "dix": 10, "onze": 11, "douze": 12,
}

BORNES = {
    "Sommeil_moyen":          (2.0, 12.0),
    "Sommeil_nuit_derniere":  (2.0, 12.0),
    "Eau_litres":             (0.0,  5.0),
    "Cafe":                   (0.0, 10.0),
    "Stress":                 (1.0,  5.0),
    "Energie":                (1.0,  5.0),
    "Productivite_7j":        (1.0,  5.0),
}


def _convertir_sommeil(val):
    if pd.isna(val):
        return np.nan

    val = str(val).lower()

    for mot, chiffre in MOTS_CHIFFRES.items():
        val = val.replace(mot, str(chiffre))

    val = (
        val
        .replace("heures", "").replace("heure", "")
        .replace("hres", "").replace("hrs", "")
        .replace("de temps", "").replace("de t", "")
        .replace("environ", "").replace("h", "")
        .replace("mnt", "").replace("mn", "")
        .strip()
    )

    val = (
        val
        .replace("ou", "-").replace("à", "-")
        .replace("a", "-").replace(" ", "")
    )

    while "--" in val:
        val = val.replace("--", "-")
    val = val.strip("-")

    try:
        if "-" in val:
            parts = val.split("-")
            nums = [float(p) for p in parts if p.replace(".", "", 1).isdigit()]
            return np.mean(nums) if nums else np.nan
        return float(val) if val else np.nan
    except Exception:
        return np.nan


def _parse_mixed(val, text_map):
    if pd.isna(val):
        return np.nan
    try:
        return float(val)
    except (ValueError, TypeError):
        return text_map.get(str(val).strip(), np.nan)


def _nettoyer_eau(val):
    if pd.isna(val):
        return np.nan
    try:
        v = float(val)
        if v > 20:
            return v / 1000
        if v > 5:
            return v * 0.25
        return v
    except Exception:
        return np.nan


def _cap_colonne(series: pd.Series, min_val: float, max_val: float) -> pd.Series:
    median = series.clip(lower=min_val, upper=max_val).median()
    out_of_bounds = (series < min_val) | (series > max_val)
    series = series.clip(lower=min_val, upper=max_val)
    series[out_of_bounds] = median
    return series


@st.cache_data
def preprocess(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = df.copy()

    df["Sommeil_moyen"]         = df["Sommeil_moyen"].apply(_convertir_sommeil)
    df["Sommeil_nuit_derniere"] = df["Sommeil_nuit_derniere"].apply(_convertir_sommeil)
    df["Frequence_sport"]       = df["Frequence_sport"].map(FREQ_MAP)
    df["Efficacite_aujourdhui"] = df["Efficacite_aujourdhui"].map(PROD_MAP)
    df["Productivite_7j"]       = pd.to_numeric(df["Productivite_7j"], errors="coerce")
    df["Stress"]                = df["Stress"].apply(_parse_mixed, text_map=STRESS_MAP)
    df["Energie"]               = pd.to_numeric(df["Energie"], errors="coerce")
    df["Cafe"]                  = pd.to_numeric(df["Cafe"], errors="coerce")
    df["Eau_litres"]            = df["Eau_litres"].apply(_nettoyer_eau)

    for col, (min_val, max_val) in BORNES.items():
        df[col] = _cap_colonne(df[col], min_val, max_val)

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
        "Moyenne sommeil (heures)":      df["Sommeil_moyen"].mean(),
        "Moyenne sommeil nuit dernière":  df["Sommeil_nuit_derniere"].mean(),
        "Moyenne productivité 7j":        df["Productivite_7j"].mean(),
        "Moyenne stress":                 df["Stress"].mean(),
        "Moyenne fréquence sport":        df["Frequence_sport"].mean(),
        "Moyenne eau (litres)":           df["Eau_litres"].mean(),
        "Moyenne énergie":                df["Energie"].mean(),
        "Moyenne caféine (verres/j)":     df["Cafe"].mean(),
    }
    return (
        pd.DataFrame.from_dict(rapport, orient="index", columns=["Moyenne"])
        .round(2)
    )