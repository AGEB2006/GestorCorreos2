import os
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


def launch_mode(mode, *args):
    command = [sys.executable]

    if not is_frozen():
        command.append("login.py")

    command.append(mode)
    command.extend(str(arg) for arg in args)
    subprocess.Popen(command)
