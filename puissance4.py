import numpy as np
import sys
import math
from colors import colors
import random
import copy

LIGNES = 6
COLONNES = 7
PLAYER_ONE = 1
PLAYER_AI = 2
IA_COMMENTAIRES = ["Tu peux faire mieux!","Mauvais choix...","Tu t'améliores...","C'est bien trop facile","Je m'ennuie","Oh non!","Les humains sont tellement bêtes...","N'essaye pas de me battre","Est-ce que je t'ai déjà dit que j'étais champion du monde?","Tu devrais peut-être te mettre au morpion, tu aurais peut-être plus de chances","C'est tout ce que tu peux faire?","Décevant..."]

'''
ANCHOR function tableau()
REVIEW creating a tab with numpy module
'''
def tableau():
	tableau = np.zeros((LIGNES,COLONNES))
	return tableau

'''
ANCHOR function addPiece() 
REVIEW adding player piece into a position
NOTE 
@tableau 
@ligne
@column
@playerPiece : PLAYER_ONE or PLAYER_AI 
'''
# playerPiece is either 1 or 2
def addPiece(tableau, ligne, column, playerPiece):
	# TODO add color for last piece
	tableau[ligne][column] = playerPiece

'''
ANCHOR function estPosition()
REVIEW checking if position is empty
NOTE 
@tableau
@column
'''
def estPosition(tableau, column):
	# Checking if position is empty
	return tableau[LIGNES-1][column] == 0
	# - 1 cause array starts at 0 

'''
ANCHOR function getLigne()
REVIEW for a given column, check what's the current line available
NOTE 
@tableau
@column
'''
def getLigne(tableau, column):
	# We check in A SPECIFIC column what's the current line
	for l in range(LIGNES):
		if tableau[l][column] == 0:
			return l 

'''
ANCHOR function isGagnant()
REVIEW checking for a winning position
NOTE
@tableau
@playerPiece : PLAYER_ONE or PLAYER_AI 
'''
def isGagnant(tableau, playerPiece):
	for c in range(COLONNES-3): # Check horizontal
		for l in range(LIGNES):
			if tableau[l][c] == playerPiece and tableau[l][c+1] == playerPiece and tableau[l][c+2] == playerPiece and tableau[l][c+3] == playerPiece:
				return True

	for c in range(COLONNES): # Check vertical
		for l in range(LIGNES-3):
			if tableau[l][c] == playerPiece and tableau[l+1][c] == playerPiece and tableau[l+2][c] == playerPiece and tableau[l+3][c] == playerPiece:
				return True

	for c in range(COLONNES-3): # check / diagonale
		for l in range(LIGNES-3):
			if tableau[l][c] == playerPiece and tableau[l+1][c+1] == playerPiece and tableau[l+2][c+2] == playerPiece and tableau[l+3][c+3] == playerPiece:
				return True

	for c in range(COLONNES-3): # check \ diagonale
		for l in range(3, LIGNES):
			if tableau[l][c] == playerPiece and tableau[l-1][c+1] == playerPiece and tableau[l-2][c+2] == playerPiece and tableau[l-3][c+3] == playerPiece:
				return True

"""
ANCHOR positionsValides()
REVIEW we're looking for available positions into the Tab
NOTE 
@tableau
"""
def positionsValides(tableau):
	pos = []
	for c in range(COLONNES):
		if estPosition(tableau,c):
			pos.append(c)
	return pos

"""
ANCHOR scorePos()
REVIEW getting score per position
NOTE 
@tableau
@piece : PLAYERPIECE
"""
def scorePos(tableau, piece):
	score = 0
	puissance = 4
	## Score center column
	center_array = [int(i) for i in list(tableau[:, COLONNES//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(LIGNES):
		row_array = [int(i) for i in list(tableau[r,:])] # Get row as []
		for c in range(COLONNES-3):
			window = row_array[c:c+puissance] # de n° colonne à taille de Puissance (4)
			score += getScore(window, piece)

	## Score Vertical
	for c in range(COLONNES):
		col_array = [int(i) for i in list(tableau[:,c])] # Get colonne as []
		for r in range(LIGNES-3):
			window = col_array[r:r+puissance]
			score += getScore(window, piece)

	## Score posiive sloped diagonal
	for r in range(LIGNES-3):
		for c in range(COLONNES-3):
			window = [tableau[r+i][c+i] for i in range(puissance)]
			score += getScore(window, piece)

	for r in range(LIGNES-3):
		for c in range(COLONNES-3):
			window = [tableau[r+3-i][c+i] for i in range(puissance)]
			score += getScore(window, piece)

	return score

"""
ANCHOR getScore()
REVIEW for given window (col,row,diagonal...) check the score for best result
NOTE 
@window : given array of pieces
@piece : PLAYERPIECE
"""
def getScore(window, piece):
	score = 0
	empty = 0 
	opp_piece = PLAYER_ONE
	if piece == PLAYER_ONE:
		opp_piece = PLAYER_AI

	if window.count(piece) == 4: # biggest score
		score += 100
	elif window.count(piece) == 3 and window.count(empty) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(empty) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(empty) == 1:
		score -= 4

	return score

"""
ANCHOR estTerminal()
REVIEW check if there's a winning pos for either player or no more valid positions
NOTE 
@tableau
"""
def estTerminal(tableau):
	return isGagnant(tableau, PLAYER_ONE) or isGagnant(tableau, PLAYER_AI) or len(positionsValides(tableau)) == 0

"""
ANCHOR minmax()
REVIEW use minmax algorithm to simulate AI thinking and get best play
NOTE 
@tableau
@profondeur : how far does it have to look for best play
@maxJoueur : maxi player chances 
TODO comment inner blocks
FIXME math.inf
"""
def minmax(tableau,profondeur,maxJoueur):
	if profondeur == 0 or estTerminal(tableau):
		if estTerminal(tableau):
			if isGagnant(tableau,PLAYER_AI): # AI
				return (None,100000000)
			if isGagnant(tableau,PLAYER_ONE):
				return (None,-100000000) # None cause no more columns
			else:
				print(str(profondeur) + " " + str(estTerminal))
				return (None,0) # plus de place dans le tableau
		else:
			score = scorePos(tableau,PLAYER_AI)
			return (None,score)
	if maxJoueur:
		val = -math.inf
		col = random.choice(positionsValides(tableau))
		for c in positionsValides(tableau):
			ligne = getLigne(tableau,c)
			copieTab = tableau.copy() # on fait une copie du tableau pour pas vraiment drop une piece
			addPiece(copieTab,ligne,c,PLAYER_AI)
			#print(".")
			newVal = minmax(copieTab,profondeur-1,False)[1] 
			#max(val, minmax(copieTab,profondeur-1,False))
			#print(newVal)
			if newVal > val:
				val = newVal
				col = c
		return col, val
	else:
		val = math.inf
		col = random.choice(positionsValides(tableau))
		for c in positionsValides(tableau):
			ligne = getLigne(tableau,c)
			copieTab = tableau.copy()
			addPiece(copieTab,ligne,c,PLAYER_ONE)
			#print("!")
			newVal = minmax(copieTab,profondeur-1,True)[1]
			#print(newVal)
			if newVal < val:
				val = newVal
				col = c
		return col, val

"""
ANCHOR printTab()
REVIEW printing the tab
"""
def printTab(tableau):
	tab = copy.deepcopy(tableau)
	for l in range(LIGNES):
		for c in range(COLONNES):
			if tab[l][c] == 1:
				print("X",end='')
			elif tab[l][c] == 2:
				print("O",end='')
			else:
				print("|",end='')
		print()
	tab = None 

tableau = tableau()
print(np.flip(tableau, 0))
gameOver = False
turn = 0

print("TAP 0 at any moment to quit")
opponent = int(input("\nPlay against - Player 2 (tap 0) - AI (tap 1): ").replace(" ",""))
if opponent == 1:
	level = int(input("\n[VERY] Easy (tap 0) - Average (tap 1) - Hard (tap 2): ").replace(" ",""))

while not gameOver:
	if turn == 0:
		print()
		print(colors.bg.red, "PLAYER 1", colors.fg.lightgrey)
		col = int(input("Player 1, make your choice: ").replace(" ",""))
		col -= 1 # we sub 1 because user will think of first column as column 1 not column 0
		if col == -1:
			print(colors.reset)
			exit()
		if estPosition(tableau, col): # check if position is available
			row = getLigne(tableau, col)
			addPiece(tableau, row, col, 1)

			if isGagnant(tableau, 1):
				gameOver = True
				print("Player 1 a gagné!")
		else:
			print("Tu vois bien qu'il n'y a plus de place dans cette colonne...")
			continue
		turn = 1


	else:
		if random.randint(0,1):
			print("AI: "+random.choice(IA_COMMENTAIRES))
		if opponent != 0:
			if level == 0:
				col, value = random.choice(positionsValides(tableau)), None
			if level == 1:
				if not random.randint(0,3):
					print("AI: Oh non j'ai fait une erreur!")
					col , value = random.choice(positionsValides(tableau)), None
				else:
					col, value = minmax(tableau,2,True)
			else:
				col, value = minmax(tableau, 5, True)
			print("\nAI choosed column: "+str(col+1))
		else:
			print(colors.bg.blue, "PLAYER 2", colors.fg.lightgrey)				
			col = int(input("Player 2, make your choice: "))
			col -= 1
			if col == -1:
				print(colors.reset)
				exit()
		if estPosition(tableau, col):
			row = getLigne(tableau, col)
			addPiece(tableau, row, col, 2)

			if isGagnant(tableau, 2):
				gameOver = True
				print("AI a gagné!")
		turn = 0

	print(np.flip(tableau, 0))
	print(colors.reset)
	#printTab(tableau)