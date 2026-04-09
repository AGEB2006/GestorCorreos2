import sqlite3

conexion = sqlite3.connect("BaseDeDatos.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Correos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    nombre TEXT
)
               
""")

conexion.commit()
print("Base de datos inicializada correctamente.")


def registrar(correo, contraseña, nombre):
    conexion = sqlite3.connect("BaseDeDatos.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("""
        INSERT INTO Correos (correo, contraseña, nombre)
        VALUES (?, ?, ?)
        """, (correo, contraseña, nombre))

        conexion.commit()
        print("Usuario registrado correctamente ")

    except sqlite3.IntegrityError:
        print("Ese correo ya está registrado en la base de datos.")

    conexion.close()

def login(correo, contraseña):
    conexion = sqlite3.connect("correo.db")
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, contraseña FROM usuarios WHERE correo = ?
    """, (correo,))

    usuario = cursor.fetchone()

    if usuario:
        if usuario[1] == contraseña:
            print("Login correcto 🔥")
            return usuario[0]  
        else:
            print("Contraseña incorrecta ❌")
    else:
        print("Usuario no existe ❌")

    conexion.close()
    return None

registrar("inge@gmail.com", "1234", "Inge")

user_id = login("inge@gmail.com", "1234")

print("ID del usuario:", user_id)