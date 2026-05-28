import os
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

# Aseguramos la ruta absoluta del .env sin importar desde dónde corras el script
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Si no lo encuentra en la raíz del backend, busca un nivel arriba por si acaso
if not ENV_PATH.exists():
    ENV_PATH = BASE_DIR.parent / ".env"

load_dotenv(dotenv_path=ENV_PATH)

def get_connection():
    # Valores de emergencia por si os.getenv devuelve None
    host_db = os.getenv("DB_HOST") or "127.0.0.1"
    port_db = int(os.getenv("DB_PORT") or 3306)
    user_db = os.getenv("DB_USER") or "root"
    pass_db = os.getenv("DB_PASSWORD") or ""  # Vacío si tu phpMyAdmin local no ocupa clave
    name_db = os.getenv("DB_NAME") or "luis_barber"

    return mysql.connector.connect(
        host=host_db,
        port=port_db,
        user=user_db,
        password=pass_db,
        database=name_db,
        connect_timeout=5  # Rompe el bucle si la BD se congela o apaga
    )