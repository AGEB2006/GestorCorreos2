# Guía de Estudio Detallada: Versión Refactorizada (POO)

Esta guía documenta y explica línea por línea la funcionalidad de los scripts en la carpeta `Refactorizado`.

## Archivo: `Funciones.py`
Este archivo contiene y maneja centralizadamente toda la lógica de conexión y operaciones con la base de datos (SQLite).
- **¿Qué necesita para funcionar?** Necesita conectarse a la Base de Datos, por lo tanto importa la función `conectar()` del archivo `bd.py` raíz.
- **`enviar_mensaje(remitente_id, destinatario_id, asunto, contenido)`**: Ejecuta un `INSERT INTO` en la tabla `Mensajes`. Recibe todos los parámetros del texto escrito en la UI y crea el nuevo correo interno.
- **`_eliminar_fisicamente_si_corresponde(cursor, mensaje_id)`**: Es una función de optimización interna (escondida por el guion bajo `_`). Revisa si TANTO el remitente como el destinatario ya borraron el archivo de sus correspondientes papeleras lógicas. Si nadie lo conserva, entonces sí borra la fila mediante un `DELETE FROM` de la tabla real de la BD para cuidar el espacio.
- **`obtener_mensajes_recibidos(usuario_id)`** / **`obtener_mensajes_enviados(usuario_id)`**: Hacen consultas SQL con la instrucción `JOIN` combinando la tabla `Mensajes` y `Correos`. El objetivo del `JOIN` es que en vez de devolver el ID del destinatario, obtenga automáticamente su correo o nombre de verdad, y filtra los eliminados con `WHERE ... eliminado_destinatario = 0`.
- **`eliminar_mensaje(mensaje_id, usuario_id)`**: Es un "borrado lógico". No hace `DELETE`, sino un `UPDATE` que prende la "bandera" (cambia un campo 0 por un 1) del valor `eliminado_remitente` o `eliminado_destinatario`. Actúa como envío a "Papelera".
- **`guardar_borrador(...)`** y **`actualizar_borrador(...)`**: Guardan un mensaje pero le imponen la etiqueta manual de `tipo = 'borrador'`. Actualizar usa `UPDATE` al registro previamente editado.
- **`obtener_papelera(usuario_id)`**: Es una consulta masiva usando `UNION ALL`, la cual extrae filas de 3 casos diferentes: Los enviados borrados, los recibidos borrados y los borradores borrados, empalmándolos en una sola lista unificada final.

## Archivo: `UI.py`
Contiene la interfaz construida usando el paradigma de Programación Orientada a Objetos.

### 1. `cargar_imagen(nombre_archivo, size)`
- **Requerimientos**: La librería `PIL (Pillow)` y la ruta que se obtiene de `app_utils.py`.
- **Funcionalidad**: Carga imágenes JPG/PNG y las transforma en instancias `CTkImage` propias de CustomTkinter. Usa bloques de seguridad `try-except` para evitar crasheos si faltan los archivos de imagen.

### 2. Clase `AppCorreos(CTk)`
Esta clase actúa como el "Molde" de nuestra aplicación. Al heredar de `CTk` (CustomTkinter principal), la clase se convierte a sí misma literalmente en la ventana madre, es por eso que dentro usa `self.geometry(...)` en lugar de una variable separada.
- **`__init__(self, ...)`**: Es la función "Constructora". Se ejecuta automáticamente apenas abre la app. Recibe variables de `login.py` e inicializa las opciones como `self.usuario_id`, así la aplicación nunca pierde la identidad de quien la está usando sin usar variables globales desorganizadas. Llama a la estructuración UI principal con `self.configurar_ui()`.
- **`configurar_ui(self)`**: Construye el primer bloque visual principal y fijo usando sistema de columnas (`grid`). Define `self.Fila` (Banner superior arriba del todo) y `self.Pilar` (barra izquierda delgada para botones). Genera dentro de `self.Msj` un gran marco que aloja un panel infinito con scroll (`self.Contenedor_Msj`).
- **`configurar_ventanas_secundarias(self)`**: Dibuja los marcos de "Redactar" y "Contactos". Los dibuja pero acto seguido llama a `place_forget()`. Ese código esencialmente esconde la UI instantáneamente para que solo salga a la vista cuando alguien de clic.
- **`configurar_botones(self)`**: Toma las imágenes cargadas, genera los `CTkButton` en forma de bloque lateral y amarra cada botón a su respectiva función mediante el parámetro dinámico `command=...`.

### 3. Métodos Auxiliares/Helpers
- **`limpiar_contenedor_mensajes(self)`**: Hace un bucle para ubicar todos los widgets antiguos en pantalla y llama a `.destroy()` que es el método nativo para borrar elementos de pantalla en la RAM y liberar el plano vacío antes de mostrar nuevos datos.
- **`crear_tarjeta_mensaje`** y **`agregar_texto_tarjeta`**: Automatizan la escritura instanciando un mini-frame con color asignado para contener correos, ahorrándose el trabajo de diseñar el widget de Tkinter paso por paso.

### 4. Métodos "Consumidores" Visuales (mostrar_...)
- **`mostrar_mensajes_recibidos(self)` (Y similares, papelera, borradores)**: 
   1. Ocultan todo tipo de ventanas con `self.cerrar_panel_...`.
   2. Limpian los restos pasados (`self.limpiar_contenedor_mensajes()`).
   3. Consultan las funciones en `Funciones.py` inyectando sus variables `self`.
   4. Si la base de datos devuelve una lista, aplican un `for` que va pintando un frame gráfico por cada mensaje. Adicionalmente amarra el botón al comando `lambda id=mensaje_id: self.mover...` logrando así direccionar cuál ventana se presiona.

### 5. Métodos de Acción Física e Inputs de Texto
- **`toggle_redactar(self)`**: Analiza el "Estado" comprobando la variable `self.frame_visible`. Si es falso, oculta todo y usa `.place(...)` para emerger el cuadro de redacción en el centro. Si es verdadero, simplemente hace el trayecto inverso con `.place_forget()`.
- **`enviar_desde_ui(self)`**: 
  - Utiliza las capacidades de los `CTkEntry` obteniendo texto con el comando `get()` y los procesa con `.strip()` (limpia espacios en blanco ignorados). 
  - Valida alertas con herramientas visuales como los de `messagebox.showerror` (si un texto fue vacío).
  - Al fin mandar el texto a `enviar_mensaje()`, limpia los boxes de texto y llama el panel para refrescar la orden generada.
