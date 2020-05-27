import os
import json


class MadeObject():
    def __init__(self, name, aliveCellsList):
        self._name = name
        self._aliveCellsList = aliveCellsList

    def getName(self):
        return self._name

    def getAliveCellsList(self):
        return self._aliveCellsList


def getAliveCellsList(path):
    a = open(path,'r')
    print(a)
    file = json.load(a)
    # file = open(path,'r').read().split('\n')
    name, di, dj, drawing = file['name'], file['di'], file['dj'], file['drawing']
    aliveCellsList = []
    for i in range(len(drawing)):
        for j in range(len(drawing[i])):
            if drawing[i][j] == 'X':
                aliveCellsList.append((i+di, j+dj))
    return name, aliveCellsList


# List of objects
fileList = os.listdir('./Premade_objects')
objectsList = []

for fileName in fileList:
    name, aliveCellsList = getAliveCellsList('./Premade_objects/' + fileName)
    obj = MadeObject(name, aliveCellsList)
    objectsList.append(obj)
