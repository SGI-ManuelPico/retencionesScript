import tkinter as tk
from tkinter import messagebox
from gui.app_gui import AppGUI
from db import ConexionDB
import bcrypt
import os
from cryptography.fernet import Fernet
import json
from audit.audit_trail import LocalAuditTrail


class LoginGUI:
    def __init__(self):
        self.audit_trail = LocalAuditTrail()
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("300x250")
        self.window.configure(bg="#f4f4f4")
        self.fernet_key = b"GJw2x2Dic6T3MWAv5a_vNDxkxJRjh04Ku4O_OtwBiNs=" 
        self.fernet = Fernet(self.fernet_key)

        self.key = self.load_encryption_key() 
        self.credentials_file = "credentials.json"

        self.create_widgets()
        self.check_remembered_credentials()

    def create_widgets(self):

        tk.Label(self.window, text="Usuario:", bg="#f4f4f4", font=("Arial", 12)).pack(pady=10)
        self.username_entry = tk.Entry(self.window, font=("Arial", 12), width=25)
        self.username_entry.pack()


        tk.Label(self.window, text="Contraseña:", bg="#f4f4f4", font=("Arial", 12)).pack(pady=10)
        self.password_entry = tk.Entry(self.window, show="*", font=("Arial", 12), width=25)
        self.password_entry.pack()

        self.remember_me_var = tk.BooleanVar()
        tk.Checkbutton(
            self.window,
            text="Recuerdame",
            variable=self.remember_me_var,
            bg="#f4f4f4",
            font=("Arial", 10)
        ).pack(pady=10)

        # Login
        self.login_button = tk.Button(
            self.window,
            text="Iniciar sesión",
            font=("Arial", 12, "bold"),
            bg="#007bff",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            width=20,
            command=self.authenticate
        )
        self.login_button.pack(pady=20)

        # Add hover effect to buttons
        self.add_hover_effect(self.login_button)

    def add_hover_effect(self, button):
        """Add hover effect to a button."""
        button.bind("<Enter>", lambda e: button.config(bg="#0056b3"))
        button.bind("<Leave>", lambda e: button.config(bg="#007bff"))

    def load_encryption_key(self):
        key_file = "encryption.key"
        if not os.path.exists(key_file):

            key = Fernet.generate_key()
            with open(key_file, "wb") as key_file:
                key_file.write(key)
        else:

            with open(key_file, "rb") as key_file:
                key = key_file.read()
        return key

    def save_credentials(self, username, password):
        encrypted_username = Fernet(self.key).encrypt(username.encode()).decode()
        encrypted_password = Fernet(self.key).encrypt(password.encode()).decode()
        with open(self.credentials_file, "w") as file:
            json.dump({"username": encrypted_username, "password": encrypted_password}, file)

    def load_credentials(self):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, "r") as file:
                data = json.load(file)
                username = Fernet(self.key).decrypt(data["username"].encode()).decode()
                password = Fernet(self.key).decrypt(data["password"].encode()).decode()
                return username, password
        return None, None

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db_config = {
            "host": "srv1182.hstgr.io",
            "user": "u438914854_contabilidad",
            "password": "RI8aiyvVRs4MY80",
            "database": "u438914854_contabilidad"
        }

        conexion = ConexionDB(**db_config).establecerConexion() 
        try:
            cursor = conexion.cursor()

            # Toma la contraseña encriptada de la base de datos
            query = "SELECT password FROM usuarios WHERE correo = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if not result:
                self.audit_trail.log_action("Login", f"Usuario '{username}' no encontrado en la base de datos")
                messagebox.showerror("Error", "Usuario no encontrado")
                return

            # Esta es la contraseña encriptada almacenada en la base de datos
            encrypted_password = result[0]

            try:
                # Desencripta la contraseña almacenada en la base de datos
                decrypted_password = self.fernet.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')

                # Comparar la contraseña proporcionada con la contraseña desencriptada
                if password == decrypted_password:
                    if self.remember_me_var.get():
                        self.save_credentials(username, password)
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                    self.audit_trail.log_action("Login", f"Usuario '{username}' inició sesión correctamente")
                    self.window.destroy()
                    AppGUI(username, self.audit_trail).run()
                else:
                    self.audit_trail.log_action("Login", f"Usuario '{username}' ingresó una contraseña incorrecta")
                    messagebox.showerror("Error", "Contraseña incorrecta")

            except Exception as decrypt_err:
                self.audit_trail.log_action("Login",
                                            f"Error al desencriptar la contraseña para el usuario '{username}': {decrypt_err}")
                messagebox.showerror("Error", "No se pudo desencriptar la contraseña. Contacte al administrador.")

        except Exception as e:
            self.audit_trail.log_action("Login", f"Error en la autenticación para el usuario '{username}': {e}")
            messagebox.showerror("Error", f"Error al consultar la base de datos: {e}")

        finally:
            if conexion and conexion.is_connected():
                conexion.close()

    def check_remembered_credentials(self):
        username, password = self.load_credentials()
        if username and password:
            self.username_entry.insert(0, username)
            self.password_entry.insert(0, password)
            self.remember_me_var.set(True)

    def run(self):
        self.window.mainloop()
