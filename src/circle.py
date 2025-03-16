import tkinter as tk
import random
import math

from .utils import *

class Circle:
    def __init__(self, canvas:tk.Canvas, w_width:int, w_height:int, size:int, state_text:int):
        self.canvas = canvas
        self.state_text = state_text
        self.w_width = w_width
        self.w_height = w_height
        self.size = size
        self.speed = 10
        self.now_event = 0
        self.frame = 0
        self.eventworker = []
        self.event_duration = 300
        self.last_event_frame = 0
        
        self.x = w_width / 2
        self.y = w_height / 2
        
        self.object = self.canvas.create_oval(self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size, fill="white")
        self.dir = random.randint(0, 360)
        
    
    def update(self):
        self.frame += 1
        self.last_event_frame 
        
        if self.frame - self.last_event_frame > 300 and self.now_event == 0:
            self.event()
            
        
        for i, work in enumerate(self.eventworker):
            if next(work) == 0:
                del self.eventworker[i]
                self.last_event_frame = self.frame
                self.canvas.itemconfigure(self.state_text, text="event:none")

        
        self.x += math.sin(math.radians(self.dir)) * self.speed
        self.y -= math.cos(math.radians(self.dir)) * self.speed
        
        if self.x < 0:
            if self.dir <= 270:
                self.dir -= (self.dir - 180) * 2
            else:
                self.dir += (360 - self.dir) * 2
        if self.w_width - self.size * 2 < self.x:
            if self.dir <= 90:
                self.dir -= self.dir * 2
            else:
                self.dir += (180 - self.dir) * 2
        if self.y < 0:
            if self.dir <= 90:
                self.dir += (90 - self.dir) * 2
            else:
                self.dir -= (self.dir - 270) * 2
        if self.w_height - self.size * 2 < self.y:
            if self.dir <= 180:
                self.dir += (270 - self.dir) * 2
            else:
                self.dir -= (self.dir - 90) * 2
        
        self.dir = self.dir % 360
        
        self.canvas.moveto(self.object, self.x, self.y)
        

    def event(self):
        if self.now_event == 0:
            if random.randint(0, 1) == 1:
                self.now_event = 1
                self.canvas.itemconfigure(self.state_text, text="event:change_color")
                self.eventworker.append(self.change_color())

    def change_color(self):
        f = 0
        while f < 300:
            rgb = [abs(int(sin(f)*255)), abs(int(sin(f+60)*255)), abs(int(sin(f+120)*255))]
            color = "#%02x%02x%02x" % tuple(rgb)
            self.canvas.itemconfigure(self.object, fill=color)
            f += 1
            yield 1
        self.canvas.itemconfigure(self.object, fill="white")
        yield 0
