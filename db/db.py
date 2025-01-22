import mysql.connector
from mysql.connector import Error

class ConexionDB:
    """
    Clase para gestionar la conexión a bases de datos MySQL.
    """
    def __init__(self, host, user, password, database):
        """
        Inicializa los atributos necesarios para la conexión.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None

    def establecerConexion(self):
        """
        Establece la conexión a la base de datos.
        
        Returns:
            Objeto de conexión si es exitoso, None en caso de error.
        """
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.conexion
        except Error as e:
            print(f"Error al conectar con la base de datos {self.database}: {e}")
            return None

    def cerrarConexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.conexion:
            self.conexion.close()
