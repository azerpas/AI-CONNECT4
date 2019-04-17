import numpy as np
import sys
import math
from colors import colors

LIGNES = 6
COLONNES = 7

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
		turn = 1


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
		turn = 0

	print(np.flip(tableau, 0))
	print(colors.reset)