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

#JEU FLASK
@app.route('/jouer/<int:ligne>/<int:colonne>')
def jouer(ligne, colonne):
    session['tableau'][ligne][colonne] = session['joueur_actuel'] #On complète le tableau en cours avec le choix du joueur

@app.route('/deuxjoueurs/')
def deuxjoueurs():
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
    session['tableau'] = TABLEAU_VIDE
    session['joueur_actuel'] = 'X'
    return redirect(url_for('deuxjoueurs'))