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

    def insertar_datos(self, ruta_excel):
        """
        Inserta datos desde un archivo Excel en la tabla retencionesiva.
        
        Args:
            ruta_excel (str): Ruta al archivo Excel que contiene los datos a insertar.
        
        Returns:
            bool: True si los datos se insertaron correctamente, False de lo contrario.
        """
        try:
            # 1. Leer datos del Excel
            datos_excel = pd.read_excel(ruta_excel)

            # 2. Reemplazar NaN por '' para evitar que aparezca 'nan' en consultas
            datos_excel.fillna('', inplace=True)

            # 3. Verificar/conectar a la base de datos
            if not self.conectar():
                return False

            # 4. Preparar la instrucción INSERT (sin incluir 'id', que es autoincrement)
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

            # 5. Crear la lista de valores según columnas del Excel
            # Ajusta estos nombres según tu archivo (encabezados)
            valores = []
            for _, fila in datos_excel.iterrows():
                fila_valores = (
                    fila["nit_proveedor"],    # nit
                    fila["detalle"],          # detalle
                    fila["ciudad"],           # ciudad
                    fila["bimestre"],         # bimestre
                    fila["anyo"],             # year
                    fila["base_sometida"],    # montoOrigen
                    fila["valor_iva"],        # baseRetencion
                    fila["valor_retencion"],  # valorRetenido
                    fila["porcentaje"]        # porcentaje
                )
                valores.append(fila_valores)

            # 6. Ejecutar inserción en lotes (más eficiente que un bucle con execute)
            self.cursor.executemany(query, valores)

            # 7. Confirmar la transacción
            self.conexion.commit()
            print("Datos insertados correctamente en la tabla retencionesiva.")
            return True

        except Exception as e:
            # Si algo falla, revertimos cualquier inserción parcial
            if self.conexion:
                self.conexion.rollback()
            
            error_msg = str(e).lower()
            if "unknown column 'nan'" in error_msg:
                print("ERROR: Se está usando 'NaN' en una instrucción (probablemente SELECT en un trigger).")
            else:
                print("Error al insertar datos en retencionesiva:", e)
            
            return False

        finally:
            # Cerrar siempre la conexión y el cursor, ocurra o no un error
            self.cerrar_conexion()


# if __name__ == "__main__":
#     # Ejemplo de uso
#     db_config = {
#         "host": "srv1182.hstgr.io",
#         "user": "u438914854_contabilidad",
#         "password": "RI8aiyvVRs4MY80",
#         "database": "u438914854_contabilidad"
#     }

#     insercion = InsercionRetencionesIVA(db_config)
#     if insercion.conectar():
#         insercion.insertar_datos("RTE IVA 6 2024.xlsx")