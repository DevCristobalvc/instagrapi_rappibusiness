from instagrapi import Client
import sys
import json
import os

USERNAME = "TU_USUARIO"
PASSWORD = "TU_CONTRASEÑA"  # o usa input si no quieres dejarlo plano
SESSION_FILE = "session.json"

def get_client():
	cl = Client()
	if os.path.exists(SESSION_FILE):
		print("Cargando sesión desde archivo...")
		try:
			cl.load_settings(SESSION_FILE)
			cl.login(USERNAME, PASSWORD)  # refresca sesión con pass
			return cl
		except Exception as e:
			print("Error iniciando con session.json:", e)
	print("Iniciando nueva sesión...")
	cl.login(USERNAME, PASSWORD)
	cl.dump_settings(SESSION_FILE)
	return cl

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Uso: python send_dm.py <usuario> <mensaje>")
		sys.exit(1)
	username = sys.argv[1]
	message = " ".join(sys.argv[2:])
	cl = get_client()
	try:
		user_id = cl.user_id_from_username(username)
		cl.direct_send(message, [user_id])
		print(f"✅ Mensaje enviado a {username}: {message}")
	except Exception as e:
		print("❌ Error enviando mensaje:", e)