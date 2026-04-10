import sqlite3

DB_PATH = "BaseDeDatos.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Correos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                correo TEXT UNIQUE NOT NULL,
                "contraseña" TEXT NOT NULL,
                nombre TEXT
            )
            """
        )


def normalizar_tabla():
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute("PRAGMA table_info(Correos)")
        columnas = [columna[1] for columna in cursor.fetchall()]

        if "contraseÃ±a" in columnas and "contraseña" not in columnas:
            cursor.execute('ALTER TABLE Correos RENAME COLUMN "contraseÃ±a" TO "contraseña"')


def registrar(correo, contrasena, nombre):
    try:
        with sqlite3.connect(DB_PATH) as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                'INSERT INTO Correos (correo, "contraseña", nombre) VALUES (?, ?, ?)',
                (correo, contrasena, nombre),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def obtener_usuario_por_credenciales(correo, contrasena):
    with sqlite3.connect(DB_PATH) as conexion:
        cursor = conexion.cursor()
        cursor.execute(
            'SELECT id, correo, "contraseña", nombre FROM Correos WHERE correo = ?',
            (correo,),
        )
        usuario = cursor.fetchone()

    if usuario and usuario[2] == contrasena:
        return {
            "id": usuario[0],
            "correo": usuario[1],
            "nombre": usuario[3] or "Usuario",
        }
    return None


def login(correo, contrasena):
    usuario = obtener_usuario_por_credenciales(correo, contrasena)
    if usuario:
        return usuario["id"]
    return None


init_db()
normalizar_tabla()
