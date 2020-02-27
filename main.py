##Imports
from tkinter import *  
from tkinter import ttk
import time
import gameState as gs
import madeObjects as mo


## Settings
defaultCellSize = 10
cellSizeMin = 2
cellSizeMax = 100

defaultSpeed = 10 #Linked to the time beetween generations
dtMin = 50 #Corresponds to the max speed
dtMax = 500 #Correspond to the min speed


## Classes
class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu de la Vie')
        self._gridWidth = self.winfo_screenwidth()-240
        self._gridHeight = self.winfo_screenheight()-90

        #Definition of widgets
        self._noteBook = ttk.Notebook(self)
        self._rightCommandsTab = Frame(self._noteBook)
        self._noteBook.add(self._rightCommandsTab,text="Commandes")
        self._objectsListbox = Listbox(self._noteBook)
        self._noteBook.add(self._objectsListbox,text="Objets")

        self._grid = Grid(self,width=self._gridWidth,height=self._gridHeight,bg='grey')

        self._informationFrame = LabelFrame(self._rightCommandsTab,text="Infos",labelanchor='n')
        self._commandFrame = LabelFrame(self._rightCommandsTab,text="Commandes",labelanchor='n')
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

        self._noteBook.select(self._rightCommandsTab)

        #Packing
        self._noteBook.pack(padx=10,side=RIGHT)

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

        self._bottomCommands.pack(padx=10,pady=10,side=BOTTOM)
        self._start.pack(side=LEFT,padx=10)
        self._stop.pack(side=LEFT,padx=10)
        self._quit.pack(side=LEFT,padx=10)

        self._grid.pack(padx=10,pady=10,side=TOP,anchor='center',expand=False)

        #Binding events
        self._grid.bind("<Button-1>",self.leftClickOnGrid)
        self._grid.bind("<Button-3>",self.rightClickOnGrid)
        self._grid.bind("<B1-Motion>",self.leftClickOnGrid)
        self._grid.bind("<B3-Motion>",self.rightClickOnGrid)

        self._objectsListbox.bind("<Button-1>",self.leftClickOnMadeObject)

        #Getting objects from the madeObjects.py file
        self.importObjects()

    def start(self):
        #Start button
        if self._grid._stopped:
            self._grid._stopped = False
            self._grid.updateCellsState()

    def quit(self):
         #Quit button
        self.destroy()

    def convertCoordinates(self,event):
        #Converts the output of the mouse click event (x,y) into a cell row and column
        i = (event.y+self._grid._yMin)//self._grid._cellSize.get()
        j = (event.x+self._grid._xMin)//self._grid._cellSize.get()
        return i,j

    def leftClickOnGrid(self,event):
        #event.x and event.y return coordinates with origin in the corner upper left ((x,y)!=(i,j))
        i,j = self.convertCoordinates(event) 
        if not self._grid._rectSelectActivated.get():
            awaked = self._grid._game_state.awake(i,j)
            if awaked: #The cell has been awaked
                self._grid.drawAliveCell(i,j)
        else:
            #Just color with red the first cell
            if not self._grid._rectSelectedOneCell.get():
                self._grid._rectSelectedOneCell.set(1)
                self._grid.drawRedCell(i,j)
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
                        awaked = self._grid._game_state.awake(lig,col)
                        if awaked:
                            self._grid.drawAliveCell(lig,col)


    def rightClickOnGrid(self,event):
        i,j = self.convertCoordinates(event)
        killed = self._grid._game_state.kill(i,j)
        if killed:
            self._grid.eraseKilledCell(i,j)

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
        #Linked to the checkbox, hides of shows the grid
        if self._grid._isShowedGrid.get():
            self._grid.showGrid()
        else:
            self._grid.hideGrid()

    def erase(self):
        #Kills every cells
        cellsAlive = self._grid._game_state._cellsAlive.copy()
        for i,j in cellsAlive:
            killed = self._grid._game_state.kill(i,j)
            if killed:
                self._grid.eraseKilledCell(i,j)
        self._grid.stop()
        self._grid._generation.set(0)

    def importObjects(self):
        for obj in mo.objectsList:
            self._objectsListbox.insert('end',obj.getName())

    def leftClickOnMadeObject(self,event):
        print(self._objectsListbox.nearest(event.y))
        #CLIC SUR LA GRILLLLLLLLE


class Grid(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, **kwargs)
        self._sizeGridX = kwargs['width']
        self._sizeGridY = kwargs['height']
        self._xMin = -self._sizeGridX//2
        self._xMax = (self._sizeGridX+1)//2 - 1
        self._yMin = -self._sizeGridY//2
        self._yMax = (self._sizeGridY+1)//2 - 1
        self._game_state = gs.GameState()
        self._generation = IntVar(0)
        self._nbCells = IntVar(0) #Total number of cells alive
        self.config(scrollregion=(self._xMin,self._yMin,self._xMax,self._yMax)) #Changing the origin of the coordinates
        self._stopped = True
        self._speed = IntVar()
        self._speed.set(defaultSpeed)
        self._cellSize = IntVar() #Number of pixels
        self._cellSize.set(defaultCellSize)
        self._gridLines = []
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
        for i,j in self._game_state._cellsAlive:
            self.eraseKilledCell(i,j)
            self.drawAliveCell(i,j)

        if self._rectSelectedOneCell.get():
            i,j = self._redCell_i,self._redCell_j
            self.deleteRedCell()
            self.drawRedCell(i,j)

    def showGrid(self):
        #Draws the lines of the grid
        for x in range(0,self._xMax,self._cellSize.get()):
            self._gridLines.append(self.create_line(x,self._yMin,x,self._yMax,fill='black'))
        for x in range(0,self._xMin,-self._cellSize.get()):
            self._gridLines.append(self.create_line(x,self._yMin,x,self._yMax,fill='black'))
        for y in range(0,self._yMax,self._cellSize.get()):
            self._gridLines.append(self.create_line(self._xMin,y,self._xMax,y,fill='black'))
        for y in range(0,self._yMin,-self._cellSize.get()):
            self._gridLines.append(self.create_line(self._xMin,y,self._xMax,y,fill='black'))

    def hideGrid(self):
        #Deletes the lines of the grid
        for line in self._gridLines:
            self.delete(line)

    def drawAliveCell(self,i,j):
        self.create_rectangle(j*self._cellSize.get(),i*self._cellSize.get(),(j+1)*self._cellSize.get(),(i+1)*self._cellSize.get(),fill='black',tags=(str(i)+','+str(j)))#(str(i),str(j)))
        self._nbCells.set(self._nbCells.get()+1)

    def eraseKilledCell(self,i,j):
        self.delete(str(i)+','+str(j))
        self._nbCells.set(self._nbCells.get()-1)

    def drawRedCell(self,i,j):
        #Create the red cell (to mark down the first corner of the rectangle selection)
        self._redCellId = self.create_rectangle(j*self._cellSize.get(),i*self._cellSize.get(),(j+1)*self._cellSize.get(),(i+1)*self._cellSize.get(),fill='red')

    def deleteRedCell(self):
        #Function called when the red cell isn't needed anymore
        self.delete(self._redCellId)

    def updateCellsState(self):
        if not self._stopped:
            t1=time.time()
            awakedCells,killedCells = self._game_state.goToNextGeneration()
            for (i,j) in awakedCells:
                self.drawAliveCell(i,j)
            for (i,j) in killedCells:
                self.eraseKilledCell(i,j)
            t2=time.time()

            self._generation.set(self._generation.get() + 1)

            #Game is stopped if every cell is dead during a generation
            if self._nbCells.get() == 0:
                self.stop()

            self._dt = dtMax - (self._speed.get() - 1)/99*(dtMax - dtMin) #time beetween generations (milliseconds)
            #If the calculation time is over self._dt, we don't wait anymore to get to the next generation
            #Otherwise, we wait the right time to get to the next generation
            self.after(max(int(self._dt-1000*(t2-t1)),1),self.updateCellsState)



## Calls
window = MainWindow()
window.attributes('-zoomed',True)
window.mainloop()