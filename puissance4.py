import numpy as np

LIGNES = 6
COLONNES = 7

def tableau():
	tableau = np.zeros((LIGNES,COLONNES))
	return tableau

def currentHauteur(tableau,column): # retourne la ligne (hauteur) du jeu dans une colonne
	for i in range(LIGNES):
		if tableau[i][column] == 0:
			return i

def isTableauCase(tableau,column):
	pass

tableau = tableau()

finJeu = False
turn = 0

while not finJeu:
	if turn == 0:
		play = int(input("PLAYER 1: Please enter column: "))
		turn += 1
	else:
		play = int(input("PLAYER 2: Please enter column: "))
		turn = 0