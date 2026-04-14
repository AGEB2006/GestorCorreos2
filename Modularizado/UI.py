import os
import sys

# Agregar la ruta principal para poder importar bd, app_utils, Funciones, Clases
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk

# Importamos nuestros componentes reutilizables
from Componentes import TarjetaMensaje, PanelInfo

from Clases import Tooltip
from Funciones import (
    actualizar_borrador, eliminar_borrador, eliminar_definitivamente,
    eliminar_mensaje, enviar_mensaje, guardar_borrador,
    obtener_borrador_por_id, obtener_borradores, obtener_mensajes_enviados,
    obtener_mensajes_recibidos, obtener_papelera, restaurar_desde_papelera,
)
from app_utils import limpiar_sesion, resource_path
from bd import agregar_contacto_por_correo, eliminar_contacto, obtener_contactos, obtener_usuario_por_correo


def cargar_imagen(nombre_archivo, size):
    ruta = resource_path(nombre_archivo)
    if os.path.exists(ruta):
        try:
            return CTkImage(light_image=Image.open(ruta), dark_image=Image.open(ruta), size=size)
        except:
            return None
    return None

class AppCorreosV2(CTk):
    """ ¡NUEVA ARQUITECTURA! Todo el código espagueti ha sido reemplazado por componentes y llamadas limpias """
    def __init__(self, usuario_id="", nombre_usuario="Usuario", correo_usuario=""):
        super().__init__()
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.correo_usuario = correo_usuario
        self.borrador_actual_id = None
        self.vista_actual = "Recibidos"

        self.geometry("1400x800")
        self.title(f"Panel Modular - {self.nombre_usuario}")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.configurar_estructura()
        self.mostrar_mensajes_recibidos()

    def configurar_estructura(self):
        # --- Diseño principal Grid ---
        self.Fila = CTkFrame(self, fg_color="#2B2B2B", height=100)
        self.Fila.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.Pilar = CTkFrame(self, width=100, fg_color="#2B2B2B")
        self.Pilar.grid(row=1, column=0, sticky="nsew")

        self.Msj = CTkFrame(self, fg_color="white")
        self.Msj.grid(row=1, column=1, sticky="nsew")
        self.Contenedor_Msj = CTkScrollableFrame(self.Msj, fg_color="transparent", border_width=0, corner_radius=0)
        self.Contenedor_Msj.pack(fill="both", expand=True)

        # --- Contenido UI estático ---
        CTkLabel(self.Fila, text=f"Usuario: {self.nombre_usuario} | ID: {self.usuario_id}", font=("Arial", 20, "bold")).place(x=20, y=35)
        
        self.menu_lateral = CTkFrame(self.Pilar, fg_color="transparent")
        self.menu_lateral.pack(fill="x", padx=6, pady=20)
        
        self.configurar_paneles()
        self.configurar_botones()

    def configurar_paneles(self):
        """ Inicializa los paneles estáticos que se ocultan y muestran """
        # Panel de Cuenta
        self.frame_cuenta = CTkFrame(self.Msj, fg_color="#202020", corner_radius=10, width=420, height=280)
        CTkLabel(self.frame_cuenta, text="Cuenta", font=CTkFont(size=24, weight="bold")).pack(pady=(20, 12))
        CTkLabel(self.frame_cuenta, text=f"Nombre: {self.nombre_usuario}\nCorreo: {self.correo_usuario}", font=CTkFont(size=16)).pack(pady=(0, 24))
        CTkButton(self.frame_cuenta, text="Cerrar", command=self.cerrar_paneles_flotantes).pack(pady=10)

    def configurar_botones(self):
        """ Carga de botones e iconografia """
        # Botones creados mediante bucles para ahorrar código
        botones_ui = [
            ("Recibidos", cargar_imagen("recibido.png", (40, 40)), self.mostrar_mensajes_recibidos),
            ("Enviados", cargar_imagen("Enviado.png", (40, 40)), self.mostrar_mensajes_enviados),
            ("Papelera", cargar_imagen("basura.png", (40, 40)), self.mostrar_papelera),
        ]
        
        for index, (txt, img, cmd) in enumerate(botones_ui):
            b = CTkButton(self.menu_lateral, text=txt, image=img, width=88, height=42, fg_color="#3A3A3A", command=cmd)
            b.pack(fill="x", pady=(0, 10))
            Tooltip(self.Pilar, b, txt)

        # Cuenta
        CTkButton(self.Fila, text="Cuenta", width=100, height=36, command=lambda: self.frame_cuenta.place(relx=0.5, rely=0.5, anchor="center")).place(relx=0.9, rely=0.3)

    # --- LÓGICA DE VISTAS INTERCAMBIABLES ---
    def vaciar_contenedor(self):
        for widget in self.Contenedor_Msj.winfo_children(): widget.destroy()
        self.cerrar_paneles_flotantes()

    def cerrar_paneles_flotantes(self):
        self.frame_cuenta.place_forget()

    def mostrar_mensajes_recibidos(self):
        self.vaciar_contenedor()
        mensajes = obtener_mensajes_recibidos(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        
        if not mensajes:
            PanelInfo(self.Contenedor_Msj, "No tienes mensajes recibidos.")
            return

        for mensaje_id, _, remitente, asunto, contenido, fecha, _ in mensajes:
            # Aquí es donde se ahorran cientas de líneas:
            # Reutilizamos el componente TarjetaMensaje para construir la interfaz
            botones = [
                ("Enviar a papelera", "#8B1E1E", "#6F1818", 140, lambda mid=mensaje_id: self.borrar_vista(mid))
            ]
            TarjetaMensaje(
                self.Contenedor_Msj, "#3B3B3B", 
                f"De: {remitente}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido}\n\n{fecha}", 
                botones
            )

    def mostrar_mensajes_enviados(self):
        self.vaciar_contenedor()
        mensajes = obtener_mensajes_enviados(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        
        if not mensajes:
            PanelInfo(self.Contenedor_Msj, "No tienes mensajes enviados.")
            return

        for mensaje_id, _, destinatario, asunto, contenido, fecha, _ in mensajes:
            # Solo cambiar color azul y botones
            botones_enviados = [("A papelera", "#8B1E1E", "#6F1818", 140, lambda mid=mensaje_id: print("Borrar", mid))]
            TarjetaMensaje(
                self.Contenedor_Msj, "#24577A", 
                f"Para: {destinatario}\nAsunto: {asunto}\n\n{contenido}\n\n{fecha}", 
                botones_enviados
            )

    def mostrar_papelera(self):
        self.vaciar_contenedor()
        mensajes = obtener_papelera(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        
        if not mensajes:
            PanelInfo(self.Contenedor_Msj, "Papelera vacía.")
            return

        for mensaje_id, tipo, remitente, asunto, contenido, fecha in mensajes:
            botones_papelera = [
                ("Restaurar", "#1F6AA5", "#18527E", 100, lambda mid=mensaje_id: print("Restaurar", mid)),
                ("Borrar Definitivo", "#8B1E1E", "#6F1818", 130, lambda mid=mensaje_id: print("Borrar def", mid))
            ]
            TarjetaMensaje(
                self.Contenedor_Msj, "#4C3A3A", 
                f"{tipo.title()} de {remitente}\nAsunto: {asunto}\n\n{fecha}", 
                botones_papelera
            )

    def borrar_vista(self, mensaje_id):
        eliminar_mensaje(mensaje_id, int(self.usuario_id))
        self.mostrar_mensajes_recibidos()

if __name__ == "__main__":
    app = AppCorreosV2("1", "Dante", "dante@test.com")
    app.mainloop()