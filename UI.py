import sys
from tkinter import messagebox

from Clases import Tooltip
from customtkinter import *
from PIL import Image

from Funciones import (
    actualizar_borrador,
    agregar_mensaje,
    eliminar_borrador,
    enviar_mensaje,
    guardar_borrador,
    obtener_borrador_por_id,
    obtener_borradores,
    obtener_mensajes_recibidos,
)
from bd import obtener_usuario_por_correo


def obtener_datos_usuario():
    usuario_id = sys.argv[1] if len(sys.argv) > 1 else ""
    nombre = sys.argv[2] if len(sys.argv) > 2 else "Usuario"
    correo = sys.argv[3] if len(sys.argv) > 3 else ""
    return usuario_id, nombre, correo


usuario_id, nombre_usuario, correo_usuario = obtener_datos_usuario()

Ventana = CTk()
Ventana.geometry("1200x700+250+50")
Ventana.title(f"Panel de {nombre_usuario}")
Ventana.grid_rowconfigure(1, weight=1)
Ventana.grid_columnconfigure(1, weight=1)

Fila = CTkFrame(Ventana, fg_color="#2B2B2B", height=100, corner_radius=-1, border_width=-1)
Fila.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
Fila.grid_columnconfigure(0, weight=1)
Fila.grid_columnconfigure(1, weight=0)

Pilar = CTkFrame(Ventana, width=100, height=100, fg_color="#2B2B2B", corner_radius=-1, border_width=-1)
Pilar.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

Msj = CTkFrame(Ventana, fg_color="white", corner_radius=-1, border_width=-1)
Msj.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
Contenedor_Msj = CTkScrollableFrame(Msj, fg_color="transparent", border_width=0, corner_radius=0)
Contenedor_Msj.pack(fill="both", expand=True)

info_usuario = CTkLabel(
    Fila,
    text=f"Usuario: {nombre_usuario}    Correo: {correo_usuario}    ID: {usuario_id}",
    text_color="white",
    font=CTkFont(size=20, weight="bold"),
)
info_usuario.grid(row=0, column=0, padx=20, pady=20, sticky="w")

borrador_actual_id = None


def limpiar_contenedor_mensajes():
    for widget in Contenedor_Msj.winfo_children():
        widget.destroy()


def mostrar_mensajes_recibidos():
    limpiar_contenedor_mensajes()
    mensajes = obtener_mensajes_recibidos(int(usuario_id)) if str(usuario_id).isdigit() else []

    if not mensajes:
        agregar_mensaje(Contenedor_Msj, "No tienes mensajes recibidos.", "recibido")
        return

    for _, _, remitente, asunto, contenido, fecha, _ in mensajes:
        texto = f"De: {remitente}\nAsunto: {asunto}\n\n{contenido}\n\n{fecha}"
        agregar_mensaje(Contenedor_Msj, texto, "recibido")


def mostrar_borradores():
    limpiar_contenedor_mensajes()
    borradores = obtener_borradores(int(usuario_id)) if str(usuario_id).isdigit() else []

    if not borradores:
        agregar_mensaje(Contenedor_Msj, "No tienes borradores guardados.", "enviado")
        return

    for borrador_id, asunto, contenido, fecha in borradores:
        tarjeta = CTkFrame(Contenedor_Msj, fg_color="#1F6AA5", corner_radius=10)
        tarjeta.pack(anchor="e", pady=5, padx=10, fill="x")

        texto = f"Asunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacío)'}\n\n{fecha}"
        label = CTkLabel(
            tarjeta,
            text=texto,
            text_color="white",
            wraplength=420,
            justify="left",
        )
        label.pack(padx=10, pady=(10, 6), anchor="w")

        acciones = CTkFrame(tarjeta, fg_color="transparent")
        acciones.pack(padx=10, pady=(0, 10), anchor="e")

        btn_editar = CTkButton(
            acciones,
            text="Editar",
            width=90,
            command=lambda bid=borrador_id: cargar_borrador_en_redactor(bid),
        )
        btn_editar.pack(side="left", padx=(0, 8))

        btn_eliminar = CTkButton(
            acciones,
            text="Eliminar",
            width=90,
            fg_color="#8B1E1E",
            hover_color="#6F1818",
            command=lambda bid=borrador_id: eliminar_borrador_y_refrescar(bid),
        )
        btn_eliminar.pack(side="left")


def limpiar_redactor():
    entry_dest.delete(0, "end")
    entry_asunto.delete(0, "end")
    textbox_contenido.delete("1.0", "end")


def preparar_redactor(titulo_boton="Enviar"):
    boton_guardar_borrador.configure(text="Guardar borrador")
    Enviar_Msj.configure(text=titulo_boton)


def cargar_borrador_en_redactor(borrador_id):
    global frame_visible, borrador_actual_id

    borrador = obtener_borrador_por_id(borrador_id)
    if not borrador:
        messagebox.showerror("Borrador no encontrado", "Ese borrador ya no existe.")
        mostrar_borradores()
        return

    _, asunto, contenido, _ = borrador
    borrar_estado_redactor()
    borrador_actual_id = borrador_id
    entry_asunto.insert(0, asunto or "")
    textbox_contenido.insert("1.0", contenido or "")
    Enviar_Msj.configure(text="Enviar borrador")
    boton_guardar_borrador.configure(text="Actualizar borrador")
    frame_redactar.place(relx=0.5, rely=0.5, anchor="center")
    frame_visible = True


def borrar_estado_redactor():
    global borrador_actual_id
    borrador_actual_id = None
    limpiar_redactor()
    preparar_redactor()


def guardar_borrador_desde_ui():
    global borrador_actual_id, frame_visible

    asunto = entry_asunto.get().strip()
    contenido = textbox_contenido.get("1.0", "end").strip()

    if not asunto and not contenido:
        messagebox.showwarning("Sin contenido", "Escribe asunto o contenido para guardar el borrador.")
        return

    if borrador_actual_id is None:
        borrador_actual_id = guardar_borrador(int(usuario_id), asunto, contenido)
        messagebox.showinfo("Borrador guardado", "El borrador se guardó correctamente.")
    else:
        actualizar_borrador(borrador_actual_id, asunto, contenido)
        messagebox.showinfo("Borrador actualizado", "Los cambios del borrador se guardaron.")

    frame_redactar.place_forget()
    frame_visible = False
    borrar_estado_redactor()
    mostrar_borradores()


def eliminar_borrador_y_refrescar(borrador_id):
    eliminado = eliminar_borrador(borrador_id)
    if eliminado:
        messagebox.showinfo("Borrador eliminado", "El borrador se eliminó correctamente.")
    mostrar_borradores()


def enviar_desde_ui():
    global frame_visible, borrador_actual_id

    destinatario = entry_dest.get().strip()
    asunto = entry_asunto.get().strip()
    contenido = textbox_contenido.get("1.0", "end").strip()

    if not destinatario or not asunto or not contenido:
        messagebox.showwarning("Campos vacios", "Completa destinatario, asunto y mensaje.")
        return

    destinatario_info = obtener_usuario_por_correo(destinatario)
    if not destinatario_info:
        messagebox.showerror("Correo no encontrado", "El correo destinatario no existe.")
        return

    enviar_mensaje(int(usuario_id), destinatario_info["id"], asunto, contenido)
    if borrador_actual_id is not None:
        eliminar_borrador(borrador_actual_id)
    frame_redactar.place_forget()
    frame_visible = False
    borrar_estado_redactor()
    messagebox.showinfo("Mensaje enviado", "El mensaje se envio correctamente.")
    mostrar_mensajes_recibidos()


def toggle_redactar():
    global frame_visible

    if not frame_visible:
        borrar_estado_redactor()
        frame_redactar.place(relx=0.5, rely=0.5, anchor="center")
        frame_visible = True
        return

    frame_redactar.place_forget()
    frame_visible = False
    borrar_estado_redactor()
    mostrar_borradores()


Enviar = CTkImage(
    light_image=Image.open("Lapiz.png"),
    dark_image=Image.open("Lapiz.png"),
    size=(30, 30),
)

frame_visible = False
frame_redactar = CTkFrame(
    Msj,
    fg_color="#202020",
    corner_radius=10,
    border_width=1,
    width=500,
    height=400,
)
frame_redactar.place_forget()
frame_redactar.grid_propagate(False)

label_dest = CTkLabel(frame_redactar, text="Para:")
label_dest.pack(pady=(10, 0))

entry_dest = CTkEntry(frame_redactar, width=300)
entry_dest.pack(pady=5)

label_asunto = CTkLabel(frame_redactar, text="Asunto:")
label_asunto.pack(pady=(10, 0))

entry_asunto = CTkEntry(frame_redactar, width=300)
entry_asunto.pack(pady=5)

label_contenido = CTkLabel(frame_redactar, text="Mensaje:")
label_contenido.pack(pady=(10, 0))

textbox_contenido = CTkTextbox(frame_redactar, width=350, height=150)
textbox_contenido.pack(pady=10)

Enviar_Msj = CTkButton(
    frame_redactar,
    text="Enviar",
    fg_color="#1F6AA5",
    hover_color="#3B3B3B",
    corner_radius=5,
    width=10,
    height=20,
    command=enviar_desde_ui,
)
Enviar_Msj.pack(pady=10)

boton_guardar_borrador = CTkButton(
    frame_redactar,
    text="Guardar borrador",
    fg_color="#5A5A5A",
    hover_color="#474747",
    command=guardar_borrador_desde_ui,
)
boton_guardar_borrador.pack(pady=(0, 10))

Boton_Enviar = CTkButton(Fila, text="", image=Enviar, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Enviar.grid(row=0, column=0, padx=0, pady=0, sticky="e")
Boton_Enviar.configure(command=toggle_redactar)
Tooltip(Fila, Boton_Enviar, "Redactar")

Borrador = CTkImage(
    light_image=Image.open("avion2.png"),
    dark_image=Image.open("avion2.png"),
    size=(70, 50),
)
Boton_Borrador = CTkButton(Pilar, text="", image=Borrador, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Borrador.place(x=10, y=25)
Boton_Borrador.configure(command=mostrar_borradores)
Tooltip(Pilar, Boton_Borrador, "Borradores")

Recibido = CTkImage(
    light_image=Image.open("recibido.png"),
    dark_image=Image.open("recibido.png"),
    size=(90, 70),
)
Boton_Recibido = CTkButton(Pilar, text="", image=Recibido, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Recibido.place(x=5, y=100)
Boton_Recibido.configure(command=mostrar_mensajes_recibidos)
Tooltip(Pilar, Boton_Recibido, "Recibido")

Borrar = CTkImage(
    light_image=Image.open("basura.png"),
    dark_image=Image.open("basura.png"),
    size=(70, 70),
)
Boton_Borrar = CTkButton(Pilar, text="", image=Borrar, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Borrar.place(x=10, y=200)
Tooltip(Pilar, Boton_Borrar, "Papelera")

Contactos = CTkImage(
    light_image=Image.open("contactos.png"),
    dark_image=Image.open("contactos.png"),
    size=(70, 70),
)
Boton_Contactos = CTkButton(Pilar, text="", image=Contactos, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Contactos.place(x=10, y=300)
Tooltip(Pilar, Boton_Contactos, "Contactos")

Cuenta = CTkImage(
    light_image=Image.open("cuenta.png"),
    dark_image=Image.open("cuenta.png"),
    size=(70, 70),
)
Boton_Cuenta = CTkButton(Fila, text="", image=Cuenta, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Cuenta.grid(row=0, column=1, padx=20, pady=20, sticky="e")
Tooltip(Fila, Boton_Cuenta, "Cuenta")

mostrar_mensajes_recibidos()

Ventana.mainloop()
