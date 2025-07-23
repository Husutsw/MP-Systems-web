
# mp_demo.py - Sistema principal modular con configuracion inicial mejorada
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import importlib.util

class MPSystemsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MP-Systems - Sistema Contable Modular")
        self.geometry("900x600")
        self.nivel_usuario = "Administrador"
        self.modulos_dir = "modulos"

        self.formato_fecha = None
        self.simbolo_moneda = None
        self.empresa_actual = None

        self.check_vars = {}

        self.withdraw()  # OCULTAR VENTANA PRINCIPAL HASTA CONFIGURAR
        self.obtener_configuracion_inicial()

    def obtener_configuracion_inicial(self):
        color_fondo = "#f8e38c"
        ventana = tk.Toplevel()
        ventana.title("Configuracion Inicial")
        ventana.geometry("400x300")
        ventana.resizable(False, False)
        ventana.grab_set()  # BLOQUEAR VENTANA PRINCIPAL
        ventana.focus_force()

        tk.Label(ventana, text="Seleccione el formato de fecha:", font=("Arial", 10)).pack(pady=5)
        opciones_fecha = ["dd/mm/yyyy", "yyyy/mm/dd", "mm/dd/yyyy"]
        self.fecha_var = tk.StringVar()
        self.fecha_combo = ttk.Combobox(ventana, values=opciones_fecha, textvariable=self.fecha_var, state="readonly")
        self.fecha_combo.set(opciones_fecha[0])
        self.fecha_combo.pack()

        tk.Label(ventana, text="Seleccione el simbolo de moneda:", font=("Arial", 10)).pack(pady=10)
        opciones_moneda = ["RD$", "US$", "EUR$", "Otros"]
        self.moneda_var = tk.StringVar()
        self.moneda_combo = ttk.Combobox(ventana, values=opciones_moneda, textvariable=self.moneda_var, state="readonly")
        self.moneda_combo.set(opciones_moneda[0])
        self.moneda_combo.pack()

        self.entry_otro_moneda = tk.Entry(ventana, state="disabled", bg=color_fondo)
        self.entry_otro_moneda.pack(pady=5)

        def activar_otro(event):
            if self.moneda_combo.get() == "Otros":
                self.entry_otro_moneda.config(state="normal")
            else:
                self.entry_otro_moneda.delete(0, tk.END)
                self.entry_otro_moneda.config(state="disabled")

        self.moneda_combo.bind("<<ComboboxSelected>>", activar_otro)

        tk.Label(ventana, text="Nombre de la empresa:", font=("Arial", 10)).pack(pady=5)
        self.empresa_var = tk.Entry(ventana, bg=color_fondo)
        self.empresa_var.pack()

        def guardar_configuracion():
            self.formato_fecha = self.fecha_var.get()
            self.simbolo_moneda = self.entry_otro_moneda.get().strip() if self.moneda_var.get() == "Otros" else self.moneda_var.get()
            self.empresa_actual = self.empresa_var.get().strip() if self.empresa_var.get().strip() else "Empresa Desconocida"

            if not self.formato_fecha or not self.simbolo_moneda:
                messagebox.showwarning("Faltan datos", "Debe seleccionar formato de fecha y moneda.")
                return
            ventana.destroy()
            self.deiconify()
            self.cargar_interfaz_principal()

        tk.Button(ventana, text="Continuar", command=guardar_configuracion).pack(pady=15)

    def cargar_interfaz_principal(self):
        self.modulos_disponibles = self.detectar_modulos()
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20)
        self.crear_interfaz()

    def detectar_modulos(self):
        modulos = {}
        for filename in os.listdir(self.modulos_dir):
            if filename.startswith("modulo_") and filename.endswith(".py"):
                nombre = filename.replace("modulo_", "").replace(".py", "").replace("_", " ").title()
                modulos[filename] = nombre
        return modulos

    def crear_interfaz(self):
        tk.Label(self.main_frame, text="Seleccione los Modulos a Instalar", font=("Arial", 14)).pack(pady=10)

        for filename, nombre in self.modulos_disponibles.items():
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.main_frame, text=nombre, variable=var, font=("Arial", 12))
            chk.pack(anchor="w")
            self.check_vars[filename] = var

        tk.Button(self.main_frame, text="Instalar Modulos Seleccionados", font=("Arial", 12, "bold"),
                  command=self.instalar_modulos).pack(pady=15)

    def instalar_modulos(self):
        seleccionados = [f for f, v in self.check_vars.items() if v.get()]
        if not seleccionados:
            messagebox.showwarning("Aviso", "Debe seleccionar al menos un modulo.")
            return

        for archivo in seleccionados:
            ruta = os.path.join(self.modulos_dir, archivo)
            nombre_modulo = archivo.replace(".py", "")
            spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            if hasattr(modulo, "ejecutar_modulo"):
                modulo.ejecutar_modulo(self)

        aviso = tk.Toplevel(self)
        aviso.title("Instalacion")
        ancho = 300
        alto = 100
        x = int((self.winfo_screenwidth() - ancho) / 2)
        y = int((self.winfo_screenheight() - alto) / 2)
        aviso.geometry(f"{ancho}x{alto}+{x}+{y}")
        aviso.attributes("-topmost", True)
        aviso.transient(self)
        aviso.grab_set()
        tk.Label(aviso, text="Modulos instalados correctamente.", font=("Arial", 11)).pack(expand=True, pady=20)
        def cerrar_aviso(event=None):
            aviso.destroy()
        aviso.bind("<Button-1>", cerrar_aviso)

if __name__ == "__main__":
    app = MPSystemsApp()
    app.mainloop()
