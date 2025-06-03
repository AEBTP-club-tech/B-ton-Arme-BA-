# Calcul Béton Armé

Une application Python pour le calcul de sections en béton armé selon l'Eurocode 2.

## Description

Cette application permet de calculer les sections d'armatures nécessaires pour des éléments en béton armé soumis à la flexion simple. Elle implémente les méthodes de calcul selon l'Eurocode 2 et offre une interface graphique moderne et intuitive.

## Fonctionnalités

### Calculs disponibles
- Flexion simple
- Calcul des sections d'armatures
- Vérification des sections
- Proposition de barres d'armatures
- Combinaisons de barres possibles

### Caractéristiques du béton
- Calcul de la résistance caractéristique (fck)
- Calcul de la résistance moyenne (fcm)
- Calcul de la résistance de calcul (fcd)
- Calcul de la résistance à la traction (fctm)
- Calcul du module d'élasticité (Ecm)
- Calcul des déformations caractéristiques
- Calcul des coefficients de résistance

### Caractéristiques de l'acier
- Calcul de la limite d'élasticité (fyk)
- Calcul de la résistance de calcul (fyd)
- Calcul des déformations caractéristiques
- Calcul des coefficients de résistance

### Interface graphique
- Interface moderne et intuitive
- Validation des entrées en temps réel
- Affichage des résultats détaillés
- Historique des calculs
- Export des résultats
- Aide contextuelle

## Installation

1. Clonez le dépôt :
```bash
git clone [URL_DU_REPO]
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Dépendances

- Python 3.7+
- tkinter
- customtkinter
- PIL (Pillow)
- pandas

## Utilisation

1. Lancez l'application :
```bash
python BA_GUI.py
```

2. Entrez les données requises :
   - Caractéristiques du béton (fck)
   - Caractéristiques de l'acier (fyk)
   - Dimensions de la section (h, bw, d)
   - Moment de flexion ultime (Mu)
   - Situation (normale ou accidentelle)

3. Cliquez sur "CALCULER" pour obtenir les résultats

## Structure du projet

- `BA.py` : Module principal contenant les classes et fonctions de calcul
- `BA_GUI.py` : Interface graphique de l'application
- `README.md` : Documentation du projet

## Classes principales

### Classe `beton`
Gère les calculs liés au béton :
- Résistances caractéristiques
- Déformations
- Coefficients de résistance

### Classe `acier`
Gère les calculs liés à l'acier :
- Limites d'élasticité
- Déformations
- Coefficients de résistance

### Classe `BetonArmeGUI`
Gère l'interface graphique :
- Saisie des données
- Validation des entrées
- Affichage des résultats
- Gestion de l'historique

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

NOPE

## Auteur

Tsaraloha Christinot 

## Remerciements

- Eurocode 2 pour les méthodes de calcul
- La communauté Python pour les bibliothèques utilisées 