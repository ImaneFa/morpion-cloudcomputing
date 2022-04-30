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