from tkinter import *
dimensions = (640, 480)
class Shape(object):
    cwidth = dimensions[0]
    cheight = dimensions[1]
    mouseX = 0
    mouseY = 0
    def __init__(self,text="empty",x=0,y=0):
        self.text = text
        self.x = self.cwidth*x/100
        self.y = self.cheight*y/100
    def setText(self,text):
        self.text = text
    def setPosition(self,x,y):
        self.x = self.cwidth * x / 100
        self.y = self.cheight * y / 100

class Button(Shape):
    def __init__(self,text="empty",x=0,y=0):
        super().__init__(text,x,y)
        self.highlighted = False
        self.height = 0.15 * Shape.cheight
        self.width = 0.3 * Shape.cwidth
    def widthScale(self,adjust):
        self.width*=adjust
    def heightScale(self,adjust):
        self.height*=adjust
    def scale(self,adjust):
        self.width*=adjust
        self.height*=adjust
    def checkWithinBounds(self,x,y):
        if(x>=self.width/2+self.x or x<=self.x-self.width/2):
           return False
        if(y >= self.height/2 + self.y or y <= self.y - self.height/2):
            return False
        return True
    def getBounds(self):
        return (self.x-self.width/2,self.y-self.height/2,self.x+self.width/2,self.y+self.height/2)
    def draw(self,canvas,overide = False):
        if(overide):
            canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2,
                                    self.y + self.height / 2, fill="white", width=4)
            canvas.create_text(self.x, self.y, text=self.text, font="Helvetica " + str(int(self.width / 6)))
            return None
        if(self.checkWithinBounds(Shape.mouseX,Shape.mouseY)):
            self.highlighted=True
        else:
            self.highlighted=False
        if(self.highlighted==False):
            canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,self.x+self.width/2,self.y+self.height/2,fill="white",width=4)
            canvas.create_text(self.x, self.y, text=self.text, font="Helvetica " + str(int(self.width / 6)))
        else:
            canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,self.x+self.width/2,self.y+self.height/2,fill="light goldenrod yellow",width=5)
            canvas.create_text(self.x, self.y, text=self.text, font="Helvetica " + str(int(self.width / 6)) + " bold")
    def clear(self,canvas):
        canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2,
                                self.y + self.height / 2, fill="white", width=4,outline = "white")

class ColorButton(Button):
    def __init__(self,x,y,color):
        self.x = Shape.cwidth * x / 100
        self.y = Shape.cheight * y / 100
        self.height = 0.15 * Shape.cwidth
        self.width = 0.15 * Shape.cwidth
        self.color = color
    def draw(self,canvas):
        if (self.checkWithinBounds(Shape.mouseX, Shape.mouseY)):
            self.highlighted = True
        else:
            self.highlighted = False
        if(self.highlighted==False):
            canvas.create_rectangle(self.x-self.width/2,self.y-self.height/2,self.x+self.width/2,self.y+self.height/2,fill = self.color,width = 3)
        else:
            canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2,\
                                    self.y + self.height / 2, fill=self.color, width=5)

class ImageButton(ColorButton):
    def draw(self,canvas,image):
        if (self.checkWithinBounds(Shape.mouseX, Shape.mouseY)):
            self.highlighted = True
        else:
            self.highlighted = False
        if (self.highlighted == False):
            canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2,
                                    self.y + self.height / 2, fill=self.color, width=2)
            canvas.create_image(self.x, self.y, anchor=CENTER, image=image)
        else:
            canvas.create_rectangle(self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2,
                                    self.y + self.height / 2, fill=self.color, width=6)
            canvas.create_image(self.x, self.y, anchor=CENTER, image=image)



class Text(Shape):
    def draw(self,canvas,size,anc=None):
        if(anc!=None):
            canvas.create_text(self.x, self.y, text=self.text, font="Helvetica " + str(int(size)),anchor=anc)
        else:
            canvas.create_text(self.x,self.y,text = self.text,font="Helvetica " +str(int(size)))

