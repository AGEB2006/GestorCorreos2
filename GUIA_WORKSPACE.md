# Guía del workspace

Este proyecto es una aplicación de escritorio hecha con Python y CustomTkinter para gestionar mensajes internos entre usuarios registrados. La app permite crear cuenta, iniciar sesión, recuperar contraseña, redactar mensajes, guardar borradores, administrar contactos y mover elementos a papelera.

## Estructura general

### Archivos principales

- `login.py`: punto de entrada de la app. Muestra la pantalla de inicio de sesión y decide si abre el panel principal, el registro o la recuperación de contraseña.
- `registro.py`: formulario para crear cuentas nuevas.
- `recuperar.py`: ventana para recuperar y cambiar la contraseña usando pregunta de seguridad.
- `UI.py`: panel principal de usuario. Aquí se ven mensajes recibidos, enviados, borradores, papelera, contactos y la cuenta.
- `Funciones.py`: lógica de alto nivel para mensajes y papelera. Usa la base de datos para enviar, guardar, actualizar, eliminar y restaurar mensajes.
- `bd.py`: capa de acceso a datos. Crea tablas, normaliza la base, hash de contraseñas, autenticación, usuarios, contactos y recuperación.
- `app_utils.py`: utilidades generales. Resuelve rutas, maneja fondos de imagen, configuración de base de datos, sesión persistente y reinicio del programa.
- `Clases.py`: contiene el componente `Tooltip` usado en la interfaz para mostrar ayudas al pasar el mouse.

### Archivos de configuración y datos

- `app_config.json.example`: ejemplo de configuración para indicar una ruta compartida de base de datos.
- `session.json`: archivo de sesión de ejemplo o antiguo que quedó en la raíz del proyecto. La app actual usa la sesión guardada en la carpeta local de usuario mediante `app_utils.py`.
- `login.spec`: configuración de PyInstaller para generar el ejecutable.
- `build/`: salida generada por PyInstaller. No es lógica del programa; se recrea al compilar.
- `.vscode/settings.json`: configuración local de VS Code para este workspace.

## Qué hace cada archivo

### `bd.py`

Es el núcleo de datos. Define la conexión SQLite y la tabla `Correos` para usuarios. También:

- crea y normaliza la estructura de la base de datos,
- guarda usuarios con contraseña cifrada con SHA-256,
- valida credenciales,
- recupera usuario por correo o por id,
- guarda y valida preguntas de seguridad,
- actualiza contraseñas,
- crea las tablas `Mensajes` y `Contactos`,
- migra columnas antiguas si faltan en la base,
- agrega y elimina contactos.

Además, al final del archivo se ejecuta la inicialización de tablas para que la base quede lista al importar el módulo.

### `Funciones.py`

Contiene la lógica operativa de mensajería:

- enviar mensajes,
- guardar borradores,
- actualizar borradores,
- leer mensajes recibidos y enviados,
- mover mensajes a papelera,
- restaurar elementos desde papelera,
- eliminar definitivamente,
- listar borradores y papelera.

En otras palabras, `bd.py` define la estructura y `Funciones.py` opera sobre los mensajes.

### `UI.py`

Es la interfaz principal después del login. Construye la ventana grande con:

- botón de redactar,
- panel de recibidos,
- panel de enviados,
- borradores,
- papelera,
- contactos,
- cuenta de usuario.

También conecta los botones con la lógica de `Funciones.py` y `bd.py`.

Flujo interno importante:

1. Abre la vista de mensajes recibidos al iniciar.
2. Permite redactar un mensaje interno a otro correo registrado.
3. Permite guardar o actualizar borradores.
4. Permite mover mensajes y borradores a papelera.
5. Permite restaurar o borrar definitivamente desde papelera.
6. Permite agregar o quitar contactos.
7. Permite cerrar sesión y volver al login.

### `login.py`

Es el arranque de la aplicación. Su responsabilidad es decidir qué pantalla mostrar:

- si ya existe una sesión válida, abre la interfaz principal,
- si no, muestra el login,
- desde el login permite ir al registro o a recuperación de contraseña.

También tiene una ruta especial para abrir directamente el panel principal cuando se llama con modo `ui`.

### `registro.py`

Muestra un formulario para registrar usuarios con:

- nombre,
- correo,
- teléfono,
- contraseña,
- confirmación de contraseña,
- pregunta de seguridad,
- respuesta de seguridad.

Valida campos vacíos y que ambas contraseñas coincidan. Luego llama a `bd.registrar`.

### `recuperar.py`

Abre una ventana secundaria para recuperar la contraseña:

- carga la pregunta de seguridad asociada al correo,
- verifica la respuesta del usuario,
- actualiza la contraseña en la base,
- rellena el login con la nueva contraseña para facilitar el acceso.

### `app_utils.py`

Centraliza utilidades del entorno:

- detecta si la app está empaquetada con PyInstaller,
- resuelve rutas de archivos dentro o fuera del ejecutable,
- busca la base de datos en una ruta configurada o en la carpeta local del usuario,
- copia una base existente si hace falta,
- guarda, carga y limpia la sesión en disco,
- abre la app en un modo específico.

También maneja el fondo de pantalla de las ventanas usando Pillow.

### `Clases.py`

Define `Tooltip`, un componente simple que muestra una ayuda visual cuando el cursor pasa sobre un botón.

## Flujo completo de uso

1. El programa empieza en `login.py`.
2. Si hay sesión guardada, se abre `UI.py` directamente.
3. Si no hay sesión, aparece el login.
4. Desde el login el usuario puede:
   - iniciar sesión,
   - crear una cuenta,
   - recuperar su contraseña.
5. Una vez dentro, la interfaz principal permite administrar mensajes y contactos.

## Archivos generados o secundarios

- `build/`: carpeta generada automáticamente al compilar con PyInstaller.
- `session.json` en la raíz: no es parte del flujo actual de sesión, pero puede servir como referencia de datos guardados.
- Base de datos: por defecto se maneja como `BaseDeDatos.db`, aunque la ruta puede cambiar según `app_config.json` o la variable de entorno `GESTOR_CORREOS_DB_PATH`.

## Observaciones rápidas

- La app está pensada como sistema de mensajería interno, no como cliente de correo real.
- La base de datos se adapta a cambios de esquema porque `bd.py` revisa columnas faltantes y las agrega.
- Las contraseñas no se guardan en texto plano para usuarios nuevos; se guardan con hash SHA-256.

## Resumen corto por archivo

- `login.py`: puerta de entrada.
- `registro.py`: alta de usuarios.
- `recuperar.py`: restablecimiento de contraseña.
- `UI.py`: panel principal.
- `Funciones.py`: operaciones sobre mensajes.
- `bd.py`: base de datos y autenticación.
- `app_utils.py`: rutas, sesión y utilidades.
- `Clases.py`: tooltip visual.
