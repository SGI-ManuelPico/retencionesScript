import pandas as pd
from db import ConexionDB
from util import validar_datos

class InsercionRetencionesIVA:
    def __init__(self, db_config):
        """
        Inicializa la clase con la configuración de la base de datos.
        
        Args:
            db_config (dict): Diccionario con los parámetros de configuración de la base de datos.
        """
        self.db_config = db_config
        self.conexion = None

    def conectar(self):
        """
        Establece una conexión con la base de datos.
        
        Returns:
            bool: True si la conexión fue exitosa, False de lo contrario.
        """
        db = ConexionDB(**self.db_config)
        self.conexion = db.establecerConexion()
        if not self.conexion:
            print("No se pudo establecer conexión con la base de datos.")
            return False
        return True

    def insertar_datos(self, ruta_excel):
        """
        Inserta datos desde un archivo Excel en la tabla retencionesiva.
        
        Args:
            ruta_excel (str): Ruta al archivo Excel que contiene los datos a insertar.
        
        Returns:
            bool: True si los datos se insertaron correctamente, False de lo contrario.
        """
        if not self.conexion:
            print("No hay conexión activa con la base de datos.")
            return False

        try:
            datos_excel = pd.read_excel(ruta_excel)

            # Validar los datos antes de insertarlos en la base de datos
            filas_validas, errores = validar_datos(datos_excel)

            if errores:
                print("Errores encontrados en los datos:")
                for error in errores:
                    print(error)
                return False  # Detener la inserción si hay errores

            # Insertar los datos validados en la base de datos
            cursor = self.conexion.cursor()
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

            self.conexion.commit()
            print("Datos insertados correctamente en la tabla retencionesiva.")
            return True

        except Exception as e:
            print(f"Error al insertar datos en retencionesiva: {e}")
            return False

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()

    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")
