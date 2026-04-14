import os
import sys

# Ajuste de ruta para poder importar modulos de la raiz principal 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tkinter import messagebox
from Clases import Tooltip
from app_utils import limpiar_sesion, resource_path
from bd import agregar_contacto_por_correo, eliminar_contacto, obtener_contactos, obtener_usuario_por_correo
from customtkinter import *
from PIL import Image, ImageTk

# Importar Funciones de BBDD Selectivamente
from ModulosClases.Funciones import (
    actualizar_borrador, eliminar_borrador, eliminar_definitivamente,
    eliminar_mensaje, enviar_mensaje, guardar_borrador, obtener_borrador_por_id,
    obtener_borradores, obtener_mensajes_enviados, obtener_mensajes_recibidos,
    obtener_papelera, restaurar_desde_papelera
)

# Importar nuestros nuevos Componentes UI
from ModulosClases.componentes import TarjetaMensaje, PanelRedactar, PanelContactos, PanelCuenta

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

        self.construir_layout()
        self.mostrar_mensajes_recibidos()

    def construir_layout(self):
        # Top Bar
        self.Fila = CTkFrame(self, fg_color="#2B2B2B", height=100, corner_radius=-1, border_width=-1)
        self.Fila.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)
        self.Fila.grid_columnconfigure(0, weight=1)
        self.Fila.grid_columnconfigure(1, weight=0)

        # Side Menu
        self.Pilar = CTkFrame(self, width=100, height=100, fg_color="#2B2B2B", corner_radius=-1, border_width=-1)
        self.Pilar.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # Main Content
        self.Msj = CTkFrame(self, fg_color="white", corner_radius=-1, border_width=-1)
        self.Msj.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        self.Contenedor_Msj = CTkScrollableFrame(self.Msj, fg_color="transparent", border_width=0, corner_radius=0)
        self.Contenedor_Msj.pack(fill="both", expand=True)

        self.info_usuario = CTkLabel(self.Fila, text=f"Usuario: {self.nombre_usuario}    Correo: {self.correo_usuario}    ID: {self.usuario_id}", text_color="white", font=CTkFont(size=20, weight="bold"))
        self.info_usuario.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.barra_superior_derecha = CTkFrame(self.Fila, fg_color="transparent")
        self.barra_superior_derecha.grid(row=0, column=1, padx=20, pady=12, sticky="e")

        self.menu_lateral = CTkFrame(self.Pilar, fg_color="transparent")
        self.menu_lateral.pack(fill="x", padx=6, pady=20)

        self.configurar_paneles()
        self.configurar_botones_navegacion()

    def configurar_paneles(self):
        # Instanciamos los modulos pasando sus funciones Callbacks
        self.panel_redactar = PanelRedactar(self.Msj, cb_enviar=self.enviar_desde_ui, cb_guardar=self.guardar_borrador_desde_ui)
        self.panel_redactar.place_forget()

        self.panel_contactos = PanelContactos(self.Msj, cb_agregar=self.agregar_contacto_desde_ui, cb_cerrar=self.cerrar_paneles)
        self.panel_contactos.place_forget()

        self.panel_cuenta = PanelCuenta(self.Msj, self.nombre_usuario, self.correo_usuario, self.usuario_id, cb_cerrar_sesion=self.cerrar_sesion, cb_cerrar=self.cerrar_paneles)
        self.panel_cuenta.place_forget()

    def configurar_botones_navegacion(self):
        Enviar, Borrador, Recibido = cargar_imagen("Lapiz.png", (30, 30)), cargar_imagen("borrador.webp", (70, 50)), cargar_imagen("recibido.png", (90, 70))
        Enviados, Borrar, Contactos = cargar_imagen("Enviado.png", (80, 60)), cargar_imagen("basura.png", (70, 70)), cargar_imagen("contactos.png", (70, 70))
        Cuenta = cargar_imagen("cuenta.png", (70, 70))

        btn_redactar = CTkButton(self.barra_superior_derecha, text="Redactar", image=Enviar, fg_color="#1F6AA5", width=120, height=36, command=self.toggle_redactar)
        btn_redactar.pack(side="left", padx=(0, 10))

        btn_cuenta = CTkButton(self.barra_superior_derecha, text="Cuenta", image=Cuenta, fg_color="#5A5A5A", width=100, height=36, command=self.mostrar_cuenta)
        btn_cuenta.pack(side="left")

        botones_laterales = [
            ("Borradores", Borrador, self.mostrar_borradores),
            ("Recibidos", Recibido, self.mostrar_mensajes_recibidos),
            ("Enviados", Enviados, self.mostrar_mensajes_enviados),
            ("Papelera", Borrar, self.mostrar_papelera),
            ("Contactos", Contactos, self.mostrar_contactos)
        ]

        for text, img, cmd in botones_laterales:
            b = CTkButton(self.menu_lateral, text=text, image=img, fg_color="#3A3A3A", width=88, height=42, command=cmd)
            b.pack(fill="x", pady=(0, 10))

    # --- Utilidades Nav ---
    def limpiar_contenedor_mensajes(self):
        for widget in self.Contenedor_Msj.winfo_children(): widget.destroy()

    def cerrar_paneles(self):
        self.panel_contactos.place_forget()
        self.panel_cuenta.place_forget()
        self.panel_redactar.place_forget()
        self.frame_visible = False

    # --- Mostrar Vistas ---
    def mostrar_mensajes_recibidos(self):
        self.cerrar_paneles()
        self.limpiar_contenedor_mensajes()
        mensajes = obtener_mensajes_recibidos(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not mensajes:
            return TarjetaMensaje(self.Contenedor_Msj, "#3B3B3B", "No tienes mensajes recibidos.")
        
        for mensaje_id, _, remitente, asunto, contenido, fecha, _ in mensajes:
            texto = f"De: {remitente}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            tarjeta = TarjetaMensaje(self.Contenedor_Msj, "#3B3B3B", texto)
            tarjeta.agregar_boton("Enviar a papelera", "#8B1E1E", "#6F1818", lambda mid=mensaje_id: self.mover_mensaje_a_papelera(mid))

    def mostrar_mensajes_enviados(self):
        self.cerrar_paneles()
        self.limpiar_contenedor_mensajes()
        mensajes = obtener_mensajes_enviados(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not mensajes:
            return TarjetaMensaje(self.Contenedor_Msj, "#3B3B3B", "No tienes mensajes enviados.")

        for mensaje_id, _, destinatario, asunto, contenido, fecha, _ in mensajes:
            texto = f"Para: {destinatario}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            tarjeta = TarjetaMensaje(self.Contenedor_Msj, "#24577A", texto)
            tarjeta.agregar_boton("Enviar a papelera", "#8B1E1E", "#6F1818", lambda mid=mensaje_id: self.mover_enviado_a_papelera(mid))

    def mostrar_borradores(self):
        self.cerrar_paneles()
        self.limpiar_contenedor_mensajes()
        borradores = obtener_borradores(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not borradores:
            return TarjetaMensaje(self.Contenedor_Msj, "#3B3B3B", "No tienes borradores guardados.")

        for borrador_id, asunto, contenido, fecha in borradores:
            texto = f"Asunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            tarjeta = TarjetaMensaje(self.Contenedor_Msj, "#1F6AA5", texto)
            tarjeta.agregar_boton("Editar", "#1F6AA5", "#18527E", lambda bid=borrador_id: self.cargar_borrador_en_redactor(bid))
            tarjeta.agregar_boton("Enviar a papelera", "#8B1E1E", "#6F1818", lambda bid=borrador_id: self.eliminar_borrador_y_refrescar(bid))

    def mostrar_papelera(self):
        self.cerrar_paneles()
        self.limpiar_contenedor_mensajes()
        elementos = obtener_papelera(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not elementos:
            return TarjetaMensaje(self.Contenedor_Msj, "#3B3B3B", "La papelera esta vacia.")

        for mensaje_id, tipo, remitente, asunto, contenido, fecha in elementos:
            color = "#5A5A5A" if tipo == "borrador" else "#4C3A3A"
            etiqueta = "Borrador" if tipo == "borrador" else "Mensaje"
            texto = f"{etiqueta} en papelera\nReferencia: {remitente}\nAsunto: {asunto or '(sin asunto)'}\n\n{contenido or '(vacio)'}\n\n{fecha}"
            
            tarjeta = TarjetaMensaje(self.Contenedor_Msj, color, texto)
            tarjeta.agregar_boton("Restaurar", "#5A5A5A", "#474747", lambda mid=mensaje_id: self.restaurar_desde_papelera_y_refrescar(mid))
            tarjeta.agregar_boton("Borrar definitivo", "#8B1E1E", "#6F1818", lambda mid=mensaje_id: self.borrar_definitivo_y_refrescar(mid))

    def mostrar_contactos(self):
        self.cerrar_paneles()
        self.panel_contactos.limpiar_lista()
        self.panel_contactos.place(relx=0.5, rely=0.5, anchor="center")

        contactos = obtener_contactos(int(self.usuario_id)) if str(self.usuario_id).isdigit() else []
        if not contactos:
            CTkLabel(self.panel_contactos.lista_contactos, text="No tienes contactos agregados.").pack(pady=30)
            return

        for relacion_id, nombre, correo in contactos:
            tarjeta = CTkFrame(self.panel_contactos.lista_contactos, fg_color="#2F2F2F", corner_radius=10)
            tarjeta.pack(fill="x", padx=10, pady=6)
            CTkLabel(tarjeta, text=f"{nombre or correo}\n{correo}", justify="left", text_color="white").pack(side="left", padx=12, pady=10)
            CTkButton(tarjeta, text="Quitar", width=90, fg_color="#8B1E1E", hover_color="#6F1818", command=lambda rid=relacion_id: self.quitar_contacto_y_refrescar(rid)).pack(side="right", padx=12, pady=10)

    def mostrar_cuenta(self):
        self.cerrar_paneles()
        self.panel_cuenta.place(relx=0.5, rely=0.5, anchor="center")

    # --- Acciones Lógicas ---
    def toggle_redactar(self):
        if not self.frame_visible:
            self.cerrar_paneles()
            self.borrador_actual_id = None
            self.panel_redactar.limpiar()
            self.panel_redactar.modo_edicion(False)
            self.panel_redactar.place(relx=0.5, rely=0.5, anchor="center")
            self.frame_visible = True
        else:
            self.cerrar_paneles()
            self.mostrar_borradores()

    def enviar_desde_ui(self):
        destinatario, asunto, contenido = self.panel_redactar.obtener_datos()
        if not destinatario or not asunto or not contenido:
            messagebox.showwarning("Campos vacios", "Completa destinatario, asunto y mensaje.")
            return

        destinatario_info = obtener_usuario_por_correo(destinatario)
        if not destinatario_info:
            messagebox.showerror("Error", "Destinatario no registrado en la app.")
            return

        enviar_mensaje(int(self.usuario_id), destinatario_info["id"], asunto, contenido)
        if self.borrador_actual_id: eliminar_definitivamente(self.borrador_actual_id)
        
        self.cerrar_paneles()
        messagebox.showinfo("Exito", "Mensaje enviado exitosamente.")
        self.mostrar_mensajes_enviados()

    def guardar_borrador_desde_ui(self):
        destinatario, asunto, contenido = self.panel_redactar.obtener_datos()
        if not asunto and not contenido:
            messagebox.showwarning("Error", "Escribe asunto o contenido para el borrador.")
            return

        if self.borrador_actual_id is None:
            self.borrador_actual_id = guardar_borrador(int(self.usuario_id), asunto, contenido)
        else:
            actualizar_borrador(self.borrador_actual_id, asunto, contenido)

        self.cerrar_paneles()
        messagebox.showinfo("Borrador guardado", "Guardado exitosamente.")
        self.mostrar_borradores()

    def cargar_borrador_en_redactor(self, borrador_id):
        borrador = obtener_borrador_por_id(borrador_id)
        if not borrador: return

        _, asunto, contenido, _ = borrador
        self.borrador_actual_id = borrador_id
        
        self.cerrar_paneles()
        self.panel_redactar.set_datos(asunto or "", contenido or "")
        self.panel_redactar.modo_edicion(True)
        self.panel_redactar.place(relx=0.5, rely=0.5, anchor="center")
        self.frame_visible = True

    def agregar_contacto_desde_ui(self):
        correo = self.panel_contactos.obtener_correo()
        exito, resultado = agregar_contacto_por_correo(int(self.usuario_id), correo)
        if not exito:
            messagebox.showerror("Error", resultado)
            return

        self.panel_contactos.limpiar_correo()
        messagebox.showinfo("Agregado", "Contacto agregado!")
        self.mostrar_contactos()

    def mover_mensaje_a_papelera(self, mid):
        eliminar_mensaje(mid, int(self.usuario_id))
        self.mostrar_mensajes_recibidos()

    def mover_enviado_a_papelera(self, mid):
        eliminar_mensaje(mid, int(self.usuario_id))
        self.mostrar_mensajes_enviados()

    def eliminar_borrador_y_refrescar(self, bid):
        eliminar_borrador(bid)
        self.mostrar_borradores()

    def restaurar_desde_papelera_y_refrescar(self, mid):
        restaurar_desde_papelera(mid, int(self.usuario_id))
        self.mostrar_papelera()

    def borrar_definitivo_y_refrescar(self, mid):
        eliminar_definitivamente(mid, int(self.usuario_id))
        self.mostrar_papelera()

    def quitar_contacto_y_refrescar(self, rid):
        eliminar_contacto(rid)
        self.mostrar_contactos()

    def cerrar_sesion(self):
        if not messagebox.askyesno("Salir", "¿Quieres cerrar la sesion actual?"): return
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