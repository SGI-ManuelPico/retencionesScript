from cx_Freeze import setup, Executable

include_files = [] 

# Dependencias
build_exe_options = {
    "packages": ["os", "pandas", "tkinter", "openpyxl", "tabulate", "mysql.connector"],
    "include_files": include_files,
    "excludes": ["matplotlib"],  
}

# Definir el ejecutable
target = Executable(
    script="main.py", 
    base="Win32GUI",  
    target_name="RetencionesApp.exe", 
)

# Configuración
setup(
    name="RetencionesApp",
    version="1.0",
    description="Gestión de Retenciones",
    options={"build_exe": build_exe_options},
    executables=[target],
)
