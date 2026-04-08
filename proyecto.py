import sqlite3

conexion = sqlite3.connect("BaseDeDatos.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Correos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    remitente TEXT, 
    destinatario TEXT, 
    asunto TEXT, 
    mensaje TEXT
)
               
""")

conexion.commit()
print("Base de datos inicializada correctamente.")

#probando a ver si ya queda el proyecto listo para subir a github

"gael es la cabra"

"ieshua puto"

"ieshua pendejo"

"gael es un reverendo pendejo alv putoputoputopuuuuuuuuuuuuuuuuuuuuuuuuuuutooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
"hola mundo"