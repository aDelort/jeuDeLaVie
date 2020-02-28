## Class definition

class MadeObject():
	def __init__(self,name,aliveCellsList):
		self._name = name
		self._aliveCellsList = aliveCellsList

	def getName(self):
		return self._name

	def getMatrix(self):
		return self._aliveCellsList


## List of objects
objectsList = []

#Slider
mat = [(1,0),(2,1),(2,2),(1,2),(0,2)]
slider = MadeObject('Glisseur',mat)
objectsList.append(slider)

#Blinker
mat = [(0,0),(0,1),(0,2)]
blinker = MadeObject('Clignotant',mat)
objectsList.append(blinker)

#Frog
mat=[(0,0),(0,1),(0,2),(1,1),(1,2),(1,3)]
frog = MadeObject('Grenouille',mat)
objectsList.append(frog)

#