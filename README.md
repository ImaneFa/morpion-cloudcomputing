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
```bash
├── Dockerfile
├── Readme.md
├── app.py : fichier qui génère l'application Flask
├── basic_functions.py : fichier contenant les différentes fonctions nécéssaires au bon déroulement du jeu de morpion
├── requirements.txt : fichier qui déclare les dépendances nécéssaires pour créer l'image Docker
├── static : contient le code CSS utilsé pour styliser la page
│   ├── css
│   │   └── main.css
│   ├── favicon.ico
│   └── favicon_io.zip
├── templates : contient les différentes pages web
│   ├── deuxjoueurs.html : page dédiée au jeu entre amis
│   ├── index.html : page d'accueil
│   └── unjoueur.html : page pour jouer contre différent algorithmes
```

## Technologies utilisées
- Python
- Flask, Session Flask
- Docker, DockerHub
- Heroku

## Disponibilité sur DockerHub

L'image a été poussée sur DockerHub par la commande suivante : ```docker push justinaguenier/morpion-ensae-cloudcomputing```

Afin de rendre l'image disponible, nous avons utilisé la commande suivante : ```docker push justinaguenier/morpion-ensae-cloudcomputing```

- ```docker pull justinaguenier/morpion-ensae-cloudcomputing ```

Commande pour faire tourner l'image 

- ```docker run -p 5000:5000 justinaguenier/morpion-ensae-cloudcomputing```

Une fois la commande effectuée, l'application doit tourner en local sur le port ```5000```

Nous avons également deployé notre application sur le web à l'aide d'Heroku. L'application est disponible via l'url suivant https://morpion-ensae-cloudcomputing.herokuapp.com/


## Déploiement Heroku : 

Voici les différentes étapes mises en oeuvre pour mettre en oeuvre le déploiement sur Heroku : 

- Installation du Heroku CLI à l'aide de Brew sur MacOS. 
- Création de l'application sur le site d'Heroku que l'on nomme ```morpion-ensae```
- Depuis la ligne de commande, on se rend dans le projet à l'aide de la commande ```d``` : 
- ```heroku login``` 
- ```heroku container:login``` 
- ```heroku create morpion-ensae-cloudcomputing```
- ```heroku container:push web -a morpion-ensae-cloudcomputing```
- ```heroku container:release web -a morpion-ensae-cloudcomputing```
- ```heroku open -a morpion-ensae-cloudcomputing```

La webapp est disponible ici : https://morpion-ensae-cloudcomputing.herokuapp.com/