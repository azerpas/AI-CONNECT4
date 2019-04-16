import numpy as np

def board():
	board = np.zeros((6,7))
	return board

board = board()

finJeu = False
turn = 0

while not finJeu:
	if turn == 0:
		play = input("PLAYER 1: Please enter column: ")
		turn += 1
	else:
		play = input("PLAYER 2: Please enter column: ")
		turn = 0