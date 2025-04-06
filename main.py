from datetime import datetime
from os import system
from random import choice
import assets.globals as data
import pygame


pygame.init()
screen = pygame.display.set_mode((data.window_width, data.window_height))
pygame.display.set_caption("Sliding Puzzle")

pygame.mixer.init()
pygame.mixer.music.load("assets/pop-1.mp3")
pygame.mixer.music.set_volume(round(data.volume * 0.1, 1))


def distance(x1, y1, x2, y2):
	return (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5


def render_text(font, font_size, text, font_color, x, y, bold=False):
	font_object = pygame.font.Font(font, round(font_size))
	font_object.set_bold(bold)
	text = font_object.render(text, True, font_color)
	text_rect = text.get_rect()
	text_rect.center = (x, y)
	screen.blit(text, text_rect)


def check_hover(left, top, width, height, radius):
	if left + radius <= pygame.mouse.get_pos()[0] <= left + width - radius and top <= pygame.mouse.get_pos()[1] <= top + height:
		return True			# checking vertical rect
	if left <= pygame.mouse.get_pos()[0] <= left + width and top + radius <= pygame.mouse.get_pos()[1] <= top + height - radius:
		return True			# checking horizontal rect
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left + radius, top + radius) <= radius:
		return True			# checking top left arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left + width - radius, top + radius) <= radius:
		return True			# checking top right arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left + radius, top + height - radius) <= radius:
		return True			# checking bottom left arc
	if distance(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], left + width - radius, top + height - radius) <= radius:
		return True			# checking bottom right arc
	return False


def simulate_button(left, top, width, height, radius, signal_code, alt_signal_code):
	radius = round(radius)
	if check_hover(left, top, width, height, radius):
		if data.click:
			if pygame.mouse.get_pressed(3)[0]:
				data.signal = signal_code
			if pygame.mouse.get_pressed(3)[2]:
				data.signal = alt_signal_code
			pygame.draw.rect(screen, data.colorset[data.theme][2], pygame.Rect(left, top, width, height), border_radius=radius)
		else:
			pygame.draw.rect(screen, data.colorset[data.theme][4], pygame.Rect(left, top, width, height), border_radius=radius)
	else:
		pygame.draw.rect(screen, data.colorset[data.theme][3], pygame.Rect(left, top, width, height), border_radius=radius)


def draw_blocks():
	for i in range(data.mode * data.mode - 1):
		if data.no_diff(data.coordinates[i][0], data.correct[i][0]) and data.no_diff(data.coordinates[i][1], data.correct[i][1]):
			pygame.draw.rect(screen, data.colorset[data.theme][4], pygame.Rect(data.coordinates[i][0], data.coordinates[i][1], data.scale_w(data.tile_size), data.scale_h(data.tile_size)))
		else:
			pygame.draw.rect(screen, data.colorset[data.theme][2], pygame.Rect(data.coordinates[i][0], data.coordinates[i][1], data.scale_w(data.tile_size), data.scale_h(data.tile_size)))
		render_text("assets/bebas-neue.ttf", data.scale_h(data.tile_size / 2), str(i + 1), data.colorset[data.theme][6], data.scale_w(data.coordinates[i][0] + data.tile_size / 2), data.scale_h(data.coordinates[i][1] + data.tile_size / 2))


def draw_volume_bars(left4, top4, width4, height4, hgap, vgap):
	for i in range(10):
		if i < data.volume:
			color = data.colorset[data.theme][4]
		else:
			color = data.colorset[data.theme][2]
		pygame.draw.rect(screen, color, pygame.Rect(left4 + (i * width4) + (i * hgap), top4 + ((9 - i) * vgap), width4, height4 - ((9 - i) * vgap)), border_radius=round(width4//2))


def draw_theme_blocks(left3, top3):
	for i in range(6):
		pygame.draw.rect(screen, data.colorset[data.theme][i], pygame.Rect(left3 + (i * data.scale_w(30)), top3, data.scale_w(30), data.scale_h(30)))


def move_up():
	target_x, target_y = data.coordinates[-1][0], data.coordinates[-1][1] + data.tile_gap + data.tile_size
	for i in range(data.mode * data.mode - 1):
		if data.no_diff(data.coordinates[i][0], target_x) and data.no_diff(data.coordinates[i][1], target_y):
			data.coordinates[i], data.coordinates[-1] = data.coordinates[-1], data.coordinates[i]
			data.moves += 1
			pygame.mixer.music.play()
			break


def move_down():
	target_x, target_y = data.coordinates[-1][0], data.coordinates[-1][1] - data.tile_gap - data.tile_size
	for i in range(data.mode * data.mode - 1):
		if data.no_diff(data.coordinates[i][0], target_x) and data.no_diff(data.coordinates[i][1], target_y):
			data.coordinates[i], data.coordinates[-1] = data.coordinates[-1], data.coordinates[i]
			data.moves += 1
			pygame.mixer.music.play()
			break


def move_left():
	target_x, target_y = data.coordinates[-1][0] + data.tile_gap + data.tile_size, data.coordinates[-1][1]
	for i in range(data.mode * data.mode - 1):
		if data.no_diff(data.coordinates[i][0], target_x) and data.no_diff(data.coordinates[i][1], target_y):
			data.coordinates[i], data.coordinates[-1] = data.coordinates[-1], data.coordinates[i]
			data.moves += 1
			pygame.mixer.music.play()
			break


def move_right():
	target_x, target_y = data.coordinates[-1][0] - data.tile_gap - data.tile_size, data.coordinates[-1][1]
	for i in range(data.mode * data.mode - 1):
		if data.no_diff(data.coordinates[i][0], target_x) and data.no_diff(data.coordinates[i][1], target_y):
			data.coordinates[i], data.coordinates[-1] = data.coordinates[-1], data.coordinates[i]
			data.moves += 1
			pygame.mixer.music.play()
			break


def completed():
	for i in range(data.mode * data.mode):
		if not (data.no_diff(data.coordinates[i][0], data.correct[i][0]) and data.no_diff(data.coordinates[i][1], data.correct[i][1])):
			return False
	return True


def shuffle(n):
	pygame.mixer.music.set_volume(0)

	for i in range(n):
		move_to_make = choice([move_up, move_down, move_left, move_right])
		move_to_make()
	data.moves = 0

	store_prime_state()

	pygame.mixer.music.set_volume(round(data.volume * 0.1, 1))


def store_prime_state():
	for i in range(data.mode * data.mode):
		data.stored[i] = data.coordinates[i]


def restore_prime_state():
	for i in range(data.mode * data.mode):
		data.coordinates[i] = data.stored[i]

	data.moves = 0
	data.finished = False
	data.start = data.end = datetime.now()


def time_format(seconds):
	minutes = str(seconds // 60).zfill(2)
	seconds = str(seconds % 60).zfill(2)
	return f"{minutes} : {seconds}"


def menu_screen():
	data.red, data.green, data.blue = data.increment(data.red), data.increment(data.green), data.increment(data.blue)
	r, g, b = data.transform(data.red), data.transform(data.green), data.transform(data.blue)
	render_text("assets/hey-comic.ttf", data.scale_h(100), "Sliding Puzzle", (r, g, b), data.scale_w(540), data.scale_h(120))

	simulate_button(data.scale_w(360), data.scale_h(310), data.scale_w(360), data.scale_h(80), data.scale_h(20), "menu-start", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "Start Game", data.colorset[data.theme][6], data.scale_w(540), data.scale_h(354), True)

	simulate_button(data.scale_w(360), data.scale_h(420), data.scale_w(360), data.scale_h(80), data.scale_h(20), "menu-instructions", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "Instructions", data.colorset[data.theme][6], data.scale_w(540), data.scale_h(464), True)

	simulate_button(data.scale_w(360), data.scale_h(530), data.scale_w(360), data.scale_h(80), data.scale_h(20), "menu-settings", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "Settings", data.colorset[data.theme][6], data.scale_w(540), data.scale_h(574), True)


def game_screen():
	if not data.finished:
		data.end = datetime.now()

	draw_blocks()

	pygame.draw.rect(screen, data.colorset[data.theme][5], pygame.Rect(data.scale_w(720), 0, data.scale_w(360), data.scale_h(720)))

	simulate_button(data.scale_w(750), data.scale_h(30), data.scale_w(300), data.scale_h(75), data.scale_h(20), "game-start", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "New Game", data.colorset[data.theme][6], data.scale_w(900), data.scale_h(72), bold=True)

	simulate_button(data.scale_w(750), data.scale_h(135), data.scale_w(300), data.scale_h(75), data.scale_h(20), "game-reset", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "Reset", data.colorset[data.theme][6], data.scale_w(900), data.scale_h(176), bold=True)

	simulate_button(data.scale_w(750), data.scale_h(240), data.scale_w(300), data.scale_h(75), data.scale_h(20), "game-menu", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "Main Menu", data.colorset[data.theme][6], data.scale_w(900), data.scale_h(280), bold=True)

	render_text("assets/fragment-core.otf", data.scale_h(40), "Time:", data.colorset[data.theme][6], data.scale_w(792), data.scale_h(679), bold=True)
	render_text("assets/fragment-core.otf", data.scale_h(40), time_format((data.end - data.start).seconds), data.colorset[data.theme][6], data.scale_w(907), data.scale_h(678))

	render_text("assets/fragment-core.otf", data.scale_h(40), "Moves:", data.colorset[data.theme][6], data.scale_w(802), data.scale_h(600), bold=True)
	render_text("assets/fragment-core.otf", data.scale_h(40), str(data.moves), data.colorset[data.theme][6], data.scale_w(900), data.scale_h(600))

	if completed():
		if not data.finished:
			data.finished = True

		overlay = pygame.Surface((data.scale_w(720), data.scale_h(720)))
		overlay.set_alpha(192)
		overlay.fill(data.black)
		screen.blit(overlay, (0, 0))
		render_text("assets/bromph-town.ttf", data.scale_h(64), "Congratulations!", data.colorset[data.theme][6], data.scale_w(360), data.scale_h(360))


def settings_screen():
	simulate_button(data.scale_w(20), data.scale_h(20), data.scale_w(90), data.scale_h(70), data.scale_h(20), "settings-back", "")
	pygame.draw.polygon(screen, data.colorset[data.theme][6], ((data.scale_w(47), data.scale_h(55)), (data.scale_w(77), data.scale_h(35)), (data.scale_w(77), data.scale_h(75))))

	pygame.draw.rect(screen, data.colorset[data.theme][5], pygame.Rect(data.scale_w(300), data.scale_h(260), data.scale_w(480), data.scale_h(90)), border_radius=round(data.scale_h(20)))
	pygame.draw.line(screen, data.colorset[data.theme][0], (data.scale_w(480), data.scale_h(275)), (data.scale_w(480), data.scale_h(335)))
	render_text("assets/fragment-core.otf", data.scale_h(40), "Volume", data.colorset[data.theme][6], data.scale_w(390), data.scale_h(310), True)
	simulate_button(data.scale_w(500), data.scale_h(285), data.scale_w(40), data.scale_h(40), data.scale_h(10), "settings-less", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "-", data.colorset[data.theme][6], data.scale_w(520), data.scale_h(304), True)
	simulate_button(data.scale_w(720), data.scale_h(285), data.scale_w(40), data.scale_h(40), data.scale_h(10), "settings-more", "")
	render_text("assets/fragment-core.otf", data.scale_h(40), "+", data.colorset[data.theme][6], data.scale_w(740), data.scale_h(303), True)
	draw_volume_bars(data.scale_w(555), data.scale_h(280), data.scale_w(6), data.scale_h(50), data.scale_w(10), data.scale_h(4))

	pygame.draw.rect(screen, data.colorset[data.theme][5], pygame.Rect(data.scale_w(300), data.scale_h(370), data.scale_w(480), data.scale_h(90)), border_radius=round(data.scale_h(20)))
	pygame.draw.line(screen, data.colorset[data.theme][0], (data.scale_w(480), data.scale_h(385)), (data.scale_w(480), data.scale_h(445)))
	render_text("assets/fragment-core.otf", data.scale_h(40), "Theme", data.colorset[data.theme][6], data.scale_w(390), data.scale_h(419), True)
	simulate_button(data.scale_w(525), data.scale_h(385), data.scale_w(210), data.scale_h(60), data.scale_h(15), "settings-theme-right", "settings-theme-left")
	pygame.draw.rect(screen, data.black, pygame.Rect(data.scale_w(539), data.scale_h(399), data.scale_w(182), data.scale_h(32)))
	draw_theme_blocks(data.scale_w(540), data.scale_h(400))


def refresh():
	data.tile_size = (680 - data.tile_gap * (data.mode - 1)) / data.mode

	data.coordinates = []
	data.correct = []
	data.stored = []
	for i in range(data.mode):
		for j in range(data.mode):
			temp = [data.tile_gap + (data.tile_gap + data.tile_size) * j, data.tile_gap + (data.tile_gap + data.tile_size) * i]
			data.coordinates.append(temp)
			data.correct.append(temp)
			data.stored.append(temp)


running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			if pygame.K_3 <= event.key <= pygame.K_7:
				data.mode = event.key - pygame.K_0
				refresh()
				shuffle(1000)
				data.finished = False
				data.start = data.end = datetime.now()

			if data.display_screen == 1 and not data.finished:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					move_up()
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					move_down()
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					move_left()
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					move_right()

		if event.type == pygame.MOUSEBUTTONDOWN:
			data.click = True

		if event.type == pygame.MOUSEBUTTONUP:
			data.click = False

			if data.signal == "menu-start":
				data.display_screen = 1
				shuffle(1000)
				data.start = data.end = datetime.now()
			if data.signal == "menu-instructions":
				system("notepad instructions.txt")
			if data.signal == "menu-settings":
				data.display_screen = 2
			if data.signal == "game-start":
				shuffle(1000)
				data.finished = False
				data.start = data.end = datetime.now()
			if data.signal == "game-reset":
				restore_prime_state()
			if data.signal == "game-menu":
				data.display_screen = 0
			if data.signal == "settings-back":
				data.display_screen = 0
			if data.signal == "settings-less" and data.volume > 0:
				data.volume -= 1
				pygame.mixer.music.set_volume(round(data.volume * 0.1, 1))
				pygame.mixer.music.play()
			if data.signal == "settings-more" and data.volume < 10:
				data.volume += 1
				pygame.mixer.music.set_volume(round(data.volume * 0.1, 1))
				pygame.mixer.music.play()
			if data.signal == "settings-theme-right":
				data.theme += 1
				data.theme %= len(data.colorset)
			if data.signal == "settings-theme-left":
				data.theme -= 1
				data.theme %= len(data.colorset)

			data.signal = ""

	screen.fill(data.colorset[data.theme][0])

	if data.display_screen == 0:
		menu_screen()
	if data.display_screen == 1:
		game_screen()
	if data.display_screen == 2:
		settings_screen()

	pygame.display.update()

pygame.quit()

with open("assets/globals.py", 'r') as file:
	all_lines = file.read().split('\n')

for ii in range(len(all_lines)):
	if "mode = " in all_lines[ii]:
		all_lines[ii] = f"mode = {data.mode}"
	elif "theme = " in all_lines[ii]:
		all_lines[ii] = f"theme = {data.theme}"
	elif "volume = " in all_lines[ii]:
		all_lines[ii] = f"volume = {data.volume}"

with open("assets/globals.py", 'w') as file:
	file.write('\n'.join(all_lines))
