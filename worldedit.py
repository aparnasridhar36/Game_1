import items
import barriers

class MapTile:
	description = "Do not create raw MapTiles! Create a subclass instead!"
	
	def __init__(self, x=0, y=0, barriers = [], items = [], enemies = []):
		self.x = x
		self.y = y
		self.contents = {'barriers': barriers, 'enemies': enemies, 'items': items}	# A dict containing all the contents of the room.
	
	def intro_text(self):
		text = self.description
		for barrier in self.contents['barriers']:
			if(barrier.verbose):
				text += " " + barrier.description()
		#for enemy in self.contents['enemies']:
		#	text += " " + enemy.description()
		for item in self.contents['items']:
			text += " " + item.room_text()
		return text
		
	def handle_input(self, verb, noun1, noun2, inventory):
		if(not noun2):
			if(verb == 'check'):
				for item in self.contents['items']:
					if(item.name.lower() == noun1):
						return [True, item.check_text(), inventory]
			elif(verb == 'take'):
				for index in range(len(self.contents['items'])):
					if(self.contents['items'][index].name.lower() == noun1):
						pickup_text = "You picked up the %s." % self.contents['items'][index].name
						inventory.append(self.contents['items'][index])
						self.contents['items'].pop(index)
						return [True, pickup_text, inventory]
			elif(verb == 'drop'):
				for index in range(len(inventory)):
					if(inventory[index].name.lower() == noun1):
						inventory[index].is_dropped = True
						drop_text = "You dropped the %s." % inventory[index].name
						if(len(self.contents['items']) > 0):
							self.contents['items'].append(inventory[index])
						else:
							self.contents['items'] = [inventory[index]]
						inventory.pop(index)
						return [True, drop_text, inventory]

		for key in self.contents.keys():
			for item in self.contents[key]:
				[status, description, inventory] = item.handle_input(verb, noun1, noun2, inventory)
				if(status):
					return [status, description, inventory]
			
		return [False, "", inventory]


class StartTile(MapTile):
	def intro_text(self):
		return """You find yourself in a maze with musty gray walls.
		You can make out four paths, each equally as dark and foreboding.
		"""
		
	
class FireElementTile(MapTile):
	def intro_text(self):
		return """You've entered the fire element! Don't get burnt!"""
			
class WaterElementTile(MapTile):
	def intro_text(self):
		return """You've entered the water element! Don't get soaked!"""
		
class AirElementTile(MapTile):
	def intro_text(self):
		return """You've entered the air element! Don't get blown away!"""
				
class EarthElementTile(MapTile):
	def intro_text(self):
		return """You've entered the earth element! Watch for dirt!"""

class Corridor(MapTile):
	description = """You find yourself in a poorly lit corridor. This is a very boring part of the maze."""
		
class StoreRoom(MapTile):
	description = """You seem to have entered an underground storeroom!"""
		
class ExpanseSW(MapTile):
	description = """You find yourself in an expansive cavern, with walls stretching out nearly as far as the eye can see. The room opens before you to the northeast."""
	
class ExpanseSE(MapTile):
	description = """You find yourself in an expansive cavern, with walls stretching out nearly as far as the eye can see. The room opens before you to the northwest. There is a small corridor leading to the east from here."""
	
class ExpanseNW(MapTile):
	description = """You find yourself in an expansive cavern, with walls stretching out nearly as far as the eye can see. The room opens before you to the southeast. There is a small corridor leading to the north from here."""
	
class ExpanseNE(MapTile):
	description = """You find yourself in an expansive cavern, with walls stretching out nearly as far as the eye can see. The room opens before you to the southwest. A small nook lies to your east."""

class Nook(MapTile):
	description = """You have entered a dank nook of the cave. The only way out is back the way you came."""
				
class NearVictory(MapTile):
	description = """You can see a light to the east at the end of this corridor. Could that be your way out?"""

class VictoryTile(MapTile):
	description = """You see a bright light in the distance...
		It grows as you get closer! It's sunlight!	
		Victory is yours!
		"""
		
class World:									# I choose to define the world as a class. This makes it more straightforward to import into the game.
	map = [
		[Corridor(barriers = [barriers.Wall('e'), barriers.Wall('n')]),													NearVictory(barriers = [barriers.Wall('s')]),								VictoryTile(),																							Corridor(barriers = [barriers.Wall('w')]), 											Corridor()],
		[None,																											ExpanseNE(barriers = [barriers.Wall('n')]),	 								Corridor(barriers = [barriers.Wall('e'), barriers.Wall('w')]), 											Corridor(barriers = [barriers.Wall('e'), barriers.Wall('w')]),						Corridor(barriers = [barriers.Wall('w')])],
		[EarthElementTile(barriers = [barriers.Wall('n'), barriers.Wall('s')]),											Corridor(barriers = [barriers.Wall('n'), barriers.Wall('s')]), 				StartTile(), 																							Corridor(barriers = [barriers.Wall('n'), barriers.Wall('s')]),		 				Corridor(barriers = [barriers.Wall('w')])],
		[None,																											None,																		Corridor(barriers = [barriers.Wall('e'), barriers.Wall('w')]), 											Corridor(barriers = [barriers.Wall('n')]), 											Corridor()],
		[Nook(),																										Corridor(barriers = [barriers.WoodenDoor('w')]),							Corridor(barriers = [barriers.Wall('w')]),																None,																				None]
	]
	
#StoreRoom(barriers = [barriers.Wall('n')], items = [items.RustySword("A rusty sword is propped against the wall.")]), >> how to items/barriers

	def __init__(self):
		for i in range(len(self.map)):			# We want to set the x, y coordinates for each tile so that it "knows" where it is in the map.
			for j in range(len(self.map[i])):	# I prefer to handle this automatically so there is no chance that the map index does not match
				if(self.map[i][j]):				# the tile's internal coordinates.
					self.map[i][j].x = j
					self.map[i][j].y = i
					
	def tile_at(self, x, y):
		if x < 0 or y < 0:
			return None
		try:
			return self.map[y][x]
		except IndexError:
			return None
			
	def check_north(self, x, y):
		for barrier in self.map[y][x].contents['barriers']:
			if(barrier.direction == 'north' and not barrier.passable):
				return [False, barrier.description()]				
				
		if y-1 < 0:
			room = None
		else:
			try:
				room = self.map[y-1][x]
			except IndexError:
				room = None
		
		if(room):
			return [True, "You head to the north."]
		else:
			return [False, "There doesn't seem to be a path to the north."]
			
	def check_south(self, x, y):
		for barrier in self.map[y][x].contents['barriers']:
			if(barrier.direction == 'south' and not barrier.passable):
				return [False, barrier.description()]	
				
		if y+1 < 0:
			room = None
		else:
			try:
				room = self.map[y+1][x]
			except IndexError:
				room = None
		
		if(room):
			return [True, "You head to the south."]
		else:
			return [False, "There doesn't seem to be a path to the south."]

	def check_west(self, x, y):
		for barrier in self.map[y][x].contents['barriers']:
			if(barrier.direction == 'west' and not barrier.passable):
				return [False, barrier.description()]	
	
		if x-1 < 0:
			room = None
		else:
			try:
				room = self.map[y][x-1]
			except IndexError:
				room = None
		
		if(room):
			return [True, "You head to the west."]
		else:
			return [False, "There doesn't seem to be a path to the west."]
			
	def check_east(self, x, y):
		for barrier in self.map[y][x].contents['barriers']:
			if(barrier.direction == 'east' and not barrier.passable):
				return [False, barrier.description()]	
				
		if x+1 < 0:
			room = None
		else:
			try:
				room = self.map[y][x+1]
			except IndexError:
				room = None
		
		if(room):
			return [True, "You head to the east."]
		else:
			return [False, "There doesn't seem to be a path to the east."]