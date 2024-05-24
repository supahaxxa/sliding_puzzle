import conditions as c
from datetime import datetime
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
	for i in range(15):
		if p[i] == correct4[i]:
			pygame.draw.rect(screen, colorset[c.theme][4], pygame.Rect(p[i][0], p[i][1], 150, 150))
		else:
			pygame.draw.rect(screen, colorset[c.theme][2], pygame.Rect(p[i][0], p[i][1], 150, 150))
		render_text("assets/cooper-black.ttf", 75, block_text4[i], colorset[c.theme][6], (p[i][0] + 75), (p[i][1] + 75))
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
	blank = coordinates4[15]
	target_index = -1
	for i in range(15):
		if blank[0] == coordinates4[i][0] and blank[1] + 174 == coordinates4[i][1]:
			target_index = i
	coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function for 'down' move
# it swaps the coordinates of the block above the blank space with that of the blank space
def down():
	blank = coordinates4[15]
	target_index = -1
	for i in range(15):
		if blank[0] == coordinates4[i][0] and blank[1] - 174 == coordinates4[i][1]:
			target_index = i
	coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function for 'left' move
# it swaps the coordinates of the block right to the blank space with that of the blank space
def left():
	blank = coordinates4[15]
	target_index = -1
	for i in range(15):
		if blank[0] + 174 == coordinates4[i][0] and blank[1] == coordinates4[i][1]:
			target_index = i
	coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function for 'right' move
# it swaps the coordinates of the block left to the blank space with that of the blank space
def right():
	blank = coordinates4[15]
	target_index = -1
	for i in range(15):
		if blank[0] - 174 == coordinates4[i][0] and blank[1] == coordinates4[i][1]:
			target_index = i
	coordinates4[15], coordinates4[target_index] = coordinates4[target_index], coordinates4[15]
	del blank, target_index, i		# deleting the variable(s) which are not needed anymore


# function to check whether the puzzle is solved or not
# it checks all the blocks' position
def completed():
	for i in range(16):
		if coordinates4[i] != correct4[i]:
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
	for i in range(16):
		new_set4[i] = coordinates4[i]
	del i		# deleting the variable(s) which are not needed anymore


# function to restore the previous state of the board after your move, for reset functionality to work
def restore_prime_state():
	for i in range(16):
		coordinates4[i] = new_set4[i]
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
	render_text("assets/hey-comic.ttf", 100, "Sliding Puzzle", colorset[c.theme][6], 540, 120)

	simulate_button(360, 310, 360, 80, 20)
	render_text("assets/fragment-core.otf", 40, "Start Game", colorset[c.theme][6], 543, 354, True)

	simulate_button(360, 420, 360, 80, 20)
	render_text("assets/fragment-core.otf", 40, "Instructions", colorset[c.theme][6], 540, 464, True)

	simulate_button(360, 530, 360, 80, 20)
	render_text("assets/fragment-core.otf", 40, "Settings", colorset[c.theme][6], 540, 574, True)


def game_screen():
	if not c.finished:
		c.end = datetime.now()

	draw_blocks(coordinates4)

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

			if c.show_screen == 2:
				if ek == pygame.K_UP or ek == pygame.K_w:
					if not c.finished and coordinates4[15][1] != 546:
						pygame.mixer.music.play()
						c.moves += 1
						up()
				if ek == pygame.K_DOWN or ek == pygame.K_s:
					if not c.finished and coordinates4[15][1] != 24:
						pygame.mixer.music.play()
						c.moves += 1
						down()
				if ek == pygame.K_LEFT or ek == pygame.K_a:
					if not c.finished and coordinates4[15][0] != 546:
						pygame.mixer.music.play()
						c.moves += 1
						left()
				if ek == pygame.K_RIGHT or ek == pygame.K_d:
					if not c.finished and coordinates4[15][0] != 24:
						pygame.mixer.music.play()
						c.moves += 1
						right()
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

			if c.show_screen == 4:
				if check_hover(20, 20, 90, 70, 20):
					c.show_screen = 1
				if check_hover(500, 285, 40, 40, 10) and c.volume > 0:
					c.volume -= 1
					pygame.mixer.music.set_volume(c.volume / 10)
				if check_hover(720, 285, 40, 40, 10) and c.volume < 10:
					c.volume += 1
					pygame.mixer.music.set_volume(c.volume / 10)
				if check_hover(525, 385, 210, 60, 15):
					c.theme = (c.theme + 1) % len(colorset)
		if et == pygame.MOUSEBUTTONUP:
			c.click = False

	screen.fill(colorset[c.theme][0])

	if c.show_screen == 1:
		menu_screen()
	elif c.show_screen == 2:
		game_screen()
	elif c.show_screen == 3:
		render_text("assets/fragment-core.otf", 60, "COMING SOON", colorset[c.theme][6], 540, 360, True)
	elif c.show_screen == 4:
		settings_screen()

	pygame.display.update()

pygame.quit()
