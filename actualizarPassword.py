from db import ConexionDB
import bcrypt

db_config = {
    "host": "srv1182.hstgr.io",
    "user": "u438914854_contabilidad",
    "password": "RI8aiyvVRs4MY80",
    "database": "u438914854_contabilidad"
}

db = ConexionDB(**db_config)
conn = db.establecerConexion()
cursor = conn.cursor()

def actualizar_password(nit, nuevo_password):
    try:
        # Genera el hash y lo decodifica a string
        hashed_password = bcrypt.hashpw(nuevo_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Asegúrate que la columna sea la correcta (nit o id)
        query = "UPDATE proveedor SET password = %s WHERE id = %s"
        cursor.execute(query, (hashed_password, nit))
        conn.commit()
        print("Contraseña actualizada correctamente.")
    except Exception as e:
        conn.rollback()
        print("Error al actualizar la contraseña:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    nit = 844003380
    nuevo_password = '844003380'
    actualizar_password(nit, nuevo_password)
