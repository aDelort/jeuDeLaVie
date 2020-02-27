#from tkinter import *
import time

class GameState():
    def __init__(self):
        self._cellsAlive = dict()

    def isAlive(self,i,j):
        #Returns the state of a cell (alive or not)
        return (i,j) in self._cellsAlive.keys()

    def awake(self,i,j):
        #Cell (i,j): dead -> alive
        if (i,j) not in self._cellsAlive.keys():
            self._cellsAlive.setdefault((i,j))
            return True
        else:
            return False

    def kill(self,i,j):
        #Cell (i,j): alive -> dead
        if (i,j) in self._cellsAlive.keys():
            self._cellsAlive.pop((i,j))
            return True
        else:
            return False


    def countAliveNeigh(self,i,j,isNeigh):
        #Counts the number of neighboors from de temporary list (list of the previous generation)
        #isNeigh contains a boolean : True if the cell to analyse is a neighboor of a cell to analyse, false if it is directly a cell to analyse : from a generation to the next one, the neignboors of alive cells must be analysed but not the neighboors of the neighboors
        nbNeigh = 0
        for di,dj in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            if not isNeigh:
                self._neighToCellsAlive.setdefault((i+di,j+dj)) #If the cell is a neighboor of a cell that must be analysed, it will be analysed
            if (i+di,j+dj) in self._cellsAliveTmp.keys():
                nbNeigh += 1
        return nbNeigh

    def killOrAwake(self,i,j,nbNeigh,alive):
        #Takes the decision to kill or awake a cell
        if alive:
            if nbNeigh > 3 or nbNeigh < 2:
                self.kill(i,j)
                return ((i,j),False)
        else:
            if nbNeigh == 3:
                self.awake(i,j)
                return ((i,j),True)
            else:
                return None
        
    def goToNextGeneration(self):
        #Goes on to the next generation
        self._cellsAliveTmp = dict(self._cellsAlive) #The generation n is copied to calculate the generation n+1
        self._neighToCellsAlive = dict()
        awakedCells = list()
        killedCells = list()

        for (i,j) in self._cellsAliveTmp.keys(): #Alive cells at the generation n are analysed
            nbNeigh = self.countAliveNeigh(i,j,False)
            result = self.killOrAwake(i,j,nbNeigh,True)
            if result != None:
                if result[1]: #A cell was awaked
                    awakedCells.append(result[0])
                else: #A cell was killed
                    killedCells.append(result[0])

        for (i,j) in self._neighToCellsAlive.keys(): #Neighboors of alive cells at the generation n are analysed
            if not (i,j) in self._cellsAliveTmp.keys():
                nbNeigh = self.countAliveNeigh(i,j,True) #True indicates that those cells are neighboors of alive cells (they were dead during the generation n), thus the neighboors of those neighboors won't be added to the list of cells to analyse
                result = self.killOrAwake(i,j,nbNeigh,False)
                if result != None:
                    if result[1]: #A cell was awaked
                        awakedCells.append(result[0])
                    else: #A cell was killed
                        killedCells.append(result[0])
        return awakedCells,killedCells