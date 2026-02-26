import pandas as pd
import streamlit as st

URL = "https://docs.google.com/spreadsheets/d/1YwuNz9lKEx8zj3th5hHfI1Z7i2WKUGexfqPnrxn6jiw/export?format=csv"

RENAME_MAP = {
    "Horodateur": "Timestamp",
    "Pour vous, être productif, c'est avant tout...": "Definition_productivite",
    "En moyenne, combien d'heures dormez-vous par nuit?": "Sommeil_moyen",
    "Combien d'heures avez-vous dormi la nuit dernière?": "Sommeil_nuit_derniere",
    "À quelle fréquence avez-vous un sommeil réparateur ?": "Sommeil_reparateur",
    "Comment évalueriez-vous votre hygiène de vie actuelle ?": "Hygiene_vie",
    "À quelle fréquence pratiquez-vous une activité physique (sport, marche active, etc.) ?": "Frequence_sport",
    "En moyenne, combien de litres d'eau bois-tu par jour ?": "Eau_litres",
    "Consommation quotidienne de café ou boissons énergétiques (nombre de tasses/verres)": "Cafe",
    "Avez-vous l'impression d'avoir été efficace dans vos tâches aujourd'hui ?": "Efficacite_aujourdhui",
    "Quel est votre niveau de stress général ces derniers jours ?": "Stress",
    "Niveau moyen de productivité ces 7 derniers jours.": "Productivite_7j",
    "Niveau d'energie aujourd'hui.": "Energie",
    "Quel est votre âge ?": "Age",
    "Quelle est votre situation actuelle ?": "Situation",
}


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(URL)

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace("\u2019", "'", regex=False)
        .str.replace("\u2018", "'", regex=False)
        .str.replace("\u00e9", "e", regex=False)
        .str.replace("é", "e", regex=False)
        .str.lower()
    )

    rename_lower = {k.lower()
                    .replace("\u2019", "'")
                    .replace("\u2018", "'")
                    .replace("é", "e")
                    .replace("è", "e")
                    .replace("ê", "e")
                    .replace("à", "a")
                    .replace("â", "a")
                    .replace("î", "i")
                    .replace("ô", "o")
                    .replace("û", "u")
                    .replace("ç", "c")
                    : v for k, v in RENAME_MAP.items()}

    df.columns = (
        df.columns
        .str.replace("è", "e", regex=False)
        .str.replace("ê", "e", regex=False)
        .str.replace("à", "a", regex=False)
        .str.replace("â", "a", regex=False)
        .str.replace("î", "i", regex=False)
        .str.replace("ô", "o", regex=False)
        .str.replace("û", "u", regex=False)
        .str.replace("ç", "c", regex=False)
    )

    df = df.rename(columns=rename_lower)
    return df