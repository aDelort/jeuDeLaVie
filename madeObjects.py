class MadeObject():
	def __init__(self,name,boolMartix):
		self._name = name
		self._boolMatrix = boolMartix

	def getName(self):
		return self._name

	def getMatrix(self):
		return self._boolMatrix

objectsList = []

#Glisseur
mat = [[1,0,1],[0,1,0],[1,0,1]]
slider = MadeObject('Slider',mat)
objectsList.append(slider)

#Blinker
mat=[[1,1,1]]
blinker = MadeObject('Blinker',mat)
objectsList.append(blinker)