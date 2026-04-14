import os
import json
import shutil
import subprocess
import sys
import tkinter as tk

from PIL import Image, ImageTk


CONFIG_FILENAME = "app_config.json"


def is_frozen():
    return getattr(sys, "frozen", False)


def get_base_dir():
    if is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", get_base_dir())
    return os.path.join(base_path, relative_path)


def poner_fondo_imagen(ventana, ruta, bg_color="#111111"):
    ruta_resuelta = resource_path(ruta)
    if not os.path.exists(ruta_resuelta):
        return

    try:
        imagen_original = Image.open(ruta_resuelta).convert("RGBA")
    except Exception:
        return

    fondo = tk.Label(ventana, bd=0, highlightthickness=0, bg=bg_color)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    fondo.lower()

    def actualizar_fondo(_event=None):
        ancho = max(1, ventana.winfo_width())
        alto = max(1, ventana.winfo_height())
        imagen = imagen_original.resize((ancho, alto), Image.LANCZOS)
        try:
            fondo_actual = ImageTk.PhotoImage(imagen)
        except Exception:
            fondo.configure(image="")
            fondo.image = None
            return

        fondo.configure(image=fondo_actual)
        fondo.image = fondo_actual

    ventana.bind("<Configure>", actualizar_fondo, add="+")
    ventana.update_idletasks()
    actualizar_fondo()


def get_app_data_dir():
    candidate_dirs = []

    local_appdata = os.getenv("LOCALAPPDATA")
    if local_appdata:
        candidate_dirs.append(os.path.join(local_appdata, "GestorCorreos2"))

    candidate_dirs.append(os.path.join(os.path.expanduser("~"), "GestorCorreos2"))
    candidate_dirs.append(get_base_dir())

    for app_dir in candidate_dirs:
        try:
            os.makedirs(app_dir, exist_ok=True)
            return app_dir
        except OSError:
            continue

    return get_base_dir()


def _normalizar_ruta_base_datos(configured_path, filename):
    ruta = os.path.expandvars(os.path.expanduser((configured_path or "").strip()))
    if not ruta:
        return None

    ruta = ruta.strip('"')
    _, extension = os.path.splitext(ruta)
    if extension.lower() not in {".db", ".sqlite", ".sqlite3"}:
        ruta = os.path.join(ruta, filename)

    if not os.path.isabs(ruta):
        ruta = os.path.abspath(os.path.join(get_base_dir(), ruta))

    return ruta


def _obtener_ruta_base_datos_configurada(filename):
    env_path = os.getenv("GESTOR_CORREOS_DB_PATH")
    ruta_env = _normalizar_ruta_base_datos(env_path, filename)
    if ruta_env:
        return ruta_env

    config_paths = [
        os.path.join(get_base_dir(), CONFIG_FILENAME),
        os.path.join(get_app_data_dir(), CONFIG_FILENAME),
    ]

    for config_path in config_paths:
        if not os.path.exists(config_path):
            continue

        try:
            with open(config_path, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)
        except (OSError, ValueError, json.JSONDecodeError):
            continue

        if not isinstance(config, dict):
            continue

        configured_path = config.get("database_path") or config.get("db_path")
        ruta_config = _normalizar_ruta_base_datos(configured_path, filename)
        if ruta_config:
            return ruta_config

    return None


def _ruta_base_datos_disponible(db_path):
    parent_dir = os.path.dirname(db_path)
    if parent_dir:
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except OSError:
            return False

    if os.path.exists(db_path):
        try:
            with open(db_path, "ab"):
                pass
        except OSError:
            return False
        return True

    if parent_dir and not os.path.isdir(parent_dir):
        return False

    if parent_dir and not os.access(parent_dir, os.W_OK):
        return False

    return True


def get_database_path(filename="BaseDeDatos.db"):
    configured_path = _obtener_ruta_base_datos_configurada(filename)
    if configured_path and _ruta_base_datos_disponible(configured_path):
        if not os.path.exists(configured_path):
            candidate_paths = [
                os.path.join(get_base_dir(), filename),
                resource_path(filename),
            ]
            for candidate_path in candidate_paths:
                if candidate_path != configured_path and os.path.exists(candidate_path):
                    try:
                        shutil.copyfile(candidate_path, configured_path)
                    except OSError:
                        pass
                    break

        return configured_path

    if configured_path:
        print("[DB] Ruta compartida no disponible, se usara base local.")

    target_path = os.path.join(get_app_data_dir(), filename)

    if os.path.exists(target_path):
        return target_path

    candidate_paths = [
        os.path.join(get_base_dir(), filename),
        resource_path(filename),
    ]
    for candidate_path in candidate_paths:
        if candidate_path != target_path and os.path.exists(candidate_path):
            try:
                shutil.copyfile(candidate_path, target_path)
            except OSError:
                pass
            break

    return target_path


def get_session_path(filename="session.json"):
    return os.path.join(get_app_data_dir(), filename)


def guardar_sesion(usuario):
    session_path = get_session_path()
    data = {
        "usuario_id": usuario["id"],
        "correo": usuario["correo"],
        "nombre": usuario["nombre"],
    }
    with open(session_path, "w", encoding="utf-8") as session_file:
        json.dump(data, session_file)


def cargar_sesion():
    session_path = get_session_path()
    if not os.path.exists(session_path):
        return None

    try:
        with open(session_path, "r", encoding="utf-8") as session_file:
            data = json.load(session_file)
    except (OSError, ValueError, json.JSONDecodeError):
        return None

    if not isinstance(data, dict):
        return None

    usuario_id = data.get("usuario_id")
    correo = data.get("correo")
    nombre = data.get("nombre")
    if usuario_id is None or not correo:
        return None

    return {
        "id": usuario_id,
        "correo": correo,
        "nombre": nombre or correo,
    }


def limpiar_sesion():
    session_path = get_session_path()
    if os.path.exists(session_path):
        os.remove(session_path)


def launch_mode(mode, *args):
    command = [sys.executable]

    if not is_frozen():
        command.append("login.py")

    command.append(mode)
    command.extend(str(arg) for arg in args)

    if is_frozen():
        # Replace the current process to avoid _MEIPASS temp-dir cleanup conflicts.
        os.execv(sys.executable, command)
        return

    subprocess.Popen(command, cwd=get_base_dir())
