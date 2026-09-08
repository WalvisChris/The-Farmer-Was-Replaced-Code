def CutLane():
	for _ in range(get_world_size()):
		harvest()
		move(East)
	
clear()
total_drones = 7
set_world_size(total_drones)
while True:
	if total_drones - num_drones() > 0:
		spawn_drone(CutLane)
		move(North)