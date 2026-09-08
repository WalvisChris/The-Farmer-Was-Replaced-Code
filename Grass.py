def SnakeStep():
	x, y = get_pos_x(), get_pos_y()
	if x % 2 == 0:
		if y == get_world_size() - 1:
			move(East)
		else:
			move(North)
	else:
		if y == 0:
			move(East)
		else:
			move(South)

clear()			
while True:
	harvest()
	SnakeStep()