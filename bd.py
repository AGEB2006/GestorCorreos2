import hashlib
import hmac
import sqlite3

DB_PATH = "BaseDeDatos.db"
HASH_PREFIX = "sha256$"


def conectar():
    return sqlite3.connect(DB_PATH)


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
    try:
        with conectar() as conexion:
            cursor = conexion.cursor()
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
    with conectar() as conexion:
        cursor = conexion.cursor()
        columna_contrasena = obtener_columna_contrasena(cursor)
        cursor.execute(
            f'SELECT id, correo, "{columna_contrasena}", nombre FROM Correos WHERE correo = ?',
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
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, correo, nombre FROM Correos WHERE correo = ?",
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


def obtener_pregunta_seguridad(correo):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT pregunta_seguridad FROM Correos WHERE correo = ?",
            (correo,),
        )
        fila = cursor.fetchone()

    if fila and fila[0]:
        return fila[0]
    return None


def verificar_respuesta_seguridad(correo, respuesta):
    with conectar() as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT respuesta_seguridad FROM Correos WHERE correo = ?",
            (correo,),
        )
        fila = cursor.fetchone()

    if not fila or not fila[0]:
        return False
    return fila[0].strip().lower() == respuesta.strip().lower()


def actualizar_contrasena(correo, nueva_contrasena):
    with conectar() as conexion:
        cursor = conexion.cursor()
        columna_contrasena = obtener_columna_contrasena(cursor)
        cursor.execute(
            f'UPDATE Correos SET "{columna_contrasena}" = ? WHERE correo = ?',
            (hash_contrasena(nueva_contrasena), correo),
        )
        conexion.commit()
        return cursor.rowcount > 0


def login(correo, contrasena):
    usuario = obtener_usuario_por_credenciales(correo, contrasena)
    if usuario:
        return usuario["id"]
    return None


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


init_db()
normalizar_tabla()
crear_tabla_mensajes()
