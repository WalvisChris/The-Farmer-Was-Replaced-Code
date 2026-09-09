# https://www.youtube.com/watch?v=ZizmvuZ3EFk&t=803s
# https://www.thonky.com/qr-code-tutorial/mask-patterns
import library

input = "hello world"
size = 29
# mode: 			byte (0100)
# version: 			3 (29x29)
# ECC: 				L (01)
# Mask: 			0
# Format String: 	111011111000100

def BitOne():
	if (get_pos_x(),get_pos_y()) in FinishedPixels:
		print("Already Finished!")
	if get_ground_type() != Grounds.Soil:
		till()
	FinishedPixels.append((get_pos_x(),get_pos_y()))

def BitZero():
	if (get_pos_x(),get_pos_y()) in FinishedPixels:
		print("Already Finished!")
	if get_ground_type() != Grounds.Grassland:
		till()
	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)
	FinishedPixels.append((get_pos_x(),get_pos_y()))

def MoveTo(x=0, y=0):
	while get_pos_x() != x or get_pos_y() != y:
		if get_pos_x() > x:
			move(West)
		elif get_pos_x() < x:
			move(East)
		if get_pos_y() > y:
			move(South)
		elif get_pos_y() < y:
			move(North)
			
def FinderPattern(x, y):
	center = 4
	for r in range(9):
		target_y = y + r
		if target_y < 0 or target_y >= get_world_size():
			continue
		for c in range(9):
			target_x = x + c
			if target_x < 0 or target_x >= get_world_size():
				continue
			MoveTo(target_x, target_y)
			dist = max(abs(r - center), abs(c - center))
			if dist == 2 or dist == 4:
				BitZero()
			else:
				BitOne()

def AlignmentPattern(x, y):
	center = 2
	for r in range(5):
		for c in range(5):
			MoveTo(x+c, r+y)
			dist = max(abs(r - center), abs(c - center))
			if dist == 1:
				BitZero()
			else:
				BitOne()

def TimingPattern(r):
	direction = {0:South, 1:East}
	steps = 0
	MoveTo(6, 22)
	move(direction[r])
	for _ in range(13):
		move(direction[r])
		if steps % 2 == 1:
			BitZero()
		else:
			BitOne()
		steps += 1

def FormatString():
	l = library.FORMAT_STRING_BITS
	for pos in l:
		x = pos[0]
		y = pos[1]
		bit = l[pos]
		MoveTo(x, y)
		if bit == 0:
			BitZero()
		else:
			BitOne()

def ConstantPatterns():
	FinderPattern(-1, -1)
	FinderPattern(-1, 21)
	FinderPattern(21, 21)
	AlignmentPattern(20, 4)
	TimingPattern(0)
	TimingPattern(1)
	FormatString()

def GetBinaryCharCount(s):
	n = len(s)
	byte = []
	for i in range(7, -1, -1):
		power = 2**i
		if n >= power:
			byte.append(1)
			n -= power
		else:
			byte.append(0)
	return byte
	
def WalkData():
	MoveTo(28,0)

def DataBits():
	DataBitsList = [0,1,0,0]
	DataBitsList += GetBinaryCharCount(input)
	
	# add characters one by one
	for i in range(len(input)):
		byte = library.ASCII_BINARY_MAP[input[i]]
		DataBitsList += byte
	
	# add 4 zeros
	DataBitsList += [0,0,0,0]
	
	# fill untill 440 bits
	while len(DataBitsList) < 440:
		DataBitsList += library.REPEATING_PATTERN_A
		if len(DataBitsList) < 440:
			DataBitsList += library.REPEATING_PATTERN_B
	
def ECCBits():
	pass

def Mask():
	pass

set_world_size(size)
FinishedPixels = []

# QR Logic
ConstantPatterns()
DataBits()
ECCBits()
Mask()