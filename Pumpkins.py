clear()
change_hat(Hats.Pumpkin_Hat)
pumpkin_cost = get_cost(Entities.Pumpkin)
total_tiles = get_world_size() * get_world_size()
pumkin_need = pumpkin_cost[Items.Carrot] * total_tiles
progress = 0

while True:
	if num_items(Items.Carrot) < pumkin_need:
		print("Not enough carrots! ", num_items(Items.Carrot), "/", pumkin_need)
	else:
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				
				if get_ground_type() != Grounds.Soil:
					till()
				
				if get_entity_type() != Entities.Pumpkin:
					plant(Entities.Pumpkin)
					progress = 0
				
				if (x % 2 == 0):
					if (get_pos_y() < get_world_size()-1):
						move(North)
				else:
					if (get_pos_y() > 0):
						move(South)
				
				if progress >= total_tiles:
					harvest()
				
				progress += 1
					
			move(East)