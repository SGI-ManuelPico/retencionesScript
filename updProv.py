from db import ConexionDB
import bcrypt
import datetime

db_config = {
    "host": "srv1182.hstgr.io",
    "user": "u438914854_contabilidad",
    "password": "RI8aiyvVRs4MY80",
    "database": "u438914854_contabilidad"
}

def asignar_password_proveedores_sin_correo_generar_txt():
    db = ConexionDB(**db_config)
    conn = db.establecerConexion()
    cursor = conn.cursor()
    
    try:
        # 1. Obtener todos los proveedores sin correo (NULL o vacío).
        #    Incluye el nombre si está disponible en tu esquema.
        query_select = """
            SELECT id, razonSocial
            FROM proveedor
            WHERE correoElectronico IS NULL
               OR correoElectronico = ''
        """
        cursor.execute(query_select)
        rows = cursor.fetchall()
        
        # Lista para llevar el registro de los proveedores actualizados
        proveedores_actualizados = []
        
        # 2. Para cada proveedor, asignarle como contraseña su propio 'id'.
        for (nit, nombre) in rows:
            # Convertir el nit a string y encriptarlo con bcrypt
            hashed_password = bcrypt.hashpw(str(nit).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            query_update = """
                UPDATE proveedor
                SET password = %s
                WHERE id = %s
            """
            cursor.execute(query_update, (hashed_password, nit))
            
            # Agregar a la lista (id, nombre) del proveedor actualizado
            proveedores_actualizados.append((nit, nombre))
        
        # 3. Confirmar cambios
        conn.commit()
        print("Contraseñas actualizadas correctamente para proveedores sin correo.")
        
        # 4. Generar el archivo .txt con la lista de proveedores actualizados
        #    Usamos fecha/hora para que el archivo no se sobrescriba cada vez.
        fecha_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"proveedores_actualizados_{fecha_hora}.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write("ID\tNOMBRE\n")
            for (id_prov, nom_prov) in proveedores_actualizados:
                # Si `nom_prov` pudiera ser None, podrías hacer nom_prov or '' para evitar errores
                f.write(f"{id_prov}\t{nom_prov if nom_prov else ''}\n")
        
        print(f"Se generó el archivo: {nombre_archivo}")
    
    except Exception as e:
        conn.rollback()
        print("Error durante la actualización:", e)
    
    finally:
        cursor.close()
        conn.close()

# Ejecución directa de la función
if __name__ == "__main__":
    asignar_password_proveedores_sin_correo_generar_txt()
