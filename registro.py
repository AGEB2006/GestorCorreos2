from tkinter import messagebox

from app_utils import poner_fondo_imagen
from customtkinter import *

from bd import registrar

set_appearance_mode("dark")

PREGUNTAS_SEGURIDAD = [
    "Como se llamo tu primera mascota?",
    "Cual es el nombre de tu papa?",
    "Cual es tu comida favorita?",
]

BACKGROUND_PATH = "paisaje-ilustracion-atardecer-en-el-bosque-montanas_3840x2160_xtrafondos.com.jpg"


def main():
    registro = CTk()
    registro.geometry("1200x700+250+50")
    registro.title("Registro")
    registro.configure(fg_color="#111111")

    poner_fondo_imagen(registro, BACKGROUND_PATH)

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

    telefono_label = CTkLabel(contenedor, text="Telefono:", text_color="#111111", fg_color="transparent")
    telefono_label.pack(pady=(10, 5))

    telefono_entry = CTkEntry(contenedor, width=260)
    telefono_entry.pack()

    contrasena_label = CTkLabel(contenedor, text="Contrasena:", text_color="#111111", fg_color="transparent")
    contrasena_label.pack(pady=(10, 5))

    contrasena_entry = CTkEntry(contenedor, width=260, show="*")
    contrasena_entry.pack()

    confirmar_label = CTkLabel(contenedor, text="Confirmar contrasena:", text_color="#111111", fg_color="transparent")
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

    def volver_login():
        registro.destroy()
        from login import ejecutar_login

        ejecutar_login()

    def registrar_usuario():
        nombre = nombre_entry.get().strip()
        correo = correo_entry.get().strip()
        telefono = telefono_entry.get().strip()
        contrasena = contrasena_entry.get().strip()
        confirmar = confirmar_entry.get().strip()
        pregunta = pregunta_var.get().strip()
        respuesta = respuesta_entry.get().strip()

        if not nombre or not correo or not telefono or not contrasena or not confirmar or not pregunta or not respuesta:
            messagebox.showwarning("Campos vacios", "Completa todos los campos antes de registrarte.")
            return

        if contrasena != confirmar:
            messagebox.showerror("Error", "Las contrasenas no coinciden.")
            return

        creado = registrar(correo, contrasena, nombre, telefono, pregunta, respuesta)
        if not creado:
            messagebox.showerror("Correo ya registrado", "Ese correo ya existe en la base de datos.")
            return

        messagebox.showinfo("Registro exitoso", "Tu cuenta se creo correctamente.")
        volver_login()

    btn_registrar = CTkButton(contenedor, text="Registrarse", command=registrar_usuario)
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


if __name__ == "__main__":
    main()
