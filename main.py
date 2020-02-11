##Imports
from tkinter import *  
import time

helpFile = open('help.txt')

## Settings
defaultCellSize = 10
cellSizeMin = 2
cellSizeMax = 100

defaultSpeed = 10
dtMin = 50 #Corresponds to the max speed
dtMax = 500 #Correspond to the min speed


## Classes
class HelpWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._helpText = Label(self,text=helpFile.read(),anchor='nw',justify='left',wraplength=800)
        '''Le Jeu de la Vie a été immaginé par Conway en 1970 (Conway\'s Game of Life). Il est régi par \
            des règles très simples pour déterminer, à partir d\'une génération n, la composition de la génération n+1. En théorie le jeu \
            doit se dérouler sur une grille infinie, mais ces conditions sont évidemment impossibles sur un ordinateur.\n\n\
            Les règles sont les suivantes :\n\
            - Une cellule vivante entourée par exactement 2 ou 3 cellules vivantes reste vivante à la génération suivante, sinon elle meurt ;\n\
            - Une cellule morte entourée par exactement 3 cellules vivantes naît à la génération suivante, sinon elle reste morte.\n\n\
            Dans la grille, les cellules vivantes sont les cellules noires, tandis que les cellules mortes sont les cellules vivantes. Le clic \
            gauche permet de faire naître une cellule, et le clic droit de la tuer.')'''
        self._okButton = Button(self,text='Ok',command=self.destroy)

        self._helpText.pack(padx=10,pady=10,side=TOP)
        self._okButton.pack(padx=10,pady=10,side=TOP)


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._gridWidth = self.winfo_screenwidth()-210
        self._gridHeight = self.winfo_screenheight()-120

        #Definition of widgets
        self._rightCommands = Frame(self)
        self._grid = Grid(self,width=self._gridWidth,height=self._gridHeight,bg='grey')
        self._informationFrame = LabelFrame(self._rightCommands,text="Infos",labelanchor='n')
        self._commandFrame = LabelFrame(self._rightCommands,text="Commandes",labelanchor='n')
        self._nbCellsScaleFrame = LabelFrame(self._commandFrame,text="Taille des cellules")
        self._nbCellsScale = Scale(self._nbCellsScaleFrame,variable=self._grid._cellSize,from_=cellSizeMin,to=cellSizeMax,command=self._grid.updateGrid,orient='horizontal',length=100)
        self._speedScaleFrame = LabelFrame(self._commandFrame,text="Vitesse")
        self._speedScale = Scale(self._speedScaleFrame,variable=self._grid._speed,from_=1,orient='horizontal',length=100)
        self._rectSelectButton = Button(self._commandFrame,text="Sélection\nRectangle",command=self.rectSelection,relief=RAISED)
        self._gridShowCheckButton = Checkbutton(self._commandFrame,text="Grille",variable=self._grid._isShowedGrid,command=self.showOrHideGrid)
        self._eraseButton = Button(self._commandFrame,text="Effacer",command=self.erase,relief=RAISED)
        self._generationCounterFrame = LabelFrame(self._informationFrame,text="Génération")
        self._generationCounter = Label(self._generationCounterFrame,textvariable=self._grid._generation)
        self._cellsCounterFrame = LabelFrame(self._informationFrame,text="Population")
        self._cellsCounter = Label(self._cellsCounterFrame,textvariable=self._grid._nbCells)
        self._bottomCommands = Frame(self)
        self._start = Button(self._bottomCommands,text='Démarrer',command=self.start)
        self._stop = Button(self._bottomCommands,text='Stop',command=self._grid.stop)
        self._quit = Button(self._bottomCommands,text='Quitter',command=self.quit)
        self._helpButton = Button(self._rightCommands,text='Aide',command=self.popHelpBox)

        #Packing
        self._rightCommands.pack(padx=10,side=RIGHT)
        self._informationFrame.pack(side=TOP,pady=30)
        self._generationCounterFrame.pack(side=TOP,pady=10)
        self._generationCounter.pack()
        self._cellsCounterFrame.pack(side=TOP,pady=10)
        self._cellsCounter.pack()
        self._commandFrame.pack(side=TOP,pady=30)
        self._nbCellsScaleFrame.pack(side=TOP,pady=10)
        self._nbCellsScale.pack()
        self._speedScaleFrame.pack(side=TOP,pady=10)
        self._speedScale.pack()
        self._rectSelectButton.pack(side=TOP,pady=10)
        self._gridShowCheckButton.pack(side=TOP,pady=10)
        self._eraseButton.pack(side=TOP,pady=10)
        self._helpButton.pack(side=TOP,padx=10,pady=20)

        self._bottomCommands.pack(padx=10,pady=10,side=BOTTOM)
        self._start.pack(side=LEFT,padx=10)
        self._stop.pack(side=LEFT,padx=10)
        self._quit.pack(side=LEFT,padx=10)

        self._grid.pack(padx=10,pady=10,side=TOP,anchor='center',expand=False)

        #Binding events
        self._grid.bind("<Button-1>",self.leftClick)
        self._grid.bind("<Button-3>",self.rightClick)
        self._grid.bind("<B1-Motion>",self.leftClick)
        self._grid.bind("<B3-Motion>",self.rightClick)

    def start(self):
        if self._grid._stopped:
            self._grid._stopped = False
            self._grid.updateCellsState()

    def quit(self):
        self.destroy()

    def convertCoordinates(self,event):
        i = (event.y+self._grid._yMin)//self._grid._cellSize.get()
        j = (event.x+self._grid._xMin)//self._grid._cellSize.get()
        return i,j

    def leftClick(self,event):
        #Be careful : event.x and event.y return coordinates with origin in the corner upper left
        #if self._grid._stopped:
        i,j = self.convertCoordinates(event) 
        if not self._grid._rectSelectActivated.get():
            self._grid.awake(i,j)
        else:
            #Just color with red the first cell
            if not self._grid._rectSelectedOneCell.get():
                self._grid._rectSelectedOneCell.set(1)
                self._grid.createRedCell(i,j)
                self._grid._redCell_i = i
                self._grid._redCell_j = j
            else:
                #Awake each cell in the rectangle
                self._grid._rectSelectedOneCell.set(0)
                self._grid.deleteRedCell()
                i1,i2 = sorted((self._grid._redCell_i,i))
                j1,j2 = sorted((self._grid._redCell_j,j))
                for lig in range(i1,i2+1):
                    for col in range(j1,j2+1):
                        self._grid.awake(lig,col)

    def rightClick(self,event):
        i,j = self.convertCoordinates(event)
        self._grid.kill(i,j)

    def rectSelection(self):
        if self._grid._rectSelectActivated.get(): #Rectangle selection was activated
            self._grid._rectSelectActivated.set(0)
            self._rectSelectButton.config(relief=RAISED)
            if self._grid._rectSelectedOneCell.get():
                self._grid.deleteRedCell()
                self._grid._rectSelectedOneCell.set(0)
        else: #Rectangle selection wasn't activated
            self._grid._rectSelectActivated.set(1)
            self._rectSelectButton.config(relief=SUNKEN)

    def showOrHideGrid(self):
        if self._grid._isShowedGrid.get():
            self._grid.showGrid()
        else:
            self._grid.hideGrid()

    def erase(self):
        cellsAlive = self._grid._cellsAlive.copy()
        for i,j in cellsAlive:
            self._grid.kill(i,j)

    def popHelpBox(self):
        self._helpWindow = HelpWindow()


class Grid(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, **kwargs)
        self._sizeGridX = kwargs['width']
        self._sizeGridY = kwargs['height']
        self._xMin = -self._sizeGridX//2
        self._xMax = (self._sizeGridX+1)//2 - 1
        self._yMin = -self._sizeGridY//2
        self._yMax = (self._sizeGridY+1)//2 - 1
        self.config(scrollregion=(self._xMin,self._yMin,self._xMax,self._yMax)) #Changing the origin of the coordinates
        self._stopped = True
        self._speed = IntVar()
        self._speed.set(defaultSpeed)
        self._generation = IntVar(0)
        self._cellSize = IntVar() #Number of pixels
        self._cellSize.set(defaultCellSize)
        self._gridLines = []
        self._cellsAlive = dict()
        self._nbCells = IntVar(0) #Total number of cells alive
        self._isShowedGrid = IntVar() #Boolean true if the grid is displayed
        self._isShowedGrid.set(1)
        self._rectSelectActivated = IntVar(0) #Boolean for the state of the self._rectSelectButton (clicked or not)
        self._rectSelectedOneCell = IntVar(0) #Boolean true when the user already selected the first corner of the rectangle
        self._redCell_i = 0
        self._redCell_j = 0
        self._redCellId = 0 #Id of the red rectangle created in the first corner of the rectangle
           
    def stop(self):
        self._stopped = True

    def updateGrid(self,uselessVariable):
        #Deletes and draws every elements in the grid
        self._nCols = self._xMax//self._cellSize.get() - self._xMin//self._cellSize.get() + 2
        self._nRows = self._yMax//self._cellSize.get() - self._yMin//self._cellSize.get() + 2
        #Modification of the grid's dimensions
        self.config(width=self._sizeGridX,height=self._sizeGridY)
        if self._isShowedGrid.get():
            #Removal of the previous grid
            self.hideGrid()
            #Creation of the new grid
            self.showGrid()
        #Updating the drawing of alive cells
        for i,j in self._cellsAlive:
            self.kill(i,j)
            self.awake(i,j)

    def showGrid(self):
        for x in range(0,self._xMax,self._cellSize.get()):
            self._gridLines.append(self.create_line(x,self._yMin,x,self._yMax,fill='black'))
        for x in range(0,self._xMin,-self._cellSize.get()):
            self._gridLines.append(self.create_line(x,self._yMin,x,self._yMax,fill='black'))
        for y in range(0,self._yMax,self._cellSize.get()):
            self._gridLines.append(self.create_line(self._xMin,y,self._xMax,y,fill='black'))
        for y in range(0,self._yMin,-self._cellSize.get()):
            self._gridLines.append(self.create_line(self._xMin,y,self._xMax,y,fill='black'))

    def hideGrid(self):
        for line in self._gridLines:
            self.delete(line)

    def isAlive(self,i,j):
        return (i,j) in self._cellsAlive.keys()

    def awake(self,i,j):
        if not self.isAlive(i,j):
            id = self.create_rectangle(j*self._cellSize.get(),i*self._cellSize.get(),(j+1)*self._cellSize.get(),(i+1)*self._cellSize.get(),fill='black')
            self._cellsAlive.setdefault((i,j),id)
            self._nbCells.set(self._nbCells.get()+1)

    def kill(self,i,j):
        if self.isAlive(i,j):
            id = self._cellsAlive.pop((i,j))
            self.delete(id)
            self._nbCells.set(self._nbCells.get()-1)

    def createRedCell(self,i,j):
        self._redCellId = self.create_rectangle(j*self._cellSize.get(),i*self._cellSize.get(),(j+1)*self._cellSize.get(),(i+1)*self._cellSize.get(),fill='red')

    def deleteRedCell(self):
        self.delete(self._redCellId)

    def countAliveNeigh(self,i,j,isNeigh):
        #Counts the numer of neighboors from de temporary list (list of the previous generation)
        nbNeigh = 0
        for di,dj in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            if not isNeigh:
                self._neighToCellsAlive.setdefault((i+di,j+dj))
            if (i+di,j+dj) in self._cellsAliveTmp.keys():
                nbNeigh += 1
        return nbNeigh

    def killOrAwake(self,i,j,nbNeigh,alive):
        #Take the decision to kill or awake a cell
        if alive:
            if nbNeigh > 3 or nbNeigh < 2:
                self.kill(i,j)
        else:
            if nbNeigh == 3:
                self.awake(i,j)
        
    def updateCellsState(self):
        #Goes on to the next generation
        t1=time.time()

        self._cellsAliveTmp = dict(self._cellsAlive)
        self._neighToCellsAlive = dict()

        for (i,j) in self._cellsAliveTmp.keys():
            nbNeigh = self.countAliveNeigh(i,j,False)
            self.killOrAwake(i,j,nbNeigh,True)

        for (i,j) in self._neighToCellsAlive.keys():
            if not (i,j) in self._cellsAliveTmp.keys():
                nbNeigh = self.countAliveNeigh(i,j,True)
                self.killOrAwake(i,j,nbNeigh,False)

        self._generation.set(self._generation.get() + 1)
        if self._nbCells.get() == 0:
            self.stop()

        t2=time.time()
        #print(t2-t1)

        if not self._stopped:
            self._dt = dtMax - (self._speed.get() - 1)/99*(dtMax - dtMin) #time beetween generations (milliseconds)
            #If the calculation time is over self._dt, we don't wait anymore to get to the next generation
            #Otherwise, we wait the right time to get to the next generation
            self.after(max(int(self._dt-1000*(t2-t1)),1),self.updateCellsState)


## Calls
window = MainWindow()
#window.attributes('-maximized',True)
window.mainloop()