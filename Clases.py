
from customtkinter import *

class Tooltip(CTkLabel):
    def __init__(self, parent, widget, text):
        self.widget = widget
        self.parent = parent

        self.tooltip = CTkLabel(
            parent,
            text = text,
            fg_color="#2B2B2B",
            text_color="white",
            corner_radius=6
        )
    
        widget.bind("<Enter>", self.mostrar)
        widget.bind("<Leave>", self.ocultar)    
    def mostrar(self, event):
     self.tooltip.update_idletasks()
     x = self.widget.winfo_x()
     y = self.widget.winfo_y()
     self.tooltip.place(
        x=x + self.widget.winfo_width()//2 - self.tooltip.winfo_width()//2,
        y=y + self.widget.winfo_height() - 40
    )
     self.tooltip.lift()
    def ocultar(self, event):
        self.tooltip.place_forget()
        