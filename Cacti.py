def back(x=0,y=0):
	while x != get_pos_x() and y != get_pos_y():
		if x - get_pos_x() > 0:
			move(East)
		else:
			move(West)
		if y - get_pos_y() > 0:
			move(North)
		else:
			move(South)

def plantCactus():
	if get_ground_type()==Grounds.Grassland:
		till()
	plant(Entities.Cactus)  

def reverse(dir):
	if(dir == West):
		return East
	if(dir == East):
		return West
	if(dir == North):
		return South
	if(dir == South):
		return North

def cactusProject(size=3):
	set_world_size(size)
	while True:
		dir=East
		vdir=North
		sorted=False
		vsorted=False
		
		for i in range(size):
			for j in range(size):
				plantCactus()
				if(j!=size-1):
					move(dir)
			if(i!=size-1):
				move(vdir)
			dir=reverse(dir)
		vdir=reverse(vdir)
		
		while not sorted or not vsorted:
			sorted=True
			vsorted=True
			for i in range(size):
				for j in range(size):
					x=get_pos_x()
					y=get_pos_y()
					current=measure()
					neighbor=measure(dir)
					down=measure(South)
					up=measure(North)
					
					# Logic to swap East/West
					if(x!=size-1 and neighbor!=None and dir==East and current>neighbor):
						swap(East)
						sorted=False
					if(x!=0 and neighbor!=None and dir==West and current<neighbor):
						swap(West)
						sorted=False
						
					# Logic to swap North/South
					if(y!=0 and down != None and current<down):
						swap(South)
						vsorted=False
					if up != None:
						if y != size-1 and current > up:
							swap(North)
							vsorted = False			
	
					if(j!=size-1):
						move(dir)
				if(i!=size-1):
					move(vdir)
				dir=reverse(dir)
			vdir=reverse(vdir)
		
		back()
		harvest()
		
clear()
cactusProject(6)