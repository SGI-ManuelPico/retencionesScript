from util import previsualizarDatos
from retencionesICA import insertarRetencionesICA
from retencionesIVA import insertarRetencionesIVA

if __name__ == "__main__":
    while True:
        print("\nOpciones:")
        print("1. Previsualizar e insertar datos en retencionesICA")
        print("2. Previsualizar e insertar datos en retencionesIVA")
        print("3. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            ruta_ICA = input("Ingresa la ruta del archivo Excel para retencionesICA: ").strip()
            previsualizarDatos(ruta_ICA)
            confirmacion = input("¿Deseas insertar estos datos en la base de datos? (s/n): ").strip().lower()
            if confirmacion == "s":
                insertarRetencionesICA(ruta_ICA)
            else:
                print("Operación cancelada.")
        elif opcion == "2":
            ruta_IVA = input("Ingresa la ruta del archivo Excel para retencionesIVA: ").strip()
            previsualizarDatos(ruta_IVA)
            confirmacion = input("¿Deseas insertar estos datos en la base de datos? (s/n): ").strip().lower()
            if confirmacion == "s":
                insertarRetencionesIVA(ruta_IVA)
            else:
                print("Operación cancelada.")
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")