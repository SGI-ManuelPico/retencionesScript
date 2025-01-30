import pandas as pd
from db import ConexionDB

class InsercionRetencionesICA:
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

    def cerrarConexion(self):
        """
        Cierra la conexión con la base de datos y su cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    def obtenerRegistrosExistentes(self):
        """
        Obtiene de la tabla retencionesica todas las columnas que consideramos
        para comparar y detectar duplicados (sin incluir 'id').
        
        Retorna un set de tuplas en el orden:
        (nit, detalle, ciudad, bimestre, year, montoOrigen, valorRetenido, porcentaje)
        """
        consulta = """
            SELECT
                nit,
                detalle,
                ciudad,
                bimestre,
                year,
                montoOrigen,
                valorRetenido,
                porcentaje
            FROM retencionesica
        """
        self.cursor.execute(consulta)
        registros = self.cursor.fetchall()  # Lista de tuplas
        
        return set(registros)

    def insertarDatos(self, ruta_excel):
        """
        Inserta datos desde un archivo Excel en la tabla retencionesica,
        evitando insertar filas duplicadas completas (todas las columnas).
        
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
            
            registros_existentes = self.obtenerRegistrosExistentes()

            query = """
                INSERT INTO retencionesica (
                    nit,
                    detalle,
                    ciudad,
                    bimestre,
                    year,
                    montoOrigen,
                    valorRetenido,
                    porcentaje
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores_a_insertar = []
            for _, fila in datos_excel.iterrows():
                # Crear tupla con las columnas en el mismo orden que el SELECT
                clave = (
                    fila["nit_proveedor"],    # nit
                    fila["detalle"],          # detalle
                    fila["ciudad"],           # ciudad
                    fila["bimestre"],         # bimestre
                    fila["anyo"],             # year
                    fila["base_sometida"],    # montoOrigen
                    fila["valor_retencion"],  # valorRetenido
                    fila["porcentaje"]        # porcentaje
                )
                if clave in registros_existentes:
                    continue

                valores_a_insertar.append(clave)
            if not valores_a_insertar:
                print("No hay registros nuevos para insertar (todos eran duplicados).")
                return True
            self.cursor.executemany(query, valores_a_insertar)
            self.conexion.commit()
            print("Datos insertados correctamente en la tabla retencionesica.")
            return True

        except Exception as e:
            # Si ocurre un error, revertimos la transacción
            if self.conexion:
                self.conexion.rollback()

            # Manejo de excepciones específicas
            error_msg = str(e).lower()
            if "unknown column 'nan'" in error_msg:
                print("ERROR: Se está usando 'NaN' en una consulta SELECT o similar (tal vez un trigger).")
            else:
                print("Error al insertar datos en retencionesica:", e)

            return False

        finally:
            self.cerrarConexion()


if __name__ == "__main__":
    # Ejemplo de uso
    db_config = {
        "host": "srv1182.hstgr.io",
        "user": "u438914854_contabilidad",
        "password": "RI8aiyvVRs4MY80",
        "database": "u438914854_contabilidad"
    }

    insercion = InsercionRetencionesICA(db_config)
    if insercion.conectar():
        insercion.insertarDatos("RTE ICA AÑO 2024.xlsx")