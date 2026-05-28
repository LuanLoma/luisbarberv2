import os
import requests  # <-- Asegúrate de que esté en tu requirements.txt si no lo tenías
from dotenv import load_dotenv

# --- FUERZA LA RUTA ABSOLUTA DEL ARCHIVO .ENV ---
base_dir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(base_dir, '.env')

if not os.path.exists(env_path):
    env_path = os.path.join(base_dir, '..', '.env')

load_dotenv(dotenv_path=env_path)
# ------------------------------------------------

def _enviar(subject, contenido, destinatario=None):
    api_key = os.getenv("RESEND_API_KEY")
    # Resend en su plan gratis te obliga a usar este remitente verificado por defecto
    from_email = "onboarding@resend.dev" 
    
    if not api_key:
        print(" [Resend Error] Falta configurar la variable RESEND_API_KEY.")
        return

    # Si es una lista de correos, los convertimos a una lista real para el JSON de Resend
    if isinstance(destinatario, (list, tuple)):
        # Resend en plan gratis solo deja mandar correos a TI mismo (tu cuenta de registro)
        # Para pruebas, lo ideal es mandar todo al correo administrador configurado
        to_emails = [os.getenv("MAIL_TO") or os-getenv("MAIL_USER")]
    else:
        to_emails = [destinatario or os.getenv("MAIL_TO")]

    # Armamos la petición HTTP POST para saltarnos el bloqueo SMTP de Render
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": f"Luis Barber <{from_email}>",
        "to": to_emails,
        "subject": subject,
        "text": contenido
    }

    try:
        # Petición HTTP directa por el puerto 443 (Abierto en todo internet)
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code in [200, 201]:
            print(" [Resend] ¡CORREO ENVIADO CON ÉXITO MEDIANTE API HTTP! 🎉")
        else:
            print(f" [Resend Error] El servicio rechazó el correo: {response.text}")
    except Exception as e:
        print(f" [Resend Exception] Falló la conexión HTTP con la API: {e}")


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
    # Formateamos el contenido con los datos que puso el cliente en la página
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
    
    # MODIFICACIÓN DE ORO: 
    # Forzamos a que el destinatario sea TU correo verificado de Resend.
    # Así te llegará la notificación con toda la info del cliente a ti, 
    # y Resend no te tirará el error 403.
    correo_destino = "luanloma13@gmail.com"
    
    # Se invoca la función pasando tu correo como único destino
    _enviar(f"Confirmacion de cita - {data.get('cliente')}", contenido, correo_destino)