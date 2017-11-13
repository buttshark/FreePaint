from tkinter import *
import graphicObjects
import backend
import cv2

def init(data):
    data.falseValue = 0
    data.drawing=False
    data.sliding = False
    data.margin = 50
    data.boxW, data.boxH = 10, 25
    data.sizeIncrement = (data.width - data.margin * 2) // 5
    data.penColor = "black"
    data.penSize = 2
    data.penType = "pen"
    data.points = []
    data.mode = 0
    data.timerCounter = 0
    data.timerDelay = 5 # milliseconds
    data.startButton = graphicObjects.Button("DRAW", 75, 75)
    data.helpButton = graphicObjects.Button("HELP",25,75)
    data.homeButton = graphicObjects.Button("Back",8,5)
    data.homeButton.scale(0.4)
    data.backButton = graphicObjects.Button("Back", 8, 5)
    data.backButton.scale(0.4)
    data.mainText = graphicObjects.Text("Drawing Board",50,20)
    data.helpText = graphicObjects.Text("Help",50,10)
    data.colorsText = graphicObjects.Text("Colors", 50, 10)
    data.sizeText = graphicObjects.Text("Size", 50, 10)
    data.penText = graphicObjects.Text("Tool", 50, 10)
    data.exitText = graphicObjects.Text("Press Esc to Go Back", 50, 90)
    data.colorButtons = []
    data.colors = ("red","orange","yellow","green","dodger blue","dark slate blue","magenta4","black")
    for i in range(int(len(data.colors)/2)):
        data.colorButtons.append(graphicObjects.ColorButton((i+1)*20,35,data.colors[i]))
    for i in range(int(len(data.colors)/2),len(data.colors)):
        data.colorButtons.append(graphicObjects.ColorButton((i+1-int(len(data.colors)/2))*20,65,data.colors[i]))
    data.eraser = PhotoImage(file="eraser.gif")
    data.eraserButton = graphicObjects.ImageButton(30,50,None)
    data.pen = PhotoImage(file="pen.gif")
    data.penButton = graphicObjects.ImageButton(70, 50, None)

def motion(event,data):
    graphicObjects.Shape.mouseX,graphicObjects.Shape.mouseY = event.x,event.y
    """if(data.mode==1):
        if b1 == "down":
            bounds = data.homeButton.getBounds()
            if((event.x<bounds[2] and event.y<bounds[3]) or event.x<0 or event.y<0):
                return None
            global xold, yold
            if xold is not None and yold is not None:
                event.widget.create_line(xold,yold,event.x,event.y,smooth=TRUE,width=data.penSize,fill=data.penColor)
                              # here's where you draw it. smooth. neat.
            xold = event.x
            yold = event.y
            data.points.append(tuple((xold,yold,data.penSize,data.penColor)))"""
    if (data.mode == 4):
        if b1 == "down":
            if (data.sliding):
                x = event.x
                if (x > data.margin and x < data.width - data.margin):
                    data.penSize = (x - 50 + data.sizeIncrement // 2) // data.sizeIncrement + 1

def mousePressed(event, data,canvas):
    global b1
    b1 = "down"
    if(data.mode==0):
        data.penType = "pen"
        data.penColor = 'black'
        if(data.startButton.checkWithinBounds(event.x,event.y)):
            preDrawingSetup(canvas,data)
            data.mode=1
        elif(data.helpButton.checkWithinBounds(event.x,event.y)):
            data.mode=2
    if(data.mode==1):
        if (data.homeButton.checkWithinBounds(event.x, event.y)):
            data.mode = 0
            data.points = []
    if (data.mode == 2):
        if (data.homeButton.checkWithinBounds(event.x, event.y)):
            data.mode = 0
    if(data.mode==3): #colors
        if(data.backButton.checkWithinBounds(event.x,event.y)):
            data.mode = 1
            preDrawingSetup(canvas, data)
            restoreImage(canvas, data)
        for i in range(len(data.colorButtons)):
            if (data.colorButtons[i].checkWithinBounds(event.x, event.y)):
                data.penColor = data.colorButtons[i].color
                if(data.penType=="eraser"):
                    data.penColor = "white"
                data.mode = 1
                preDrawingSetup(canvas, data)
                restoreImage(canvas, data)
    if (data.mode == 4):
        if (checkSliding(data, event.x, event.y)):
            data.sliding = True
        else:
            data.sliding = False
        if (data.backButton.checkWithinBounds(event.x, event.y)):
            data.mode = 1
            preDrawingSetup(canvas, data)
            restoreImage(canvas, data)
    if (data.mode == 5):
        if (data.backButton.checkWithinBounds(event.x, event.y)):
            data.mode = 1
            preDrawingSetup(canvas, data)
            restoreImage(canvas, data)
        if (data.eraserButton.checkWithinBounds(event.x, event.y)):
            data.penType = "eraser"
            data.penColor = "white"
            data.mode = 1
            preDrawingSetup(canvas, data)
            restoreImage(canvas, data)
        elif (data.penButton.checkWithinBounds(event.x, event.y)):
            data.penType = "pen"
            data.penColor = "black"
            data.mode = 1
            preDrawingSetup(canvas, data)
            restoreImage(canvas, data)

def restoreImage(canvas,data):
    for i in range(len(data.points)-1):
        canvas.create_line(data.points[i][0], data.points[i][1], data.points[i+1][0], data.points[i+1][1], smooth=TRUE,width = data.points[i][2],fill = data.points[i][3])

def keyPressed(event,canvas,data):
    if(data.mode!=0 and data.mode!=2):
        if(event.keysym=="2"):
            data.mode=3
        if (event.keysym == "3"):
            data.mode = 4
        if (event.keysym == "4"):
            data.mode = 5
        if(event.keysym=="c"):
            canvas.delete(ALL)
            canvas.update()
            data.backButton.draw(canvas)
            data.points = []
    if(data.mode!=1):
        if(event.keysym=="Escape"):
            preDrawingSetup(canvas,data)
            data.mode = 1
            restoreImage(canvas, data)
    elif(data.mode==1):
        if (event.keysym == "Escape"):
            data.mode = 0
            data.points = []

def timerFired(data,canvas):
    coord,fingers = backend.getInfo()
    if(fingers!=0 and coord[0]!=None and coord[1]!=None):
        data.drawing=True
    else:
        data.drawing=False
        global b1, xold, yold
        xold = None  # reset the line when you let go of the button
        yold = None
    print(data.drawing)
    if(data.mode==1 and data.drawing):
        print("drawing")
        bounds = data.homeButton.getBounds()
        if ((coord[0] < bounds[2] and coord[1] < bounds[3]) or coord[0] < 0 or coord[1] < 0):
            return None
        if(xold!=None and yold!=None):
            if(abs(coord[0]-xold)>130 or abs(coord[1]-yold)>130):
                if(data.falseValue>3):
                    xold = None
                    yold = None
                    data.falseValue = 0
                else:
                    data.falseValue+=1
                return None
        #global xold, yold
        if xold is not None and yold is not None:
            canvas.create_line(xold, yold, coord[0], coord[1], smooth=TRUE, width=data.penSize, fill=data.penColor)
            # here's where you draw it. smooth. neat.
        xold = coord[0]
        yold = coord[1]
        data.points.append(tuple((xold, yold, data.penSize, data.penColor)))
    print(coord,fingers)

def checkSliding(data, x, y):
    x1, x2 = data.margin - data.boxW // 2 + (data.penSize - 1) * data.sizeIncrement, data.margin + data.boxW // 2 + (
    data.penSize - 1) * data.sizeIncrement
    y1, y2 = data.height // 2 - data.boxH // 2, data.height // 2 + data.boxH // 2
    if (not (x >= x1 and x <= x2 and y >= y1 and y <= y2)):
        return False
    return True

def drawHelp(data,canvas):
    data.helpText.draw(canvas, 50)
    data.homeButton.draw(canvas)
    graphicObjects.Text("- Press 2 To Change Color",5,20,).draw(canvas,25,"nw")
    graphicObjects.Text("- Press 3 To Change Size", 5, 28, ).draw(canvas, 25, "nw")
    graphicObjects.Text("- Press 4 To Change Tool", 5, 36, ).draw(canvas, 25, "nw")
    graphicObjects.Text("- Press c To Clear Canvas", 5, 44, ).draw(canvas, 25, "nw")

def drawSlider(data, canvas):
    drawSlideBack(canvas, data)
    drawSlideBox(canvas, data)
    drawSlideText(canvas, data)

def drawSlideBack(canvas, data):
    x1, x2 = data.margin, data.width - data.margin
    y1, y2 = data.height // 2 - 6, data.height // 2 + 6
    canvas.create_rectangle(x1, y1, x2, y2, fill="black", width=0)
    x1, x2 = data.margin, data.margin + data.sizeIncrement * (data.penSize - 1)
    y1, y2 = data.height // 2 - 2, data.height // 2 + 2
    canvas.create_rectangle(x1 + 4, y1, x2 - 4, y2, fill="gray", width=0)

def drawSlideText(canvas, data):
    canvas.create_text(data.width - data.margin // 2, data.height // 2, text=str(data.penSize))

def drawSlideBox(canvas, data):
    x1, x2 = data.margin - data.boxW // 2 + (data.penSize - 1) * data.sizeIncrement, data.margin + data.boxW // 2 + (
    data.penSize - 1) * data.sizeIncrement
    y1, y2 = data.height // 2 - data.boxH // 2, data.height // 2 + data.boxH // 2
    canvas.create_rectangle(x1, y1, x2, y2, fill="orange", width=0)

def redrawAll(canvas, data):
    if(data.mode==0): #start screen
        data.startButton.draw(canvas)
        data.helpButton.draw(canvas)
        data.mainText.draw(canvas,60)
    elif(data.mode==1): #drawing panel
        pass
    elif(data.mode==2): #help
        drawHelp(data,canvas)
    elif(data.mode==3):#colors
        data.colorsText.draw(canvas,50)
        data.backButton.draw(canvas)
        for i in range(len(data.colorButtons)):
            data.colorButtons[i].draw(canvas)
        data.exitText.draw(canvas, 38)
    elif (data.mode == 4):  # size
        data.sizeText.draw(canvas, 50)
        data.backButton.draw(canvas)
        drawSlider(data, canvas)
        data.exitText.draw(canvas, 38)
    elif (data.mode == 5):  # pen
        data.penText.draw(canvas,50)
        data.backButton.draw(canvas)
        data.exitText.draw(canvas,38)
        data.eraserButton.draw(canvas,data.eraser)
        data.penButton.draw(canvas, data.pen)

def preDrawingSetup(canvas,data):
    canvas.delete(ALL)
    canvas.update()
    data.homeButton.highlighted=False
    data.homeButton.draw(canvas,True)

#from 112 barebones event handling
def run(width,height):
    def redrawAllWrapper(canvas, data):
        if(data.mode!=1):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height,
                                    fill='white', width=0)
            redrawAll(canvas, data)
        canvas.update()

    def b1up(event):
        global b1, xold, yold
        b1 = "up"
        xold = None  # reset the line when you let go of the button
        yold = None

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data,canvas)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event,canvas, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data,canvas)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data)
    # set up events
    root.bind("<ButtonRelease-1>", b1up)
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event:
                            motion(event, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run(graphicObjects.dimensions[0],graphicObjects.dimensions[1])

