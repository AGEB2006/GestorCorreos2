from customtkinter import *

Ventana = CTk()
Ventana.geometry("1200x700+250+50")
Pilar = CTkFrame(Ventana, width=100, height=1000,  fg_color="#2B2B2B")
Pilar.place( relx = 0, rely = 0)

Fila = CTkFrame(Ventana, width=3000, height=100,  fg_color="#2B2B2B")
Fila.place( relx = 0, rely = 0)

Ventana.mainloop()