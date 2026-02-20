[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/85yijL-Y)
## Sujet 1 : Analyse des habitudes de consommation

**Le concept :** Les étudiants créent un formulaire pour suivre les dépenses quotidiennes ou la consommation de ressources (café, temps d'écran, transport) au sein de la classe.

* **Collecte :** Formulaire avec champs : Date, Catégorie (Alimentation, Transport, Loisirs), Montant, et Sentiment (échelle de 1 à 5).
* **Analyse avec NumPy/Pandas :**
* Calculer la dépense moyenne par jour.
* Grouper les données par catégorie avec Pandas pour voir où part l'argent.
* Identifier le jour de la semaine le plus "coûteux".

* **Visualisation (Matplotlib) :**
* **Diagramme circulaire (Pie Chart) :** Répartition des dépenses par catégorie.
* **Histogramme :** Distribution des montants dépensés.

---

## Sujet 2 : Évaluation des performances et quiz interactif

**Le concept :** Créer un quiz de connaissances générales ou techniques. Les données collectées servent à analyser le niveau global des participants.

* **Collecte :** Formulaire type "QCM". Les colonnes Google Sheet contiendront les réponses (vraies/fausses).
* **Analyse avec NumPy/Pandas :**
* Transformer les réponses textuelles en valeurs numériques (1 pour correct, 0 pour incorrect).
* Utiliser NumPy pour calculer l'écart-type (`std()`) des scores pour mesurer l'homogénéité du groupe.
* Calculer le taux de réussite par question pour identifier les sujets les plus difficiles.


* **Visualisation (Matplotlib) :**
* **Bar Chart :** Taux de réussite pour chaque question.
* **Boxplot (Boîte à moustaches) :** Pour visualiser la dispersion des notes et les valeurs aberrantes (outliers).

---

## Sujet 3 : Étude de corrélation : Santé et Productivité

**Le concept :** Explorer s'il existe un lien entre des facteurs de vie (heures de sommeil, sport) et le sentiment de productivité ou de stress.

* **Collecte :** Formulaire anonyme demandant : Heures de sommeil, nombre de verres d'eau, minutes de sport, et niveau de stress ressenti (0 à 10), ect.
* **Analyse avec NumPy/Pandas :**
* Nettoyage des données (gestion des valeurs manquantes ou aberrantes).
* Calculer la matrice de corrélation avec `pandas.corr()`.
* Utiliser NumPy pour normaliser les données (mettre toutes les valeurs sur une échelle de 0 à 1).

* **Visualisation (Matplotlib) :**
* **Scatter Plot (Nuage de points) :** Afficher l'évolution de la productivité en fonction des heures de sommeil.
* **Heatmap (Carte de chaleur) :** Représenter la matrice de corrélation pour voir quels facteurs sont liés entre eux.