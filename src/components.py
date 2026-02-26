import streamlit as st
import pandas as pd


def kpi_row(df: pd.DataFrame) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Sommeil moyen",   f"{df['Sommeil_moyen'].mean():.1f}h")
    col2.metric("Stress moyen",    f"{df['Stress'].mean():.1f} / 5")
    col3.metric("Energie moyenne", f"{df['Energie'].mean():.1f} / 5")
    col4.metric("Productivite 7j", f"{df['Productivite_7j'].mean():.1f} / 5")
    col5.metric("Repondants",      str(len(df)))


def section_header(title: str, description: str = "") -> None:
    st.title(title)
    if description:
        st.markdown(f"_{description}_")
    st.divider()


def rapport_table(rapport_df: pd.DataFrame) -> None:
    st.dataframe(
        rapport_df.style
        .format({"Moyenne": "{:.2f}"})
        .background_gradient(cmap="Blues", subset=["Moyenne"]),
        use_container_width=True,
    )