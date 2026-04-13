from bd import conectar


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


def obtener_mensajes_enviados(usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT
                m.id,
                m.destinatario_id,
                COALESCE(c.nombre, c.correo, 'Desconocido') AS destinatario,
                m.asunto,
                m.contenido,
                m.fecha,
                m.leido
            FROM Mensajes m
            LEFT JOIN Correos c ON c.id = m.destinatario_id
            WHERE m.remitente_id = ? AND m.eliminado = 0 AND m.tipo = 'enviado'
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
        return cursor.rowcount > 0


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
        return cursor.lastrowid


def actualizar_borrador(borrador_id, asunto, contenido):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Mensajes
            SET asunto = ?, contenido = ?, fecha = CURRENT_TIMESTAMP
            WHERE id = ? AND tipo = 'borrador'
            """,
            (asunto, contenido, borrador_id),
        )
        conexion.commit()
        return cursor.rowcount > 0


def obtener_borrador_por_id(borrador_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT id, asunto, contenido, fecha
            FROM Mensajes
            WHERE id = ? AND tipo = 'borrador' AND eliminado = 0
            """,
            (borrador_id,),
        )
        return cursor.fetchone()


def eliminar_borrador(borrador_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Mensajes
            SET eliminado = 1
            WHERE id = ? AND tipo = 'borrador'
            """,
            (borrador_id,),
        )
        conexion.commit()
        return cursor.rowcount > 0


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


def obtener_papelera(usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT
                m.id,
                m.tipo,
                COALESCE(c.nombre, c.correo, 'Sin remitente') AS remitente,
                m.asunto,
                m.contenido,
                m.fecha
            FROM Mensajes m
            LEFT JOIN Correos c ON c.id = m.remitente_id
            WHERE
                m.eliminado = 1
                AND (m.destinatario_id = ? OR m.remitente_id = ?)
            ORDER BY m.fecha DESC
            """,
            (usuario_id, usuario_id),
        )
        return cursor.fetchall()


def restaurar_desde_papelera(mensaje_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Mensajes
            SET eliminado = 0
            WHERE id = ?
            """,
            (mensaje_id,),
        )
        conexion.commit()
        return cursor.rowcount > 0


def eliminar_definitivamente(mensaje_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            DELETE FROM Mensajes
            WHERE id = ?
            """,
            (mensaje_id,),
        )
        conexion.commit()
        return cursor.rowcount > 0
