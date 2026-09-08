total_drones = 7

def CutLane():
	for _ in range(get_world_size()):
		harvest()
		if (get_pos_x() + get_pos_y()) % 2 == 0:
			plant(Entities.Tree)
		else:
			plant(Entities.Bush)
		move(East)
	
clear()
set_world_size(total_drones*2)
while True:
	if total_drones - num_drones() > 0:
		spawn_drone(CutLane)
		move(North)