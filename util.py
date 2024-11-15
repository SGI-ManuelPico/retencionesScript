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


def validar_datos(datos_excel):
    """
    Valida los datos antes de insertarlos en la base de datos.

    Args:
        datos_excel (DataFrame): DataFrame con los datos cargados desde el archivo Excel.

    Returns:
        tuple: DataFrame de filas válidas, lista de errores por fila.
    """
    errores = []
    filas_validas = []

    for idx, fila in datos_excel.iterrows():
        fila_error = {}

        # Validar 'nit_proveedor'
        if pd.isna(fila['nit_proveedor']):
            fila_error['nit_proveedor'] = "Falta valor"
        elif not isinstance(fila['nit_proveedor'], int):
            fila_error['nit_proveedor'] = "Debe ser un entero"

        # Validar 'bimestre'
        if pd.isna(fila['bimestre']):
            fila_error['bimestre'] = "Falta valor"
        elif not (1 <= fila['bimestre'] <= 6):
            fila_error['bimestre'] = "Debe estar entre 1 y 6"

        if not fila_error:
            filas_validas.append(fila)
        else:
            fila_error['indice_fila'] = idx
            errores.append(fila_error)

    filas_validas_df = pd.DataFrame(filas_validas)
    return filas_validas_df, errores
