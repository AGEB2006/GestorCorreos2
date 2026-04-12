import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

from customtkinter import *
from PIL import Image, ImageTk

from bd import registrar

set_appearance_mode("dark")

PREGUNTAS_SEGURIDAD = [
    "¿Cómo se llamó tu primera mascota?",
    "¿Cuál es el nombre de tu papá?",
    "¿Cuál es tu comida favorita?",
]

registro = CTk()
registro.geometry("1200x700+250+50")
registro.title("Registro")
registro.configure(fg_color="#111111")

BACKGROUND_PATH = "paisaje-ilustracion-atardecer-en-el-bosque-montanas_3840x2160_xtrafondos.com.jpg"


def poner_fondo(ruta):
    if not os.path.exists(ruta):
        return

    fondo = tk.Label(registro, bd=0, highlightthickness=0, bg="#111111")
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    fondo.lower()

    imagen_original = Image.open(ruta).convert("RGBA")

    def actualizar_fondo(_event=None):
        ancho = max(1, registro.winfo_width())
        alto = max(1, registro.winfo_height())
        imagen = imagen_original.resize((ancho, alto), Image.LANCZOS)
        fondo_actual = ImageTk.PhotoImage(imagen)
        fondo.configure(image=fondo_actual)
        fondo.image = fondo_actual

    registro.bind("<Configure>", actualizar_fondo, add="+")
    registro.update_idletasks()
    actualizar_fondo()


poner_fondo(BACKGROUND_PATH)

contenedor = CTkScrollableFrame(
    registro,
    width=450,
    height=540,
    corner_radius=16,
    fg_color="#FFFFFF",
)
contenedor.place(relx=0.5, rely=0.5, anchor="center")

title = CTkLabel(
    registro,
    text="Crear Cuenta",
    text_color="#FFFFFF",
    font=CTkFont(size=50, weight="bold"),
    fg_color="transparent",
    bg_color="transparent",
)
title.place(relx=0.5, rely=0.5, anchor="center", y=-290)
title.lift()

nombre_label = CTkLabel(contenedor, text="Nombre:", text_color="#111111", fg_color="transparent")
nombre_label.pack(pady=(20, 5))

nombre_entry = CTkEntry(contenedor, width=260)
nombre_entry.pack()

correo_label = CTkLabel(contenedor, text="Correo:", text_color="#111111", fg_color="transparent")
correo_label.pack(pady=(10, 5))

correo_entry = CTkEntry(contenedor, width=260)
correo_entry.pack()

telefono_label = CTkLabel(contenedor, text="Teléfono:", text_color="#111111", fg_color="transparent")
telefono_label.pack(pady=(10, 5))

telefono_entry = CTkEntry(contenedor, width=260)
telefono_entry.pack()

contrasena_label = CTkLabel(contenedor, text="Contraseña:", text_color="#111111", fg_color="transparent")
contrasena_label.pack(pady=(10, 5))

contrasena_entry = CTkEntry(contenedor, width=260, show="*")
contrasena_entry.pack()

confirmar_label = CTkLabel(contenedor, text="Confirmar contraseña:", text_color="#111111", fg_color="transparent")
confirmar_label.pack(pady=(10, 5))

confirmar_entry = CTkEntry(contenedor, width=260, show="*")
confirmar_entry.pack()

pregunta_label = CTkLabel(contenedor, text="Pregunta de seguridad:", text_color="#111111", fg_color="transparent")
pregunta_label.pack(pady=(10, 5))

pregunta_var = StringVar(value=PREGUNTAS_SEGURIDAD[0])
pregunta_menu = CTkOptionMenu(contenedor, values=PREGUNTAS_SEGURIDAD, variable=pregunta_var, width=260)
pregunta_menu.pack()

respuesta_label = CTkLabel(contenedor, text="Respuesta de seguridad:", text_color="#111111", fg_color="transparent")
respuesta_label.pack(pady=(10, 5))

respuesta_entry = CTkEntry(contenedor, width=260)
respuesta_entry.pack()


def registrar_usuario():
    nombre = nombre_entry.get().strip()
    correo = correo_entry.get().strip()
    telefono = telefono_entry.get().strip()
    contrasena = contrasena_entry.get().strip()
    confirmar = confirmar_entry.get().strip()
    pregunta = pregunta_var.get().strip()
    respuesta = respuesta_entry.get().strip()

    if not nombre or not correo or not telefono or not contrasena or not confirmar or not pregunta or not respuesta:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos antes de registrarte.")
        return

    if contrasena != confirmar:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    creado = registrar(correo, contrasena, nombre, telefono, pregunta, respuesta)
    if not creado:
        messagebox.showerror("Correo ya registrado", "Ese correo ya existe en la base de datos.")
        return

    messagebox.showinfo("Registro exitoso", "Tu cuenta se creó correctamente.")
    volver_login()


def volver_login():
    registro.destroy()
    subprocess.Popen([sys.executable, "login.py"])


btn_registrar = CTkButton(
    contenedor,
    text="Registrarse",
    command=registrar_usuario,
)
btn_registrar.pack(pady=(20, 12))

btn_volver = CTkButton(
    contenedor,
    text="Volver al login",
    command=volver_login,
    fg_color="#5A5A5A",
    hover_color="#474747",
)
btn_volver.pack(pady=(0, 20))

registro.mainloop()
