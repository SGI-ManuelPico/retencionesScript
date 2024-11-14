from cx_Freeze import setup, Executable

# Include additional files if necessary
include_files = []  # Add any files like Excel templates here, e.g., ["template.xlsx"]

# Dependencies
build_exe_options = {
    "packages": ["os", "pandas", "tkinter", "openpyxl", "tabulate", "mysql.connector"],
    "include_files": include_files,
    "excludes": ["matplotlib"],  # Exclude unnecessary libraries if not used
}

# Define the executable
target = Executable(
    script="main.py",  # Replace with your main script
    base="Win32GUI",  # Use "Win32GUI" to hide the console; omit this for a console app
    target_name="RetencionesApp.exe",  # Name of the output executable
)

# Setup
setup(
    name="RetencionesApp",
    version="1.0",
    description="Gestión de Retenciones",
    options={"build_exe": build_exe_options},
    executables=[target],
)
