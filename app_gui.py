import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from util import validar_datos
from retencionesICA import insertarRetencionesICA
from retencionesIVA import insertarRetencionesIVA
import pandas as pd
import time

class AppGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gestión de Retenciones")
        self.window.geometry("900x700")
        self.window.minsize(700, 500)
        self.theme_dark = False  # Default theme: light

        # Apply the initial theme
        self.apply_theme()

        # Global variables
        self.ruta_ica = None
        self.ruta_iva = None
        self.datos_ica = None
        self.datos_iva = None

        # Create GUI components
        self.create_menu()
        self.create_widgets()
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

    def create_menu(self):
        # Create menu bar
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        # Create "Options" menu
        opciones_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Opciones", menu=opciones_menu)

        # Add "Change Theme" option
        opciones_menu.add_command(label="Cambiar Tema", command=self.toggle_theme)

    def toggle_theme(self):
        self.theme_dark = not self.theme_dark
        self.apply_theme()

    def apply_theme(self):
        if self.theme_dark:
            bg_color = "#333333"
            fg_color = "#ffffff"
            btn_bg_color = "#555555"
        else:
            bg_color = "#f4f4f4"
            fg_color = "#000000"
            btn_bg_color = "SystemButtonFace"

        # Update the window background
        self.window.configure(bg=bg_color)

        # Update button and label styles
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=btn_bg_color, fg=fg_color)
            elif isinstance(widget, tk.Label):
                widget.config(bg=bg_color, fg=fg_color)

    def create_widgets(self):
        # Label for preview
        self.label_preview = tk.Label(self.window, text="Previsualización de los datos:", font=("Arial", 12))
        self.label_preview.pack(pady=5)

        # Treeview for data preview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#f4f4f4", foreground="#000000")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#d9d9d9", foreground="#000000")

        frame_treeview = tk.Frame(self.window)
        frame_treeview.pack(pady=5, fill="both", expand=True)

        scroll_x = tk.Scrollbar(frame_treeview, orient="horizontal")
        scroll_y = tk.Scrollbar(frame_treeview, orient="vertical")
        self.tree_previsualizacion = ttk.Treeview(
            frame_treeview, height=15, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )
        scroll_x.config(command=self.tree_previsualizacion.xview)
        scroll_y.config(command=self.tree_previsualizacion.yview)
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        self.tree_previsualizacion.pack(side="left", fill="both", expand=True)

        # Combobox for selecting datasets
        self.combo_opciones = ttk.Combobox(
            self.window, state="readonly", values=["Retenciones ICA", "Retenciones IVA"], font=("Arial", 10)
        )
        self.combo_opciones.set("Retenciones ICA")
        self.combo_opciones.pack(pady=5)
        self.combo_opciones.bind("<<ComboboxSelected>>", lambda e: self.actualizar_opciones())

        # Buttons
        self.btn_procesar_ica = self.create_hover_button("Seleccionar Retenciones ICA", self.procesar_ica)
        self.btn_insertar_ica = self.create_hover_button("Insertar Retenciones ICA", self.insertar_ica, state="disabled")
        self.btn_procesar_iva = self.create_hover_button("Seleccionar Retenciones IVA", self.procesar_iva)
        self.btn_insertar_iva = self.create_hover_button("Insertar Retenciones IVA", self.insertar_iva, state="disabled")
        self.btn_salir = self.create_hover_button("Salir", self.window.quit)

        # Pack buttons
        self.btn_procesar_ica.pack(pady=5)
        self.btn_insertar_ica.pack(pady=5)
        self.btn_procesar_iva.pack(pady=5)
        self.btn_insertar_iva.pack(pady=5)
        self.btn_salir.pack(pady=5)

    def create_hover_button(self, text, command, state="normal"):
        button = tk.Button(self.window, text=text, command=command, width=30, state=state)
        button.bind("<Enter>", lambda e: button.config(bg="#d9d9d9"))
        button.bind("<Leave>", lambda e: button.config(bg="SystemButtonFace"))
        return button

    def procesar_ica(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if ruta:
            self.ruta_ica = ruta
            datos_excel = pd.read_excel(ruta)
            filas_validas, errores = validar_datos(datos_excel)

            if errores:
                self.mostrar_errores(errores)
                self.btn_insertar_ica.config(state="disabled")
            else:
                self.datos_ica = filas_validas
                self.mostrar_previsualizacion(self.datos_ica)
                self.btn_insertar_ica.config(state="normal")

    def procesar_iva(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if ruta:
            self.ruta_iva = ruta
            datos_excel = pd.read_excel(ruta)
            filas_validas, errores = validar_datos(datos_excel)

            if errores:
                self.mostrar_errores(errores)
                self.btn_insertar_iva.config(state="disabled")
            else:
                self.datos_iva = filas_validas
                self.mostrar_previsualizacion(self.datos_iva)
                self.btn_insertar_iva.config(state="normal")

    def insertar_ica(self):
        if self.ruta_ica and self.datos_ica is not None:
            self.show_progress()
            insertarRetencionesICA(self.datos_ica)
            messagebox.showinfo("Éxito", "Datos insertados correctamente en retencionesICA.")
            self.btn_insertar_ica.config(state="disabled")

    def insertar_iva(self):
        if self.ruta_iva and self.datos_iva is not None:
            self.show_progress()
            insertarRetencionesIVA(self.datos_iva)
            messagebox.showinfo("Éxito", "Datos insertados correctamente en retencionesIVA.")
            self.btn_insertar_iva.config(state="disabled")

    def show_progress(self):
        for i in range(101):
            time.sleep(0.02)  # Simulate processing delay
            self.progress_bar["value"] = i
            self.window.update_idletasks()
        self.progress_bar["value"] = 0

    def mostrar_errores(self, errores):
        errores_str = "\n".join(
            [f"Fila {err['indice_fila']}: {', '.join([f'{k}: {v}' for k, v in err.items() if k != 'indice_fila'])}" for err in errores]
        )
        messagebox.showerror("Errores de Validación", errores_str)

    def mostrar_previsualizacion(self, datos_excel):
        self.tree_previsualizacion.delete(*self.tree_previsualizacion.get_children())
        self.tree_previsualizacion["column"] = list(datos_excel.columns)
        self.tree_previsualizacion["show"] = "headings"
        for columna in datos_excel.columns:
            self.tree_previsualizacion.heading(columna, text=columna)
            self.tree_previsualizacion.column(columna, width=120)
        for _, fila in datos_excel.iterrows():
            self.tree_previsualizacion.insert("", "end", values=list(fila))

    def actualizar_opciones(self):
        opcion = self.combo_opciones.get()
        if opcion == "Retenciones ICA" and self.datos_ica is not None:
            self.mostrar_previsualizacion(self.datos_ica)
        elif opcion == "Retenciones IVA" and self.datos_iva is not None:
            self.mostrar_previsualizacion(self.datos_iva)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = AppGUI()
    app.run()
