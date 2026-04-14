import os
import sys

# Agregamos la ruta principal para que pueda importar módulos como 'bd', 'app_utils' y 'Clases'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from customtkinter import *

class TarjetaMensaje(CTkFrame):
    def __init__(self, master, color, texto):
        super().__init__(master, fg_color=color, corner_radius=10)
        self.pack(anchor="e", pady=5, padx=10, fill="x")
        
        self.label = CTkLabel(self, text=texto, text_color="white", wraplength=420, justify="left")
        self.label.pack(padx=10, pady=(10, 6), anchor="w")
        
        self.acciones = CTkFrame(self, fg_color="transparent")
        self.acciones.pack(padx=10, pady=(0, 10), anchor="e")

    def agregar_boton(self, texto, color, hover, comando):
        btn = CTkButton(self.acciones, text=texto, width=140, fg_color=color, hover_color=hover, command=comando)
        btn.pack(side="left", padx=(0, 8))
        return btn

class PanelRedactar(CTkFrame):
    def __init__(self, master, cb_enviar, cb_guardar):
        super().__init__(master, fg_color="#202020", corner_radius=10, border_width=1, width=500, height=400)
        self.grid_propagate(False)
        self.cb_enviar = cb_enviar
        self.cb_guardar = cb_guardar
        
        CTkLabel(self, text="Para (correo registrado en la app):").pack(pady=(10, 0))
        self.entry_dest = CTkEntry(self, width=300)
        self.entry_dest.pack(pady=5)
        
        CTkLabel(self, text="Asunto:").pack(pady=(10, 0))
        self.entry_asunto = CTkEntry(self, width=300)
        self.entry_asunto.pack(pady=5)
        
        CTkLabel(self, text="Mensaje:").pack(pady=(10, 0))
        self.textbox_contenido = CTkTextbox(self, width=350, height=150)
        self.textbox_contenido.pack(pady=10)
        
        self.btn_enviar = CTkButton(self, text="Enviar", fg_color="#1F6AA5", hover_color="#3B3B3B", corner_radius=5, width=10, height=20, command=self.cb_enviar)
        self.btn_enviar.pack(pady=10)
        
        self.btn_guardar = CTkButton(self, text="Guardar borrador", fg_color="#5A5A5A", hover_color="#474747", command=self.cb_guardar)
        self.btn_guardar.pack(pady=(0, 10))

    def obtener_datos(self):
        return self.entry_dest.get().strip(), self.entry_asunto.get().strip(), self.textbox_contenido.get("1.0", "end").strip()

    def set_datos(self, asunto, contenido):
        self.limpiar()
        self.entry_asunto.insert(0, asunto)
        self.textbox_contenido.insert("1.0", contenido)

    def limpiar(self):
        self.entry_dest.delete(0, "end")
        self.entry_asunto.delete(0, "end")
        self.textbox_contenido.delete("1.0", "end")

    def modo_edicion(self, en_edicion=True):
        if en_edicion:
            self.btn_enviar.configure(text="Enviar borrador")
            self.btn_guardar.configure(text="Actualizar borrador")
        else:
            self.btn_enviar.configure(text="Enviar")
            self.btn_guardar.configure(text="Guardar borrador")

class PanelContactos(CTkFrame):
    def __init__(self, master, cb_agregar, cb_cerrar):
        super().__init__(master, fg_color="#202020", corner_radius=10, border_width=1, width=500, height=400)
        self.pack_propagate(False)
        self.cb_agregar = cb_agregar
        
        CTkLabel(self, text="Contactos", font=CTkFont(size=24, weight="bold")).pack(pady=(12, 8))
        self.lista_contactos = CTkScrollableFrame(self, width=440, height=220, fg_color="transparent")
        self.lista_contactos.pack(padx=20, pady=(0, 12), fill="both", expand=False)
        
        seccion_agregar = CTkFrame(self, fg_color="transparent")
        seccion_agregar.pack(padx=20, pady=(0, 12), fill="x")

        CTkLabel(seccion_agregar, text="Agregar por correo:").pack(anchor="w")
        self.entry_contacto_correo = CTkEntry(seccion_agregar, width=320)
        self.entry_contacto_correo.pack(side="left", padx=(0, 8), pady=(6, 0))

        CTkButton(seccion_agregar, text="Agregar", width=90, command=self.cb_agregar).pack(side="left", pady=(6, 0))
        CTkButton(self, text="Cerrar", fg_color="#5A5A5A", hover_color="#474747", command=cb_cerrar).pack(pady=(0, 12))

    def obtener_correo(self):
        return self.entry_contacto_correo.get().strip()

    def limpiar_correo(self):
        self.entry_contacto_correo.delete(0, "end")

    def limpiar_lista(self):
        for widget in self.lista_contactos.winfo_children(): 
            widget.destroy()

class PanelCuenta(CTkFrame):
    def __init__(self, master, nombre, correo, usuario_id, cb_cerrar_sesion, cb_cerrar):
        super().__init__(master, fg_color="#202020", corner_radius=10, border_width=1, width=420, height=280)
        self.pack_propagate(False)

        CTkLabel(self, text="Cuenta", font=CTkFont(size=24, weight="bold")).pack(pady=(20, 12))
        datos_cuenta = CTkLabel(self, text=f"Nombre: {nombre}\nCorreo: {correo}\nID: {usuario_id}", justify="left", text_color="white", font=CTkFont(size=16))
        datos_cuenta.pack(pady=(0, 24))

        CTkButton(self, text="Cerrar sesion", fg_color="#8B1E1E", hover_color="#6F1818", command=cb_cerrar_sesion).pack(pady=(0, 10))
        CTkButton(self, text="Cerrar", fg_color="#5A5A5A", hover_color="#474747", command=cb_cerrar).pack()
