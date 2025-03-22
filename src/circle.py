import tkinter as tk
import random
import math

from .utils import *

class Circle:
    def __init__(self, canvas:tk.Canvas, w_width:int, w_height:int, size:int, state_text:int, **kwargs):
        
        self.canvas = canvas
        self.color = kwargs["color"] if "color" in kwargs.keys() else "white"
        self.state_text = state_text
        self.w_width = w_width
        self.w_height = w_height
        self.size = size
        self.speed = 10
        self.eventFlag = False
        self.frame = 0
        self.eventworker = []
        self.now_event = []
        self.event_interval = kwargs["event_interval"] if "event_interval" in kwargs.keys() else 0
        self.last_event_frame = 0
        
        self.x = kwargs["x"] if "x" in kwargs.keys() else w_width / 2
        self.y = kwargs["y"]  if "y" in kwargs.keys() else w_height / 2
        
        self.object = self.canvas.create_oval(self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size, fill=self.color)
        self.dir = kwargs["dir"]  if "dir" in kwargs.keys() else random.randint(0, 360)
        
        #デフォルトのイベント設定用 divisionイベント用
        if "default_events" in kwargs.keys():
            for event in kwargs["default_events"]:
                match event:
                    case "change_color":
                        self.eventworker.append(self.event_change_color())
                    case "speedup":
                        self.eventworker.append(self.event_speedup())
        
    
    def update(self):
        self.frame += 1
        
        if self.frame - self.last_event_frame > self.event_interval and not self.eventFlag:
            self.randomevent()
            
        for i, work in enumerate(self.eventworker):
            if next(work) == 0:
                del self.eventworker[i]
                self.last_event_frame = self.frame
                self.canvas.itemconfigure(self.state_text, text="event:none")
        if len(self.eventworker) == 0:
            self.eventFlag = False
        
        

        
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
    
    def delete(self):
        self.canvas.delete(self.object)

    def randomevent(self):
        
        if self.eventFlag == False:
            self.eventFlag = True
            now_event = []
            
            event_overlap = 0
            
            while event_overlap == 0:
                
                r = random.randint(0, 2)
                #r = 2
                match r:
                    case 0:
                        now_event.append("change_color")
                        self.eventworker.append(self.event_change_color())
                    case 1:
                        now_event.append("speedup")
                        self.eventworker.append(self.event_speedup())
                    case 2:
                        now_event.append("division")
                        self.eventworker.append(self.event_division())
                
                event_overlap = random.randint(0, 1)
            
            disptext = "event:"
            self.now_event = now_event

            for event in now_event:
                if 1 < now_event.count(event):
                    disptext += f"{event}*{now_event.count(event)} + "
                    
                elif now_event.count(event) == 1:
                    disptext += f"{event} + "
                    
                now_event = [s for s in now_event if s != event]

            self.canvas.itemconfigure(self.state_text, text=disptext[0:-3])



    def event_temp(self):
        f = 0
        while f < 300:
            
            f += 1
            yield 1
        yield 0

    def event_change_color(self):
        f = 0
        while f < 300:
            rgb = [abs(int(sin(f)*255)), abs(int(sin(f+60)*255)), abs(int(sin(f+120)*255))]
            color = "#%02x%02x%02x" % tuple(rgb)
            self.canvas.itemconfigure(self.object, fill=color)
            f += 1
            yield 1
        self.canvas.itemconfigure(self.object, fill="white")
        yield 0
    
    def event_speedup(self):
        f = 0
        self.speed *= 2
        while f < 300:
            f += 1
            yield 1
        self.speed = 10
        yield 0

    def event_division(self):
        f = 0
        
        copy = Circle(self.canvas, self.w_width, self.w_height, self.size, self.state_text, event_interval=9999, x=self.x, y=self.y, default_events=self.now_event, color="#b0b0b0")
        while f < 300:
            copy.update()
            f += 1
            yield 1
        
        copy.delete()
        del copy
        yield 0