# Explicacion de conceptos en UI.py

Este documento resume los conceptos de programacion presentes en el archivo UI.py, con ejemplos y consejos para aprenderlos mejor.

## 1) Modularidad e importaciones
UI.py importa funciones y clases desde otros modulos para separar responsabilidades:

- `Funciones`: logica de mensajes, borradores y papelera.
- `bd`: acceso a contactos y usuarios.
- `app_utils`: utilidades comunes.
- `Clases`: componentes personalizados como `Tooltip`.
- `customtkinter` y `tkinter`: interfaz grafica.

Ejemplo:

```python
from Funciones import obtener_mensajes_recibidos
```

Tip: cuando leas un archivo, identifica que responsabilidades se delegan a otros modulos y que queda en el archivo principal.

## 2) Funciones y alcance (scope)
Se definen muchas funciones dentro de `main()`. Esto permite que esas funciones accedan a variables de la UI sin tener que pasarlas como parametros.

Ejemplo:

```python
def mostrar_mensajes_recibidos():
    mensajes = obtener_mensajes_recibidos(int(usuario_id))
```

Tip: practica con funciones anidadas y analiza que variables vienen del alcance externo.

## 3) Variables de estado y `nonlocal`
Se usa `nonlocal` para modificar variables de `main()` desde funciones internas. Esto es util para mantener estado de la UI.

Ejemplo:

```python
borrador_actual_id = None
frame_visible = False

def cargar_borrador_en_redactor(borrador_id):
    nonlocal frame_visible, borrador_actual_id#####
```

Tip: dibuja un diagrama simple de estado (por ejemplo, "redactor visible" y "borrador actual") y actualizalo mentalmente al leer el codigo.

## 4) Programacion orientada a eventos (GUI)
La interfaz se basa en eventos: botones que ejecutan funciones cuando el usuario hace clic.

Ejemplo:

```python
Boton_Recibido.configure(command=mostrar_mensajes_recibidos)
```

Tip: localiza los `command=...` para entender el flujo real de la aplicacion.

## 5) Widgets y composicion de UI
Se crean frames, labels, botones y contenedores scrollables. La UI se arma como un arbol de componentes.

Ejemplo:

```python
Msj = CTkFrame(Ventana)
Contenedor_Msj = CTkScrollableFrame(Msj)
```

Tip: relaciona cada widget con su padre inmediato para entender su ubicacion.

## 6) Layout: `grid`, `pack` y `place`
El archivo combina diferentes gestores de geometria:

- `grid` para la estructura principal.
- `pack` para listas verticales.
- `place` para paneles flotantes.

Ejemplo:

```python
Fila.grid(row=0, column=0, columnspan=2, sticky="nsew")
menu_lateral.pack(fill="x")
frame_redactar.place(relx=0.5, rely=0.5, anchor="center")
```

Tip: si un widget no se ve, revisa primero el gestor de geometria y el contenedor.

## 7) Manejo de listas dinamicas (crear y limpiar)
Para refrescar contenido, se destruyen widgets previos y se crean nuevos.

Ejemplo:

```python
for widget in Contenedor_Msj.winfo_children():
    widget.destroy()
```

Tip: cuando renderizas listas, separa en funciones: limpiar, crear tarjeta, agregar texto, agregar acciones.

## 8) Validacion de entradas
Antes de ejecutar acciones, se valida que los campos no esten vacios o que el usuario exista.

Ejemplo:

```python
if not destinatario or not asunto or not contenido:
    messagebox.showwarning("Campos vacios", "Completa destinatario, asunto y mensaje.")
```

Tip: usa mensajes de error claros y valida temprano ("fail fast").

## 9) Control de flujo y estados de paneles
Se ocultan y muestran paneles con `place_forget()` y banderas como `frame_visible`.

Ejemplo:

```python
frame_redactar.place_forget()
frame_visible = False
```

Tip: centraliza los cambios de estado para evitar errores por inconsistencias.

## 10) Uso de imagenes y recursos
`cargar_imagen()` busca recursos empaquetados y valida que `ImageTk` este disponible.

Ejemplo:

```python
ruta = resource_path(nombre_archivo)
if os.path.exists(ruta):
    imagen = Image.open(ruta)
```

Tip: cuando uses archivos externos, maneja excepciones para evitar caidas de la app.

## 11) Manejo de errores y feedback al usuario
Se usan `messagebox.showinfo`, `showwarning` y `showerror` para comunicar resultados.

Ejemplo:

```python
messagebox.showinfo("Mensaje enviado", "El mensaje interno se guardo correctamente.")
```

Tip: cada accion importante deberia tener feedback claro y breve.

## 12) Lambdas y cierres (closures)
Se pasan argumentos a callbacks usando `lambda` para capturar IDs.

Ejemplo:

```python
command=lambda mid=mensaje_id: mover_mensaje_a_papelera(mid)
```

Tip: usa nombres claros en los parametros de la lambda para evitar confusiones.

## 13) Conversión y validacion de tipos
Se convierte `usuario_id` a `int` solo si es digito.

Ejemplo:

```python
mensajes = obtener_mensajes_recibidos(int(usuario_id)) if str(usuario_id).isdigit() else []
```

Tip: valida datos de entrada si vienen de la linea de comandos o archivos.

## 14) Punto de entrada del programa
El archivo tiene un bloque para ejecutar la app si se llama directamente.

Ejemplo:

```python
if __name__ == "__main__":
    main(usuario_id, nombre_usuario, correo_usuario)
```

Tip: este patron permite importar `main()` desde otros modulos sin ejecutar la UI.

## 15) Separacion de capas (UI vs logica)
La UI llama a funciones de negocio (borradores, mensajes, contactos) sin duplicar la logica.

Ejemplo:

```python
guardar_borrador(int(usuario_id), asunto, contenido)
```

Tip: mantener la logica fuera de la UI facilita pruebas y mantenimiento.

---

## Consejos para aprender mejor

1. Lee el archivo por secciones: inicio (imports), layout, callbacks, final.
2. Haz un mapa de pantallas: recibidos, enviados, borradores, papelera, contactos, cuenta.
3. Traza el flujo al dar click en cada boton (que funcion se ejecuta y que cambia).
4. Prueba cambios pequenos: por ejemplo, cambia un color o un texto y observa el efecto.
5. Anota dudas de funciones externas y abre los archivos importados para completar el mapa mental.

## Mini ejercicios sugeridos

1. Agrega un contador de mensajes recibidos en la barra superior.
2. Crea un boton para refrescar bandeja de entrada sin cambiar de panel.
3. Resalta en color distinto los mensajes sin asunto.
4. Agrega validacion para no permitir destinatarios con espacios.
5. Crea un tip (Tooltip) adicional en el boton de "Papelera".
