from customtkinter import *
from PIL import Image

Ventana = CTk()
Ventana.geometry("1200x700+250+50")
Ventana.grid_rowconfigure(1, weight=1)
Ventana.grid_columnconfigure(1, weight=1)
Fila = CTkFrame(Ventana,  fg_color="#2B2B2B", height=100,corner_radius=-1, border_width=-1)
Fila.grid(row = 0, column = 0, columnspan=2, sticky="nsew",padx=0, pady=0)
Pilar= CTkFrame(Ventana, width=100, height=100,  fg_color="#2B2B2B", corner_radius=-1, border_width=-1)
Pilar.grid(row = 1, column = 0, sticky="nsew", padx=0, pady=0)
Msj = CTkFrame (Ventana, fg_color = "#676767", corner_radius=-1, border_width=-1)
Msj.grid(row = 1, column = 1, sticky="nsew", padx=0, pady=0)
#----------------------------------------------------------------------------------------------------------
Enviar = CTkImage(light_image=Image.open("avion2.png"),
                       dark_image=Image.open("avion2.png"),
                       size=(70, 50))
Boton_Enviar = CTkButton(Pilar, text="", image=Enviar, fg_color="#2B2B2B",hover_color="#3B3B3B", 
                         corner_radius=0,width=0,height=0)
Boton_Enviar.place(x=10, y=25)
tooltip = CTkLabel(Pilar, text="Enviar", fg_color="#2B2B2B", text_color="white", corner_radius=6)
def mostrar_tooltip(event):
    x = Boton_Enviar.winfo_rootx() - Pilar.winfo_rootx()
    y = Boton_Enviar.winfo_rooty() - Pilar.winfo_rooty()
    tooltip.place(x=x + Boton_Enviar.winfo_width()//2 - tooltip.winfo_width()//2,
              y=y + Boton_Enviar.winfo_height() - 40)
    tooltip.lift()
def ocultar_tooltip(event):
    tooltip.place_forget()
Boton_Enviar.bind("<Enter>", mostrar_tooltip)
Boton_Enviar.bind("<Leave>", ocultar_tooltip)
#---------------------------------------------------------------------------------------------------
Recibido = CTkImage(light_image=Image.open("recibido.png"),
                       dark_image=Image.open("recibido.png"),
                       size=(90, 70))
Boton_Recibido = CTkButton(Pilar, text="", image=Recibido, fg_color="#2B2B2B",
                           hover_color="#3B3B3B", 
                           corner_radius=0,width=0,height=0)
Boton_Recibido.place(x=5, y=100)
tooltip2 = CTkLabel(Pilar, text="Recibido", fg_color="#2B2B2B", text_color="white", corner_radius=6)
def mostrar_tooltip2(event):
    x = Boton_Recibido.winfo_rootx() - Pilar.winfo_rootx()
    y = Boton_Recibido.winfo_rooty() - Pilar.winfo_rooty()
    tooltip2.place(x=x + Boton_Recibido.winfo_width()//2 - tooltip2.winfo_width()//2,
              y=y + Boton_Recibido.winfo_height() - 40)
    tooltip2.lift()  
def ocultar_tooltip2(event):
    tooltip2.place_forget()
Boton_Recibido.bind("<Enter>", mostrar_tooltip2)
Boton_Recibido.bind("<Leave>", ocultar_tooltip2)
#---------------------------------------------------------------------------------------------------
Borrar = CTkImage(light_image=Image.open("basura.png"),
                       dark_image=Image.open("basura.png"),
                       size=(70, 70))
Boton_Borrar = CTkButton(Pilar, text="", image=Borrar, fg_color="#2B2B2B", hover_color="#3B3B3B",
                         corner_radius=0,width=0,height=0)
Boton_Borrar.place(x=10, y=200)
tooltip3 = CTkLabel(Pilar, text="Borrar", fg_color="#2B2B2B", text_color="white", corner_radius=6)
def mostrar_tooltip3(event):
    x = Boton_Borrar.winfo_rootx() - Pilar.winfo_rootx()
    y = Boton_Borrar.winfo_rooty() - Pilar.winfo_rooty()
    tooltip3.place(x=x + Boton_Borrar.winfo_width()//2 - tooltip3.winfo_width()//2,
              y=y + Boton_Borrar.winfo_height() - 40)  
    tooltip3.lift()  
def ocultar_tooltip3(event):
    tooltip3.place_forget()
Boton_Borrar.bind("<Enter>", mostrar_tooltip3)
Boton_Borrar.bind("<Leave>", ocultar_tooltip3)
#---------------------------------------------------------------------------------------------------
Contactos = CTkImage(light_image=Image.open("contactos.png"),
                       dark_image=Image.open("contactos.png"),
                       size=(70, 70))
Boton_Contactos = CTkButton(Pilar, text="", image=Contactos, fg_color="#2B2B2B", hover_color="#3B3B3B", 
                            corner_radius=0,width=0,height=0)       
Boton_Contactos.place(x=10, y=300)
tooltip4 = CTkLabel(Pilar, text="Contactos", fg_color="#2B2B2B", text_color="white", corner_radius=6)
def mostrar_tooltip4(event):
    x = Boton_Contactos.winfo_rootx() - Pilar.winfo_rootx()
    y = Boton_Contactos.winfo_rooty() - Pilar.winfo_rooty()
    tooltip4.place(x=x + Boton_Contactos.winfo_width()//2 - tooltip4.winfo_width()//2,
              y=y + Boton_Contactos.winfo_height() - 40)
    tooltip4.lift()
def ocultar_tooltip4(event):
    tooltip4.place_forget()
Boton_Contactos.bind("<Enter>", mostrar_tooltip4)
Boton_Contactos.bind("<Leave>", ocultar_tooltip4)
""""
#---------------------------------------------------------------------------------------------------
cuenta = CTkImage(light_image=Image.open("cuenta.png"),
                       dark_image=Image.open("cuenta.png"),
                       size=(70, 80))
Boton_Cuenta = CTkButton(Ventana, text="", image=cuenta, fg_color="#2B2B2B", hover_color="#3B3B3B", 
                            corner_radius=-10,width=-30,height=-30)
Boton_Cuenta.place(x=1450, y=10)
tooltip5 = CTkLabel(Ventana, text="Cuenta", fg_color="#2B2B2B", text_color="white", corner_radius=6)
def mostrar_tooltip5(event):
    x = Boton_Cuenta.winfo_rootx() - Ventana.winfo_rootx()
    y = Boton_Cuenta.winfo_rooty() - Ventana.winfo_rooty()
    tooltip5.place(x=x + Boton_Cuenta.winfo_width()//2 - 10,  
                   y=y + Boton_Cuenta.winfo_height() + -40)   
    tooltip5.lift()  
def ocultar_tooltip5(event):
    tooltip5.place_forget()
Boton_Cuenta.bind("<Enter>", mostrar_tooltip5)
Boton_Cuenta.bind("<Leave>", ocultar_tooltip5)
"""""


Ventana.mainloop()