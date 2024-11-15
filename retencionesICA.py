import pandas as pd
from db import ConexionDB
from util import validar_datos

def insertarRetencionesICA(ruta_excel):
    """
    Función para insertar datos desde un archivo Excel en la tabla retencionesica.
    
    Args:
        ruta_excel (str): Ruta al archivo Excel que contiene los datos a insertar.
    """
    # Configuración de conexión a la base de datos
    db1_config = {
        "host": "localhost",
        "user": "root",
        "password": "12345678",
        "database": "test2"
    }


    # db1_config = {
    #     "host": "srv1182.hstgr.io",
    #     "user": "u438914854_contabilidad",
    #     "password": "RI8aiyvVRs4MY80",
    #     "database": "u438914854_contabilidad"
    # }

    # Crear conexión
    db = ConexionDB(**db1_config)
    conexion = db.establecerConexion()

    if not conexion:
        print("No se pudo establecer conexión con la base de datos.")
        return

    try:
        datos_excel = pd.read_excel(ruta_excel)
        filas_validas, errores = validar_datos(datos_excel)
        
        if errores:
            print("Errores en los datos:")
            for error in errores:
                print(error)
            return False  # Detener la inserción si hay errores en los datos
        cursor = conexion.cursor()
        query = """
            INSERT INTO retencionesica (nit, detalle, ciudad, bimestre, year, montoOrigen, valorRetenido, porcentaje)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, fila in filas_validas.iterrows():
            valores = (
                fila["nit_proveedor"],
                fila["detalle"],
                fila["ciudad"],
                fila["bimestre"],
                fila["anyo"],
                fila["base_sometida"],
                fila["valor_retencion"],
                fila["porcentaje"]
            )
            cursor.execute(query, valores)

        conexion.commit()
        print("Datos insertados correctamente en la tabla retencionesica.")
    except Exception as e:
        print(f"Error al insertar datos en retencionesica: {e}")
    finally:
        cursor.close()
        db.cerrarConexion()
