def login(correo, contraseña):
    conexion = sqlite3.connect("BaseDeDatos.db")  # MISMA BD
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id, contraseña FROM Correos WHERE correo = ?
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