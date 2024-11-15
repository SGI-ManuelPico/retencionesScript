import pandas as pd
from db import ConexionDB
import numpy as np
from util import validar_datos

def insertarRetencionesIVA(ruta_excel):
    """
    Función para insertar datos desde un archivo Excel en la tabla retencionesiva.
    
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

    db = ConexionDB(**db1_config)
    conexion = db.establecerConexion()

    if not conexion:
        print("No se pudo establecer conexión con la base de datos.")
        return

    try:
        datos_excel = pd.read_excel(ruta_excel)

        # Validar los datos antes de insertarlos en la base de datos
        filas_validas, errores = validar_datos(datos_excel)

        if errores:
            print("Errores encontrados en los datos:")
            for error in errores:
                print(error)
            return False # Detener la inserción si hay errores

        # Insertar los datos validados en la base de datos
        cursor = conexion.cursor()
        query = """
            INSERT INTO retencionesiva (nit, detalle, ciudad, bimestre, year, montoOrigen, baseRetencion, valorRetenido, porcentaje)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, fila in filas_validas.iterrows():
            
            valores = tuple(
                None if pd.isna(fila[col]) else fila[col]
                for col in [
                    "nit_proveedor",
                    "detalle",
                    "ciudad",
                    "bimestre",
                    "anyo",
                    "base_sometida",
                    "valor_iva",
                    "valor_retencion",
                    "porcentaje",
                ]
            )
            cursor.execute(query, valores)

        conexion.commit()
        print("Datos insertados correctamente en la tabla retencionesiva.")
    except Exception as e:
        print(f"Error al insertar datos en retencionesiva: {e}")
    finally:
        cursor.close()
        db.cerrarConexion()
