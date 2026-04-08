from customtkinter import *

Ventana = CTk()
Ventana.geometry("1200x700+250+50")

Pilar = CTkFrame(Ventana,  fg_color="#2B2B2B", corner_radius=0)
Pilar.place( x = 0, y = 40, relwidth=0.105, relheight=1)
Fila = CTkFrame(Ventana, width=3000, height=120,  fg_color="#2B2B2B", corner_radius=0)
Fila.place( x = 0, y = 0, relwidth=1)


Ventana.mainloop()