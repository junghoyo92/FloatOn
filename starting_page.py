'''
Home screen of the game
'''

from tkinter import *
import controller

class StartingPage:
    def __init__(self):
        self.window = Tk()
        self.window.title("Float On")
        #http://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
        image = PhotoImage(file="startingpage.gif")
        self.lbl = Label(self.window, text="Welcome to Float On!", font=('Times', 70)).pack()
        play_button = Button(self.window, text="Play",command = self.PlayGame).pack()                      
        instructions_button = Button(self.window, text="Instructions",
                                     command=self.Instructions).pack()
        #highscore_button = Button(self.window, text="Highest Score",
        #                             command=self.HighScore).pack()
        self.imageLabel = Label(self.window, image=image).pack()
     
        
        self.window.mainloop()

    def PlayGame(self):
        '''create a button that when pressed, starts the game'''
        gameWindow = Tk()
        try:
            self.window.destroy()
        except:
            pass
        app = controller.FloatOnAnimation(gameWindow)
        gameWindow.mainloop()


    def Instructions(self):
        '''create a window displaying instructions of the game'''
        f = open("instructions.txt") 
        
        self.window = Tk()
        self.window.title("Instructions")
        
        #http://stackoverflow.com/questions/110923/close-a-tkinter-window
        def Close():
            '''create a button that will close the instructions window'''
            self.window.destroy()
    
        
        entry_msg = f.read()
        inst = Label(self.window, text=entry_msg).pack()
        close_button = Button(self.window, text="Close", command=Close).pack()
        
        self.window.mainloop()
    
    
    def HighScore(self):
        '''create a window that displays the highest score and the scorer'''
        f = open("high_score.txt") 
        
        self.window = Tk()
        self.window.title("High Score")
        
        #http://stackoverflow.com/questions/110923/close-a-tkinter-window
        def Close():
            '''create a button that will close the instructions window'''
            self.window.destroy()
        
        entry_msg = f.read()
        inst = Label(self.window, text=entry_msg).pack()
        close_button = Button(self.window, text="Close", command=Close).pack()
        
        self.window.mainloop()
        
StartingPage()
