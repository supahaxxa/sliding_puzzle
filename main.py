from random import choice
from warehouse import *
import pygame


BLACK = (0, 0, 0)
GREEN = (42, 187, 167)
RED = (240, 40, 74)
OFFWHITE = (192, 192, 192)

pygame.init()

WIDTH, HEIGHT = 720, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")


def render_text(font, font_size, text, font_color, x, y):
	font_object = pygame.font.Font(font, font_size)
	text = font_object.render(text, True, font_color)
	text_rect = text.get_rect()
	text_rect.center = (x, y)
	screen.blit(text, text_rect)


def draw_blocks(p):
	side = WIDTH * 5 / 24
	for i in range(15):
		if p[i] == correct[i]:
			pygame.draw.rect(screen, GREEN, pygame.Rect(p[i][0], p[i][1], side, side), border_radius=10)
		else:
			pygame.draw.rect(screen, RED, pygame.Rect(p[i][0], p[i][1], side, side), border_radius=10)
		render_text("cooper-black.ttf", int(side / 2), block_text[i], OFFWHITE, (p[i][0] + (side / 2)), (p[i][1] + (side / 2)))

	del side, i


def up():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] == coordinates[i][0] and blank[1] + 174 == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]


def down():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] == coordinates[i][0] and blank[1] - 174 == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]


def left():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] + 174 == coordinates[i][0] and blank[1] == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]


def right():
	blank = coordinates[15]
	target_index = -1
	for i in range(15):
		if blank[0] - 174 == coordinates[i][0] and blank[1] == coordinates[i][1]:
			target_index = i
	coordinates[15], coordinates[target_index] = coordinates[target_index], coordinates[15]

	del blank, target_index, i


def completed():
	for i in range(16):
		if coordinates[i] != correct[i]:
			return False
	return True


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


shuffle(200)
finished = False
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit()
			if event.key == pygame.K_n:
				shuffle(200)
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				if not finished:
					up()
			if event.key == pygame.K_DOWN or event.key == pygame.K_s:
				if not finished:
					down()
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				if not finished:
					left()
			if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				if not finished:
					right()

	screen.fill(BLACK)

	draw_blocks(coordinates)

	if completed():
		finished = True

		overlay = pygame.Surface((720, 720))
		overlay.set_alpha(192)
		overlay.fill(BLACK)
		screen.blit(overlay, (0, 0))

		render_text("fragment-core.otf", 64, "Congratulations!", OFFWHITE, 360, 200)

	pygame.display.update()
