import os
from getpass import getpass
from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired

USERNAME = os.getenv("IG_USERNAME") or input("Tu usuario IG: ")
PASSWORD = os.getenv("IG_PASSWORD") or getpass("Tu contraseña IG: ")
SESSION_FILE = "session.json"

cl = Client()
print("Iniciando sesión...")

try:
    cl.login(USERNAME, PASSWORD)
except TwoFactorRequired:
    print("Se requiere verificación de dos pasos (2FA).")
    two_factor_code = input("Tu código 2FA (Authenticator o SMS): ")
    # ⚠️ IMPORTANTE: cambia "verification_method" según tu caso:
    # 1 = SMS/WhatsApp, 2 = Authenticator App
    cl.login(
        USERNAME,
        PASSWORD,
        verification_code=two_factor_code,
        verification_method="2"  # Usa "1" si recibes código por SMS/WhatsApp
    )

# Guardar la sesión
cl.dump_settings(SESSION_FILE)
print("✅ Sesión guardada en", SESSION_FILE)