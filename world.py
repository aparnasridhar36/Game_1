class MapTile:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def intro_text(self):
		raise NotImplementedError("Create a subclass instead!")
	description = "Do not create raw MapTiles! Create a subclass instead!"
	enemies = []
	items = []

class StartTile(MapTile):
	def intro_text(self):
		return """You find yourself in a maze with musty gray walls.
		You can make out four paths, each equally as dark and foreboding.
		"""


class BoringTile(MapTile):
	def intro_text(self):
		return """This is a very boring part of the maze."""

		
		
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
		

class SecretTile(MapTile):
	def intro_text(self):
		return """You've entered a secret dead end."""
		
class World:									# I choose to define the world as a class. This makes it more straightforward to import into the game.
	map = [
		[None,							None, 							FireElementTileTile(), 				None					None],
		[None,							None, 							BoringTile(), 					None					None],
		[EarthElementTile(),				BoringTile(), 							StartTile(), 					BoringTile(), 				AirElementTile()],
		[None,							None, 							BoringTile(), 					None					None],
		[SecretTile(),					BoringTile(), 							WaterElementTile() 				None					None]
	]
	
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
		if y-1 < 0:
			room = None
		try:
			room = self.map[y-1][x]
		except IndexError:
			room = None
		
		if(room):
			return [True, "You head to the north."]
		else:
			return [False, "There doesn't seem to be anything to the north."]
			
	def check_south(self, x, y):
		if y+1 < 0:
			room = None
		try:
			room = self.map[y+1][x]
		except IndexError:
			room = None
		
		if(room):
			return [True, "You head to the south."]
		else:
			return [False, "There doesn't seem to be anything to the south."]

	def check_west(self, x, y):
		if x-1 < 0:
			room = None
		try:
			room = self.map[y][x-1]
		except IndexError:
			room = None
		
		if(room):
			return [True, "You head to the west."]
		else:
			return [False, "There doesn't seem to be anything to the west."]
			
	def check_east(self, x, y):
		if x+1 < 0:
			room = None
		try:
			room = self.map[y][x+1]
		except IndexError:
			room = None
		
		if(room):
			return [True, "You head to the east."]
		else:
			return [False, "There doesn't seem to be anything to the east."]
