import mysql.connector
import bcrypt
from cryptography.fernet import Fernet

import mysql.connector
import bcrypt
from cryptography.fernet import Fernet

def debug_decryption(username, password):
    # Database configuration
    db_config = {
        "host": "srv1182.hstgr.io",
        "user": "u438914854_contabilidad",
        "password": "RI8aiyvVRs4MY80",
        "database": "u438914854_contabilidad"
    }

    # Fernet key provided
    fernet_key = b"GJw2x2Dic6T3MWAv5a_vNDxkxJRjh04Ku4O_OtwBiNs="
    fernet = Fernet(fernet_key)

    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the encrypted password for the user
        query = "SELECT password FROM usuarios WHERE correo = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if not result:
            print(f"User '{username}' not found.")
            return

        encrypted_password = result[0]
        print(f"Encrypted password (from DB): {encrypted_password}")

        # Decrypt the password
        decrypted_password = fernet.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')
        print(f"Decrypted password: {decrypted_password}")

        # Compare directly with the user-provided password
        if password == decrypted_password:
            print("Password is correct.")
        else:
            print("Password is incorrect.")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


debug_decryption("jchavezmass@gmail.com", "SGI#1007229389@")