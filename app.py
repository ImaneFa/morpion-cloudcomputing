# LIBRAIRIES
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session 
from tempfile import mkdtemp
import os
from random import choice

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

coins = [[0,0], [0,2], [2,0], [2,2]]

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


def nbcasesvides(tableau):
    res = 0
    for ligne in tableau:
        for element in ligne:
            if element is None:
                res += 1
    return res

# STRATEGIES DES BOTS
def bot(tableau, strat):
    #Fonction de réponse générale à l'action du joueur en mode 1 joueur
    if strat==1: #Réponse aléatoire
        return bot_strategie_1(tableau)
    elif strat==2:
        return bot_strategie_2(tableau)
    elif strat==3:
        return bot_strategie_3(tableau)


def bot_strategie_1(tableau):
    """
    Stratégie de réponse aléatoire parmi les cases vides
    """
    #Etablissement de la liste des cases vides
    cases_vides = []
    for i in range(3):
        for j in range(3):
            if tableau[i][j] is None:
                cases_vides.append([i,j])
    #On choisi aléatoirement une case vide
    return choice(cases_vides)


def bot_strategie_2(tableau):
    # Si on est sur le point de gagner, compléter la ligne
    for position in combinaisons:
        groupe = (tableau[position[0][0]][position[0][1]], 
                    tableau[position[1][0]][position[1][1]],
                    tableau[position[2][0]][position[2][1]])
        if groupe.count('O') == 2 and groupe.count(None) == 1: 
            indice_nouvellecase = groupe.index(None) 
            return position[indice_nouvellecase]
        
    # Si le joueur est sur le point de gagner, le bloquer     
    for position in combinaisons:
        groupe = (tableau[position[0][0]][position[0][1]], 
                    tableau[position[1][0]][position[1][1]],
                    tableau[position[2][0]][position[2][1]])
        if groupe.count('X') == 2 and groupe.count(None) == 1: 
            indice_nouvellecase = groupe.index(None) 
            return position[indice_nouvellecase]
      
    return bot_strategie_1(tableau)


def bot_strategie_3(tableau):
    # Si on est sur le point de gagner, compléter la ligne
    for position in combinaisons:
        groupe = (tableau[position[0][0]][position[0][1]], 
            tableau[position[1][0]][position[1][1]],
            tableau[position[2][0]][position[2][1]])
        if groupe.count('O') == 2 and groupe.count(None) == 1: 
            indice_nouvellecase = groupe.index(None) 
            return position[indice_nouvellecase]
    # Si le joueur est sur le point de gagner, le bloquer     
    for position in combinaisons:
        groupe = (tableau[position[0][0]][position[0][1]], 
                tableau[position[1][0]][position[1][1]],
                tableau[position[2][0]][position[2][1]])
        if groupe.count('X') == 2 and groupe.count(None) == 1: 
            indice_nouvellecase = groupe.index(None) 
            return position[indice_nouvellecase]
    # Si on s'est déjà positionné sur 0 ou 1 case, on prend une nouvelle case avec en priorité les coins, puis le centre puis aléatoire sur le reste       
    if tableau[0].count('O') + tableau[1].count('O') + tableau[2].count('O') <= 1 : 
        for coin in coins:
            if tableau[coin[0]][coin[1]]==None:
                return coin
        if tableau[1][1]==None:
            return [1,1]
        else:
            return reponse_aleatoire(tableau)
     
    # Checker les cases vides restantes
    cases_vides = []

    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j]== None:
                cases_vides.append([i,j])
                
    # Stratégie 1
    # Si on s'est déjà positionné sur 2 cases ou plus
    if tableau[0].count('O') + tableau[1].count('O') + tableau[2].count('O') > 1 : 
        # Si on a les coins en haut à gauche et en haut à droite et si un des 2 autres coins est vide, on se place dessus
        if tableau[coins[0][0]][coins[0][1]]=='O' and tableau[coins[1][0]][coins[1][1]]=='O':
            if coins[2] in cases_vides:
                return coins[2]
            elif coins[3] in cases_vides:
                return coins[3]
        # Si on a les coins en haut à gauche et en bas à gauche et si un des 2 autres coins est vide, on se place dessus
        elif tableau[coins[0][0]][coins[0][1]]=='O' and tableau[coins[2][0]][coins[2][1]]=='O':
            if coins[1] in cases_vides:
                return coins[1]
            elif coins[3] in cases_vides:
                return coins[3]
        # Si on a les coins en haut à gauche et en bas à droite et si un des 2 autres coins est vide, on se place dessus
        elif tableau[coins[0][0]][coins[0][1]]=='O' and tableau[coins[3][0]][coins[3][1]]=='O':
            if coins[1] in cases_vides:
                return coins[1]
            elif coins[2] in cases_vides:
                return coins[2]
        # Si on a les coins en haut à droite et en bas à gauche et si un des 2 autres coins est vide, on se place dessus
        elif tableau[coins[1][0]][coins[1][1]]=='O' and tableau[coins[2][0]][coins[2][1]]=='O':
            if coins[0] in cases_vides:
                return coins[0]
            elif coins[3] in cases_vides:
                return coins[3]
        # Si on a les coins en haut à droite et en bas à droite et si un des 2 autres coins est vide, on se place dessus
        elif tableau[coins[1][0]][coins[1][1]]=='O' and tableau[coins[3][0]][coins[3][1]]=='O':
            if coins[0] in cases_vides:
                return coins[0]
            elif coins[2] in cases_vides:
                return coins[2]        
        # Si on a les coins en bas à gauche et en bas à droite et si un des 2 autres coins est vide, on se place dessus
        elif tableau[coins[2][0]][coins[2][1]]=='O' and tableau[coins[3][0]][coins[3][1]]=='O':
            if coins[0] in cases_vides:
                return coins[0]
            elif coins[1] in cases_vides:
                return coins[1]  
            
        # Stratégie 2
        # Si on a le centre et un coin et qu'un autre coin est libre, se placer dessus
        for i in range(4):
            if tableau[1][1]=='O' and tableau[coins[i][0]][coins[i][1]]=='O':
                for j in range(4):
                    if tableau[coins[j][0]][coins[j][1]]==None: 
                        return coins[j]
                    
        # Stratégie 3 + 4
        # Si on a la case (1,0) et la case (2,1) alors prendre (1,1) ou (2,0) si libres
        if tableau[1][0]=='O' and tableau[2][1]=='O':
            if tableau[1][1]==None:
                return [1,1]
            elif tableau[2][0]==None:
                return [2,0]
        # Si on a la case (2,1) et la case (1,2) alors prendre (1,1) ou (2,2) si libres
        elif tableau[2][1]=='O' and tableau[1][2]=='O':
            if tableau[1][1]==None:
                return [1,1]
            elif tableau[2][2]==None:
                return [2,2]
        # Si on a la case (1,2) et la case (0,1) alors prendre (1,1) ou (0,2) si libres
        elif tableau[1][2]=='O' and tableau[0][1]=='O':
            if tableau[1][1]==None:
                return [1,1]
            elif tableau[2][0]==None:
                return [0,2]
        # Si on a la case (0,1) et la case (1,0) alors prendre (1,1) ou (0,0) si libres
        elif tableau[0][1]=='O' and tableau[1][0]=='O':
            if tableau[1][1]==None:
                return [1,1]
            elif tableau[2][0]==None:
                return [0,0]
    
        # Sinon, on complète en priorité les coins, puis le centre puis de manière aléatoire sur le reste
        else:
            for coin in coins:
                if tableau[coin[0]][coin[1]]==None:
                    return coin
            if tableau[1][1]==None:
                return [1,1]
            else:
                return bot_strategie_1(tableau)


#JEU FLASK
@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/jouer/<int:ligne>/<int:colonne>')
def jouer(ligne, colonne):
    session['tableau'][ligne][colonne] = session['joueur_actuel'] #On complète le tableau en cours avec le choix du joueur


@app.route('/retouraccueil/')
def retouraccueil():
    session['tableau'] = TABLEAU_VIDE
    session['joueur_actuel'] = 'X'
    return redirect(url_for('accueil'))


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


@app.route('/unjoueur/<int:strat>')
def unjoueur(strat):
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
    #On change la case jouée
    session['tableau'][ligne][colonne] = 'X'
    if verif_gagnant(session['tableau']) == 'Aucun' and nbcasesvides(session['tableau'])>0:
        reponse = bot(session['tableau'], strat=session['strat']) #Appel d'une fonction de stratégie 
        session['tableau'][reponse[0]][reponse[1]] = 'O'
    return redirect(url_for('unjoueur', strat=session['strat']))


@app.route('/unjoueur/raz')
def razunjoueur():
    session['tableau'] = TABLEAU_VIDE
    session['joueur_actuel'] = 'X'
    return redirect(url_for('unjoueur', strat=session['strat']))