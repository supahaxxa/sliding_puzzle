# 3x3 > 24 | 208
# 4x4 > 24 | 150
# 5x5 > 20 | 120

import conditions as c
from datetime import datetime
from math import floor, pi, sin
from random import choice
from warehouse import *
import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/pop-1.mp3")		# loading the sound for move - up, down, left, and right
pygame.mixer.music.set_volume(1)				# setting volume of the loaded audio clip

screen = pygame.display.set_mode((WIDTH, HEIGHT))		# setting window size
pygame.display.set_caption("Sliding Puzzle")			# setting window title


# function to find out distance between the points (x1, y1) and (x2, y2)
def distance(x1, y1, x2, y2):
	return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5


# function to show text in the window
def render_text(font, font_size, text, font_color, x, y, bold=False):
	font_object = pygame.font.Font(font, font_size)			# initializing the font object with font and size
	font_object.set_bold(bold)								# defining whether the font will be bold or not
	text = font_object.render(text, True, font_color)		# rendering the text with its color
	text_rect = text.get_rect()								# returns a rect object surrounding the text
	text_rect.center = (x, y)								# positioning the text
	screen.blit(text, text_rect)							# displaying the text in the window
	del font_object, text, text_rect						# deleting the variable(s) which are not needed anymore


# function to check whether the cursor is over a button or not
def check_hover(left2, top2, width2, height2, radius2):
	# checking vertical rect
	if left2 + radius2 <= pygame.mouse.get_pos()[0] <= left2 + width2 - radius2 and top2 <= pygame.mouse.get_pos()[1] <= top2 + height2:
		return True
	# checking horizontal rect
	if left2 <= pygame.mouse.get_pos()[0] <= left2 + width2 and top2 + radius2 <= pygame.mouse.get_pos()[1] <= top2 + height2 - radius2:
		return True
	# checking top left arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left2 + radius2, top2 + radius2) <= radius2:
		return True
	# checking top right arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left2 + width2 - radius2, top2 + radius2) <= radius2:
		return True
	# checking bottom left arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left2 + radius2, top2 + height2 - radius2) <= radius2:
		return True
	# checking bottom right arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left2 + width2 - radius2, top2 + height2 - radius2) <= radius2:
		return True
	return False


# function to implement the behavior of a button
def simulate_button(left5, top5, width5, height5, radius5):
	if check_hover(left5, top5, width5, height5, radius5):
		if c.click:
			pygame.draw.rect(screen, colorset[c.theme][2], pygame.Rect(left5, top5, width5, height5), border_radius=radius5)
		else:
			pygame.draw.rect(screen, colorset[c.theme][4], pygame.Rect(left5, top5, width5, height5), border_radius=radius5)
	else:
		pygame.draw.rect(screen, colorset[c.theme][3], pygame.Rect(left5, top5, width5, height5), border_radius=radius5)


# function to draw the movable blocks, from 1 to 15
def draw_blocks(p):
	if c.mode == 3:
		for i in range(8):
			if p[i] == correct3[i]:
				pygame.draw.rect(screen, colorset[c.theme][4], pygame.Rect(p[i][0], p[i][1], 208, 208))
			else:
				pygame.draw.rect(screen, colorset[c.theme][2], pygame.Rect(p[i][0], p[i][1], 208, 208))
			render_text("assets/bebas-neue.ttf", 104, block_text3[i], colorset[c.theme][6], p[i][0] + 104, p[i][1] + 104)
	elif c.mode == 4:
		for i in range(15):
			if p[i] == correct4[i]:
				pygame.draw.rect(screen, colorset[c.theme][4], pygame.Rect(p[i][0], p[i][1], 150, 150))
			else:
				pygame.draw.rect(screen, colorset[c.theme][2], pygame.Rect(p[i][0], p[i][1], 150, 150))
			render_text("assets/bebas-neue.ttf", 75, block_text4[i], colorset[c.theme][6], p[i][0] + 75, p[i][1] + 75)
	elif c.mode == 5:
		for i in range(24):
			if p[i] == correct5[i]:
				pygame.draw.rect(screen, colorset[c.theme][4], pygame.Rect(p[i][0], p[i][1], 120, 120))
			else:
				pygame.draw.rect(screen, colorset[c.theme][2], pygame.Rect(p[i][0], p[i][1], 120, 120))
			render_text("assets/bebas-neue.ttf", 60, block_text5[i], colorset[c.theme][6], p[i][0] + 60, p[i][1] + 60)
	del i		# deleting the variable(s) which are not needed anymore


def draw_volume_bars(left4, top4, width4, height4, hgap, vgap):
	for i in range(10):
		if i < c.volume:
			color = colorset[c.theme][4]
		else:
			color = colorset[c.theme][2]
		pygame.draw.rect(screen, color, pygame.Rect(left4 + (i * width4) + (i * hgap), top4 + ((9 - i) * vgap), width4, height4 - ((9 - i) * vgap)), border_radius=width4//2)


def draw_theme_blocks(left3, top3):
	for i in range(6):
		pygame.draw.rect(screen, colorset[c.theme][i], pygame.Rect(left3 + (i * 30), top3, 30, 30))


# function for 'up' move
# it swaps the coordinates of the block below the blank space with that of the blank space
def up():
	target_index = -1
	if c.mode == 3:
		blank = coordinates3[8]
		for i in range(8):
			if blank[0] == coordinates3[i][0] and blank[1] + 232 == coordinates3[i][1]:
				target_index = i
		coordinates3[8], coordinates3[target_index] = coordinates3[target_index], coordinates3[8]
	elif c.mode == 4:
		blank = coordinates4[15]
		for i in range(15):
			if blank[0] == coordinates4[i][0] and blank[1] + 174 == coordinates4[i][1]:
				target_index = i
		coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	elif c.mode == 5:
		blank = coordinates5[24]
		for i in range(24):
			if blank[0] == coordinates5[i][0] and blank[1] + 140 == coordinates5[i][1]:
				target_index = i
		coordinates5[24], coordinates5[target_index] = coordinates5[target_index], coordinates5[24]

	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function for 'down' move
# it swaps the coordinates of the block above the blank space with that of the blank space
def down():
	target_index = -1
	if c.mode == 3:
		blank = coordinates3[8]
		for i in range(8):
			if blank[0] == coordinates3[i][0] and blank[1] - 232 == coordinates3[i][1]:
				target_index = i
		coordinates3[8], coordinates3[target_index] = coordinates3[target_index], coordinates3[8]
	elif c.mode == 4:
		blank = coordinates4[15]
		for i in range(15):
			if blank[0] == coordinates4[i][0] and blank[1] - 174 == coordinates4[i][1]:
				target_index = i
		coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	elif c.mode == 5:
		blank = coordinates5[24]
		for i in range(24):
			if blank[0] == coordinates5[i][0] and blank[1] - 140 == coordinates5[i][1]:
				target_index = i
		coordinates5[24], coordinates5[target_index] = coordinates5[target_index], coordinates5[24]

	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function for 'left' move
# it swaps the coordinates of the block right to the blank space with that of the blank space
def left():
	target_index = -1
	if c.mode == 3:
		blank = coordinates3[8]
		for i in range(8):
			if blank[0] + 232 == coordinates3[i][0] and blank[1] == coordinates3[i][1]:
				target_index = i
		coordinates3[8], coordinates3[target_index] = coordinates3[target_index], coordinates3[8]
	elif c.mode == 4:
		blank = coordinates4[15]
		for i in range(15):
			if blank[0] + 174 == coordinates4[i][0] and blank[1] == coordinates4[i][1]:
				target_index = i
		coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	elif c.mode == 5:
		blank = coordinates5[24]
		for i in range(24):
			if blank[0] + 140 == coordinates5[i][0] and blank[1] == coordinates5[i][1]:
				target_index = i
		coordinates5[24], coordinates5[target_index] = coordinates5[target_index], coordinates5[24]

	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function for 'right' move
# it swaps the coordinates of the block left to the blank space with that of the blank space
def right():
	target_index = -1
	if c.mode == 3:
		blank = coordinates3[8]
		for i in range(8):
			if blank[0] - 232 == coordinates3[i][0] and blank[1] == coordinates3[i][1]:
				target_index = i
		coordinates3[8], coordinates3[target_index] = coordinates3[target_index], coordinates3[8]
	elif c.mode == 4:
		blank = coordinates4[15]
		for i in range(15):
			if blank[0] - 174 == coordinates4[i][0] and blank[1] == coordinates4[i][1]:
				target_index = i
		coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	elif c.mode == 5:
		blank = coordinates5[24]
		for i in range(24):
			if blank[0] - 140 == coordinates5[i][0] and blank[1] == coordinates5[i][1]:
				target_index = i
		coordinates5[24], coordinates5[target_index] = coordinates5[target_index], coordinates5[24]

	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function to check whether the puzzle is solved or not
# it checks all the blocks' position
def completed():
	if c.mode == 3:
		for i in range(9):
			if coordinates3[i] != correct3[i]:
				del i		# deleting the variable(s) which are not needed anymore
				return False
	elif c.mode == 4:
		for i in range(16):
			if coordinates4[i] != correct4[i]:
				del i		# deleting the variable(s) which are not needed anymore
				return False
	elif c.mode == 5:
		for i in range(25):
			if coordinates5[i] != correct5[i]:
				del i		# deleting the variable(s) which are not needed anymore
				return False

	del i		# deleting the variable(s) which are not needed anymore
	return True


# function to generate new, totally random, board for every new game
# it does n moves of up(), down(), left(), or right(), randomly
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
	del move, i		# deleting the variable(s) which are not needed anymore


# function to store the previous state of the board before you move, for reset functionality to work
def store_prime_state():
	if c.mode == 3:
		for i in range(9):
			new_set3[i] = coordinates3[i]
	elif c.mode == 4:
		for i in range(16):
			new_set4[i] = coordinates4[i]
	elif c.mode == 5:
		for i in range(25):
			new_set5[i] = coordinates5[i]

	del i		# deleting the variable(s) which are not needed anymore


# function to restore the previous state of the board after your move, for reset functionality to work
def restore_prime_state():
	if c.mode == 3:
		for i in range(9):
			coordinates3[i] = new_set3[i]
	elif c.mode == 4:
		for i in range(16):
			coordinates4[i] = new_set4[i]
	elif c.mode == 5:
		for i in range(25):
			coordinates5[i] = new_set5[i]

	del i		# deleting the variable(s) which are not needed anymore


# function to find out the time in mm:ss format
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


def menu_screen():
	c.red, c.green, c.blue = (c.red + 0.5) % 180, (c.green + 0.5) % 180, (c.blue + 0.5) % 180
	r, g, b = floor(255 * sin(c.red * pi / 180)), floor(255 * sin(c.green * pi / 180)), floor(255 * sin(c.blue * pi / 180))
	render_text("assets/hey-comic.ttf", 100, "Sliding Puzzle", (r, g, b), 540, 120)

	simulate_button(360, 310, 360, 80, 20)
	render_text("assets/fragment-core.otf", 40, "Start Game", colorset[c.theme][6], 543, 354, True)

	simulate_button(360, 420, 360, 80, 20)
	render_text("assets/fragment-core.otf", 40, "Instructions", colorset[c.theme][6], 540, 464, True)

	simulate_button(360, 530, 360, 80, 20)
	render_text("assets/fragment-core.otf", 40, "Settings", colorset[c.theme][6], 540, 574, True)


def game_screen():
	if not c.finished:
		c.end = datetime.now()

	if c.mode == 3:
		draw_blocks(coordinates3)
	elif c.mode == 4:
		draw_blocks(coordinates4)
	elif c.mode == 5:
		draw_blocks(coordinates5)

	# for showing the options panel on the right
	pygame.draw.rect(screen, colorset[c.theme][5], pygame.Rect(720, 0, 360, 720))

	simulate_button(750, 30, 300, 75, 20)
	render_text("assets/fragment-core.otf", 40, "New Game", colorset[c.theme][6], 900, 72, bold=True)

	simulate_button(750, 135, 300, 75, 20)
	render_text("assets/fragment-core.otf", 40, "Reset", colorset[c.theme][6], 900, 176, bold=True)

	simulate_button(750, 240, 300, 75, 20)
	render_text("assets/fragment-core.otf", 40, "Main Menu", colorset[c.theme][6], 900, 280, bold=True)

	render_text("assets/fragment-core.otf", 40, "Time:", colorset[c.theme][6], 792, 679, bold=True)
	render_text("assets/fragment-core.otf", 40, time_format((c.end - c.start).seconds), colorset[c.theme][6], 907, 678)

	render_text("assets/fragment-core.otf", 40, "Moves:", colorset[c.theme][6], 802, 600, bold=True)
	render_text("assets/fragment-core.otf", 40, str(c.moves), colorset[c.theme][6], 900, 600)

	if completed():
		if not c.finished:
			c.finished = True

		overlay = pygame.Surface((720, 720))
		overlay.set_alpha(192)
		overlay.fill((0, 0, 0))
		screen.blit(overlay, (0, 0))
		render_text("assets/bromph-town.ttf", 64, "Congratulations!", (192, 192, 192), 360, 360)


def instructions_screen(n):
	# the button to return to main menu
	simulate_button(20, 20, 90, 70, 20)
	pygame.draw.polygon(screen, colorset[c.theme][6], ((47, 55), (77, 35), (77, 75)))

	# background rectangle to contain the instructions
	pygame.draw.rect(screen, colorset[c.theme][5], pygame.Rect(180, 30, 720, 660))

	# navigation buttons
	simulate_button(100, 330, 60, 60, 15)
	pygame.draw.polygon(screen, colorset[c.theme][6], ((140, 345), (115, 360), (140, 375)))
	simulate_button(920, 330, 60, 60, 15)
	pygame.draw.polygon(screen, colorset[c.theme][6], ((940, 345), (965, 360), (940, 375)))

	# page indicator
	for i in range(3):
		if i == c.instructions_screen:
			color = colorset[c.theme][3]
		else:
			color = colorset[c.theme][1]
		pygame.draw.circle(screen, color, (520 + (i * 20), 705), 5)

	if n == 0:
		# headline
		render_text("assets/bebas-neue.ttf", 40, "HOW TO PLAY?", colorset[c.theme][6], 540, 75)

		# general text
		render_text("assets/type-machine.ttf", 20, "Starting in the top left corner, move the tiles in ascend-", colorset[c.theme][6], 538, 130)
		render_text("assets/type-machine.ttf", 20, "ing order in the grid. The tile in the lower right corner", colorset[c.theme][6], 534, 165)
		render_text("assets/type-machine.ttf", 20, "should be empty. To move a tile you can use your arrow", colorset[c.theme][6], 534, 200)
		render_text("assets/type-machine.ttf", 20, "keys or your W A S D keys. The resulting order should", colorset[c.theme][6], 532, 235)
		render_text("assets/type-machine.ttf", 20, "be like:", colorset[c.theme][6], 293, 270)

		# sample images
		threexthree = pygame.image.load("assets/3x3.png")
		threexthree = pygame.transform.scale(threexthree, (180, 180))
		screen.blit(threexthree, (250, 370))
		fourxfour = pygame.image.load("assets/4x4.png")
		fourxfour = pygame.transform.scale(fourxfour, (180, 180))
		screen.blit(fourxfour, (450, 370))
		fivexfive = pygame.image.load("assets/5x5.png")
		fivexfive = pygame.transform.scale(fivexfive, (180, 180))
		screen.blit(fivexfive, (650, 370))

	if n == 1:
		# headline
		render_text("assets/bebas-neue.ttf", 40, "SETTINGS", colorset[c.theme][6], 540, 75)

		# general text
		render_text("assets/type-machine.ttf", 20, "You can change the volume and theme from the settings.", colorset[c.theme][6], 539, 130)
		render_text("assets/type-machine.ttf", 20, "To change the volume, click on the + or - button.", colorset[c.theme][6], 497, 165)
		render_text("assets/type-machine.ttf", 20, "To toggle the theme, left click for next theme,", colorset[c.theme][6], 485, 200)
		render_text("assets/type-machine.ttf", 20, "and right click for next theme.", colorset[c.theme][6], 430, 235)

	if n == 2:
		# headline
		render_text("assets/bebas-neue.ttf", 40, "SHORTCUTS", colorset[c.theme][6], 540, 75)

		# general text
		render_text("assets/type-machine.ttf", 20, "To start a new game, you can press N key.", colorset[c.theme][6], 467, 130)
		render_text("assets/type-machine.ttf", 20, "To reset the game, you can press R key.", colorset[c.theme][6], 453, 165)
		render_text("assets/type-machine.ttf", 20, "To change the game mode, you can press SPACE key.", colorset[c.theme][6], 518, 200)
		render_text("assets/type-machine.ttf", 20, "To return to main menu from any other screen,", colorset[c.theme][6], 494, 235)
		render_text("assets/type-machine.ttf", 20, "you can press BACKSPACE key.", colorset[c.theme][6], 435, 270)
		render_text("assets/type-machine.ttf", 20, "To change the theme, you can press TAB key.", colorset[c.theme][6], 481, 305)
		render_text("assets/type-machine.ttf", 20, "To exit the game at any time, you can press the ESC key.", colorset[c.theme][6], 541, 340)

def settings_screen():
	simulate_button(20, 20, 90, 70, 20)
	pygame.draw.polygon(screen, colorset[c.theme][6], ((47, 55), (77, 35), (77, 75)))

	pygame.draw.rect(screen, colorset[c.theme][5], pygame.Rect(300, 260, 480, 90), border_radius=20)
	pygame.draw.line(screen, colorset[c.theme][0], (480, 275), (480, 335))
	render_text("assets/fragment-core.otf", 40, "Volume", colorset[c.theme][6], 390, 310, True)
	simulate_button(500, 285, 40, 40, 10)
	render_text("assets/fragment-core.otf", 40, "-", colorset[c.theme][6], 520, 304, True)
	simulate_button(720, 285, 40, 40, 10)
	render_text("assets/fragment-core.otf", 40, "+", colorset[c.theme][6], 740, 303, True)
	draw_volume_bars(555, 280, 6, 50, 10, 4)

	pygame.draw.rect(screen, colorset[c.theme][5], pygame.Rect(300, 370, 480, 90), border_radius=20)
	pygame.draw.line(screen, colorset[c.theme][0], (480, 385), (480, 445))
	render_text("assets/fragment-core.otf", 40, "Theme", colorset[c.theme][6], 390, 419, True)
	simulate_button(525, 385, 210, 60, 15)
	pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(539, 399, 182, 32))
	draw_theme_blocks(540, 400)


# game loop
while c.running:
	for event in pygame.event.get():
		et = event.type

		if et == pygame.QUIT:
			c.running = False
		if et == pygame.KEYDOWN:
			ek = event.key

			if ek == pygame.K_ESCAPE:
				c.running = False
			if ek == pygame.K_TAB:
				c.theme = (c.theme + 1) % len(colorset)
			if ek == pygame.K_BACKSPACE:
				c.show_screen = 1
				c.instructions_screen = 0

			if c.show_screen == 2:
				if ek == pygame.K_UP or ek == pygame.K_w:
					if c.mode == 3:
						if not c.finished and coordinates3[8][1] != 488:
							pygame.mixer.music.play()
							c.moves += 1
							up()
					elif c.mode == 4:
						if not c.finished and coordinates4[15][1] != 546:
							pygame.mixer.music.play()
							c.moves += 1
							up()
					elif c.mode == 5:
						if not c.finished and coordinates5[24][1] != 580:
							pygame.mixer.music.play()
							c.moves += 1
							up()
				if ek == pygame.K_DOWN or ek == pygame.K_s:
					if c.mode == 3:
						if not c.finished and coordinates3[8][1] != 24:
							pygame.mixer.music.play()
							c.moves += 1
							down()
					elif c.mode == 4:
						if not c.finished and coordinates4[15][1] != 24:
							pygame.mixer.music.play()
							c.moves += 1
							down()
					elif c.mode == 5:
						if not c.finished and coordinates5[24][1] != 20:
							pygame.mixer.music.play()
							c.moves += 1
							down()
				if ek == pygame.K_LEFT or ek == pygame.K_a:
					if c.mode == 3:
						if not c.finished and coordinates3[8][0] != 488:
							pygame.mixer.music.play()
							c.moves += 1
							left()
					elif c.mode == 4:
						if not c.finished and coordinates4[15][0] != 546:
							pygame.mixer.music.play()
							c.moves += 1
							left()
					elif c.mode == 5:
						if not c.finished and coordinates5[24][0] != 580:
							pygame.mixer.music.play()
							c.moves += 1
							left()
				if ek == pygame.K_RIGHT or ek == pygame.K_d:
					if c.mode == 3:
						if not c.finished and coordinates3[8][0] != 24:
							pygame.mixer.music.play()
							c.moves += 1
							right()
					elif c.mode == 4:
						if not c.finished and coordinates4[15][0] != 24:
							pygame.mixer.music.play()
							c.moves += 1
							right()
					elif c.mode == 5:
						if not c.finished and coordinates5[24][0] != 20:
							pygame.mixer.music.play()
							c.moves += 1
							right()
				if ek == pygame.K_n:
					shuffle(200)
					store_prime_state()
					c.start = datetime.now()
					c.end = c.start
					c.moves = 0
					c.finished = False
				if ek == pygame.K_r and not c.finished:
					restore_prime_state()
				if ek == pygame.K_SPACE:
					c.mode += 1
					if c.mode == 6:
						c.mode -= 3
					shuffle(200)
					store_prime_state()
					c.start = datetime.now()
					c.end = c.start
					c.moves = 0
					c.finished = False

			if c.show_screen == 3:
				if ek == pygame.K_LEFT and c.instructions_screen > 0:
					c.instructions_screen -= 1
				if ek == pygame.K_RIGHT and c.instructions_screen < 2:
					c.instructions_screen += 1
		if et == pygame.MOUSEBUTTONDOWN:
			c.click = True

			if c.show_screen == 1:
				if check_hover(360, 310, 360, 80, 20):
					c.show_screen = 2
					shuffle(200)
					store_prime_state()
					c.start = datetime.now()
					c.end = c.start
					c.moves = 0
					c.finished = False
				if check_hover(360, 420, 360, 80, 20):
					c.show_screen = 3
				if check_hover(360, 530, 360, 80, 20):
					c.show_screen = 4

			if c.show_screen == 2:
				if check_hover(750, 30, 300, 75, 20):
					shuffle(200)
					store_prime_state()
					c.start = datetime.now()
					c.end = c.start
					c.moves = 0
					c.finished = False
				if check_hover(750, 135, 300, 75, 20) and not c.finished:
					restore_prime_state()
				if check_hover(750, 240, 300, 75, 20):
					c.show_screen = 1

			if c.show_screen == 3:
				if check_hover(20, 20, 90, 70, 20):
					c.show_screen = 1
					c.instructions_screen = 0
				if check_hover(100, 330, 60, 60, 15):
					if c.instructions_screen > 0:
						c.instructions_screen -= 1
				if check_hover(920, 330, 60, 60, 15):
					if c.instructions_screen < 2:
						c.instructions_screen += 1

			if c.show_screen == 4:
				if check_hover(20, 20, 90, 70, 20):
					c.show_screen = 1
				if check_hover(500, 285, 40, 40, 10) and c.volume > 0:
					c.volume -= 1
					pygame.mixer.music.set_volume(c.volume / 10)
					pygame.mixer.music.play()
				if check_hover(720, 285, 40, 40, 10) and c.volume < 10:
					c.volume += 1
					pygame.mixer.music.set_volume(c.volume / 10)
					pygame.mixer.music.play()
				if check_hover(525, 385, 210, 60, 15):
					if pygame.mouse.get_pressed(3)[0]:
						c.theme = (c.theme + 1) % len(colorset)
					if pygame.mouse.get_pressed(3)[2]:
						c.theme = (c.theme - 1) % len(colorset)
		if et == pygame.MOUSEBUTTONUP:
			c.click = False

	screen.fill(colorset[c.theme][0])

	if c.show_screen == 1:
		menu_screen()
	elif c.show_screen == 2:
		game_screen()
	elif c.show_screen == 3:
		instructions_screen(c.instructions_screen)
	elif c.show_screen == 4:
		settings_screen()

	pygame.display.update()

pygame.quit()
