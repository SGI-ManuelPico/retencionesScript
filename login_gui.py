import tkinter as tk
from tkinter import messagebox
from app_gui import AppGUI
from db import ConexionDB
import bcrypt
import os
from cryptography.fernet import Fernet
import json

class LoginGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("300x250")
        self.window.configure(bg="#f4f4f4")

        self.key = self.load_encryption_key()  # Load encryption key
        self.credentials_file = "credentials.json"

        # Load UI components
        self.create_widgets()
        self.check_remembered_credentials()

    def create_widgets(self):
        # Username Label and Entry
        tk.Label(self.window, text="Usuario:", bg="#f4f4f4", font=("Arial", 12)).pack(pady=10)
        self.username_entry = tk.Entry(self.window, font=("Arial", 12), width=25)
        self.username_entry.pack()

        # Password Label and Entry
        tk.Label(self.window, text="Contraseña:", bg="#f4f4f4", font=("Arial", 12)).pack(pady=10)
        self.password_entry = tk.Entry(self.window, show="*", font=("Arial", 12), width=25)
        self.password_entry.pack()

        # Remember Me Checkbox
        self.remember_me_var = tk.BooleanVar()
        tk.Checkbutton(
            self.window,
            text="Recuerdame",
            variable=self.remember_me_var,
            bg="#f4f4f4",
            font=("Arial", 10)
        ).pack(pady=10)

        # Login Button
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
            # Generate a new encryption key if not exists
            key = Fernet.generate_key()
            with open(key_file, "wb") as key_file:
                key_file.write(key)
        else:
            # Load the existing encryption key
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
            "password": "RI8aiyVVRs4MY80",
            "database": "u438914854_contabilidad"
        }
        db_config_test = {
            "host": "localhost",
            "user": "root",
            "password": "12345678",
            "database": "test"
        }
        conexion = ConexionDB(**db_config_test).establecerConexion()

        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor = conexion.cursor()
            query = "SELECT password FROM usuario WHERE correo = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                stored_hashed_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    if self.remember_me_var.get():
                        self.save_credentials(username, password)
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                    self.window.destroy()
                    AppGUI().run()
                else:
                    messagebox.showerror("Error", "Contraseña incorrecta")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar la base de datos: {e}")
        finally:
            conexion.close()

    def check_remembered_credentials(self):
        username, password = self.load_credentials()
        if username and password:
            self.username_entry.insert(0, username)
            self.password_entry.insert(0, password)
            self.remember_me_var.set(True)

    def run(self):
        self.window.mainloop()
