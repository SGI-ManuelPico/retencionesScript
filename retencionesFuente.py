import pandas as pd
from db import ConexionDB

class InsercionRetencionesFuente:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conexion = None
        self.cursor = None

    def conectar(self):
        db = ConexionDB(**self.db_config)
        self.conexion = db.establecerConexion()
        if not self.conexion:
            print("No se pudo establecer conexión con la base de datos.")
            return False
        self.cursor = self.conexion.cursor()
        return True

    def cerrarConexion(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    def obtenerRegistrosExistentes(self):
        """
        Obtiene de la tabla retencionesfuente todas las columnas 
        para comparar y detectar duplicados (sin incluir 'id').
        """
        consulta = """
            SELECT
                nit,
                detalle,
                ciudad,
                year,
                montoOrigen,
                valorRetenido,
                porcentaje
            FROM retencionesfuente
        """
        self.cursor.execute(consulta)
        registros = self.cursor.fetchall()  # Lista de tuplas
        return set(registros)

    def insertarDatos(self, ruta_excel):
        try:
            datos_excel = pd.read_excel(ruta_excel)
            # Rellenar celdas vacías con cadena vacía (o 0 según tus necesidades)
            datos_excel.fillna('', inplace=True)

            if not self.conectar():
                return False
            
            registros_existentes = self.obtenerRegistrosExistentes()

            query = """
                INSERT INTO retencionesfuente (
                    nit,
                    detalle,
                    ciudad,
                    year,
                    montoOrigen,
                    valorRetenido,
                    porcentaje
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            valores_a_insertar = []
            for _, fila in datos_excel.iterrows():
                # Ajusta los nombres de columna a lo que venga en tu Excel:
                clave = (
                    fila["nit_proveedor"],     # nit
                    fila["detalle"],           # detalle
                    fila["ciudad"],            # ciudad
                    fila["anyo"],              # year
                    fila["base_sometida"],     # montoOrigen
                    fila["valor_retencion"],   # valorRetenido
                    fila["porcentaje"]         # porcentaje
                )

                # Evitamos insertar si ya existe exactamente este registro
                if clave in registros_existentes:
                    continue

                valores_a_insertar.append(clave)

            if not valores_a_insertar:
                print("No hay registros nuevos para insertar (todos eran duplicados).")
                return True

            self.cursor.executemany(query, valores_a_insertar)
            self.conexion.commit()
            print("Datos insertados correctamente en la tabla retencionesfuente.")
            return True

        except Exception as e:
            if self.conexion:
                self.conexion.rollback()
            print("Error al insertar datos en retencionesfuente:", e)
            return False

        finally:
            self.cerrarConexion()


if __name__ == "__main__":
    db_config = {
        "host": "srv1182.hstgr.io",
        "user": "u438914854_contabilidad",
        "password": "RI8aiyvVRs4MY80",
        "database": "u438914854_contabilidad"
    }

    insercion = InsercionRetencionesFuente(db_config)
    insercion.insertarDatos("RTEFUENTE  AÑO  2024.xlsx")
