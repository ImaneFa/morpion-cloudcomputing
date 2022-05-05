# Projet de Cloud Computing - Morpion
### Justin AGUENIER, Matteo CUVELIER, Imane FARES
### ENSAE 2021/2022

## Introduction
L'objectif de ce projet est de développer un jeu de morpion en python, que l'on utilisera sur un navigateur web par le biais d'une application Flask, utilisant des templates HTML mis en forme par une feuille de style CSS.

Ce jeu sera disponible sur DockerHub en tant qu'image Docker et sur Heroku comme site web interactif.

### Stratégies 
Le jeu pourra se faire à deux joueurs (qui joueront successivement) ou avec un joueur qui affrontera l'ordinateur selon 3 niveaux de difficultés (croissantes) :

- **Niveau 1** : L'ordinateur choisit au hasard parmis les cases non sélectionnées. 

- **Niveau 2** : Pour ce niveau de difficulté, si l’ordinateur est sur le point de gagner, alors il complète la ligne/colonne et gagne. Sinon, il regarde si le joueur est sur le point de gagner et si c’est le cas, il le bloque. Sinon, il choisit une position aléatoire parmi les cases vides restantes.

- **Niveau 3** : Pour ce troisième niveau de difficulté, nous nous sommes inspirés des stratégies développées sur https://www.instructables.com/Winning-tic-tac-toe-strategies/. 
    - Tout d’abord, si l’ordinateur est sur le point de gagner, alors il complète la ligne et gagne. Sinon, il regarde si le joueur est sur le point de gagner et si c’est le cas, il le bloque.
    - Sinon, si l’ordinateur s’est déjà positionné sur 0 ou 1 case, alors il se place sur l’une des cases vides restantes en priorisant les coins, puis le centre, sinon il choisit une position aléatoire parmi les cases vides restantes.
    - Si l’ordinateur s’est déjà positionné sur 2 cases ou plus, alors :
        - S’il s‘est déjà positionné sur 2 coins et qu’un troisième est encore vide, il se place dessus
        - Sinon, s’il s’est déjà positionné sur le centre ainsi que sur un coin et qu’un autre coin est encore vide, il se place dessus.
        - Sinon, s’il s’est déjà positionné sur une case milieu de ligne et une case milieu de colonne, alors il se positionne sur la case adjacente ou sur le centre selon leur disponibilité
    - Si aucune des précédentes stratégies n’a pu être appliquée, alors l’ordinateur se place sur l’une des cases vides restantes en priorisant les coins, puis le centre puis une case aléatoire.

## Organisation
Organisation du répertoire

## Technologies utilisées
- Python
- Flask, Session Flask