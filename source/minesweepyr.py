import numpy as np
import random
import sys
from sys import platform as _platform
import os

GEN_SEED = int(random.SystemRandom().random() * 100)
NUM_ROWS   = 10
NUM_COLS   = 10
NUM_MINES  = 10

def initialize(seed):
	random.seed(seed)
	grid_linear = ([True] * NUM_MINES) + \
	[False] * (NUM_ROWS * NUM_COLS - NUM_MINES)
	random.shuffle(grid_linear)
	grid = np.array(grid_linear)
	grid = grid.reshape(NUM_ROWS, NUM_COLS)
	return grid

def print_full_board(grid):
	global NUM_ROWS
	global NUM_COLS

	board = "\n    | "
	horizon = range(1, NUM_COLS + 1)
	for i in horizon:
		m = len(str(i))
		space = " " * (2 - m)
		board += str(i) + space
	board += "\n"
	for i in board:
		board += "-"
	board += "\n"

	# (NUM_ROWS, NUM_COLS) = grid.shape
	for r in range(NUM_ROWS):
		m = len(str(r + 1))
		space = " " * (4 - m)
		board += str(r + 1) + space + "| "
		# board += str(r + 1) + " | "
		for c in range(NUM_COLS):
			board += str(grid[r, c]) + " "
		board += "\n"
	print("\r" + board)

def reveal_board_cell(reveal_grid, grid, row, col):

	adj_mines = 0
	mine = "M"

	if grid[row][col] == True:
		reveal_grid[row, col] = mine
		if "M" in reveal_grid:
			for r in range(NUM_ROWS):
				for c in range(NUM_COLS):
					if(grid[r,c] == True):
						reveal_grid[r,c] = "M"
					else:
						reveal_grid[r,c] = " "
			return reveal_grid

	for r in range (row - 1, row + 2):
			for c in range (col - 1, col + 2):
				if (r >= 0 and r < NUM_ROWS and c >= 0 and c < NUM_COLS):
					if grid[r][c] == True:
						adj_mines += 1
	reveal_grid[row, col] = adj_mines

	if adj_mines == 0:
		for r in range (row - 1, row + 2):
				for c in range (col - 1, col + 2):
					if (r >= 0 and r < NUM_ROWS and c >= 0 and c < NUM_COLS):
						reveal_grid[r, c] = " "

	return reveal_grid

def clear_sys():
	if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
		os.system('clear')
	elif _platform == "win32" or _platform == "win64":
		os.system('cls')

def main():
	global NUM_ROWS
	global NUM_COLS

	if (len(sys.argv) > 1):
		seed = int(sys.argv[1])
	else:
		seed = GEN_SEED

	clear_sys()

	init_board = "\n    | "
	horizon = range(1, NUM_COLS + 1)
	vertice = range(1, NUM_ROWS + 1)
	for i in horizon:
		m = len(str(i))
		space = " " * (2 - m)
		init_board += str(i) + space
	init_board += "\n"
	for i in init_board:
		init_board += "-"
	init_board += "\n"
	for i in vertice:
		m = len(str(i))
		space = " " * (4 - m)
		init_board += str(i) + space + "| " + (". " * NUM_COLS) + "\n"
	print(init_board)

	input_history = []
	mines_grid = initialize(seed)
	cell = "."
	cells = ([[cell] * (NUM_ROWS * NUM_COLS)])
	cells_array = np.array((cells))
	cells_array = cells_array.reshape(NUM_ROWS, NUM_COLS)

	continue_game = True
	while continue_game == True:
		try:
			row = int(input("row: ")) - 1
			col = int(input("col: ")) - 1
		except:
			print("\ninvalid input - exiting game. ")
			break

		if row + 1 > NUM_ROWS or row + 1 <= 0 or col + 1 > NUM_COLS or col + 1 <= 0:
			print("\ninvalid selection - try again. ")
			continue
		if (str(row) + str(col)) in input_history:
			print("\nalready selected - try again. ")
			continue
		input_history.append(str(row) + str(col))

		clear_sys()

		cells_array = reveal_board_cell(cells_array, mines_grid, row, col)
		board = print_full_board(cells_array)

		if "M" in cells_array:
			exit("\ngame over :( ")

		cell_count = 0
		for i in cells_array:
			for cell in i:
				cell_count += 1
				if cell_count < 1:
					exit("\nyou win! :) ")

main()
