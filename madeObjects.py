import os

## Class definition

class MadeObject():
	def __init__(self,name,aliveCellsList):
		self._name = name
		self._aliveCellsList = aliveCellsList

	def getName(self):
		return self._name

	def getAliveCellsList(self):
		return self._aliveCellsList


def getAliveCellsList(path):
	file = open(path,'r').read().split('\n')
	information = file[0:3]
	drawing = file[4:]
	aliveCellsList = []
	name = information[0]
	di,dj = int(information[1]),int(information[2])
	for i in range(len(drawing)):
		for j in range(len(drawing[0])):
			if drawing[i][j] == 'X':
				aliveCellsList.append((i+di,j+dj))
	return name,aliveCellsList


## List of objects
fileList = os.listdir('./Premade_objects')
objectsList = []

for fileName in fileList:
	name,aliveCellsList = getAliveCellsList('./Premade_objects/' + fileName)
	obj = MadeObject(name,aliveCellsList)
	objectsList.append(obj)