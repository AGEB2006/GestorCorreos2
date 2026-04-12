from customtkinter import *


def agregar_mensaje(contenedor, texto, tipo="recibido"):
    if tipo == "recibido":
        anchor = "w"
        color = "#3B3B3B"
    else:
        anchor = "e"
        color = "#1F6AA5"

    burbuja = CTkFrame(
        contenedor,
        fg_color=color,
        corner_radius=10
    )

    label = CTkLabel(
        burbuja,
        text=texto,
        text_color="white",
        wraplength=300,
        justify="left"
    )
    label.pack(padx=10, pady=5)

    burbuja.pack(anchor=anchor, pady=5, padx=10)