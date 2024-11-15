import pandas as pd
from db import ConexionDB
from util import validar_datos

class InsercionRetencionesICA:
    def __init__(self, db_config):
        """
        Inicializa la clase con la configuración de la base de datos.

        Args:
            db_config (dict): Diccionario con los parámetros de configuración de la base de datos.
        """
        self.db_config = db_config
        self.conexion = None
        self.cursor = None

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
        self.cursor = self.conexion.cursor()
        return True

    def cerrarConexion(self):
        """
        Cierra la conexión con la base de datos y su cursor.

        Returns:
            None
        """

        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

    def insertar_datos(self, ruta_excel):
        """
        Inserta datos desde un archivo Excel en la tabla retencionesica.
        
        Args:
            ruta_excel (str): Ruta al archivo Excel que contiene los datos a insertar.
        
        Returns:
            bool: True si los datos se insertaron correctamente, False de lo contrario.
        """
        try:
            datos_excel = pd.read_excel(ruta_excel)
            filas_validas, errores = validar_datos(datos_excel)

            if errores:
                print("Errores en los datos:")
                for error in errores:
                    print(error)
                return False  # Detener la inserción si hay errores en los datos

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
                self.cursor.execute(query, valores)

            self.conexion.commit()
            print("Datos insertados correctamente en la tabla retencionesica.")
            return True
        except Exception as e:
            print(f"Error al insertar datos en retencionesica: {e}")
            return False
        finally:
            self.cerrarConexion()
