total_drones = 7

def HarvestLane():
	for x in range(get_world_size()):
		harvest()	
		if x < (get_world_size() / 3) // 1:
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Carrot)
		elif (get_pos_x() + get_pos_y()) % 2 == 0:
			plant(Entities.Grass)
		else:
			plant(Entities.Tree)
		move(East)

clear()
while True:
	if total_drones - num_drones() > 0:
		spawn_drone(HarvestLane)
		move(North)