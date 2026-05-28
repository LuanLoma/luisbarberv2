import os
import smtplib
import socket
import threading  # <-- ADICIÓN: Para correr el envío en segundo plano
from email.message import EmailMessage
from dotenv import load_dotenv

# --- FUERZA LA RUTA ABSOLUTA DEL ARCHIVO .ENV ---
base_dir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(base_dir, '.env')

if not os.path.exists(env_path):
    env_path = os.path.join(base_dir, '..', '.env')

load_dotenv(dotenv_path=env_path)
# ------------------------------------------------


def _ejecutar_envio_async(email, server, port, user, password):
    """Función interna que corre en segundo plano sin trabar a Flask"""
    try:
        # Intentamos resolver por IPv4 dinámico
        direcciones = socket.getaddrinfo(server, int(port), socket.AF_INET, socket.SOCK_STREAM)
        ip_ipv4 = direcciones[0][4][0]
        
        # Conexión con un timeout corto de 8 segundos
        with smtplib.SMTP_SSL(ip_ipv4, int(port), timeout=8) as smtp:
            smtp.login(user, password)
            smtp.send_message(email)
            print(" [SMTP Async] Correo enviado con éxito en segundo plano.")
    except Exception as e:
        # Se queda registrado en los logs de Render, pero ya no tumba la petición HTTP
        print(f" [SMTP Async Error] No se pudo mandar el correo en segundo plano: {e}")


def _enviar(subject, contenido, destinatario=None):
    user = os.getenv("MAIL_USER")
    password = os.getenv("MAIL_PASSWORD")
    server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    port = os.getenv("MAIL_PORT", "465")

    if not user or not password:
        print(" [SMTP Error] Falta configuración de credenciales de correo.")
        return

    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = user
    
    if isinstance(destinatario, (list, tuple)):
        email["To"] = ", ".join(destinatario)
    else:
        email["To"] = destinatario or os.getenv("MAIL_TO", user)
        
    email.set_content(contenido)

    # --- TRUCO MAESTRO: DISPARAR HILO EN SEGUNDO PLANO ---
    # Creamos un hilo independiente para que Flask continúe su camino de inmediato
    hilo_correo = threading.Thread(
        target=_ejecutar_envio_async, 
        args=(email, server, port, user, password)
    )
    hilo_correo.daemon = True  # Permite que el hilo muera si el servidor principal se apaga
    hilo_correo.start()
    print(" [SMTP] El envío se delegó a un hilo en segundo plano de forma exitosa.")


def enviar_correo_contacto(nombre, correo, mensaje):
    _enviar(
        "Nuevo mensaje para Luis Barber",
        f"""Nuevo mensaje recibido desde el formulario de contacto.

Nombre: {nombre}
Correo: {correo}

Mensaje:
{mensaje}
""",
    )


def enviar_correo_cita(data, servicio):
    contenido = f"""Cita registrada en Luis Barber.

Cliente: {data.get("cliente")}
Telefono: {data.get("telefono")}
Correo: {data.get("correo")}
Servicio: {servicio.get("nombre")}
Precio: ${servicio.get("precio")}
Fecha: {data.get("fecha")}
Hora: {data.get("hora")}

Comentarios:
{data.get("comentarios", "Sin comentarios")}
"""
    correo_barbero = os.getenv("MAIL_TO") or os.getenv("MAIL_USER")
    correo_cliente = data.get("correo")
    
    destinatarios = [correo_cliente, correo_barbero]
    _enviar("Confirmacion de cita - Luis Barber", contenido, destinatarios)