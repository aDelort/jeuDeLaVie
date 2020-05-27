# Imports
from tkinter import Tk, TOP, RIGHT, Frame, Listbox, LabelFrame, SINGLE, Scale, Button, Checkbutton, Label, RAISED, LEFT, BOTTOM, SUNKEN, IntVar, Canvas, ttk
import time
import GameState as gs
import MadeObjects as mo


# Settings
defaultCellSize = 10
cellSizeMin = 2
cellSizeMax = 100

defaultSpeed = 10  # Linked to the time beetween generations
dtMin = 50  # Corresponds to the max speed
dtMax = 500  # Correspond to the min speed


# Classes
class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu de la Vie')
        # Index on the object selected in the listbox (-1 if no object is selected)
        self._objectSelected = -1
        self._fieldWidth = self.winfo_screenwidth()-240
        self._fieldHeight = self.winfo_screenheight()-90

        # Definition of widgets
        self._noteBook = ttk.Notebook(self)
        self._rightCommandsTab = Frame(self._noteBook)
        self._noteBook.add(self._rightCommandsTab, text="Commandes")
        self._objectsTab = Frame(self._noteBook)
        self._noteBook.add(self._objectsTab, text='Objets')

        self._objectsListbox = Listbox(
            self._objectsTab, selectmode=SINGLE, height=0, cursor='pencil')
        self._cancelObjectSelectionButton = Button(
            self._objectsTab, text='Annuler', command=self.unselectObject)

        self._field = Field(self, width=self._fieldWidth,
                            height=self._fieldHeight, bg='grey', cursor='tcross')

        self._informationFrame = LabelFrame(
            self._rightCommandsTab, text="Infos", labelanchor='n')
        self._commandFrame = LabelFrame(
            self._rightCommandsTab, text="Commandes", labelanchor='n')
        self._nbCellsScaleFrame = LabelFrame(
            self._commandFrame, text="Taille des cellules")
        self._nbCellsScale = Scale(self._nbCellsScaleFrame, variable=self._field._cellSize, from_=cellSizeMin,
                                   to=cellSizeMax, command=self._field.updateField, orient='horizontal', length=100)
        self._speedScaleFrame = LabelFrame(self._commandFrame, text="Vitesse")
        self._speedScale = Scale(
            self._speedScaleFrame, variable=self._field._speed, from_=1, orient='horizontal', length=100)
        self._rectSelectButton = Button(
            self._commandFrame, text="Sélection\nRectangle", command=self.rectSelection, relief=RAISED)
        self._fieldShowCheckButton = Checkbutton(
            self._commandFrame, text="Grille", variable=self._field._isShowedField, command=self.showOrHideField)
        self._eraseButton = Button(
            self._commandFrame, text="Effacer", command=self.erase, relief=RAISED)
        self._generationCounterFrame = LabelFrame(
            self._informationFrame, text="Génération")
        self._generationCounter = Label(
            self._generationCounterFrame, textvariable=self._field._generation)
        self._cellsCounterFrame = LabelFrame(
            self._informationFrame, text="Population")
        self._cellsCounter = Label(
            self._cellsCounterFrame, textvariable=self._field._nbCells)

        self._bottomCommands = Frame(self)
        self._start = Button(self._bottomCommands,
                             text='Démarrer', command=self.start)
        self._stop = Button(self._bottomCommands,
                            text='Stop', command=self._field.stop)
        self._quit = Button(self._bottomCommands,
                            text='Quitter', command=self.quit)

        self._noteBook.select(self._rightCommandsTab)

        # Packing
        # self._objectsTab
        self._noteBook.pack(padx=10, side=RIGHT)
        self._objectsListbox.pack(side=TOP)
        self._cancelObjectSelectionButton.pack(pady=10, side=TOP)

        self._informationFrame.pack(side=TOP, pady=30)
        self._generationCounterFrame.pack(side=TOP, pady=10)
        self._generationCounter.pack()
        self._cellsCounterFrame.pack(side=TOP, pady=10)
        self._cellsCounter.pack()
        self._commandFrame.pack(side=TOP, pady=30)
        self._nbCellsScaleFrame.pack(side=TOP, pady=10)
        self._nbCellsScale.pack()
        self._speedScaleFrame.pack(side=TOP, pady=10)
        self._speedScale.pack()
        self._rectSelectButton.pack(side=TOP, pady=10)
        self._fieldShowCheckButton.pack(side=TOP, pady=10)
        self._eraseButton.pack(side=TOP, pady=10)

        self._bottomCommands.pack(padx=10, pady=10, side=BOTTOM)
        self._start.pack(side=LEFT, padx=10)
        self._stop.pack(side=LEFT, padx=10)
        self._quit.pack(side=LEFT, padx=10)

        self._field.pack(padx=10, pady=10, side=TOP,
                         anchor='center', expand=False)

        # Binding events
        self._field.bind("<Button-1>", self.leftClickOnField)
        self._field.bind("<Button-3>", self.rightClickOnField)
        self._field.bind("<B1-Motion>", self.leftClickOnField)
        self._field.bind("<B3-Motion>", self.rightClickOnField)

        self._objectsListbox.bind("<Button-1>", self.leftClickOnMadeObject)
        self._noteBook.bind("<Button-1>", self.unselectObject)

        # Getting objects from the madeObjects.py file
        self.importObjects()

    def start(self):
        # Start button
        if self._field._stopped:
            self._field._stopped = False
            self._field.updateCellsState()

    def quit(self):
        # Quit button
        self.destroy()

    def convertCoordinates(self, event):
        # Converts the output of the mouse click event (x,y) into a cell row and column
        i = (event.y+self._field._yMin)//self._field._cellSize.get()
        j = (event.x+self._field._xMin)//self._field._cellSize.get()
        # print("event.x : "+str(event.x), "event.y : "+str(event.y))
        # print("(i,j) = " + str(i) + "," + str(j))
        return i, j

    def leftClickOnField(self, event):
        # event.x and event.y return coordinates with origin in the corner upper left ((x,y)!=(i,j))
        i, j = self.convertCoordinates(event)
        if self._field._rectSelectActivated.get():
            if not self._field._rectSelectedOneCell.get():
                # Just color with red the first cell
                self._field._rectSelectedOneCell.set(1)
                self._field.drawRedCell(i, j)
                self._field._redCell_i = i
                self._field._redCell_j = j
            else:
                # Awake each cell in the rectangle
                self._field._rectSelectedOneCell.set(0)
                self._field.deleteRedCell()
                i1, i2 = sorted((self._field._redCell_i, i))
                j1, j2 = sorted((self._field._redCell_j, j))
                for lig in range(i1, i2+1):
                    for col in range(j1, j2+1):
                        awaked = self._field._game_state.awake(lig, col)
                        if awaked:
                            self._field.drawAliveCell(lig, col)
        elif self._objectSelected >= 0:
            for (di, dj) in mo.objectsList[self._objectSelected].getAliveCellsList():
                awaked = self._field._game_state.awake(i+di, j+dj)
                if awaked:  # The cell has been awaked
                    self._field.drawAliveCell(i+di, j+dj)
        else:
            awaked = self._field._game_state.awake(i, j)
            if awaked:  # The cell has been awaked
                self._field.drawAliveCell(i, j)

    def rightClickOnField(self, event):
        i, j = self.convertCoordinates(event)
        killed = self._field._game_state.kill(i, j)
        if killed:
            self._field.eraseKilledCell(i, j)

    def rectSelection(self):
        if self._field._rectSelectActivated.get():  # Rectangle selection was activated
            self.cancelRectSelection()
        else:  # Rectangle selection wasn't activated
            self._field._rectSelectActivated.set(1)
            self._rectSelectButton.config(relief=SUNKEN)

    def cancelRectSelection(self):
        self._field._rectSelectActivated.set(0)
        self._rectSelectButton.config(relief=RAISED)
        if self._field._rectSelectedOneCell.get():
            self._field.deleteRedCell()
            self._field._rectSelectedOneCell.set(0)

    def showOrHideField(self):
        # Linked to the checkbox, hides of shows the field
        if self._field._isShowedField.get():
            self._field.showField()
        else:
            self._field.hideField()

    def erase(self):
        # Kills every cells
        cellsAlive = self._field._game_state._cellsAlive.copy()
        for i, j in cellsAlive:
            killed = self._field._game_state.kill(i, j)
            if killed:
                self._field.eraseKilledCell(i, j)
        self._field.stop()
        self._field._generation.set(0)

    def importObjects(self):
        for obj in mo.objectsList:
            self._objectsListbox.insert('end', obj.getName())

    def leftClickOnMadeObject(self, event):
        self._objectSelected = self._objectsListbox.nearest(event.y)

    def unselectObject(self, *event):
        # Delete th selected object if it exists
        self._objectsListbox.selection_clear(0, 'end')
        self._objectSelected = -1
        # If rectangle selection was activated
        if self._field._rectSelectActivated.get():
            self.cancelRectSelection()


class Field(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, **kwargs)
        self._sizeFieldX = kwargs['width']
        self._sizeFieldY = kwargs['height']
        self._xMin = -self._sizeFieldX//2
        self._xMax = (self._sizeFieldX+1)//2 - 1
        self._yMin = -self._sizeFieldY//2
        self._yMax = (self._sizeFieldY+1)//2 - 1
        self._game_state = gs.GameState()
        self._generation = IntVar(0)
        self._nbCells = IntVar(0)  # Total number of cells alive
        # Changing the origin of the coordinates
        self.config(scrollregion=(
            self._xMin, self._yMin, self._xMax, self._yMax))
        self._stopped = True
        self._speed = IntVar()
        self._speed.set(defaultSpeed)
        self._cellSize = IntVar()  # Number of pixels
        self._cellSize.set(defaultCellSize)
        self._fieldLines = []
        self._isShowedField = IntVar()  # Boolean true if the field is displayed
        self._isShowedField.set(1)
        # Boolean for the state of the self._rectSelectButton (clicked or not)
        self._rectSelectActivated = IntVar(0)
        # Boolean true when the user already selected the first corner of the rectangle
        self._rectSelectedOneCell = IntVar(0)
        self._redCell_i = 0
        self._redCell_j = 0
        self._redCellId = 0  # Id of the red rectangle created in the first corner of the rectangle

    def stop(self):
        self._stopped = True

    def updateField(self, uselessVariable):
        # Deletes and draws every elements in the field
        self._nCols = self._xMax//self._cellSize.get() - self._xMin//self._cellSize.get() + 2
        self._nRows = self._yMax//self._cellSize.get() - self._yMin//self._cellSize.get() + 2
        # Modification of the field's dimensions
        self.config(width=self._sizeFieldX, height=self._sizeFieldY)
        if self._isShowedField.get():
            # Removal of the previous field
            self.hideField()
            # Creation of the new field
            self.showField()
        # Updating the drawing of alive cells
        for i, j in self._game_state._cellsAlive:
            self.eraseKilledCell(i, j)
            self.drawAliveCell(i, j)

        if self._rectSelectedOneCell.get():
            i, j = self._redCell_i, self._redCell_j
            self.deleteRedCell()
            self.drawRedCell(i, j)

    def showField(self):
        # Draws the lines of the field
        for x in range(0, self._xMax, self._cellSize.get()):
            self._fieldLines.append(self.create_line(
                x, self._yMin, x, self._yMax, fill='black'))
        for x in range(0, self._xMin, -self._cellSize.get()):
            self._fieldLines.append(self.create_line(
                x, self._yMin, x, self._yMax, fill='black'))
        for y in range(0, self._yMax, self._cellSize.get()):
            self._fieldLines.append(self.create_line(
                self._xMin, y, self._xMax, y, fill='black'))
        for y in range(0, self._yMin, -self._cellSize.get()):
            self._fieldLines.append(self.create_line(
                self._xMin, y, self._xMax, y, fill='black'))

    def hideField(self):
        # Deletes the lines of the field
        for line in self._fieldLines:
            self.delete(line)

    def drawAliveCell(self, i, j):
        self.create_rectangle(j*self._cellSize.get(), i*self._cellSize.get(), (j+1)*self._cellSize.get(
        ), (i+1)*self._cellSize.get(), fill='black', tags=(str(i)+','+str(j)))
        self._nbCells.set(self._nbCells.get()+1)

    def eraseKilledCell(self, i, j):
        self.delete(str(i)+','+str(j))
        self._nbCells.set(self._nbCells.get()-1)

    def drawRedCell(self, i, j):
        # Create the red cell (to mark down the first corner of the rectangle selection)
        self._redCellId = self.create_rectangle(j*self._cellSize.get(), i*self._cellSize.get(
        ), (j+1)*self._cellSize.get(), (i+1)*self._cellSize.get(), fill='red')

    def deleteRedCell(self):
        # Function called when the red cell isn't needed anymore
        self.delete(self._redCellId)

    def updateCellsState(self):
        if not self._stopped:
            t1 = time.time()
            awakedCells, killedCells = self._game_state.goToNextGeneration()
            for (i, j) in awakedCells:
                self.drawAliveCell(i, j)
            for (i, j) in killedCells:
                self.eraseKilledCell(i, j)
            t2 = time.time()

            self._generation.set(self._generation.get() + 1)

            # Game is stopped if every cell is dead during a generation
            if self._nbCells.get() == 0:
                self.stop()

            # time beetween generations (milliseconds)
            self._dt = dtMax - (self._speed.get() - 1)/99*(dtMax - dtMin)
            # If the calculation time is over self._dt, we don't wait anymore to get to the next generation
            # Otherwise, we wait the right time to get to the next generation
            self.after(max(int(self._dt-1000*(t2-t1)), 1),
                       self.updateCellsState)


# Calls
window = MainWindow()
window.attributes('-zoomed',True)
window.mainloop()
