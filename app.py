# LIBRAIRIES
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session 
from tempfile import mkdtemp

#tableau
TABLEAU_VIDE = [[None,None,None], [None, None, None], [None, None, None]]

# FLASK 
app = Flask(__name__) #Initialisation Flask
app.config['SESSION_FILE_DIR'] = mkdtemp() # Stockage temporaire de la session, servira a conserver le tableau de jeu pendant la partie
app.config['SESSION_PERMANENT'] = False # Pas de stockage permanent
app.config['SESSION_TYPE'] = 'filesystem' # Type de session
Session(app) # Lancement de la session

# JEU 
combinaisons = [[[0,0], [0,1], [0,2]], #Lignes
                [[1,0], [1,1], [1,2]],
                [[2,0], [2,1], [2,2]],
                [[0,0], [1,0], [2,0]], #Colonnes
                [[0,1], [1,1], [2,1]],
                [[0,2], [1,2], [2,2]],
                [[0,0], [1,1], [2,2]], #Diagonales
                [[0,2], [1,1], [2,0]]]

def verif_gagnant(tableau):
    # Renvoie X, O ou None respectivement si X a gagné dans le tableau, si O a gagné ou s'il n'y a pas de gagnant.'''
    for combi in combinaisons:
        nbX, nbO = 0, 0
        for case in combi:
            if tableau[case[0]][case[1]]=='X':
                nbX += 1
            elif tableau[case[0]][case[1]]=='O':
                nbO += 1
        if nbX == 3:
            return 'X'
        elif nbO == 3:
            return 'O'
    return 'Aucun'
