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
	count = 0
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			
			if can_harvest():
				harvest()
			
			if i > (get_world_size() / 3) // 1:
				if count % 2 == 0:
					plant(Entities.Tree)
			else:
				if get_ground_type() == Grounds.Grassland:
					till()
				plant(Entities.Carrot)
			
			SnakeStep()
			count += 1