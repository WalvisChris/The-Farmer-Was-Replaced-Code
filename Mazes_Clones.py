directions = {0: North, 1: East, 2: South, 3: West}
maze_upgrade_level = 3
max_drones = 8

def MoveTo(x, y):
	# horizontal
	while get_pos_x() != x:
		if x - get_pos_x() > 0:
			move(East)
		else:
			move(West)
	# vertical
	while get_pos_y() != y:
		if y - get_pos_y() > 0:
			move(North)
		else:
			move(South)

def SolveMazeLeft():
	rotation = 0
	while get_entity_type() == Entities.Hedge:
		attempt = (rotation + 3) % 4
		if can_move(directions[attempt]):
			rotation = attempt
			move(directions[rotation])
		elif can_move(directions[rotation]):
			move(directions[rotation])
		else:
			rotation = (rotation + 1) % 4
			move(directions[rotation])
	if get_entity_type() == Entities.Treasure:
		harvest()

def SolveMazeRight():
	rotation = 0
	while get_entity_type() == Entities.Hedge:
		attempt = (rotation + 1) % 4
		if can_move(directions[attempt]):
			rotation = attempt
			move(directions[rotation])
		elif can_move(directions[rotation]):
			move(directions[rotation])
		else:
			rotation = (rotation + 3) % 4
			move(directions[rotation])
	if get_entity_type() == Entities.Treasure:
		harvest()

def SolveMazeRandom():
	rotation = 0
	steps = 0
	while get_entity_type() == Entities.Hedge:
		rotation = random() * 4 // 1
		move(directions[rotation])
		steps += 1
		if steps > 50 and max_drones > num_drones():
			spawn_drone(SolveMazeRandom)
			steps = 0
	if get_entity_type() == Entities.Treasure:
		harvest()

clear()
while True:
	MoveTo(0, 0)
	
	if get_entity_type() == Entities.Hedge:
		spawn_drone(SolveMazeLeft)
		spawn_drone(SolveMazeRight)
		SolveMazeRandom()
		
	elif get_entity_type() != Entities.Bush:
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, get_world_size()*(2**maze_upgrade_level))