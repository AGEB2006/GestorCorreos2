import os
import sys

# Agregar la ruta principal para poder importar bd, app_utils, Funciones, Clases
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from customtkinter import *

class TarjetaMensaje(CTkFrame):
    def __init__(self, master, bg_color, texto, botones_info=None):
        """
        botones_info: lista de tuplas (texto, color_fondo, color_hover, comando)
        """
        super().__init__(master, fg_color=bg_color, corner_radius=10)
        self.pack(anchor="e", pady=5, padx=10, fill="x")

        # Texto del mensaje
        etiqueta = CTkLabel(self, text=texto, text_color="white", wraplength=420, justify="left")
        etiqueta.pack(padx=10, pady=(10, 6), anchor="w")

        # Configuración de botones en línea
        if botones_info:
            acciones = CTkFrame(self, fg_color="transparent")
            acciones.pack(padx=10, pady=(0, 10), anchor="e")
            
            for index, (txt, bg, hover, width, cmd) in enumerate(botones_info):
                b = CTkButton(acciones, text=txt, fg_color=bg, hover_color=hover, width=width, command=cmd)
                b.pack(side="left", padx=(0, 8) if index < len(botones_info)-1 else 0)

class PanelInfo(CTkFrame):
    """ Un panel simple para mostrar avisos cuando no hay mensajes o contactos """
    def __init__(self, master, texto):
        super().__init__(master, fg_color="#3B3B3B", corner_radius=10)
        self.pack(anchor="e", pady=5, padx=10, fill="x")
        CTkLabel(self, text=texto, text_color="white", wraplength=420, justify="left").pack(padx=10, pady=(10, 6), anchor="w")
