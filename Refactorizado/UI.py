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
                prueba = ImageTk.PhotoImage(imagen.resize((1, 1)))
                del prueba
            except Exception:
                return None
            return CTkImage(light_image=imagen, dark_image=imagen, size=size)
        except Exception:
            return None
    return None

class AppCorreos(CTk):
    def __init__(self, usuario_id="", nombre_usuario="Usuario", correo_usuario=""):
        super().__init__()
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.correo_usuario = correo_usuario
        self.borrador_actual_id = None
        self.frame_visible = False

        self.geometry("1200x700+250+50")
        self.title(f"Panel de {self.nombre_usuario}")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.configurar_ui()
        self.mostrar_mensajes_recibidos()

    def configurar_ui(self):
        # Frame fila superior
        self.Fila = CTkFrame(self, fg_color="#2B2B2B", height=100, corner_radius=-1, border_width=-1)
        self.Fila.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
        self.Fila.grid_columnconfigure(0, weight=1)
        self.Fila.grid_columnconfigure(1, weight=0)

        # Frame lateral
        self.Pilar = CTkFrame(self, width=100, height=100, fg_color="#2B2B2B", corner_radius=-1, border_width=-1)
        self.Pilar.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Panel central mensajes
        self.Msj = CTkFrame(self, fg_color="white", corner_radius=-1, border_width=-1)
        self.Msj.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        self.Contenedor_Msj = CTkScrollableFrame(self.Msj, fg_color="transparent", border_width=0, corner_radius=0)
        self.Contenedor_Msj.pack(fill="both", expand=True)

        self.info_usuario = CTkLabel(
            self.Fila,
            text=f"Usuario: {self.nombre_usuario}    Correo: {self.correo_usuario}    ID: {self.usuario_id}",
            text_color="white",
            font=CTkFont(size=20, weight="bold"),
        )
        self.info_usuario.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.barra_superior_derecha = CTkFrame(self.Fila, fg_color="transparent")
        self.barra_superior_derecha.grid(row=0, column=1, padx=20, pady=12, sticky="e")

        self.menu_lateral = CTkFrame(self.Pilar, fg_color="transparent")
        self.menu_lateral.pack(fill="x", padx=6, pady=20)

        self.configurar_ventanas_secundarias()
        self.configurar_botones()

    def configurar_ventanas_secundarias(self):
        # ====== REDACTAR ======
        self.frame_redactar = CTkFrame(self.Msj, fg_color="#202020", corner_radius=10, border_width=1, width=500, height=400)
        self.frame_redactar.grid_propagate(False)
        self.frame_redactar.place_forget()

        CTkLabel(self.frame_redactar, text="Para (correo registrado en la app):").pack(pady=(10, 0))
        self.entry_dest = CTkEntry(self.frame_redactar, width=300)
        self.entry_dest.pack(pady=5)

        CTkLabel(self.frame_redactar, text="Asunto:").pack(pady=(10, 0))
        self.entry_asunto = CTkEntry(self.frame_redactar, width=300)
        self.entry_asunto.pack(pady=5)

        CTkLabel(self.frame_redactar, text="Mensaje:").pack(pady=(10, 0))
        self.textbox_contenido = CTkTextbox(self.frame_redactar, width=350, height=150)
        self.textbox_contenido.pack(pady=10)

        self.Enviar_Msj = CTkButton(self.frame_redactar, text="Enviar", fg_color="#1F6AA5", hover_color="#3B3B3B", corner_radius=5, width=10, height=20, command=self.enviar_desde_ui)
        self.Enviar_Msj.pack(pady=10)

        self.boton_guardar_borrador = CTkButton(self.frame_redactar, text="Guardar borrador", fg_color="#5A5A5A", hover_color="#474747", command=self.guardar_borrador_desde_ui)
        self.boton_guardar_borrador.pack(pady=(0, 10))

        # ====== CONTACTOS ======
        self.frame_contactos = CTkFrame(self.Msj, fg_color="#202020", corner_radius=10, border_width=1, width=500, height=400)
        self.frame_contactos.pack_propagate(False)
        self.frame_contactos.place_forget()

        CTkLabel(self.frame_contactos, text="Contactos", font=CTkFont(size=24, weight="bold")).pack(pady=(12, 8))
        self.lista_contactos = CTkScrollableFrame(self.frame_contactos, width=440, height=220, fg_color="transparent")
        self.lista_contactos.pack(padx=20, pady=(0, 12), fill="both", expand=False)
        
        seccion_agregar = CTkFrame(self.frame_contactos, fg_color="transparent")
        seccion_agregar.pack(padx=20, pady=(0, 12), fill="x")

        CTkLabel(seccion_agregar, text="Agregar por correo:").pack(anchor="w")
        self.entry_contacto_correo = CTkEntry(seccion_agregar, width=320)
        self.entry_contacto_correo.pack(side="left", padx=(0, 8), pady=(6, 0))

        CTkButton(seccion_agregar, text="Agregar", width=90, command=self.agregar_contacto_desde_ui).pack(side="left", pady=(6, 0))
        CTkButton(self.frame_contactos, text="Cerrar", fg_color="#5A5A5A", hover_color="#474747", command=self.cerrar_panel_contactos).pack(pady=(0, 12))

        # ====== CUENTA ======
        self.frame_cuenta = CTkFrame(self.Msj, fg_color="#202020", corner_radius=10, border_width=1, width=420, height=280)
        self.frame_cuenta.pack_propagate(False)
        self.frame_cuenta.place_forget()

        CTkLabel(self.frame_cuenta, text="Cuenta", font=CTkFont(size=24, weight="bold")).pack(pady=(20, 12))
        datos_cuenta = CTkLabel(self.frame_cuenta, text=f"Nombre: {self.nombre_usuario}\nCorreo: {self.correo_usuario}\nID: {self.usuario_id}", justify="left", text_color="white", font=CTkFont(size=16))
        datos_cuenta.pack(pady=(0, 24))

        CTkButton(self.frame_cuenta, text="Cerrar sesion", fg_color="#8B1E1E", hover_color="#6F1818", command=self.cerrar_sesion).pack(pady=(0, 10))
        CTkButton(self.frame_cuenta, text="Cerrar", fg_color="#5A5A5A", hover_color="#474747", command=self.cerrar_panel_cuenta).pack()

    def configurar_botones(self):
        Enviar = cargar_imagen("Lapiz.png", (30, 30))
        Borrador = cargar_imagen("borrador.webp", (70, 50))
        Recibido = cargar_imagen("recibido.png", (90, 70))
        Enviados = cargar_imagen("Enviado.png", (80, 60))
        Borrar = cargar_imagen("basura.png", (70, 70))
        Contactos = cargar_imagen("contactos.png", (70, 70))
        Cuenta = cargar_imagen("cuenta.png", (70, 70))

        # Botones Superiores
        btn = CTkButton(self.barra_superior_derecha, text="Redactar", image=Enviar, fg_color="#1F6AA5", hover_color="#18527E", corner_radius=8, width=120, height=36, text_color="white", command=self.toggle_redactar)
        btn.pack(side="left", padx=(0, 10))
        Tooltip(self.Fila, btn, "Redactar")

        btn = CTkButton(self.barra_superior_derecha, text="Cuenta", image=Cuenta, fg_color="#5A5A5A", hover_color="#474747", corner_radius=8, width=100, height=36, text_color="white", command=self.mostrar_cuenta)
        btn.pack(side="left")
        Tooltip(self.Fila, btn, "Cuenta")

        # Botones Laterales
        botones_laterales = [
            ("Borradores", Borrador, self.mostrar_borradores),
            ("Recibidos", Recibido, self.mostrar_mensajes_recibidos),
            ("Enviados", Enviados, self.mostrar_mensajes_enviados),
            ("Papelera", Borrar, self.mostrar_papelera),
            ("Contactos", Contactos, self.mostrar_contactos)
        ]

        for i, (text, img, cmd) in enumerate(botones_laterales):
            b = CTkButton(self.menu_lateral, text=text, image=img, fg_color="#3A3A3A", hover_color="#4A4A4A", corner_radius=8, width=88, height=42, text_color="white", command=cmd)
            b.pack(fill="x", pady=(0, 10))
            Tooltip(self.Pilar, b, text)

    # --- Utilidades y Helpers ---
    def limpiar_contenedor_mensajes(self):
        for widget in self.Contenedor_Msj.winfo_children():
            widget.destroy()

    def crear_tarjeta_mensaje(self, color="#3B3B3B"):
        tarjeta = CTkFrame(self.Contenedor_Msj, fg_color=color, corner_radius=10)
        tarjeta.pack(anchor="e", pady=5, padx=10, fill="x")
        return tarjeta

    def agregar_texto_tarjeta(self, tarjeta, texto):
        label = CTkLabel(tarjeta, text=texto, text_color="white", wraplength=420, justify="left")
        label.pack(padx=10, pady=(10, 6), anchor="w")

    def crear_acciones_tarjeta(self, tarjeta):
        acciones = CTkFrame(tarjeta, fg_color="transparent")
        acciones.pack(padx=10, pady=(0, 10), anchor="e")
        return acciones

    def mostrar_tarjeta_info(self, texto):
        tarjeta = self.crear_tarjeta_mensaje("#3B3B3B")
        self.agregar_texto_tarjeta(tarjeta, texto)

    # --- Paneles Vistas ---
    def cerrar_panel_contactos(self):
        self.frame_contactos.place_forget()
        
    def cerrar_panel_cuenta(self):
        self.frame_cuenta.place_forget()

    def mostrar_mensajes_recibidos(self):
        self.cerrar_panel_contactos()
        self.cerrar_panel_cuenta()
        self.limpiar_contenedor_mensajes()
        mensajes = obtener_mensajes_recibidos(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not mensajes:
            self.mostrar_tarjeta_info("No tienes mensajes recibidos.")
            return
        for mensaje_id, _, remitente, asunto, contenido, fecha, _ in mensajes:
            tarjeta = self.crear_tarjeta_mensaje("#3B3B3B")
            texto = f"De: {remitente}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            self.agregar_texto_tarjeta(tarjeta, texto)
            acciones = self.crear_acciones_tarjeta(tarjeta)
            CTkButton(acciones, text="Enviar a papelera", width=140, fg_color="#8B1E1E", hover_color="#6F1818", command=lambda mid=mensaje_id: self.mover_mensaje_a_papelera(mid)).pack(side="left")

    def mostrar_mensajes_enviados(self):
        self.cerrar_panel_contactos()
        self.cerrar_panel_cuenta()
        self.limpiar_contenedor_mensajes()
        mensajes = obtener_mensajes_enviados(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not mensajes:
            self.mostrar_tarjeta_info("No tienes mensajes enviados.")
            return
        for mensaje_id, _, destinatario, asunto, contenido, fecha, _ in mensajes:
            tarjeta = self.crear_tarjeta_mensaje("#24577A")
            texto = f"Para: {destinatario}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            self.agregar_texto_tarjeta(tarjeta, texto)
            acciones = self.crear_acciones_tarjeta(tarjeta)
            CTkButton(acciones, text="Enviar a papelera", width=140, fg_color="#8B1E1E", hover_color="#6F1818", command=lambda mid=mensaje_id: self.mover_enviado_a_papelera(mid)).pack(side="left")

    def mostrar_borradores(self):
        self.cerrar_panel_contactos()
        self.cerrar_panel_cuenta()
        self.limpiar_contenedor_mensajes()
        borradores = obtener_borradores(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not borradores:
            self.mostrar_tarjeta_info("No tienes borradores guardados.")
            return
        for borrador_id, asunto, contenido, fecha in borradores:
            tarjeta = self.crear_tarjeta_mensaje("#1F6AA5")
            texto = f"Asunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            self.agregar_texto_tarjeta(tarjeta, texto)
            acciones = self.crear_acciones_tarjeta(tarjeta)
            btn_editar = CTkButton(acciones, text="Editar", width=90, command=lambda bid=borrador_id: self.cargar_borrador_en_redactor(bid))
            btn_editar.pack(side="left", padx=(0, 8))
            btn_eliminar = CTkButton(acciones, text="Enviar a papelera", width=140, fg_color="#8B1E1E", hover_color="#6F1818", command=lambda bid=borrador_id: self.eliminar_borrador_y_refrescar(bid))
            btn_eliminar.pack(side="left")

    def mostrar_papelera(self):
        self.cerrar_panel_contactos()
        self.cerrar_panel_cuenta()
        self.limpiar_contenedor_mensajes()
        elementos = obtener_papelera(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not elementos:
            self.mostrar_tarjeta_info("La papelera esta vacia.")
            return
        for mensaje_id, tipo, remitente, asunto, contenido, fecha in elementos:
            color = "#5A5A5A" if tipo == "borrador" else "#4C3A3A"
            tarjeta = self.crear_tarjeta_mensaje(color)
            etiqueta_tipo = "Borrador" if tipo == "borrador" else "Mensaje"
            texto = f"{etiqueta_tipo} en papelera\nReferencia: {remitente}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            self.agregar_texto_tarjeta(tarjeta, texto)
            acciones = self.crear_acciones_tarjeta(tarjeta)
            btn_restaurar = CTkButton(acciones, text="Restaurar", width=100, command=lambda mid=mensaje_id: self.restaurar_desde_papelera_y_refrescar(mid))
            btn_restaurar.pack(side="left", padx=(0, 8))
            btn_borrar = CTkButton(acciones, text="Borrar definitivo", width=130, fg_color="#8B1E1E", hover_color="#6F1818", command=lambda mid=mensaje_id: self.borrar_definitivo_y_refrescar(mid))
            btn_borrar.pack(side="left")

    def mostrar_contactos(self):
        self.frame_redactar.place_forget()
        self.frame_visible = False
        self.cerrar_panel_cuenta()
        for widget in self.lista_contactos.winfo_children(): widget.destroy()
        self.frame_contactos.place(relx=0.5, rely=0.5, anchor="center")

        contactos = obtener_contactos(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not contactos:
            CTkLabel(self.lista_contactos, text="No tienes contactos agregados.\nPuedes agregar uno usando su correo.", justify="center").pack(pady=30)
            return

        for relacion_id, nombre, correo in contactos:
            tarjeta = CTkFrame(self.lista_contactos, fg_color="#2F2F2F", corner_radius=10)
            tarjeta.pack(fill="x", padx=10, pady=6)
            CTkLabel(tarjeta, text=f"{nombre or correo}\n{correo}", justify="left", text_color="white").pack(side="left", padx=12, pady=10)
            CTkButton(tarjeta, text="Quitar", width=90, fg_color="#8B1E1E", hover_color="#6F1818", command=lambda rid=relacion_id: self.quitar_contacto_y_refrescar(rid)).pack(side="right", padx=12, pady=10)

    def mostrar_cuenta(self):
        self.frame_redactar.place_forget()
        self.frame_visible = False
        self.cerrar_panel_contactos()
        self.frame_cuenta.place(relx=0.5, rely=0.5, anchor="center")

    # --- Acciones y Eventos ---
    def cargar_borrador_en_redactor(self, borrador_id):
        borrador = obtener_borrador_por_id(borrador_id)
        if not borrador:
            messagebox.showerror("Borrador no encontrado", "Ese borrador ya no existe.")
            self.mostrar_borradores()
            return
        _, asunto, contenido, _ = borrador
        self.borrar_estado_redactor()
        self.borrador_actual_id = borrador_id
        self.entry_asunto.insert(0, asunto or "")
        self.textbox_contenido.insert("1.0", contenido or "")
        self.Enviar_Msj.configure(text="Enviar borrador")
        self.boton_guardar_borrador.configure(text="Actualizar borrador")
        self.frame_redactar.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_visible = True

    def borrar_estado_redactor(self):
        self.borrador_actual_id = None
        self.entry_dest.delete(0, "end")
        self.entry_asunto.delete(0, "end")
        self.textbox_contenido.delete("1.0", "end")
        self.boton_guardar_borrador.configure(text="Guardar borrador")
        self.Enviar_Msj.configure(text="Enviar")

    def toggle_redactar(self):
        if not self.frame_visible:
            self.cerrar_panel_contactos()
            self.cerrar_panel_cuenta()
            self.borrar_estado_redactor()
            self.frame_redactar.place(relx=0.5, rely=0.5, anchor="center")
            self.frame_visible = True
            return
        self.frame_redactar.place_forget()
        self.frame_visible = False
        self.borrar_estado_redactor()
        self.mostrar_borradores()

    def enviar_desde_ui(self):
        destinatario = self.entry_dest.get().strip()
        asunto = self.entry_asunto.get().strip()
        contenido = self.textbox_contenido.get("1.0", "end").strip()
        if not destinatario or not asunto or not contenido:
            messagebox.showwarning("Campos vacios", "Completa destinatario, asunto y mensaje.")
            return

        destinatario_info = obtener_usuario_por_correo(destinatario)
        if not destinatario_info:
            messagebox.showerror("Correo no encontrado", "El destinatario debe estar registrado en esta misma aplicacion.")
            return

        enviar_mensaje(int(self.usuario_id), destinatario_info["id"], asunto, contenido)
        if self.borrador_actual_id is not None:
            eliminar_definitivamente(self.borrador_actual_id)

        self.frame_redactar.place_forget()
        self.frame_visible = False
        self.borrar_estado_redactor()
        messagebox.showinfo("Mensaje enviado", "El mensaje interno se guardo correctamente y quedo disponible en la aplicacion.")
        self.mostrar_mensajes_enviados()

    def guardar_borrador_desde_ui(self):
        asunto = self.entry_asunto.get().strip()
        contenido = self.textbox_contenido.get("1.0", "end").strip()
        if not asunto and not contenido:
            messagebox.showwarning("Sin contenido", "Escribe asunto o contenido para guardar el borrador.")
            return

        if self.borrador_actual_id is None:
            self.borrador_actual_id = guardar_borrador(int(self.usuario_id), asunto, contenido)
            messagebox.showinfo("Borrador guardado", "El borrador se guardo correctamente.")
        else:
            actualizar_borrador(self.borrador_actual_id, asunto, contenido)
            messagebox.showinfo("Borrador actualizado", "Los cambios del borrador se guardaron.")

        self.frame_redactar.place_forget()
        self.frame_visible = False
        self.borrar_estado_redactor()
        self.mostrar_borradores()

    def agregar_contacto_desde_ui(self):
        correo_contacto = self.entry_contacto_correo.get().strip()
        if not correo_contacto:
            messagebox.showwarning("Correo vacio", "Escribe el correo del contacto.")
            return
        exito, resultado = agregar_contacto_por_correo(int(self.usuario_id), correo_contacto)
        if not exito:
            messagebox.showerror("No se pudo agregar", resultado)
            return

        self.entry_contacto_correo.delete(0, "end")
        messagebox.showinfo("Contacto agregado", f"Se agrego a {resultado['nombre']} correctamente.")
        self.mostrar_contactos()

    def mover_mensaje_a_papelera(self, mensaje_id):
        if eliminar_mensaje(mensaje_id, int(self.usuario_id)):
            messagebox.showinfo("Mensaje enviado a papelera", "El mensaje se movio a la papelera.")
        self.mostrar_mensajes_recibidos()

    def mover_enviado_a_papelera(self, mensaje_id):
        if eliminar_mensaje(mensaje_id, int(self.usuario_id)):
            messagebox.showinfo("Enviado a papelera", "El mensaje enviado se movio a la papelera.")
        self.mostrar_mensajes_enviados()

    def eliminar_borrador_y_refrescar(self, borrador_id):
        if eliminar_borrador(borrador_id):
            messagebox.showinfo("Borrador enviado a papelera", "El borrador se movio a la papelera.")
        self.mostrar_borradores()

    def restaurar_desde_papelera_y_refrescar(self, mensaje_id):
        if restaurar_desde_papelera(mensaje_id, int(self.usuario_id)):
            messagebox.showinfo("Elemento restaurado", "El elemento volvio desde la papelera.")
        self.mostrar_papelera()

    def borrar_definitivo_y_refrescar(self, mensaje_id):
        if eliminar_definitivamente(mensaje_id, int(self.usuario_id)):
            messagebox.showinfo("Elemento eliminado", "El elemento se borro definitivamente.")
        self.mostrar_papelera()

    def quitar_contacto_y_refrescar(self, relacion_id):
        if eliminar_contacto(relacion_id):
            messagebox.showinfo("Contacto eliminado", "El contacto se quito de tu lista.")
        self.mostrar_contactos()

    def cerrar_sesion(self):
        confirmar = messagebox.askyesno("Cerrar sesion", "Quieres cerrar la sesion actual y volver al login?")
        if not confirmar:
            return
        limpiar_sesion()
        self.destroy()
        from login import ejecutar_login
        ejecutar_login()

def main(usuario_id="", nombre_usuario="Usuario", correo_usuario=""):
    app = AppCorreos(usuario_id, nombre_usuario, correo_usuario)
    app.mainloop()

if __name__ == "__main__":
    usuario_id = sys.argv[1] if len(sys.argv) > 1 else ""
    nombre_usuario = sys.argv[2] if len(sys.argv) > 2 else "Usuario"
    correo_usuario = sys.argv[3] if len(sys.argv) > 3 else ""
    main(usuario_id, nombre_usuario, correo_usuario)