import sys
from Clases import *
from customtkinter import *
from PIL import Image
from Funciones import *


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
agregar_mensaje(Contenedor_Msj, "Hola", "recibido")

info_usuario = CTkLabel(
    Fila,
    text=f"Usuario: {nombre_usuario}    Correo: {correo_usuario}    ID: {usuario_id}",
    text_color="white",
    font=CTkFont(size=20, weight="bold"),
)
info_usuario.grid(row=0, column=0, padx=20, pady=20, sticky="w")


Enviar = CTkImage(
    light_image=Image.open("Lapiz.png"),
    dark_image=Image.open("Lapiz.png"),
    size=(30, 30),
)

frame_visible = False
frame_redactar = CTkFrame(Msj, fg_color="#202020", corner_radius=10, border_width=1, 
                           width=500, height=400) 
frame_redactar.place_forget()
frame_redactar.grid_propagate(False)

# Correo destinatario
label_dest = CTkLabel(frame_redactar, text="Para:")
label_dest.pack(pady=(10, 0))

entry_dest = CTkEntry(frame_redactar, width=300)
entry_dest.pack(pady=5)

# Asunto
label_asunto = CTkLabel(frame_redactar, text="Asunto:")
label_asunto.pack(pady=(10, 0))

entry_asunto = CTkEntry(frame_redactar, width=300)
entry_asunto.pack(pady=5)

# Contenido
label_contenido = CTkLabel(frame_redactar, text="Mensaje:")
label_contenido.pack(pady=(10, 0))

textbox_contenido = CTkTextbox(frame_redactar, width=350, height=150)
textbox_contenido.pack(pady=10)

Enviar_Msj = CTkButton(frame_redactar, text="Enviar", fg_color="#1F6AA5", hover_color="#3B3B3B", corner_radius=5, width=10, height=20)
Enviar_Msj.pack(pady=10)

dest = entry_dest.get()
asunto = entry_asunto.get()
contenido = textbox_contenido.get("1.0", "end").strip()

if asunto or contenido:
    guardar_borrador(usuario_id, dest, asunto, contenido)
def toggle_redactar():
    global frame_visible

    if not frame_visible:
        frame_redactar.place(relx=0.5, rely=0.5, anchor="center")
        frame_visible = True
    else:
        frame_redactar.place_forget()
        frame_visible = False

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
Tooltip(Pilar, Boton_Borrador, "Borradores")







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