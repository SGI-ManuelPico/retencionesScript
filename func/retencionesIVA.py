import pandas as pd
from db.db import ConexionDB

class InsercionRetencionesIVA:
    def __init__(self, db_config):
        """
        Inicializa la clase con la configuración de la base de datos.
        Args:
            db_config (dict): Parámetros de configuración de la base de datos.
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

    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos y su cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    def obtener_registros_existentes(self):
        """
        Lee de la tabla retencionesiva todas las columnas (excepto 'id'),
        para detectar si hay filas duplicadas completas.
        
        Retorna un set con tuplas de la forma:
        (nit, detalle, ciudad, bimestre, year, montoOrigen, baseRetencion, valorRetenido, porcentaje)
        """
        query = """
            SELECT
                nit,
                detalle,
                ciudad,
                bimestre,
                year,
                montoOrigen,
                baseRetencion,
                valorRetenido,
                porcentaje
            FROM retencionesiva
        """
        self.cursor.execute(query)
        registros = self.cursor.fetchall()  # lista de tuplas
        
        # Convertimos a set para tener búsquedas rápidas
        return set(registros)

    def insertar_datos(self, ruta_excel):
        """
        Inserta datos desde un archivo Excel en la tabla retencionesiva,
        comparando TODAS las columnas para evitar duplicados completos.
        
        Args:
            ruta_excel (str): Ruta al archivo Excel que contiene los datos a insertar.
        
        Returns:
            bool: True si los datos se insertaron correctamente, False de lo contrario.
        """
        try:
            datos_excel = pd.read_excel(ruta_excel)
            datos_excel.fillna('', inplace=True)


            if not self.conectar():
                return False
            
            registros_existentes = self.obtener_registros_existentes()

            query = """
                INSERT INTO retencionesiva (
                    nit,
                    detalle,
                    ciudad,
                    bimestre,
                    year,
                    montoOrigen,
                    baseRetencion,
                    valorRetenido,
                    porcentaje
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores_a_insertar = []
            for _, fila in datos_excel.iterrows():
                clave = (
                    fila["nit_proveedor"],
                    fila["detalle"],
                    fila["ciudad"],
                    fila["bimestre"],
                    fila["anyo"],
                    fila["base_sometida"],
                    fila["valor_iva"],
                    fila["valor_retencion"],
                    fila["porcentaje"]
                )

                if clave in registros_existentes:
                    continue
                valores_a_insertar.append(clave)

            if not valores_a_insertar:
                print("No hay registros nuevos para insertar (todos eran duplicados).")
                return True

            self.cursor.executemany(query, valores_a_insertar)
            self.conexion.commit()
            print("Datos insertados correctamente en la tabla retencionesiva.")
            return True

        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            
            error_msg = str(e).lower()
            if "unknown column 'nan'" in error_msg:
                print("ERROR: Se está usando 'NaN' en una instrucción (probablemente SELECT en un trigger).")
            else:
                print("Error al insertar datos en retencionesiva:", e)
            
            return False

        finally:
            self.cerrar_conexion()




if __name__ == "__main__":
    db_config = {
        "host": "srv1182.hstgr.io",
        "user": "u438914854_contabilidad",
        "password": "RI8aiyvVRs4MY80",
        "database": "u438914854_contabilidad"
    }

    insercion = InsercionRetencionesIVA(db_config)
    if insercion.conectar():
        insercion.insertar_datos("RTE IVA 6 2024.xlsx")