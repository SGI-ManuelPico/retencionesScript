from cx_Freeze import setup, Executable
import os

# Archivos adicionales necesarios
include_files = [
    ("audit_key.key", "audit_key.key"),  # Explicit source and destination
    ("audit_log.txt", "audit_log.txt"),
    ("credentials.json", "credentials.json"),
]

# Dependencias y configuraciones
build_exe_options = {
    "packages": [
        "os",
        "pandas",
        "tkinter",
        "openpyxl",
        "tabulate",
        "mysql.connector",
        "bcrypt",
        "cryptography.fernet",
        "time",
    ],
    "include_files": include_files,
    "excludes": ["matplotlib"],  # Exclude unused dependencies
}

# Configuración del ejecutable
target = Executable(
    script="main.py",  # Entry-point script
    base="Win32GUI",  # For GUI apps on Windows
    target_name="RetencionesApp.exe",  # Desired executable name
    icon=None,  # Add an icon file here if you have one
)

# Configuración de setup
setup(
    name="RetencionesApp",
    version="1.0",
    description="Gestión de Retenciones",
    options={"build_exe": build_exe_options},
    executables=[target],
)
