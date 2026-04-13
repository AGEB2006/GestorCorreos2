import os
import json
import shutil
import subprocess
import sys


def is_frozen():
    return getattr(sys, "frozen", False)


def get_base_dir():
    if is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", get_base_dir())
    return os.path.join(base_path, relative_path)


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


def get_database_path(filename="BaseDeDatos.db"):
    target_path = os.path.join(get_app_data_dir(), filename)

    if os.path.exists(target_path):
        return target_path

    candidate_paths = [
        os.path.join(get_base_dir(), filename),
        resource_path(filename),
    ]
    for candidate_path in candidate_paths:
        if candidate_path != target_path and os.path.exists(candidate_path):
            shutil.copyfile(candidate_path, target_path)
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
