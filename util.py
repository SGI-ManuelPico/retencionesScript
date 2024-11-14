from tabulate import tabulate
import pandas as pd

def previsualizarDatos(ruta_excel):
    """
    Función para previsualizar los datos del archivo Excel antes de insertarlos en la base de datos.
    
    Args:
        ruta_excel (str): Ruta al archivo Excel que contiene los datos a insertar.
    """
    try:
        # Cargar el archivo Excel
        datos_excel = pd.read_excel(ruta_excel)
        # Mostrar una previsualización de los primeros registros
        print("Previsualización de los datos:")
        print(tabulate(datos_excel.head(10), headers="keys", tablefmt="grid"))  # Mostrar las primeras 10 filas
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")