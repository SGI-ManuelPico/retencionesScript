from db import ConexionDB
import bcrypt
import datetime

db_config = {
    "host": "srv1182.hstgr.io",
    "user": "u438914854_contabilidad",
    "password": "RI8aiyvVRs4MY80",
    "database": "u438914854_contabilidad"
}

db = ConexionDB(**db_config)
conn = db.establecerConexion()


if conn:
    print("Conexion exitosa")
else:
    print("No se pudo establecer la conexion con la base de datos")