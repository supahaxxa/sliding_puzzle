from random import choice		# for generating new board everytime
from warehouse import *			# for importing monotonous preset data
from datetime import datetime
import pygame


# declaring all the necessary colors by RGB value
BLACK = (0, 0, 0)
BLUE = (24, 119, 242)
GREEN = (42, 187, 167)
GREY = (127, 127, 127)
RED = (240, 40, 74)
OFFWHITE = (192, 192, 192)
PURPLE = (136, 65, 250)

# initializing the main module and the audio system
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/pop-1.mp3")		# loading the audio file
pygame.mixer.music.set_volume(1)				# setting volume between 0 to 1

WIDTH, HEIGHT = 1080, 720		# declaring resolution of the screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))		# creating the window
pygame.display.set_caption("Sliding Puzzle")			# setting the title of the window


# function to show text in the screen
# the (x, y) here are the coordinates of the center of the textbox
def render_text(font, font_size, text, font_color, x, y, bold=False):
	font_object = pygame.font.Font(font, font_size)
	font_object.set_bold(bold)
	text = font_object.render(text, True, font_color)
	text_rect = text.get_rect()
	text_rect.center = (x, y)
	screen.blit(text, text_rect)


# function for showing the blocks of the sliding puzzle
def draw_blocks(p):
	for i in range(15):
		if p[i] == correct[i]:
			pygame.draw.rect(screen, GREEN, pygame.Rect(p[i][0], p[i][1], 150, 150))
		else:
			pygame.draw.rect(screen, RED, pygame.Rect(p[i][0], p[i][1], 150, 150))
		render_text("assets/cooper-black.ttf", 75, block_text[i], OFFWHITE, (p[i][0] + 75), (p[i][1] + 75))

	del i		# deleting the variable, that is not necessary anymore


# implementation of the functions for four moves: up, down, left, and right
# at first takes the coordinates of the blank block
# then finds the index of the block that's supposed to move there
# then swaps their coordinates
def up():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] == coordinates[i][0] and blank[1] + 174 == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]

	del blank, target_index, i		# deleting the variable, that is not necessary anymore


def down():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] == coordinates[i][0] and blank[1] - 174 == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]

	del blank, target_index, i		# deleting the variable, that is not necessary anymore


def left():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] + 174 == coordinates[i][0] and blank[1] == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]

	del blank, target_index, i		# deleting the variable, that is not necessary anymore


def right():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] - 174 == coordinates[i][0] and blank[1] == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]

	del blank, target_index, i		# deleting the variable, that is not necessary anymore


# function to check completion
def completed():
	for i in range(16):
		if coordinates[i] != correct[i]:
			del i
			return False
	del i
	return True


# to randomize the new game everytime
def shuffle(n):
	for i in range(n):
		move = choice(range(4))
		if move == 0:
			up()
		elif move == 1:
			down()
		elif move == 2:
			left()
		else:
			right()

	del move, i		# deleting the variable, that is not necessary anymore


# store the state of the board of every new game
def store_prime_state():
	for i in range(16):
		new_set[i] = coordinates[i]

	del i		# deleting the variable, that is not necessary anymore


# restore the primary state of the game, takes to the configuration having zero moves
def restore_prime_state():
	for i in range(16):
		coordinates[i] = new_set[i]

	del i		# deleting the variable, that is not necessary anymore


def time_format(s):
	seconds = s % 60
	if seconds < 10:
		seconds = '0' + str(seconds)
	else:
		seconds = str(seconds)

	minutes = s // 60
	if minutes < 10:
		minutes = '0' + str(minutes)
	else:
		minutes = str(minutes)

	return minutes + ' : ' + seconds


shuffle(200)		# random configured start
moves = 0
start = datetime.now()
end = datetime.now()
store_prime_state()		# setting up for reset functionality to work
new_game_clicked = False
reset_clicked = False
finished = False
running = True
while running:
	if not finished:
		end = datetime.now()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit()
			if event.key == pygame.K_n:
				shuffle(200)
				moves = 0
				start = datetime.now()
				store_prime_state()
				finished = False
			if event.key == pygame.K_r:
				restore_prime_state()
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				if not finished and coordinates[15][1] != 546:
					pygame.mixer.music.play()
					up()
					moves += 1
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				if not finished and coordinates[15][1] != 24:
					pygame.mixer.music.play()
					down()
					moves += 1
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				if not finished and coordinates[15][0] != 546:
					pygame.mixer.music.play()
					left()
					moves += 1
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				if not finished and coordinates[15][0] != 24:
					pygame.mixer.music.play()
					right()
					moves += 1
		if event.type == pygame.MOUSEBUTTONDOWN:
			if 750 <= pygame.mouse.get_pos()[0] <= 1050 and 30 <= pygame.mouse.get_pos()[1] <= 105:
				new_game_clicked = True
				shuffle(200)
				moves = 0
				start = datetime.now()
				store_prime_state()
				finished = False

			if 750 <= pygame.mouse.get_pos()[0] <= 1050 and 135 <= pygame.mouse.get_pos()[1] <= 210:
				reset_clicked = True
				restore_prime_state()
				finished = False
		if event.type == pygame.MOUSEBUTTONUP:
			new_game_clicked = False
			reset_clicked = False

	screen.fill(BLACK)

	draw_blocks(coordinates)

	menu_panel_background = pygame.Surface((360, 720))
	menu_panel_background.fill(GREY)
	screen.blit(menu_panel_background, (720, 0))

	# showing the "new game" button
	if new_game_clicked:
		pygame.draw.rect(screen, PURPLE, pygame.Rect(750, 30, 300, 75))
	else:
		pygame.draw.rect(screen, BLUE, pygame.Rect(750, 30, 300, 75))
	render_text("assets/fragment-core.otf", 40, "New Game", OFFWHITE, 900, 72, bold=True)

	# showing the "reset" button
	if reset_clicked:
		pygame.draw.rect(screen, PURPLE, pygame.Rect(750, 135, 300, 75))
	else:
		pygame.draw.rect(screen, BLUE, pygame.Rect(750, 135, 300, 75))
	render_text("assets/fragment-core.otf", 40, "Reset", OFFWHITE, 900, 176, bold=True)

	# showing elapsed time
	render_text("assets/fragment-core.otf", 40, "Time:", OFFWHITE, 792, 679, bold=True)
	render_text("assets/fragment-core.otf", 40, time_format((end - start).seconds), OFFWHITE, 907, 678)

	# showing number of moves
	render_text("assets/fragment-core.otf", 40, "Moves:", OFFWHITE, 802, 600, bold=True)
	render_text("assets/fragment-core.otf", 40, str(moves), OFFWHITE, 900, 600)

	# post completion message
	if completed():
		finished = True

		overlay = pygame.Surface((720, 720))
		overlay.set_alpha(192)
		overlay.fill(BLACK)
		screen.blit(overlay, (0, 0))

		render_text("assets/bromph-town.ttf", 64, "Congratulations!", OFFWHITE, 360, 200)

	pygame.display.update()
