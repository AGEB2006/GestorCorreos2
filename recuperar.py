from tkinter import messagebox

from customtkinter import *

from bd import actualizar_contrasena, obtener_pregunta_seguridad, verificar_respuesta_seguridad


def abrir_recuperacion(ventana_padre, correo_entry, contrasena_entry):
    ventana_recuperacion = CTkToplevel(ventana_padre)
    ventana_recuperacion.title("Recuperar contrasena")
    ventana_recuperacion.geometry("460x560+500+180")
    ventana_recuperacion.minsize(460, 560)
    ventana_recuperacion.configure(fg_color="#1A1A1A")
    ventana_recuperacion.resizable(False, False)
    ventana_recuperacion.transient(ventana_padre)
    ventana_recuperacion.lift()
    ventana_recuperacion.focus_force()
    ventana_recuperacion.attributes("-topmost", True)
    ventana_recuperacion.after(200, lambda: ventana_recuperacion.attributes("-topmost", False))
    ventana_recuperacion.grab_set()

    titulo = CTkLabel(
        ventana_recuperacion,
        text="Recuperar contrasena",
        text_color="#FFFFFF",
        font=CTkFont(size=24, weight="bold"),
    )
    titulo.pack(pady=(20, 18))

    correo_rec_label = CTkLabel(ventana_recuperacion, text="Correo:", text_color="#FFFFFF")
    correo_rec_label.pack(pady=(0, 5))
    correo_rec_entry = CTkEntry(ventana_recuperacion, width=280)
    correo_rec_entry.pack(pady=(0, 10))
    correo_rec_entry.insert(0, correo_entry.get().strip())

    pregunta_mostrada = StringVar(value="Primero escribe tu correo y carga tu pregunta.")
    pregunta_label = CTkLabel(
        ventana_recuperacion,
        text="Pregunta de seguridad:",
        text_color="#FFFFFF",
    )
    pregunta_label.pack(pady=(0, 5))

    pregunta_valor = CTkLabel(
        ventana_recuperacion,
        textvariable=pregunta_mostrada,
        text_color="#D8D8D8",
        wraplength=340,
        justify="center",
    )
    pregunta_valor.pack(pady=(0, 10))

    respuesta_label = CTkLabel(ventana_recuperacion, text="Tu respuesta:", text_color="#FFFFFF")
    respuesta_label.pack(pady=(0, 5))
    respuesta_entry = CTkEntry(ventana_recuperacion, width=280)
    respuesta_entry.pack(pady=(0, 10))

    nueva_label = CTkLabel(ventana_recuperacion, text="Nueva contrasena:", text_color="#FFFFFF")
    nueva_label.pack(pady=(0, 5))
    nueva_entry = CTkEntry(ventana_recuperacion, width=280, show="*")
    nueva_entry.pack(pady=(0, 10))

    confirmar_label = CTkLabel(ventana_recuperacion, text="Confirmar contrasena:", text_color="#FFFFFF")
    confirmar_label.pack(pady=(0, 5))
    confirmar_entry = CTkEntry(ventana_recuperacion, width=280, show="*")
    confirmar_entry.pack(pady=(0, 16))

    def cargar_pregunta():
        correo = correo_rec_entry.get().strip()
        if not correo:
            messagebox.showwarning("Correo vacio", "Escribe tu correo primero.", parent=ventana_recuperacion)
            return

        pregunta = obtener_pregunta_seguridad(correo)
        if not pregunta:
            pregunta_mostrada.set("No se encontro pregunta de seguridad para ese correo.")
            return

        pregunta_mostrada.set(pregunta)

    def guardar_nueva_contrasena():
        correo = correo_rec_entry.get().strip()
        respuesta = respuesta_entry.get().strip()
        nueva = nueva_entry.get().strip()
        confirmar = confirmar_entry.get().strip()

        if not correo or not respuesta or not nueva or not confirmar:
            messagebox.showwarning("Campos vacios", "Completa todos los campos.", parent=ventana_recuperacion)
            return

        pregunta = obtener_pregunta_seguridad(correo)
        if not pregunta:
            messagebox.showerror(
                "Sin configuracion",
                "Ese correo no tiene pregunta de seguridad registrada.",
                parent=ventana_recuperacion,
            )
            return

        if nueva != confirmar:
            messagebox.showerror("Error", "Las contrasenas no coinciden.", parent=ventana_recuperacion)
            return

        if not verificar_respuesta_seguridad(correo, respuesta):
            messagebox.showerror(
                "Respuesta incorrecta",
                "La respuesta de seguridad no coincide.",
                parent=ventana_recuperacion,
            )
            return

        actualizado = actualizar_contrasena(correo, nueva)
        if not actualizado:
            messagebox.showerror("Correo no encontrado", "No existe una cuenta con ese correo.", parent=ventana_recuperacion)
            return

        correo_entry.delete(0, "end")
        correo_entry.insert(0, correo)
        contrasena_entry.delete(0, "end")
        contrasena_entry.insert(0, nueva)
        messagebox.showinfo(
            "Contrasena actualizada",
            "Ya puedes iniciar sesion con tu nueva contrasena.",
            parent=ventana_recuperacion,
        )
        ventana_recuperacion.destroy()

    btn_cargar_pregunta = CTkButton(
        ventana_recuperacion,
        text="Cargar pregunta",
        command=cargar_pregunta,
    )
    btn_cargar_pregunta.pack(pady=(0, 10))

    btn_guardar = CTkButton(
        ventana_recuperacion,
        text="Restablecer contrasena",
        command=guardar_nueva_contrasena,
    )
    btn_guardar.pack(pady=(0, 10))