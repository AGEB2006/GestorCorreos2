import os
import tkinter as tk
from customtkinter import *
from PIL import Image, ImageSequence, ImageTk

set_appearance_mode("dark")

login = CTk()
login.geometry("1200x700+250+50")
login.title("Login")
login.configure(fg_color="#111111")

BACKGROUND_PATH = "paisaje-ilustracion-atardecer-en-el-bosque-montanas_3840x2160_xtrafondos.com.jpg"


def poner_fondo(ruta):
    if not os.path.exists(ruta):
        return

    fondo = tk.Label(login, bd=0, highlightthickness=0, bg="#111111") 
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    fondo.lower()

    imagen_original = Image.open(ruta).convert("RGBA")

    def actualizar_fondo(_event=None):
        ancho = max(1, login.winfo_width())
        alto = max(1, login.winfo_height())
        imagen = imagen_original.resize((ancho, alto), Image.LANCZOS)
        fondo_actual = ImageTk.PhotoImage(imagen)
        fondo.configure(image=fondo_actual)
        fondo.image = fondo_actual

    login.bind("<Configure>", actualizar_fondo, add="+")
    login.update_idletasks()
    actualizar_fondo()


poner_fondo(BACKGROUND_PATH)


contenedor = CTkFrame(
    login,
    width=450,
    height=360,
    corner_radius=16,
    fg_color="#FFFFFF",
)
contenedor.place(relx=0.5, rely=0.5, anchor="center")
contenedor.pack_propagate(False)


title = CTkLabel(
    login,
    text="Iniciar Sesión",
    text_color="#FFFFFF",
    font=CTkFont(size=60, weight="bold"),
    fg_color="transparent",
    bg_color="transparent"
)
title.place(relx=0.5, rely=0.5, anchor="center", y=-230)
title.lift()  


correo_label = CTkLabel(contenedor, text="Correo:", text_color="#111111", fg_color="transparent")
correo_label.pack(pady=(25, 8))

correo_entry = CTkEntry(
    contenedor,
    width=260,
    fg_color="#FFFFFF",
    text_color="#111111",
)
correo_entry.pack(pady=5)

contraseña_label = CTkLabel(contenedor, text="Contraseña:", text_color="#111111", fg_color="transparent")
contraseña_label.pack(pady=(12, 8))

contraseña_entry = CTkEntry(
    contenedor,
    width=260,
    fg_color="#FFFFFF",
    text_color="#111111",
    show="*",
)
contraseña_entry.pack(pady=5)


def iniciar_sesion():
    correo = correo_entry.get()
    contraseña = contraseña_entry.get()
    print(f"Correo: {correo}, Contraseña: {contraseña}")

def crear_cuenta():
    print("Crear cuenta")

def recuperar_contraseña():
    print("Recuperar contraseña")

iniciar_sesion_button = CTkButton(
    contenedor,
    text="Iniciar Sesión",
    command=iniciar_sesion
)
iniciar_sesion_button.pack(pady=20)

contraseña_olvidada = CTkButton(
    contenedor,
    text="¿Olvidaste tu contraseña?",
    command=recuperar_contraseña,
    width=220,
    height=32,
    corner_radius=10,
    fg_color="transparent",
    hover_color=None,
    border_width=0,
    text_color="#111111",
)
contraseña_olvidada.pack(pady=(0, 10))

crear_cuenta_button = CTkButton(
    contenedor,
    text="Crear Cuenta",
    command=crear_cuenta,
    width=220,
    height=32,
    corner_radius=10,
    fg_color="#5A5A5A",
    hover_color="#474747",
    text_color="#FFFFFF",
)
crear_cuenta_button.pack(pady=10)

login.mainloop()