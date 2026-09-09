total_drones = 7

def HarvestLane():
	while num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)
		harvest()
		move(East)

clear()
set_world_size(total_drones+1)
for _ in range(total_drones):
	spawn_drone(HarvestLane)
	move(North)
HarvestLane()