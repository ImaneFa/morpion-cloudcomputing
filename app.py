#############################################
##### CLOUD COMPUTING - ENSAE 2021/2022 #####
#############################################

## GROUPE 3 ##
# - Justin AGUENIER
# - Matteo CUVELIER
# - Imane FARES

#Nous réalisons ici un jeu de morpion en flask

################
## LIBRAIRIES ##
################

from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session 
from tempfile import mkdtemp
from basic_functions import *
import os

####################
## TABLEAU DE JEU ##
#################### 
# On définit un tableau de jeu sous forme de liste de liste
TABLEAU_VIDE = [[None,None,None], [None, None, None], [None, None, None]]

#########################
## CONFIGURATION FLASK ##
#########################
app = Flask(__name__) #Initialisation Flask
app.config['SESSION_FILE_DIR'] = mkdtemp() # Stockage temporaire de la session, servira a conserver le tableau de jeu pendant la partie
app.config['SESSION_PERMANENT'] = False # Pas de stockage permanent
app.config['SESSION_TYPE'] = 'filesystem' # Type de session
Session(app) # Lancement de la session

#################
## JEU - FLASK ##
#################


@app.route('/')
def accueil():
    """
    Accueil et choix du mode de jeu (liens html)
    @return:
    """
    return render_template('index.html')


@app.route('/jouer/<int:ligne>/<int:colonne>')
def jouer(ligne, colonne):
    """
    Fonction de jeu : une action (complétion du tableau de jeu)
    @param ligne:
    @param colonne:
    @return:
    """
    session['tableau'][ligne][colonne] = session['joueur_actuel'] #On complète le tableau en cours avec le choix du joueur


@app.route('/retouraccueil/')
def retouraccueil():
    """
    Retour à l'accueil
    @return:
    """
    session['tableau'] = TABLEAU_VIDE
    session['joueur_actuel'] = 'X'
    return redirect(url_for('accueil'))


@app.route('/deuxjoueurs/')
def deuxjoueurs():
    """
    MODE 1 : 2 JOUEURS
    La fonction affiche la situation actuelle stockée dans la session sous session['tableau']
    @return:
    """
    #On commence par initialiser en chargeant le tableau vide, le joueur X commence, si c'est le début de la partie
    if 'tableau' not in session:
        session['tableau'] = TABLEAU_VIDE
        session['joueur_actuel'] = 'X'
    #On actualise la vairiable gagnat qui contient Aucun, X ou O (initialisée à Aucun)
    gagnant = verif_gagnant(session['tableau'])
    #Affichage dans le navigateur
    return render_template('deuxjoueurs.html', joueur=session['joueur_actuel'], jeu=session['tableau'], gagnant=gagnant)


@app.route('/deuxjoueurs/jouerdeuxjoueurs/<int:ligne>/<int:colonne>')
def jouerdeuxjoueurs(ligne, colonne):
    """
    Jouer une case
    @param ligne:
    @param colonne:
    @return:
    """
    #On change la case jouée
    session['tableau'][ligne][colonne] = session['joueur_actuel']
    #On chage le joueur en cours
    if session['joueur_actuel'] == 'X':
        session['joueur_actuel'] = 'O'
    else: 
        session['joueur_actuel'] = 'X'
    return redirect(url_for('deuxjoueurs'))


@app.route('/deuxjoueurs/raz')
def razdeuxjoueurs():
    """
    Nouvelle partie
    @return:
    """
    session['tableau'] = TABLEAU_VIDE
    session['joueur_actuel'] = 'X'
    return redirect(url_for('deuxjoueurs'))


@app.route('/unjoueur/<int:strat>')
def unjoueur(strat):
    """
    MODE 2 : UN JOUEUR
    @param strat:
    @return:
    """
    #On commence par initialiser en chargeant le tableau vide, le joueur X commence, si c'est le début de la partie
    if 'tableau' not in session:
        session['tableau'] = TABLEAU_VIDE
    #On définit la strategie
    session['strat'] = strat
    #On actualise la vairiable gagnat qui contient Aucun, X ou O (initialisée à Aucun)
    gagnant = verif_gagnant(session['tableau'])
    #Affichage dans le navigateur
    return render_template('unjoueur.html', joueur='X', jeu=session['tableau'], gagnant=gagnant, strat=session['strat'])


@app.route('/unjoueur/jouer/<int:ligne>/<int:colonne>')
def jouerunjoueur(ligne, colonne):
    """
    Jouer une case d'utilisateur et une case du bot si le joueur n'a pas gagné
    @param ligne:
    @param colonne:
    @return:
    """
    #On change la case jouée
    session['tableau'][ligne][colonne] = 'X'
    if verif_gagnant(session['tableau']) == 'Aucun' and nbcasesvides(session['tableau'])>0:
        reponse = bot(session['tableau'], strat=session['strat']) #Appel d'une fonction de stratégie 
        session['tableau'][reponse[0]][reponse[1]] = 'O'
    return redirect(url_for('unjoueur', strat=session['strat']))


@app.route('/unjoueur/raz')
def razunjoueur():
    """
    Nouvelle partie
    @return:
    """
    session['tableau'] = TABLEAU_VIDE
    session['joueur_actuel'] = 'X'
    return redirect(url_for('unjoueur', strat=session['strat']))