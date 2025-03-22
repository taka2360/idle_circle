import math

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def tan(x):
    return math.tan(math.radians(x))

class Worker:
    def __init__(self):
        self.worker = list()
    
    def add_work(self, func):
        self.wo