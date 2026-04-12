import sys
from Clases import *
from customtkinter import *
from PIL import Image


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

Msj = CTkFrame(Ventana, fg_color="#676767", corner_radius=-1, border_width=-1)
Msj.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)

info_usuario = CTkLabel(
    Fila,
    text=f"Usuario: {nombre_usuario}    Correo: {correo_usuario}    ID: {usuario_id}",
    text_color="white",
    font=CTkFont(size=20, weight="bold"),
)
info_usuario.grid(row=0, column=0, padx=20, pady=20, sticky="w")

Enviar = CTkImage(
    light_image=Image.open("avion2.png"),
    dark_image=Image.open("avion2.png"),
    size=(70, 50),
)
Boton_Enviar = CTkButton(Pilar, text="", image=Enviar, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Enviar.place(x=10, y=25)
Tooltip(Pilar, Boton_Enviar, "Enviar")

Recibido = CTkImage(
    light_image=Image.open("recibido.png"),
    dark_image=Image.open("recibido.png"),
    size=(90, 70),
)
Boton_Recibido = CTkButton(Pilar, text="", image=Recibido, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Recibido.place(x=5, y=100)
Tooltip(Pilar, Boton_Recibido, "Recibido"    )
    
Borrar = CTkImage(
    light_image=Image.open("basura.png"),
    dark_image=Image.open("basura.png"),
    size=(70, 70),
)
Boton_Borrar = CTkButton(Pilar, text="", image=Borrar, fg_color="#2B2B2B", hover_color="#3B3B3B", corner_radius=0, width=0, height=0)
Boton_Borrar.place(x=10, y=200)
Tooltip(Pilar, Boton_Borrar, "Papelería")

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


Ventana.mainloop()