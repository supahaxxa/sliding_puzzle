from math import floor, pi, sin


increment = lambda n: (n + 0.5) % 180
no_diff = lambda a, b: abs(a - b) < 0.1
scale_h = lambda n: n / 720 * window_height
scale_w = lambda n: n / 1080 * window_width
transform = lambda n: floor(255 * sin(n * pi / 180))

window_width, window_height = 1080, 720

display_screen = 0
mode = 5					# need to save its state
moves = 0
theme = 0					# need to save its state
volume = 0					# need to save its state
start = end = 0

tile_gap = 20
tile_size = (680 - tile_gap * (mode - 1)) / mode

black = "#000000"
red, green, blue = 0, 45, 90
colorset = [
	["#051720", "#03273C", "#004D74", "#006494", "#006DA4", "#003554", "#C0C0C0"],
	["#05161A", "#072E33", "#0C7075", "#0F969C", "#6DA5C0", "#294D61", "#C0C0C0"],
	["#143601", "#1A4301", "#538D22", "#73A942", "#AAD576", "#245501", "#190019"],
	["#0A2344", "#3B1D4A", "#9C1057", "#CC095D", "#FD0363", "#6B1650", "#190019"],
	["#7F5539", "#9C6644", "#DDB892", "#E6CCB2", "#EDE0D4", "#B08968", "#190019"],
	["#618943", "#82AA57", "#C5D86D", "#F2EFBB", "#F9F7DC", "#9EBC63", "#190019"],
	["#B9375E", "#E05780", "#FF9EBB", "#FFC2D4", "#FFE0E9", "#FF7AA2", "#190019"]
]

coordinates = []
correct = []
stored = []
for i in range(mode):
	for j in range(mode):
		temp = [tile_gap + (tile_gap + tile_size) * j, tile_gap + (tile_gap + tile_size) * i]
		coordinates.append(temp)
		correct.append(temp)
		stored.append(temp)

click = False
finished = False

signal = ""
