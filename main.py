import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from util import previsualizarDatos
from retencionesICA import insertarRetencionesICA
from retencionesIVA import insertarRetencionesIVA
import pandas as pd

# Variables globales
ruta_ica = None
ruta_iva = None
datos_ica = None
datos_iva = None

def seleccionar_archivo():
    return filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])

def mostrar_previsualizacion(datos_excel, tree_widget):
    tree_widget.delete(*tree_widget.get_children())
    tree_widget["column"] = list(datos_excel.columns)
    tree_widget["show"] = "headings"
    for columna in datos_excel.columns:
        tree_widget.heading(columna, text=columna)
        tree_widget.column(columna, width=120)
    for _, fila in datos_excel.iterrows():
        tree_widget.insert("", "end", values=list(fila))

def procesar_ica():
    global ruta_ica, datos_ica
    ruta = seleccionar_archivo()
    if ruta:
        ruta_ica = ruta
        datos_ica = pd.read_excel(ruta)
        mostrar_previsualizacion(datos_ica, tree_previsualizacion)
        combo_opciones.set("Retenciones ICA")
        actualizar_opciones()
        btn_insertar_ica.config(state="normal")

def procesar_iva():
    global ruta_iva, datos_iva
    ruta = seleccionar_archivo()
    if ruta:
        ruta_iva = ruta
        datos_iva = pd.read_excel(ruta)
        mostrar_previsualizacion(datos_iva, tree_previsualizacion)
        combo_opciones.set("Retenciones IVA")
        actualizar_opciones()
        btn_insertar_iva.config(state="normal")

def insertar_ica():
    global ruta_ica
    if ruta_ica:
        insertarRetencionesICA(ruta_ica)
        messagebox.showinfo("Éxito", "Datos insertados correctamente en retencionesICA.")
        btn_insertar_ica.config(state="disabled")

def insertar_iva():
    global ruta_iva
    if ruta_iva:
        insertarRetencionesIVA(ruta_iva)
        messagebox.showinfo("Éxito", "Datos insertados correctamente en retencionesIVA.")
        btn_insertar_iva.config(state="disabled")

def actualizar_opciones():
    opcion = combo_opciones.get()
    if opcion == "Retenciones ICA" and datos_ica is not None:
        mostrar_previsualizacion(datos_ica, tree_previsualizacion)
    elif opcion == "Retenciones IVA" and datos_iva is not None:
        mostrar_previsualizacion(datos_iva, tree_previsualizacion)

def estilizar_boton(boton):
    """Agregar efecto hover a un botón."""
    boton.bind("<Enter>", lambda e: boton.config(bg="#d9d9d9"))
    boton.bind("<Leave>", lambda e: boton.config(bg="SystemButtonFace"))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Retenciones")
ventana.geometry("900x700")  # Tamaño más grande por defecto
ventana.configure(bg="#f4f4f4")

# Crear estilo para el combobox
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#ffffff", background="#e6e6e6", foreground="#000000")

# Etiqueta de previsualización
label_previsualizacion = tk.Label(ventana, text="Previsualización de los datos:", bg="#f4f4f4", font=("Arial", 12))
label_previsualizacion.pack(pady=5)

# Frame del Treeview
frame_treeview = tk.Frame(ventana)
frame_treeview.pack(pady=5, fill="both", expand=True)

scroll_x = tk.Scrollbar(frame_treeview, orient="horizontal")
scroll_y = tk.Scrollbar(frame_treeview, orient="vertical")
tree_previsualizacion = ttk.Treeview(frame_treeview, height=15, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.config(command=tree_previsualizacion.xview)
scroll_y.config(command=tree_previsualizacion.yview)
scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
tree_previsualizacion.pack(side="left", fill="both", expand=True)

# Combobox
combo_opciones = ttk.Combobox(ventana, state="readonly", values=["Retenciones ICA", "Retenciones IVA"], font=("Arial", 10))
combo_opciones.set("Retenciones ICA")
combo_opciones.pack(pady=5)
combo_opciones.bind("<<ComboboxSelected>>", lambda e: actualizar_opciones())

# Crear los botones con estilos
btn_procesar_ica = tk.Button(ventana, text="Seleccionar Retenciones ICA", command=procesar_ica, width=30, font=("Arial", 10))
btn_insertar_ica = tk.Button(ventana, text="Insertar Retenciones ICA", command=insertar_ica, width=30, font=("Arial", 10), state="disabled")
btn_procesar_iva = tk.Button(ventana, text="Seleccionar Retenciones IVA", command=procesar_iva, width=30, font=("Arial", 10))
btn_insertar_iva = tk.Button(ventana, text="Insertar Retenciones IVA", command=insertar_iva, width=30, font=("Arial", 10), state="disabled")
btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit, width=30, font=("Arial", 10))

# Aplicar estilos hover
for boton in [btn_procesar_ica, btn_insertar_ica, btn_procesar_iva, btn_insertar_iva, btn_salir]:
    estilizar_boton(boton)

# Colocar los botones
btn_procesar_ica.pack(pady=5)
btn_insertar_ica.pack(pady=5)
btn_procesar_iva.pack(pady=5)
btn_insertar_iva.pack(pady=5)
btn_salir.pack(pady=5)

# Ejecutar la ventana
ventana.mainloop()
