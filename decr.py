from cryptography.fernet import Fernet

# Rutas de los archivos
ruta_clave = "audit_key.key"
ruta_log_cifrado = "audit_log.txt"
ruta_log_descifrado = "audit_log_legible.txt"

def descifrar_y_guardar_log():
    """
    Descifra el contenido del log y lo guarda en un archivo legible con el encoding adecuado.
    """
    try:
        # Leer la clave de cifrado
        with open(ruta_clave, "rb") as archivo_clave:
            clave = archivo_clave.read()
    except FileNotFoundError:
        print("El archivo de clave no se encontró.")
        return

    fernet = Fernet(clave)

    try:
        # Leer el contenido cifrado del log
        with open(ruta_log_cifrado, "rb") as archivo_log:
            contenido_cifrado = archivo_log.read()

        # Descifrar el contenido
        contenido_descifrado = fernet.decrypt(contenido_cifrado).decode("utf-8-sig")
        print("Contenido del log descifrado:")
        print(contenido_descifrado)

        # Guardar el contenido descifrado en un archivo legible
        with open(ruta_log_descifrado, "w", encoding="utf-8-sig") as archivo_legible:
            archivo_legible.write(contenido_descifrado)

        print(f"El log descifrado se guardó en '{ruta_log_descifrado}'.")
    except FileNotFoundError:
        print("El archivo de log cifrado no se encontró.")
    except Exception as e:
        print(f"Error al descifrar el contenido: {e}")

# Ejecutar la función
descifrar_y_guardar_log()
