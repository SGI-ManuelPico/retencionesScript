from cx_Freeze import setup, Executable

# Archivos adicionales necesarios
include_files = [
    "audit_key.key", 
    "audit_log.txt", 
    "credentials.json", 
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
    "excludes": ["matplotlib"],  
}

# Configuración del ejecutable
target = Executable(
    script="main.py", 
    base="Win32GUI",  
    target_name="RetencionesApp.exe", 
    icon=None,  
)

# Configuración de setup
setup(
    name="RetencionesApp",
    version="1.0",
    description="Gestión de Retenciones",
    options={"build_exe": build_exe_options},
    executables=[target],
)
