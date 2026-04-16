import json
import os
import smtplib
import ssl
from email.message import EmailMessage

from app_utils import CONFIG_FILENAME, get_app_data_dir, get_base_dir

DEFAULT_SMTP_CONFIG = {
    "host": "",
    "port": 587,
    "username": "",
    "password": "",
    "from_email": "",
    "sender_name": "",
    "use_tls": True,
    "use_ssl": False,
}


def _to_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "si", "on"}


def _to_int(value, default=587):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _config_paths():
    return [
        os.path.join(get_app_data_dir(), CONFIG_FILENAME),
        os.path.join(get_base_dir(), CONFIG_FILENAME),
    ]


def _load_raw_config():
    for path in _config_paths():
        if not os.path.exists(path):
            continue

        try:
            with open(path, "r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        except (OSError, ValueError, json.JSONDecodeError):
            continue

        if isinstance(data, dict):
            return data, path

    return {}, _config_paths()[0]


def load_smtp_config():
    config_data, _ = _load_raw_config()
    smtp_data = config_data.get("smtp", {}) if isinstance(config_data, dict) else {}

    merged = dict(DEFAULT_SMTP_CONFIG)
    if isinstance(smtp_data, dict):
        merged.update(smtp_data)

    env_overrides = {
        "host": os.getenv("SMTP_HOST"),
        "port": os.getenv("SMTP_PORT"),
        "username": os.getenv("SMTP_USER"),
        "password": os.getenv("SMTP_PASSWORD"),
        "from_email": os.getenv("SMTP_FROM"),
        "sender_name": os.getenv("SMTP_SENDER_NAME"),
        "use_tls": os.getenv("SMTP_USE_TLS"),
        "use_ssl": os.getenv("SMTP_USE_SSL"),
    }

    for key, value in env_overrides.items():
        if value is not None and str(value).strip() != "":
            merged[key] = value

    merged["port"] = _to_int(merged.get("port"), 587)
    merged["use_tls"] = _to_bool(merged.get("use_tls"), True)
    merged["use_ssl"] = _to_bool(merged.get("use_ssl"), False)

    for key in ("host", "username", "password", "from_email", "sender_name"):
        merged[key] = str(merged.get(key, "")).strip()

    if merged["use_ssl"]:
        merged["use_tls"] = False

    return merged


def save_smtp_config(smtp_config):
    config_data, target_path = _load_raw_config()
    if not isinstance(config_data, dict):
        config_data = {}

    normalized = dict(DEFAULT_SMTP_CONFIG)
    normalized.update(smtp_config or {})

    normalized["host"] = str(normalized.get("host", "")).strip()
    normalized["port"] = _to_int(normalized.get("port"), 587)
    normalized["username"] = str(normalized.get("username", "")).strip()
    normalized["password"] = str(normalized.get("password", "")).strip()
    normalized["from_email"] = str(normalized.get("from_email", "")).strip()
    normalized["sender_name"] = str(normalized.get("sender_name", "")).strip()
    normalized["use_tls"] = _to_bool(normalized.get("use_tls"), True)
    normalized["use_ssl"] = _to_bool(normalized.get("use_ssl"), False)

    if normalized["use_ssl"]:
        normalized["use_tls"] = False

    config_data["smtp"] = normalized

    target_dir = os.path.dirname(target_path)
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)

    with open(target_path, "w", encoding="utf-8") as config_file:
        json.dump(config_data, config_file, ensure_ascii=True, indent=2)


def smtp_configurado(smtp_config):
    return all(
        str(smtp_config.get(key, "")).strip()
        for key in ("host", "username", "password")
    ) and _to_int(smtp_config.get("port"), 0) > 0


def enviar_correo_smtp(destinatario, asunto, contenido, smtp_config, reply_to=None):
    if not smtp_configurado(smtp_config):
        raise ValueError("SMTP no esta configurado completamente.")

    host = smtp_config["host"]
    port = _to_int(smtp_config.get("port"), 587)
    username = smtp_config["username"]
    password = smtp_config["password"]
    from_email = smtp_config.get("from_email") or username
    sender_name = smtp_config.get("sender_name", "").strip()
    use_tls = _to_bool(smtp_config.get("use_tls"), True)
    use_ssl = _to_bool(smtp_config.get("use_ssl"), False)

    if use_ssl:
        use_tls = False

    mensaje = EmailMessage()
    mensaje["From"] = f"{sender_name} <{from_email}>" if sender_name else from_email
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    if reply_to:
        mensaje["Reply-To"] = reply_to
    mensaje.set_content(contenido)

    timeout_seconds = 30
    ssl_context = ssl.create_default_context()

    if use_ssl:
        with smtplib.SMTP_SSL(host, port, timeout=timeout_seconds, context=ssl_context) as server:
            server.login(username, password)
            server.send_message(mensaje)
        return

    with smtplib.SMTP(host, port, timeout=timeout_seconds) as server:
        server.ehlo()
        if use_tls:
            server.starttls(context=ssl_context)
            server.ehlo()
        server.login(username, password)
        server.send_message(mensaje)
