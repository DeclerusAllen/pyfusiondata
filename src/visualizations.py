import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

LABELS = {
    "Sommeil_moyen"        : "Sommeil moyen (h)",
    "Sommeil_nuit_derniere": "Sommeil nuit dernière (h)",
    "Frequence_sport"      : "Fréquence sport",
    "Eau_litres"           : "Hydratation (L/j)",
    "Cafe"                 : "Caféine (verres/j)",
    "Efficacite_aujourdhui": "Efficacité aujourd'hui",
    "Stress"               : "Niveau de stress",
    "Productivite_7j"      : "Productivité 7 jours",
    "Energie"              : "Énergie aujourd'hui",
}

SPORT_LABELS = {
    0: "Jamais",
    1: "1-2×/sem",
    2: "3-4×/sem",
    3: "5+×/sem",
    4: "Quotidien",
}

EFF_MAP = {
    1: "Mou du genou",
    2: "Propre",
    3: "Déterminé",
}

EFF_PALETTE = {
    "Mou du genou": "#E74C3C",
    "Propre":       "#F39C12",
    "Déterminé":    "#2ECC71",
}

FOOTER = (
    "Source : PyFusion  |  "
    "Corrélation de Pearson sur données normalisées  |  "
    "Seuil de significativité : p < 0.05"
)


def _apply_style(fig: plt.Figure, ax: plt.Axes = None) -> None:
    fig.patch.set_facecolor("#FAFAFA")
    if ax:
        ax.set_facecolor("#FAFAFA")


def plot_scatter_sommeil_productivite(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(7, 5))
    _apply_style(fig, ax)

    sns.regplot(
        data=df, x="Sommeil_moyen", y="Productivite_7j", ax=ax,
        color="#5B9BD5",
        scatter_kws={"alpha": 0.7, "s": 80, "edgecolors": "white", "linewidth": 0.5},
        line_kws={"color": "#C0392B", "lw": 2, "linestyle": "--"},
    )

    r, p = stats.pearsonr(df["Sommeil_moyen"], df["Productivite_7j"])
    ax.annotate(
        f"r = {r:.2f}  |  p = {p:.3f}",
        xy=(0.05, 0.92), xycoords="axes fraction",
        fontsize=10, color="#2C3E50",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="lightgray"),
    )

    ax.set_title("Relation Sommeil vs Productivité", fontsize=13, fontweight="bold")
    ax.set_xlabel("Heures de sommeil moyen")
    ax.set_ylabel("Productivité moyenne 7 jours")
    ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    return fig


def plot_distributions(df: pd.DataFrame) -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    _apply_style(fig)

    configs = [
        ("Sommeil_moyen",  "Sommeil moyen (h)",    "#5B9BD5", df["Sommeil_moyen"].mean(),  8,    "Recommandé: 8h"),
        ("Stress",         "Niveau de stress",      "#E74C3C", df["Stress"].mean(),          None, None),
        ("Energie",        "Énergie aujourd'hui",   "#2ECC71", df["Energie"].mean(),         None, None),
    ]

    for ax, (col, title, color, mean_val, ref_val, ref_label) in zip(axes, configs):
        sns.histplot(data=df, x=col, kde=True, ax=ax, color=color, alpha=0.75)
        ax.axvline(mean_val, color="#2C3E50", linestyle="--", lw=1.8,
                   label=f"Moy: {mean_val:.1f}")
        if ref_val:
            ax.axvline(ref_val, color="#27AE60", linestyle=":", lw=1.5, label=ref_label)
        ax.set_title(title, fontweight="bold")
        ax.set_facecolor("#FAFAFA")
        ax.legend(fontsize=8)

    fig.suptitle("Distribution des variables clés", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def plot_sommeil_efficacite_kde(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    _apply_style(fig, ax)

    df_plot = df.copy()
    df_plot["Efficacité"] = df_plot["Efficacite_aujourdhui"].map(EFF_MAP)

    sns.kdeplot(
        data=df_plot, x="Sommeil_moyen",
        hue="Efficacité", fill=True, alpha=0.4, ax=ax,
        palette=EFF_PALETTE,
    )
    ax.set_title("Distribution du sommeil selon l'efficacité", fontsize=13, fontweight="bold")
    ax.set_xlabel("Heures de sommeil moyen")
    ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    return fig


def plot_sport_productivite_energie(df: pd.DataFrame) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    _apply_style(fig)

    df_plot = df.copy()
    df_plot["Sport_label"] = df_plot["Frequence_sport"].map(SPORT_LABELS)
    order = list(SPORT_LABELS.values())

    sns.boxplot(
        data=df_plot, x="Sport_label", y="Productivite_7j",
        order=order, ax=axes[0], palette="Blues",
    )
    axes[0].set_title("Sport → Productivité 7j", fontweight="bold")
    axes[0].set_xlabel("Fréquence de sport")
    axes[0].set_ylabel("Productivité 7 jours")
    axes[0].set_facecolor("#FAFAFA")

    sns.barplot(
        data=df_plot, x="Sport_label", y="Energie",
        order=order, ax=axes[1], palette="Greens", errorbar="sd",
    )
    axes[1].set_title("Sport → Énergie", fontweight="bold")
    axes[1].set_xlabel("Fréquence de sport")
    axes[1].set_ylabel("Énergie aujourd'hui")
    axes[1].set_facecolor("#FAFAFA")

    plt.tight_layout()
    return fig


def plot_definition_productivite(df: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    _apply_style(fig, ax)

    order = (
        df.groupby("Definition_productivite")["Productivite_7j"]
        .mean()
        .sort_values(ascending=False)
        .index
    )

    sns.barplot(
        data=df, x="Definition_productivite", y="Productivite_7j",
        order=order, ax=ax, palette="coolwarm", errorbar="sd",
    )
    ax.set_title(
        "Productivité moyenne selon la définition de la productivité",
        fontsize=13, fontweight="bold",
    )
    ax.set_xlabel("")
    ax.set_ylabel("Productivité 7 jours (moy.)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha="right", fontsize=9)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()
    return fig


def plot_pairplot(df: pd.DataFrame) -> plt.Figure:
    cols = ["Sommeil_moyen", "Stress", "Energie", "Productivite_7j"]
    df_plot = df[cols].copy()
    df_plot["Efficacité"] = df["Efficacite_aujourdhui"].map(EFF_MAP)

    g = sns.pairplot(
        df_plot, hue="Efficacité",
        palette=EFF_PALETTE,
        plot_kws={"alpha": 0.7},
        diag_kind="kde",
    )
    g.figure.suptitle(
        "Pairplot — Sommeil, Stress, Énergie, Productivité",
        y=1.02, fontsize=13, fontweight="bold",
    )
    return g.figure


def plot_correlation(corr: pd.DataFrame, df_normalized: pd.DataFrame) -> plt.Figure:
    corr_labeled = corr.rename(index=LABELS, columns=LABELS)

    num_data = df_normalized[list(LABELS.keys())]
    p_values = num_data.apply(
        lambda col_a: num_data.apply(
            lambda col_b: stats.pearsonr(col_a, col_b)[1]
        )
    ).rename(index=LABELS, columns=LABELS)

    mask_upper = np.triu(np.ones_like(corr_labeled, dtype=bool), k=1)
    mask_sig   = (p_values >= 0.05) & ~mask_upper

    fig, ax = plt.subplots(figsize=(13, 11), facecolor="#FAFAFA")

    sns.heatmap(
        corr_labeled, ax=ax, mask=mask_upper,
        annot=True, fmt=".2f", cmap="coolwarm",
        center=0, vmin=-1, vmax=1,
        linewidths=0.6, linecolor="white",
        annot_kws={"size": 10, "weight": "bold"},
        square=True,
        cbar_kws={"shrink": 0.75, "label": "Coefficient de Pearson (r)"},
    )

    annot_ns        = corr_labeled.copy().astype(str)
    annot_ns[:]     = ""
    annot_ns[mask_sig] = "ns"

    sns.heatmap(
        corr_labeled, ax=ax, mask=~mask_sig,
        annot=annot_ns, fmt="", cmap=["none"],
        linewidths=0, square=True, cbar=False,
        annot_kws={"size": 7, "color": "gray", "style": "italic"},
    )

    ax.set_title(
        "Étude de corrélation — Santé & Productivité\n"
        "Lien entre habitudes de vie (sommeil, sport, hydratation) et productivité / stress",
        fontsize=14, fontweight="bold", pad=20, loc="left",
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)

    patches = [
        mpatches.Patch(color="#d73027", label="Corrélation positive forte (→ 1)"),
        mpatches.Patch(color="#4575b4", label="Corrélation négative forte (→ -1)"),
        mpatches.Patch(color="#f7f7f7", label="Pas de lien (→ 0)"),
        mpatches.Patch(facecolor="white", edgecolor="gray",
                       label="ns = non significatif (p ≥ 0.05)"),
    ]
    ax.legend(
        handles=patches, loc="upper right",
        bbox_to_anchor=(1.32, 1.02), fontsize=9,
        frameon=True, framealpha=0.9, edgecolor="lightgray",
    )

    fig.text(0.5, 0.01, FOOTER, ha="center", fontsize=8, color="gray", style="italic")

    plt.tight_layout()
    return fig
