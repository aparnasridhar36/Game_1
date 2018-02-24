#!/usr/bin/env python3
class Item:
	self.name = "Do not create raw Item objects!"
	self.description = "You should define a description for items in their subclass."
	self.dropped_description = "You should define the description for this item after it is dropped in its subclass."
	
	is_dropped = False	# This is going to store the status of whether this item has been picked up and dropped before.
	
		
	def __init__(self, description = ""):
		if(description):
			self.intro_description = description
		else:
			self.intro_description = self.dropped_description
			
	def __str__(self):
		return self.name	

	def room_text(self):
		if(not self.is_dropped):					# We may want to have a different description for a weapon the first time it is encountered vs. after it has been dropped.
			return self.intro_description
		else:
			return self.dropped_description

	def check_text(self):
		return self.description
		
	def drop(self):
		self.is_dropped = True
		
	def pick_up(self):
		self.is_dropped = False
		
	def handle_input(self, verb, noun1, noun2, inventory):
		return [False, None, inventory]

class Crowbar(Item):
	def __init__(self):
		self.name = "Crowbar"
		self.description = "A normal crowbar. Great for knocking people out."
		self.dropped_description = "A normal crowbar is dropped on the floor in front of you."
		self.damage = 10

	def __str__(self):
		return self.name

class Axe(Item):
	def __init__(self):
		self.name = "Axe"
		self.descrption = "An axe. Blade is slightly blunt."
		self.dropped_description = "An axe is dropped on the floor in front of you."
		self.damage = 15

	def __str__(self):
		return self.name

class Knife(Item):
	def __init__(self):
		self.name = "Knife"
		self.description = "A very sharp knife."
		self.dropped_description = "A knife is dropped on the floor in front of you."
		self.damage = 20

	def __str__(self):
		return self.name

class Consumable(Item):
	consume_description = "You should define flavor text for consuming this item in its subclass."

	healing_value = 0		# Define this appropriately in your subclass.
		
	def consume(self):
		return [self.consume_description, self.healing_value]

class Apple(Consumable):
	self.name = "apple"
	self.healing_value = 10
	
	self.description = "A juicy red apple."
	self.dropped_description = "An apple is dropped in front of you."
	
class Container:
	name = "Do not create raw Container objects!"
	
	closed_description = "You should define a closed description for containers in their subclass."
	open_description = "You should define an open description for containers in their subclass."
	
	closed = True
	
	contents = []
	
	def __init__(self, items = []):
		for item in items:
			if(len(self.contents) == 0):
				self.contents = [item]
			else:
				self.contents.append(item)
	
	def add_item(self, item):
		if(len(self.contents) == 0):
			self.contents = [item]		# Initialize the list if it is empty.
		else:
			self.contents.append(item)	# Add to the list if it is not empty.
			
	def remove_item(self, item):
		removal_index = -1
		for index in range(len(self.contents)):
			if(self.contents[index].name == item.name):
				removal_index = index
		if(removal_index >= 0):
			self.contents.pop(removal_index)
	
			
	def __str__(self):
		return self.name	

	def room_text(self):
		if(self.closed):					# We may want to have a different description for a container if it is open or closed.
			return self.closed_description
		else:
			return self.open_description

	def check_text(self):
		if(self.closed):
			return self.closed_description
		else:
			if(len(self.contents) > 0):
			
				print("The %s contains:" % self.name)
				for item in self.contents:
					print('* ' + str(item).title())
			else:
				return "The %s is empty." % self.name
		
	def handle_input(self, verb, noun1, noun2, inventory):			
		return [False, "", inventory]

class Chest(Container)
	self.name = "chest"
	self.closed_description = "A wooden chest sits against the wall, its lid shut tightly."
	self.open_description = "A wooden chest sits against the wall, its lid open wide."
	
	
	def handle_input(self, verb, noun1, noun2, inventory):
		if(noun1 == self.name):
			if(verb == 'check'):
				return [True, self.check_text(), inventory]
			if(verb == 'open'):
				if(self.closed == True):
					self.closed = False
					return [True, "You pry the lid of the wooden chest open.", inventory]
				else:
					return [True, "The wooden chest is already wide open.", inventory]
			if(verb == 'close'):
				if(self.closed == False):
					self.closed = True
					return [True, "You close the lid of the wooden chest.", inventory]
				else:
					return [True, "The woodennn chest is already closed.", inventory]
		elif(noun1):
			if(verb == 'take'):
				if(not self.closed):
					for index in range(len(self.contents)):
						if(self.contents[index].name.lower() == noun1):
							if(isinstance(self.contents[index], Item)):
								pickup_text = "You took the %s from the old chest and added it to your inventory." % self.contents[index].name
								inventory.append(self.contents[index])
								self.contents.pop(index)
								return [True, pickup_text, inventory]
							else:
								return [True, "The %s is too heavy to pick up." % self.contents[index].name, inventory]
			if(verb == 'check'):
				if(not self.closed):
					for index in range(len(self.contents)):
						if(self.contents[index].name.lower() == noun1):
							if(isinstance(self.contents[index], Item)):
								return [True, self.contents[index].check_text(), inventory]
		return [False, None, inventory]

	
def play():
	inventory = [Knife()]
	print("Defeat the enemy and escape the maze")
	
