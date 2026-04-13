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


def get_database_path(filename="BaseDeDatos.db"):
    runtime_dir = get_base_dir()
    target_path = os.path.join(runtime_dir, filename)

    if os.path.exists(target_path):
        return target_path

    bundled_path = resource_path(filename)
    if bundled_path != target_path and os.path.exists(bundled_path):
        shutil.copyfile(bundled_path, target_path)

    return target_path


def get_session_path(filename="session.json"):
    return os.path.join(get_base_dir(), filename)


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
