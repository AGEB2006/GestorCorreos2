import hashlib
import hmac
import os
import sqlite3

from app_utils import get_database_path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = get_database_path("BaseDeDatos.db")
HASH_PREFIX = "sha256$"


def conectar():
    conexion = sqlite3.connect(DB_PATH, timeout=30)
    conexion.execute("PRAGMA busy_timeout = 30000")
    return conexion


def normalizar_correo(correo):
    return correo.strip().lower()


def obtener_columna_contrasena(cursor):
    cursor.execute("PRAGMA table_info(Correos)")
    columnas = [columna[1] for columna in cursor.fetchall()]

    for nombre in columnas:
        if "contrase" in nombre.lower():
            return nombre
    return "contrasena"


def hash_contrasena(contrasena):
    return f"{HASH_PREFIX}{hashlib.sha256(contrasena.encode('utf-8')).hexdigest()}"


def verificar_contrasena_guardada(contrasena_ingresada, contrasena_guardada):
    if not contrasena_guardada:
        return False

    if contrasena_guardada.startswith(HASH_PREFIX):
        hash_esperado = hash_contrasena(contrasena_ingresada)
        return hmac.compare_digest(hash_esperado, contrasena_guardada)

    return hmac.compare_digest(contrasena_ingresada, contrasena_guardada)


def init_db():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Correos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correo TEXT UNIQUE NOT NULL,
                contrasena TEXT NOT NULL,
                nombre TEXT,
                telefono TEXT,
                pregunta_seguridad TEXT,
                respuesta_seguridad TEXT
            )
            """
        )


def normalizar_tabla():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("PRAGMA table_info(Correos)")
        columnas = [columna[1] for columna in cursor.fetchall()]

        if "telefono" not in columnas:
            cursor.execute("ALTER TABLE Correos ADD COLUMN telefono TEXT")
        if "pregunta_seguridad" not in columnas:
            cursor.execute("ALTER TABLE Correos ADD COLUMN pregunta_seguridad TEXT")
        if "respuesta_seguridad" not in columnas:
            cursor.execute("ALTER TABLE Correos ADD COLUMN respuesta_seguridad TEXT")


def registrar(correo, contrasena, nombre, telefono, pregunta_seguridad, respuesta_seguridad):
    correo = normalizar_correo(correo)
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT 1 FROM Correos WHERE LOWER(correo) = ?", (correo,))
            if cursor.fetchone():
                return False
            columna_contrasena = obtener_columna_contrasena(cursor)
            cursor.execute(
                f"""
                INSERT INTO Correos (
                    correo, "{columna_contrasena}", nombre, telefono, pregunta_seguridad, respuesta_seguridad
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    correo,
                    hash_contrasena(contrasena),
                    nombre,
                    telefono,
                    pregunta_seguridad,
                    respuesta_seguridad.strip().lower(),
                ),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def obtener_usuario_por_credenciales(correo, contrasena):
    correo = normalizar_correo(correo)
    with conectar() as conexion:
        cursor = conexion.cursor()
        columna_contrasena = obtener_columna_contrasena(cursor)
        cursor.execute(
            f'SELECT id, correo, "{columna_contrasena}", nombre FROM Correos WHERE LOWER(correo) = ?',
            (correo,),
        )
        usuario = cursor.fetchone()

        if usuario and verificar_contrasena_guardada(contrasena, usuario[2]):
            # Migra cuentas antiguas en texto plano al nuevo formato hash.
            if not usuario[2].startswith(HASH_PREFIX):
                cursor.execute(
                    f'UPDATE Correos SET "{columna_contrasena}" = ? WHERE id = ?',
                    (hash_contrasena(contrasena), usuario[0]),
                )
                conexion.commit()

            return {
                "id": usuario[0],
                "correo": usuario[1],
                "nombre": usuario[3] or "Usuario",
            }

    return None


def obtener_usuario_por_correo(correo):
    correo = normalizar_correo(correo)
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, correo, nombre FROM Correos WHERE LOWER(correo) = ?",
            (correo,),
        )
        usuario = cursor.fetchone()

    if usuario:
        return {
            "id": usuario[0],
            "correo": usuario[1],
            "nombre": usuario[2] or usuario[1],
        }
    return None


def obtener_usuario_por_id(usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, correo, nombre FROM Correos WHERE id = ?",
            (usuario_id,),
        )
        usuario = cursor.fetchone()

    if usuario:
        return {
            "id": usuario[0],
            "correo": usuario[1],
            "nombre": usuario[2] or usuario[1],
        }
    return None


def obtener_pregunta_seguridad(correo):
    correo = normalizar_correo(correo)
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT pregunta_seguridad FROM Correos WHERE LOWER(correo) = ?",
            (correo,),
        )
        fila = cursor.fetchone()

    if fila and fila[0]:
        return fila[0]
    return None


def verificar_respuesta_seguridad(correo, respuesta):
    correo = normalizar_correo(correo)
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT respuesta_seguridad FROM Correos WHERE LOWER(correo) = ?",
            (correo,),
        )
        fila = cursor.fetchone()

    if not fila or not fila[0]:
        return False
    return fila[0].strip().lower() == respuesta.strip().lower()


def actualizar_contrasena(correo, nueva_contrasena):
    correo = normalizar_correo(correo)
    with conectar() as conexion:
        cursor = conexion.cursor()
        columna_contrasena = obtener_columna_contrasena(cursor)
        cursor.execute(
            f'UPDATE Correos SET "{columna_contrasena}" = ? WHERE LOWER(correo) = ?',
            (hash_contrasena(nueva_contrasena), correo),
        )
        conexion.commit()
        return cursor.rowcount > 0


def crear_tabla_mensajes():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente_id INTEGER,
                destinatario_id INTEGER,
                asunto TEXT,
                contenido TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                leido INTEGER DEFAULT 0,
                eliminado INTEGER DEFAULT 0,
                tipo TEXT DEFAULT 'enviado',
                FOREIGN KEY(remitente_id) REFERENCES Correos(id),
                FOREIGN KEY(destinatario_id) REFERENCES Correos(id)
            )
            """
        )


def normalizar_tabla_mensajes():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute("PRAGMA table_info(Mensajes)")
        columnas = [columna[1] for columna in cursor.fetchall()]

        if "eliminado_remitente" not in columnas:
            cursor.execute("ALTER TABLE Mensajes ADD COLUMN eliminado_remitente INTEGER DEFAULT 0")
            cursor.execute("UPDATE Mensajes SET eliminado_remitente = COALESCE(eliminado, 0)")

        if "eliminado_destinatario" not in columnas:
            cursor.execute("ALTER TABLE Mensajes ADD COLUMN eliminado_destinatario INTEGER DEFAULT 0")
            cursor.execute(
                """
                UPDATE Mensajes
                SET eliminado_destinatario = CASE
                    WHEN tipo = 'borrador' THEN 1
                    ELSE COALESCE(eliminado, 0)
                END
                """
            )

        if "visible_remitente" not in columnas:
            cursor.execute("ALTER TABLE Mensajes ADD COLUMN visible_remitente INTEGER DEFAULT 1")
            cursor.execute("UPDATE Mensajes SET visible_remitente = 1")

        if "visible_destinatario" not in columnas:
            cursor.execute("ALTER TABLE Mensajes ADD COLUMN visible_destinatario INTEGER DEFAULT 1")
            cursor.execute(
                """
                UPDATE Mensajes
                SET visible_destinatario = CASE
                    WHEN tipo = 'borrador' THEN 0
                    ELSE 1
                END
                """
            )

        cursor.execute(
            """
            UPDATE Mensajes
            SET eliminado_destinatario = 1
            WHERE tipo = 'borrador'
            """
        )
        cursor.execute(
            """
            UPDATE Mensajes
            SET visible_destinatario = 0
            WHERE tipo = 'borrador'
            """
        )
        conexion.commit()


def crear_tabla_contactos():
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                contacto_id INTEGER NOT NULL,
                UNIQUE(usuario_id, contacto_id),
                FOREIGN KEY(usuario_id) REFERENCES Correos(id),
                FOREIGN KEY(contacto_id) REFERENCES Correos(id)
            )
            """
        )


def obtener_contactos(usuario_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT
                c.id,
                u.nombre,
                u.correo
            FROM Contactos c
            JOIN Correos u ON u.id = c.contacto_id
            WHERE c.usuario_id = ?
            ORDER BY COALESCE(u.nombre, u.correo), u.correo
            """,
            (usuario_id,),
        )
        return cursor.fetchall()


def agregar_contacto_por_correo(usuario_id, correo_contacto):
    correo_contacto = normalizar_correo(correo_contacto)
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, correo, nombre FROM Correos WHERE LOWER(correo) = ?",
            (correo_contacto,),
        )
        contacto = cursor.fetchone()

        if not contacto:
            return False, "No existe una cuenta con ese correo."

        if contacto[0] == usuario_id:
            return False, "No puedes agregarte a ti mismo como contacto."

        try:
            cursor.execute(
                """
                INSERT INTO Contactos (usuario_id, contacto_id)
                VALUES (?, ?)
                """,
                (usuario_id, contacto[0]),
            )
            conexion.commit()
        except sqlite3.IntegrityError:
            return False, "Ese contacto ya está agregado."

    return True, {
        "id": contacto[0],
        "correo": contacto[1],
        "nombre": contacto[2] or contacto[1],
    }


def eliminar_contacto(contacto_relacion_id):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            DELETE FROM Contactos
            WHERE id = ?
            """,
            (contacto_relacion_id,),
        )
        conexion.commit()
        return cursor.rowcount > 0


init_db()
normalizar_tabla()
crear_tabla_mensajes()
normalizar_tabla_mensajes()
crear_tabla_contactos()
