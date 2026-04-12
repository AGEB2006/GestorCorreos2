import sys
from tkinter import messagebox

from Clases import Tooltip
from customtkinter import *
from PIL import Image

from Funciones import (
    actualizar_borrador,
    eliminar_borrador,
    eliminar_definitivamente,
    eliminar_mensaje,
    enviar_mensaje,
    guardar_borrador,
    obtener_borrador_por_id,
    obtener_borradores,
    obtener_mensajes_recibidos,
    obtener_papelera,
    restaurar_desde_papelera,
)
from bd import agregar_contacto_por_correo, eliminar_contacto, obtener_contactos, obtener_usuario_por_correo


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


def crear_tarjeta_mensaje(color="#3B3B3B"):
    tarjeta = CTkFrame(Contenedor_Msj, fg_color=color, corner_radius=10)
    tarjeta.pack(anchor="e", pady=5, padx=10, fill="x")
    return tarjeta


def agregar_texto_tarjeta(tarjeta, texto):
    label = CTkLabel(
        tarjeta,
        text=texto,
        text_color="white",
        wraplength=420,
        justify="left",
    )
    label.pack(padx=10, pady=(10, 6), anchor="w")


def crear_acciones_tarjeta(tarjeta):
    acciones = CTkFrame(tarjeta, fg_color="transparent")
    acciones.pack(padx=10, pady=(0, 10), anchor="e")
    return acciones


def mostrar_tarjeta_info(texto):
    tarjeta = crear_tarjeta_mensaje("#3B3B3B")
    agregar_texto_tarjeta(tarjeta, texto)


def mostrar_mensajes_recibidos():
    limpiar_contenedor_mensajes()
    mensajes = obtener_mensajes_recibidos(int(usuario_id)) if str(usuario_id).isdigit() else []

    if not mensajes:
        mostrar_tarjeta_info("No tienes mensajes recibidos.")
        return

    for mensaje_id, _, remitente, asunto, contenido, fecha, _ in mensajes:
        tarjeta = crear_tarjeta_mensaje("#3B3B3B")
        texto = f"De: {remitente}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacío)'}\n\n{fecha}"
        agregar_texto_tarjeta(tarjeta, texto)
        acciones = crear_acciones_tarjeta(tarjeta)

        btn_eliminar = CTkButton(
            acciones,
            text="Enviar a papelera",
            width=140,
            fg_color="#8B1E1E",
            hover_color="#6F1818",
            command=lambda mid=mensaje_id: mover_mensaje_a_papelera(mid),
        )
        btn_eliminar.pack(side="left")


def mostrar_borradores():
    limpiar_contenedor_mensajes()
    borradores = obtener_borradores(int(usuario_id)) if str(usuario_id).isdigit() else []

    if not borradores:
        mostrar_tarjeta_info("No tienes borradores guardados.")
        return

    for borrador_id, asunto, contenido, fecha in borradores:
        tarjeta = crear_tarjeta_mensaje("#1F6AA5")
        texto = f"Asunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacío)'}\n\n{fecha}"
        agregar_texto_tarjeta(tarjeta, texto)
        acciones = crear_acciones_tarjeta(tarjeta)

        btn_editar = CTkButton(
            acciones,
            text="Editar",
            width=90,
            command=lambda bid=borrador_id: cargar_borrador_en_redactor(bid),
        )
        btn_editar.pack(side="left", padx=(0, 8))

        btn_eliminar = CTkButton(
            acciones,
            text="Enviar a papelera",
            width=140,
            fg_color="#8B1E1E",
            hover_color="#6F1818",
            command=lambda bid=borrador_id: eliminar_borrador_y_refrescar(bid),
        )
        btn_eliminar.pack(side="left")


def mostrar_papelera():
    limpiar_contenedor_mensajes()
    elementos = obtener_papelera(int(usuario_id)) if str(usuario_id).isdigit() else []

    if not elementos:
        mostrar_tarjeta_info("La papelera está vacía.")
        return

    for mensaje_id, tipo, remitente, asunto, contenido, fecha in elementos:
        color = "#5A5A5A" if tipo == "borrador" else "#4C3A3A"
        tarjeta = crear_tarjeta_mensaje(color)
        etiqueta_tipo = "Borrador" if tipo == "borrador" else "Mensaje"
        texto = (
            f"{etiqueta_tipo} en papelera\n"
            f"Referencia: {remitente}\n"
            f"Asunto: {asunto or '(sin asunto)'}\n\n"
            f"{contenido or '(vacío)'}\n\n{fecha}"
        )
        agregar_texto_tarjeta(tarjeta, texto)
        acciones = crear_acciones_tarjeta(tarjeta)

        btn_restaurar = CTkButton(
            acciones,
            text="Restaurar",
            width=100,
            command=lambda mid=mensaje_id: restaurar_desde_papelera_y_refrescar(mid),
        )
        btn_restaurar.pack(side="left", padx=(0, 8))

        btn_borrar = CTkButton(
            acciones,
            text="Borrar definitivo",
            width=130,
            fg_color="#8B1E1E",
            hover_color="#6F1818",
            command=lambda mid=mensaje_id: borrar_definitivo_y_refrescar(mid),
        )
        btn_borrar.pack(side="left")


def limpiar_redactor():
    entry_dest.delete(0, "end")
    entry_asunto.delete(0, "end")
    textbox_contenido.delete("1.0", "end")


def limpiar_panel_contactos():
    for widget in lista_contactos.winfo_children():
        widget.destroy()


def cerrar_panel_contactos():
    frame_contactos.place_forget()


def mostrar_contactos():
    limpiar_panel_contactos()
    frame_contactos.place(relx=0.5, rely=0.5, anchor="center")

    contactos = obtener_contactos(int(usuario_id)) if str(usuario_id).isdigit() else []

    if not contactos:
        aviso = CTkLabel(
            lista_contactos,
            text="No tienes contactos agregados.\nPuedes agregar uno usando su correo.",
            justify="center",
        )
        aviso.pack(pady=30)
        return

    for relacion_id, nombre, correo in contactos:
        tarjeta = CTkFrame(lista_contactos, fg_color="#2F2F2F", corner_radius=10)
        tarjeta.pack(fill="x", padx=10, pady=6)

        texto = CTkLabel(
            tarjeta,
            text=f"{nombre or correo}\n{correo}",
            justify="left",
            text_color="white",
        )
        texto.pack(side="left", padx=12, pady=10)

        boton_quitar = CTkButton(
            tarjeta,
            text="Quitar",
            width=90,
            fg_color="#8B1E1E",
            hover_color="#6F1818",
            command=lambda rid=relacion_id: quitar_contacto_y_refrescar(rid),
        )
        boton_quitar.pack(side="right", padx=12, pady=10)


def agregar_contacto_desde_ui():
    correo_contacto = entry_contacto_correo.get().strip()

    if not correo_contacto:
        messagebox.showwarning("Correo vacío", "Escribe el correo del contacto.")
        return

    exito, resultado = agregar_contacto_por_correo(int(usuario_id), correo_contacto)
    if not exito:
        messagebox.showerror("No se pudo agregar", resultado)
        return

    entry_contacto_correo.delete(0, "end")
    messagebox.showinfo("Contacto agregado", f"Se agregó a {resultado['nombre']} correctamente.")
    mostrar_contactos()


def quitar_contacto_y_refrescar(relacion_id):
    if eliminar_contacto(relacion_id):
        messagebox.showinfo("Contacto eliminado", "El contacto se quitó de tu lista.")
    mostrar_contactos()


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
        messagebox.showinfo("Borrador enviado a papelera", "El borrador se movió a la papelera.")
    mostrar_borradores()


def mover_mensaje_a_papelera(mensaje_id):
    eliminado = eliminar_mensaje(mensaje_id)
    if eliminado:
        messagebox.showinfo("Mensaje enviado a papelera", "El mensaje se movió a la papelera.")
    mostrar_mensajes_recibidos()


def restaurar_desde_papelera_y_refrescar(mensaje_id):
    restaurado = restaurar_desde_papelera(mensaje_id)
    if restaurado:
        messagebox.showinfo("Elemento restaurado", "El elemento volvió desde la papelera.")
    mostrar_papelera()


def borrar_definitivo_y_refrescar(mensaje_id):
    borrado = eliminar_definitivamente(mensaje_id)
    if borrado:
        messagebox.showinfo("Elemento eliminado", "El elemento se borró definitivamente.")
    mostrar_papelera()


def enviar_desde_ui():
    global frame_visible, borrador_actual_id

    destinatario = entry_dest.get().strip()
    asunto = entry_asunto.get().strip()
    contenido = textbox_contenido.get("1.0", "end").strip()

    if not destinatario or not asunto or not contenido:
        messagebox.showwarning("Campos vacíos", "Completa destinatario, asunto y mensaje.")
        return

    destinatario_info = obtener_usuario_por_correo(destinatario)
    if not destinatario_info:
        messagebox.showerror("Correo no encontrado", "El correo destinatario no existe.")
        return

    enviar_mensaje(int(usuario_id), destinatario_info["id"], asunto, contenido)
    if borrador_actual_id is not None:
        eliminar_definitivamente(borrador_actual_id)
    frame_redactar.place_forget()
    frame_visible = False
    borrar_estado_redactor()
    messagebox.showinfo("Mensaje enviado", "El mensaje se envió correctamente.")
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

frame_contactos = CTkFrame(
    Msj,
    fg_color="#202020",
    corner_radius=10,
    border_width=1,
    width=500,
    height=400,
)
frame_contactos.place_forget()
frame_contactos.pack_propagate(False)

titulo_contactos = CTkLabel(
    frame_contactos,
    text="Contactos",
    font=CTkFont(size=24, weight="bold"),
)
titulo_contactos.pack(pady=(12, 8))

lista_contactos = CTkScrollableFrame(
    frame_contactos,
    width=440,
    height=220,
    fg_color="transparent",
)
lista_contactos.pack(padx=20, pady=(0, 12), fill="both", expand=False)

seccion_agregar = CTkFrame(frame_contactos, fg_color="transparent")
seccion_agregar.pack(padx=20, pady=(0, 12), fill="x")

label_contacto_correo = CTkLabel(seccion_agregar, text="Agregar por correo:")
label_contacto_correo.pack(anchor="w")

entry_contacto_correo = CTkEntry(seccion_agregar, width=320)
entry_contacto_correo.pack(side="left", padx=(0, 8), pady=(6, 0))

boton_agregar_contacto = CTkButton(
    seccion_agregar,
    text="Agregar",
    width=90,
    command=agregar_contacto_desde_ui,
)
boton_agregar_contacto.pack(side="left", pady=(6, 0))

boton_cerrar_contactos = CTkButton(
    frame_contactos,
    text="Cerrar",
    fg_color="#5A5A5A",
    hover_color="#474747",
    command=cerrar_panel_contactos,
)
boton_cerrar_contactos.pack(pady=(0, 12))

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
Boton_Borrar.configure(command=mostrar_papelera)
Tooltip(Pilar, Boton_Borrar, "Papelera")

Contactos = CTkImage(
    light_image=Image.open("contactos.png"),
    dark_image=Image.open("contactos.png"),
    size=(70, 70),
)
Boton_Contactos = CTkButton(Pilar, text="", image=Contactos, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Contactos.place(x=10, y=300)
Boton_Contactos.configure(command=mostrar_contactos)
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
