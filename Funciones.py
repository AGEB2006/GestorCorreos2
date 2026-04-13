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


def _eliminar_fisicamente_si_corresponde(cursor, mensaje_id):
    cursor.execute(
        """
        DELETE FROM Mensajes
        WHERE id = ?
          AND (
              (tipo = 'borrador' AND visible_remitente = 0)
              OR (tipo <> 'borrador' AND visible_remitente = 0 AND visible_destinatario = 0)
          )
        """,
        (mensaje_id,),
    )


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
            WHERE
                m.destinatario_id = ?
                AND m.tipo = 'enviado'
                AND m.visible_destinatario = 1
                AND m.eliminado_destinatario = 0
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
            WHERE
                m.remitente_id = ?
                AND m.tipo = 'enviado'
                AND m.visible_remitente = 1
                AND m.eliminado_remitente = 0
            ORDER BY m.fecha DESC
            """,
            (usuario_id,),
        )
        return cursor.fetchall()


def eliminar_mensaje(mensaje_id, usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Mensajes
            SET
                eliminado_remitente = CASE
                    WHEN remitente_id = ? AND visible_remitente = 1 THEN 1
                    ELSE eliminado_remitente
                END,
                eliminado_destinatario = CASE
                    WHEN destinatario_id = ? AND visible_destinatario = 1 THEN 1
                    ELSE eliminado_destinatario
                END
            WHERE id = ?
              AND (
                  (remitente_id = ? AND visible_remitente = 1)
                  OR (destinatario_id = ? AND visible_destinatario = 1)
              )
            """,
            (usuario_id, usuario_id, mensaje_id, usuario_id, usuario_id),
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
            WHERE
                id = ?
                AND tipo = 'borrador'
                AND visible_remitente = 1
                AND eliminado_remitente = 0
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
            SET eliminado_remitente = 1
            WHERE id = ? AND tipo = 'borrador' AND visible_remitente = 1
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
            WHERE
                remitente_id = ?
                AND tipo = 'borrador'
                AND visible_remitente = 1
                AND eliminado_remitente = 0
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
                id,
                tipo,
                referencia,
                asunto,
                contenido,
                fecha
            FROM (
                SELECT
                    m.id,
                    m.tipo,
                    'Borrador' AS referencia,
                    m.asunto,
                    m.contenido,
                    m.fecha
                FROM Mensajes m
                WHERE
                    m.tipo = 'borrador'
                    AND m.remitente_id = ?
                    AND m.visible_remitente = 1
                    AND m.eliminado_remitente = 1

                UNION ALL

                SELECT
                    m.id,
                    m.tipo,
                    COALESCE(c.nombre, c.correo, 'Sin destinatario') AS referencia,
                    m.asunto,
                    m.contenido,
                    m.fecha
                FROM Mensajes m
                LEFT JOIN Correos c ON c.id = m.destinatario_id
                WHERE
                    m.tipo = 'enviado'
                    AND m.remitente_id = ?
                    AND m.visible_remitente = 1
                    AND m.eliminado_remitente = 1

                UNION ALL

                SELECT
                    m.id,
                    m.tipo,
                    COALESCE(c.nombre, c.correo, 'Sin remitente') AS referencia,
                    m.asunto,
                    m.contenido,
                    m.fecha
                FROM Mensajes m
                LEFT JOIN Correos c ON c.id = m.remitente_id
                WHERE
                    m.tipo = 'enviado'
                    AND m.destinatario_id = ?
                    AND m.visible_destinatario = 1
                    AND m.eliminado_destinatario = 1
            )
            ORDER BY fecha DESC
            """,
            (usuario_id, usuario_id, usuario_id),
        )
        return cursor.fetchall()


def restaurar_desde_papelera(mensaje_id, usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE Mensajes
            SET
                eliminado_remitente = CASE
                    WHEN remitente_id = ? AND visible_remitente = 1 THEN 0
                    ELSE eliminado_remitente
                END,
                eliminado_destinatario = CASE
                    WHEN destinatario_id = ? AND visible_destinatario = 1 THEN 0
                    ELSE eliminado_destinatario
                END
            WHERE id = ?
              AND (
                  (remitente_id = ? AND visible_remitente = 1)
                  OR (destinatario_id = ? AND visible_destinatario = 1)
              )
            """,
            (usuario_id, usuario_id, mensaje_id, usuario_id, usuario_id),
        )
        conexion.commit()
        return cursor.rowcount > 0


def eliminar_definitivamente(mensaje_id, usuario_id=None):
    with conectar() as conexion:
        cursor = conexion.cursor()

        if usuario_id is None:
            cursor.execute(
                """
                DELETE FROM Mensajes
                WHERE id = ? AND tipo = 'borrador'
                """,
                (mensaje_id,),
            )
        else:
            cursor.execute(
                """
                UPDATE Mensajes
                SET
                    visible_remitente = CASE
                        WHEN remitente_id = ? AND visible_remitente = 1 THEN 0
                        ELSE visible_remitente
                    END,
                    visible_destinatario = CASE
                        WHEN destinatario_id = ? AND visible_destinatario = 1 THEN 0
                        ELSE visible_destinatario
                    END
                WHERE id = ?
                  AND (
                      (remitente_id = ? AND visible_remitente = 1)
                      OR (destinatario_id = ? AND visible_destinatario = 1)
                  )
                """,
                (usuario_id, usuario_id, mensaje_id, usuario_id, usuario_id),
            )
            if cursor.rowcount > 0:
                _eliminar_fisicamente_si_corresponde(cursor, mensaje_id)

        conexion.commit()
        return cursor.rowcount > 0
