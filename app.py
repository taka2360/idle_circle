from src import *

import tkinter as tk
from tkinter import messagebox
import _tkinter
import time
import sys

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


class App:
    def __init__(self):
        self.close = False
        self.is_opening_settings = False
        
        self.mode = "circle"
        
        self.root = tk.Tk()
        self.root.title("idle circle")
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black", borderwidth=0, highlightthickness=0)
        self.root.bind("<Escape>", self.open_setting)
        self.canvas.pack()
        
        
        
        self.state_text = self.canvas.create_text(SCREEN_WIDTH-10, SCREEN_HEIGHT, text="event:none", fill="#b0b0b0", font=("Meiryo", 10), anchor="se")
        self.object = Circle(canvas=self.canvas, w_width=SCREEN_WIDTH, w_height=SCREEN_HEIGHT, size=20, state_text=self.state_text)
    
    def open_setting(self, _):
        
        self.setting_window = tk.Tk()
        self.setting_window.title("settings")
        self.setting_window.geometry("300x500")
        self.setting_window.resizable(False, False)
        
        self.setting_window.option_add("*tearOff", tk.FALSE)
        
        self.menu = tk.Menu(self.setting_window)
        self.menu_file = tk.Menu(self.setting_window)
        self.menu_file.add_command(label="このソフトを終了(X)", underline=3, command=self.menu_closeapp)
        self.menu_file.add_command(label="適用", command=self.settings_apply)
        self.menu.add_cascade(menu=self.menu_file, label="ファイル(F)", underline=5)
        
        self.menu_help = tk.Menu(self.setting_window)
        self.menu.add_cascade(menu=self.menu_help, label="ヘルプ(H)", underline=4)
        self.menu_help.add_command(label="このソフトについて", underline=3)
        self.menu_help.add_separator()
        self.menu_help.add_command(label="バージョン情報(V)", underline=3, command=self.menu_showinfo)
        
        self.settings_isborderless = tk.BooleanVar(self.setting_window)
        self.settings_isborderless.set(False)
        self.settings_cb = tk.Checkbutton(self.setting_window, variable=self.settings_isborderless, text='ボーダーレスウィンドウにする')
        self.settings_cb.place(x = 10, y=10)
        
        self.setting_window.config(menu=self.menu)
        self.setting_window.protocol("WM_DELETE_WINDOW", self.menu_closemenu)
        
        self.is_opening_settings = True
        
        self.setting_window.update()
    
    def relative_position(self, _) :
        cx, cy = self.root.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.root.bind('<Motion>', self.drag_wid)

    def drag_wid(self, _) :
        cx, cy = self.root.winfo_pointerxy()
        x = cx - self.relX
        y = cy - self.relY
        self.root.geometry('+%i+%i' % (x, y))

    def drag_unbind(self, _):
        self.root.unbind('<Motion>')

    def settings_apply(self):
        self.root.overrideredirect(self.settings_isborderless.get())
        if self.settings_isborderless.get():
            self.bindid1 = self.root.bind('<Button-1>', self.relative_position)
            self.bindid2 = self.root.bind('<ButtonRelease-1>', self.drag_unbind)
        else:
            self.root.unbind("<Button-1>")
            self.root.unbind('<ButtonRelease-1>')
        
        self.root.update()
    
    def menu_closemenu(self):
        self.setting_window.destroy()
        self.is_opening_settings = False
    
    def menu_closeapp(self):
        self.setting_window.destroy()
        self.is_opening_settings = False
        self.close = True
    
    def menu_showinfo(self):
        s = self.__class__.__name__
        s += " Version Beta 0.1(2025/3/20)\n"
        s += "©2025 Taka\n"
        s += "with Python " + sys.version
        messagebox.showinfo(self.__class__.__name__, s)


        
    
    def mainloop(self):
        while not self.close:
            if self.is_opening_settings:
                self.setting_window.update()
            else:
                self.object.update()
                self.root.update()
            time.sleep(1 / 60)
        
        self.root.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()