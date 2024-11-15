from cryptography.fernet import Fernet
import os
import json
from datetime import datetime

class LocalAuditTrail:
    def __init__(self, log_file="audit_log.txt", key_file="audit_key.key"):
        self.log_file = log_file
        self.key_file = key_file
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)

    def load_or_generate_key(self):
        """Genera o carga la clave de encriptación."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
            return key

    def log_action(self, user, action):
        """Registra una acción."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"user": user, "action": action, "timestamp": timestamp}

        # Encripta la entrada del log
        encrypted_entry = self.fernet.encrypt(json.dumps(log_entry).encode())

        # Guarda la entrada en el archivo
        with open(self.log_file, "ab") as log:
            log.write(encrypted_entry + b"\n")

    def read_logs(self):
        """Desencripta y muestra los logs almacenados."""
        if not os.path.exists(self.log_file):
            print("No hay registros de auditoría.")
            return

        with open(self.log_file, "rb") as log:
            for line in log:
                try:
                    decrypted_entry = self.fernet.decrypt(line.strip()).decode()
                    print(json.loads(decrypted_entry))
                except Exception as e:
                    print(f"Error al leer una entrada del log: {e}")
