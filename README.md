# Projet de Cloud Computing - Morpion
### Justin AGUENIER, Matteo CUVELIER, Imane FARES
### ENSAE 2021/2022

## Introduction
L'objectif de ce projet est de développer un jeu de morpion en python, que l'on utilisera sur un navigateur web par le biais d'une application Flask, utilisant des templates HTML mis en forme par une feuille de style CSS.

Ce jeu sera disponible sur DockerHub en tant qu'image Docker et sur Heroku comme site web interactif.

### Stratégies 
- **Niveau 1** : L'ordinateur choisit au hasard parmis les cases non sélectionnées. 

- **Niveau 2** : Pour ce niveau de difficulté, si l’ordinateur est sur le point de gagner, alors il complète la ligne/colonne et gagne. Sinon, il regarde si le joueur est sur le point de gagner et si c’est le cas, il le bloque. Sinon, il choisit une position aléatoire parmi les cases vides restantes.

## Organisation
Organisation du répertoire

## Technologies utilisées
- Python
- Flask, Session Flask