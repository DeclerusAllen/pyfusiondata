# [![Ouvrir l’application en ligne](https://img.shields.io/badge/🚀%20Voir%20PyFusion%20en%20ligne-Streamlit-green?style=for-the-badge)](https://pyfusiondata.streamlit.app/)
# Santé & Productivité 📊

Bienvenue sur ce projet d’analyse interactive des liens entre habitudes de vie et productivité !  
Ce tableau de bord, développé avec Streamlit, permet d’explorer comment le sommeil, le sport, l’hydratation ou encore le stress influencent notre efficacité au quotidien.

## 🌱 Objectif

L’objectif est simple :  
Mieux comprendre, grâce à la donnée, quels facteurs de santé impactent le plus notre sentiment de productivité et d’énergie.

## 🔍 Fonctionnalités principales

- **Chargement automatique des données** (Google Sheets, anonymes, mises à jour toutes les 5 min)
- **Nettoyage et normalisation** des réponses (gestion des valeurs manquantes, conversion des unités…)
- **Visualisations interactives** :
  - Nuages de points (sommeil vs productivité)
  - Distributions et heatmaps de corrélation
  - Analyse croisée sport, énergie, efficacité
  - Pairplots et analyses multivariées
- **KPIs dynamiques** : sommeil moyen, stress, énergie, productivité, nombre de répondants
- **Rapport statistique** et synthèse des conclusions

## 🛠️ Technologies utilisées

- Python 3.13+
- Streamlit
- Pandas, NumPy
- Matplotlib, Seaborn, SciPy

## 🚀 Lancer l’application

1. Installe les dépendances :
	```sh
	pip install -r requirements.txt
	```
	ou avec le pyproject.toml :
	```sh
	pip install .
	```

2. Lance le dashboard Streamlit :
	```sh
	streamlit run main.py
	```

3. Ouvre le lien local affiché dans ton navigateur.

## 📊 Structure du projet

- `main.py` : point d’entrée Streamlit, navigation et affichage
- `src/data_loader.py` : chargement et renommage des données
- `src/preprocessing.py` : nettoyage, normalisation, mapping des réponses
- `src/visualizations.py` : toutes les fonctions de graphiques
- `src/components.py` : composants réutilisables (KPIs, tableaux, headers)
- `pyproject.toml` : dépendances et configuration du projet

## 📈 Exemple de questions analysées

- Dormir plus = être plus productif ?
- Le sport régulier réduit-il le stress ?
- L’hydratation influence-t-elle l’énergie ?
- Quels facteurs sont les plus corrélés à la productivité ?

## 🙌 Remerciements

Merci à tous les participants pour leurs réponses anonymes et à l’équipe pédagogique pour l’inspiration !


---

## 🗂️ Architecture du code

Voici l’organisation du projet :

```
├── main.py                # Point d'entrée Streamlit, logique de navigation et affichage principal
├── pyproject.toml         # Dépendances et configuration du projet Python
├── README.md              # Documentation du projet
├── data/
│   └── data.csv           # Jeu de données local (optionnel, sinon Google Sheets)
├── src/
│   ├── __init__.py        # Fichier d'initialisation du module
│   ├── components.py      # Composants Streamlit réutilisables (KPIs, tableaux, headers)
│   ├── data_loader.py     # Chargement et renommage des données depuis Google Sheets
│   ├── preprocessing.py   # Nettoyage, normalisation, mapping des réponses
│   ├── visualizations.py  # Fonctions de visualisation (graphiques, heatmaps, etc.)
│   └── test.ipynb         # Notebook de tests et d'exploration (optionnel)
└── .venv/                 # (optionnel) Environnement virtuel Python
```

### Rôle des principaux fichiers/dossiers

- **main.py** : Orchestration de l’application, navigation entre les pages, affichage des sections.
- **src/data_loader.py** : Téléchargement et préparation des données brutes.
- **src/preprocessing.py** : Nettoyage, normalisation, conversion des réponses, création de rapports statistiques.
- **src/visualizations.py** : Toutes les fonctions de graphiques (scatter, heatmap, pairplot, etc.).
- **src/components.py** : Fonctions pour afficher des KPIs, tableaux, titres, etc. dans Streamlit.
- **data/** : Contient éventuellement un export local des données (non versionné si sensible).
- **pyproject.toml** : Liste des dépendances et configuration du projet Python.
- **README.md** : Ce fichier, pour comprendre et utiliser le projet.

N’hésite pas à explorer chaque fichier pour voir comment les données sont traitées et visualisées !