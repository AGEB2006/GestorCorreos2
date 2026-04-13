import os
import sys
from tkinter import messagebox

from Clases import Tooltip
from Funciones import (
    actualizar_borrador,
    eliminar_borrador,
    eliminar_definitivamente,
    eliminar_mensaje,
    enviar_mensaje,
    guardar_borrador,
    obtener_borrador_por_id,
    obtener_borradores,
    obtener_mensajes_enviados,
    obtener_mensajes_recibidos,
    obtener_papelera,
    restaurar_desde_papelera,
)
from app_utils import limpiar_sesion, resource_path
from bd import agregar_contacto_por_correo, eliminar_contacto, obtener_contactos, obtener_usuario_por_correo
from customtkinter import *
from PIL import Image, ImageTk


def cargar_imagen(nombre_archivo, size):
    ruta = resource_path(nombre_archivo)
    if os.path.exists(ruta):
        try:
            imagen = Image.open(ruta)
            try:
                # Validate that ImageTk support is actually available in runtime.
                prueba = ImageTk.PhotoImage(imagen.resize((1, 1)))
                del prueba
            except Exception:
                return None

            return CTkImage(light_image=imagen, dark_image=imagen, size=size)
        except Exception:
            return None
    return None


def main(usuario_id="", nombre_usuario="Usuario", correo_usuario=""):
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

    barra_superior_derecha = CTkFrame(Fila, fg_color="transparent")
    barra_superior_derecha.grid(row=0, column=1, padx=20, pady=12, sticky="e")

    menu_lateral = CTkFrame(Pilar, fg_color="transparent")
    menu_lateral.pack(fill="x", padx=6, pady=20)

    borrador_actual_id = None
    frame_visible = False

    def limpiar_contenedor_mensajes():
        for widget in Contenedor_Msj.winfo_children():
            widget.destroy()

    def crear_tarjeta_mensaje(color="#3B3B3B"):
        tarjeta = CTkFrame(Contenedor_Msj, fg_color=color, corner_radius=10)
        tarjeta.pack(anchor="e", pady=5, padx=10, fill="x")
        return tarjeta

    def agregar_texto_tarjeta(tarjeta, texto):
        label = CTkLabel(tarjeta, text=texto, text_color="white", wraplength=420, justify="left")
        label.pack(padx=10, pady=(10, 6), anchor="w")

    def crear_acciones_tarjeta(tarjeta):
        acciones = CTkFrame(tarjeta, fg_color="transparent")
        acciones.pack(padx=10, pady=(0, 10), anchor="e")
        return acciones

    def mostrar_tarjeta_info(texto):
        tarjeta = crear_tarjeta_mensaje("#3B3B3B")
        agregar_texto_tarjeta(tarjeta, texto)

    def limpiar_panel_contactos():
        for widget in lista_contactos.winfo_children():
            widget.destroy()

    def cerrar_panel_contactos():
        frame_contactos.place_forget()

    def cerrar_panel_cuenta():
        frame_cuenta.place_forget()

    def mostrar_mensajes_recibidos():
        cerrar_panel_contactos()
        cerrar_panel_cuenta()
        limpiar_contenedor_mensajes()
        mensajes = obtener_mensajes_recibidos(int(usuario_id)) if str(usuario_id).isdigit() else []

        if not mensajes:
            mostrar_tarjeta_info("No tienes mensajes recibidos.")
            return

        for mensaje_id, _, remitente, asunto, contenido, fecha, _ in mensajes:
            tarjeta = crear_tarjeta_mensaje("#3B3B3B")
            texto = f"De: {remitente}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
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

    def mostrar_mensajes_enviados():
        cerrar_panel_contactos()
        cerrar_panel_cuenta()
        limpiar_contenedor_mensajes()
        mensajes = obtener_mensajes_enviados(int(usuario_id)) if str(usuario_id).isdigit() else []

        if not mensajes:
            mostrar_tarjeta_info("No tienes mensajes enviados.")
            return

        for mensaje_id, _, destinatario, asunto, contenido, fecha, _ in mensajes:
            tarjeta = crear_tarjeta_mensaje("#24577A")
            texto = f"Para: {destinatario}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            agregar_texto_tarjeta(tarjeta, texto)
            acciones = crear_acciones_tarjeta(tarjeta)

            btn_eliminar = CTkButton(
                acciones,
                text="Enviar a papelera",
                width=140,
                fg_color="#8B1E1E",
                hover_color="#6F1818",
                command=lambda mid=mensaje_id: mover_enviado_a_papelera(mid),
            )
            btn_eliminar.pack(side="left")

    def mostrar_borradores():
        cerrar_panel_contactos()
        cerrar_panel_cuenta()
        limpiar_contenedor_mensajes()
        borradores = obtener_borradores(int(usuario_id)) if str(usuario_id).isdigit() else []

        if not borradores:
            mostrar_tarjeta_info("No tienes borradores guardados.")
            return

        for borrador_id, asunto, contenido, fecha in borradores:
            tarjeta = crear_tarjeta_mensaje("#1F6AA5")
            texto = f"Asunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            agregar_texto_tarjeta(tarjeta, texto)
            acciones = crear_acciones_tarjeta(tarjeta)

            btn_editar = CTkButton(acciones, text="Editar", width=90, command=lambda bid=borrador_id: cargar_borrador_en_redactor(bid))
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
        cerrar_panel_contactos()
        cerrar_panel_cuenta()
        limpiar_contenedor_mensajes()
        elementos = obtener_papelera(int(usuario_id)) if str(usuario_id).isdigit() else []

        if not elementos:
            mostrar_tarjeta_info("La papelera esta vacia.")
            return

        for mensaje_id, tipo, remitente, asunto, contenido, fecha in elementos:
            color = "#5A5A5A" if tipo == "borrador" else "#4C3A3A"
            tarjeta = crear_tarjeta_mensaje(color)
            etiqueta_tipo = "Borrador" if tipo == "borrador" else "Mensaje"
            texto = (
                f"{etiqueta_tipo} en papelera\n"
                f"Referencia: {remitente}\n"
                f"Asunto: {asunto or '(sin asunto)'}\n\n"
                f"{contenido or '(vacio)'}\n\n{fecha}"
            )
            agregar_texto_tarjeta(tarjeta, texto)
            acciones = crear_acciones_tarjeta(tarjeta)

            btn_restaurar = CTkButton(acciones, text="Restaurar", width=100, command=lambda mid=mensaje_id: restaurar_desde_papelera_y_refrescar(mid))
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

    def preparar_redactor(titulo_boton="Enviar"):
        boton_guardar_borrador.configure(text="Guardar borrador")
        Enviar_Msj.configure(text=titulo_boton)

    def cargar_borrador_en_redactor(borrador_id):
        nonlocal frame_visible, borrador_actual_id

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
        nonlocal borrador_actual_id
        borrador_actual_id = None
        limpiar_redactor()
        preparar_redactor()

    def guardar_borrador_desde_ui():
        nonlocal borrador_actual_id, frame_visible
        asunto = entry_asunto.get().strip()
        contenido = textbox_contenido.get("1.0", "end").strip()

        if not asunto and not contenido:
            messagebox.showwarning("Sin contenido", "Escribe asunto o contenido para guardar el borrador.")
            return

        if borrador_actual_id is None:
            borrador_actual_id = guardar_borrador(int(usuario_id), asunto, contenido)
            messagebox.showinfo("Borrador guardado", "El borrador se guardo correctamente.")
        else:
            actualizar_borrador(borrador_actual_id, asunto, contenido)
            messagebox.showinfo("Borrador actualizado", "Los cambios del borrador se guardaron.")

        frame_redactar.place_forget()
        frame_visible = False
        borrar_estado_redactor()
        mostrar_borradores()

    def eliminar_borrador_y_refrescar(borrador_id):
        if eliminar_borrador(borrador_id):
            messagebox.showinfo("Borrador enviado a papelera", "El borrador se movio a la papelera.")
        mostrar_borradores()

    def mover_mensaje_a_papelera(mensaje_id):
        if eliminar_mensaje(mensaje_id, int(usuario_id)):
            messagebox.showinfo("Mensaje enviado a papelera", "El mensaje se movio a la papelera.")
        mostrar_mensajes_recibidos()

    def mover_enviado_a_papelera(mensaje_id):
        if eliminar_mensaje(mensaje_id, int(usuario_id)):
            messagebox.showinfo("Enviado a papelera", "El mensaje enviado se movio a la papelera.")
        mostrar_mensajes_enviados()

    def restaurar_desde_papelera_y_refrescar(mensaje_id):
        if restaurar_desde_papelera(mensaje_id, int(usuario_id)):
            messagebox.showinfo("Elemento restaurado", "El elemento volvio desde la papelera.")
        mostrar_papelera()

    def borrar_definitivo_y_refrescar(mensaje_id):
        if eliminar_definitivamente(mensaje_id, int(usuario_id)):
            messagebox.showinfo("Elemento eliminado", "El elemento se borro definitivamente.")
        mostrar_papelera()

    def mostrar_contactos():
        nonlocal frame_visible
        frame_redactar.place_forget()
        frame_visible = False
        cerrar_panel_cuenta()
        limpiar_panel_contactos()
        frame_contactos.place(relx=0.5, rely=0.5, anchor="center")

        contactos = obtener_contactos(int(usuario_id)) if str(usuario_id).isdigit() else []
        if not contactos:
            aviso = CTkLabel(lista_contactos, text="No tienes contactos agregados.\nPuedes agregar uno usando su correo.", justify="center")
            aviso.pack(pady=30)
            return

        for relacion_id, nombre, correo in contactos:
            tarjeta = CTkFrame(lista_contactos, fg_color="#2F2F2F", corner_radius=10)
            tarjeta.pack(fill="x", padx=10, pady=6)

            texto = CTkLabel(tarjeta, text=f"{nombre or correo}\n{correo}", justify="left", text_color="white")
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
            messagebox.showwarning("Correo vacio", "Escribe el correo del contacto.")
            return

        exito, resultado = agregar_contacto_por_correo(int(usuario_id), correo_contacto)
        if not exito:
            messagebox.showerror("No se pudo agregar", resultado)
            return

        entry_contacto_correo.delete(0, "end")
        messagebox.showinfo("Contacto agregado", f"Se agrego a {resultado['nombre']} correctamente.")
        mostrar_contactos()

    def quitar_contacto_y_refrescar(relacion_id):
        if eliminar_contacto(relacion_id):
            messagebox.showinfo("Contacto eliminado", "El contacto se quito de tu lista.")
        mostrar_contactos()

    def cerrar_sesion():
        confirmar = messagebox.askyesno("Cerrar sesion", "Quieres cerrar la sesion actual y volver al login?")
        if not confirmar:
            return

        limpiar_sesion()
        Ventana.destroy()
        from login import ejecutar_login

        ejecutar_login()

    def mostrar_cuenta():
        nonlocal frame_visible
        frame_redactar.place_forget()
        frame_visible = False
        cerrar_panel_contactos()
        frame_cuenta.place(relx=0.5, rely=0.5, anchor="center")

    def enviar_desde_ui():
        nonlocal frame_visible, borrador_actual_id
        destinatario = entry_dest.get().strip()
        asunto = entry_asunto.get().strip()
        contenido = textbox_contenido.get("1.0", "end").strip()

        if not destinatario or not asunto or not contenido:
            messagebox.showwarning("Campos vacios", "Completa destinatario, asunto y mensaje.")
            return

        destinatario_info = obtener_usuario_por_correo(destinatario)
        if not destinatario_info:
            messagebox.showerror(
                "Correo no encontrado",
                "El destinatario debe estar registrado en esta misma aplicacion.",
            )
            return

        enviar_mensaje(int(usuario_id), destinatario_info["id"], asunto, contenido)
        if borrador_actual_id is not None:
            eliminar_definitivamente(borrador_actual_id)

        frame_redactar.place_forget()
        frame_visible = False
        borrar_estado_redactor()
        messagebox.showinfo(
            "Mensaje enviado",
            "El mensaje interno se guardo correctamente y quedo disponible en la aplicacion.",
        )
        mostrar_mensajes_enviados()

    def toggle_redactar():
        nonlocal frame_visible
        if not frame_visible:
            cerrar_panel_contactos()
            cerrar_panel_cuenta()
            borrar_estado_redactor()
            frame_redactar.place(relx=0.5, rely=0.5, anchor="center")
            frame_visible = True
            return

        frame_redactar.place_forget()
        frame_visible = False
        borrar_estado_redactor()
        mostrar_borradores()

    Enviar = cargar_imagen("Lapiz.png", (30, 30))
    Borrador = cargar_imagen("borrador.webp", (70, 50))
    Recibido = cargar_imagen("recibido.png", (90, 70))
    Enviados = cargar_imagen("Enviado.png", (80, 60))
    Borrar = cargar_imagen("basura.png", (70, 70))
    Contactos = cargar_imagen("contactos.png", (70, 70))
    Cuenta = cargar_imagen("cuenta.png", (70, 70))

    frame_redactar = CTkFrame(Msj, fg_color="#202020", corner_radius=10, border_width=1, width=500, height=400)
    frame_redactar.place_forget()
    frame_redactar.grid_propagate(False)

    label_dest = CTkLabel(frame_redactar, text="Para (correo registrado en la app):")
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

    Enviar_Msj = CTkButton(frame_redactar, text="Enviar", fg_color="#1F6AA5", hover_color="#3B3B3B", corner_radius=5, width=10, height=20, command=enviar_desde_ui)
    Enviar_Msj.pack(pady=10)

    boton_guardar_borrador = CTkButton(frame_redactar, text="Guardar borrador", fg_color="#5A5A5A", hover_color="#474747", command=guardar_borrador_desde_ui)
    boton_guardar_borrador.pack(pady=(0, 10))

    frame_contactos = CTkFrame(Msj, fg_color="#202020", corner_radius=10, border_width=1, width=500, height=400)
    frame_contactos.place_forget()
    frame_contactos.pack_propagate(False)

    titulo_contactos = CTkLabel(frame_contactos, text="Contactos", font=CTkFont(size=24, weight="bold"))
    titulo_contactos.pack(pady=(12, 8))

    lista_contactos = CTkScrollableFrame(frame_contactos, width=440, height=220, fg_color="transparent")
    lista_contactos.pack(padx=20, pady=(0, 12), fill="both", expand=False)

    seccion_agregar = CTkFrame(frame_contactos, fg_color="transparent")
    seccion_agregar.pack(padx=20, pady=(0, 12), fill="x")

    label_contacto_correo = CTkLabel(seccion_agregar, text="Agregar por correo:")
    label_contacto_correo.pack(anchor="w")
    entry_contacto_correo = CTkEntry(seccion_agregar, width=320)
    entry_contacto_correo.pack(side="left", padx=(0, 8), pady=(6, 0))

    boton_agregar_contacto = CTkButton(seccion_agregar, text="Agregar", width=90, command=agregar_contacto_desde_ui)
    boton_agregar_contacto.pack(side="left", pady=(6, 0))

    boton_cerrar_contactos = CTkButton(frame_contactos, text="Cerrar", fg_color="#5A5A5A", hover_color="#474747", command=cerrar_panel_contactos)
    boton_cerrar_contactos.pack(pady=(0, 12))

    frame_cuenta = CTkFrame(Msj, fg_color="#202020", corner_radius=10, border_width=1, width=420, height=280)
    frame_cuenta.place_forget()
    frame_cuenta.pack_propagate(False)

    titulo_cuenta = CTkLabel(frame_cuenta, text="Cuenta", font=CTkFont(size=24, weight="bold"))
    titulo_cuenta.pack(pady=(20, 12))

    datos_cuenta = CTkLabel(frame_cuenta, text=f"Nombre: {nombre_usuario}\nCorreo: {correo_usuario}\nID: {usuario_id}", justify="left", text_color="white", font=CTkFont(size=16))
    datos_cuenta.pack(pady=(0, 24))

    boton_cerrar_sesion = CTkButton(frame_cuenta, text="Cerrar sesion", fg_color="#8B1E1E", hover_color="#6F1818", command=cerrar_sesion)
    boton_cerrar_sesion.pack(pady=(0, 10))

    boton_cerrar_cuenta = CTkButton(frame_cuenta, text="Cerrar", fg_color="#5A5A5A", hover_color="#474747", command=cerrar_panel_cuenta)
    boton_cerrar_cuenta.pack()

    Boton_Enviar = CTkButton(
        barra_superior_derecha,
        text="Redactar",
        image=Enviar,
        fg_color="#1F6AA5",
        hover_color="#18527E",
        corner_radius=8,
        width=120,
        height=36,
        text_color="white",
    )
    Boton_Enviar.pack(side="left", padx=(0, 10))
    Boton_Enviar.configure(command=toggle_redactar)
    Tooltip(Fila, Boton_Enviar, "Redactar")

    Boton_Borrador = CTkButton(
        menu_lateral,
        text="Borradores",
        image=Borrador,
        fg_color="#3A3A3A",
        hover_color="#4A4A4A",
        corner_radius=8,
        width=88,
        height=42,
        text_color="white",
    )
    Boton_Borrador.pack(fill="x", pady=(0, 10))
    Boton_Borrador.configure(command=mostrar_borradores)
    Tooltip(Pilar, Boton_Borrador, "Borradores")

    Boton_Recibido = CTkButton(
        menu_lateral,
        text="Recibidos",
        image=Recibido,
        fg_color="#3A3A3A",
        hover_color="#4A4A4A",
        corner_radius=8,
        width=88,
        height=42,
        text_color="white",
    )
    Boton_Recibido.pack(fill="x", pady=(0, 10))
    Boton_Recibido.configure(command=mostrar_mensajes_recibidos)
    Tooltip(Pilar, Boton_Recibido, "Recibido")

    Boton_Enviados = CTkButton(
        menu_lateral,
        text="Enviados",
        image=Enviados,
        fg_color="#3A3A3A",
        hover_color="#4A4A4A",
        corner_radius=8,
        width=88,
        height=42,
        text_color="white",
        command=mostrar_mensajes_enviados,
    )
    Boton_Enviados.pack(fill="x", pady=(0, 10))
    Tooltip(Pilar, Boton_Enviados, "Enviados")

    Boton_Borrar = CTkButton(
        menu_lateral,
        text="Papelera",
        image=Borrar,
        fg_color="#3A3A3A",
        hover_color="#4A4A4A",
        corner_radius=8,
        width=88,
        height=42,
        text_color="white",
    )
    Boton_Borrar.pack(fill="x", pady=(0, 10))
    Boton_Borrar.configure(command=mostrar_papelera)
    Tooltip(Pilar, Boton_Borrar, "Papelera")

    Boton_Contactos = CTkButton(
        menu_lateral,
        text="Contactos",
        image=Contactos,
        fg_color="#3A3A3A",
        hover_color="#4A4A4A",
        corner_radius=8,
        width=88,
        height=42,
        text_color="white",
    )
    Boton_Contactos.pack(fill="x", pady=(0, 10))
    Boton_Contactos.configure(command=mostrar_contactos)
    Tooltip(Pilar, Boton_Contactos, "Contactos")

    Boton_Cuenta = CTkButton(
        barra_superior_derecha,
        text="Cuenta",
        image=Cuenta,
        fg_color="#5A5A5A",
        hover_color="#474747",
        corner_radius=8,
        width=100,
        height=36,
        text_color="white",
    )
    Boton_Cuenta.pack(side="left")
    Boton_Cuenta.configure(command=mostrar_cuenta)
    Tooltip(Fila, Boton_Cuenta, "Cuenta")

    mostrar_mensajes_recibidos()
    Ventana.mainloop()


if __name__ == "__main__":
    usuario_id = sys.argv[1] if len(sys.argv) > 1 else ""
    nombre_usuario = sys.argv[2] if len(sys.argv) > 2 else "Usuario"
    correo_usuario = sys.argv[3] if len(sys.argv) > 3 else ""
    main(usuario_id, nombre_usuario, correo_usuario)
#actualizacion
