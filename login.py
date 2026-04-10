import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

from customtkinter import *
from PIL import Image, ImageTk

from bd import obtener_usuario_por_credenciales

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
    text="Iniciar Sesion",
    text_color="#FFFFFF",
    font=CTkFont(size=60, weight="bold"),
    fg_color="transparent",
    bg_color="transparent",
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

contrasena_label = CTkLabel(contenedor, text="Contrasena:", text_color="#111111", fg_color="transparent")
contrasena_label.pack(pady=(12, 8))

contrasena_entry = CTkEntry(
    contenedor,
    width=260,
    fg_color="#FFFFFF",
    text_color="#111111",
    show="*",
)
contrasena_entry.pack(pady=5)


def iniciar_sesion():
    correo = correo_entry.get().strip()
    contrasena = contrasena_entry.get().strip()

    if not correo or not contrasena:
        messagebox.showwarning("Campos vacios", "Ingresa tu correo y tu contrasena.")
        return

    usuario = obtener_usuario_por_credenciales(correo, contrasena)
    if not usuario:
        messagebox.showerror("Acceso denegado", "El correo o la contrasena no son correctos.")
        return

    login.destroy()
    subprocess.Popen(
        [
            sys.executable,
            "UI.py",
            str(usuario["id"]),
            usuario["nombre"],
            usuario["correo"],
        ]
    )


def crear_cuenta():
    login.destroy()
    subprocess.Popen([sys.executable, "registro.py"])


def recuperar_contrasena():
    messagebox.showinfo("Recuperar contrasena", "Esta funcion aun no esta implementada.")


iniciar_sesion_button = CTkButton(
    contenedor,
    text="Iniciar Sesion",
    command=iniciar_sesion,
)
iniciar_sesion_button.pack(pady=20)

contrasena_olvidada = CTkButton(
    contenedor,
    text="Olvidaste tu contrasena?",
    command=recuperar_contrasena,
    width=220,
    height=32,
    corner_radius=10,
    fg_color="transparent",
    hover_color=None,
    border_width=0,
    text_color="#111111",
)
contrasena_olvidada.pack(pady=(0, 10))

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
