import os
import sys
import tkinter as tk
from tkinter import messagebox

from customtkinter import *
from PIL import Image, ImageTk

from app_utils import resource_path
from bd import obtener_usuario_por_credenciales
from recuperar import abrir_recuperacion

set_appearance_mode("dark")

BACKGROUND_PATH = "paisaje-ilustracion-atardecer-en-el-bosque-montanas_3840x2160_xtrafondos.com.jpg"


def poner_fondo(ventana, ruta):
    ruta_resuelta = resource_path(ruta)
    if not os.path.exists(ruta_resuelta):
        return

    fondo = tk.Label(ventana, bd=0, highlightthickness=0, bg="#111111")
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    fondo.lower()

    imagen_original = Image.open(ruta_resuelta).convert("RGBA")

    def actualizar_fondo(_event=None):
        ancho = max(1, ventana.winfo_width())
        alto = max(1, ventana.winfo_height())
        imagen = imagen_original.resize((ancho, alto), Image.LANCZOS)
        try:
            fondo_actual = ImageTk.PhotoImage(imagen)
        except Exception:
            fondo.configure(image="")
            fondo.image = None
            return

        fondo.configure(image=fondo_actual)
        fondo.image = fondo_actual

    ventana.bind("<Configure>", actualizar_fondo, add="+")
    ventana.update_idletasks()
    actualizar_fondo()


def ejecutar_login():
    login = CTk()
    login.geometry("1200x700+250+50")
    login.title("Login")
    login.configure(fg_color="#111111")

    poner_fondo(login, BACKGROUND_PATH)

    contenedor = CTkFrame(login, width=450, height=360, corner_radius=16, fg_color="#FFFFFF")
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

    correo_entry = CTkEntry(contenedor, width=260, fg_color="#FFFFFF", text_color="#111111")
    correo_entry.pack(pady=5)

    contrasena_label = CTkLabel(contenedor, text="Contrasena:", text_color="#111111", fg_color="transparent")
    contrasena_label.pack(pady=(12, 8))

    contrasena_entry = CTkEntry(contenedor, width=260, fg_color="#FFFFFF", text_color="#111111", show="*")
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
        from UI import main as main_ui

        main_ui(str(usuario["id"]), usuario["nombre"], usuario["correo"])

    def crear_cuenta():
        login.destroy()
        from registro import main as main_registro

        main_registro()

    def recuperar_contrasena():
        abrir_recuperacion(login, correo_entry, contrasena_entry)

    iniciar_sesion_button = CTkButton(contenedor, text="Iniciar Sesion", command=iniciar_sesion)
    iniciar_sesion_button.pack(pady=20)

    contrasena_olvidada = CTkButton(
        contenedor,
        text="Olvide mi contrasena",
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


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "login"

    if modo == "ui":
        from UI import main as main_ui

        usuario_id = sys.argv[2] if len(sys.argv) > 2 else ""
        nombre = sys.argv[3] if len(sys.argv) > 3 else "Usuario"
        correo = sys.argv[4] if len(sys.argv) > 4 else ""
        main_ui(usuario_id, nombre, correo)
        return

    if modo == "registro":
        from registro import main as main_registro

        main_registro()
        return

    ejecutar_login()


if __name__ == "__main__":
    main()
