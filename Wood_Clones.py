max_drones = 16

def CutLane():
	for _ in range(get_world_size()):
		if can_harvest():
			harvest()
			if (get_pos_x() + get_pos_y()) % 2 == 0:
				plant(Entities.Tree)
			else:
				plant(Entities.Bush)
		move(East)
	
clear()
set_world_size(max_drones)
while True:
	if max_drones > num_drones():
		spawn_drone(CutLane)
		move(North)