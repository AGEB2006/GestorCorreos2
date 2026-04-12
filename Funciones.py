from customtkinter import *

from bd import conectar


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
        corner_radius=10,
    )

    label = CTkLabel(
        burbuja,
        text=texto,
        text_color="white",
        wraplength=300,
        justify="left",
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
            (remitente_id, destinatario_id, asunto, contenido),
        )
        conexion.commit()


def obtener_mensajes_recibidos(usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT
                m.id,
                m.remitente_id,
                COALESCE(c.nombre, c.correo, 'Desconocido') AS remitente,
                m.asunto,
                m.contenido,
                m.fecha,
                m.leido
            FROM Mensajes m
            LEFT JOIN Correos c ON c.id = m.remitente_id
            WHERE m.destinatario_id = ? AND m.eliminado = 0 AND m.tipo = 'enviado'
            ORDER BY m.fecha DESC
            """,
            (usuario_id,),
        )
        return cursor.fetchall()


def eliminar_mensaje(mensaje_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE Mensajes SET eliminado = 1 WHERE id = ?",
            (mensaje_id,),
        )
        conexion.commit()


def guardar_borrador(remitente_id, asunto, contenido):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO Mensajes (remitente_id, asunto, contenido, tipo)
            VALUES (?, ?, ?, 'borrador')
            """,
            (remitente_id, asunto, contenido),
        )
        conexion.commit()


def obtener_borradores(remitente_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT id, asunto, contenido, fecha
            FROM Mensajes
            WHERE remitente_id = ? AND tipo = 'borrador' AND eliminado = 0
            ORDER BY fecha DESC
            """,
            (remitente_id,),
        )
        return cursor.fetchall()
