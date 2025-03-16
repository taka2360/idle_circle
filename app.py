from src import *

import tkinter as tk
import _tkinter
import time

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


class App:
    def __init__(self):
        self.mode = "circle"
        
        self.root = tk.Tk()
        self.root.title("idle circle")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black", borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        
        self.state_text = self.canvas.create_text(SCREEN_WIDTH-10, SCREEN_HEIGHT, text="event:none", fill="#b0b0b0", font=("Meiryo", 10), anchor="se")
        self.object = Circle(canvas=self.canvas, w_width=SCREEN_WIDTH, w_height=SCREEN_HEIGHT, size=20, state_text=self.state_text)
    
    
    def mainloop(self):
        while True:
            
            self.object.update()
            
            self.root.update()
            time.sleep(1 / 60)


if __name__ == "__main__":
    app = App()
    app.mainloop()