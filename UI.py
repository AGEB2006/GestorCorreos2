from customtkinter import *
from PIL import Image

Ventana = CTk()
Ventana.geometry("1200x700+250+50")

Pilar = CTkFrame(Ventana,  fg_color="#2B2B2B", corner_radius=0)
Pilar.place( x = 0, y = 40, relwidth=0.105, relheight=1)
Fila = CTkFrame(Ventana, width=2000, height=100,  fg_color="#2B2B2B", corner_radius=0)
Fila.place( x = 0, y = 0, relwidth=1)
Msj= CTkFrame (Ventana, fg_color = "blue", corner_radius=0)
Msj.place( x = 126, y = 100, relwidth=0.985, relheight=1)
#---------------------------------------------------------------------------------------------------
Enviar = CTkImage(light_image=Image.open("avion2.png"),
                       dark_image=Image.open("avion2.png"),
                       size=(70, 50))
Boton_Enviar = CTkButton(Ventana, text="", image=Enviar, fg_color="#2B2B2B",hover_color="#3B3B3B", 
                         corner_radius=0,width=0,height=0)
Boton_Enviar.place(x=32, y=100)
tooltip = CTkLabel(Ventana, text="Enviar", fg_color="#2B2B2B", text_color="white", corner_radius=6)

def mostrar_tooltip(event):
    x = Boton_Enviar.winfo_rootx() - Ventana.winfo_rootx()
    y = Boton_Enviar.winfo_rooty() - Ventana.winfo_rooty()
    tooltip.place(x=x + Boton_Enviar.winfo_width()//2 - 10,  
                  y=y + Boton_Enviar.winfo_height() + -40) 
    tooltip.lift()
def ocultar_tooltip(event):
    tooltip.place_forget()
Boton_Enviar.bind("<Enter>", mostrar_tooltip)
Boton_Enviar.bind("<Leave>", ocultar_tooltip)

#----------------------------------------------------------------------------------
Recibido = CTkImage(light_image=Image.open("recibido.png"),
                       dark_image=Image.open("recibido.png"),
                       size=(90, 70))
Boton_Recibido = CTkButton(Ventana, text="", image=Recibido, fg_color="#2B2B2B",
                           hover_color="#3B3B3B", 
                           corner_radius=0,width=0,height=0)
Boton_Recibido.place(x=25, y=165)
tooltip2 = CTkLabel(Ventana, text="Recibido", fg_color="#2B2B2B", text_color="white", corner_radius=6)

def mostrar_tooltip2(event):
    x = Boton_Recibido.winfo_rootx() - Ventana.winfo_rootx()
    y = Boton_Recibido.winfo_rooty() - Ventana.winfo_rooty()
    tooltip2.place(x=x + Boton_Recibido.winfo_width()//2 - 10,  
                   y=y + Boton_Recibido.winfo_height() + -40)   
    tooltip2.lift()  
def ocultar_tooltip2(event):
    tooltip2.place_forget()
Boton_Recibido.bind("<Enter>", mostrar_tooltip2)
Boton_Recibido.bind("<Leave>", ocultar_tooltip2)

Ventana.mainloop()