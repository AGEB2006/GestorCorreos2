# Guía de Estudio Detallada: Versión Modularizada

En la versión de Programación Orientada a Objetos existía mucho código visual repetitivo entre apartados (Se repetía línea sobre línea las propiedades estéticas y espaciales al crear tarjetas para "Recibidos", "Borradores" o "Enviados"). 
Esta carpeta soluciona el código masivo central usando la **Arquitectura Modular basada en Componentes**, respaldándose fuertemente en el principio informático **DRY (Don't Repeat Yourself - No te repitas)**.

## Archivo: `Componentes.py`
Este archivo NO es una aplicación auto-ejecutable y no tiene función `main`. Su único rol es forjar "widgets personalizados" armados o mini piezas de un set de legos global de la UI en la que todos pueden acceder.
- **Requiere**: Importa CustomTkinter y requiere ser instanciado con un contenedor raíz (`master`).

### 1. Clase `TarjetaMensaje(CTkFrame)`
Éste componente de clase absorbe la carga monumental que solía ser generar frames dinámicos incrustados. Esta clase es el Widget "Estandarizado y Reutilizable".
- **Requisitos en Parámetros**: Requiere el `master` para saber donde empaquetarse. El código Hexadecimal de color (`bg_color`). El string o variables f string combinadas `texto` para acomodar la información cruda del correo y la variable vital `botones_info` (la lista opcional de atributos del botón individual).
- **Cómo interactúa el Código Constructor (`__init__`)**:
  - Ejecuta a su padre `super()` forjándose sobre Tkinter con curvas integradas `corner_radius=10`.
  - Ordena de forma automática en una línea su propio posicionado interno usando un `self.pack(...)` empujando los elementos hacia alinearse al este ("e").
  - Coloca internamente su Label genérico previniendo texto infinito por fuera dictando los limites de tope por `wraplength`.
  - **La Magia Creadora Iterativa de Botones**: Evalúa si el que lo llamó incluyó la tupla opcional `botones_info`. Si esta existe se lee, se desenvuelve el contenido y arranca un for iterativo dinámico que inyecta en línea horizontal tantos botones se ocupen (`for index, (txt, bg, hover, width, cmd)...`) creando instancias de `CTkButton`. Manda y configura los colores e inclina sus características propias separando comandos individuales asíncronos. 

### 2. Clase `PanelInfo(CTkFrame)`
Cumple un acomodo análogo en simplificación al marco descrito previamente pero carece radicalmente de dinámicas accionales o botones. Es únicamente un rectángulo gráfico con características universales para plasmar a un usuario que una lista de una consulta de un arreglo vacío (Ejemplo: Buscar en papelera y que haya 0 items).

## Archivo: `UI.py` (AppCorreosV2)
Este código importa los "componentes legos" anteriores usando `from Componentes import TarjetaMensaje` dejando que resuelvan la visualización compleja.

### La Estructura Limpia en Archivo Principal
- **`configurar_estructura()` y `configurar_paneles()`**: Levanta los lienzos en blanco estáticos, barra superior `Fila`, Menú lateral `Pilar` y un contendor inagotable `Contenedor_Msj`. 
- **`configurar_botones(self)`**: En la versión anterior se solicitaban explícitamente 10 bloques masivos dictando los atributos de Tkinter en cada uno para el Layout de UI del pilar secundario. Ahora generamos matrices o listas (`botones_ui` que contiene las recetas: Titulo, Imagen y qué método detonan). Con un único ciclo `for` empaquetan, inyectando código y levantando las ayudas dinámicas en la variable emergente `Tooltip`.

### Vistas Dinámicas y Eficientes (`mostrar_mensajes...`)
La aplicación verdadera que le da valides radical a la creación de `Componentes.py` en paralelo. En cada pantalla del buzón ahora, este archivo ya no administra ni programa las variables físicas (No se preocupa de la posición lateral, ni del color fuente, ni del Padding interno de la UI, esa tarea es del constructor componente externo). Actúa consumiendo datos bajo el patrón:
1. `vaciar_contenedor`: Llama al método encargado de liberar un `destroy()` sobre los hijos visuales ya listados.
2. Inyecta comunicación DB de `Funciones.py`.
3. Validadores en Seco: Usa un bloque validador if verificando si el arreglo devolvió False/Empty y en una corta línea usa a `PanelInfo()`
4. Relleno Componente (Iteraciones): Al detectar correos entra a un `for` regular listando la fila:
   - Genera matriz/receta `botones` y la transfiere por la invocación del objeto `TarjetaMensaje`.
   ```python
   # Un botón de 140 width, con fondo rojo rubí y que llama a "self.borrar_vista"
   botones = [("Enviar a papelera", "#8B1E1E", "#6F1818", 140, lambda mid=mensaje_id: self.borrar_vista(mid))]
   
   # La instanciación ultra delgada en una sola línea del Frontend actual
   TarjetaMensaje(
       self.Contenedor_Msj, "#3B3B3B", 
       f"De: {remitente}... 
\n{fecha}", 
       botones
   )
   ```
- **Conclusión y Motivo del Beneficio de POO Compartido**: Modularizando conseguimos separar fuertemente la "Capa de UI de Presentación" de las capas "De Integración Funcional". Esto da origen al Patrón de la Industria al forzar separacion de interes `(Separation of concerns)`. Si la marca de colores de todo el sistema se vuelve púrpura claro, solamente se abre al "Componente", afectando uniformemente múltiples vistas y protegiendo el código delicado y pesado del back-end de bugs producidos por editar atributos gráficos.
