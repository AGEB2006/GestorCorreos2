from customtkinter import *
from bd import *

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

def enviar_mensaje(remitente_id, destinatario_id, asunto, contenido):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO Mensajes (remitente_id, destinatario_id, asunto, contenido)
            VALUES (?, ?, ?, ?)
            """,
            (remitente_id, destinatario_id, asunto, contenido)
        )
        conexion.commit()

def obtener_mensajes_recibidos(usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT id, remitente_id, asunto, contenido, fecha, leido
            FROM Mensajes
            WHERE destinatario_id = ? AND eliminado = 0
            ORDER BY fecha DESC
            """,
            (usuario_id,)
        )
        return cursor.fetchall()

def eliminar_mensaje(mensaje_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE Mensajes SET eliminado = 1 WHERE id = ?",
            (mensaje_id,)
        )
        conexion.commit()