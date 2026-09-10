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

def BitOne(addToFixed=False):
	pos = (get_pos_x(),get_pos_y())
	if pos in FixedPixels:
		print("Already Fixed! " + str(pos))
	else:
		if get_ground_type() != Grounds.Soil:
			till()
		if addToFixed:
			FixedPixels.append(pos)

def BitZero(addToFixed=False):
	pos = (get_pos_x(),get_pos_y())
	if pos in FixedPixels:
		print("Already Fixed!" + str(pos))
	else:
		if get_ground_type() != Grounds.Grassland:
			till()
		if get_entity_type() != Entities.Bush:
			plant(Entities.Bush)
		if addToFixed:
			FixedPixels.append(pos)

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
				BitZero(True)
			else:
				BitOne(True)

def AlignmentPattern(x, y):
	center = 2
	for r in range(5):
		for c in range(5):
			MoveTo(x+c, r+y)
			dist = max(abs(r - center), abs(c - center))
			if dist == 1:
				BitZero(True)
			else:
				BitOne(True)

def TimingPattern():
	# Horizontale Timing Pattern op Y = 22 (rij 6 vanaf de bovenkant)
	# MOET in FixedPixels staan
	MoveTo(7, 22)
	for x in range(8, 21):
		move(East)
		if x % 2 == 0:
			BitOne(True)
		else:
			BitZero(True)

	# Verticale Timing Pattern op X = 6 (van Y = 8 t/m 20)
	# Mag NIET in FixedPixels staan (kolom 6 wordt door TraverseQRGrid overgeslagen)
	MoveTo(6, 7)
	for y in range(8, 21):
		move(North)
		if y % 2 == 0:
			BitOne(True)
		else:
			BitZero(True)

def FormatString():
	l = library.FORMAT_STRING_BITS
	for pos in l:
		x = pos[0]
		y = pos[1]
		bit = l[pos]
		MoveTo(x, y)
		if bit == 0:
			BitZero(True)
		else:
			BitOne(True)

def ConstantPatterns():
	FinderPattern(-1, -1)
	FinderPattern(-1, 21)
	FinderPattern(21, 21)
	AlignmentPattern(20, 4)
	TimingPattern()
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

def ExecuteBitAction(bit):
	# MASK 0 TOEPASSING: (row + column) % 2 == 0
	# Bij Mask 0 wordt de bit geïnverteerd als (x + y) % 2 == 0
	x = get_pos_x()
	y = get_pos_y()
	
	if (x + y) % 2 == 0:
		# Inverteer het bit
		if bit == 0:
			bit = 1
		else:
			bit = 0

	# Plaats het (eventueel gemaskerde) bit op het veld
	if bit == 0:
		BitZero()
	elif bit == 1:
		BitOne()
	
def TraverseQRGrid(FixedPixels, DataBitsList):
	reserved = set(FixedPixels)
	index = 0
	total_bits = len(DataBitsList)

	# Start bij de meest rechte kolom-pair (col = 28 en 27)
	col = 28
	while col > 0:
		# Sla de verticale timing-strip (kolom 6) over
		if col == 6:
			col -= 1
			continue

		# Bepaal de verticaal door te lopen Y-waardes
		# Kolom 28-27 gaat OMHOOG, 26-25 omlaag, etc.
		# Aangezien we van rechts (28) naar links werken, berekenen we de richting:
		col_pair_index = (28 - col) // 2
		moving_up = (col_pair_index % 2 == 0)
		
		if moving_up:
			y_range = range(0, 29)
		else:
			y_range = range(28, -1, -1)
			
		
		

		for y in y_range:
			# Verwerk de 2 kolommen van rechts naar links: c = col, daarna c = col - 1
			for c in [col, col - 1]:
				MoveTo(c, y)
				if (c, y) not in reserved:
					if index < total_bits:
						ExecuteBitAction(DataBitsList[index])
						index += 1
		col -= 2

def DataBits():
	# Modus indicator: Byte mode (0100)
	DataBitsList = [0,1,0,0]
	DataBitsList += GetBinaryCharCount(input)
	
	# Karakters toevoegen
	for i in range(len(input)):
		byte = library.ASCII_BINARY_MAP[input[i]]
		DataBitsList += byte
	
	# Terminator (4 nullen)
	DataBitsList += [0,0,0,0]
	
	# Opvullen tot exact 440 bits (55 bytes)
	while len(DataBitsList) < 440:
		DataBitsList += library.REPEATING_PATTERN_A
		if len(DataBitsList) < 440:
			DataBitsList += library.REPEATING_PATTERN_B
	
	# Zorg dat we exact 440 bits overhouden
	return DataBitsList[:440]

# --- REED-SOLOMON ERROR CORRECTION LOGICA ---
def xor_bytes(a, b):
	result = 0
	multiplier = 1
	for _ in range(8):
		bit_a = a % 2
		bit_b = b % 2
		
		if bit_a != bit_b:
			result = result + multiplier
			
		a = a // 2
		b = b // 2
		multiplier = multiplier * 2
	return result

GF_SIZE = 256
PRIMITIVE_POLY = 285

exp_table = []
log_table = []
for _ in range(GF_SIZE):
	exp_table.append(0)
	log_table.append(0)

x = 1
for i in range(256):
	exp_table[i] = x
	log_table[x] = i
	x = x * 2
	if x >= 256:
		x = xor_bytes(x, PRIMITIVE_POLY)

def gf_mul(x, y):
	if x == 0 or y == 0:
		return 0
	return exp_table[(log_table[x] + log_table[y]) % 255]

def get_generator_poly_15():
	g = [1]
	for i in range(15):
		next_g = []
		for _ in range(len(g) + 1):
			next_g.append(0)
			
		for j in range(len(g)):
			next_g[j] = xor_bytes(next_g[j], g[j])
			next_g[j + 1] = xor_bytes(next_g[j + 1], gf_mul(g[j], exp_table[i]))
		g = next_g
	return g

def generate_ec_bytes(data_bytes, ec_count=15):
	gen_poly = get_generator_poly_15()
	
	res = list(data_bytes)
	for _ in range(ec_count):
		res.append(0)

	for i in range(len(data_bytes)):
		coef = res[i]
		if coef != 0:
			for j in range(1, len(gen_poly)):
				res[i + j] = xor_bytes(res[i + j], gf_mul(gen_poly[j], coef))

	return res[len(data_bytes):]
	
def bits_to_bytes(bit_list):
	bytes_list = []
	for i in range(0, len(bit_list), 8):
		byte_val = 0
		for bit in bit_list[i:i+8]:
			byte_val = (byte_val * 2) + bit
		bytes_list.append(byte_val)
	return bytes_list

def bytes_to_bits(byte_list):
	bit_list = []
	for b in byte_list:
		bit_list.append((b // 128) % 2)
		bit_list.append((b // 64) % 2)
		bit_list.append((b // 32) % 2)
		bit_list.append((b // 16) % 2)
		bit_list.append((b // 8) % 2)
		bit_list.append((b // 4) % 2)
		bit_list.append((b // 2) % 2)
		bit_list.append(b % 2)
	return bit_list

def generate_full_data_bits(DataBitsList):
	data_bytes = bits_to_bytes(DataBitsList)
	ec_bytes = generate_ec_bytes(data_bytes, 15)
	ec_bits = bytes_to_bits(ec_bytes)
	full_bits = DataBitsList + ec_bits + [0,0,0,0,0,0,0]
	return full_bits

# --- HOOFDPROGRAMMA ---
set_world_size(size)
FixedPixels = []

# 1. Vaste patronen plaatsen
ConstantPatterns()

# 2. Data generator & Error Correction berekenen
raw_data_bits = DataBits()
FullDataBitsList = generate_full_data_bits(raw_data_bits)

# 3. Traverseren en data + mask direct plaatsen
TraverseQRGrid(FixedPixels, FullDataBitsList)

# 4. Log
quick_print(FullDataBitsList)

while True:
	pass