import numpy as np
import sys, pygame, time, countapi
pygame.init()

# Sizes
figure_size = 90
space_size = 20

# Colors
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_gray = (109, 112, 110)

# Set screen size
scr_width = 3 * (figure_size + space_size) + space_size
scr_height = 3 * (figure_size + space_size) + space_size
screen = pygame.display.set_mode((scr_width, scr_height))

# Grids
grid = previous_grid = np.full((3, 3), 0)

# Draw X in specified position
def drawX (x, y):
	# Line 1
	pygame.draw.line(
		screen,
		color_white,
		# Point 1
		((x * figure_size) + ((x + 1) * space_size),
		(y * figure_size) + ((y + 1) * space_size)),
		# Point 2
		((x * figure_size) + ((x + 1) * space_size + figure_size),
		(y * figure_size) + ((y + 1) * space_size) + figure_size),
		5)
	# Line 2
	pygame.draw.line(
		screen,
		color_white,
		# Point 1
		(((x + 1) * figure_size) + ((x + 1) * space_size),
		(y * figure_size) + ((y + 1) * space_size)),
		# Point 2
		((x * figure_size) + ((x + 1) * space_size),
		(y * figure_size) + ((y + 1) * space_size) + figure_size),
		5)

# Draw O in specified position
def drawO(x, y):
	pygame.draw.circle(
		screen,
		color_white,
		[(space_size * (x + 1)) + (figure_size * x) + figure_size / 2,
			(space_size * (y + 1)) + (figure_size * y) + figure_size / 2],
		figure_size / 2,
		5)

# Draw background in specified position
def drawBg(x, y):
	pygame.draw.rect(
		screen,
		color_gray,
		[(x * figure_size) + ((x + 1) * space_size),
		(y * figure_size) + ((y + 1) * space_size),
		figure_size, figure_size],
		0)

# Get clicked cell
def registerClick(pos):
	x = int(pos[0] / (figure_size + space_size))
	y = int(pos[1] / (figure_size + space_size))
	if screen.get_at(pos) != color_black:
		return (x, y)
	else:
		return (-1, -1)

# Check win
def checkWin(input):
	result = 3
	if 0 in input:
		result = 0
	for j in range (0, 2):
		# Check rows
		for i in range(0, 3):
			if np.all(input[i] == input[i][0]):
				return input[i][0]
			# Check diagonal
		if input[0][0] == input[1][1] == input[2][2]:
			return input[0][0]
		input = np.rot90(input)
	return result
	  
# Main loop
while True:
	# Menu
	choice = input("Create / Join / Quit: ").lower()
	if choice == 'create':
		id = countapi.createGame()
		turn = True
		playerId = 1
	elif choice == 'join':
		id = input("Enter ID: ")
		turn = False
		playerId = 2
	elif choice == 'quit':
		break
	else:
		print("Couldn't recognize command \'" + choice + "\'")
		continue

	# Play
	while True:
		# Loop trough events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.MOUSEBUTTONUP:
				if turn:
					click = registerClick(pygame.mouse.get_pos())
					if click != (-1, -1) and grid[click[1], click[0]] == 0:
						grid[click[1], click[0]] = playerId
						countapi.setGrid(id, grid)
						previous_grid = grid
						turn = False

		# Check if there are changes
		grid = countapi.getGrid(id)
		if not np.array_equal(grid, previous_grid):
			turn = True

		# Draw grid
		for row in range(0, 3):
			for col in range(0, 3):
				drawBg(row, col)
				if grid[col, row] == 1:
					drawX(row, col)
				elif grid[col, row] == 2:
					drawO(row, col)
		pygame.display.flip()

		# Check for win
		s = checkWin(grid)
		if s > 0:
			print("GAME OVER")
			turn = False
			if s == 3:
				print("It's a draw") 
			elif s == playerId:
				print("You won") 
			else:
				print("You lost")
			break
		time.sleep(0.1)