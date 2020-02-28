## Class definition

class MadeObject():
	def __init__(self,name,aliveCellsMartix):
		self._name = name
		self._aliveCellsMatrix = aliveCellsMartix

	def getName(self):
		return self._name

	def getMatrix(self):
		return self._aliveCellsMatrix


## List of objects
objectsList = []

#Glisseur
mat = [(0,0),(2,0),(0,2),(2,2),(1,1)]
slider = MadeObject('Slider',mat)
objectsList.append(slider)

#Blinker
mat = [(0,0),(0,1),(0,2)]
blinker = MadeObject('Blinker',mat)
objectsList.append(blinker)