'''
An animated game called FloatOn
'''
 
from tkinter import *
import tkinter.messagebox #https://www.youtube.com/watch?v=IB6VkXJVf0Y
from random import randint
import time #https://docs.python.org/2/library/time.html
 
'''accurately called the exitClean method to close the animation program, but it still closes with errors'''

#draw floor 
def draw_floor(canvas):
    canvas.create_rectangle(0,500,1000,750, fill="black") 
       
#draw obstacles
def drawTopCube(canvas,top_cubeX):
    canvas.create_rectangle(top_cubeX,200,top_cubeX+100,300, 
                            fill="black", tag="T") 
 
def drawBottomCube(canvas, bottom_cubeX):
    canvas.create_rectangle(bottom_cubeX, 400, bottom_cubeX+100,500,
                            fill="black", tag="B")
    
#taken from lab 12 - helpers.py
def get_random_color():
    '''generate a random color to change the ball color after every 100 points'''
    return '#{:02X}{:02X}{:02X}'.format(randint(0,255), randint(0,255), randint(0,255))
             
#create the game animation
class FloatOnAnimation:
    '''Models a game that dodges obstacles
    Invariants:
        Width of the window must be 1000
        self.game must be True for the animation to run
        self.terminate must be False for the game to exit properly
    '''
    #constructor
    def __init__(self, window):
        self.window = window
        self.window.title("Float On")
        self.window.protocol('WM_DELETE_WINDOW', self.exitClean)
        self.canvas = Canvas(self.window, bg='white', width = 1000, 
                             height = 1000)
        self.canvas.pack()
        self.canvas.focus_set()
        draw_floor(self.canvas)

        #sets the speed of the game
        self.gameSpeed = 10
        self.ballSpeed = 32
    
        #variables to create the ball
        self.x1 = 175
        self.y1 = 275
        self.x2 = 325
        self.y2 = 425
        self.color = "black"
        self.game = True
        #variables to show where cubes start appearing on screen
        self.cube1 = 1000
        self.cube2 = 1000
        self.cube3 = 1000
        self.cube4 = 1000
        #variables to keep track of whether the cubes are on the screen
        self.cube1R = True
        self.cube2R = False
        self.cube3R = False
        self.cube4R = False
        #variables to generate random values to determine whether an obstacle will be on the top or bottom
        self.cube1Rand = 0
        self.cube2Rand = 0
        self.cube3Rand = 0
        self.cube4Rand = 0
        #variables to keep track of other features of the game
        self.tracker = 0
        self.scoretracker = 0
        self.running = True
        self.startTime = 0.0
        
        self.animate()

    #animation method
    def animate(self):
        '''creates an animation for the game'''
        self.drawBall(self.y1, self.color)
        #code needed to delay the start of the game to give user time to start
        self.canvas.update()
        self.canvas.after(1000)      
        #starts a timer to keep track of the "score"
        #binds arrow keys with the motion of the ball up and down
        self.canvas.bind('<Up>', self.processUp)
        self.canvas.bind('<Down>', self.processDown)
        self.canvas.bind('<space>', self.pause)
        self.canvas.after(1)
        #code to crash game if ball hits obstacle
        while self.game==True:
            if self.gameSpeed == 7:
                self.ballSpeed = 38
            elif self.gameSpeed == 8:
                self.ballSpeed = 32
            elif self.gameSpeed == 9:
                self.ballSpeed = 28
            elif self.gameSpeed == 10:
                self.ballSpeed = 23
            elif self.gameSpeed == 11:
                self.ballSpeed = 19
            self.canvas.update()
            if self.running: #keeps track if game is paused or not
                self.startTime = time.time() 
                cubes = [self.cube1, self.cube2, self.cube3, self.cube4]
                for each in cubes:
                    if (each > 90 and each < 250):
                        if cubes[0] == each:
                            if self.cube1Rand == 0:
                                if (self.y1 < 300):
                                    self.game = False
                            elif self.cube1Rand == 1:
                                if ((self.y1+150) > 400):
                                    self.game = False   
                        if cubes[1] == each:
                            if self.cube2Rand == 0:
                                if (self.y1 < 300):
                                    self.game = False
                            elif self.cube2Rand == 1:
                                if ((self.y1+150) > 400):
                                    self.game = False
                        if cubes[2] == each:
                            if self.cube3Rand == 0:
                                if (self.y1 < 300):
                                    self.game = False
                            elif self.cube3Rand == 1:
                                if ((self.y1+150) > 400):
                                    self.game = False
                        if cubes[3] == each:
                            if self.cube4Rand == 0:
                                if (self.y1 < 300):
                                    self.game = False
                            elif self.cube4Rand == 1:
                                if ((self.y1+150) > 400):
                                    self.game = False
                    #displays the current score in the top right corner as the game runs
                    #http://stackoverflow.com/questions/28840882/how-do-you-delete-a-create-text-in-a-canvas
                    scoreKeeper = time.time() - self.startTime
                    self.scoretracker += abs(scoreKeeper)
                    self.canvas.delete("scoreKeeper")
                    theScore = "Score: %d" % int(self.scoretracker*100)
                    self.canvas.create_text(935, 35, text=theScore, font=('Times', 25), tag="scoreKeeper")
                    
                f=open("high_score.txt")
                highScore = f.read()
                highScore = highScore.split(" ")
                TopMsg = "High Score: " + highScore[1]
                self.canvas.create_text(90, 25, text=TopMsg, font=('Times',25))
                f.close()
    
                self.canvas.delete("Ball")
    
                #make ball change color every 100 points
                if int(self.scoretracker*100) > 9 and int(self.scoretracker*100)%100 == 0:
                    self.color = get_random_color()
    
                #make sure canvas clears obstacles as necessary
                self.drawBall(self.y1, self.color)
                self.canvas.delete("T")
                self.canvas.delete("B")
    
                #starts rolling out cube 1 once cube 4 reaches 350
                if 650 <= self.cube4 <= 661:
                    self.cube1= 1000
                    self.cube1R = True
                    #randomize cube between top or bottom
                    self.cube1Rand = randint(0,1)
                if self.cube1Rand == 0:
                    drawTopCube(self.canvas, self.cube1)
                else:
                    drawBottomCube(self.canvas, self.cube1)
                
                #starts rolling out cube 2 once cube 1 reaches 350
                if 650 <= self.cube1 <= 661:
                    self.cube2 = 1000
                    self.cube2R = True
                    #randomize cube between top or bottom
                    self.cube2Rand = randint(0,1)
                if self.cube2Rand == 0:
                    drawTopCube(self.canvas, self.cube2)
                else:
                    drawBottomCube(self.canvas, self.cube2)
    
                #starts rolling out cube 3 once cube 2 reaches 350
                if 650 <= self.cube2 <= 661:
                    self.cube3 = 1000
                    self.cube3R = True
                    #randomize cube between top or bottom
                    self.cube3Rand = randint(0,1)
                if self.cube3Rand == 0:
                    drawTopCube(self.canvas, self.cube3)
                else:
                    drawBottomCube(self.canvas, self.cube3)
    
                #starts rolling out cube 4 once cube 3 reaches 350
                if 650 <= self.cube3 <= 661:
                    self.cube4 = 1000
                    self.cube4R = True
                    #randomize cube between top or bottom
                    self.cube4Rand = randint(0,1)
                if self.cube4Rand == 0:
                    drawTopCube(self.canvas, self.cube4)
                else:
                    drawBottomCube(self.canvas, self.cube4)
    
                #checks to see if the cube is on the screen or not
                if self.cube1 == -100:
                    self.cube1R = False
                if self.cube2 == -100:
                    self.cube2R = False
                if self.cube3 == -100:
                    self.cube3R = False
                if self.cube4 == -100:
                    self.cube4R = False
    
                #increments cube's X value if it is on the screen so that the cube moves across the screen
                if self.cube1R:
                    self.cube1 -= self.gameSpeed
                if self.cube2R:
                    self.cube2 -= self.gameSpeed
                if self.cube3R:
                    self.cube3 -= self.gameSpeed
                if self.cube4R:
                    self.cube4 -= self.gameSpeed
    
                #brings the circle back to the middle after a couple seconds, "reset"
                if self.tracker >= self.ballSpeed and self.y1 != 275:
                    self.y1 = 275
                    self.tracker = 0
                self.tracker+=1

                #speed up the game every 150 seconds
                if int(self.scoretracker*100) > 100 and int(self.scoretracker*1000)%1500 == 0:
                    if self.gameSpeed != 11:
                        self.gameSpeed += 1
                    else:
                        None
            else:
                None
            
        
        #self.window.destroy()
        self.canvas.delete("scoreKeeper")
        self.canvas.delete("Ball")
        self.canvas.delete("T")
        self.canvas.delete("B")
        #http://stackoverflow.com/questions/15457504/how-to-set-the-font-size-of-a-canvas-text-item
        self.canvas.create_text(500, 250, text="GAME OVER!", font=('Times', 75))
        
        #displays score on Game Over screen
        score = "Your score was: %d" %  int(self.scoretracker*100)
        self.canvas.create_text(500, 350, text=score, font=('Times', 25))

        self.GameOver()

    #game over method
    def GameOver(self):
        '''create a Game Over screen with options to retry or quit'''
        #variables to track the highest score
        f=open("high_score.txt")
        message = f.read()
        highname = message.split(" ")
        f.close()
        if int(self.scoretracker*100) > int(highname[1]):
            self.setHighscore()
            
        windowOver = Tk()
        windowOver.title("Game Over")
            

        def Retry():
            '''gives the option to retry the game'''
            self.exitClean()
            windowOver.destroy()
            gameWindow = Tk()
            gameWindow.title("Line Runner")
            FloatOnAnimation(gameWindow)
            
        def Quit():
            '''gives the option to quit the game'''
            self.exitClean()
            windowOver.destroy()
        
        retry = Button(windowOver, text="Retry", command=Retry).pack()
        quit = Button(windowOver, text="Quit", command=Quit).pack()
    
    #draw ball
    def drawBall(self, y1, color):
        ''' Draws the ball that 'moves' throughout the game'''
        self.canvas.create_oval(self.x1, y1, self.x2, y1+150,
                                fill=color, tag = "Ball")

    def setHighscore(self):
        def Enter():
            name = e.get()
            self.scorer = str(name) + ' ' + str(int(self.scoretracker*100))
            print(self.scorer)
            f.write(self.scorer)
            f.close()
            scoreWindow.destroy()

        f=open("high_score.txt", 'w')
        scoreWindow = Tk()
        scoreWindow.title("New High Score!")
            
        name_lbl = Label(scoreWindow, text="Please enter your first name: ", font=('Times', 40)).pack()
        e = Entry(scoreWindow, width=10)
        e.pack()
        self.scorer = ''
        close = Button(scoreWindow, text="Enter", command=Enter)
        close.pack()
    
    #up arrow key method 
    def processUp(self, event):
        ''' Method that gives the arrow key a function when the 'up' key is pressed'''
        self.canvas.delete("Ball")
        if self.y1 >= 275:
            self.y1 = self.y1 - 50
            self.tracker = 0
        else:
            None
    #down arrow key method 
    def processDown(self, event):
        ''' Method that gives the arrow key a function when the 'down' key is pressed'''
        self.canvas.delete("Ball")
        if self.y1 <= 275:
            self.y1 = self.y1 + 50
            self.tracker = 0
        else:
            None

    #spacebar key method
    def pause(self, event):
        ''' Method that gives the arrow key a function when the 'spacebar' key is pressed''' 
        if self.running == True:
            self.running = False
        else:
            self.running = True

    #taken from example in moodle: linesWithArrows.py
    def exitClean(self):
        '''makes sure program quits without error'''
        self.game = False
        #self.terminate = True
        self.window.destroy()

if __name__ == '__main__':
    root = Tk()
    app = FloatOnAnimation(root) 
    root.mainloop()

