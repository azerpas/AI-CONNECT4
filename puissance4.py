import numpy as np
import sys
import math
from colors import colors
import random

LIGNES = 6
COLONNES = 7
PLAYER_ONE = 1
PLAYER_AI = 2

def tableau():
	tableau = np.zeros((LIGNES,COLONNES))
	return tableau

# playerPiece is either 1 or 2
def addPiece(tableau, ligne, column, playerPiece):
	tableau[ligne][column] = playerPiece

def estPosition(tableau, column):
	# Checking if position is empty
	return tableau[LIGNES-1][column] == 0
	# - 1 cause array starts at 0 

def getLigne(tableau, column):
	# We check in A SPECIFIC column what's the current line
	for l in range(LIGNES):
		if tableau[l][column] == 0:
			return l 

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
* On cherche les positions valides du tableau
* @return: [] positions valides
"""
def positionsValides(tableau):
	pos = []
	for c in range(COLONNES):
		if estPosition(tableau,c):
			pos.append(c)
	return pos

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

def estTerminal(tableau):
	return isGagnant(tableau, PLAYER_ONE) or isGagnant(tableau, PLAYER_AI) or len(positionsValides(tableau)) == 0

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


tableau = tableau()
print(np.flip(tableau, 0))
gameOver = False
turn = 0

print("TAP 0 at any moment to quit")

while not gameOver:
	if turn == 0:
		print(colors.bg.red, "PLAYER 1", colors.fg.lightgrey)
		col = int(input("Player 1, make your choice: "))
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
		turn = 1


	else:
		#print(colors.bg.blue, "PLAYER 2", colors.fg.lightgrey)				
		#col = int(input("Player 2, make your choice: "))
		#col -= 1
		col, value = minmax(tableau, 3, True)
		#if col == -1:
		##	print(colors.reset)
		#	exit()
		print("AI choosed column: "+str(col+1))
		if estPosition(tableau, col):
			row = getLigne(tableau, col)
			addPiece(tableau, row, col, 2)

			if isGagnant(tableau, 2):
				gameOver = True
				print("AI a gagné!")
		turn = 0

	print(np.flip(tableau, 0))
	print(colors.reset)